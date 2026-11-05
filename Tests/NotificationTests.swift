import XCTest
@testable import Quizfolk

@MainActor final class NotificationTests:XCTestCase {
    func testDefaultChoicesRequireExplicitOptIn() {
        let choices=NotificationPreferences()
        XCTAssertFalse(choices.enabled)
        XCTAssertEqual(Set(choices.dictionary.keys),Set(["enabled","challenges","duelResults","tournamentPrizes","friendsTournaments"]))
    }
    func testTapPayloadOnlyAcceptsKnownDestinations() {
        for kind in ["challenges","duelResults","tournamentPrizes","friendsTournaments"] {XCTAssertNotNil(PushDestination(["kind":kind,"id":"week:20261105:22","topicID":"22"]))}
        XCTAssertNil(PushDestination(["kind":"openURL","id":"anything"]))
        XCTAssertNil(PushDestination(["kind":"challenges","id":"https://example.com/"]))
        XCTAssertNil(PushDestination(["kind":"challenges","id":""]))
    }
    func testPreferencesPersistThroughServiceAndFailedSaveKeepsPreviousChoices() async throws {
        let store=QuizStore();await store.connect()
        var saved=NotificationPreferences();var reject=false
        store.testResponse={route,body in
            if route=="notification-preferences" {
                if reject {throw APIError.message("Connection interrupted")}
                let raw=try JSONSerialization.data(withJSONObject:body!["preferences"]!)
                saved=try JSONDecoder().decode(NotificationPreferences.self,from:raw)
            } else {XCTAssertEqual(route,"notification-settings")}
            return try JSONEncoder().encode(NotificationSettingsReply(preferences:saved,delivery:PushDelivery(ios:false,android:false)))
        }
        var next=NotificationPreferences();next.enabled=true;next.challenges=false;next.friendsTournaments=false
        await store.saveNotificationChoices(next)
        XCTAssertEqual(store.notificationSettings.preferences,next)
        let reopened=QuizStore();reopened.testResponse=store.testResponse;await reopened.loadNotificationSettings()
        XCTAssertEqual(reopened.notificationSettings.preferences,next)
        reject=true;var failed=next;failed.tournamentPrizes=false
        await store.saveNotificationChoices(failed)
        XCTAssertEqual(store.notificationSettings.preferences,next);XCTAssertNotNil(store.notificationError)
    }
    func testForegroundFilterRespectsMasterAndIndividualChoices() throws {
        let previous=UserDefaults.standard.data(forKey:"pushPreferences")
        defer{UserDefaults.standard.set(previous,forKey:"pushPreferences")}
        var choices=NotificationPreferences();choices.enabled=true;choices.challenges=false
        UserDefaults.standard.set(try JSONEncoder().encode(choices),forKey:"pushPreferences")
        XCTAssertFalse(PushCoordinator.shouldPresent(["kind":"challenges"]))
        XCTAssertTrue(PushCoordinator.shouldPresent(["kind":"tournamentPrizes"]))
        choices.enabled=false;UserDefaults.standard.set(try JSONEncoder().encode(choices),forKey:"pushPreferences")
        XCTAssertFalse(PushCoordinator.shouldPresent(["kind":"tournamentPrizes"]))
    }
}
