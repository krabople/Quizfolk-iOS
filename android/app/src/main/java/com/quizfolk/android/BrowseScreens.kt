package com.quizfolk.android

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import kotlinx.coroutines.delay
import java.util.UUID

@Composable fun DiscoverPage(store: QuizStore) {
    var query by remember { mutableStateOf("") }; var mode by remember { mutableIntStateOf(0) }; var interests by remember { mutableStateOf(false) }
    Body(Modifier.testTag("discover"), maxWidth = 1180.dp) {
        BrandHeader("Find your people.", "A little knowledge. A great rivalry.")
        Row(verticalAlignment = Alignment.CenterVertically) {
            OutlinedTextField(query, { query = it }, Modifier.weight(1f).testTag("topicSearch"), placeholder = { Text("Find your favourite subject") }, singleLine = true, shape = RoundedCornerShape(16.dp), leadingIcon = { Icon(Icons.Default.Search, null) })
            IconButton({ interests = true }) { Icon(Icons.Default.Tune, "Choose interests") }
        }
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedButton({ store.push(Page("topic", store.topics.filter { it.id != "mixed" }.random().id)) }, Modifier.weight(1f).testTag("randomTopic"), shape = RoundedCornerShape(14.dp)) { Text("Random topic", fontWeight = FontWeight.Bold) }
            OutlinedButton({ store.push(Page("topic", "mixed")) }, Modifier.weight(1f).testTag("mixedTopic"), shape = RoundedCornerShape(14.dp)) { Text("Mixed topics", fontWeight = FontWeight.Bold) }
        }
        Segments(listOf("All topics", "My interests"), mode) { mode = it }
        val visible = store.topics.filter { (mode == 0 || it.id in store.favourites) && (query.isBlank() || it.name.contains(query, true)) }
        if (visible.isEmpty()) Hint(if (mode == 1) "Follow a few topics to make this space your own." else "No topics match that search.")
        AdaptiveCards(visible, minWidth = 200.dp, compactColumns = 2, gap = 12.dp) { topic, modifier ->
            TopicTile(topic, store, modifier) { store.push(Page("topic", topic.id)) }
        }
        ErrorText(store.connectionError) { store.perform { store.resume() } }
    }
    if (interests) InterestsDialog(store) { interests = false }
}

@Composable fun InterestsDialog(store: QuizStore, close: (() -> Unit)? = null) {
    Dialog(onDismissRequest = { close?.invoke() }, properties = DialogProperties(usePlatformDefaultWidth = false)) {
        Surface(Modifier.padding(16.dp).widthIn(max = 550.dp).fillMaxHeight(.9f), shape = RoundedCornerShape(25.dp), color = CanvasColor) {
            Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                BrandHeader("What makes you curious?", "Choose the topics you love. You can change these any time.")
                Column(Modifier.weight(1f).verticalScroll(rememberScrollState()), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    store.topics.forEach { topic -> Row(Modifier.fillMaxWidth().clickable { store.toggle(topic) }.padding(vertical = 3.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(topic.emoji, fontSize = 25.sp); Text(topic.name, Modifier.weight(1f).padding(start = 12.dp), fontWeight = FontWeight.SemiBold)
                        Checkbox(topic.id in store.favourites, { store.toggle(topic) })
                    } }
                }
                Action("Done", tag = "interestsDone") { store.finishInterests(); close?.invoke() }
            }
        }
    }
}

