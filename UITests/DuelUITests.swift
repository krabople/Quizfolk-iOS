import XCTest
final class DuelUITests:XCTestCase {
    @MainActor func testNotificationPreferencesAreSeparateAndHonestAboutDelivery() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:8) {app.buttons["Done"].tap()}
        app.tabBars.buttons["You"].tap()
        let link=app.buttons["notificationSettings"]
        for _ in 0..<5 {if link.isHittable {break};app.swipeUp()}
        XCTAssertTrue(link.waitForExistence(timeout:5));link.tap()
        let master=app.switches["push-enabled"];XCTAssertTrue(master.waitForExistence(timeout:5));XCTAssertEqual(master.value as? String,"0")
        // SwiftUI exposes the entire labelled row as a switch; tap the trailing native control.
        master.coordinate(withNormalizedOffset:CGVector(dx:0.92,dy:0.5)).tap()
        XCTAssertEqual(XCTWaiter.wait(for:[XCTNSPredicateExpectation(predicate:NSPredicate(format:"value == %@","1"),object:master)],timeout:5),.completed)
        let challenges=app.switches["push-challenges"];challenges.coordinate(withNormalizedOffset:CGVector(dx:0.92,dy:0.5)).tap()
        XCTAssertEqual(XCTWaiter.wait(for:[XCTNSPredicateExpectation(predicate:NSPredicate(format:"value == %@","0"),object:challenges)],timeout:5),.completed)
        XCTAssertEqual(app.switches["push-tournamentPrizes"].value as? String,"1")
        XCTAssertTrue(app.staticTexts["push-unavailable"].exists);capture("NotificationChoices")
    }
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
            if i==0 {
                for n in 0..<4 {XCTAssertTrue(app.buttons["answer-\(n)"].isHittable,"Every answer must be visible without scrolling")}
                XCTAssertEqual(app.buttons["answer-0"].frame.minY,app.buttons["answer-1"].frame.minY,accuracy:3)
                XCTAssertGreaterThan(app.buttons["answer-2"].frame.minY,app.buttons["answer-0"].frame.minY)
                XCTAssertTrue(app.descendants(matching:.any).matching(identifier:"duelProgress").firstMatch.exists)
            }
            if i==0 {XCTAssertTrue(app.otherElements["roundTimer"].exists);XCTAssertTrue(app.descendants(matching:.any).matching(identifier:"answerTimeBar").firstMatch.exists);capture("Question")}
            if i==0 {app.buttons["power-right"].tap()}else if option.isEnabled {option.tap()}
            let next=app.buttons["advanceQuestion"]
            if !next.isHittable {app.swipeUp()}
            XCTAssertTrue(next.waitForExistence(timeout:12))
            if i==0 {
                let marker=app.descendants(matching:.any).matching(identifier:"roundMarker-0").firstMatch
                XCTAssertTrue(marker.label.contains(": correct") || marker.label.contains(": incorrect"))
                XCTAssertTrue(marker.label.contains(": correct"),"Right Answer must select and submit the correct option automatically")
                let rival=app.descendants(matching:.any).matching(identifier:"opponentRoundMarker-0").firstMatch
                XCTAssertTrue(rival.label.contains(": correct") || rival.label.contains(": incorrect"))
                capture("AnswerReview")
            }
            next.tap()
        }
        let back=app.buttons["Back to topics"]
        if !back.isHittable {app.swipeUp();app.swipeUp()}
        XCTAssertTrue(back.waitForExistence(timeout:8));capture("Result")
        let rematch=app.buttons["rematchDuel"];for _ in 0..<6{if rematch.isHittable{break};app.swipeDown()};XCTAssertTrue(rematch.waitForExistence(timeout:5));rematch.tap()
        XCTAssertTrue(app.buttons["Start duel"].waitForExistence(timeout:8));XCTAssertFalse(app.descendants(matching:.any).matching(identifier:"winnerAnnouncement").firstMatch.exists)
        app.buttons["Leave match"].tap();XCTAssertFalse(app.buttons["Leave duel"].exists)
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
        // The simulator's Photos service can take more than 30 seconds to
        // initialise after importing its first image. Still require selection
        // and the actual preview; a slow system picker is not an app failure.
        XCTAssertTrue(image.waitForExistence(timeout:60),app.debugDescription)
        capture("PhotoPicker")
        image.tap()
        XCTAssertTrue(app.staticTexts["Your player picture"].waitForExistence(timeout:15))
        XCTAssertTrue(app.buttons["Use this picture"].isHittable)
        capture("PicturePreview")
        app.buttons["Cancel"].tap()
        XCTAssertTrue(picker.waitForExistence(timeout:5))
    }
    @MainActor func testFreeFriendsTournamentSetting() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        app.tabBars.buttons["Tournaments"].tap()
        let friends=app.buttons["friendsTournaments"]
        XCTAssertTrue(friends.waitForExistence(timeout:8));friends.tap()
        let composer=app.buttons["Create or join a tournament"]
        XCTAssertTrue(composer.waitForExistence(timeout:8));composer.tap()
        let prizes=app.switches["partyPrizes"]
        XCTAssertTrue(prizes.waitForExistence(timeout:8))
        // SwiftUI exposes both the labelled row and the trailing UISwitch.
        // Tapping the row's centre hits its label; target the actual control.
        let control=prizes.switches.firstMatch
        XCTAssertTrue(control.waitForExistence(timeout:5));control.tap()
        XCTAssertTrue(app.staticTexts["Free entry · no coins, badges or tournament prizes"].waitForExistence(timeout:5))
        capture("FreeFriendsTournamentSettings")
        let create=app.buttons["Create free · no prizes"]
        for _ in 0..<3 {if create.exists{break};app.swipeUp()}
        XCTAssertTrue(create.waitForExistence(timeout:5))
        app.buttons["Done"].tap()
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
        let rivalry=app.descendants(matching:.any).matching(identifier:"headToHead").firstMatch
        XCTAssertTrue(rivalry.exists)
        XCTAssertTrue(rivalry.label.contains("1 draw · 3 completed meetings"),"A single drawn game must use the singular label")
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
        app.buttons["league-player-test-rival"].tap()
        XCTAssertTrue(app.buttons["followPlayer"].waitForExistence(timeout:5));capture("ProfileFromTopicLeague")
        app.navigationBars.buttons.element(boundBy:0).tap()
        app.tabBars.buttons["Tournaments"].tap()
        let event=app.descendants(matching:.any).matching(identifier:"tournament-test-event").firstMatch
        XCTAssertTrue(event.waitForExistence(timeout:5));capture("Tournaments");event.tap()
        XCTAssertTrue(app.buttons["enterTournament"].waitForExistence(timeout:5))
        XCTAssertTrue(app.staticTexts["Guaranteed podium prizes"].exists)
        XCTAssertTrue(app.staticTexts["150 coins"].exists)
        XCTAssertTrue(app.staticTexts["100 coins"].exists)
        XCTAssertTrue(app.staticTexts["50 coins"].exists)
        XCTAssertTrue(app.descendants(matching:.any).matching(identifier:"tournamentRules").firstMatch.exists)
        capture("TournamentRules")
    }
    @MainActor func testTournamentEntryUsesCentralConfirmation() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        app.tabBars.buttons["Tournaments"].tap()
        let event=app.descendants(matching:.any).matching(identifier:"tournament-test-event").firstMatch
        XCTAssertTrue(event.waitForExistence(timeout:5));event.tap()
        XCTAssertTrue(app.buttons["enterTournament"].waitForExistence(timeout:5));app.buttons["enterTournament"].tap()
        let alert=app.alerts["Enter for 25 coins?"]
        XCTAssertTrue(alert.waitForExistence(timeout:5));XCTAssertTrue(alert.buttons["Cancel"].exists)
        capture("TournamentEntryConfirmation");alert.buttons["Cancel"].tap()
        XCTAssertTrue(app.buttons["enterTournament"].exists)
    }
    @MainActor func testPreviousMatchOpensOpponentProfileForFollowing() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing","--history-fixture"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        app.tabBars.buttons["Duels"].tap();app.buttons["Device history"].tap()
        let match=app.buttons["history-match-history-fixture"];XCTAssertTrue(match.waitForExistence(timeout:5));match.tap()
        XCTAssertTrue(app.buttons["historyRematch"].waitForExistence(timeout:5))
        app.buttons["historyOpponentProfile"].tap()
        XCTAssertTrue(app.buttons["followPlayer"].waitForExistence(timeout:5));app.buttons["followPlayer"].tap()
        XCTAssertTrue(app.buttons["Following"].waitForExistence(timeout:5));capture("FollowFromPreviousMatch")
        app.navigationBars.buttons.element(boundBy:0).tap();app.buttons["historyResult"].tap()
        let portrait=app.buttons["resultProfile-test-rival"];XCTAssertTrue(portrait.waitForExistence(timeout:5));capture("CompletedHumanDuel")
        portrait.tap();XCTAssertTrue(app.buttons["followPlayer"].waitForExistence(timeout:5));XCTAssertTrue(app.buttons["Following"].exists)
    }
    @MainActor func testInsufficientCoinsStaysOnTournamentDetails() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing","--ui-testing-empty-wallet"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        app.tabBars.buttons["Tournaments"].tap()
        let event=app.descendants(matching:.any).matching(identifier:"tournament-test-event").firstMatch
        XCTAssertTrue(event.waitForExistence(timeout:5));event.tap()
        XCTAssertTrue(app.buttons["enterTournament"].waitForExistence(timeout:5));app.buttons["enterTournament"].tap()
        let alert=app.alerts["Not enough coins"]
        XCTAssertTrue(alert.waitForExistence(timeout:5));capture("TournamentInsufficientCoins")
        XCTAssertFalse(app.staticTexts["Preparing your run…"].exists)
        alert.buttons["OK"].tap();XCTAssertTrue(app.buttons["enterTournament"].exists)
        XCTAssertFalse(app.buttons["Close tournament run"].exists)
    }
    @MainActor func testTournamentCongratulationsAcknowledgedOnce() {
        let app=launchWithPrize()
        XCTAssertTrue(app.staticTexts["Congratulations!"].waitForExistence(timeout:8))
        XCTAssertTrue(app.staticTexts["You finished in 1st place"].exists)
        XCTAssertTrue(app.staticTexts["Prize: 150 coins"].exists);capture("TournamentCongratulations")
        app.buttons["Continue"].tap()
        XCTAssertTrue(app.tabBars.buttons["You"].waitForExistence(timeout:5))
        app.tabBars.buttons["You"].tap()
        XCTAssertFalse(app.descendants(matching:.any).matching(NSPredicate(format:"label CONTAINS 'profile picture, tournament'")).firstMatch.exists)
        XCUIDevice.shared.press(.home);app.activate()
        XCTAssertTrue(app.buttons["changeProfilePicture"].waitForExistence(timeout:8))
        XCTAssertFalse(app.staticTexts["Congratulations!"].exists,"Acknowledged prizes must not reopen after returning to the app")
        app.buttons["Tournament badges"].tap()
        XCTAssertTrue(app.buttons.matching(NSPredicate(format:"label CONTAINS 'Geography · 1st place'")).firstMatch.waitForExistence(timeout:5))
    }
    @MainActor func testTournamentBadgesShowTopicAndEvent() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        app.tabBars.buttons["You"].tap();app.buttons["Tournament badges"].tap()
        let daily=app.buttons["earnedBadge-test-prize"],weekly=app.buttons["earnedBadge-test-weekly"],friends=app.buttons["earnedBadge-test-friends"]
        XCTAssertTrue(daily.waitForExistence(timeout:8));XCTAssertTrue(daily.label.contains("Geography"))
        XCTAssertTrue(weekly.exists);XCTAssertTrue(weekly.label.contains("Weekly tournament"))
        XCTAssertTrue(friends.exists);XCTAssertTrue(friends.label.contains("Friends tournament"))
        capture("DistinctTournamentBadges")
    }
    @MainActor func testWearTournamentBadgeAndRemoveIt() {
        let app=launchWithPrize()
        XCTAssertTrue(app.buttons["Wear this badge"].waitForExistence(timeout:8));app.buttons["Wear this badge"].tap()
        XCTAssertTrue(app.staticTexts["Badge added!"].waitForExistence(timeout:5));capture("BadgeAddedConfirmation")
        app.buttons["badgeConfirmationDone"].tap()
        XCTAssertTrue(app.tabBars.buttons["You"].waitForExistence(timeout:5));app.tabBars.buttons["You"].tap()
        let portrait=app.descendants(matching:.any).matching(identifier:"UI Player profile picture, tournament 1st place badge").firstMatch
        XCTAssertTrue(portrait.waitForExistence(timeout:5));capture("TournamentBadgeOnProfile")
        app.buttons["Tournament badges"].tap()
        XCTAssertTrue(app.buttons["No tournament badge"].waitForExistence(timeout:5));app.buttons["No tournament badge"].tap()
        app.navigationBars.buttons.element(boundBy:0).tap()
        XCTAssertTrue(app.buttons["changeProfilePicture"].waitForExistence(timeout:5));XCTAssertFalse(portrait.exists)
    }
    @MainActor func testCoinTrailShowsProgressAndUnusedTopics() {
        let app=XCUIApplication();app.launchArguments=["--ui-testing"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        app.tabBars.buttons["You"].tap()
        let earn=app.buttons["Earn coins"],badges=app.buttons["Tournament badges"]
        XCTAssertTrue(earn.waitForExistence(timeout:5));XCTAssertTrue(badges.exists)
        XCTAssertEqual(earn.frame.width,badges.frame.width,accuracy:2)
        XCTAssertEqual(earn.frame.height,badges.frame.height,accuracy:2)
        XCTAssertEqual(earn.frame.minY,badges.frame.minY,accuracy:2);capture("ProfileActionButtons")
        earn.tap()
        XCTAssertTrue(app.navigationBars["Daily Trail"].waitForExistence(timeout:5))
        XCTAssertTrue(app.staticTexts["110 coins"].waitForExistence(timeout:5))
        XCTAssertTrue(app.staticTexts["10 / 45 earned today"].exists)
        XCTAssertTrue(app.staticTexts["10 coins earned"].exists)
        XCTAssertTrue(app.staticTexts["2 of 5 daily trails · earn 50 bonus coins"].exists);capture("DailyCoinTrail")
        XCTAssertFalse(app.buttons["Geography"].exists,"A topic already credited today must not be offered again")
        let next=app.buttons.matching(NSPredicate(format:"label CONTAINS 'General Knowledge'")).firstMatch
        for _ in 0..<6 {if next.isHittable {break};app.swipeUp()}
        XCTAssertTrue(next.waitForExistence(timeout:5));next.tap()
        XCTAssertTrue(app.buttons["League"].waitForExistence(timeout:5))
    }
    @MainActor private func launchWithPrize()->XCUIApplication {
        let app=XCUIApplication();app.launchArguments=["--ui-testing","--prize-popup"];app.launch()
        if app.buttons["Done"].waitForExistence(timeout:3){app.buttons["Done"].tap()}
        return app
    }
    @MainActor private func capture(_ name:String) {let a=XCTAttachment(screenshot:XCUIApplication().screenshot());a.name=name;a.lifetime = .keepAlways;add(a)}
}
