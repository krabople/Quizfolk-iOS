import XCTest
import UIKit

/// Opt-in marketing captures. Run only through the manual store-screenshots workflow.
final class StoreScreenshotTests:XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure=false
        try XCTSkipUnless(ProcessInfo.processInfo.environment["STORE_SCREENSHOTS"]=="1", "App Store captures are opt-in")
    }
    @MainActor private func launch()->XCUIApplication {
        XCUIDevice.shared.orientation = .portrait
        let app=XCUIApplication()
        app.launchArguments=["--ui-testing","--store-screenshots"]
        app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        XCTAssertTrue(tab(app,"Discover").waitForExistence(timeout:8))
        if ProcessInfo.processInfo.environment["CAPTURE_DEVICE"]=="ipad-13" {
            let window=app.windows.firstMatch.frame
            let pixels=XCUIScreen.main.screenshot().image.cgImage!
            let scale=UIScreen.main.scale
            XCTAssertEqual(window.width,CGFloat(pixels.width)/scale,accuracy:3,"iPad app must fill the native screen, without iPhone compatibility margins")
            XCTAssertEqual(window.height,CGFloat(pixels.height)/scale,accuracy:3)
            print("Native iPad viewport:",window,"screen pixels:",pixels.width,pixels.height)
        }
        return app
    }
    @MainActor private func tab(_ app:XCUIApplication,_ title:String)->XCUIElement {
        let tab=app.tabBars.buttons[title].firstMatch
        return tab.exists ? tab:app.buttons[title].firstMatch
    }
    @MainActor private func scroll(_ app:XCUIApplication,velocity:XCUIGestureVelocity = .default) {
        if ProcessInfo.processInfo.environment["CAPTURE_DEVICE"]=="ipad-13" {app.scrollViews.firstMatch.swipeUp(velocity:velocity)}
        else {app.swipeUp(velocity:velocity)}
    }
    @MainActor private func capture(_ name:String) {
        let shot=XCTAttachment(screenshot:XCUIScreen.main.screenshot())
        shot.name="STORE-"+name;shot.lifetime = .keepAlways;add(shot)
    }
    @MainActor private func topic(_ app:XCUIApplication) {
        if ProcessInfo.processInfo.environment["CAPTURE_DEVICE"]=="ipad-13" {
            // Use the real interests filter so the keyboard does not cover the grid.
            let interests=app.buttons["My interests"]
            XCTAssertTrue(interests.waitForExistence(timeout:8));interests.tap()
        } else {
            let field=app.textFields["Search categories"]
            XCTAssertTrue(field.waitForExistence(timeout:8));field.tap();field.typeText("Geography")
        }
        let link=app.descendants(matching:.any).matching(identifier:"topic-22").firstMatch
        for _ in 0..<3 {if link.isHittable{break};scroll(app)}
        XCTAssertTrue(link.waitForExistence(timeout:8));link.tap()
        XCTAssertTrue(app.buttons["League"].waitForExistence(timeout:8))
    }
    @MainActor func test01Topics() {
        let app=launch()
        if ProcessInfo.processInfo.environment["CAPTURE_DEVICE"]=="ipad-13" {
            let first=app.descendants(matching:.any).matching(identifier:"topic-9").firstMatch
            XCTAssertTrue(first.waitForExistence(timeout:8));XCTAssertTrue(first.isHittable)
            capture("02-topics")
            return
        }
        let interests=app.buttons["Choose interests"]
        XCTAssertTrue(interests.waitForExistence(timeout:8));interests.tap()
        XCTAssertTrue(app.staticTexts["What makes you tick?"].waitForExistence(timeout:8))
        capture("02-topics")
    }
    @MainActor func test02Gameplay() {
        let app=launch();topic(app)
        let duel=app.buttons["Find a duel"]
        for _ in 0..<4 {if duel.isHittable{break};scroll(app)}
        XCTAssertTrue(duel.waitForExistence(timeout:8));duel.tap()
        let start=app.buttons["Start duel"]
        XCTAssertTrue(start.waitForExistence(timeout:12));start.tap()
        XCTAssertTrue(app.buttons["answer-0"].waitForExistence(timeout:12))
        for n in 0..<4 {XCTAssertTrue(app.buttons["answer-\(n)"].isHittable)}
        capture("01-duel")
    }
    @MainActor func test03Challenges() {
        let app=launch();tab(app,"Duels").tap()
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
        let heading=app.staticTexts["Geography league"]
        XCTAssertTrue(heading.waitForExistence(timeout:8))
        let targetY=app.navigationBars.firstMatch.frame.maxY+16
        let delta=heading.frame.minY-targetY
        if delta>20,ProcessInfo.processInfo.environment["CAPTURE_DEVICE"] != "ipad-13" {
            let scrollView=app.scrollViews.firstMatch
            let start=scrollView.coordinate(withNormalizedOffset:CGVector(dx:0.5,dy:0.78))
            let end=start.withOffset(CGVector(dx:0,dy:-delta))
            start.press(forDuration:0.1,thenDragTo:end,withVelocity:.slow,thenHoldForDuration:0.3)
        }
        // The topic heading must remain visible rather than sliding under the navigation bar.
        XCTAssertGreaterThanOrEqual(heading.frame.minY,app.navigationBars.firstMatch.frame.maxY-2)
        capture("05-topic-league")
    }
    @MainActor func test06Tournament() {
        let app=launch();tab(app,"Tournaments").tap()
        let event=app.descendants(matching:.any).matching(identifier:"tournament-test-event").firstMatch
        for _ in 0..<3 {if event.isHittable{break};scroll(app)}
        XCTAssertTrue(event.waitForExistence(timeout:8));event.tap()
        XCTAssertTrue(app.buttons["enterTournament"].waitForExistence(timeout:8))
        scroll(app,velocity:300)
        capture("06-tournament")
    }
    @MainActor func test07Friends() {
        let app=launch();tab(app,"Tournaments").tap()
        XCTAssertTrue(app.buttons["friendsTournaments"].waitForExistence(timeout:8));app.buttons["friendsTournaments"].tap()
        let room=app.buttons.matching(NSPredicate(format:"label CONTAINS 'Friday quiz club'")).firstMatch
        XCTAssertTrue(room.waitForExistence(timeout:8));room.tap()
        XCTAssertTrue(app.buttons["friends-league-player-test-self"].waitForExistence(timeout:8))
        capture("07-friends")
    }
    @MainActor func test08Badges() {
        let app=launch();tab(app,"You").tap()
        XCTAssertTrue(app.buttons["Tournament badges"].waitForExistence(timeout:8));app.buttons["Tournament badges"].tap()
        XCTAssertTrue(app.buttons["earnedBadge-test-prize"].waitForExistence(timeout:8))
        capture("08-badges")
    }
    @MainActor func test09Profile() {
        let app=launch();tab(app,"People").tap()
        let player=app.descendants(matching:.any).matching(identifier:"player-test-rival").firstMatch
        XCTAssertTrue(player.waitForExistence(timeout:8));player.tap()
        XCTAssertTrue(app.buttons["followPlayer"].waitForExistence(timeout:8))
        capture("09-rival-profile")
    }
    @MainActor func test10Result() {
        let app=launch();tab(app,"Duels").tap();app.buttons["Device history"].tap()
        let history=app.buttons["history-match-history-fixture"]
        XCTAssertTrue(history.waitForExistence(timeout:8));history.tap()
        XCTAssertTrue(app.buttons["historyResult"].waitForExistence(timeout:8));app.buttons["historyResult"].tap()
        XCTAssertTrue(app.descendants(matching:.any).matching(identifier:"winnerAnnouncement").firstMatch.waitForExistence(timeout:8))
        capture("10-result")
    }
}
