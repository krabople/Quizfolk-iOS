import XCTest
final class DuelUITests:XCTestCase {
    @MainActor func testOfflineDuelAndHistory() {
        let app=XCUIApplication();app.launch()
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
        XCTAssertTrue(back.waitForExistence(timeout:8));capture("Result");back.tap()
        app.navigationBars.buttons.element(boundBy:0).tap()
        app.tabBars.buttons["Matches"].tap()
        XCTAssertTrue(app.staticTexts["Offline practice"].waitForExistence(timeout:5))
        capture("History")
    }
    @MainActor func testProfilePhotoPicker() {
        let app=XCUIApplication();app.launch()
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
        capture("PhotoPicker")
        cancel.tap()
        XCTAssertTrue(picker.waitForExistence(timeout:5))
    }
    @MainActor private func capture(_ name:String) {let a=XCTAttachment(screenshot:XCUIApplication().screenshot());a.name=name;a.lifetime = .keepAlways;add(a)}
}
