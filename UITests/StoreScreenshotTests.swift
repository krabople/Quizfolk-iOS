import XCTest

/// Opt-in marketing captures. Run only through the manual store-screenshots workflow.
final class StoreScreenshotTests:XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure=false
        try XCTSkipUnless(ProcessInfo.processInfo.environment["STORE_SCREENSHOTS"]=="1", "App Store captures are opt-in")
    }
    @MainActor private func launch()->XCUIApplication {
        let app=XCUIApplication()
        app.launchArguments=["--ui-testing","--store-screenshots"]
        app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        XCTAssertTrue(app.tabBars.buttons["Discover"].waitForExistence(timeout:8))
        return app
    }
    @MainActor private func capture(_ name:String) {
        let shot=XCTAttachment(screenshot:XCUIScreen.main.screenshot())
        shot.name="STORE-"+name;shot.lifetime = .keepAlways;add(shot)
    }
    @MainActor private func topic(_ app:XCUIApplication) {
        let field=app.textFields["Search categories"]
        XCTAssertTrue(field.waitForExistence(timeout:8));field.tap();field.typeText("Geography")
        let link=app.descendants(matching:.any).matching(identifier:"topic-22").firstMatch
        for _ in 0..<3 {if link.isHittable{break};app.swipeUp()}
        XCTAssertTrue(link.waitForExistence(timeout:8));link.tap()
        XCTAssertTrue(app.buttons["League"].waitForExistence(timeout:8))
    }
    @MainActor func test01Topics() {
        let app=launch()
        // A short scroll shows the actual topic grid while keeping the page identity visible.
        app.swipeUp(velocity:300)
        capture("02-topics")
    }
    @MainActor func test02Gameplay() {
        let app=launch();topic(app)
        let duel=app.buttons["Find a duel"]
        for _ in 0..<4 {if duel.isHittable{break};app.swipeUp()}
        XCTAssertTrue(duel.waitForExistence(timeout:8));duel.tap()
        let start=app.buttons["Start duel"]
        XCTAssertTrue(start.waitForExistence(timeout:12));start.tap()
        XCTAssertTrue(app.buttons["answer-0"].waitForExistence(timeout:12))
        for n in 0..<4 {XCTAssertTrue(app.buttons["answer-\(n)"].isHittable)}
        capture("01-duel")
    }
    @MainActor func test03Challenges() {
        let app=launch();app.tabBars.buttons["Duels"].tap()
        XCTAssertTrue(app.staticTexts["Maya"].waitForExistence(timeout:8))
        capture("03-challenges")
    }
    @MainActor func test04Progress() {
        let app=launch();topic(app)
        capture("04-topic-progress")
    }
    @MainActor func test05League() {
        let app=launch();topic(app);app.buttons["League"].tap()
        let entry=app.buttons["league-player-test-rival"]
        XCTAssertTrue(entry.waitForExistence(timeout:8))
        app.swipeUp(velocity:350)
        capture("05-topic-league")
    }
    @MainActor func test06Tournament() {
        let app=launch();app.tabBars.buttons["Tournaments"].tap()
        let event=app.descendants(matching:.any).matching(identifier:"tournament-test-event").firstMatch
        for _ in 0..<3 {if event.isHittable{break};app.swipeUp()}
        XCTAssertTrue(event.waitForExistence(timeout:8));event.tap()
        XCTAssertTrue(app.buttons["enterTournament"].waitForExistence(timeout:8))
        app.swipeUp(velocity:300)
        capture("06-tournament")
    }
    @MainActor func test07Friends() {
        let app=launch();app.tabBars.buttons["Tournaments"].tap()
        XCTAssertTrue(app.buttons["friendsTournaments"].waitForExistence(timeout:8));app.buttons["friendsTournaments"].tap()
        let room=app.buttons.matching(NSPredicate(format:"label CONTAINS 'Friday quiz club'")).firstMatch
        XCTAssertTrue(room.waitForExistence(timeout:8));room.tap()
        XCTAssertTrue(app.buttons["friends-league-player-test-self"].waitForExistence(timeout:8))
        capture("07-friends")
    }
    @MainActor func test08Badges() {
        let app=launch();app.tabBars.buttons["You"].tap()
        XCTAssertTrue(app.buttons["Tournament badges"].waitForExistence(timeout:8));app.buttons["Tournament badges"].tap()
        XCTAssertTrue(app.buttons["earnedBadge-test-prize"].waitForExistence(timeout:8))
        capture("08-badges")
    }
    @MainActor func test09Profile() {
        let app=launch();app.tabBars.buttons["People"].tap()
        let player=app.descendants(matching:.any).matching(identifier:"player-test-rival").firstMatch
        XCTAssertTrue(player.waitForExistence(timeout:8));player.tap()
        XCTAssertTrue(app.buttons["followPlayer"].waitForExistence(timeout:8))
        capture("09-rival-profile")
    }
    @MainActor func test10Result() {
        let app=launch();app.tabBars.buttons["Duels"].tap();app.buttons["Device history"].tap()
        let history=app.buttons["history-match-history-fixture"]
        XCTAssertTrue(history.waitForExistence(timeout:8));history.tap()
        XCTAssertTrue(app.buttons["historyResult"].waitForExistence(timeout:8));app.buttons["historyResult"].tap()
        XCTAssertTrue(app.descendants(matching:.any).matching(identifier:"winnerAnnouncement").firstMatch.waitForExistence(timeout:8))
        capture("10-result")
    }
}
