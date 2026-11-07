package com.quizfolk.android

import android.content.Intent
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import android.graphics.Bitmap
import android.app.UiAutomation
import android.view.Surface
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.AndroidComposeTestRule
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.After
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/** Runs only in the dedicated tablet CI job, with isolated debug fixture data. */
@RunWith(AndroidJUnit4::class)
class TabletLayoutTest {
    @get:Rule(order=0) val compose = AndroidComposeTestRule(
        ActivityScenarioRule<MainActivity>(Intent(ApplicationProvider.getApplicationContext<android.content.Context>(), MainActivity::class.java).putExtra("ui_test", true)),
        { rule -> var activity: MainActivity? = null; rule.scenario.onActivity { activity = it }; requireNotNull(activity) }
    )
    @get:Rule(order=1) val failureScreenshot = object : org.junit.rules.TestWatcher() {
        override fun failed(error: Throwable, description: org.junit.runner.Description) {
            runCatching { capture("Failed-${description.methodName}") }
        }
    }
    private val store get() = compose.activity.store
    @After fun restoreDeviceRotation() {
        InstrumentationRegistry.getInstrumentation().uiAutomation.setRotation(UiAutomation.ROTATION_UNFREEZE)
    }
    private fun tap(tag: String) = compose.onNodeWithTag(tag).performClick()
    private fun text(value: String) = compose.onNodeWithText(value, useUnmergedTree = true)
    private fun waitFor(tag: String, timeout: Long = 10000) {
        compose.waitUntil(timeout) { compose.onAllNodesWithTag(tag).fetchSemanticsNodes().isNotEmpty() }
    }
    private fun ready() {
        compose.waitUntil(30000) { store.ready && store.profile != null }
        compose.runOnIdle { assertTrue("All tablet requests must stay in the debug fixtures", store.transport is FixtureTransport) }
        rotate(false)
    }
    private fun rotate(landscape: Boolean) {
        val orientation = if (landscape) Configuration.ORIENTATION_LANDSCAPE else Configuration.ORIENTATION_PORTRAIT
        val activity = compose.activity
        val physical = activity.windowManager.maximumWindowMetrics.bounds
        val currentRotation = requireNotNull(activity.display).rotation
        val sideways = currentRotation == Surface.ROTATION_90 || currentRotation == Surface.ROTATION_270
        val naturalLandscape = if (sideways) physical.height() > physical.width() else physical.width() > physical.height()
        // Rotate the device, not only the Activity: forcing a portrait Activity on a
        // landscape tablet display invokes Android's letterbox tutorial and blocks taps.
        compose.runOnUiThread {
            compose.activity.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
        }
        assertTrue("The tablet display must rotate", InstrumentationRegistry.getInstrumentation().uiAutomation.setRotation(
            if (landscape == naturalLandscape) UiAutomation.ROTATION_FREEZE_0 else UiAutomation.ROTATION_FREEZE_90
        ))
        compose.waitUntil(15000) {
            val bounds = compose.activity.windowManager.currentWindowMetrics.bounds
            val screen = compose.activity.windowManager.maximumWindowMetrics.bounds
            compose.activity.resources.configuration.orientation == orientation &&
                (bounds.width() > bounds.height()) == landscape && (screen.width() > screen.height()) == landscape
        }
        compose.waitForIdle()
    }
    private fun assertNativeWindow() {
        val activity = compose.activity
        val bounds = activity.windowManager.currentWindowMetrics.bounds
        val screen = activity.windowManager.maximumWindowMetrics.bounds
        val density = activity.resources.displayMetrics.density
        assertTrue("Tablet must retain native tablet configuration", activity.resources.configuration.smallestScreenWidthDp >= 600)
        assertEquals("The app window must fill the tablet width", screen.width().toFloat(), bounds.width().toFloat(), 24 * density)
        assertEquals("The app window must fill the tablet height", screen.height().toFloat(), bounds.height().toFloat(), 24 * density)
        val root = compose.onNodeWithTag("appRoot").fetchSemanticsNode().boundsInRoot
        assertEquals("Content must use native window width", bounds.width().toFloat(), root.width, 24 * density)
        assertEquals("Content must use native window height", bounds.height().toFloat(), root.height, 40 * density)
    }
    private fun assertThreeTopicColumns() {
        compose.onNodeWithTag("topic-9").performScrollTo()
        val tiles = listOf("9", "10", "11").map { compose.onNodeWithTag("topic-$it").fetchSemanticsNode().boundsInRoot }
        assertEquals("Tablet should show at least three subjects in a row", tiles[0].top, tiles[1].top, 3f)
        assertEquals("Tablet should show at least three subjects in a row", tiles[0].top, tiles[2].top, 3f)
        assertTrue(tiles[0].left < tiles[1].left && tiles[1].left < tiles[2].left)
    }
    private fun assertAllAnswersVisible() {
        waitFor("answer-0")
        val tiles = (0..3).map { index ->
            compose.onNodeWithTag("answer-$index").assertIsDisplayed().assertHasClickAction().fetchSemanticsNode().boundsInRoot
        }
        val root = compose.onNodeWithTag("appRoot").fetchSemanticsNode().boundsInRoot
        tiles.forEach { tile ->
            assertTrue("Each complete answer must fit in the viewport", tile.left >= root.left && tile.top >= root.top && tile.right <= root.right + 1 && tile.bottom <= root.bottom + 1)
        }
        assertEquals("First answer pair must share a row", tiles[0].top, tiles[1].top, 3f)
        assertEquals("Second answer pair must share a row", tiles[2].top, tiles[3].top, 3f)
        assertTrue(tiles[2].top > tiles[0].bottom && tiles[1].left > tiles[0].left)
    }
    private fun capture(name: String) {
        compose.waitForIdle()
        InstrumentationRegistry.getInstrumentation().waitForIdleSync()
        android.os.SystemClock.sleep(600)
        val bitmap = InstrumentationRegistry.getInstrumentation().uiAutomation.takeScreenshot()
        val resolver = compose.activity.contentResolver
        val values = android.content.ContentValues().apply {
            put(android.provider.MediaStore.Images.Media.DISPLAY_NAME, "Tablet-$name.png")
            put(android.provider.MediaStore.Images.Media.MIME_TYPE, "image/png")
            put(android.provider.MediaStore.Images.Media.RELATIVE_PATH, "Pictures/Quizfolk-Screenshots")
        }
        val uri = requireNotNull(resolver.insert(android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values))
        resolver.openOutputStream(uri).use { bitmap.compress(Bitmap.CompressFormat.PNG, 100, requireNotNull(it)) }
    }

