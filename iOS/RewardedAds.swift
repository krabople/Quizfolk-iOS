import SwiftUI
import UIKit
import GoogleMobileAds
import UserMessagingPlatform

struct RewardedWallet:Decodable {let coins:Int}
struct RewardedAttempt:Decodable,Equatable {
    let id:String;let platform:String;let status:String;let adUnitId:String;let customData:String
    let created:Double;let expires:Double;let awardedCoins:Int
}
struct RewardedStatus:Decodable {
    let enabled:Bool;let available:Bool;let reason:String;let reward:Int
    let dailyLimit:Int?;let earnedToday:Int;let remainingToday:Int?;let resets:Double;let nextAvailableAt:Double?
    let wallet:RewardedWallet;let attempt:RewardedAttempt?
}
private struct SavedRewardedAttempt:Codable {
    let account:String;let endpoint:String;let requestKey:String
    var attemptID:String?;var mayHaveEarned:Bool=false
}
enum RewardedConfiguration {
    static var productionUnit:String {Bundle.main.object(forInfoDictionaryKey:"QuizfolkRewardedAdUnitID") as? String ?? ""}
    static var configured:Bool {
        let appID=Bundle.main.object(forInfoDictionaryKey:"GADApplicationIdentifier") as? String ?? ""
        return appID.hasPrefix("ca-app-pub-") && appID.contains("~") && productionUnit.hasPrefix("ca-app-pub-") && productionUnit.contains("/") && !productionUnit.contains("3940256099942544")
    }
}

@MainActor protocol RewardedAdProvider:AnyObject {
    var privacyOptionsRequired:Bool {get}
    func updateConsent() async throws
    func gatherConsent(from:UIViewController) async throws
    func privacyOptions(from:UIViewController) async throws
    func load(unit:String,customData:String) async throws
    func present(from:UIViewController,reward:@escaping ()->Void,dismiss:@escaping (Bool,Error?)->Void) throws
    func discard()
}

/// Google callbacks signal completion; only the authenticated server can award coins.
@MainActor final class GoogleRewardedAdProvider:NSObject,RewardedAdProvider,FullScreenContentDelegate {
    private var ad:RewardedAd?
    private var initialized=false
    private var consentUpdated=false
    private var earned=false
    private var onReward:(()->Void)?
    private var onDismiss:((Bool,Error?)->Void)?
    var privacyOptionsRequired:Bool {ConsentInformation.shared.privacyOptionsRequirementStatus == .required}
    func updateConsent() async throws {
        guard !consentUpdated else{return}
        try await withCheckedThrowingContinuation { (continuation:CheckedContinuation<Void,Error>) in
            ConsentInformation.shared.requestConsentInfoUpdate(with:RequestParameters()) {error in
                if let error {continuation.resume(throwing:error)}else{continuation.resume()}
            }
        }
        consentUpdated=true
    }
    func gatherConsent(from presenter:UIViewController) async throws {
        try await updateConsent()
        try await ConsentForm.loadAndPresentIfRequired(from:presenter)
        guard ConsentInformation.shared.canRequestAds else {throw APIError.message("Your privacy choices do not currently allow an ad to load.")}
    }
    func privacyOptions(from presenter:UIViewController) async throws {
        discard()
        try await ConsentForm.presentPrivacyOptionsForm(from:presenter)
    }
    func load(unit:String,customData:String) async throws {
        guard ConsentInformation.shared.canRequestAds else {throw APIError.message("Please review your ad privacy choices first.")}
        if !initialized {
            let configuration=MobileAds.shared.requestConfiguration
            configuration.maxAdContentRating=GADMaxAdContentRating.general
            configuration.publisherPrivacyPersonalizationState = .disabled
            configuration.setPublisherFirstPartyIDEnabled(false)
            configuration.coarseLocationCollectionEnabled=false
            await MobileAds.shared.start()
            initialized=true
        }
        #if DEBUG
        let requestedUnit="ca-app-pub-3940256099942544/1712485313"
        #else
        let requestedUnit=unit
        #endif
        let request=Request()
        let extras=Extras();extras.additionalParameters=["npa":"1"];request.register(extras)
        let loaded:RewardedAd
        do {loaded=try await RewardedAd.load(with:requestedUnit,request:request)}
        catch {throw APIError.message("No video is available right now. Please try again later.")}
        let verification=ServerSideVerificationOptions()
        verification.customRewardText=customData
        // No user ID, account name, token or other profile data is sent to Google.
        loaded.serverSideVerificationOptions=verification
        loaded.fullScreenContentDelegate=self
        ad=loaded
    }
    func present(from presenter:UIViewController,reward:@escaping ()->Void,dismiss:@escaping (Bool,Error?)->Void) throws {
        guard ConsentInformation.shared.canRequestAds,let ad else {throw APIError.message("This ad is no longer ready. Please load another.")}
        try ad.canPresent(from:presenter)
        earned=false;onReward=reward;onDismiss=dismiss
        ad.present(from:presenter) { [weak self] in
            guard let self else{return}
            self.earned=true;self.onReward?()
        }
    }
    func discard() {ad=nil}
    func adDidDismissFullScreenContent(_ ad:FullScreenPresentingAd) {
        let callback=onDismiss;let completed=earned
        self.ad=nil;onReward=nil;onDismiss=nil
        callback?(completed,nil)
    }
    func ad(_ ad:FullScreenPresentingAd,didFailToPresentFullScreenContentWithError error:Error) {
        let callback=onDismiss
        self.ad=nil;onReward=nil;onDismiss=nil
        callback?(earned,error)
    }
}

