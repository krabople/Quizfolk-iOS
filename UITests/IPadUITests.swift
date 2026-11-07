import XCTest
import UIKit

/// Exercises the normal app views and existing isolated API fixtures on a native iPad.
/// The App Store fixture is intentionally not enabled in this regression suite.
final class IPadUITests:XCTestCase {
    @MainActor override func setUpWithError() throws {
        continueAfterFailure=false
        try XCTSkipUnless(UIDevice.current.userInterfaceIdiom == .pad,"Native iPad layout checks run in the dedicated iPad job")
    }

    @MainActor private func launch(_ orientation:UIDeviceOrientation)->XCUIApplication {
        XCUIDevice.shared.orientation=orientation
        let app=XCUIApplication()
        // Launch-domain defaults avoid inheriting onboarding or interests from another test.
        app.launchArguments=["--ui-testing","-didChooseInterests","YES","-favourites","()"]
        app.launch()
        if app.buttons["Done"].waitForExistence(timeout:2) {app.buttons["Done"].tap()}
        XCTAssertTrue(tab(app,"Discover").waitForExistence(timeout:10))
        waitForOrientation(app,landscape:orientation.isLandscape)
        assertNativeWindow(app)
        return app
    }

    @MainActor private func tab(_ app:XCUIApplication,_ name:String)->XCUIElement {
        let nativeTab=app.tabBars.buttons[name].firstMatch
        return nativeTab.exists ? nativeTab:app.buttons[name].firstMatch
    }

    @MainActor private func waitForOrientation(_ app:XCUIApplication,landscape:Bool) {
        let ready=XCTNSPredicateExpectation(predicate:NSPredicate {_,_ in
            let frame=app.windows.firstMatch.frame
            return landscape ? frame.width>frame.height:frame.height>frame.width
        },object:nil)
        XCTAssertEqual(XCTWaiter.wait(for:[ready],timeout:8),.completed,"App must adopt the iPad's current orientation")
    }

    @MainActor private func assertNativeWindow(_ app:XCUIApplication) {
        let window=app.windows.firstMatch.frame
        let pixels=XCUIScreen.main.screenshot().image.cgImage!
        let scale=UIScreen.main.scale
        // XCTest can retain portrait CGImage backing pixels and encode landscape
        // in UIImage orientation. Compare exact native edges independently of that
        // metadata; waitForOrientation separately verifies the window's orientation.
        let screenEdges=[CGFloat(pixels.width)/scale,CGFloat(pixels.height)/scale].sorted()
        let windowEdges=[window.width,window.height].sorted()
        XCTAssertEqual(window.minX,0,accuracy:3)
        XCTAssertEqual(window.minY,0,accuracy:3)
        XCTAssertEqual(windowEdges[0],screenEdges[0],accuracy:3,"Native iPad must fill the screen without iPhone compatibility bars")
        XCTAssertEqual(windowEdges[1],screenEdges[1],accuracy:3)
        print("Native iPad window:",window,"screen pixels:",pixels.width,pixels.height)
    }

    @MainActor private func reveal(_ element:XCUIElement,in app:XCUIApplication) {
        for _ in 0..<6 {
            if element.isHittable {return}
            app.scrollViews.firstMatch.swipeUp(velocity:500)
        }
        XCTAssertTrue(element.isHittable,"Required control must be reachable: \(element.identifier)")
    }

    @MainActor private func openFirstTopic(_ app:XCUIApplication) {
        let topic=app.descendants(matching:.any).matching(identifier:"topic-9").firstMatch
        XCTAssertTrue(topic.waitForExistence(timeout:8));reveal(topic,in:app);topic.tap()
        XCTAssertTrue(app.buttons["League"].waitForExistence(timeout:8))
    }

    @MainActor private func assertAdaptiveGrid(_ app:XCUIApplication) {
        let first=app.descendants(matching:.any).matching(identifier:"topic-9").firstMatch
        XCTAssertTrue(first.waitForExistence(timeout:8));reveal(first,in:app)
        let tiles=["9","10","11"].map {app.descendants(matching:.any).matching(identifier:"topic-\($0)").firstMatch}
        for tile in tiles {XCTAssertTrue(tile.isHittable,"At least three topic columns should be visible on full-screen iPad")}
        XCTAssertEqual(tiles[0].frame.minY,tiles[1].frame.minY,accuracy:3)
        XCTAssertEqual(tiles[0].frame.minY,tiles[2].frame.minY,accuracy:3)
        XCTAssertGreaterThan(tiles[1].frame.minX,tiles[0].frame.maxX)
        XCTAssertGreaterThan(tiles[2].frame.minX,tiles[1].frame.maxX)
        XCTAssertGreaterThanOrEqual(tiles[0].frame.width,180)
    }

