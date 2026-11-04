package com.quizfolk.android

import android.os.SystemClock
import androidx.compose.runtime.*
import kotlinx.coroutines.*
import java.util.UUID
import kotlin.math.max
import kotlin.random.Random

/** One controller for a seven-round duel or an unlimited survival run. Online time and scores always come from the server. */
class GameSession(val store: QuizStore, val topic: Topic, val online: Boolean, private val start: J? = null,
    val event: J? = null, private val admitted: J? = null, private val saved: MatchRecord? = null) {
    val id = UUID.randomUUID().toString()
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)
    private var clock: Job? = null
    private var reader: Job? = null
    private var progress: Job? = null
    private var closed = false
    private var background = false
    private var searchID: String? = null
    private val requestID = UUID.randomUUID().toString()
    private var offlineDeck: List<Question> = emptyList()
    private var readDeadline = 0L
    private var answerDeadline = 0L
    private var pendingIndex: Int? = null
    private var pendingElapsed = 0.0
    private var serverID = ""
    var question by mutableStateOf<Question?>(null)
    var rounds by mutableStateOf<List<Round>>(emptyList())
    var round by mutableIntStateOf(0)
    var score by mutableIntStateOf(0)
    var opponentScore by mutableIntStateOf(0)
    var opponent by mutableStateOf("Pip · Bot")
    var opponentID by mutableStateOf<String?>(null)
    var opponentAvatar by mutableStateOf<String?>(null)
    var duelID by mutableStateOf<String?>(null)
    var kind by mutableStateOf("bot")
    var pending by mutableStateOf(false)
    var prepared by mutableStateOf(false)
    var searching by mutableStateOf(online && start == null && event == null && saved == null)
    var intro by mutableStateOf(event == null && saved == null)
    var counting by mutableStateOf(false)
    var countdown by mutableIntStateOf(3)
    var reading by mutableStateOf(false)
    var remaining by mutableDoubleStateOf(10.0)
    var selected by mutableStateOf<Int?>(null)
    var revealed by mutableStateOf(false)
    var finished by mutableStateOf(false)
    var runEnded by mutableStateOf(false)
    var streak by mutableIntStateOf(0)
    var lastPoints by mutableIntStateOf(0)
    var busy by mutableStateOf(false)
    var error by mutableStateOf<String?>(null)
    var powerError by mutableStateOf<String?>(null)
    var power by mutableStateOf(Power())
    var powerAllowed by mutableStateOf(true)
    var opponentAnswered by mutableIntStateOf(0)
    var opponentResults by mutableStateOf<List<Boolean?>>(emptyList())
    val survival get() = event != null
    val human get() = online && kind != "bot"
    val canClose get() = finished || runEnded || (!survival && rounds.size == 7) || (intro && question == null)

    fun begin() = scope.launch {
        if (prepared || busy || closed) return@launch
        busy = true; error = null
        try {
            if (saved != null) {
                serverID = saved.id; kind = if (saved.kind == "practice") "bot" else saved.kind; opponent = saved.opponent
                opponentID = saved.opponentID; opponentAvatar = saved.opponentAvatar; duelID = saved.duelID
                rounds = saved.rounds; score = saved.score; opponentScore = saved.opponentScore; pending = saved.pending
                question = rounds.lastOrNull()?.question; round = max(0, rounds.size - 1); prepared = true; finished = true; revealed = true; intro = false; searching = false
                return@launch
            }
            if (survival) {
                store.authenticated()
                val reply = admitted ?: store.api("tournament-enter", json("event" to event!!.s("id"), "requestID" to requestID))
                serverID = reply.s("id"); applyRun(reply); prepared = true; intro = false; loadRound()
            } else if (online) {
                store.authenticated()
                if (start != null) applyStart(start) else {
                    for (attempt in 0..6) {
                        ensureActive(); if (closed) return@launch
                        val reply = store.api("match-search", json("topic" to topic.id, "requestID" to requestID))
                        searchID = reply.s("searchID")
                        if (reply.o("match") != null) { applyStart(reply.getJSONObject("match")); break }
                        delay(2000)
                    }
                    check(serverID.isNotEmpty()) { "The search took too long. Please try again." }
                }
                prepared = true
            } else {
                offlineDeck = withContext(Dispatchers.Default) { freshPacket(store.bank, store.history, topic.id) }
                check(offlineDeck.size == 7) { "This topic needs seven different questions. Please choose another topic." }
                prepared = true
            }
        } catch (e: Exception) { if (e is CancellationException) throw e; error = e.message }
        finally { busy = false; searching = false }
    }
    private fun applyStart(r: J) {
        serverID = r.s("id"); kind = r.s("kind", "bot"); opponent = r.s("opponent", "Pip · Bot")
        opponentID = r.s("opponentID").ifEmpty { null }; opponentAvatar = r.s("opponentAvatar").ifEmpty { null }; duelID = r.s("duelID").ifEmpty { null }
        pending = r.b("pending"); powerAllowed = r.b("powerAllowed", true)
        rounds = r.a("played").objects().map(Round::parse); score = r.n("score"); opponentScore = r.n("opponentScore")
        round = rounds.size; opponentAnswered = if (kind == "human") 7 else 0
        if (rounds.size == 7) { round = 6; question = rounds.last().question; revealed = true; finished = true; saveResult() }
    }
    fun startDuel() = scope.launch {
        if (!prepared || busy || counting || closed) return@launch
        counting = true
        try {
            for (n in 3 downTo 1) { countdown = n; delay(1000) }
            intro = false; busy = true
            if (online) { loadRound(); pollProgress() } else offlineQuestion()
        } catch (e: Exception) { if (e is CancellationException) throw e; error = e.message }
        finally { counting = false; busy = false }
    }
    private fun applyRun(r: J) {
        score = r.n("score"); streak = r.n("streak"); round = r.n("turn"); runEnded = r.s("state", "playing") != "playing"
    }
    private suspend fun loadRound() {
        val r = store.api(if (survival) "tournament-round" else "round", json((if (survival) "run" else "match") to serverID))
        if (survival) { applyRun(r); if (runEnded) { finished = true; return } } else round = r.n("round")
        selected = null; revealed = false; pendingIndex = null; powerError = null; power = r.o("power")?.let(Power::parse) ?: power.next()
        applyQuestion(r)
    }
    private fun applyQuestion(r: J) {
        r.o("question")?.let { question = Question.parse(it, topic.id) }
        reading = r.s("phase") == "reading"; remaining = r.d("remaining", 10.0)
        if (reading) {
            clock?.cancel(); reader?.cancel()
            reader = scope.launch {
                try {
                    delay((r.d("readingRemaining", 3.0).coerceAtLeast(0.0) * 1000).toLong())
                    if (closed || background) return@launch
                    val reply = store.api(if (survival) "tournament-reveal" else "reveal", json((if (survival) "run" else "match") to serverID))
                    if (survival) { applyRun(reply); if (runEnded) { finished = true; return@launch } }
                    // Do not cancel the task which is applying its own successful response.
                    reader = null; applyQuestion(reply)
                } catch (e: Exception) { if (e is CancellationException) throw e; error = e.message }
            }
        } else startClock(remaining)
    }
    private fun offlineQuestion() {
        clock?.cancel(); reader?.cancel(); question = offlineDeck[round]; selected = null; revealed = false; power = power.next(); powerError = null
        reading = true; remaining = 10.0; readDeadline = SystemClock.elapsedRealtime() + 3000; answerDeadline = readDeadline + 10000
        offlineRead()
    }
    private fun offlineRead() {
        reader = scope.launch {
            delay((readDeadline - SystemClock.elapsedRealtime()).coerceAtLeast(0))
            if (!closed && !background) { reading = false; startClock((answerDeadline - SystemClock.elapsedRealtime()) / 1000.0) }
        }
    }
    private fun startClock(seconds: Double) {
        clock?.cancel(); remaining = seconds.coerceAtLeast(0.0); answerDeadline = SystemClock.elapsedRealtime() + (remaining * 1000).toLong()
        clock = scope.launch {
            while (isActive && !closed && !revealed && !background) {
                remaining = ((answerDeadline - SystemClock.elapsedRealtime()) / 1000.0).coerceAtLeast(0.0)
                if (remaining <= 0 && !busy) { scope.launch { answer(-1) }; return@launch }
                delay(50)
            }
        }
    }
    private fun pollProgress() {
        progress?.cancel()
        if (!online || survival) return
        progress = scope.launch {
            while (isActive && !closed && !finished) {
                try {
                    val r = store.api("match-progress", json("match" to serverID)); opponentAnswered = r.n("opponentAnswered")
                    val results = r.a("opponentResults"); opponentResults = (0 until results.length()).map { if (results.isNull(it)) null else results.getBoolean(it) }
                } catch (e: Exception) { if (e is CancellationException) throw e }
                delay(8000)
            }
        }
    }
    fun choose(index: Int) = scope.launch { answer(index) }
    private suspend fun answer(index: Int) {
        if (busy || reading || revealed || finished || runEnded || closed) return
        val q = question ?: return; clock?.cancel(); selected = index; pendingIndex = index; pendingElapsed = (10 - remaining).coerceAtLeast(0.0)
        busy = true; error = null
        try {
            if (online) {
                val reply = store.api(if (survival) "tournament-answer" else "answer", if (survival) json("run" to serverID, "turn" to round, "answer" to index) else json("match" to serverID, "round" to round, "answer" to index))
                if (reply.b("questionChanged")) { pendingIndex = null; loadRound(); return }
                if (reply.b("retry")) { power = Power.parse(reply.o("power")); selected = null; pendingIndex = null; startClock(reply.d("remaining", remaining)); return }
                complete(reply, q, index, pendingElapsed)
            } else {
                if (power.type == "double" && power.hidden.isEmpty() && index >= 0 && index != q.correctIndex && remaining > 0) {
                    power = power.copy(hidden = setOf(index)); selected = null; pendingIndex = null; startClock(remaining); return
                }
                val points = Scoring.points(index == q.correctIndex, pendingElapsed, round)
                val chance = when (q.difficulty) { "easy" -> .83; "hard" -> .45; else -> .65 }
                val other = Scoring.points(Random.nextDouble() < chance, Random.nextDouble(1.2,9.8), round)
                complete(json("points" to points, "correctIndex" to q.correctIndex, "selectedIndex" to index, "score" to score + points,
                    "opponentPoints" to other, "opponentScore" to opponentScore + other), q, index, pendingElapsed)
            }
        } catch (e: Exception) { if (e is CancellationException) throw e; error = e.message }
        finally { busy = false }
    }
    private fun complete(reply: J, q: Question, fallback: Int, elapsed: Double) {
        clock?.cancel(); selected = reply.n("selectedIndex", fallback); question = q.copy(correctIndex = reply.n("correctIndex", q.correctIndex)); lastPoints = reply.n("points")
        if (survival) applyRun(reply) else {
            score = reply.n("score"); opponentScore = reply.n("opponentScore"); pending = reply.b("pending")
            rounds = rounds + Round(question!!, selected!!, elapsed, lastPoints, reply.n("opponentPoints"))
            if (kind == "bot" || !online) { opponentAnswered = rounds.size; opponentResults = rounds.map { it.opponentPoints > 0 } }
            if (rounds.size == 7) saveResult()
        }
        revealed = true; reading = false; pendingIndex = null
    }
    fun usePower(assist: Assist) = scope.launch {
        val q = question ?: return@launch
        if (busy || reading || revealed || finished || runEnded || power.used || !powerAllowed || remaining <= 0) return@launch
        busy = true; powerError = null
        try {
            if (online) {
                val r = store.api(if (survival) "tournament-power" else "power", json((if (survival) "run" else "match") to serverID,
                    "turn" to round, "type" to assist.key, "autoAnswer" to (assist == Assist.RIGHT)))
                power = Power.parse(r.o("power")); store.coins = r.n("coins"); remaining = r.d("remaining", remaining)
                val answer = r.o(if (survival) "tournamentAnswer" else "duelAnswer")
                if (answer != null) complete(answer, q, answer.n("correctIndex"), r.d("acceptedElapsed", (10 - remaining).coerceAtLeast(0.0))) else startClock(remaining)
            } else power = Power(true, assist.key,
                if (assist == Assist.FIFTY) q.answers.indices.filter { it != q.correctIndex }.shuffled().take(2).toSet() else emptySet(), if (assist == Assist.RIGHT) q.correctIndex else null)
        } catch (e: Exception) { if (e is CancellationException) throw e; powerError = e.message }
        finally { busy = false }
        if (assist == Assist.RIGHT && !revealed && power.used && power.highlight != null) answer(power.highlight!!)
        else if (remaining <= 0 && !revealed) answer(-1)
    }
    fun next() = scope.launch {
        if (!revealed || busy) return@launch
        if (survival && runEnded || !survival && rounds.size == 7) {
            finished = true
            if (!survival) saveResult()
            if (online) store.perform { store.connect(); store.refreshSocial(); store.loadPrizes() }
            return@launch
        }
        busy = true; error = null
        try { if (online) loadRound() else { round++; offlineQuestion() } }
        catch (e: Exception) { if (e is CancellationException) throw e; error = e.message }
        finally { busy = false }
    }
    private fun saveResult() {
        if (rounds.size != 7) return
        store.save(MatchRecord(if (online) serverID else id, topic.id, System.currentTimeMillis() / 1000, score, opponentScore, opponent,
            if (online) kind else "practice", rounds, duelID, pending, opponentID, opponentAvatar))
    }
    fun retry() = scope.launch {
        error = null
        if (!prepared) { begin(); return@launch }
        val retry = pendingIndex
        if (retry != null) { pendingIndex = null; revealed = false; busy = false; answer(retry) }
        else if (intro) startDuel()
        else { busy = true; try { loadRound() } catch (e: Exception) { if (e is CancellationException) throw e; error = e.message } finally { busy = false } }
    }
    fun refreshResult() = scope.launch {
        val duel = duelID ?: return@launch; busy = true
        try { applyStart(store.api("duel-open", json("duel" to duel))); store.connect(); store.refreshSocial() }
        catch (e: Exception) { if (e is CancellationException) throw e; error = e.message }
        finally { busy = false }
    }
    fun close() {
        if (survival && !runEnded && serverID.isNotEmpty()) {
            scope.launch { busy = true; try { applyRun(store.api("tournament-end", json("run" to serverID))); store.game = null; stop() }
                catch (e: Exception) { if (e is CancellationException) throw e; error = e.message; busy = false } }
        } else { store.game = null; stop() }
    }
    fun onBackground() { background = true; clock?.cancel(); reader?.cancel(); progress?.cancel() }
    fun onForeground() = scope.launch {
        if (!background || closed) return@launch; background = false
        if (intro || finished || revealed || busy || !prepared) return@launch
        try {
            if (online) { loadRound(); pollProgress() }
            else if (reading) offlineRead() else startClock((answerDeadline - SystemClock.elapsedRealtime()) / 1000.0)
        } catch (e: Exception) { if (e is CancellationException) throw e; error = e.message }
    }
    fun stop() {
        if (closed) return; closed = true; scope.cancel()
        searchID?.let { search -> store.perform { store.api("cancel-search", json("searchID" to search)) } }
    }
}
