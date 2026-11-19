import XCTest
@testable import Quizfolk

@MainActor final class RewardedAvailabilityTests:XCTestCase {
    func testReleaseRequestsOnlyGoogleDemoUnit() {
        XCTAssertTrue(RewardedConfiguration.enabledInThisRelease)
        XCTAssertTrue(RewardedConfiguration.testAdsInThisRelease)
        XCTAssertEqual(RewardedConfiguration.requestedUnit,"ca-app-pub-3940256099942544/1712485313")
    }
    func testCompletedTestVideoRetriesRealWalletCreditAfterRelaunch() async throws {
        let store=QuizStore();await store.connect()
        let account=try XCTUnwrap(store.profile?.id)
        let key="rewarded-test-settlement-"+UUID().uuidString
        defer {UserDefaults.standard.removeObject(forKey:key)}
        let saved:[String:Any]=["account":account,"endpoint":store.apiURL,"requestKey":"existing-request","attemptID":"existing-attempt","mayHaveEarned":true,"testCompletionReceived":true]
        UserDefaults.standard.set(try JSONSerialization.data(withJSONObject:saved),forKey:key)
        var routes:[String]=[]
        store.testResponse={route,body in
            routes.append(route)
            XCTAssertEqual(route,"rewarded-test-complete")
            XCTAssertEqual(body?["attempt"] as? String,"existing-attempt")
            XCTAssertEqual(body?["platform"] as? String,"ios")
            return Data(#"{"enabled":true,"available":true,"reason":"ready","reward":5,"testMode":true,"dailyLimit":null,"earnedToday":1,"remainingToday":null,"resets":1794441600,"nextAvailableAt":null,"wallet":{"coins":115},"attempt":{"id":"existing-attempt","platform":"ios","status":"awarded","adUnitId":"ca-app-pub-3940256099942544/1712485313","customData":"opaque","created":1794355200,"expires":1794355800,"awardedCoins":5}}"#.utf8)
        }
        let ads=RewardedAdCoordinator(persistenceKey:key)
        await ads.activate(store)
        XCTAssertEqual(routes,["rewarded-test-complete"])
        XCTAssertEqual(store.coinBalance,115)
        XCTAssertEqual(ads.phase,.awarded)
        XCTAssertNil(UserDefaults.standard.data(forKey:key))
        XCTAssertTrue(ads.canPrepare)
    }
    func testPresentingVideoAloneDoesNotRequestTestCoins() async throws {
        let store=QuizStore();await store.connect()
        let account=try XCTUnwrap(store.profile?.id)
        let key="rewarded-test-not-completed-"+UUID().uuidString
        defer {UserDefaults.standard.removeObject(forKey:key)}
        let saved:[String:Any]=["account":account,"endpoint":store.apiURL,"requestKey":"existing-request","attemptID":"existing-attempt","mayHaveEarned":true]
        UserDefaults.standard.set(try JSONSerialization.data(withJSONObject:saved),forKey:key)
        store.testResponse={route,_ in
            XCTAssertEqual(route,"rewarded-status","Only the SDK completion callback authorizes a test reward request")
            return Data(#"{"enabled":true,"available":true,"reason":"ready","reward":5,"testMode":true,"dailyLimit":null,"earnedToday":0,"remainingToday":null,"resets":1794441600,"nextAvailableAt":null,"wallet":{"coins":110},"attempt":{"id":"existing-attempt","platform":"ios","status":"cancelled","adUnitId":"test-unit","customData":"opaque","created":1794355200,"expires":1794355800,"awardedCoins":0}}"#.utf8)
        }
        let ads=RewardedAdCoordinator(persistenceKey:key)
        await ads.activate(store)
        XCTAssertEqual(store.coinBalance,110)
        XCTAssertEqual(ads.phase,.idle)
        XCTAssertNil(UserDefaults.standard.data(forKey:key))
    }
}
