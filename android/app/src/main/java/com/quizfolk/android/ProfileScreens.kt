package com.quizfolk.android

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
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
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import java.util.UUID

@Composable fun ProfilePage(store: QuizStore) {
    var draft by remember(store.name) { mutableStateOf(store.name) }
    var advanced by remember { mutableStateOf(false) }; var endpoint by remember { mutableStateOf(store.endpoint) }
    var pendingPhoto by remember { mutableStateOf<String?>(null) }
    val context = LocalContext.current; val scope = rememberCoroutineScope(); val links = LocalUriHandler.current
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
        if (uri != null) scope.launch { try { pendingPhoto = withContext(Dispatchers.IO) { PhotoProcessor.make(context, uri) } } catch (e: Exception) { store.notice = Notice("Couldn’t use that picture", e.message ?: "Please try another photo.") } }
    }
    Body {
        BrandHeader("A curious mind.", "Look how far your knowledge takes you.")
        Column(Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(13.dp)) {
            Avatar(store.name, store.avatar, size = 100.dp, badge = store.ownCard?.o("displayBadge"), store = store)
            TextButton({ picker.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)) }, enabled = !store.busy, modifier = Modifier.testTag("changeProfilePicture")) { Icon(Icons.Default.Photo, null); Spacer(Modifier.width(8.dp)); Text("Change profile picture") }
            if (store.avatar != null) TextButton({ store.perform { store.authenticated(); store.api("update-avatar", json("avatar" to null)); store.connect() } }) { Text("Remove profile picture") }
            Text(store.name, fontSize = 25.sp, fontWeight = FontWeight.Bold)
        }
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            ProfileShortcut("Earn coins", Modifier.weight(1f), coin = true) { store.push(Page("coins")) }
            ProfileShortcut("Tournament badges", Modifier.weight(1f)) { store.push(Page("badges")) }
        }
        Text("A DIFFERENT LEVEL IN EVERY TOPIC", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Ink.copy(alpha = .55f))
        Action("Your public card, titles & achievements", color = Ink, tag = "publicProfile") {
            store.perform { store.authenticated(); store.selfID?.let { store.push(Page("player", it)) } }
        }
        Panel { Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceAround) {
            Metric("${store.history.size}", "Duels"); Metric("${store.history.count { it.won }}", "Wins")
            val answered = store.history.flatMap { it.rounds }; Metric(if (answered.isEmpty()) "—" else "${answered.count { it.points > 0 } * 100 / answered.size}%", "Accuracy")
        } }
        Heading("Your topic journey")
        store.topics.filter { it.id in store.favourites || store.topicXP(it.id) > 0 }.forEach { topic -> Panel(Modifier.clickable { store.push(Page("topic", topic.id)) }) { TopicLevel(topic, store.topicXP(topic.id)) } }
        Panel {
            Heading("Your player card")
            OutlinedTextField(draft, { draft = it }, Modifier.fillMaxWidth().testTag("playerName"), label = { Text("Display name") }, singleLine = true, shape = RoundedCornerShape(12.dp))
            Hint("Player names are unique. Capitalisation and repeated spaces do not create a different name. Your current name is kept if a new one is taken.")
            Hint("Your player account stays on this device. Cross-device sign-in and account recovery are not available yet.")
            Action("Save player card", enabled = !store.busy) { store.perform { store.authenticated(); store.api("update-profile", json("name" to draft)); store.connect(); store.notice = Notice("Player card saved", "Your name is now ${store.name}.") } }
            TextButton({ advanced = !advanced }) { Text("Advanced connection settings") }
            if (advanced) {
                OutlinedTextField(endpoint, { endpoint = it }, Modifier.fillMaxWidth(), label = { Text("HTTPS service address") })
                Hint("Only change this if you run your own quiz service. Changing the address creates a separate player account.")
                OutlinedButton({ store.perform { store.changeEndpoint(endpoint.trim()) } }, enabled = !store.busy) { Text("Save service address") }
            }
            ErrorText(store.connectionError) { store.perform { store.resume() } }
            if (store.profile != null) TextButton({ store.notice = Notice("Delete your online account?", "Your server player card, follows, wallet and online records will be deleted. Local practice history will remain on this device.", "Delete account", { store.perform { store.deleteAccount() } }, true) }) { Text("Delete online account", color = Coral) }
        }
        Panel { Heading("Made for curious people"); Hint("Quizfolk is an independent app inspired by classic topic-based trivia. It is not affiliated with QuizUp. Questions have been individually reviewed and edited for clarity, accuracy and topic relevance. Use duel review to see each correct answer.")
            TextButton({ links.openUri("https://www.ways2earn.com/quizfolk-api/credits.html") }) { Text("Credits & licences") }
            TextButton({ links.openUri("https://www.ways2earn.com/quizfolk-api/privacy.html") }) { Text("Privacy policy") }
        }
    }
    if (pendingPhoto != null) AlertDialog(onDismissRequest = { pendingPhoto = null }, title = { Text("Your player picture") }, text = {
        Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(16.dp)) { Avatar(store.name, pendingPhoto, size = 160.dp); Text("This square crop appears on your player card, in duels and leagues. Photo location and other metadata are removed.") }
    }, confirmButton = { TextButton({ val photo = pendingPhoto; pendingPhoto = null; store.perform { store.authenticated(); store.api("update-avatar", json("avatar" to photo)); store.connect(); store.notice = Notice("Picture updated", "Your new player picture has been saved.") } }) { Text("Use this picture") } }, dismissButton = { TextButton({ pendingPhoto = null }) { Text("Cancel") } })
}
@Composable private fun ProfileShortcut(text: String, modifier: Modifier, coin: Boolean = false, action: () -> Unit) {
    Column(modifier.height(96.dp).background(Color.White, RoundedCornerShape(16.dp)).border(1.dp, Ink.copy(alpha = .12f), RoundedCornerShape(16.dp))
        .clickable(onClick = action).testTag(text).padding(8.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
        if (coin) CoinSymbol(28.dp) else Icon(Icons.Default.EmojiEvents, null, tint = Coral, modifier = Modifier.size(28.dp))
        Spacer(Modifier.height(9.dp)); Text(text, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, textAlign = TextAlign.Center)
    }
}

@Composable fun PlayerPage(store: QuizStore, id: String, navigate: (Page) -> Unit = store::push, onBlocked: () -> Unit = store::back) {
    val result = remote("player-$id") { store.authenticated(); store.api("player", query = mapOf("id" to id)) }
    Body {
        result.value?.let { card ->
            val stats = card.o("stats") ?: json()
            Column(Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Avatar(card.s("name"), card.s("avatar"), size = 100.dp, badge = card.o("displayBadge"), store = store)
                Text(card.s("name"), fontSize = 29.sp, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center)
                Text(card.s("title"), color = Coral, fontWeight = FontWeight.Bold)
                Hint("${card.n("followers")} followers · ${card.n("followingCount")} following")
            }
            Panel { Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceAround) { Metric("${stats.n("matches")}", "Duels"); Metric("${stats.n("wins")}", "Wins"); Metric(if (stats.n("answered") == 0) "—" else "${stats.n("correct") * 100 / stats.n("answered")}%", "Accuracy") } }
            if (id != store.selfID) {
                card.o("headToHead")?.let { Rivalry(it) }
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Action(if (card.b("following")) "Following" else "Follow", Modifier.weight(1f), if (card.b("following")) Color.Gray else Coral, !store.busy, "followPlayer") {
                        store.perform { store.api("follow", json("player" to id, "enabled" to !card.b("following"))); result.refresh() }
                    }
                    Action("Challenge", Modifier.weight(1f), Color(0xFF348C98), card.b("canChallenge"), "challengePlayer") { navigate(Page("challenge", id, json("name" to card.s("name")))) }
                }
                if (!card.b("canChallenge")) Hint("This player has paused new challenges.")
            } else PublicPreferences(store, card, result::refresh)
            Panel {
                Heading("Shared interests & favourite topics")
                val interests = card.a("interests").strings(); val shared = card.a("sharedTopics").strings()
                if (interests.isEmpty()) Hint("No topics followed yet.")
                store.topics.filter { it.id in interests }.forEach { topic -> Row(Modifier.fillMaxWidth().clickable { navigate(Page("topic", topic.id)) }.padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                    Text("${topic.emoji} ${topic.name}", Modifier.weight(1f), fontWeight = FontWeight.SemiBold); if (topic.id in shared) Text("Shared", color = tint(topic.color), fontSize = 12.sp); Icon(Icons.Default.ChevronRight, null)
                } }
            }
            Panel {
                Heading("Topic levels")
                val progress = card.a("topics").objects(); if (progress.isEmpty()) Hint("Complete an online duel to start your first topic level.")
                progress.forEach { p -> Column(Modifier.fillMaxWidth().clickable { navigate(Page("topic", p.s("topicID"))) }.padding(vertical = 7.dp)) { TopicLevel(store.topic(p.s("topicID")), p.n("xp")) } }
            }
            Panel {
                Heading("Titles & achievements")
                card.a("badges").objects().forEach { badge -> Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(13.dp), modifier = Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
                    if (badge.s("kind").isNotEmpty()) Medal(badge, store) else Icon(when (badge.s("symbol")) { "bolt.fill" -> Icons.Default.Bolt; "target" -> Icons.Default.Adjust; "flame.fill" -> Icons.Default.LocalFireDepartment; else -> Icons.Default.EmojiEvents }, null, tint = if (badge.b("earned")) Coral else Color.Gray, modifier = Modifier.size(36.dp))
                    Column(Modifier.weight(1f)) { Text(badge.s("name"), fontWeight = FontWeight.SemiBold); Hint(if (badge.b("earned")) "Earned" else "Keep playing to unlock") }
                    if (badge.b("earned")) Icon(Icons.Default.CheckCircle, null, tint = Color(0xFF30A66B))
                } }
            }
            if (id != store.selfID) TextButton({ store.notice = Notice("Block this player?", "Following links will be removed and unfinished challenges between you will be cancelled.", "Block", { store.perform { store.api("block", json("player" to id, "enabled" to true)); store.refreshSocial(); onBlocked() } }, true) }) { Text("Block player", color = Coral) }
        }
        if (result.loading) Busy("Loading player card…")
        ErrorText(result.error, result::refresh)
        TextButton(result::refresh) { Text("Refresh player card") }
    }
}
@Composable fun Rivalry(tally: J) = Panel(Modifier.testTag("headToHead")) {
    Hint("YOUR RIVALRY · ${tally.n("games")} GAMES")
    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceAround) { Metric("${tally.n("wins")}", "Your wins"); Metric("${tally.n("draws")}", "Draws"); Metric("${tally.n("losses")}", "Their wins") }
}
@Composable fun PublicPreferences(store: QuizStore, card: J, refresh: () -> Unit) {
    var discoverable by remember(card) { mutableStateOf(card.b("discoverable")) }; var challenges by remember(card) { mutableStateOf(card.b("challengesOpen")) }
    var title by remember(card) { mutableStateOf(card.s("selectedTitle", "newcomer")) }; var menu by remember { mutableStateOf(false) }
    Panel {
        Heading("Your public player card")
        Hint("Your name, picture, followed topics and completed online results appear on your card. Each topic has its own level.")
        Box { OutlinedButton({ menu = true }) { Text("Title: ${card.a("titles").objects().firstOrNull { it.s("id") == title }?.s("name") ?: card.s("title")}") }
            DropdownMenu(menu, { menu = false }) { card.a("titles").objects().forEach { entry -> DropdownMenuItem(text = { Text(entry.s("name")) }, onClick = { title = entry.s("id"); menu = false }) } } }
        Hint("Topic titles unlock at levels 10, 20, 30, 40 and 50. Select any title you have earned.")
        Row(verticalAlignment = Alignment.CenterVertically) { Text("Show me in player discovery", Modifier.weight(1f)); Switch(discoverable, { discoverable = it }) }
        Row(verticalAlignment = Alignment.CenterVertically) { Text("Allow direct challenges", Modifier.weight(1f)); Switch(challenges, { challenges = it }) }
        Action("Save public card", enabled = !store.busy) { store.perform { store.api("social-settings", json("titleID" to title, "discoverable" to discoverable, "challengesOpen" to challenges)); refresh(); store.notice = Notice("Saved", "Your public card settings have been saved.") } }
    }
}

