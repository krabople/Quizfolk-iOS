package com.quizfolk.android

import android.content.Intent
import android.graphics.Bitmap
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.AndroidComposeTestRule
import androidx.compose.ui.unit.dp
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File

@RunWith(AndroidJUnit4::class)
class QuizfolkScreenTest {
    @get:Rule(order=0) val compose = AndroidComposeTestRule(
        ActivityScenarioRule<MainActivity>(Intent(ApplicationProvider.getApplicationContext<android.content.Context>(), MainActivity::class.java).putExtra("ui_test",true)),
        { rule -> var activity: MainActivity? = null; rule.scenario.onActivity { activity = it }; requireNotNull(activity) }
    )
    @get:Rule(order=1) val failureScreenshot = object : org.junit.rules.TestWatcher() {
        override fun failed(error: Throwable, description: org.junit.runner.Description) { runCatching { capture("Failed-${description.methodName}") } }
    }
    private val store get() = compose.activity.store
    private fun ready() {
        // Configure only the debug app before allowing a service connection.
        compose.runOnUiThread { }
        compose.waitUntil(30000) { store.ready && store.profile != null }
    }
    private fun tapTag(tag: String) = compose.onNodeWithTag(tag).performClick()
    private fun text(text: String) = compose.onNodeWithText(text, useUnmergedTree = true)
    private fun capture(name: String) {
        compose.waitForIdle()
        InstrumentationRegistry.getInstrumentation().waitForIdleSync()
        // Wait for the emulator compositor and the finite answer-slide animation before capturing pixels.
        android.os.SystemClock.sleep(600)
        val bitmap = InstrumentationRegistry.getInstrumentation().uiAutomation.takeScreenshot()
        if (android.os.Build.VERSION.SDK_INT >= 29) {
            val resolver = compose.activity.contentResolver
            val values = android.content.ContentValues().apply {
                put(android.provider.MediaStore.Images.Media.DISPLAY_NAME,"$name.png")
                put(android.provider.MediaStore.Images.Media.MIME_TYPE,"image/png")
                put(android.provider.MediaStore.Images.Media.RELATIVE_PATH,"Pictures/Quizfolk-Screenshots")
            }
            val uri = requireNotNull(resolver.insert(android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI,values))
            resolver.openOutputStream(uri).use { bitmap.compress(Bitmap.CompressFormat.PNG,100,requireNotNull(it)) }
        }
    }
    @Test fun discoverMixedRandomAndTopicLeague() {
        ready(); compose.onNodeWithTag("randomTopic").assertExists(); compose.onNodeWithTag("mixedTopic").assertExists(); capture("Discover")
        tapTag("topicSearch"); compose.onNodeWithTag("topicSearch").performTextInput("Geography"); tapTag("topic-22")
        tapTag("segment-League"); text("This month").assertExists(); text("All time").assertExists(); capture("TopicLeague")
        compose.onNodeWithTag("league-player-test-rival").performScrollTo().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithTag("followPlayer").fetchSemanticsNodes().isNotEmpty() }
        tapTag("followPlayer"); compose.waitUntil(5000) { compose.onAllNodesWithText("Following").fetchSemanticsNodes().isNotEmpty() }
        text("Draw").assertExists(); text("Draws").assertDoesNotExist(); capture("ProfileFromLeague")
    }
    @Test fun settledDuelShowsLevelUpAndHistoryDoesNotCelebrateAgain() {
        ready()
        compose.runOnUiThread {
            val api = store.transport as FixtureTransport
            api.topicXP = 1400; api.duelPending = false
            store.perform { store.connect(); store.game = GameSession(store,store.topic("22"),true) }
        }
        compose.waitUntil(10000) { compose.onAllNodesWithTag("startDuel").fetchSemanticsNodes().isNotEmpty() }; tapTag("startDuel")
        repeat(7) {
            compose.waitUntil(7000) { compose.onAllNodesWithTag("answer-0").fetchSemanticsNodes().isNotEmpty() }
            val right = compose.runOnIdle { store.game!!.question!!.let { q -> store.bank.first { it.id == q.id }.correctIndex } }
            tapTag("answer-$right")
            compose.waitUntil(5000) { compose.onAllNodesWithTag("advanceQuestion").fetchSemanticsNodes().isNotEmpty() }; tapTag("advanceQuestion")
        }
        compose.waitUntil(10000) { compose.onAllNodesWithTag("topicLevelUp").fetchSemanticsNodes().isNotEmpty() }
        text("LEVEL UP!").assertExists(); text("Level 2").assertExists(); capture("TopicLevelUp")
        compose.runOnIdle { assertEquals(1700,store.topicXP("22")); assertEquals(2,store.game!!.levelUp!!.progress.level) }
        compose.onNodeWithText("Back to topics").performScrollTo().performClick()
        compose.runOnUiThread { store.game = GameSession(store,store.topic("22"),true,saved=store.history.first { it.id == "test-match" }) }
        compose.waitUntil(5000) { compose.onAllNodesWithTag("winnerAnnouncement").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithTag("topicLevelUp").assertDoesNotExist()
    }
    @Test fun fullPracticeDuelReadingPowerProgressResultRematchAndFinishedClose() {
        ready()
        compose.runOnIdle {
            assertEquals(32,store.botNames.size); assertEquals(32,store.botNames.toSet().size)
            val names = (0..5).map { store.nextBotName() }
            assertEquals(6,names.toSet().size); assertTrue(names.all { it in store.botNames && it.endsWith(" · Bot") })
        }
        compose.onNodeWithTag("topicSearch").performTextInput("Geography"); tapTag("topic-22")
        compose.onNodeWithTag("practice").performScrollTo().performClick(); compose.waitUntil(15000) { compose.onAllNodesWithTag("startDuel").fetchSemanticsNodes().isNotEmpty() }; capture("Matchup"); tapTag("startDuel")
        compose.waitUntil(7000) { compose.onAllNodesWithTag("readingPhase").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithTag("answer-0").assertDoesNotExist(); capture("Reading")
        repeat(7) { round ->
            compose.waitUntil(7000) { compose.onAllNodesWithTag("answer-0").fetchSemanticsNodes().isNotEmpty() }
            if (round == 0) { compose.onNodeWithTag("answerTimeBar").assertExists(); capture("Question"); tapTag("power-right") }
            else tapTag("answer-0")
            compose.waitUntil(5000) { compose.onAllNodesWithTag("advanceQuestion").fetchSemanticsNodes().isNotEmpty() }
            if (round == 0) { compose.onNodeWithTag("roundMarker-0").assertContentDescriptionEquals("Round 1: correct"); capture("AnswerReview"); assertTrue(store.game!!.power.used) }
            tapTag("advanceQuestion")
        }
        compose.waitUntil(5000) { compose.onAllNodesWithTag("winnerAnnouncement").fetchSemanticsNodes().isNotEmpty() }; capture("Result")
        compose.onNodeWithTag("rematchDuel").performScrollTo().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithTag("startDuel").fetchSemanticsNodes().isNotEmpty() }
        tapTag("leaveMatch"); compose.waitUntil(5000) { store.game == null }; text("An unfinished duel earns no XP.").assertDoesNotExist()
        tapTag("tab-Duels"); tapTag("segment-Device history"); text("Offline practice").assertExists(); capture("History")
    }
    @Test fun profileButtonsCoinsAndPersistentBadgeConfirmation() {
        ready(); tapTag("tab-You"); compose.onNodeWithTag("Earn coins").assertHeightIsEqualTo(96.dp)
        compose.onNodeWithTag("Tournament badges").assertHeightIsEqualTo(96.dp); capture("Profile")
        tapTag("Earn coins"); compose.waitUntil(5000) { compose.onAllNodesWithText("Daily Trail · extra coins").fetchSemanticsNodes().isNotEmpty() }; capture("DailyCoins")
        compose.runOnUiThread { (store.transport as FixtureTransport).pendingPrize = true; store.perform { store.loadPrizes() } }
        compose.waitUntil(5000) { compose.onAllNodesWithText("Wear this badge").fetchSemanticsNodes().isNotEmpty() }; text("Wear this badge").performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithTag("badgeConfirmationDone").fetchSemanticsNodes().isNotEmpty() }; text("Badge added!").assertExists(); capture("BadgeAdded")
        tapTag("badgeConfirmationDone"); compose.runOnIdle { assertEquals("test-prize",store.ownCard?.o("displayBadge")?.s("id")); assertTrue(store.pendingPrizes.isEmpty()) }
    }
    @Test fun tournamentEntryPreflightPreventsEmptyWalletAndShowsFixedPrizes() {
        ready(); compose.runOnUiThread { (store.transport as FixtureTransport).wallet = 0; store.coins = 0 }
        tapTag("tab-Tournaments"); compose.waitUntil(5000) { compose.onAllNodesWithTag("tournament-test-event-daily-0").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithTag("tournament-test-event-daily-0").performScrollTo().performClick()
        compose.onNodeWithTag("enterTournament").performScrollTo().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithText("Not enough coins").fetchSemanticsNodes().isNotEmpty() }; capture("InsufficientCoins")
        compose.runOnIdle { assertEquals(0,(store.transport as FixtureTransport).entries); assertNull(store.game) }
        text("OK").performClick(); compose.onNodeWithText("Guaranteed podium prizes").performScrollTo().assertExists()
        text("150 coins").assertExists(); text("100 coins").assertExists(); text("50 coins").assertExists()
    }
    @Test fun survivalRightAnswerSubmitsOnceAndFirstWrongEndsRun() {
        ready(); tapTag("tab-Tournaments"); compose.waitUntil(5000) { compose.onAllNodesWithTag("tournament-test-event-daily-0").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithTag("tournament-test-event-daily-0").performScrollTo().performClick(); compose.onNodeWithTag("enterTournament").performScrollTo().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithText("Enter · 25 coins", substring = false).fetchSemanticsNodes().isNotEmpty() }
        // The dialog's button is the final entry confirmation.
        compose.onAllNodesWithText("Enter · 25 coins").onLast().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithTag("answer-0").fetchSemanticsNodes().isNotEmpty() }; tapTag("power-right")
        compose.waitUntil(5000) { store.game?.revealed == true }
        compose.runOnIdle {
            assertEquals(1,store.game!!.streak); assertEquals(20,store.game!!.score)
            val api = store.transport as FixtureTransport
            assertEquals(1,api.entries); assertEquals(100,api.wallet)
            assertTrue(api.calls.last { it.first == "tournament-power" }.second!!.b("autoAnswer"))
            assertFalse(api.calls.any { it.first == "tournament-answer" })
        }
        tapTag("advanceQuestion"); compose.waitUntil(5000) { compose.onAllNodesWithTag("answer-0").fetchSemanticsNodes().isNotEmpty() }
        val wrong = compose.runOnIdle { val api = store.transport as FixtureTransport; val q = store.bank.first { it.id == store.game!!.question!!.id }; (q.correctIndex + 1)%4 }
        tapTag("answer-$wrong"); compose.waitUntil(5000) { store.game!!.runEnded }; tapTag("advanceQuestion")
        compose.waitUntil(5000) { compose.onAllNodesWithText("RUN COMPLETE").fetchSemanticsNodes().isNotEmpty() }; capture("SurvivalResult")
    }
    @Test fun previousMatchAndResultPortraitOpenFollowablePlayer() {
        ready(); compose.runOnUiThread {
            val rounds = store.bank.filter { it.categoryID == "22" }.take(7).map { Round(it,it.correctIndex,1.0,19,10) }
            store.save(MatchRecord("saved-human","22",1793836800,133,70,"Sample Rival","human",rounds,opponentID="test-rival"))
        }
        tapTag("tab-Duels"); tapTag("segment-Device history"); compose.onNodeWithTag("history-match-saved-human").performClick()
        tapTag("historyOpponentProfile"); compose.waitUntil(5000) { compose.onAllNodesWithTag("followPlayer").fetchSemanticsNodes().isNotEmpty() }; tapTag("followPlayer")
        compose.waitUntil(5000) { compose.onAllNodesWithText("Following").fetchSemanticsNodes().isNotEmpty() }; capture("FollowFromHistory"); tapTag("back")
        tapTag("historyResult"); compose.waitUntil(5000) { compose.onAllNodesWithTag("winnerAnnouncement").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithContentDescription("View Sample Rival's profile").performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithTag("followPlayer").fetchSemanticsNodes().isNotEmpty() }; text("Following").assertExists(); capture("ProfileFromResult")
    }
    @Test fun privateFriendsTournamentCanBeFreeWithoutPrizes() {
        ready(); tapTag("tab-Tournaments"); tapTag("friendsTournaments"); text("Create or join a tournament").performClick()
        compose.onNodeWithTag("partyPrizes").performScrollTo().performClick()
        text("Free entry · no coins, badges or tournament prizes").assertExists(); capture("FriendsFreeEntry")
        compose.onNodeWithTag("submitParty").performScrollTo().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithText("Invite friends").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithText("Tournament standings").performScrollTo().assertExists(); compose.runOnIdle { assertEquals(0,(store.transport as FixtureTransport).party!!.n("entryCoins")) }; capture("PrivateTournament")
    }
    @Test fun notificationChoicesAreIndependentPersistAndReportUnavailableDelivery() {
        ready();tapTag("tab-You");compose.onNodeWithTag("notificationSettings").performScrollTo().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithTag("push-enabled").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithTag("push-enabled").assertIsOff().performClick()
        compose.waitUntil(5000) { store.notificationChoices.b("enabled") }
        compose.onNodeWithTag("push-challenges").performScrollTo().performClick()
        compose.waitUntil(5000) { !store.notificationChoices.b("challenges") }
        compose.onNodeWithTag("push-tournamentPrizes").performScrollTo().assertIsOn()
        capture("NotificationChoices");tapTag("back")
        compose.onNodeWithTag("notificationSettings").performScrollTo().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithTag("push-challenges").fetchSemanticsNodes().isNotEmpty() }
        compose.onNodeWithTag("push-challenges").performScrollTo().assertIsOff()
        compose.onNodeWithText("Push delivery is not available yet. Your choices will be saved.").performScrollTo().assertExists()
        compose.onNodeWithTag("push-enabled").performScrollTo().performClick()
        compose.waitUntil(5000) { !store.notificationChoices.b("enabled") }
    }
    @Test fun notificationTapKeepsCurrentGameUntilPlayerChoosesToLeave() {
        ready();compose.runOnUiThread { store.game=GameSession(store,store.topic("22"),false) }
        compose.waitUntil(15000) { compose.onAllNodesWithTag("startDuel").fetchSemanticsNodes().isNotEmpty() };tapTag("startDuel")
        compose.waitUntil(7000) { compose.onAllNodesWithTag("readingPhase").fetchSemanticsNodes().isNotEmpty() }
        val original=compose.runOnIdle { store.game!!.id }
        compose.runOnUiThread { store.pendingPush=PushDestination("challenges","test-duel","22") }
        compose.waitUntil(5000) { compose.onAllNodesWithText("Notification saved").fetchSemanticsNodes().isNotEmpty() }
        compose.runOnIdle { assertEquals(original,store.game!!.id);assertNotNull(store.pendingPush) }
        text("OK").performClick();tapTag("leaveMatch");text("Leave duel").performClick()
        compose.waitUntil(5000) { store.game!=null && store.game!!.id!=original && store.game!!.prepared }
        compose.runOnIdle { assertNull(store.pendingPush);assertEquals("Sample Rival",store.game!!.opponent) }
    }
    @Test fun bundledBankAndSecureCredentialStorage() {
        ready(); compose.runOnIdle {
            assertEquals(21667,store.bank.size); assertEquals(31,store.topics.size)
            store.topics.filter { it.id != "mixed" }.forEach { assertTrue(it.count >= 150); assertEquals(it.count,store.bank.count { q -> q.categoryID == it.id }) }
        }
        val context = compose.activity
        val vault = PlayerVault(context); vault.save("https://test.invalid", "only-a-test-key")
        assertEquals("only-a-test-key",vault.read("https://test.invalid")); assertNull(vault.read("https://other.invalid"))
        assertFalse(context.getSharedPreferences("encrypted_player",0).getString("value","")!!.contains("only-a-test-key")); vault.clear()
    }
    @Test fun nativePhotoPickerPreviewAndMetadataFreeUpload() {
        ready()
        val source = File(compose.activity.cacheDir,"picker-photo.jpg")
        val image = Bitmap.createBitmap(500,300,Bitmap.Config.ARGB_8888).apply { eraseColor(android.graphics.Color.RED) }
        source.outputStream().use { image.compress(Bitmap.CompressFormat.JPEG,90,it) }
        androidx.exifinterface.media.ExifInterface(source).apply {
            setAttribute(androidx.exifinterface.media.ExifInterface.TAG_ORIENTATION,"6")
            setAttribute(androidx.exifinterface.media.ExifInterface.TAG_GPS_LATITUDE,"51/1,30/1,0/1")
            setAttribute(androidx.exifinterface.media.ExifInterface.TAG_GPS_LATITUDE_REF,"N")
            setAttribute(androidx.exifinterface.media.ExifInterface.TAG_GPS_LONGITUDE,"0/1,7/1,0/1")
            setAttribute(androidx.exifinterface.media.ExifInterface.TAG_GPS_LONGITUDE_REF,"W")
            saveAttributes()
        }
        androidx.test.espresso.intent.Intents.init()
        try {
            androidx.test.espresso.intent.Intents.intending(androidx.test.espresso.intent.matcher.IntentMatchers.hasAction(android.provider.MediaStore.ACTION_PICK_IMAGES))
                .respondWith(android.app.Instrumentation.ActivityResult(android.app.Activity.RESULT_OK,Intent().setData(android.net.Uri.fromFile(source))))
            tapTag("tab-You"); tapTag("changeProfilePicture")
            compose.waitUntil(8000) { compose.onAllNodesWithText("Use this picture").fetchSemanticsNodes().isNotEmpty() }; capture("PhotoPreview")
            text("Use this picture").performClick()
            compose.waitUntil(5000) { store.avatar != null }
            val bytes = android.util.Base64.decode(store.avatar,android.util.Base64.NO_WRAP)
            val photo = android.graphics.BitmapFactory.decodeByteArray(bytes,0,bytes.size)
            assertEquals(128,photo.width); assertEquals(128,photo.height); assertTrue(bytes.size <= 16384)
            assertNull(androidx.exifinterface.media.ExifInterface(java.io.ByteArrayInputStream(bytes)).getAttribute(androidx.exifinterface.media.ExifInterface.TAG_GPS_LATITUDE))
            compose.waitUntil(5000) { compose.onAllNodesWithText("Picture updated").fetchSemanticsNodes().isNotEmpty() }
            text("OK").performClick(); compose.waitForIdle()
            // Verify the captured native intent directly; a just-dismissed dialog can briefly retain Espresso's root focus.
            assertEquals(1,androidx.test.espresso.intent.Intents.getIntents().count { it.action==android.provider.MediaStore.ACTION_PICK_IMAGES })
        } finally { androidx.test.espresso.intent.Intents.release() }
    }
}
