import XCTest
import UIKit

/// Uses the DEBUG-only provider and server fixture. These tests never request an ad.
final class RewardedAdUITests:XCTestCase {
    @MainActor override func setUpWithError() throws {continueAfterFailure=false}
    @MainActor private func launch(_ flags:[String]=[])->XCUIApplication {
        XCUIDevice.shared.orientation = .portrait
        let app=XCUIApplication()
        app.launchArguments=["--ui-testing","-didChooseInterests","YES"]+flags
        app.launch()
        let native=app.tabBars.buttons["You"].firstMatch
        let tab=native.waitForExistence(timeout:6) ? native:app.buttons["You"].firstMatch
        XCTAssertTrue(tab.waitForExistence(timeout:8));tab.tap()
        let earn=app.buttons["Earn coins"]
        XCTAssertTrue(earn.waitForExistence(timeout:8));reveal(earn,in:app);earn.tap()
        XCTAssertTrue(app.navigationBars["Daily Trail"].waitForExistence(timeout:6))
        return app
    }
    @MainActor private func reveal(_ element:XCUIElement,in app:XCUIApplication) {
        for _ in 0..<8 {if element.isHittable{return};app.swipeUp(velocity:500)}
        XCTAssertTrue(element.isHittable,"Rewarded control must remain reachable")
    }
    @MainActor private func loadAndShow(_ app:XCUIApplication) {
        let load=app.buttons["rewardedLoad"]
        XCTAssertTrue(load.waitForExistence(timeout:6));reveal(load,in:app)
        let enabled=XCTNSPredicateExpectation(predicate:NSPredicate(format:"isEnabled == true"),object:load)
        XCTAssertEqual(XCTWaiter.wait(for:[enabled],timeout:6),.completed);load.tap()
        let show=app.buttons["rewardedShow"]
        XCTAssertTrue(show.waitForExistence(timeout:6));reveal(show,in:app);show.tap()
        XCTAssertTrue(app.buttons["rewardedFixtureComplete"].waitForExistence(timeout:6))
    }
    @MainActor private func capture(_ app:XCUIApplication,_ name:String) {
        // Capture the physical screen: app.screenshot() can crop its rotated window.
        let attachment=XCTAttachment(screenshot:XCUIScreen.main.screenshot());attachment.name=name;attachment.lifetime = .keepAlways;add(attachment)
    }
    @MainActor private func assertLandscapeViewport(_ app:XCUIApplication,control:XCUIElement) {
        guard UIDevice.current.userInterfaceIdiom == .pad else{return}
        let settled=XCTNSPredicateExpectation(predicate:NSPredicate {_,_ in
            let frame=app.windows.firstMatch.frame
            return frame.width>frame.height
        },object:nil)
        XCTAssertEqual(XCTWaiter.wait(for:[settled],timeout:8),.completed)
        let window=app.windows.firstMatch.frame
        let pixels=XCUIScreen.main.screenshot().image.cgImage!
        let screen=[CGFloat(pixels.width)/UIScreen.main.scale,CGFloat(pixels.height)/UIScreen.main.scale].sorted()
        let edges=[window.width,window.height].sorted()
        XCTAssertEqual(window.minX,0,accuracy:3);XCTAssertEqual(window.minY,0,accuracy:3)
        XCTAssertEqual(edges[0],screen[0],accuracy:3);XCTAssertEqual(edges[1],screen[1],accuracy:3)
        XCTAssertTrue(control.isHittable)
        XCTAssertGreaterThanOrEqual(control.frame.minX,window.minX)
        XCTAssertLessThanOrEqual(control.frame.maxX,window.maxX)
        XCTAssertGreaterThanOrEqual(control.frame.minY,window.minY)
        XCTAssertLessThanOrEqual(control.frame.maxY,window.maxY)
        print("Rewarded landscape viewport:",window,"control:",control.frame)
    }
    @MainActor func testCompletedVideoAddsExactlyFiveCoinsAndAllowsAnother() {
        let app=launch();loadAndShow(app)
        if UIDevice.current.userInterfaceIdiom == .pad {XCUIDevice.shared.orientation = .landscapeLeft}
        let complete=app.buttons["rewardedFixtureComplete"]
        assertLandscapeViewport(app,control:complete)
        XCTAssertTrue(complete.isHittable);capture(app,"RewardedVideo-Native");complete.tap()
        XCTAssertTrue(app.staticTexts["rewardedConfirmed"].waitForExistence(timeout:8))
        XCTAssertTrue(app.staticTexts["115 coins"].exists)
        XCTAssertFalse(app.staticTexts.matching(NSPredicate(format:"label CONTAINS 'videos available today'")).firstMatch.exists)
        assertLandscapeViewport(app,control:app.buttons["rewardedLoad"])
        capture(app,"RewardedConfirmed-Native")
        XCUIDevice.shared.orientation = .portrait
        loadAndShow(app);app.buttons["rewardedFixtureComplete"].tap()
        XCTAssertTrue(app.staticTexts["120 coins"].waitForExistence(timeout:8))
    }
    @MainActor func testClosingVideoEarlyDoesNotAddCoins() {
        let app=launch();loadAndShow(app);app.buttons["rewardedFixtureClose"].tap()
        XCTAssertTrue(app.staticTexts["Video closed before completion. No coins were added."].waitForExistence(timeout:8))
        XCTAssertTrue(app.staticTexts["110 coins"].exists)
        XCTAssertFalse(app.staticTexts["rewardedConfirmed"].exists)
        XCTAssertTrue(app.buttons["rewardedLoad"].isEnabled)
    }
    @MainActor func testNoFillAndConsentRefusalLeaveWalletUnchanged() {
        for flag in ["--rewarded-no-fill","--rewarded-consent-denied"] {
            let app=launch([flag]);let load=app.buttons["rewardedLoad"]
            XCTAssertTrue(load.waitForExistence(timeout:6));reveal(load,in:app);load.tap()
            XCTAssertTrue(app.staticTexts["rewardedMessage"].waitForExistence(timeout:8))
            XCTAssertFalse(app.buttons["rewardedShow"].exists)
            XCTAssertTrue(app.staticTexts["110 coins"].exists)
            if flag == "--rewarded-no-fill" {
                let details=app.buttons["Failure details"]
                XCTAssertTrue(details.waitForExistence(timeout:5));reveal(details,in:app);details.tap()
                let copy=app.buttons["rewardedCopyFailure"]
                reveal(copy,in:app);copy.tap()
                XCTAssertTrue(app.staticTexts["rewardedFailureCopied"].waitForExistence(timeout:5))
                capture(app,"RewardedFailureDetails-Native")
            } else {
                XCTAssertFalse(app.buttons["Failure details"].exists,"Consent refusal must not be mislabeled as a Google load failure")
            }
            app.terminate()
        }
    }
    @MainActor func testPendingRewardSurvivesRelaunchAndPrivacyChoicesRemainAvailable() {
        let app=launch(["--rewarded-pending"]);loadAndShow(app)
        app.buttons["rewardedFixtureComplete"].tap()
        XCTAssertTrue(app.staticTexts["rewardedPending"].waitForExistence(timeout:8))
        XCTAssertTrue(app.staticTexts["110 coins"].exists)
        app.terminate()
        let resumed=launch(["--rewarded-resume"])
        XCTAssertTrue(resumed.staticTexts["115 coins"].waitForExistence(timeout:8))
        XCTAssertFalse(resumed.buttons["rewardedFixtureComplete"].exists)
        let privacy=resumed.buttons["rewardedPrivacy"]
        XCTAssertTrue(privacy.waitForExistence(timeout:6));reveal(privacy,in:resumed);privacy.tap()
        XCTAssertTrue(resumed.alerts["Ad privacy choices"].waitForExistence(timeout:6))
        resumed.alerts.buttons["Done"].tap()
    }
    @MainActor func testLostStartResponseCanRecoverAndReleaseUnusedReservation() {
        let app=launch(["--rewarded-start-lost"])
        let load=app.buttons["rewardedLoad"]
        XCTAssertTrue(load.waitForExistence(timeout:6));reveal(load,in:app);load.tap()
        XCTAssertTrue(app.staticTexts["rewardedMessage"].waitForExistence(timeout:8))
        XCTAssertTrue(load.isEnabled);load.tap()
        XCTAssertTrue(app.staticTexts["rewardedPending"].waitForExistence(timeout:8))
        let cancel=app.buttons["rewardedCancel"]
        reveal(cancel,in:app);cancel.tap()
        XCTAssertTrue(load.waitForExistence(timeout:6));loadAndShow(app)
        app.buttons["rewardedFixtureComplete"].tap()
        XCTAssertTrue(app.staticTexts["115 coins"].waitForExistence(timeout:8))
    }
}
