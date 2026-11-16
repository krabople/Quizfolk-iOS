package com.quizfolk.android

import android.app.Application
import androidx.lifecycle.ViewModelStore
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import kotlinx.coroutines.*
import org.json.JSONArray
import org.junit.After
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith

/** No HTTP requests: exercise the real match/store lifecycle against server-shaped responses. */
@RunWith(AndroidJUnit4::class)
class ProgressRecoveryTest {
    private val stores = mutableListOf<QuizStore>()
    private val owners = mutableListOf<ViewModelStore>()
    private val topic = Topic("22", "Geography", "008080", "", 150)

    private fun newStore(api: Transport): QuizStore {
        val store = QuizStore(ApplicationProvider.getApplicationContext<Application>()).apply {
            testing = true; transport = api; ready = true; topics = listOf(topic)
            profile = json("id" to "progress-self", "name" to "Progress Tester", "xp" to 0)
            ownCard = json("id" to "progress-self", "topics" to JSONArray())
        }
        stores += store
        owners += ViewModelStore().apply {
            ViewModelProvider(this, object : ViewModelProvider.Factory {
                @Suppress("UNCHECKED_CAST")
                override fun <T : ViewModel> create(modelClass: Class<T>): T = store as T
            })[QuizStore::class.java]
        }
        return store
    }

    @After fun clearStores() = runBlocking {
        withContext(Dispatchers.Main) {
            stores.forEach { it.game?.stop() }
            owners.forEach { it.clear() }
        }
    }

    private suspend fun idle(store: QuizStore) {
        withTimeout(5000) { while (store.busy) delay(10) }
    }

    private suspend fun completeDuel(store: QuizStore, api: ProgressTransport): GameSession {
        val game = GameSession(store, topic, true, start = api.match())
        store.game = game
        game.begin().join(); game.startDuel().join()
        repeat(7) { turn ->
            game.choose(0).join()
            assertNull(game.error)
            assertEquals(turn + 1, game.rounds.size)
            if (turn < 6) game.next().join()
        }
        return game
    }

    @Test fun seventhAcceptedAnswerRefreshesZeroXpEvenWhenClosedBeforeResults() = runBlocking {
        withContext(Dispatchers.Main) {
            val api = ProgressTransport().apply { playerGate = CompletableDeferred() }
            val store = newStore(api)
            val game = completeDuel(store, api)
            withTimeout(5000) { api.playerReadStarted.await() }
            assertFalse(game.finished) // The player has not pressed See results.
            assertEquals(0, store.onlineTopicXP("22")) // Keep the last confirmed server value.
            game.close()
            api.playerGate!!.complete(Unit)
            idle(store)
            assertNull(store.game)
            assertEquals(300, store.onlineTopicXP("22"))
            assertEquals(300, store.profile!!.n("xp"))
            assertEquals(1, api.calls.count { it == "player" })
            assertFalse(api.calls.contains("social-settings"))
            assertFalse(api.calls.contains("register"))

            val reopened = newStore(api)
            reopened.history = store.history.map { MatchRecord.parse(J(it.json().toString())) }
            reopened.refreshPlayerProgress()
            reopened.refreshPlayerProgress()
            assertEquals(300, reopened.topicXP("22"))
            assertEquals(1, reopened.history.size)
        }
    }

    @Test fun pendingDuelGetsAuthoritativeXpOnceAfterOpponentFinishes() = runBlocking {
        withContext(Dispatchers.Main) {
            val api = ProgressTransport().apply { pending = true }
            val store = newStore(api)
            val game = completeDuel(store, api)
            idle(store)
            assertTrue(store.history.single().pending)
            assertEquals(0, store.topicXP("22"))
            game.close()
            api.pending = false; api.serverXP = 300
            store.refreshSocial()
            assertFalse(store.history.single().pending)
            assertEquals(300, store.topicXP("22"))
            val reads = api.calls.count { it == "player" }
            store.refreshSocial()
            assertEquals(reads, api.calls.count { it == "player" })
            assertEquals(300, store.topicXP("22"))
            assertEquals(1, store.history.size)
        }
    }

