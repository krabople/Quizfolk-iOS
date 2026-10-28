import Foundation
import SwiftUI
import Security

@MainActor final class QuizStore: ObservableObject {
    @Published var topics: [Topic] = []
    @Published var questions: [Question] = []
    @Published var favourites: Set<String> = []
    @Published var history: [MatchRecord] = []
    @Published var name = "Explorer-"+UUID().uuidString.replacingOccurrences(of:"-",with:"").prefix(10).uppercased()
    @Published var apiURL = "https://www.ways2earn.com/quizfolk-api/index.php"
    @Published var loadError: String?
    @Published var onlineError: String?
    @Published var profile: OnlineProfile?
    @Published var board: [BoardEntry] = []
    @Published var profileBusy=false
    @Published var avatar:String?
    @Published var people:[PlayerCard]=[]
    @Published var challenges:[ChallengeCard]=[]
    @Published var activity:[FriendActivity]=[]
    @Published var ownCard:PlayerCard?
    @Published var socialError:String?
    var testFollowing=false
    #if DEBUG
    var testResponse:((String,[String:Any]?) async throws -> Data)?
    #endif
    var isUITesting:Bool {
        #if DEBUG
        return ProcessInfo.processInfo.arguments.contains("--ui-testing") || ProcessInfo.processInfo.environment["XCTestConfigurationFilePath"] != nil
        #else
        return false
        #endif
    }
    private var token: String?
    private var connectionTask:Task<Void,Never>?
    private var boardRequest=UUID()
    var peopleRequest=UUID()
    init() {
        do {
            topics = try Self.resource("categories")
            questions = try Self.resource("questions")
        } catch { loadError = "The question bank could not be loaded: \(error.localizedDescription)" }
        favourites = Set(UserDefaults.standard.stringArray(forKey:"favourites") ?? [])
        name = UserDefaults.standard.string(forKey:"name") ?? name
        if name=="Quiz explorer" {name="Explorer-"+UUID().uuidString.replacingOccurrences(of:"-",with:"").prefix(10).uppercased()}
        UserDefaults.standard.set(name,forKey:"name")
        apiURL = UserDefaults.standard.string(forKey:"apiURL") ?? "https://www.ways2earn.com/quizfolk-api/index.php"
        if let data = UserDefaults.standard.data(forKey:"history"), let saved = try? JSONDecoder().decode([MatchRecord].self,from:data) { history=saved }
        if UserDefaults.standard.string(forKey:"tokenEndpoint")==apiURL { token = Keychain.read();avatar=UserDefaults.standard.string(forKey:"avatar") }
    }
    static func resource<T:Decodable>(_ name:String) throws -> T {
        guard let url=Bundle.main.url(forResource:name,withExtension:"json") else { throw CocoaError(.fileNoSuchFile) }
        return try JSONDecoder().decode(T.self,from:Data(contentsOf:url))
    }
    func toggle(_ topic:Topic) {
        if favourites.contains(topic.id) { favourites.remove(topic.id) } else { favourites.insert(topic.id) }
        UserDefaults.standard.set(Array(favourites),forKey:"favourites")
        if profile?.socialVersion==1 && !isUITesting {Task{try? await saveSocial(interests:Array(favourites))}}
    }
    func saveSettings() {
        UserDefaults.standard.set(apiURL,forKey:"apiURL")
    }
    func packet(_ topic:Topic) -> [Question] {
        let seen=Set(history.filter{$0.topicID==topic.id}.flatMap{$0.rounds.map{$0.question.id}})
        let bank=questions.filter{$0.categoryID==topic.id}
        let fresh=bank.filter{!seen.contains($0.id)}.shuffled()
        let extra=bank.filter{seen.contains($0.id)}.shuffled()
        return Array((fresh+extra).prefix(7)).map{$0.shuffled()}
    }
    func save(_ match:MatchRecord) {
        guard !history.contains(where:{$0.id==match.id}) else {return}
        history.insert(match,at:0)
        persistHistory()
    }
    func persistHistory() {if let data=try? JSONEncoder().encode(history){UserDefaults.standard.set(data,forKey:"history")}}
    var xp:Int { history.reduce(0){$0+$1.xp} }
    func topicXP(_ topic:Topic)->Int {
        if let ownCard {return ownCard.topics.first{$0.topicID==topic.id}?.xp ?? 0}
        return history.filter{$0.topicID==topic.id && $0.kind != "practice"}.reduce(0){$0+$1.xp}
    }
    func level(_ topic:Topic)->Int {1+topicXP(topic)/300}
    func request<T:Decodable>(_ route:String,body:[String:Any]?=nil,query:[URLQueryItem]=[]) async throws -> T {
        #if DEBUG
        if let testResponse {return try JSONDecoder().decode(T.self,from:await testResponse(route,body))}
        #endif
        if isUITesting {throw APIError.message("UI test network is disabled.")}
        guard var parts=URLComponents(string:apiURL),parts.scheme=="https",parts.host != nil else {throw APIError.message("Enter the deployed HTTPS API URL in your profile first.")}
        parts.queryItems=(parts.queryItems ?? [])+[URLQueryItem(name:"r",value:route)]+query
        guard let url=parts.url else {throw APIError.message("Invalid API URL")}
        var req=URLRequest(url:url);req.timeoutInterval=20
        req.setValue("3",forHTTPHeaderField:"X-Quizfolk-Client")
        if let token,UserDefaults.standard.string(forKey:"tokenEndpoint")==apiURL {req.setValue("Bearer \(token)",forHTTPHeaderField:"Authorization")}
        if let body {req.httpMethod="POST";req.setValue("application/json",forHTTPHeaderField:"Content-Type");req.httpBody=try JSONSerialization.data(withJSONObject:body)}
        let (data,response)=try await URLSession.shared.data(for:req)
        guard let http=response as? HTTPURLResponse,(200..<300).contains(http.statusCode) else {
            let failure=try? JSONDecoder().decode(Failure.self,from:data)
            throw APIError.message(failure?.error ?? "Server request failed. Please try again.")
        }
        return try JSONDecoder().decode(T.self,from:data)
    }
    func connect() async {
        if isUITesting {name="UI Player";profile=OnlineProfile(id:"test-self",socialVersion:1,name:name,avatar:nil,matches:0,wins:0,xp:0,correct:0,answered:0);ownCard=Self.testCard(following:false,own:true);return}
        if let running=connectionTask {await running.value;return}
        let running=Task {await self.performConnect()};connectionTask=running
        await running.value;connectionTask=nil
    }
    private func performConnect() async {
        profileBusy=true;defer{profileBusy=false}
        saveSettings();onlineError=nil
        if UserDefaults.standard.string(forKey:"tokenEndpoint") != apiURL {token=nil;profile=nil;avatar=nil;UserDefaults.standard.removeObject(forKey:"avatar")}
        do {
            if token==nil {
                let auth:AuthReply=try await request("register",body:["name":name,"automaticName":name.hasPrefix("Explorer-")])
                guard Keychain.save(auth.token) else {throw APIError.message("Could not securely save your account key.")}
                token=auth.token
                UserDefaults.standard.set(apiURL,forKey:"tokenEndpoint")
            }
            profile=try await request("profile")
            avatar=profile?.avatar
            UserDefaults.standard.set(avatar,forKey:"avatar")
            if let actual=profile?.name {name=actual;UserDefaults.standard.set(name,forKey:"name")}
            if profile?.socialVersion==1 {
                let _:OKReply=try await request("social-settings",body:["interests":Array(favourites)])
                ownCard=try await request("player")
            }
        } catch {onlineError=error.localizedDescription}
    }
    func changeName(to requested:String) async {
        onlineError=nil
        if profile==nil {await connect();if onlineError != nil {return}}
        profileBusy=true;defer{profileBusy=false}
        do {
            let response:NameReply=try await request("update-profile",body:["name":requested])
            name=response.name;UserDefaults.standard.set(name,forKey:"name")
            profile=try await request("profile")
        } catch {onlineError=error.localizedDescription}
    }
    func changeAvatar(_ data:Data?) async {
        onlineError=nil
        if profile==nil {await connect();if onlineError != nil {return}}
        profileBusy=true;defer{profileBusy=false}
        do {
            let value:Any = data == nil ? NSNull() : data!.base64EncodedString()
            let _:OKReply=try await request("update-avatar",body:["avatar":value])
            avatar=data?.base64EncodedString();UserDefaults.standard.set(avatar,forKey:"avatar")
            profile=try await request("profile")
        } catch {onlineError=error.localizedDescription}
    }
    func deleteAccount() async {
        onlineError=nil
        do {
            let _:OKReply=try await request("delete-account",body:[:])
            Keychain.delete();token=nil;profile=nil;board=[];avatar=nil;ownCard=nil;people=[];challenges=[];activity=[]
            UserDefaults.standard.removeObject(forKey:"tokenEndpoint");UserDefaults.standard.removeObject(forKey:"avatar")
        } catch {onlineError=error.localizedDescription}
    }
    func loadBoard(topicID:String,monthly:Bool=true,friendsOnly:Bool=false) async {
        let requestID=UUID();boardRequest=requestID;board=[]
        onlineError=nil
        if profile==nil {await connect();if onlineError != nil {return}}
        do { let response:BoardReply=try await request("leaderboard",query:[URLQueryItem(name:"topic",value:topicID),URLQueryItem(name:"period",value:monthly ? "month":"all"),URLQueryItem(name:"scope",value:friendsOnly ? "following":"all")])
            if boardRequest==requestID {board=response.entries}
        } catch {onlineError=error.localizedDescription}
    }
}
enum APIError: LocalizedError {
    case message(String)
    var errorDescription:String? {if case .message(let s)=self{return s};return nil}
}
struct Failure:Decodable {let error:String}
struct OKReply:Decodable {let ok:Bool}
struct NameReply:Decodable {let ok:Bool;let name:String}
struct AuthReply:Decodable {let token:String}
struct OnlineProfile:Decodable {var id:String? = nil;var socialVersion:Int? = nil;let name:String;let avatar:String?;let matches:Int;let wins:Int;let xp:Int;let correct:Int;let answered:Int}
struct BoardEntry:Decodable,Identifiable {let id:String;let name:String;let avatar:String?;let xp:Int;let matches:Int}
struct BoardReply:Decodable {let entries:[BoardEntry]}
enum Keychain {
    static let service="com.quizfolk.player"
    static func read()->String? {
        let q:[String:Any]=[kSecClass as String:kSecClassGenericPassword,kSecAttrService as String:service,kSecAttrAccount as String:"token",kSecReturnData as String:true,kSecMatchLimit as String:kSecMatchLimitOne]
        var item:CFTypeRef?
        guard SecItemCopyMatching(q as CFDictionary,&item)==errSecSuccess,let data=item as? Data else {return nil}
        return String(data:data,encoding:.utf8)
    }
    static func save(_ token:String)->Bool {
        let q:[String:Any]=[kSecClass as String:kSecClassGenericPassword,kSecAttrService as String:service,kSecAttrAccount as String:"token"]
        let attrs:[String:Any]=[kSecValueData as String:Data(token.utf8),kSecAttrAccessible as String:kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly]
        let status=SecItemUpdate(q as CFDictionary,attrs as CFDictionary)
        if status==errSecItemNotFound {return SecItemAdd(q.merging(attrs){_,new in new} as CFDictionary,nil)==errSecSuccess}
        return status==errSecSuccess
    }
    static func delete() {SecItemDelete([kSecClass as String:kSecClassGenericPassword,kSecAttrService as String:service,kSecAttrAccount as String:"token"] as CFDictionary)}
}