@Composable fun TopicPage(store: QuizStore, topic: Topic) {
    var section by remember { mutableIntStateOf(0) }
    Body {
        Text(topic.emoji, fontSize = 60.sp)
        Text(topic.name, fontSize = 31.sp, fontWeight = FontWeight.ExtraBold)
        Hint("%,d questions · Your kind of curiosity".format(topic.count))
        OutlinedButton({ store.toggle(topic) }, shape = RoundedCornerShape(12.dp)) { Text(if (topic.id in store.favourites) "Following topic" else "Follow topic") }
        Segments(listOf("Play & progress", "League"), section) { section = it }
        if (section == 0) {
            Panel { TopicLevel(topic, store.topicXP(topic.id)) }
            Heading("A rival is waiting.")
            Hint("We search for a human first, including recorded human runs. A bot is offered after six seconds when nobody is available. Play at your own pace.")
            Action("Find a duel", color = tint(topic.color)) { store.game = GameSession(store, topic, true) }
            OutlinedButton({ store.game = GameSession(store, topic, false) }, Modifier.fillMaxWidth().testTag("practice"), shape = RoundedCornerShape(14.dp)) { Text("Practise against a bot", fontWeight = FontWeight.Bold) }
            Hint("Read each question for 3 seconds, then answer within 10 seconds. Correct answers earn 11–20 points for speed; the final round counts double. Wrong answers and timeouts score zero. Maximum 160. One power-up per duel: Fifty Fifty (5 coins), Double Choice (10) or Right Answer (25). Practice power-ups are free.")
        } else LeaguePanel(store, topic)
    }
}

@Composable fun LeaguePanel(store: QuizStore, topic: Topic) {
    var period by remember { mutableIntStateOf(0) }; var following by remember { mutableIntStateOf(0) }
    val result = remote("${topic.id}-$period-$following") {
        store.authenticated(); store.api("leaderboard", query = mapOf("topic" to topic.id, "period" to if (period == 0) "month" else "all", "scope" to if (following == 0) "all" else "following"))
    }
    Heading("${topic.name} league")
    Segments(listOf("This month", "All time"), period) { period = it }
    Segments(listOf("Everyone", "Following + you"), following) { following = it }
    Hint(if (period == 0) "Monthly topic XP · resets on the 1st at 00:00 UTC" else "Lifetime XP earned in this topic")
    result.value?.a("entries")?.objects()?.let { entries ->
        if (entries.isEmpty()) Hint(if (following == 1) "Follow players in People to build your friends’ league." else "No completed online duels in this topic yet. Play one to set the pace.")
        entries.forEachIndexed { i, entry ->
            Panel(Modifier.clickable { store.push(Page("player", entry.s("id"))) }.testTag("league-player-${entry.s("id")}")) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("${i+1}", fontSize = 22.sp, fontWeight = FontWeight.Bold, color = if (i < 3) Color(0xFFC28D2F) else Ink)
                    Avatar(entry.s("name"), entry.s("avatar"))
                    Column(Modifier.weight(1f)) { Text(entry.s("name"), fontWeight = FontWeight.Bold); Hint("${entry.n("matches")} duels") }
                    Text("${entry.n("xp")}", fontSize = 22.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
    if (result.loading) Busy("Loading rankings…")
    ErrorText(result.error, result::refresh)
    TextButton(result::refresh) { Text("Refresh ${topic.name} league") }
    Hint("XP = your match score + 40 for finishing + 100 for a win or 50 for a draw. Challenges enter the table after both players finish. Practice stays out of online leagues.")
}

@Composable fun PeoplePage(store: QuizStore) {
    var query by remember { mutableStateOf("") }; var mode by remember { mutableIntStateOf(0) }
    val result = remote("people-$mode-$query") {
        delay(250); store.authenticated()
        store.api(if (mode == 2) "activity" else "people", query = if (mode == 2) emptyMap() else mapOf("q" to query, "mode" to if (mode == 0) "discover" else "following"))
    }
    Body {
        BrandHeader("Good company.", "Find a friend. Start a rivalry.")
        Segments(listOf("Discover", "Following", "Activity"), mode) { mode = it }
        if (mode != 2) OutlinedTextField(query, { query = it }, Modifier.fillMaxWidth().testTag("playerSearch"), singleLine = true, placeholder = { Text("Find a player") }, leadingIcon = { Icon(Icons.Default.Search, null) }, shape = RoundedCornerShape(15.dp))
        if (mode == 2) {
            val events = result.value?.a("events")?.objects().orEmpty()
            if (events.isEmpty() && !result.loading) Hint("Follow people to see their completed duels here.")
            events.forEach { event -> Panel(Modifier.clickable { store.push(Page("player", event.s("playerID"))) }) {
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
                    Avatar(event.s("name"), event.s("avatar")); Column {
                        Text(event.s("name"), fontWeight = FontWeight.Bold)
                        Hint("${if (event.b("draw")) "Drew" else if (event.b("won")) "Won" else "Played"} in ${store.topic(event.s("topicID")).name} · ${event.n("score")} points")
                        Hint(date(event.d("date")))
                    }
                }
            } }
        } else {
            val people = result.value?.a("players")?.objects().orEmpty()
            if (people.isEmpty() && !result.loading) Hint(if (mode == 1) "Follow players to keep your favourite rivals close." else "No players found. Try another name.")
            people.forEach { card -> PlayerRow(store, card) { store.push(Page("player", card.s("id"))) } }
        }
        if (result.loading) Busy("Finding players…")
        ErrorText(result.error, result::refresh)
        TextButton(result::refresh) { Text("Refresh players") }
    }
}
@Composable fun PlayerRow(store: QuizStore, card: J, click: () -> Unit) {
    Panel(Modifier.clickable(onClick = click).testTag("player-${card.s("id")}")) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Avatar(card.s("name"), card.s("avatar"), badge = card.o("displayBadge"), store = store)
            Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(card.s("name"), fontWeight = FontWeight.Bold); Text(card.s("title"), color = Coral, fontSize = 13.sp)
                Hint(if (card.a("sharedTopics").length() > 0) "${card.a("sharedTopics").length()} shared interests" else "${card.o("stats")?.n("matches") ?: 0} completed duels")
            }
            Icon(Icons.Default.ChevronRight, null)
        }
    }
}