    @Test fun existingPracticeHistoryRecoversAfterReopenAndSurvivesServerRefresh() = runBlocking {
        withContext(Dispatchers.Main) {
            val api = ProgressTransport()
            val store = newStore(api)
            val complete = practiceRecord("old-practice")
            val serialized = JSONArray(listOf(complete, complete, complete.copy(id = "unfinished", rounds = complete.rounds.take(6)),
                complete.copy(id = "pending", pending = true), complete.copy(id = "other-topic", topicID = "23"),
                complete.copy(id = "online", kind = "bot")).map { it.json() }).toString()
            store.history = JSONArray(serialized).objects().map(MatchRecord::parse)
            assertEquals(280, store.practiceXP("22"))
            assertEquals(0, store.onlineTopicXP("22"))
            assertEquals(280, store.topicXP("22"))
            assertEquals(0, store.topicXP("unused"))
            api.serverXP = 700
            store.refreshPlayerProgress()
            assertEquals(980, store.topicXP("22"))

            val reopened = newStore(api)
            reopened.history = JSONArray(serialized).objects().map(MatchRecord::parse)
            repeat(2) { reopened.refreshPlayerProgress() }
            assertEquals(280, reopened.practiceXP("22"))
            assertEquals(700, reopened.onlineTopicXP("22"))
            assertEquals(980, reopened.topicXP("22"))
            assertEquals(700, reopened.ownCard!!.a("topics").getJSONObject(0).n("xp"))
        }
    }

    @Test fun practiceFinalAnswerAddsXpAndResultsCelebrateLevelUpOnlyOnce() = runBlocking {
        withContext(Dispatchers.Main) {
            val api = ProgressTransport()
            val store = newStore(api)
            store.history = (0..4).map { practiceRecord("earlier-$it") }
            assertEquals(1400, store.topicXP("22"))
            val game = GameSession(store, topic, false)
            store.game = game
            // Resume at the final answer; use the production offline answer/scoring/save path.
            game.prepared = true; game.intro = false; game.round = 6
            game.rounds = practiceRecord("fixture").rounds.take(6)
            game.score = 120; game.question = ProgressTransport.question(6)
            game.choose(0).join(); game.next().join()
            assertEquals(1700, store.practiceXP("22"))
            assertEquals(0, store.onlineTopicXP("22"))
            assertEquals(2, game.levelUp!!.progress.level)
            val saved = store.history.first()
            game.next().join()
            assertEquals(1700, store.topicXP("22"))
            game.close()
            val reopened = GameSession(store, topic, false, saved = saved)
            store.game = reopened; reopened.begin().join()
            assertNull(reopened.levelUp)
            assertTrue(api.calls.isEmpty())
        }
    }

    @Test fun failedRefreshKeepsConfirmedOnlineAndRecoveredPracticeXp() = runBlocking {
        withContext(Dispatchers.Main) {
            val api = ProgressTransport().apply { serverXP = 700 }
            val store = newStore(api)
            store.history = listOf(practiceRecord("old-practice"))
            store.refreshPlayerProgress()
            api.serverXP = 1000; api.failPlayer = true
            assertTrue(runCatching { store.refreshPlayerProgress() }.isFailure)
            assertEquals(700, store.profile!!.n("xp"))
            assertEquals(980, store.topicXP("22"))
            api.failPlayer = false
            store.refreshPlayerProgress()
            assertEquals(1280, store.topicXP("22"))
        }
    }

