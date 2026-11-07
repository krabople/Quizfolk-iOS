#if DEBUG
import SwiftUI
import UIKit

/// Isolated fixture transport. Never instantiated outside the UI-test launch.
@MainActor final class RewardedFixture {
    var attempt:RewardedAttempt?
    var verified=false
    private var coins=110
    private var awards=0
    private var credited=false
    private var lostStart=false
    var arguments:[String] {ProcessInfo.processInfo.arguments}
    func start(key:String)->RewardedAttempt {
        if let attempt,attempt.status == "pending" {return attempt}
        credited=false;verified=false
        let value=RewardedAttempt(id:UUID().uuidString,platform:"ios",status:"pending",adUnitId:"fixture-unit",customData:"fixture-opaque",created:Date().timeIntervalSince1970,expires:Date().timeIntervalSince1970+600,awardedCoins:0)
        attempt=value;return value
    }
    func receiveCompletion() {if !arguments.contains("--rewarded-pending"){verified=true}}
    func restoreVerifiedAttempt(id:String) {
        attempt=RewardedAttempt(id:id,platform:"ios",status:"pending",adUnitId:"fixture-unit",customData:"fixture-opaque",created:Date().timeIntervalSince1970-60,expires:Date().timeIntervalSince1970+540,awardedCoins:0)
        verified=true
    }
    func request(_ route:String,body:[String:Any]?,attempt requested:String?) throws -> RewardedStatus {
        if route == "rewarded-start" {
            _ = start(key:body?["requestKey"] as? String ?? "fixture")
            if arguments.contains("--rewarded-start-lost"),!lostStart {lostStart=true;throw APIError.message("Connection interrupted while reserving the video. Please try again.")}
        }
        if route == "rewarded-cancel",let value=attempt,!verified {
            attempt=RewardedAttempt(id:value.id,platform:value.platform,status:"cancelled",adUnitId:value.adUnitId,customData:value.customData,created:value.created,expires:value.expires,awardedCoins:0)
        }
        if verified,let value=attempt {
            if !credited {coins+=5;awards+=1;credited=true}
            attempt=RewardedAttempt(id:value.id,platform:value.platform,status:"awarded",adUnitId:value.adUnitId,customData:value.customData,created:value.created,expires:value.expires,awardedCoins:5)
        }
        let pending=attempt?.status == "pending"
        return RewardedStatus(enabled:true,available:!pending,reason:pending ? "pending":"ready",reward:5,dailyLimit:nil,earnedToday:awards,remainingToday:nil,resets:Date().timeIntervalSince1970+86400,nextAvailableAt:nil,wallet:RewardedWallet(coins:coins),attempt:attempt)
    }
}

@MainActor final class FixtureRewardedAdProvider:RewardedAdProvider {
    let fixture:RewardedFixture
    private var loaded=false
    var privacyOptionsRequired:Bool {true}
    init(fixture:RewardedFixture){self.fixture=fixture}
    func updateConsent() async throws {}
    func gatherConsent(from:UIViewController) async throws {
        if fixture.arguments.contains("--rewarded-consent-denied") {throw APIError.message("Your privacy choices do not currently allow an ad to load.")}
    }
    func privacyOptions(from presenter:UIViewController) async throws {
        let alert=UIAlertController(title:"Ad privacy choices",message:"Isolated test privacy form. No advertising SDK was started.",preferredStyle:.alert)
        alert.addAction(UIAlertAction(title:"Done",style:.default));presenter.present(alert,animated:false)
    }
    func load(unit:String,customData:String) async throws {
        if fixture.arguments.contains("--rewarded-no-fill") {throw APIError.message("No video is available right now. Please try again later.")}
        loaded=true
    }
    func present(from presenter:UIViewController,reward:@escaping ()->Void,dismiss:@escaping (Bool,Error?)->Void) throws {
        guard loaded else {throw APIError.message("Fixture ad was not loaded")}
        let controller=UIHostingController(rootView:FixtureRewardedVideo())
        controller.rootView=FixtureRewardedVideo { [weak controller] completed in
            if completed {reward()}
            controller?.dismiss(animated:false){dismiss(completed,nil)}
        }
        controller.modalPresentationStyle = .fullScreen
        presenter.present(controller,animated:false)
        loaded=false
    }
    func discard(){loaded=false}
}
private struct FixtureRewardedVideo:View {
    var finish:(Bool)->Void={_ in}
    var body:some View {
        ZStack {
            Color.ink.ignoresSafeArea()
            VStack(spacing:24) {
                Text("Test video").font(.largeTitle.bold())
                Text("An isolated UI-test ad. No advertiser request is made.").multilineTextAlignment(.center)
                Button("Complete test video"){finish(true)}.buttonStyle(PrimaryButton()).accessibilityIdentifier("rewardedFixtureComplete")
                Button("Close video"){finish(false)}.buttonStyle(PrimaryButton(color:.gray)).accessibilityIdentifier("rewardedFixtureClose")
            }.foregroundStyle(.white).frame(maxWidth:540).padding(30)
        }.accessibilityIdentifier("rewardedFixtureVideo")
    }
}
#endif