@Composable fun DuelsPage(store: QuizStore) {
    var section by remember { mutableIntStateOf(0) }
    LaunchedEffect(Unit) { runCatching { store.authenticated(); store.refreshSocial() } }
    if (section == 1) {
        Box(Modifier.fillMaxSize(), contentAlignment = Alignment.TopCenter) {
        LazyColumn(Modifier.widthIn(max = 960.dp).fillMaxSize().testTag("history"), contentPadding = PaddingValues(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            item { BrandHeader("Good rivalries.", "Every duel has a story.") }
            item { Segments(listOf("Challenges", "Device history"), section) { section = it } }
            if (store.history.isEmpty()) item { Hint("Your first rival is waiting. Pick a topic and play your first duel.") }
            items(store.history, key = { it.id }) { match -> Panel(Modifier.clickable { store.push(Page("match", record = match)) }.testTag("history-match-${match.id}")) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(store.topic(match.topicID).emoji, fontSize = 31.sp, modifier = Modifier.padding(end = 12.dp))
                    Column(Modifier.weight(1f)) { Text(store.topic(match.topicID).name, fontWeight = FontWeight.Bold); Hint("vs ${match.opponent}"); Hint(when (match.kind) { "challenge" -> "Asynchronous challenge"; "human" -> "Recorded human run"; "practice" -> "Offline practice"; else -> "Bot duel" }) }
                    Column(horizontalAlignment = Alignment.End) { Text("${match.score}–${match.opponentScore}", fontWeight = FontWeight.Bold); Text(if (match.pending) "WAITING" else if (match.tied) "DRAW" else if (match.won) "WON" else "LOST", color = if (match.won) Color(0xFF2CA65D) else Coral, fontSize = 11.sp, fontWeight = FontWeight.Bold) }
                }
            } }
        }
        }
    } else Body {
        BrandHeader("A rivalry worth keeping.", "Play now. Let them catch up later.")
        Segments(listOf("Challenges", "Device history"), section) { section = it }
        Action("Find people to challenge", color = Ink) { store.tab = 3 }
        if (store.challenges.isEmpty()) Hint("No challenges yet. Find a player in People, open their card and send a challenge.")
        store.challenges.forEach { challenge ->
            val complete = challenge.s("status") == "complete"; val available = challenge.s("status") in listOf("invited", "accepted")
            Panel {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Avatar(challenge.s("opponent"), challenge.s("avatar"), onClick = challenge.s("opponentID").takeIf { it.isNotEmpty() }?.let { id -> { store.push(Page("player", id)) } })
                    Column(Modifier.weight(1f)) { Text(challenge.s("opponent"), fontWeight = FontWeight.Bold); Hint(store.topic(challenge.s("topicID")).name) }
                    Text(if (complete) { if (challenge.n("score") == challenge.n("opponentScore")) "Draw" else if (challenge.n("score") > challenge.n("opponentScore")) "You won" else "You lost" }
                        else if (!available) challenge.s("status").replaceFirstChar { it.uppercase() } else if (challenge.b("ownFinished")) "Run saved" else "Your turn", color = Coral, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
                if (available && challenge.b("ownFinished")) Hint("Waiting for their answers. Your result and topic XP update after both runs finish.")
                if (complete || available && !challenge.b("ownFinished")) Action(if (complete) "View result" else if (challenge.b("incoming") && !challenge.b("accepted")) "Accept & play" else "Play your turn", enabled = !store.busy) {
                    store.perform { val start = store.api("duel-open", json("duel" to challenge.s("id"))); store.game = GameSession(store, store.topic(challenge.s("topicID")), true, start = start) }
                }
                if (available && challenge.b("incoming") && !challenge.b("accepted")) TextButton({ store.perform { store.api("duel-decline", json("duel" to challenge.s("id"))); store.refreshSocial() } }) { Text("Decline", color = Coral) }
                if (challenge.s("opponentID").isNotBlank()) TextButton({ store.push(Page("player", challenge.s("opponentID"))) }) { Text("Player card") }
            }
        }
        ErrorText(store.connectionError) { store.perform { store.resume() } }
        TextButton({ store.perform { store.authenticated(); store.refreshSocial() } }) { Text("Refresh challenges") }
    }
}