@Composable fun ChallengePage(store: QuizStore, playerID: String, name: String, initialTopic: String = "9") {
    var topic by remember { mutableStateOf(initialTopic) }; val requestID = remember(topic) { UUID.randomUUID().toString() }
    Body {
        Text("You vs $name", fontSize = 29.sp, fontWeight = FontWeight.Bold)
        Text("Play your seven questions now. They can accept and answer later. The same questions and answer order are used for both of you.")
        TopicChooser(store, "Topic", topic) { topic = it }
        Hint("The result and your head-to-head record update when both runs are finished. Invitations expire after 14 days.")
        Action("Send challenge & play", enabled = !store.busy, tag = "sendChallenge") { store.perform {
            store.authenticated(); val start = store.api("challenge", json("player" to playerID, "topic" to topic, "requestID" to requestID)); store.game = GameSession(store, store.topic(topic), true, start = start)
        } }
    }
}
@Composable fun TopicChooser(store: QuizStore, label: String, selected: String, change: (String) -> Unit) {
    var menu by remember { mutableStateOf(false) }
    Column {
        Hint(label)
        Box { OutlinedButton({ menu = true }, Modifier.fillMaxWidth(), shape = RoundedCornerShape(14.dp)) { Text("${store.topic(selected).emoji} ${store.topic(selected).name}", Modifier.weight(1f)); Icon(Icons.Default.ExpandMore, null) }
            DropdownMenu(menu, { menu = false }, Modifier.heightIn(max = 400.dp)) { store.topics.forEach { topic -> DropdownMenuItem(text = { Text("${topic.emoji} ${topic.name}") }, onClick = { change(topic.id); menu = false }) } }
        }
    }
}