    @Test fun nativeDiscoveryAdaptsInPortraitAndLandscape() {
        ready(); assertNativeWindow(); assertThreeTopicColumns(); capture("Topics-Portrait")
        rotate(true); assertNativeWindow(); assertThreeTopicColumns()
        compose.onNodeWithTag("navigationRail").assertIsDisplayed(); capture("Topics-Landscape")
        tap("tab-People"); waitFor("player-test-rival")
        compose.onNodeWithTag("player-test-rival").performScrollTo().performClick(); waitFor("followPlayer")
        compose.onNodeWithTag("followPlayer").performScrollTo().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithText("Following").fetchSemanticsNodes().isNotEmpty() }
        capture("Player-Landscape")
        rotate(false); assertNativeWindow(); text("Following").assertExists(); capture("Player-Portrait")
    }

    @Test fun playableDuelPreservesScoreAndQuestionAcrossRotation() {
        ready()
        compose.runOnUiThread { store.game = GameSession(store, store.topic("22"), false) }
        waitFor("startDuel", 15000); tap("startDuel"); waitFor("answer-0")
        val session = compose.runOnIdle { store.game!! }
        val correct = compose.runOnIdle { session.question!!.correctIndex }
        // Submit while the real ten-second clock is running. Layout inspection and
        // screenshot encoding follow the answer, so CI rendering cannot consume it.
        tap("answer-$correct"); waitFor("advanceQuestion")
        val score = compose.runOnIdle { session.score }
        val question = compose.runOnIdle { session.question!!.id }
        assertTrue("First correct answer must award points", score > 0)
        assertAllAnswersVisible(); compose.onNodeWithTag("answerTimeBar").assertIsDisplayed()
        capture("AnswerReview-Portrait")
        rotate(true); assertNativeWindow()
        compose.runOnIdle {
            assertSame("Rotation must keep the active duel", session, store.game)
            assertEquals(score, session.score); assertEquals(0, session.round); assertEquals(question, session.question!!.id)
            assertTrue(session.revealed); assertEquals(1, session.rounds.size)
        }
        compose.onNodeWithTag("advanceQuestion").assertIsDisplayed(); capture("AnswerReview-Landscape")
        tap("advanceQuestion"); waitFor("answer-0"); capture("Question-Landscape"); assertAllAnswersVisible()
        compose.runOnIdle { assertEquals(1, session.round); assertEquals(score, session.score) }
        val secondQuestion = compose.runOnIdle { session.question!!.id }
        rotate(false)
        compose.runOnIdle { assertSame(session, store.game); assertEquals(1, session.round); assertEquals(secondQuestion, session.question!!.id); assertEquals(score, session.score) }
        assertAllAnswersVisible(); capture("Question-After-Rotation")
    }

    @Test fun profileAndNotificationControlsRemainReachableWhenRotated() {
        ready(); rotate(true); tap("tab-You"); assertNativeWindow(); capture("Profile-Landscape")
        compose.onNodeWithTag("notificationSettings").performScrollTo().performClick(); waitFor("push-enabled")
        compose.onNodeWithTag("push-enabled").assertIsOff().performClick()
        compose.waitUntil(5000) { store.notificationChoices.b("enabled") }
        rotate(false); compose.onNodeWithTag("push-enabled").assertIsOn()
        compose.onNodeWithTag("push-challenges").performScrollTo().performClick()
        compose.waitUntil(5000) { !store.notificationChoices.b("challenges") }
        capture("Notifications-Portrait")
        rotate(true); compose.onNodeWithTag("push-challenges").assertIsOff(); capture("Notifications-Landscape")
    }

    @Test fun tournamentAndPrizeDialogsWorkInLandscape() {
        ready(); rotate(true); tap("tab-Tournaments"); waitFor("tournament-test-event-daily-0")
        compose.onNodeWithTag("tournament-test-event-daily-0").performScrollTo().performClick()
        compose.onNodeWithTag("enterTournament").performScrollTo().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithText("Enter · 25 coins").fetchSemanticsNodes().isNotEmpty() }
        text("Cancel").assertIsDisplayed(); capture("Tournament-Entry-Landscape"); text("Cancel").performClick()
        compose.onNodeWithText("Guaranteed podium prizes").performScrollTo().assertExists(); capture("Tournament-Landscape")
        compose.runOnUiThread { (store.transport as FixtureTransport).pendingPrize = true; store.perform { store.loadPrizes() } }
        compose.waitUntil(5000) { compose.onAllNodesWithText("Wear this badge").fetchSemanticsNodes().isNotEmpty() }
        text("Wear this badge").assertIsDisplayed(); capture("Prize-Landscape"); text("Wear this badge").performClick()
        waitFor("badgeConfirmationDone"); text("Badge added!").assertExists(); tap("badgeConfirmationDone")
        compose.runOnIdle { assertEquals("test-prize", store.ownCard?.o("displayBadge")?.s("id")); assertTrue(store.pendingPrizes.isEmpty()) }
    }
}