@MainActor final class RewardedAdCoordinator:ObservableObject {
    static let shared=RewardedAdCoordinator()
    enum Phase:Equatable {case idle,loading,ready,presenting,checking,awarded}
    @Published private(set) var phase=Phase.idle
    @Published private(set) var status:RewardedStatus?
    @Published private(set) var message:String?
    @Published private(set) var privacyOptionsRequired=false
    @Published private(set) var polling=false
    @Published private(set) var preparing=false
    private weak var store:QuizStore?
    private weak var anchor:UIViewController?
    private var provider:RewardedAdProvider?
    private var saved:SavedRewardedAttempt?
    private var scope=""
    private var pollTask:Task<Void,Never>?
    private var consentTask:Task<Void,Never>?
    private var preparationID:UUID?
    private var pollingID:UUID?
    private let persistenceKey="quizfolk.rewarded.pending.v1"
    #if DEBUG
    private var fixture:RewardedFixture?
    #endif
    var busy:Bool {preparing || phase == .loading || phase == .presenting}
    var canPrepare:Bool {!busy && phase != .ready && phase != .checking && status?.available == true}
    var hasPending:Bool {saved?.attemptID != nil && status?.attempt?.status == "pending"}
    var canCancel:Bool {hasPending && saved?.mayHaveEarned == false && !busy}

