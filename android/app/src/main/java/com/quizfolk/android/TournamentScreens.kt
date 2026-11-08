package com.quizfolk.android

import android.content.Intent
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import java.util.UUID

@Composable fun TournamentsPage(store: QuizStore) {
    var section by remember { mutableIntStateOf(0) }
    val result = remote("tournaments") { store.authenticated(); store.api("tournaments").also { store.coins = it.getJSONObject("wallet").n("coins") } }
    Body(maxWidth = 1180.dp) {
        BrandHeader("Keep your streak alive.", "One wrong answer. One final score.")
        Action("Friends tournaments", color = Ink, tag = "friendsTournaments") { store.push(Page("friends")) }
        Panel { Row(verticalAlignment = Alignment.CenterVertically) { CoinAmount(store.coins, true); Spacer(Modifier.weight(1f)); TextButton({ store.push(Page("coins")) }) { Text("Earn coins") } }; Hint("Open Quizfolk each day for 50 coins. Earn up to 45 more through your Daily Trail.") }
        Hint("Build the biggest score before your first wrong answer or timeout. Faster correct answers earn more points. Your best run counts.")
        Segments(listOf("Daily", "Weekly", "My entries"), section) { section = it }
        if (section == 0) Hint("Three topics each day · 25 coins each to enter")
        val events = result.value?.a("events")?.objects().orEmpty().filter { if (section == 2) it.n("attempts") > 0 else !it.b("closed") && it.b("featured", true) && it.s("kind") == if (section == 0) "daily" else "weekly" }
        if (events.isEmpty() && !result.loading) Hint(if (section == 2) "Your next trophy awaits. Enter a tournament to save your first score." else "New tournaments soon. Daily topics rotate at midnight UTC; weekly events close on Monday at midnight UTC.")
        AdaptiveCards(events, minWidth = 340.dp) { event, cardModifier -> val topic = store.topic(event.s("topicID")); val prizes = podium(event)
            Panel(cardModifier.clickable { store.push(Page("event", event.s("id"), event)) }.testTag("tournament-${event.s("id")}")) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                    Text(topic.emoji, fontSize = 32.sp, modifier = Modifier.background(tint(topic.color).copy(alpha = .12f), RoundedCornerShape(16.dp)).padding(13.dp))
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                        Text(topic.name, fontWeight = FontWeight.Bold)
                        Hint(if (event.b("closed")) "Finished · Best ${event.n("best")} points" else "${event.n("coins")} coins · ${event.n("players")} players")
                        Text(if (event.b("closed")) "Final place #${event.n("rank")} · ${event.n("reward")} prize coins" else "1st ${prizes[0]} · 2nd ${prizes[1]} · 3rd ${prizes[2]} coins", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = tint(topic.color))
                        if (!event.b("closed")) Hint("Closes ${date(event.d("ends"))}")
                    }
                    Icon(Icons.Default.ChevronRight, null)
                }
            }
        }
        if (result.loading) Busy("Loading tournaments…")
        ErrorText(result.error, result::refresh); TextButton(result::refresh) { Text("Refresh tournaments") }
    }
}
@Composable fun TournamentPage(store: QuizStore, event: J) {
    val result = remote("event-${event.s("id")}") { store.authenticated(); store.api("tournament-board", query = mapOf("event" to event.s("id"))).also { store.coins = it.getJSONObject("wallet").n("coins") } }
    val current = result.value?.o("event") ?: event; val topic = store.topic(current.s("topicID")); val prizes = podium(current)
    val requestID = remember(event.s("id")) { UUID.randomUUID().toString() }
    fun start() { store.perform {
        val admitted = store.api("tournament-enter", json("event" to current.s("id"), "requestID" to requestID))
        store.coins = store.api("coins").getJSONObject("wallet").n("coins")
        store.game = GameSession(store, topic, true, event = current, admitted = admitted)
    } }
    fun prepare() { store.perform {
        val fresh = store.api("tournament-board", query = mapOf("event" to current.s("id"))); result.value = fresh
        val updated = fresh.getJSONObject("event"); val balance = fresh.getJSONObject("wallet").n("coins"); store.coins = balance
        if (updated.b("closed")) store.notice = Notice("Tournament finished", "Entries have closed. Choose one of today’s tournaments.")
        else if (updated.s("activeRun").isNotEmpty()) start()
        else if (balance < updated.n("coins")) store.notice = Notice("Not enough coins", "This tournament costs ${updated.n("coins")} coins. Your balance is $balance coins. Open Earn coins for your Daily Trail.")
        else store.notice = Notice("Enter for ${updated.n("coins")} coins?", "Each new attempt costs ${updated.n("coins")} coins. Only your best score counts. Resuming an admitted run costs nothing further.", "Enter · ${updated.n("coins")} coins", { start() }, true)
    } }
    Body(maxWidth = 960.dp) {
        Text(topic.emoji, fontSize = 62.sp); Text(topic.name, fontSize = 30.sp, fontWeight = FontWeight.Bold)
        Text("${current.s("kind").replaceFirstChar { it.uppercase() }} survival tournament", fontWeight = FontWeight.Bold, color = tint(topic.color))
        Hint("${if (current.b("closed")) "Closed" else "Closes"} ${date(current.d("ends"))}")
        Panel { Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceAround) { Metric("${current.n("best")}", "Your best"); Metric("${current.n("players")}", "Players"); Metric("${current.n("attempts")}", "Attempts") } }
        if (!current.b("closed")) {
            CoinAmount(store.coins)
            if (current.b("featured", true) || current.s("activeRun").isNotEmpty()) Action(if (current.s("activeRun").isEmpty()) "Enter · ${current.n("coins")} coins" else "Resume your run · already entered", color = tint(topic.color), enabled = !store.busy, tag = "enterTournament", onClick = ::prepare)
            else Hint("New entries are closed for this earlier tournament. Your score is kept until the tournament ends.")
        }
        Panel(Modifier.testTag("tournamentPrizes")) {
            Heading("Guaranteed podium prizes")
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceAround) { prizes.forEachIndexed { index, coins -> Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(5.dp)) {
                Medal(json("topicID" to topic.id, "kind" to current.s("kind"), "rank" to index + 1), store, 42.dp)
                Text(listOf("1st","2nd","3rd")[index], fontWeight = FontWeight.Bold); Text("$coins coins", fontSize = 14.sp, fontWeight = FontWeight.Bold)
            } } }
            Hint("Awarded when the tournament closes, regardless of the number of entries.")
        }
        Panel(Modifier.testTag("tournamentStandings")) {
            Heading(if (current.b("closed")) "Final standings" else "Tournament standings")
            Hint("Best score counts · equal scores share a place")
            val entries = result.value?.a("entries")?.objects().orEmpty()
            if (entries.isEmpty() && !result.loading) Hint("Be the first player to set a score.")
            entries.forEach { entry -> Row(Modifier.fillMaxWidth().clickable { store.push(Page("player", entry.s("id"))) }.padding(vertical = 9.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("#${entry.n("rank")}", fontWeight = FontWeight.Bold); Avatar(entry.s("name"), entry.s("avatar"), size = 38.dp)
                Column(Modifier.weight(1f)) { Text(entry.s("name"), fontWeight = FontWeight.SemiBold); Hint("${entry.n("streak")} correct in that run") }
                Text("${entry.n("score")}", color = tint(topic.color), fontSize = 22.sp, fontWeight = FontWeight.Bold)
            } }
            val own = result.value?.a("own")?.objects()?.firstOrNull()
            if (own != null && entries.none { it.s("id") == own.s("id") }) Text("Your place: #${own.n("rank")} · ${own.n("score")} points", fontWeight = FontWeight.Bold)
            TextButton(result::refresh) { Text("Refresh standings") }
        }
        Panel(Modifier.testTag("tournamentRules")) {
            Heading("How this tournament works")
            Hint("Keep answering in ${topic.name} until your first wrong answer or timeout. Read each question for 3 seconds, then answer within 10 seconds. Correct answers earn 11–20 points for speed; every question has the same value. Your score is the total points in that run.")
            Hint("One power-up during the entire run: Fifty Fifty removes two wrong choices (5 coins); Double Choice allows a second pick (10); Right Answer selects and submits the correct answer (25). The clock keeps running.")
            Hint("Try again for the displayed entry cost. Attempts do not add together; only your best run counts. Every question in a run is different. Clearing the whole topic bank completes your run.")
            Hint("Prizes: ${prizes[0]} coins for first, ${prizes[1]} for second, ${prizes[2]} for third. A sole entrant receives first prize. Tied players share the combined prizes for the places they occupy, rounded down to whole coins. Coins and profile badges are awarded after closure; leading an open tournament is provisional.")
            Hint("Earned points are kept if you end a run early or the event closes. Tournament points are separate from duel XP and topic levels.")
        }
        if (result.loading) Busy("Loading tournament…")
        ErrorText(result.error, result::refresh)
    }
}