    @MainActor private func startPractice(_ app:XCUIApplication) {
        openFirstTopic(app)
        let practice=app.buttons["Practise against a bot"]
        reveal(practice,in:app);practice.tap()
        XCTAssertTrue(app.buttons["Start duel"].waitForExistence(timeout:8))
        app.buttons["Start duel"].tap()
        XCTAssertTrue(app.buttons["answer-0"].waitForExistence(timeout:10))
    }

    @MainActor private func assertAnswerLayout(_ app:XCUIApplication,landscape:Bool) {
        let answers=(0..<4).map {app.buttons["answer-\($0)"]}
        let window=app.windows.firstMatch.frame.insetBy(dx:-2,dy:-2)
        for answer in answers {
            XCTAssertTrue(answer.isHittable,"All four answers must be visible without scrolling")
            XCTAssertTrue(window.contains(answer.frame),"Answers must stay within the visible iPad window")
            XCTAssertGreaterThanOrEqual(answer.frame.height,60)
        }
        XCTAssertEqual(answers[0].frame.minY,answers[1].frame.minY,accuracy:3)
        XCTAssertEqual(answers[2].frame.minY,answers[3].frame.minY,accuracy:3)
        XCTAssertGreaterThan(answers[2].frame.minY,answers[0].frame.maxY)
        XCTAssertGreaterThan(answers[1].frame.minX,answers[0].frame.maxX)
        let question=app.descendants(matching:.any).matching(identifier:"quizQuestion").firstMatch
        XCTAssertTrue(question.exists)
        if landscape {
            XCTAssertGreaterThanOrEqual(answers[0].frame.minX,question.frame.maxX-3,"Wide iPad places answers beside the question")
        }
        XCTAssertTrue(app.descendants(matching:.any).matching(identifier:"answerTimeBar").firstMatch.exists)
    }

    @MainActor func testPortraitDiscoverGridAndInterestsSheet() {
        let app=launch(.portrait)
        assertAdaptiveGrid(app)
        capture("iPad-Portrait-Discover")
        let interests=app.buttons["Choose interests"]
        // The filter is above the grid; return to the start before opening its sheet.
        app.scrollViews.firstMatch.swipeDown()
        XCTAssertTrue(interests.isHittable);interests.tap()
        XCTAssertTrue(app.staticTexts["What makes you tick?"].waitForExistence(timeout:8))
        XCTAssertTrue(app.buttons["Done"].isHittable)
        capture("iPad-Portrait-Interests")
        app.buttons["Done"].tap()
    }

    @MainActor func testLandscapeDiscoverTopicAndLeague() {
        let app=launch(.landscapeLeft)
        assertAdaptiveGrid(app)
        capture("iPad-Landscape-Discover")
        openFirstTopic(app)
        let overview=app.descendants(matching:.any).matching(identifier:"topicOverview").firstMatch
        let section=app.segmentedControls["topicSection"]
        XCTAssertTrue(overview.waitForExistence(timeout:8))
        let sideBySide=XCTNSPredicateExpectation(predicate:NSPredicate {_,_ in
            overview.frame.width>0 && overview.frame.maxX<section.frame.minX
        },object:nil)
        XCTAssertEqual(XCTWaiter.wait(for:[sideBySide],timeout:8),.completed,"A wide iPad topic page must place its overview beside play and league controls")
        print("Native topic frames: navigation",app.navigationBars.firstMatch.frame,"overview",overview.frame,"section",section.frame)
        capture("iPad-Landscape-Topic")
        let league=app.segmentedControls["topicSection"].buttons["League"]
        league.coordinate(withNormalizedOffset:CGVector(dx:0.5,dy:0.5)).tap()
        let selected=XCTNSPredicateExpectation(predicate:NSPredicate{_,_ in league.isSelected},object:nil)
        XCTAssertEqual(XCTWaiter.wait(for:[selected],timeout:5),.completed,"A real touch must switch the topic to League")
        let rival=app.buttons["league-player-test-rival"]
        XCTAssertTrue(rival.waitForExistence(timeout:8));reveal(rival,in:app)
        XCTAssertTrue(app.buttons["This month"].exists)
        XCTAssertTrue(app.buttons["All time"].exists)
        capture("iPad-Landscape-League")
        rival.tap()
        XCTAssertTrue(app.buttons["followPlayer"].waitForExistence(timeout:8))
    }

