import XCTest
@testable import Quizfolk

@MainActor final class CoinsTests:XCTestCase {
    func testAcknowledgementFailureKeepsPrizeUntilRetrySucceeds() async throws {
        let store=QuizStore();await store.connect()
        var acknowledged=false
        var attempts=0
        store.testResponse={route,body in
            switch route {
            case "prizes":
                return try JSONSerialization.data(withJSONObject:["pending":acknowledged ? []:[Self.prize],"earned":[Self.prize],"selected":NSNull()])
            case "prize-seen":
                XCTAssertEqual(body?["event"] as? String,"test-prize")
                attempts+=1
                if attempts==1 {throw APIError.message("Connection interrupted")}
                acknowledged=true
                return Data(#"{"ok":true}"#.utf8)
            default: XCTFail("Unexpected request: \(route)");throw APIError.message("Unexpected request")
            }
        }
        await store.loadPrizes()
        XCTAssertEqual(store.earnedPrizes.count,1)
        let prize=try XCTUnwrap(store.pendingPrizes.first)
        do {try await store.acknowledgePrize(prize,wear:false);XCTFail("Expected interrupted acknowledgement")}catch{}
        XCTAssertEqual(store.pendingPrizes.map(\.id),[prize.id],"A failed acknowledgement must not lose the celebration")
        try await store.acknowledgePrize(prize,wear:false)
        XCTAssertTrue(store.pendingPrizes.isEmpty)
        await store.loadPrizes()
        XCTAssertTrue(store.pendingPrizes.isEmpty,"Already acknowledged prizes must not reopen on the next refresh")
        XCTAssertEqual(store.earnedPrizes.count,1,"Acknowledgement must not remove the earned badge")
        XCTAssertEqual(attempts,2)
    }
    func testFailedBadgeSelectionDoesNotAcknowledgePrize() async throws {
        let store=QuizStore();await store.connect()
        store.pendingPrizes=[QuizStore.testPrize]
        var routes:[String]=[]
        store.testResponse={route,body in
            routes.append(route)
            XCTAssertEqual(body?["event"] as? String,"test-prize")
            throw APIError.message("Unable to save badge")
        }
        do {try await store.acknowledgePrize(QuizStore.testPrize,wear:true);XCTFail("Expected selection error")}catch{}
        XCTAssertEqual(routes,["select-badge"],"The result stays unseen if saving the requested badge failed")
        XCTAssertEqual(store.pendingPrizes.count,1)
        XCTAssertNil(store.ownCard?.displayBadge)
    }
    func testCoinTrailUsesServerBalanceAndProgress() async throws {
        let store=QuizStore()
        store.testResponse={route,body in
            XCTAssertEqual(route,"coins");XCTAssertNil(body)
            return Data(#"{"wallet":{"coins":205,"tickets":0,"dailyClaimed":true},"topics":["22","17","9"],"earnedToday":45,"dailyMaximum":45,"completedDays":5,"weeklyBonusEarned":true,"resets":1793232000}"#.utf8)
        }
        let status=try await store.coinTrail()
        XCTAssertEqual(status.wallet.coins,205)
        XCTAssertEqual(status.topics,["22","17","9"])
        XCTAssertEqual(status.earnedToday,45)
        XCTAssertTrue(status.weeklyBonusEarned)
    }
    private static var prize:[String:Any] {["id":"test-prize","topicID":"22","kind":"daily","rank":1,"coins":75,"date":1_793_145_600,"score":120]}
}
