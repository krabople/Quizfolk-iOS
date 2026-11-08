package com.quizfolk.android

import android.content.Context
import org.json.JSONArray

@Suppress("UNUSED_PARAMETER")
fun fixtureTransport(context: Context, bank: List<Question>): Transport = FixtureTransport(bank.filter { it.categoryID == "22" }.take(7))

/** Emulator-only service: never contacts production, creates players or spends real coins. */
class FixtureTransport(private val questions: List<Question>) : Transport {
    var notificationChoices = defaultPushChoices()
    var wallet = 150
    var claimed = true
    var following = false
    var selectedBadge: J? = null
    var pendingPrize = false
    var acknowledged = false
    var entries = 0
    var party: J? = null
    var powerUsed = false
    var turn = 0
    var score = 0
    var topicXP = 700
    var duelPending = true
    private var xpAwarded = false
    var streak = 0
    var state = "playing"
    var avatar: String? = null
    var name = "UI Player"
    val calls = mutableListOf<Pair<String,J?>>()
    private var cachedAnswer: J? = null
    private val admitted = mutableMapOf<String,J>()
    val prize: J get() = json("id" to "test-prize", "topicID" to "22", "kind" to "daily", "rank" to 1, "coins" to 150, "date" to 1793836800, "score" to 120)
    private fun card(id: String = "test-rival"): J = json("id" to id, "name" to if (id == "test-self") name else "Sample Rival", "avatar" to if (id == "test-self") avatar else null,
        "title" to "Newcomer", "interests" to JSONArray(listOf("22","17")), "sharedTopics" to JSONArray(listOf("22")), "following" to following,
        "followers" to if (following) 1 else 0, "followingCount" to 0, "canChallenge" to (id != "test-self"),
        "stats" to json("matches" to 4, "wins" to 2, "draws" to 1, "xp" to topicXP, "correct" to 20, "answered" to 28, "perfect" to 1),
        "topics" to JSONArray(listOf(json("topicID" to "22", "xp" to topicXP, "level" to TopicLevelling.progress(topicXP).level, "matches" to 4, "wins" to 2))),
        "titles" to JSONArray(listOf(json("id" to "newcomer", "name" to "Newcomer"))), "selectedTitle" to "newcomer", "discoverable" to true,
        "challengesOpen" to true, "headToHead" to json("games" to 3, "wins" to 1, "draws" to 1, "losses" to 1),
        "badges" to JSONArray(listOf(json("id" to "first", "name" to "First duel", "symbol" to "bolt.fill", "earned" to true))), "displayBadge" to if (id == "test-self") selectedBadge else null)
    private fun event(index: Int = 0, weekly: Boolean = false): J = json("id" to "test-event-${if (weekly) "weekly" else "daily"}-$index", "topicID" to "22", "kind" to if (weekly) "weekly" else "daily", "starts" to 1793830000,
        "ends" to 1893836800, "coins" to if (weekly) 50 else 25, "tickets" to 0, "closed" to false, "best" to score, "streak" to streak, "attempts" to entries,
        "players" to 1, "activeRun" to null, "rank" to null, "reward" to 0, "featured" to true, "prizePool" to if (weekly) 1750 else 875,
        "prizes" to JSONArray(if (weekly) listOf(1000,500,250) else listOf(500,250,125)))
    private fun wallet() = json("coins" to wallet, "tickets" to 0, "dailyClaimed" to false)
    private fun run() = json("id" to "test-run", "eventID" to "test-event-daily-0", "score" to score, "streak" to streak, "turn" to turn, "state" to state)
    private fun q() = questions[turn % questions.size]
    private fun start(): J { turn = 0; score = 0; powerUsed = false; cachedAnswer = null; xpAwarded = false; return json("id" to "test-match", "kind" to "challenge", "opponent" to "Sample Rival", "opponentID" to "test-rival", "duelID" to "test-duel", "pending" to duelPending, "powerAllowed" to true) }
    private fun awardDuelXP() { if (turn == 7 && !duelPending && !xpAwarded) { topicXP += Scoring.experience(score,0); xpAwarded = true } }
    override suspend fun request(route: String, body: J?, query: Map<String,String>): J {
        calls.add(route to body?.copyJson())
        return when (route) {
            "notification-settings" -> json("preferences" to notificationChoices.copyJson(), "delivery" to json("ios" to false, "android" to false))
            "notification-preferences" -> { notificationChoices=body!!.getJSONObject("preferences").copyJson();json("preferences" to notificationChoices.copyJson(),"delivery" to json("ios" to false,"android" to false)) }
            "notification-device" -> json("ok" to true)

            "register" -> json("token" to "emulator-only-token")
            "profile" -> json("id" to "test-self", "socialVersion" to 1, "name" to name, "avatar" to avatar, "matches" to 4, "wins" to 2, "xp" to 700, "correct" to 20, "answered" to 28)
            "player" -> card(query["id"] ?: "test-self")
            "social-settings", "block", "report", "cancel-search", "duel-decline" -> json("ok" to true)
            "update-profile" -> { require(body!!.s("name") != "Taken Name") { "That player name is already in use." }; name = body.s("name"); json("ok" to true) }
            "update-avatar" -> { avatar = body!!.s("avatar").ifEmpty { null }; json("ok" to true) }
            "daily-login" -> { val awarded = if (claimed) 0 else 50; wallet += awarded; claimed = true; json("wallet" to wallet(), "awarded" to awarded, "day" to "2026-11-04", "resets" to 1793923200) }
            "coins" -> json("wallet" to wallet(), "topics" to JSONArray(listOf("22")), "earnedToday" to 10, "dailyMaximum" to 45, "completedDays" to 2, "weeklyBonusEarned" to false, "loginClaimed" to claimed, "resets" to 1793923200)
            "prizes" -> json("pending" to JSONArray(if (pendingPrize && !acknowledged) listOf(prize) else emptyList<J>()), "earned" to JSONArray(listOf(prize)), "selected" to selectedBadge, "wallet" to wallet())
            "select-badge" -> { selectedBadge = if (body!!.s("event").isEmpty()) null else prize; if (body.b("acknowledge")) acknowledged = true; json("ok" to true, "acknowledged" to body.b("acknowledge")) }
            "prize-seen" -> { acknowledged = true; json("ok" to true) }
            "follow" -> { following = body!!.b("enabled"); json("ok" to true) }
            "people" -> json("players" to JSONArray(if (query["mode"] == "following" && !following) emptyList<J>() else listOf(card())))
            "activity" -> json("events" to JSONArray())
            "duels" -> json("duels" to JSONArray())
            "leaderboard" -> json("entries" to JSONArray(listOf(json("id" to "test-rival", "name" to "Sample Rival", "avatar" to null, "xp" to 700, "matches" to 4))))
            "challenge", "duel-open", "party-play", "match" -> start()
            "match-search" -> json("searchID" to "test-search", "state" to "matched", "elapsed" to 6, "match" to start())
            "match-progress" -> json("ownAnswered" to turn, "opponentAnswered" to turn, "opponentResults" to JSONArray((0 until 7).map { if (it < turn) it % 2 == 0 else null }))
            "round", "reveal" -> json("round" to turn, "question" to q().json().apply { remove("correctIndex") }, "remaining" to 10, "phase" to "answer")
            "answer" -> { if (body!!.n("round") < turn && cachedAnswer != null) cachedAnswer!! else {
                val right = body.n("answer") == q().correctIndex; val points = Scoring.points(right, 0.0, turn); val correct = q().correctIndex
                score += points; turn++; awardDuelXP(); json("points" to points, "selectedIndex" to body.n("answer"), "correctIndex" to correct, "opponentPoints" to 0, "finished" to (turn == 7), "score" to score, "opponentScore" to 0, "pending" to duelPending).also { cachedAnswer = it }
            } }
            "power", "tournament-power" -> {
                check(!powerUsed) { "Only one power-up is allowed." }; val type = body!!.s("type"); val price = Assist.entries.first { it.key == type }.price; check(wallet >= price) { "Not enough coins." }; wallet -= price; powerUsed = true
                val correct = q().correctIndex; val state = json("used" to true, "type" to type, "hidden" to JSONArray(if (type == "fifty") q().answers.indices.filter { it != correct }.take(2) else emptyList()), "highlight" to if (type == "right") correct else null)
                val response = json("power" to state, "remaining" to 9.9, "acceptedElapsed" to .1, "coins" to wallet)
                if (type == "right" && body.b("autoAnswer")) {
                    score += if (route == "power" && turn == 6) 40 else 20; turn++; streak++
                    if (route == "power") awardDuelXP()
                    val answer = if (route == "power") json("selectedIndex" to correct, "correctIndex" to correct, "points" to if (turn == 7) 40 else 20, "opponentPoints" to 0, "finished" to (turn == 7), "score" to score, "opponentScore" to 0, "pending" to duelPending)
                        else run().put("selectedIndex", correct).put("correctIndex", correct).put("points",20).put("correct",true)
                    cachedAnswer = answer; response.put(if (route == "power") "duelAnswer" else "tournamentAnswer", answer)
                }; response
            }
            "tournaments" -> json("events" to JSONArray((0..2).map { event(it) } + (0..2).map { event(it, true) }), "wallet" to wallet())
            "tournament-board" -> json("event" to event(weekly = query["event"]?.contains("weekly") == true), "entries" to JSONArray(listOf(json("id" to "test-rival", "name" to "Sample Rival", "avatar" to null, "rank" to 1, "score" to 100, "streak" to 5, "reward" to 0))), "own" to JSONArray(), "wallet" to wallet())
            "tournament-enter" -> { val key = body!!.s("requestID"); admitted[key] ?: run {
                val fee = if (body.s("event").contains("weekly")) 50 else 25
                check(wallet >= fee) { "Not enough coins." }; wallet -= fee; entries++; turn = 0; score = 0; streak = 0; state = "playing"; powerUsed = false; run().also { admitted[key] = it }
            } }
            "tournament-round", "tournament-reveal" -> run().put("question", q().json().apply { remove("correctIndex") }).put("remaining",10).put("phase","answer")
            "tournament-answer" -> { val correct = q().correctIndex; val right = body!!.n("answer") == correct; turn++; if (right) { score += 20; streak++ } else state = "finished"
                run().put("selectedIndex", body.n("answer")).put("correctIndex",correct).put("points",if (right) 20 else 0).put("correct",right)
            }
            "tournament-end" -> { state = "ended"; run() }
            "parties" -> json("parties" to JSONArray(party?.let { listOf(it) } ?: emptyList<J>()))
            "party-preview" -> json("name" to "Friends game", "entryCoins" to 0, "status" to "lobby", "alreadyMember" to false)
            "party-create", "party-join" -> { val fee = body!!.n("entryCoins"); check(wallet >= fee) { "Not enough coins." }; wallet -= fee
                json("id" to "test-party", "name" to body.s("name", "Friends game"), "code" to "ABC123", "hostID" to "test-self", "status" to "lobby", "cycles" to body.n("cycles",1), "days" to body.n("days",7), "powers" to body.b("powers"), "ends" to 1893836800, "members" to 2, "entryCoins" to fee).also { party = it }
            }
            "party-start" -> { party?.put("status","playing"); json("ok" to true) }
            "party-cancel" -> { party?.put("status","cancelled"); json("ok" to true) }
            "party-topic" -> json("ok" to true)
            "party-board" -> json("party" to party, "standings" to JSONArray(listOf("test-self","test-rival").mapIndexed { i,id -> json("id" to id,"name" to if (i == 0) name else "Sample Rival", "avatar" to null, "topicID" to "22", "rank" to 1, "played" to 0, "wins" to 0, "draws" to 0, "losses" to 0, "points" to 0, "quizPoints" to 0) }), "fixtures" to JSONArray(), "selfID" to "test-self", "coins" to wallet)
            "delete-account" -> json("ok" to true)
            else -> error("Unexpected emulator route: $route")
        }
    }
}