@Composable fun FriendsPage(store: QuizStore) {
    val result = remote("parties") { store.authenticated(); store.api("parties") }; var composer by remember { mutableStateOf(false) }
    Body(maxWidth = 1000.dp) {
        Heading("Home topic. Away topic. Bragging rights.")
        Hint("A private round-robin for 2–8 friends. Each pair plays one duel in each person’s home topic per cycle. Play together at a party or catch up later.")
        Action("Create or join a tournament", color = Ink) { composer = true }
        Heading("Your friends tournaments")
        val rooms = result.value?.a("parties")?.objects().orEmpty()
        if (rooms.isEmpty() && !result.loading) Hint("Create a tournament and share its invitation code with your friends.")
        AdaptiveCards(rooms) { room, cardModifier -> Panel(cardModifier.clickable { store.push(Page("party", room.s("id"), room)) }) { Text(room.s("name"), fontWeight = FontWeight.Bold); Hint("${room.n("members")} players · ${room.s("status").replaceFirstChar { it.uppercase() }}") } }
        if (result.loading) Busy(); ErrorText(result.error, result::refresh); TextButton(result::refresh) { Text("Refresh friends tournaments") }
    }
    if (composer) FriendsComposer(store, { composer = false }, { room -> composer = false; result.refresh(); store.push(Page("party", room.s("id"), room)) })
}

