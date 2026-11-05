package com.quizfolk.android

import android.app.Application
import android.util.AtomicFile
import androidx.compose.runtime.*
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import org.json.JSONArray
import java.io.File
import java.util.UUID
import java.util.concurrent.atomic.AtomicLong

data class Notice(val title: String, val message: String, val confirm: String = "OK", val action: (() -> Unit)? = null, val cancel: Boolean = false)
data class Page(val type: String, val id: String = "", val value: J? = null, val record: MatchRecord? = null)

class QuizStore(application: Application) : AndroidViewModel(application) {
    val prefs = application.getSharedPreferences("quizfolk", 0)
    private val vault = PlayerVault(application)
    private val connectionLock = Mutex()
    private val resumeLock = Mutex()
    private val historyLock = Any()
    private val historyGeneration = AtomicLong()
    private var tasks = 0
    private var token: String? = null
    var testing = false
    var notificationGeneration=0
    var notificationChoices by mutableStateOf(defaultPushChoices())
    var pushDelivery by mutableStateOf(false)
    var pushPermission by mutableStateOf(false)
    var notificationError by mutableStateOf<String?>(null)
    var pendingPush by mutableStateOf<PushDestination?>(null)
    var transport: Transport = HttpTransport({ endpoint }, { token })
    var endpoint by mutableStateOf(prefs.getString("endpoint", "https://www.ways2earn.com/quizfolk-api/index.php")!!)
    var name by mutableStateOf(prefs.getString("name", "Explorer-" + UUID.randomUUID().toString().replace("-", "").take(10).uppercase())!!)
    var topics by mutableStateOf<List<Topic>>(emptyList())
    var bank: List<Question> = emptyList(); private set
    var ready by mutableStateOf(false)
    var loadError by mutableStateOf<String?>(null)
    var connectionError by mutableStateOf<String?>(null)
    var busy by mutableStateOf(false)
    var favourites by mutableStateOf(prefs.getStringSet("favourites", emptySet())!!.toSet())
    var choseInterests by mutableStateOf(prefs.getBoolean("choseInterests", false))
    var history by mutableStateOf<List<MatchRecord>>(emptyList())
    var profile by mutableStateOf<J?>(null)
    var ownCard by mutableStateOf<J?>(null)
    var coins by mutableIntStateOf(0)
    var pendingPrizes by mutableStateOf<List<J>>(emptyList())
    var earnedPrizes by mutableStateOf<List<J>>(emptyList())
    var badgeApplied by mutableStateOf<J?>(null)
    var notice by mutableStateOf<Notice?>(null)
    var challenges by mutableStateOf<List<J>>(emptyList())
    var activity by mutableStateOf<List<J>>(emptyList())
    var game by mutableStateOf<GameSession?>(null)
    val pages = mutableStateListOf<Page>()
    var tab by mutableIntStateOf(0)
    val avatar get() = profile?.s("avatar")?.ifEmpty { null }
    val selfID get() = profile?.s("id")