@Composable fun CoinsPage(store: QuizStore) {
    val result = remote("coins") { store.authenticated(); store.api("coins").also { store.coins = it.getJSONObject("wallet").n("coins") } }
    Body {
        Heading("A little curiosity pays off.")
        Text("Complete an online duel with at least 4 correct answers in each of 3 different topics today.")
        CoinAmount(store.coins, true)
        Panel { Row(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) { CoinSymbol(34.dp); Column { Text("50 coins for opening Quizfolk each day", fontWeight = FontWeight.Bold); Hint(if (result.value?.b("loginClaimed") == true) "Today's opening reward is claimed" else "Credited automatically when you open the app") } } }
        result.value?.let { data ->
            val credited = data.a("topics").strings()
            Heading("Daily Trail · extra coins")
            Hint("${data.n("earnedToday")} / 45 trail coins earned today")
            (0..2).forEach { i -> val topic = credited.getOrNull(i)?.let(store::topic)
                Panel { Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) { Icon(if (topic == null) Icons.Default.RadioButtonUnchecked else Icons.Default.CheckCircle, null, tint = if (topic == null) Color.Gray else Color(0xFF30A66B)); Column { Text(topic?.name ?: "Topic ${i+1}", fontWeight = FontWeight.Bold); Hint(if (topic == null) "4 correct answers in one completed duel" else "10 coins earned") } } }
            }
            Text("10 coins per topic + 15 for finishing all three", fontWeight = FontWeight.Bold)
            Panel { Heading("Your weekly trail"); LinearProgressIndicator(progress = { data.n("completedDays").coerceAtMost(5)/5f }, modifier = Modifier.fillMaxWidth()); Text(if (data.b("weeklyBonusEarned")) "50-coin weekly bonus earned" else "${data.n("completedDays").coerceAtMost(5)} of 5 daily trails · earn 50 bonus coins") }
            Hint("Opening reward: 50 coins once per day. Trail limit: 45 extra coins per day. Weekly trail bonus: once per week. Days reset at 00:00 UTC; weeks reset on Monday. Repeating a topic, offline practice and tournament attempts do not earn trail coins.")
            if (credited.size < 3) { Heading("Choose your next topic"); store.topics.filter { it.id !in credited }.forEach { topic -> OutlinedButton({ store.push(Page("topic", topic.id)) }, Modifier.fillMaxWidth()) { Text("${topic.emoji} ${topic.name}") } } }
        }
        if (result.loading) Busy("Loading your trail…")
        ErrorText(result.error, result::refresh); TextButton(result::refresh) { Text("Refresh coin trail") }
    }
}
@Composable fun BadgesPage(store: QuizStore) {
    val result = remote("badges") { store.authenticated(); store.loadPrizes(); json() }
    Body {
        Heading("Beside your profile picture")
        OutlinedButton({ store.perform { store.api("select-badge", json("event" to null)); store.ownCard = store.ownCard?.copyJson()?.put("displayBadge", J.NULL); store.notice = Notice("Badge removed", "Your profile picture no longer has a tournament badge.") } }) { Text("No tournament badge") }
        if (store.earnedPrizes.isEmpty() && !result.loading) Hint("Finish in the top three of a tournament to earn your first badge.")
        store.earnedPrizes.forEach { prize -> Panel(Modifier.clickable { store.perform { store.api("select-badge", json("event" to prize.s("id"))); store.ownCard = store.ownCard?.copyJson()?.put("displayBadge", prize); store.badgeApplied = prize } }.testTag("earnedBadge-${prize.s("id")}")) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) { Medal(prize, store); Column(Modifier.weight(1f)) { Text("${store.topic(prize.s("topicID")).name} · ${placing(prize.n("rank"))}", fontWeight = FontWeight.Bold); Hint("${if (prize.s("kind") == "party") "Friends" else prize.s("kind").replaceFirstChar { it.uppercase() }} tournament"); Hint(date(prize.d("date"))) }; if (store.ownCard?.o("displayBadge")?.s("id") == prize.s("id")) Icon(Icons.Default.Check, null) }
        } }
        ErrorText(result.error, result::refresh)
    }
}
fun placing(rank: Int) = when (rank) { 1 -> "1st place"; 2 -> "2nd place"; else -> "3rd place" }
@Composable fun PrizeDialog(store: QuizStore, prize: J) {
    Dialog(onDismissRequest = { }, properties = DialogProperties(usePlatformDefaultWidth = false)) {
        Surface(Modifier.padding(22.dp).widthIn(max = 440.dp), shape = RoundedCornerShape(28.dp), color = CanvasColor) {
            Column(Modifier.padding(26.dp).verticalScroll(rememberScrollState()), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Medal(prize, store, 95.dp)
                Text("Congratulations!", fontSize = 29.sp, fontWeight = FontWeight.Bold)
                Text("${placing(prize.n("rank"))} · ${store.topic(prize.s("topicID")).name}", fontWeight = FontWeight.Bold, textAlign = TextAlign.Center)
                Hint("${if (prize.s("kind") == "party") "Friends" else prize.s("kind").replaceFirstChar { it.uppercase() }} tournament · ${date(prize.d("date"))}")
                CoinAmount(prize.n("coins"), true)
                val adjustment = prize.n("adjustmentCoins")
                Hint(if (adjustment > 0 && adjustment < prize.n("coins")) "$adjustment additional coins have been credited to your wallet. Your total prize is ${prize.n("coins")} coins." else "Your prize coins have been credited to your wallet.")
                Action("Wear this badge", enabled = !store.busy) { store.perform { store.acknowledge(prize, true) } }
                TextButton({ store.perform { store.acknowledge(prize, false) } }, enabled = !store.busy) { Text("Continue") }
            }
        }
    }
}