    func setAnchor(_ controller:UIViewController) {anchor=controller}
    private func presenter() throws -> UIViewController {
        guard UIApplication.shared.applicationState == .active,
              let root=anchor?.view.window?.rootViewController else {throw APIError.message("Return to Earn coins to watch the ad.")}
        var visible=root
        while let presented=visible.presentedViewController,!presented.isBeingDismissed {visible=presented}
        return visible
    }
    func activate(_ store:QuizStore) async {
        #if DEBUG
        if StoreScreenshotFixture.enabled {return}
        #endif
        guard let account=store.profile?.id else{return}
        let newScope=store.apiURL+"|"+account
        self.store=store
        if scope != newScope {
            pollTask?.cancel();consentTask?.cancel();provider?.discard()
            pollTask=nil;pollingID=nil;polling=false;preparationID=nil;preparing=false
            scope=newScope;status=nil;phase = .idle;message=nil
            saved=UserDefaults.standard.data(forKey:persistenceKey).flatMap{try? JSONDecoder().decode(SavedRewardedAttempt.self,from:$0)}
            if saved?.account != account || saved?.endpoint != store.apiURL {saved=nil}
            #if DEBUG
            if store.isUITesting {
                let fake=RewardedFixture()
                fixture=fake;provider=FixtureRewardedAdProvider(fixture:fake)
                if ProcessInfo.processInfo.arguments.contains("--rewarded-resume"),let id=saved?.attemptID {fake.restoreVerifiedAttempt(id:id)}
                else {saved=nil;persist()}
            } else {fixture=nil;provider=GoogleRewardedAdProvider()}
            #else
            provider=GoogleRewardedAdProvider()
            #endif
            // Updating consent does not initialize ads, load an ad, or show a form.
            if isConfigured {
                consentTask=Task { [weak self] in
                    guard let self,let provider=self.provider else{return}
                    try? await provider.updateConsent()
                    guard self.scope == newScope else{return}
                    self.privacyOptionsRequired=provider.privacyOptionsRequired
                }
            }
        }
        await refresh()
        if hasPending,saved?.mayHaveEarned == true,phase != .presenting,phase != .ready,phase != .loading {startPolling()}
    }
    private var isConfigured:Bool {
        #if DEBUG
        if fixture != nil {return true}
        #endif
        return RewardedConfiguration.configured
    }
    private func persist() {
        if let saved,let data=try? JSONEncoder().encode(saved) {UserDefaults.standard.set(data,forKey:persistenceKey)}
        else {UserDefaults.standard.removeObject(forKey:persistenceKey)}
    }
    private func request(_ route:String,body:[String:Any]?=nil,attempt:String?=nil) async throws -> RewardedStatus {
        #if DEBUG
        if let fixture {return try fixture.request(route,body:body,attempt:attempt)}
        #endif
        guard let store else {throw APIError.message("Connect to your Quizfolk account first.")}
        var query=[URLQueryItem(name:"platform",value:"ios")]
        if let attempt {query.append(URLQueryItem(name:"attempt",value:attempt))}
        let expectedScope=scope
        let expectedAttempt=saved?.attemptID
        let expectedRequest=saved?.requestKey
        let result:RewardedStatus=try await store.request(route,body:body,query:body == nil ? query:[])
        guard expectedScope == scope else {throw CancellationError()}
        if route == "rewarded-start" {
            guard expectedRequest == saved?.requestKey else {throw CancellationError()}
        } else {
            guard expectedAttempt == saved?.attemptID,expectedRequest == saved?.requestKey else {throw CancellationError()}
        }
        return result
    }
    private func apply(_ result:RewardedStatus) {
        status=result;store?.coinBalance=result.wallet.coins
        guard let attempt=result.attempt else{return}
        if saved?.attemptID == nil,attempt.status == "pending",let store,let account=store.profile?.id {
            if saved != nil {
                // Recover a reserved attempt after its start response was lost.
                saved?.attemptID=attempt.id
            } else {
                // A restored attempt may have completed before the app was closed.
                saved=SavedRewardedAttempt(account:account,endpoint:store.apiURL,requestKey:UUID().uuidString,attemptID:attempt.id,mayHaveEarned:true)
            }
            persist()
        }
        if attempt.status == "awarded",attempt.awardedCoins == 5 {
            saved=nil;persist();phase = .awarded;message="5 coins added to your wallet."
        } else if ["expired","cancelled","rejected"].contains(attempt.status) {
            saved=nil;persist();provider?.discard();phase = .idle
            if attempt.status != "cancelled" {message="This ad reward could not be confirmed. No coins were added."}
        } else if attempt.status == "pending",phase != .ready,phase != .loading,phase != .presenting {
            phase = .checking
        }
    }
    func refresh() async {
        guard store != nil,!busy,phase != .ready else{return}
        do {apply(try await request("rewarded-status",attempt:saved?.attemptID))}
        catch is CancellationError {return}
        catch {if phase != .presenting {message=hasPending ? "Your reward is still pending. Check again when you’re connected.":"Ads are unavailable right now. Please try again later."}}
    }
    func prepare() async {
        guard !busy,phase != .ready,phase != .checking,let store,let account=store.profile?.id else{return}
        guard isConfigured,let provider else {message="Ads are not available yet. You can still earn coins from your daily trail.";return}
        let expectedScope=scope
        let operationID=UUID();preparationID=operationID;preparing=true
        defer {if preparationID == operationID {preparationID=nil;preparing=false}}
        phase = .loading;message=nil
        do {
            let current=try await request("rewarded-status",attempt:saved?.attemptID);apply(current)
            guard current.available else {phase=hasPending ? .checking:.idle;return}
            phase = .loading
            await consentTask?.value
            guard scope == expectedScope else{return}
            try await provider.gatherConsent(from:presenter())
            guard scope == expectedScope else{return}
            privacyOptionsRequired=provider.privacyOptionsRequired
            if saved == nil {saved=SavedRewardedAttempt(account:account,endpoint:store.apiURL,requestKey:UUID().uuidString);persist()}
            let response=try await request("rewarded-start",body:["platform":"ios","requestKey":saved!.requestKey]);apply(response)
            if response.attempt?.status == "awarded" {return}
            guard let attempt=response.attempt,attempt.status == "pending",attempt.platform == "ios" else {throw APIError.message("An ad reward is already being checked. Please try again after it settles.")}
            saved?.attemptID=attempt.id;persist()
            #if DEBUG
            let usesFixture=fixture != nil
            #else
            let usesFixture=false
            #endif
            guard usesFixture || attempt.adUnitId == RewardedConfiguration.productionUnit else {throw APIError.message("This ad is not available for this version of Quizfolk.")}
            try await provider.load(unit:attempt.adUnitId,customData:attempt.customData)
            guard scope == expectedScope,saved?.attemptID == attempt.id else{provider.discard();return}
            phase = .ready;message="Your video is ready. Complete it to earn 5 coins."
        } catch {
            guard scope == expectedScope else{return}
            let explanation=error.localizedDescription
            if saved?.attemptID != nil,saved?.mayHaveEarned == false {await cancel()}
            phase=hasPending ? .checking:.idle
            message=explanation
            privacyOptionsRequired=provider.privacyOptionsRequired
        }
    }
    func show() {
        guard phase == .ready,let provider,let attempt=status?.attempt else{return}
        let expectedScope=scope
        guard attempt.expires>Date().timeIntervalSince1970 else {Task{await cancel();message="This ad expired. Please load another."};return}
        do {
            let controller=try presenter()
            saved?.mayHaveEarned=true;persist();phase = .presenting;message=nil
            try provider.present(from:controller,reward:{ [weak self] in
                guard let self,self.scope == expectedScope,self.saved?.attemptID == attempt.id else{return}
                self.saved?.mayHaveEarned=true;self.persist()
                #if DEBUG
                self.fixture?.receiveCompletion()
                #endif
            },dismiss:{ [weak self] earned,error in
                guard let self,self.scope == expectedScope else{return}
                guard self.saved?.attemptID == attempt.id || self.status?.attempt?.id == attempt.id && self.status?.attempt?.status == "awarded" else{return}
                if earned {
                    if self.status?.attempt?.status != "awarded" {self.phase = .checking;self.message="Checking your reward…";self.startPolling()}
                }
                else {
                    self.saved?.mayHaveEarned=false;self.persist()
                    Task {
                        guard self.scope == expectedScope,self.saved?.attemptID == attempt.id else{return}
                        await self.cancel()
                        if self.scope == expectedScope,self.phase != .awarded {self.message=error == nil ? "Video closed before completion. No coins were added.":"The ad could not be shown. No coins were added."}
                    }
                }
            })
        } catch {
            saved?.mayHaveEarned=false;persist()
            Task {guard scope == expectedScope,saved?.attemptID == attempt.id else{return};await cancel();if scope == expectedScope {message=error.localizedDescription}}
        }
    }
    func cancel() async {
        guard let attempt=saved?.attemptID,saved?.mayHaveEarned == false else{return}
        let expectedScope=scope
        provider?.discard()
        do {
            let response=try await request("rewarded-cancel",body:["platform":"ios","attempt":attempt]);apply(response)
            if response.attempt?.status != "awarded" {phase = .idle;message=nil}
        }
        catch {guard scope == expectedScope,saved?.attemptID == attempt else{return};phase = .checking;message="We couldn’t cancel this unused ad. Please check again when you’re connected."}
    }
    func checkReward() {startPolling()}
    private func startPolling() {
        guard pollTask == nil,hasPending else{return}
        let generation=UUID();pollingID=generation
        polling=true
        pollTask=Task { [weak self] in
            guard let self else{return}
            defer {if self.pollingID == generation {self.polling=false;self.pollTask=nil;self.pollingID=nil}}
            for delay in [0,2,2,4,5,8,10] {
                if Task.isCancelled{return}
                if delay>0 {try? await Task.sleep(for:.seconds(delay))}
                if Task.isCancelled{return}
                await self.refresh()
                if !self.hasPending{return}
            }
            if self.hasPending {self.message="Your completed video is awaiting confirmation. Your coins will be added once it is verified, even if you close the app."}
        }
    }
    func showPrivacyOptions() async {
        guard !busy,let provider else{return}
        if phase == .ready {await cancel()}
        do {try await provider.privacyOptions(from:presenter());privacyOptionsRequired=provider.privacyOptionsRequired}
        catch {message="Privacy options are unavailable right now. Please try again."}
    }
}