    suspend fun initialize() {
        if (ready) return
        try {
            val loaded = withContext(Dispatchers.IO) {
                val assets = getApplication<Application>().assets
                val categories = assets.open("categories.json").bufferedReader().use { JSONArray(it.readText()).objects().map(Topic::parse) }
                val questions = assets.open("questions.json").bufferedReader().use(::readQuestionBank)
                val file = AtomicFile(File(getApplication<Application>().filesDir, "history.json"))
                val saved = if (file.baseFile.exists()) file.openRead().bufferedReader().use { JSONArray(it.readText()).objects().map(MatchRecord::parse) } else emptyList()
                Triple(categories, questions, saved)
            }
            bank = loaded.second; topics = loaded.first + Topic("mixed", "Mixed topics", "7253A4", "🎨", bank.size); history = loaded.third
            require(bank.size >= 20000 && topics.size == 31) { "The question bank could not be loaded." }
            ready = true
            if (testing) { transport = requireNotNull(fixtureTransport(getApplication(), bank)); choseInterests = true }
            resume()
        } catch (e: Exception) { if (e is CancellationException) throw e; loadError = e.message ?: "The question bank could not be loaded." }
    }
    suspend fun connect() = connectionLock.withLock {
        try {
            if (token == null && !testing) token = withContext(Dispatchers.IO) { vault.read(endpoint) }
            if (token == null) {
                val auth = api("register", json("name" to name, "automaticName" to name.startsWith("Explorer-")))
                val key = auth.s("token"); require(key.isNotBlank()) { "The player key was not returned." }
                if (!testing) withContext(Dispatchers.IO) { vault.save(endpoint, key) }
                token = key
            }
            val current = api("profile"); profile = current; name = current.s("name", name)
            prefs.edit().putString("name", name).apply()
            api("social-settings", json("interests" to JSONArray(favourites.toList())))
            ownCard = api("player"); connectionError = null
        } catch (e: Exception) { if (e is CancellationException) throw e; connectionError = e.message ?: "Could not connect your player card."; throw e }
    }
    suspend fun resume() {
        if (!ready || !resumeLock.tryLock()) return
        try {
            connect()
            coins = api("daily-login", json()).getJSONObject("wallet").n("coins")
            refreshSocial()
            loadPrizes()
            syncNotifications()
        } catch (e: Exception) { if (e is CancellationException) throw e; connectionError = e.message }
        finally { resumeLock.unlock() }
    }
    suspend fun api(route: String, body: J? = null, query: Map<String,String> = emptyMap()) = transport.request(route, body, query)
    suspend fun authenticated() { if (profile == null) connect() }
    suspend fun loadPrizes() {
        val inbox = api("prizes"); pendingPrizes = inbox.a("pending").objects(); earnedPrizes = inbox.a("earned").objects()
        inbox.o("wallet")?.let { coins = it.n("coins") }
    }
    suspend fun acknowledge(prize: J, wear: Boolean) {
        if (wear) {
            val saved = api("select-badge", json("event" to prize.s("id"), "acknowledge" to true))
            if (!saved.b("acknowledged")) api("prize-seen", json("event" to prize.s("id")))
            ownCard = ownCard?.copyJson()?.put("displayBadge", prize); badgeApplied = prize
        } else api("prize-seen", json("event" to prize.s("id")))
        pendingPrizes = pendingPrizes.filterNot { it.s("id") == prize.s("id") }
    }
    suspend fun refreshSocial() {
        challenges = api("duels").a("duels").objects(); activity = api("activity").a("events").objects()
        for (challenge in challenges.filter { it.s("status") == "complete" }) {
            val old = history.firstOrNull { it.duelID == challenge.s("id") && it.pending } ?: continue
            val reply = api("duel-open", json("duel" to challenge.s("id")))
            val updated = old.copy(score = reply.n("score"), opponentScore = reply.n("opponentScore"), opponent = reply.s("opponent"),
                rounds = reply.a("played").objects().map(Round::parse), pending = false, opponentID = reply.s("opponentID").ifEmpty { null }, opponentAvatar = reply.s("opponentAvatar").ifEmpty { null })
            history = history.map { if (it.id == old.id) updated else it }; persistHistory()
        }
    }
    fun perform(block: suspend () -> Unit) {
        viewModelScope.launch {
            tasks++; busy = true
            try { block() } catch (e: Exception) { if (e is CancellationException) throw e; notice = Notice("Couldn’t complete that", e.message ?: "Please try again.") }
            finally { tasks--; busy = tasks > 0 }
        }
    }
    fun push(page: Page) { pages.add(page) }
    fun back() { if (pages.isNotEmpty()) pages.removeAt(pages.lastIndex) }
    fun topic(id: String) = topics.firstOrNull { it.id == id } ?: topics.first()
    fun topicXP(id: String): Int = ownCard?.a("topics")?.objects()?.firstOrNull { it.s("topicID") == id }?.n("xp")
        ?: history.filter { it.topicID == id && it.kind != "practice" }.sumOf { it.xp }
    fun toggle(topic: Topic) {
        favourites = if (topic.id in favourites) favourites - topic.id else favourites + topic.id
        prefs.edit().putStringSet("favourites", favourites).apply()
        if (profile != null) perform { api("social-settings", json("interests" to JSONArray(favourites.toList()))) }
    }
    fun finishInterests() { choseInterests = true; prefs.edit().putBoolean("choseInterests", true).apply() }
    fun save(record: MatchRecord) { if (history.none { it.id == record.id }) { history = listOf(record) + history; persistHistory() } }
    private fun persistHistory() {
        if (testing) return
        val snapshot = JSONArray(history.map { it.json() }).toString().toByteArray()
        val generation = historyGeneration.incrementAndGet()
        viewModelScope.launch(Dispatchers.IO) {
            synchronized(historyLock) {
                if (generation != historyGeneration.get()) return@synchronized
                val file = AtomicFile(File(getApplication<Application>().filesDir, "history.json"))
                val stream = file.startWrite()
                try { stream.write(snapshot); file.finishWrite(stream) } catch (e: Exception) { file.failWrite(stream); throw e }
            }
        }
    }
    suspend fun rematch(topic: Topic, opponentID: String?, online: Boolean, requestID: String) {
        val start = if (opponentID != null) api("challenge", json("player" to opponentID, "topic" to topic.id, "requestID" to requestID))
            else if (online) api("match", json("topic" to topic.id, "botOnly" to true)) else null
        game = GameSession(this, topic, online || opponentID != null, start = start)
    }
    suspend fun deleteAccount() {
        api("delete-account", json()); PushNotifications.clear(getApplication());notificationChoices=defaultPushChoices(); if (!testing) withContext(Dispatchers.IO) { vault.clear() }
        token = null; profile = null; ownCard = null; challenges = emptyList(); activity = emptyList(); pendingPrizes = emptyList(); earnedPrizes = emptyList(); badgeApplied = null; coins = 0
        pages.clear()
    }
    suspend fun changeEndpoint(value: String) {
        require(android.net.Uri.parse(value).scheme == "https") { "Use an HTTPS address." }
        if (endpoint != value) {
            if (profile != null) runCatching { api("notification-device",json("platform" to "android","installation" to PushNotifications.installation(getApplication()),"enabled" to false)) }
            PushNotifications.clear(getApplication());notificationChoices=defaultPushChoices();pushDelivery=false
        }
        if (endpoint != value) { endpoint = value; token = null; profile = null; ownCard = null; pendingPrizes = emptyList(); earnedPrizes = emptyList(); badgeApplied = null; coins = 0; prefs.edit().putString("endpoint", value).apply() }
        resume()
    }
}