@Composable fun FriendsComposer(store: QuizStore, close: () -> Unit, opened: (J) -> Unit) {
    var mode by remember { mutableIntStateOf(0) }; var name by remember { mutableStateOf("Game night") }; var code by remember { mutableStateOf("") }
    var topic by remember { mutableStateOf("22") }; var cycles by remember { mutableIntStateOf(1) }; var days by remember { mutableIntStateOf(7) }
    var powers by remember { mutableStateOf(false) }; var prizes by remember { mutableStateOf(true) }; var invitation by remember { mutableStateOf<J?>(null) }
    val requestID = remember { UUID.randomUUID().toString() }
    Dialog(onDismissRequest = close, properties = DialogProperties(usePlatformDefaultWidth = false)) {
        Surface(Modifier.padding(12.dp).widthIn(max = 550.dp).fillMaxHeight(.94f), shape = RoundedCornerShape(24.dp), color = CanvasColor) {
            Column {
                TopBar("Play with friends", close)
                Body {
                    Segments(listOf("Create", "Join"), mode) { mode = it; invitation = null }
                    if (mode == 1) OutlinedTextField(code, { code = it.uppercase(); invitation = null }, Modifier.fillMaxWidth(), label = { Text("Invitation code") }, singleLine = true)
                    else {
                        OutlinedTextField(name, { name = it }, Modifier.fillMaxWidth(), label = { Text("Tournament name") }, singleLine = true)
                        Row(verticalAlignment = Alignment.CenterVertically) { Text("$cycles cycle${if (cycles == 1) "" else "s"} · ${cycles * 2} duels per pair", Modifier.weight(1f), fontSize = 14.sp); IconButton({ cycles-- }, enabled = cycles > 1) { Icon(Icons.Default.Remove, "Fewer cycles") }; IconButton({ cycles++ }, enabled = cycles < 3) { Icon(Icons.Default.Add, "More cycles") } }
                        Text("Time to finish", fontWeight = FontWeight.Bold)
                        Segments(listOf("1 day", "3 days", "7 days", "14 days"), listOf(1,3,7,14).indexOf(days)) { days = listOf(1,3,7,14)[it] }
                        Row(verticalAlignment = Alignment.CenterVertically) { Text("Coin entry and podium prizes", Modifier.weight(1f)); Switch(prizes, { prizes = it }, Modifier.testTag("partyPrizes")) }
                        Hint(if (prizes) "10 coins per person · coin and badge prizes" else "Free entry · no coins, badges or tournament prizes")
                        Row(verticalAlignment = Alignment.CenterVertically) { Text("Allow power-ups", Modifier.weight(1f)); Switch(powers, { powers = it }) }
                    }
                    TopicChooser(store, "My home topic", topic) { topic = it }
                    invitation?.let { quote -> Panel { Text(quote.s("name"), fontWeight = FontWeight.Bold); Hint(if (quote.b("alreadyMember")) "You already joined · no further charge" else if (quote.n("entryCoins") == 0) "Free entry · no prizes" else "Entry: ${quote.n("entryCoins")} coins · coin and badge prizes"); if (quote.s("status") != "lobby" && !quote.b("alreadyMember")) Hint("Entries have closed") } }
                    Hint("The host chooses free entry without prizes, or a 10-coin entry with podium prizes. Any entry fee is charged when you create or join. The host starts once everyone has joined and picked a topic. Topics and settings then lock.")
                    Hint("Win = 3 league points; draw = 1. Each pair plays in both home topics every cycle. Unfinished duels earn no league points. Only members can see standings. Unstarted lobbies expire after 24 hours and refund entries.")
                    Hint("Paid tournaments divide the entry pool: two players share 60% / 40%; three or more share 50% / 30% / 20%. Tied places share those prizes. Free tournaments have no prizes.")
                    val label = if (mode == 0) { if (prizes) "Create · 10 coins" else "Create free · no prizes" } else if (invitation == null) "Check invitation" else if (invitation!!.b("alreadyMember")) "Open tournament" else if (invitation!!.n("entryCoins") == 0) "Join free" else "Join · ${invitation!!.n("entryCoins")} coins"
                    Action(label, enabled = !store.busy && if (mode == 0) name.trim().length >= 2 else code.isNotBlank() && (invitation == null || invitation!!.b("alreadyMember") || invitation!!.s("status") == "lobby"), tag = "submitParty") {
                        store.perform {
                            store.authenticated()
                            if (mode == 1 && invitation == null) invitation = store.api("party-preview", json("code" to code.trim()))
                            else {
                                val room = store.api(if (mode == 1) "party-join" else "party-create", if (mode == 1) json("code" to code.trim(), "topic" to topic, "expectedEntryCoins" to invitation!!.n("entryCoins"))
                                    else json("requestID" to requestID, "name" to name.trim(), "topic" to topic, "cycles" to cycles, "days" to days, "powers" to powers, "entryCoins" to if (prizes) 10 else 0))
                                store.coins = store.api("coins").getJSONObject("wallet").n("coins"); opened(room)
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable fun FriendsBoardPage(store: QuizStore, room: J) {
    val result = remote("party-${room.s("id")}") { store.authenticated(); store.api("party-board", query = mapOf("id" to room.s("id"))) }
    val current = result.value?.o("party") ?: room; var topic by remember { mutableStateOf("22") }; val context = LocalContext.current
    LaunchedEffect(result.value) { result.value?.let { board -> board.a("standings").objects().firstOrNull { it.s("id") == board.s("selfID") }?.let { topic = it.s("topicID", "22") } } }
    fun command(route: String) { store.perform { store.api(route, json("party" to room.s("id"))); store.coins = store.api("coins").getJSONObject("wallet").n("coins"); result.refresh() } }
    Body(maxWidth = 1000.dp) {
        Heading(current.s("name")); Hint("Private · ${current.n("members")} players · ${current.s("status").replaceFirstChar { it.uppercase() }}")
        if (current.s("status") == "lobby") {
            Panel { Text(current.s("code"), fontSize = 25.sp, fontWeight = FontWeight.Bold); Action("Invite friends", color = Ink) {
                context.startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).setType("text/plain").putExtra(Intent.EXTRA_TEXT, "Join my Quizfolk friends tournament: ${current.s("name")}. Invitation code: ${current.s("code")}"), "Share invitation"))
            } }
            Hint(if (current.n("entryCoins") == 0) "Free entry with no prizes. The lobby expires in 24 hours if it isn't started." else "Joining costs ${current.n("entryCoins")} coins. The lobby expires in 24 hours if it isn't started.")
            TopicChooser(store, "My home topic", topic) { topic = it }
            OutlinedButton({ store.perform { store.api("party-topic", json("party" to room.s("id"), "topic" to topic)); result.refresh() } }, enabled = !store.busy) { Text("Save home topic") }
            if (result.value?.s("selfID") == current.s("hostID")) {
                Action("Start tournament · lock players and topics", enabled = !store.busy && current.n("members") >= 2) { command("party-start") }
                TextButton({ store.notice = Notice("Cancel this tournament?", if (current.n("entryCoins") == 0) "The free lobby will close." else "All entry coins will be refunded.", "Cancel tournament", { command("party-cancel") }, true) }) { Text(if (current.n("entryCoins") == 0) "Cancel tournament" else "Cancel and refund all entries", color = Coral) }
            } else Hint("The host will start when everyone is ready.")
        } else if (current.s("status") == "playing") Hint("Finish by ${date(current.d("ends"))}")
        Hint("${current.n("cycles")} cycles · ${if (current.b("powers")) "Power-ups allowed" else "Power-ups off"} · ${if (current.n("entryCoins") == 0) "Free, no prizes" else "${current.n("entryCoins")} coins per player"}")
        Panel {
            Heading(if (current.s("status") == "complete") "Final standings" else "Tournament standings")
            Hint("Win = 3 · draw = 1 · equal league points share a place")
            result.value?.a("standings")?.objects()?.forEach { player -> Row(Modifier.fillMaxWidth().clickable { store.push(Page("player", player.s("id"))) }.padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("#${player.n("rank")}", fontWeight = FontWeight.Bold); Avatar(player.s("name"), player.s("avatar"), size = 36.dp)
                Column(Modifier.weight(1f)) { Text(player.s("name"), fontWeight = FontWeight.SemiBold); Hint("${player.n("played")} played · ${player.n("wins")}W ${player.n("draws")}D ${player.n("losses")}L"); Hint("Home: ${store.topic(player.s("topicID")).name}") }
                Text("${player.n("points")}", fontSize = 24.sp, fontWeight = FontWeight.Bold)
            } }
        }
        Heading("Your fixtures")
        val board = result.value
        if (board != null) {
            val mine = board.a("fixtures").objects().filter { it.s("a") == board.s("selfID") || it.s("b") == board.s("selfID") }
            if (mine.isEmpty()) Hint("Your fixtures appear after the host starts the tournament.")
            AdaptiveCards(mine) { fixture, cardModifier ->
                val other = if (fixture.s("a") == board.s("selfID")) fixture.s("b") else fixture.s("a")
                val name = board.a("standings").objects().firstOrNull { it.s("id") == other }?.s("name") ?: "Former player"
                Panel(cardModifier) {
                    Text("You vs $name", fontWeight = FontWeight.Bold); Hint("${store.topic(fixture.s("topicID")).name} · Cycle ${fixture.n("cycle")} · ${fixture.s("status")}")
                    if (current.s("status") == "playing" || fixture.s("status") == "complete") Action(if (fixture.s("status") == "complete") "View result" else if (fixture.b("ownFinished")) "Run saved · check result" else "Play duel", enabled = !store.busy) {
                        store.perform { val start = store.api("party-play", json("party" to room.s("id"), "fixture" to fixture.s("id"))); store.game = GameSession(store, store.topic(fixture.s("topicID")), true, start = start) }
                    } else Hint("Unfinished · no league points")
                }
            }
        }
        if (result.loading) Busy("Loading friends tournament…")
        ErrorText(result.error, result::refresh); TextButton(result::refresh) { Text("Refresh tournament") }
    }
}
