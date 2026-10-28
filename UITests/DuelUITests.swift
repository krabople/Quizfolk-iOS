import XCTest
final class DuelUITests:XCTestCase {
    @MainActor func testOfflineDuelAndHistory() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:8) {app.buttons["Done"].tap()}
        let search=app.textFields["Search categories"]
        XCTAssertTrue(search.waitForExistence(timeout:10))
        capture("Discover")
        search.tap();search.typeText("Geography")
        let link=app.descendants(matching:.any).matching(identifier:"topic-22").firstMatch
        XCTAssertTrue(link.waitForExistence(timeout:5));link.tap()
        app.swipeUp()
        let practice=app.buttons["Practise against a bot"]
        XCTAssertTrue(practice.waitForExistence(timeout:5));practice.tap()
        XCTAssertTrue(app.descendants(matching:.any).matching(identifier:"matchupTitle").firstMatch.waitForExistence(timeout:5))
        capture("Matchup")
        XCTAssertFalse(app.buttons["answer-0"].exists)
        app.buttons["Start duel"].tap()
        for i in 0..<7 {
            let option=app.buttons["answer-3"]
            XCTAssertTrue(option.waitForExistence(timeout:8))
            if i==0 {for n in 0..<4 {XCTAssertTrue(app.buttons["answer-\(n)"].isHittable,"Every answer must be visible without scrolling")}}
            if i==0 {XCTAssertTrue(app.otherElements["roundTimer"].exists);capture("Question")}
            if option.isEnabled {option.tap()}
            let next=app.buttons["advanceQuestion"]
            if !next.isHittable {app.swipeUp()}
            XCTAssertTrue(next.waitForExistence(timeout:12))
            if i==0 {
                let marker=app.descendants(matching:.any).matching(identifier:"roundMarker-0").firstMatch
                XCTAssertTrue(marker.label.contains(": correct") || marker.label.contains(": incorrect"))
                capture("AnswerReview")
            }
            next.tap()
        }
        let back=app.buttons["Back to topics"]
        if !back.isHittable {app.swipeUp();app.swipeUp()}
        XCTAssertTrue(back.waitForExistence(timeout:8));capture("Result");app.buttons["Leave match"].tap();XCTAssertFalse(app.buttons["Leave duel"].exists)
        app.navigationBars.buttons.element(boundBy:0).tap()
        app.tabBars.buttons["Duels"].tap();app.buttons["Device history"].tap()
        XCTAssertTrue(app.staticTexts["Offline practice"].waitForExistence(timeout:5))
        capture("History")
    }
    @MainActor func testProfilePhotoPicker() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3) {app.buttons["Done"].tap()}
        app.tabBars.buttons["You"].tap()
        let picker=app.buttons["changeProfilePicture"]
        XCTAssertTrue(picker.waitForExistence(timeout:8))
        expectation(for:NSPredicate(format:"enabled == true"),evaluatedWith:picker)
        waitForExpectations(timeout:25)
        capture("PlayerCard")
        picker.tap()
        let cancel=app.buttons["Cancel"]
        XCTAssertTrue(cancel.waitForExistence(timeout:8))
        let image=app.images.matching(NSPredicate(format:"label BEGINSWITH 'Photo,'")).firstMatch
        XCTAssertTrue(image.waitForExistence(timeout:30),app.debugDescription)
        capture("PhotoPicker")
        image.tap()
        XCTAssertTrue(app.staticTexts["Your player picture"].waitForExistence(timeout:15))
        XCTAssertTrue(app.buttons["Use this picture"].isHittable)
        capture("PicturePreview")
        app.buttons["Cancel"].tap()
        XCTAssertTrue(picker.waitForExistence(timeout:5))
    }
    @MainActor func testPeopleProfilesAndChallengeComposer() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        app.tabBars.buttons["People"].tap()
        XCTAssertTrue(app.textFields["playerSearch"].waitForExistence(timeout:8))
        let card=app.descendants(matching:.any).matching(identifier:"player-test-rival").firstMatch
        XCTAssertTrue(card.waitForExistence(timeout:8));capture("People");card.tap()
        XCTAssertTrue(app.buttons["followPlayer"].waitForExistence(timeout:8));app.buttons["followPlayer"].tap()
        XCTAssertTrue(app.buttons["Following"].waitForExistence(timeout:5))
        XCTAssertTrue(app.descendants(matching:.any).matching(identifier:"headToHead").firstMatch.exists)
        capture("RivalProfile")
        app.buttons["challengePlayer"].tap()
        XCTAssertTrue(app.buttons["sendChallenge"].waitForExistence(timeout:5));capture("ChallengeComposer")
        app.buttons["Cancel"].tap()
    }
    @MainActor func testTopicLeagueAndTournamentNavigation() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        app.textFields["Search categories"].tap();app.textFields["Search categories"].typeText("Geography")
        let topic=app.descendants(matching:.any).matching(identifier:"topic-22").firstMatch
        XCTAssertTrue(topic.waitForExistence(timeout:5));topic.tap()
        XCTAssertTrue(app.buttons["League"].waitForExistence(timeout:5));app.buttons["League"].tap()
        XCTAssertTrue(app.buttons["This month"].waitForExistence(timeout:5))
        XCTAssertTrue(app.buttons["All time"].exists);capture("TopicLeague")
        app.tabBars.buttons["Tournaments"].tap()
        let event=app.descendants(matching:.any).matching(identifier:"tournament-test-event").firstMatch
        XCTAssertTrue(event.waitForExistence(timeout:5));capture("Tournaments");event.tap()
        XCTAssertTrue(app.buttons["enterTournament"].waitForExistence(timeout:5))
        XCTAssertTrue(app.descendants(matching:.any).matching(identifier:"tournamentRules").firstMatch.exists)
        capture("TournamentRules")
    }
    @MainActor private func capture(_ name:String) {let a=XCTAttachment(screenshot:XCUIApplication().screenshot());a.name=name;a.lifetime = .keepAlways;add(a)}
}