struct RewardedAdCard:View {
    @EnvironmentObject private var store:QuizStore
    @ObservedObject private var ads=RewardedAdCoordinator.shared
    var body:some View {
        VStack(alignment:.leading,spacing:14) {
            HStack(spacing:12){Image(systemName:"play.rectangle.fill").font(.title).foregroundStyle(Color.coral);VStack(alignment:.leading,spacing:4){Text("A video, 5 coins").font(.title3.bold());Text("An optional way to top up.").font(.subheadline).foregroundStyle(.secondary)}}
            Text("Complete a short ad to earn 5 coins. It’s always your choice.").font(.subheadline)
            if let remaining=ads.status?.remainingToday,let limit=ads.status?.dailyLimit {Text("\(remaining) of \(limit) videos available today").font(.caption).foregroundStyle(.secondary)}
            if ads.phase == .loading {ProgressView("Getting your ad ready…").accessibilityIdentifier("rewardedLoading")}
            else if ads.phase == .ready {
                Button("Watch video · +5 coins"){ads.show()}.buttonStyle(PrimaryButton()).accessibilityIdentifier("rewardedShow")
                Button("Cancel"){Task{await ads.cancel()}}.accessibilityIdentifier("rewardedCancel")
            } else if ads.phase == .checking {
                Text(ads.message ?? "Checking your reward…").font(.subheadline).accessibilityIdentifier("rewardedPending")
                Button(ads.polling ? "Checking…":"Check reward"){ads.checkReward()}.buttonStyle(PrimaryButton()).disabled(ads.polling).accessibilityIdentifier("rewardedCheck")
                if ads.canCancel {Button("Cancel unused ad"){Task{await ads.cancel()}}.accessibilityIdentifier("rewardedCancel")}
            } else {
                Button("Load a video · +5 coins"){Task{await ads.prepare()}}.buttonStyle(PrimaryButton()).disabled(!ads.canPrepare).accessibilityIdentifier("rewardedLoad")
            }
            if ads.phase != .checking,let message=ads.message {Text(message).font(.subheadline).foregroundStyle(ads.phase == .awarded ? .green:.secondary).accessibilityIdentifier(ads.phase == .awarded ? "rewardedConfirmed":"rewardedMessage")}
            if ads.status?.enabled == false {Text("Videos are unavailable right now. Your daily rewards and trail are still available.").font(.caption).foregroundStyle(.secondary)}
            if ads.privacyOptionsRequired {Button("Ad privacy choices"){Task{await ads.showPrivacyOptions()}}.disabled(ads.busy).accessibilityIdentifier("rewardedPrivacy")}
        }.padding(20).frame(maxWidth:.infinity,alignment:.leading).background(.white,in:RoundedRectangle(cornerRadius:18))
            .accessibilityIdentifier("rewardedCard")
            .background(RewardedPresentationAnchor {ads.setAnchor($0)}.frame(width:0,height:0))
            .task {await ads.activate(store)}
    }
}
private struct RewardedPresentationAnchor:UIViewControllerRepresentable {
    let ready:(UIViewController)->Void
    func makeUIViewController(context:Context)->RewardedAnchorController {let controller=RewardedAnchorController();controller.ready=ready;return controller}
    func updateUIViewController(_ controller:RewardedAnchorController,context:Context) {controller.ready=ready}
}
private final class RewardedAnchorController:UIViewController {
    var ready:((UIViewController)->Void)?
    override func viewDidAppear(_ animated:Bool) {super.viewDidAppear(animated);ready?(self)}
}
