package com.quizfolk.android

import org.json.JSONArray
import org.json.JSONObject
import java.text.Normalizer
import java.util.Locale
import kotlin.math.floor

typealias J = JSONObject
fun json(vararg values: Pair<String, Any?>): J = J().apply { values.forEach { put(it.first, it.second ?: J.NULL) } }
fun J.s(key: String, fallback: String = "") = if (isNull(key)) fallback else optString(key, fallback)
fun J.n(key: String, fallback: Int = 0) = optInt(key, fallback)
fun J.d(key: String, fallback: Double = 0.0) = optDouble(key, fallback)
fun J.b(key: String, fallback: Boolean = false) = optBoolean(key, fallback)
fun J.o(key: String): J? = optJSONObject(key)
fun J.a(key: String): JSONArray = optJSONArray(key) ?: JSONArray()
fun J.copyJson() = J(toString())
fun JSONArray.objects(): List<J> = (0 until length()).mapNotNull { optJSONObject(it) }
fun JSONArray.strings(): List<String> = (0 until length()).map { getString(it) }

data class Topic(val id: String, val name: String, val color: String, val emoji: String, val count: Int) {
    companion object { fun parse(j: J) = Topic(j.s("id"), j.s("name"), j.s("color"), j.s("emoji"), j.n("questionCount")) }
}
data class Question(val id: String, val categoryID: String, val difficulty: String, val prompt: String, val answers: List<String>, val correctIndex: Int) {
    val key get() = promptKey(prompt)
    fun shuffled(): Question {
        val order = answers.indices.shuffled()
        return copy(answers = order.map { answers[it] }, correctIndex = order.indexOf(correctIndex))
    }
    fun json() = json("id" to id, "categoryID" to categoryID, "difficulty" to difficulty, "prompt" to prompt, "answers" to JSONArray(answers), "correctIndex" to correctIndex)
    companion object { fun parse(j: J, topic: String = "") = Question(j.s("id"), j.s("categoryID", topic), j.s("difficulty", "mixed"), j.s("prompt"), j.a("answers").strings(), j.n("correctIndex", -1)) }
}
fun promptKey(prompt: String): String = Normalizer.normalize(prompt, Normalizer.Form.NFKC)
    .lowercase(Locale.ROOT).replace("ß", "ss").replace("ς", "σ")
    .replace('‘', '\'').replace('’', '\'').replace('“', '"').replace('”', '"')
    .replace(Regex("[\\p{Z}\\p{C}\\s]+"), " ").trim().replace(Regex("\\?+$"), "")
    .replace(Regex("(?<=\\p{L})[.!]+$"), "")

data class Round(val question: Question, val selected: Int, val elapsed: Double, val points: Int, val opponentPoints: Int) {
    fun json() = json("question" to question.json(), "selected" to selected, "elapsed" to elapsed, "points" to points, "opponentPoints" to opponentPoints)
    companion object { fun parse(j: J) = Round(Question.parse(j.getJSONObject("question")), j.n("selected", -1), j.d("elapsed"), j.n("points"), j.n("opponentPoints")) }
}
data class MatchRecord(val id: String, val topicID: String, val date: Long, val score: Int, val opponentScore: Int, val opponent: String,
    val kind: String, val rounds: List<Round>, val duelID: String? = null, val pending: Boolean = false, val opponentID: String? = null, val opponentAvatar: String? = null) {
    val won get() = !pending && score > opponentScore
    val tied get() = !pending && score == opponentScore
    val xp get() = if (pending) 0 else Scoring.experience(score, opponentScore)
    fun json() = json("id" to id, "topicID" to topicID, "date" to date, "score" to score, "opponentScore" to opponentScore, "opponent" to opponent,
        "kind" to kind, "rounds" to JSONArray(rounds.map { it.json() }), "duelID" to duelID, "pending" to pending, "opponentID" to opponentID, "opponentAvatar" to opponentAvatar)
    companion object { fun parse(j: J) = MatchRecord(j.s("id"), j.s("topicID"), j.optLong("date"), j.n("score"), j.n("opponentScore"), j.s("opponent"), j.s("kind"), j.a("rounds").objects().map(Round::parse), j.s("duelID").ifEmpty { null }, j.b("pending"), j.s("opponentID").ifEmpty { null }, j.s("opponentAvatar").ifEmpty { null }) }
}
object Scoring {
    fun points(correct: Boolean, elapsed: Double, round: Int) = if (!correct || !elapsed.isFinite() || elapsed < 0 || elapsed >= 10) 0 else (20 - floor(elapsed).toInt()) * if (round == 6) 2 else 1
    fun experience(score: Int, other: Int) = score + 40 + if (score > other) 100 else if (score == other) 50 else 0
}
fun freshPacket(bank: List<Question>, history: List<MatchRecord>, topicID: String): List<Question> {
    val seen = history.filter { topicID == "mixed" || it.topicID == topicID }.flatMap { it.rounds }.map { it.question }
    val ids = seen.map { it.id }.toSet(); val keys = seen.map { it.key }.toSet()
    val pool = bank.filter { topicID == "mixed" || it.categoryID == topicID }
    val (fresh, old) = pool.partition { it.id !in ids && it.key !in keys }
    var deck = fresh.shuffled() + old.shuffled()
    if (topicID == "mixed") deck = deck.groupBy { it.categoryID }.values.shuffled().map { it.first() }
    val usedIDs = mutableSetOf<String>(); val usedKeys = mutableSetOf<String>()
    return deck.filter { it.key.isNotBlank() && usedIDs.add(it.id) && usedKeys.add(it.key) }.take(7).map { it.shuffled() }
}
data class Power(val used: Boolean = false, val type: String? = null, val hidden: Set<Int> = emptySet(), val highlight: Int? = null) {
    fun next() = Power(used)
    companion object { fun parse(j: J?) = if (j == null) Power() else Power(j.b("used"), j.s("type").ifEmpty { null }, (0 until j.a("hidden").length()).map { j.a("hidden").getInt(it) }.toSet(), if (j.isNull("highlight")) null else j.n("highlight")) }
}
enum class Assist(val key: String, val title: String, val price: Int) { FIFTY("fifty", "Fifty Fifty", 5), DOUBLE("double", "Double Choice", 10), RIGHT("right", "Right Answer", 25) }

fun podium(event: J): List<Int> = if (event.a("prizes").length() == 3) (0..2).map { event.a("prizes").getInt(it) } else if (event.s("kind") == "weekly") listOf(500,250,125) else listOf(150,100,50)