@Composable fun MatchPage(store: QuizStore, match: MatchRecord) {
    val requestID = remember(match.id) { UUID.randomUUID().toString() }
    Body {
        Heading("${match.score} – ${match.opponentScore} vs ${match.opponent}")
        if (match.pending) Hint("Your run is saved. Waiting for ${match.opponent}.")
        if (match.rounds.size == 7) Action("View result", tag = "historyResult") { store.game = GameSession(store, store.topic(match.topicID), match.kind != "practice", saved = match) }
        match.opponentID?.let { id -> Panel(Modifier.clickable { store.push(Page("player", id)) }.testTag("historyOpponentProfile")) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) { Avatar(match.opponent, match.opponentAvatar); Column { Text(match.opponent, fontWeight = FontWeight.Bold); Hint("View profile & follow") }; Spacer(Modifier.weight(1f)); Icon(Icons.Default.ChevronRight, null) }
        } }
        if (!match.pending && (match.opponentID != null || match.kind in listOf("bot", "practice"))) Action("Rematch", color = Ink, enabled = !store.busy, tag = "historyRematch") {
            store.perform { store.rematch(store.topic(match.topicID), match.opponentID, match.kind != "practice", requestID) }
        }
        match.rounds.forEachIndexed { index, r -> Panel {
            Text("${index + 1}. ${r.question.prompt}", fontWeight = FontWeight.Bold)
            Text("Correct: ${r.question.answers.getOrNull(r.question.correctIndex) ?: "Unavailable"}")
            Hint("Your answer: ${r.question.answers.getOrNull(r.selected) ?: "Timed out"}")
            Hint("${r.points} points · %.1f seconds".format(r.elapsed))
        } }
    }
}
