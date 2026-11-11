import XCTest
@testable import Quizfolk

@MainActor final class RewardedAvailabilityTests:XCTestCase {
    func testPausedReleaseCannotStartAnAdOrRequestConsent() async {
        XCTAssertFalse(RewardedConfiguration.enabledInThisRelease)
        XCTAssertFalse(RewardedConfiguration.enabled)
        let store=QuizStore();await store.connect()
        var routes:[String]=[]
        store.testResponse={route,_ in
            routes.append(route)
            throw APIError.message("No reward request is expected while paused")
        }
        let ads=RewardedAdCoordinator(persistenceKey:"rewarded-paused-test-"+UUID().uuidString)
        await ads.activate(store)
        await ads.refresh()
        await ads.prepare()
        ads.show()
        await ads.showPrivacyOptions()
        XCTAssertTrue(routes.isEmpty)
        XCTAssertFalse(ads.canPrepare)
        XCTAssertFalse(ads.privacyOptionsRequired)
        XCTAssertEqual(ads.phase,.idle)
        XCTAssertNil(ads.message)
    }

    func testPausedReleaseStillSettlesAnAlreadyEarnedReward() async throws {
        let store=QuizStore();await store.connect()
        let account=try XCTUnwrap(store.profile?.id)
        let key="rewarded-settlement-test-"+UUID().uuidString
        defer {UserDefaults.standard.removeObject(forKey:key)}
        let saved:[String:Any]=["account":account,"endpoint":store.apiURL,"requestKey":"existing-request","attemptID":"existing-attempt","mayHaveEarned":true]
        UserDefaults.standard.set(try JSONSerialization.data(withJSONObject:saved),forKey:key)
        var routes:[String]=[]
        store.testResponse={route,body in
            routes.append(route)
            XCTAssertEqual(route,"rewarded-status")
            XCTAssertNil(body)
            return Data(#"{"enabled":true,"available":true,"reason":"ready","reward":5,"dailyLimit":null,"earnedToday":1,"remainingToday":null,"resets":1794441600,"nextAvailableAt":null,"wallet":{"coins":115},"attempt":{"id":"existing-attempt","platform":"ios","status":"awarded","adUnitId":"existing-unit","customData":"opaque","created":1794355200,"expires":1794355800,"awardedCoins":5}}"#.utf8)
        }
        let ads=RewardedAdCoordinator(persistenceKey:key)
        await ads.activate(store)
        XCTAssertEqual(store.coinBalance,115)
        XCTAssertEqual(ads.phase,.awarded)
        XCTAssertNil(UserDefaults.standard.data(forKey:key))
        XCTAssertFalse(ads.canPrepare)
        await ads.refresh()
        await ads.prepare()
        XCTAssertEqual(routes,["rewarded-status"],"Settling an old reward must not enable new requests")
    }
}
