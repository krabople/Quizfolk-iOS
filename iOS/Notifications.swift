import SwiftUI
import UserNotifications
import UIKit

struct NotificationPreferences:Codable,Equatable {
    var enabled=false
    var challenges=true
    var duelResults=true
    var tournamentPrizes=true
    var friendsTournaments=true
    var dictionary:[String:Bool] { ["enabled":enabled,"challenges":challenges,"duelResults":duelResults,"tournamentPrizes":tournamentPrizes,"friendsTournaments":friendsTournaments] }
}
struct PushDelivery:Codable {var ios:Bool;var android:Bool}
struct NotificationSettingsReply:Codable {var preferences:NotificationPreferences;var delivery:PushDelivery}
struct PushDestination:Identifiable,Equatable {
    let kind:String;let id:String;let topicID:String?
    init?(_ data:[AnyHashable:Any]) {
        guard let kind=data["kind"] as? String,["challenges","duelResults","tournamentPrizes","friendsTournaments"].contains(kind),let id=data["id"] as? String,
              id.range(of:"^[A-Za-z0-9:-]{1,160}$",options:.regularExpression) != nil else{return nil}
        self.kind=kind;self.id=id;self.topicID=data["topicID"] as? String
    }
}
extension Notification.Name {
    static let quizfolkPushToken=Notification.Name("QuizfolkPushTokenChanged")
}
@MainActor final class PushCoordinator:ObservableObject {
    static let shared=PushCoordinator()
    @Published var destination:PushDestination?
    @Published var permission:UNAuthorizationStatus = .notDetermined
    @Published var registrationError:String?
    var token:String? {UserDefaults.standard.string(forKey:"pushDeviceToken")}
    var installation:String {
        if let id=UserDefaults.standard.string(forKey:"pushInstallation"){return id}
        let id=UUID().uuidString;UserDefaults.standard.set(id,forKey:"pushInstallation");return id
    }
    var allowed:Bool {permission == .authorized || permission == .provisional || permission == .ephemeral}
    func refresh() async {permission=await UNUserNotificationCenter.current().notificationSettings().authorizationStatus}
    func askPermission() async {
        do{_ = try await UNUserNotificationCenter.current().requestAuthorization(options:[.alert,.sound,.badge]);await refresh()}
        catch{registrationError="Notifications could not be enabled. Please try again."}
    }
    func receiveToken(_ data:Data) {
        let value=data.map{String(format:"%02x",$0)}.joined()
        UserDefaults.standard.set(value,forKey:"pushDeviceToken");registrationError=nil
        NotificationCenter.default.post(name:.quizfolkPushToken,object:nil)
    }
    nonisolated static func shouldPresent(_ data:[AnyHashable:Any])->Bool {
        guard let kind=data["kind"] as? String,let raw=UserDefaults.standard.data(forKey:"pushPreferences"),let prefs=try? JSONDecoder().decode(NotificationPreferences.self,from:raw) else{return false}
        return prefs.enabled && prefs.dictionary[kind]==true
    }
}
final class PushAppDelegate:NSObject,UIApplicationDelegate,UNUserNotificationCenterDelegate {
    func application(_ application:UIApplication,didFinishLaunchingWithOptions launchOptions:[UIApplication.LaunchOptionsKey:Any]?=nil)->Bool {
        UNUserNotificationCenter.current().delegate=self;return true
    }
    func application(_ application:UIApplication,didRegisterForRemoteNotificationsWithDeviceToken deviceToken:Data) {Task{@MainActor in PushCoordinator.shared.receiveToken(deviceToken)}}
    func application(_ application:UIApplication,didFailToRegisterForRemoteNotificationsWithError error:Error) {Task{@MainActor in PushCoordinator.shared.registrationError="This device could not connect to Apple notifications. Please try again later."}}
    func userNotificationCenter(_ center:UNUserNotificationCenter,willPresent notification:UNNotification,withCompletionHandler completionHandler:@escaping(UNNotificationPresentationOptions)->Void) {
        completionHandler(PushCoordinator.shouldPresent(notification.request.content.userInfo) ? [.banner,.sound]:[])
    }
    func userNotificationCenter(_ center:UNUserNotificationCenter,didReceive response:UNNotificationResponse,withCompletionHandler completionHandler:@escaping()->Void) {
        let destination=PushDestination(response.notification.request.content.userInfo)
        Task{@MainActor in PushCoordinator.shared.destination=destination};completionHandler()
    }
}
extension QuizStore {
    func clearClientNotifications() {
        guard !isUITesting else{return}
        UIApplication.shared.unregisterForRemoteNotifications()
        for key in ["pushPreferences","pushRegisteredEndpoint","pushDeviceToken"] {UserDefaults.standard.removeObject(forKey:key)}
        UNUserNotificationCenter.current().removeAllDeliveredNotifications()
    }
    func detachPreviousNotificationEndpoint() async throws {
        guard !isUITesting,let previous=UserDefaults.standard.string(forKey:"pushRegisteredEndpoint"),previous != apiURL,
              previous==UserDefaults.standard.string(forKey:"tokenEndpoint"),let key=Keychain.read() else{return}
        guard var parts=URLComponents(string:previous),parts.scheme=="https",parts.host != nil else{throw APIError.message("The previous notification connection is invalid.")}
        parts.queryItems=(parts.queryItems ?? [])+[URLQueryItem(name:"r",value:"notification-device")]
        guard let url=parts.url else{throw APIError.message("The previous notification connection is invalid.")}
        var request=URLRequest(url:url);request.httpMethod="POST";request.timeoutInterval=8
        request.setValue("Bearer \(key)",forHTTPHeaderField:"Authorization");request.setValue("application/json",forHTTPHeaderField:"Content-Type")
        request.httpBody=try JSONSerialization.data(withJSONObject:["installation":PushCoordinator.shared.installation,"platform":"ios","enabled":false])
        let (_,response)=try await URLSession.shared.data(for:request)
        guard let http=response as? HTTPURLResponse,(200..<300).contains(http.statusCode) else{throw APIError.message("Could not stop notifications from the previous connection. Please reconnect and try again.")}
        clearClientNotifications()
    }
    private var usingNotificationFixtures:Bool {
        #if DEBUG
        return isUITesting && testResponse==nil
        #else
        return false
        #endif
    }
    func loadNotificationSettings() async {
        if usingNotificationFixtures {notificationSettings=NotificationSettingsReply(preferences:notificationSettings.preferences,delivery:PushDelivery(ios:false,android:false));return}
        let generation=notificationGeneration
        do{let reply:NotificationSettingsReply=try await request("notification-settings");guard generation==notificationGeneration else{return};notificationSettings=reply;cacheNotificationChoices();notificationError=nil}
        catch{notificationError=error.localizedDescription}
    }
    func cacheNotificationChoices() {
        if let raw=try? JSONEncoder().encode(notificationSettings.preferences){UserDefaults.standard.set(raw,forKey:"pushPreferences")}
    }
    func syncNotificationDevice() async {
        guard !isUITesting,profile != nil else{return}
        await loadNotificationSettings();await PushCoordinator.shared.refresh()
        let push=PushCoordinator.shared
        if notificationSettings.preferences.enabled && notificationSettings.delivery.ios && push.allowed && push.token==nil {UIApplication.shared.registerForRemoteNotifications()}
        var body:[String:Any]=["installation":push.installation,"platform":"ios","enabled":false]
        if notificationSettings.preferences.enabled && notificationSettings.delivery.ios && push.allowed,let token=push.token {
            body["enabled"]=true;body["token"]=token
            #if DEBUG
            body["environment"]="sandbox"
            #else
            body["environment"]="production"
            #endif
        }
        do{
            let _:OKReply=try await request("notification-device",body:body)
            if body["enabled"] as? Bool == true {UserDefaults.standard.set(apiURL,forKey:"pushRegisteredEndpoint")}
            else if UserDefaults.standard.string(forKey:"pushRegisteredEndpoint")==apiURL {UserDefaults.standard.removeObject(forKey:"pushRegisteredEndpoint");UIApplication.shared.unregisterForRemoteNotifications();UserDefaults.standard.removeObject(forKey:"pushDeviceToken")}
        }catch{notificationError=error.localizedDescription}
    }
    func saveNotificationChoices(_ prefs:NotificationPreferences) async {
        guard !notificationBusy else{return};notificationGeneration+=1;notificationBusy=true;defer{notificationBusy=false}
        if usingNotificationFixtures {notificationSettings.preferences=prefs;cacheNotificationChoices();return}
        do {
            notificationSettings=try await request("notification-preferences",body:["preferences":prefs.dictionary]);cacheNotificationChoices();notificationError=nil
            if prefs.enabled && notificationSettings.delivery.ios && PushCoordinator.shared.permission == .notDetermined {await PushCoordinator.shared.askPermission()}
            await syncNotificationDevice()
        } catch{notificationError=error.localizedDescription}
    }
}
struct NotificationSettingsView:View {
    @EnvironmentObject var store:QuizStore
    @ObservedObject private var push=PushCoordinator.shared
    @Environment(\.openURL) private var openURL
    private func choice(_ key:WritableKeyPath<NotificationPreferences,Bool>)->Binding<Bool> {
        Binding(get:{store.notificationSettings.preferences[keyPath:key]},set:{value in var prefs=store.notificationSettings.preferences;prefs[keyPath:key]=value;Task{await store.saveNotificationChoices(prefs)}})
    }
    var body:some View {
        Form {
            Section {
                Toggle("Push notifications",isOn:choice(\.enabled)).accessibilityIdentifier("push-enabled")
                if !store.notificationSettings.delivery.ios {Text("Push delivery is not available yet. Your choices will be saved.").font(.footnote).foregroundStyle(.secondary).accessibilityIdentifier("push-unavailable")}
                else if push.permission == .denied {Text("Notifications are switched off in Settings. Your choices below are saved.").font(.footnote);Button("Open notification settings"){if let url=URL(string:UIApplication.openNotificationSettingsURLString){openURL(url)}}}
                else if store.notificationSettings.preferences.enabled && !push.allowed {Button("Allow notifications on this device"){Task{await push.askPermission();await store.syncNotificationDevice()}}}
            } footer:{Text("Choose what you hear about. You can switch everything off at any time.")}
            Section("Notify me about") {
                Toggle("New challenges",isOn:choice(\.challenges)).accessibilityIdentifier("push-challenges")
                Text("When another player challenges you to a duel.").font(.caption).foregroundStyle(.secondary)
                Toggle("Duel results",isOn:choice(\.duelResults)).accessibilityIdentifier("push-duelResults")
                Text("When both players finish and the result is decided.").font(.caption).foregroundStyle(.secondary)
                Toggle("Tournament prizes",isOn:choice(\.tournamentPrizes)).accessibilityIdentifier("push-tournamentPrizes")
                Text("Your final place, coin prize and badge after a tournament closes.").font(.caption).foregroundStyle(.secondary)
                Toggle("Friends tournaments",isOn:choice(\.friendsTournaments)).accessibilityIdentifier("push-friendsTournaments")
                Text("When a friends tournament starts or finishes.").font(.caption).foregroundStyle(.secondary)
            }
            if let error=store.notificationError {Section{Text(error).foregroundStyle(.red);Button("Try again"){Task{await store.loadNotificationSettings()}}}}
            if let error=push.registrationError {Section{Text(error).foregroundStyle(.secondary)}}
        }.disabled(store.notificationBusy).navigationTitle("Notifications").task{await store.loadNotificationSettings();if !store.isUITesting {await push.refresh()}}
    }
}
struct NotificationDestinationView:View {
    @EnvironmentObject var store:QuizStore
    let destination:PushDestination
    @State private var game:GameSession?
    @State private var tournament:TournamentBoard?
    @State private var friends:FriendsBoard?
    @State private var error:String?
    var body:some View {
        Group {
            if let game {GameView(game:game)}
            else if let tournament,let topic=store.topics.first(where:{$0.id==tournament.event.topicID}){TournamentDetailView(event:tournament.event,topic:topic)}
            else if let friends {FriendsTournamentView(room:friends.party)}
            else if let error {ContentUnavailableView("Couldn’t open notification",systemImage:"bell.slash",description:Text(error))}
            else {ProgressView("Opening…")}
        }.task(id:destination){
            await store.connect()
            do {
                switch destination.kind {
                case "challenges","duelResults":
                    let start=try await store.openChallenge(destination.id)
                    guard let topic=store.topics.first(where:{$0.id==destination.topicID}) else{throw APIError.message("This topic is no longer available.")}
                    game=GameSession(topic:topic,store:store,online:true,match:start)
                case "tournamentPrizes":tournament=try await store.request("tournament-board",query:[URLQueryItem(name:"event",value:destination.id)])
                case "friendsTournaments":friends=try await store.request("party-board",query:[URLQueryItem(name:"id",value:destination.id)])
                default:break
                }
            }catch{self.error=error.localizedDescription}
        }
    }
}