    @MainActor func testPortraitDuelHasFourPlayableAnswers() {
        let app=launch(.portrait)
        startPractice(app)
        assertAnswerLayout(app,landscape:false)
        capture("iPad-Portrait-Duel")
        app.buttons["answer-0"].tap()
        XCTAssertTrue(app.buttons["advanceQuestion"].waitForExistence(timeout:8))
    }

    @MainActor func testLandscapeDuelAndRotationPreserveQuestion() {
        let app=launch(.landscapeLeft)
        startPractice(app)
        assertAnswerLayout(app,landscape:true)
        capture("iPad-Landscape-Duel")
        app.buttons["answer-0"].tap()
        let next=app.buttons["advanceQuestion"]
        XCTAssertTrue(next.waitForExistence(timeout:8))
        let question=app.descendants(matching:.any).matching(identifier:"quizQuestion").firstMatch.label
        XCUIDevice.shared.orientation = .portrait
        waitForOrientation(app,landscape:false)
        assertNativeWindow(app)
        XCTAssertEqual(app.descendants(matching:.any).matching(identifier:"quizQuestion").firstMatch.label,question,"Rotation must not restart or replace the current question")
        XCTAssertTrue(next.isHittable)
        capture("iPad-Portrait-RotatedAnswerReview")
        next.tap()
        XCTAssertTrue(app.buttons["answer-0"].waitForExistence(timeout:10))
    }

    @MainActor func testTournamentDetailRotatesAndFriendsSettingsStayReachable() {
        let app=launch(.portrait)
        tab(app,"Tournaments").tap()
        let event=app.descendants(matching:.any).matching(identifier:"tournament-test-event").firstMatch
        XCTAssertTrue(event.waitForExistence(timeout:8));reveal(event,in:app);event.tap()
        let entry=app.buttons["enterTournament"]
        XCTAssertTrue(entry.waitForExistence(timeout:8));reveal(entry,in:app)
        capture("iPad-Portrait-Tournament")
        XCUIDevice.shared.orientation = .landscapeLeft
        waitForOrientation(app,landscape:true);assertNativeWindow(app)
        reveal(entry,in:app);entry.tap()
        let confirm=app.alerts["Enter for 25 coins?"]
        XCTAssertTrue(confirm.waitForExistence(timeout:8))
        capture("iPad-Landscape-TournamentEntry")
        confirm.buttons["Cancel"].tap()
        app.navigationBars.buttons.element(boundBy:0).tap()
        let friends=app.buttons["friendsTournaments"]
        reveal(friends,in:app);friends.tap()
        let create=app.buttons["Create or join a tournament"]
        XCTAssertTrue(create.waitForExistence(timeout:8));create.tap()
        XCTAssertTrue(app.switches["partyPrizes"].waitForExistence(timeout:8))
        XCTAssertTrue(app.buttons["Done"].isHittable)
        capture("iPad-Landscape-FriendsTournamentSettings")
        app.buttons["Done"].tap()
    }

    @MainActor func testLandscapeSocialProfileAndPortraitChallengeSheet() {
        let app=launch(.landscapeLeft)
        tab(app,"People").tap()
        let player=app.descendants(matching:.any).matching(identifier:"player-test-rival").firstMatch
        XCTAssertTrue(player.waitForExistence(timeout:8));player.tap()
        let follow=app.buttons["followPlayer"]
        XCTAssertTrue(follow.waitForExistence(timeout:8));reveal(follow,in:app);follow.tap()
        XCTAssertTrue(app.buttons["Following"].waitForExistence(timeout:8))
        capture("iPad-Landscape-PlayerProfile")
        app.buttons["challengePlayer"].tap()
        let send=app.buttons["sendChallenge"]
        XCTAssertTrue(send.waitForExistence(timeout:8))
        XCUIDevice.shared.orientation = .portrait
        waitForOrientation(app,landscape:false)
        XCTAssertTrue(send.isHittable)
        XCTAssertTrue(app.buttons["Cancel"].isHittable)
        capture("iPad-Portrait-ChallengeComposer")
        app.buttons["Cancel"].tap()
    }

    @MainActor private func capture(_ name:String) {
        let attachment=XCTAttachment(screenshot:XCUIScreen.main.screenshot())
        attachment.name=name;attachment.lifetime = .keepAlways;add(attachment)
    }
}