    @Test fun allThreePowersWorkOnceInDuelAndTournamentAndDoubleChoiceSurvivesFifty() = runBlocking {
        withContext(Dispatchers.Main) {
            for (tournament in listOf(false, true)) {
                val api = FixtureTransport((0..6).map { ProgressTransport.question(it) })
                val store = newStore(api)
                val game = if (tournament) GameSession(store, topic, true, event = json("id" to "test-event-daily-0"))
                    else GameSession(store, topic, true, start = api.request("match", json(), emptyMap()))
                store.game = game; game.begin().join()
                if (!tournament) game.startDuel().join()
                val initialCoins = api.wallet
                game.usePower(Assist.DOUBLE).join()
                game.usePower(Assist.FIFTY).join()
                assertTrue(game.power.active(Assist.DOUBLE))
                val wrong = (1..3).first { it !in game.power.hidden }
                game.choose(wrong).join()
                assertFalse(game.revealed)
                assertEquals(wrong, game.power.firstWrong)
                assertTrue(wrong in game.power.hidden)
                assertEquals(0, game.score)
                game.usePower(Assist.RIGHT).join()
                assertTrue(game.revealed)
                assertEquals(20, game.score)
                assertEquals(initialCoins - 40, api.wallet)
                game.next().join()
                assertTrue(Assist.entries.all { game.power.hasUsed(it) })
                assertTrue(game.power.hidden.isEmpty())
                val calls = api.calls.size
                for (assist in Assist.entries) game.usePower(assist).join()
                assertEquals(calls, api.calls.size)
                assertEquals(initialCoins - 40, api.wallet)
                assertNull(game.powerError)
                game.stop()
            }
        }
    }

    private fun practiceRecord(id: String) = MatchRecord(id, "22", 1, 140, 0, "Practice Bot", "practice",
        (0..6).map { Round(ProgressTransport.question(it), 0, 1.0, 20, 0) })
}

private class ProgressTransport : Transport {
    val calls = mutableListOf<String>()
    var pending = false
    var serverXP = 0
    var failPlayer = false
    var playerGate: CompletableDeferred<Unit>? = null
    val playerReadStarted = CompletableDeferred<Unit>()
    private var turn = 0
    private val played = mutableListOf<Round>()
    private val score get() = played.sumOf { it.points }
    fun match() = json("id" to "progress-match", "kind" to if (pending) "challenge" else "bot", "opponent" to "Other Player",
        "duelID" to "progress-duel", "score" to score, "opponentScore" to 0, "pending" to pending, "played" to JSONArray(played.map { it.json() }))
    override suspend fun request(route: String, body: J?, query: Map<String, String>): J {
        calls += route
        return when (route) {
            "profile" -> json("id" to "progress-self", "name" to "Progress Tester", "xp" to serverXP)
            "player" -> {
                playerReadStarted.complete(Unit); playerGate?.await()
                check(!failPlayer) { "Player card temporarily unavailable" }
                json("id" to "progress-self", "topics" to JSONArray(listOf(json("topicID" to "22", "xp" to serverXP))))
            }
            "round" -> json("round" to turn, "phase" to "answer", "remaining" to 10, "question" to question(turn).json())
            "answer" -> {
                val points = if (turn == 6) 40 else 20
                played += Round(question(turn), 0, 0.0, points, 0); turn++
                if (turn == 7 && !pending) serverXP = 300
                json("points" to points, "correctIndex" to 0, "selectedIndex" to 0, "score" to score, "opponentPoints" to 0, "opponentScore" to 0, "pending" to pending)
            }
            "match-progress" -> json("opponentAnswered" to 0, "opponentResults" to JSONArray())
            "duels" -> json("duels" to JSONArray(if (turn == 7 && !pending) listOf(json("id" to "progress-duel", "status" to "complete")) else emptyList<J>()))
            "duel-open" -> match()
            "activity" -> json("events" to JSONArray())
            "prizes" -> json("pending" to JSONArray(), "earned" to JSONArray())
            else -> error("Unexpected route: $route")
        }
    }
    companion object {
        fun question(index: Int) = Question("progress-question-$index", "22", "easy", "Test question $index?", listOf("Correct", "Wrong one", "Wrong two", "Wrong three"), 0)
    }
}
