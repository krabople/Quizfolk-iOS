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
    @get:Rule val compose = AndroidComposeTestRule(
        ActivityScenarioRule<MainActivity>(Intent(ApplicationProvider.getApplicationContext<android.content.Context>(), MainActivity::class.java).putExtra("ui_test",true)),
        { rule -> var activity: MainActivity? = null; rule.scenario.onActivity { activity = it }; requireNotNull(activity) }
    )
    private val store get() = compose.activity.store
    private fun ready() {
        // Configure only the debug app before allowing a service connection.
        compose.runOnUiThread { }
        compose.waitUntil(30000) { store.ready && store.profile != null }
    }
    private fun tapTag(tag: String) = compose.onNodeWithTag(tag).performClick()
    private fun text(text: String) = compose.onNodeWithText(text, useUnmergedTree = true)
    private fun capture(name: String) {
        val bitmap = InstrumentationRegistry.getInstrumentation().uiAutomation.takeScreenshot()
        val folder = File(compose.activity.getExternalFilesDir(null),"screenshots").apply { mkdirs() }
        File(folder,"$name.png").outputStream().use { bitmap.compress(Bitmap.CompressFormat.PNG,100,it) }
    }
    @Test fun discoverMixedRandomAndTopicLeague() {
        ready(); text("Random topic").assertExists(); text("Mixed topics").assertExists(); capture("Discover")
        tapTag("topicSearch"); compose.onNodeWithTag("topicSearch").performTextInput("Geography"); tapTag("topic-22")
        tapTag("segment-League"); text("This month").assertExists(); text("All time").assertExists(); capture("TopicLeague")
        compose.onNodeWithTag("league-player-test-rival").performScrollTo().performClick()
        compose.waitUntil(5000) { compose.onAllNodesWithTag("followPlayer").fetchSemanticsNodes().isNotEmpty() }
        tapTag("followPlayer"); compose.waitUntil(5000) { compose.onAllNodesWithText("Following").fetchSemanticsNodes().isNotEmpty() }; capture("ProfileFromLeague")
    }
    @Test fun fullPracticeDuelReadingPowerProgressResultRematchAndFinishedClose() {
        ready(); compose.onNodeWithTag("topicSearch").performTextInput("Geography"); tapTag("topic-22")
        compose.onNodeWithTag("practice").performScrollTo().performClick(); compose.waitUntil(5000) { compose.onAllNodesWithTag("startDuel").fetchSemanticsNodes().isNotEmpty() }; capture("Matchup"); tapTag("startDuel")
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
}
