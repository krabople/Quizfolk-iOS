package com.quizfolk.android

import android.provider.Settings
import androidx.activity.compose.BackHandler
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.*
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.*
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.*
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import java.util.UUID
import kotlin.math.*

@Composable fun GameScreen(game: GameSession) {
    val store = game.store; val owner = LocalLifecycleOwner.current
    var leave by remember(game.id) { mutableStateOf(false) }; var profileID by remember(game.id) { mutableStateOf<String?>(null) }
    val rematchID = remember(game.id) { UUID.randomUUID().toString() }
    val close = { if (game.canClose) game.close() else leave = true }
    LaunchedEffect(game.id) { game.begin() }
    DisposableEffect(game.id, owner) {
        val observer = LifecycleEventObserver { _, event -> when (event) { Lifecycle.Event.ON_STOP -> game.onBackground(); Lifecycle.Event.ON_START -> game.onForeground(); else -> Unit } }
        owner.lifecycle.addObserver(observer)
        onDispose { owner.lifecycle.removeObserver(observer); game.stop() }
    }
    BackHandler { if (profileID != null) profileID = null else close() }
    if (profileID != null) {
        Column(Modifier.fillMaxSize().background(CanvasColor).safeDrawingPadding()) {
            TopBar("Player card", { profileID = null })
            PlayerPage(store, profileID!!, navigate = { page -> store.game = null; store.push(page) }, onBlocked = { profileID = null })
        }
        return
    }
    MaterialTheme(colorScheme = darkColorScheme(primary = Coral, onPrimary = Color.White, surface = Navy, onSurface = Color.White, background = Navy)) {
        CompositionLocalProvider(LocalContentColor provides Color.White) {
        Column(Modifier.fillMaxSize().background(Brush.linearGradient(listOf(Navy, tint(game.topic.color), Color(0xFF123452)))).safeDrawingPadding()) {
            Row(Modifier.fillMaxWidth().height(56.dp).padding(horizontal = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                IconButton(close, Modifier.testTag("leaveMatch")) { Icon(Icons.Default.Close, "Leave match") }
                Text(game.topic.name, Modifier.weight(1f), textAlign = TextAlign.Center, fontWeight = FontWeight.Bold, fontSize = 19.sp)
                Spacer(Modifier.width(48.dp))
            }
            Box(Modifier.weight(1f)) {
                when {
                    game.finished && game.pending && !game.survival -> PendingResult(game) { profileID = it }
                    game.finished -> ResultScreen(game, { profileID = it }, { store.perform { store.rematch(game.topic, game.opponentID, game.online, rematchID) } })
                    game.searching || !game.prepared && game.online && !game.survival -> SearchScreen(game)
                    game.intro -> IntroScreen(game)
                    else -> PlayScreen(game)
                }
            }
        }
        }
        if (leave) AlertDialog(onDismissRequest = { leave = false }, title = { Text(if (game.survival) "End this run?" else "Leave this duel?") },
            text = { Text(if (game.survival) "Your earned score will be kept. Another attempt costs the displayed entry fee." else "An unfinished duel earns no XP.") },
            confirmButton = { TextButton({ leave = false; game.close() }) { Text(if (game.survival) "End run" else "Leave duel") } }, dismissButton = { TextButton({ leave = false }) { Text("Keep playing") } })
    }
}
@Composable private fun SearchScreen(game: GameSession) = Column(Modifier.fillMaxSize().padding(28.dp).testTag("humanSearch"), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(25.dp, Alignment.CenterVertically)) {
    Icon(Icons.Default.Groups, null, Modifier.size(70.dp), tint = Gold)
    Text("Finding a human rival", fontSize = 28.sp, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center)
    Text("Looking for players in ${game.topic.name}…", textAlign = TextAlign.Center)
    if (game.error == null) CircularProgressIndicator(color = Color.White)
    Text("We check other searchers and recorded human runs before a bot is offered.", textAlign = TextAlign.Center, color = Color.White.copy(alpha = .75f))
    GameError(game)
}
@Composable private fun IntroScreen(game: GameSession) {
    var visible by remember { mutableStateOf(false) }; LaunchedEffect(Unit) { visible = true }
    Column(Modifier.fillMaxSize().padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(24.dp)) {
        BrandMark(66.dp)
        Text("A NEW RIVALRY", fontSize = 12.sp, fontWeight = FontWeight.Black, letterSpacing = 3.sp)
        Row(verticalAlignment = Alignment.Top, modifier = Modifier.fillMaxWidth().testTag("matchupTitle")) {
            AnimatedVisibility(visible, enter = slideInHorizontally { -it } + fadeIn(), modifier = Modifier.weight(1f)) { Contestant(game.store.name, game.store.avatar, false) }
            Text("VS", fontSize = 25.sp, fontWeight = FontWeight.Black, color = Gold, modifier = Modifier.padding(top = 25.dp, start = 8.dp, end = 8.dp))
            AnimatedVisibility(visible, enter = slideInHorizontally { it } + fadeIn(), modifier = Modifier.weight(1f)) { Contestant(game.opponent, game.opponentAvatar, !game.human) }
        }
        Text("${game.topic.emoji} ${game.topic.name}", fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Text(if (game.duelID != null) "A human challenge. Play now or later.\nThe result settles when both runs finish." else if (game.human) "A recorded human run.\nSame seven questions. Your own pace." else if (game.online) "We couldn’t find a human opponent.\nYou have been matched with a bot instead." else "Seven questions. A friendly bot.\nSpeed and knowledge decide the winner.", textAlign = TextAlign.Center, color = Color.White.copy(alpha = .8f), fontSize = 14.sp)
        Spacer(Modifier.weight(1f))
        if (game.prepared) {
            Text(if (game.counting) "${game.countdown}" else "Ready for your duel?", fontSize = if (game.counting) 48.sp else 18.sp, fontWeight = FontWeight.Bold)
            Action(if (game.counting) "Get ready…" else "Start duel", enabled = !game.busy && !game.counting, tag = "startDuel") { game.startDuel() }
        } else if (game.busy) Busy("Preparing your duel…")
        GameError(game)
    }
}
@Composable private fun Contestant(name: String, photo: String?, bot: Boolean) = Column(Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(12.dp)) { Avatar(name, photo, bot, 88.dp); Text(name, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center, maxLines = 2) }

@Composable private fun PlayScreen(game: GameSession) {
    BoxWithConstraints(Modifier.fillMaxSize().padding(horizontal = 16.dp, vertical = 8.dp)) {
        val tileTarget = if (game.reading) 0.dp else maxHeight * if (game.revealed) .32f else .38f
        val answersHeight by animateDpAsState(tileTarget, tween(450), label = "answerSpace")
        Column(Modifier.fillMaxSize(), verticalArrangement = Arrangement.spacedBy(if (game.revealed) 5.dp else 7.dp)) {
            if (game.survival) Row(Modifier.fillMaxWidth().height(46.dp), verticalAlignment = Alignment.CenterVertically) {
                Text("SURVIVAL", fontWeight = FontWeight.Black, fontSize = 12.sp, color = Gold); Spacer(Modifier.weight(1f)); Text("${game.score} points", fontSize = 23.sp, fontWeight = FontWeight.Bold); Spacer(Modifier.width(14.dp)); Text("${game.streak} in a row", fontWeight = FontWeight.Bold)
            } else {
                Row(Modifier.height(if (game.revealed) 42.dp else 48.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    SmallPlayer(game.store.name, game.store.avatar, game.score.toString(), false, Modifier.weight(1f))
                    Text("VS", fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.White.copy(alpha = .6f))
                    SmallPlayer(game.opponent, game.opponentAvatar, if (game.duelID != null && game.pending) "—" else "${game.opponentScore}", !game.human, Modifier.weight(1f))
                }
                DuelProgress(game)
            }
            Row(Modifier.fillMaxWidth().height(if (game.revealed) 50.dp else 62.dp), verticalAlignment = Alignment.CenterVertically) {
                Column(verticalArrangement = Arrangement.spacedBy(5.dp), modifier = Modifier.weight(1f)) {
                    Text(if (game.survival) "QUESTION ${game.round + if (game.revealed) 0 else 1}" else if (game.round == 6) "FINAL ROUND" else "ROUND ${game.round + 1} OF 7", fontSize = 12.sp, fontWeight = FontWeight.Black, letterSpacing = 1.sp)
                    Text(if (!game.survival && game.round == 6) "DOUBLE POINTS" else "FASTER = MORE POINTS", fontSize = 9.sp, fontWeight = FontWeight.Bold, color = Gold)
                }
                if (game.reading) Icon(Icons.Default.MenuBook, "Reading time", tint = Gold, modifier = Modifier.size(47.dp)) else TimerRing(game.remaining, if (game.revealed) 46.dp else 60.dp)
            }
            TimeBar(game.remaining, game.reading)
            val question = game.question
            if (question != null) {
                Box(Modifier.weight(1f).fillMaxWidth().testTag("questionPrompt"), contentAlignment = Alignment.Center) { AutoText(question.prompt, 25, 10, Color.White) }
                if (game.reading) Text("Read the question · 3 seconds", Modifier.fillMaxWidth().testTag("readingPhase"), fontWeight = FontWeight.Bold, textAlign = TextAlign.Center, fontSize = 14.sp)
                Column(Modifier.fillMaxWidth().height(answersHeight).clip(RectangleShape), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    if (!game.reading && question.answers.size == 4) (0..1).forEach { row -> Row(Modifier.weight(1f), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        (0..1).forEach { col -> val index = row * 2 + col
                            AnswerTile(game, question, index, Modifier.weight(1f).fillMaxHeight())
                        }
                    } }
                }
                PowerTray(game)
                game.powerError?.let { Text(it, fontSize = 11.sp, color = Gold) }
                if (game.revealed) Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text(if (game.lastPoints > 0) "+${game.lastPoints} points · Correct!" else if (game.selected == -1) "Time’s up!" else "Correct answer shown", Modifier.weight(1f), fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                    Button({ game.next() }, shape = RoundedCornerShape(14.dp), modifier = Modifier.heightIn(min = 48.dp).testTag("advanceQuestion")) { Text(if (game.survival && game.runEnded || !game.survival && game.round == 6) "See results" else "Next question", fontWeight = FontWeight.Bold) }
                }
            } else { Spacer(Modifier.weight(1f)); CircularProgressIndicator(color = Color.White); Spacer(Modifier.weight(1f)) }
            GameError(game)
        }
    }
}
@Composable private fun AutoText(text: String, base: Int, lines: Int, color: Color) {
    val measurer = rememberTextMeasurer(); val density = LocalDensity.current
    BoxWithConstraints(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        val width = with(density) { maxWidth.roundToPx() }.coerceAtLeast(1); val height = with(density) { maxHeight.roundToPx() }.coerceAtLeast(1)
        val font = remember(text, width, height, density.fontScale) {
            (base downTo 13).firstOrNull { size ->
                val measured = measurer.measure(text, TextStyle(fontFamily = QuizFont, fontSize = size.sp, fontWeight = FontWeight.Bold, lineHeight = (size * 1.2f).sp), maxLines = lines, constraints = Constraints(maxWidth = width))
                !measured.hasVisualOverflow && measured.size.height <= height
            } ?: 13
        }
        Text(text, fontSize = font.sp, lineHeight = (font * 1.2f).sp, maxLines = lines, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center, color = color)
    }
}
@Composable private fun AnswerTile(game: GameSession, question: Question, index: Int, modifier: Modifier) {
    val right = game.revealed && index == question.correctIndex
    val wrong = game.revealed && game.selected == index && !right || game.power.type == "double" && index in game.power.hidden
    val hidden = index in game.power.hidden && !wrong
    val background = if (right) Color(0xFF26A879) else if (wrong) Coral else if (hidden) Color.White.copy(alpha = .08f) else Color.White
    Column(modifier.background(background, RoundedCornerShape(8.dp)).then(if (game.power.highlight == index) Modifier.border(3.dp, Gold, RoundedCornerShape(8.dp)) else Modifier)
        .clickable(enabled = !game.busy && !game.reading && !game.revealed && game.error == null && index !in game.power.hidden) { game.choose(index) }.testTag("answer-$index")
        .semantics { contentDescription = if (hidden) "Removed answer" else question.answers[index] + if (right) ", correct" else if (wrong) ", incorrect" else "" }
        .padding(11.dp), horizontalAlignment = Alignment.CenterHorizontally) {
        Box(Modifier.weight(1f)) { if (!hidden) AutoText(question.answers[index], 19, 6, if (right || wrong) Color.White else Ink) }
        if (right || wrong) Icon(if (right) Icons.Default.CheckCircle else Icons.Default.Cancel, null, tint = Color.White, modifier = Modifier.size(19.dp))
    }
}
@Composable private fun SmallPlayer(name: String, photo: String?, score: String, bot: Boolean, modifier: Modifier) = Row(modifier, verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(7.dp)) {
    Avatar(name, photo, bot, 34.dp); Column { Text(name, maxLines = 1, fontSize = 10.sp, lineHeight = 12.sp, fontWeight = FontWeight.SemiBold); Text(score, fontSize = 25.sp, lineHeight = 28.sp, fontWeight = FontWeight.Bold) }
}
@Composable private fun DuelProgress(game: GameSession) = Column(Modifier.fillMaxWidth().testTag("duelProgress"), verticalArrangement = Arrangement.spacedBy(5.dp)) {
    ProgressRow(game.store.name, game.rounds.size, game.rounds.map { it.points > 0 }, game.round, "roundMarker")
    ProgressRow(game.opponent, game.opponentAnswered, if (game.kind == "bot" || !game.online || game.kind == "human") game.rounds.map { it.opponentPoints > 0 } else game.opponentResults, null, "opponentRoundMarker")
}
@Composable private fun ProgressRow(name: String, answered: Int, results: List<Boolean?>, current: Int?, tag: String) = Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
    Text(name, Modifier.width(92.dp), fontSize = 9.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
    (0..6).forEach { i -> val result = if (i < answered) results.getOrNull(i) else null
        val label = if (result == true) "correct" else if (result == false) "incorrect" else if (i < answered) "answered, result pending" else if (i == current) "current" else "upcoming"
        Box(Modifier.weight(1f).height(12.dp).background(if (result == true) Color(0xFF32C778) else if (result == false) Coral else if (i == current && i >= answered) Gold else Color.White.copy(alpha = if (i < answered) .32f else .17f), CircleShape)
            .testTag("$tag-$i").semantics { contentDescription = "Round ${i+1}: $label" }, contentAlignment = Alignment.Center) {
            if (result != null) Icon(if (result) Icons.Default.Check else Icons.Default.Close, null, tint = Color.White, modifier = Modifier.size(9.dp))
        }
    }
    Text("$answered/7", fontSize = 10.sp, fontWeight = FontWeight.Bold)
}
@Composable private fun TimeBar(seconds: Double, reading: Boolean) {
    val fraction = if (reading) 1f else (seconds / 10).toFloat().coerceIn(0f,1f)
    Box(Modifier.fillMaxWidth().height(9.dp).clip(CircleShape).background(Color.White.copy(alpha = .18f)).testTag("answerTimeBar")
        .semantics { contentDescription = if (reading) "Reading time; answer clock has not started" else "%.1f seconds remaining".format(seconds) }) {
        Box(Modifier.fillMaxWidth(fraction).fillMaxHeight().background(if (reading) Color.White.copy(alpha = .4f) else if (seconds <= 3) Coral else if (seconds <= 5) Gold else Mint, CircleShape))
    }
}
@Composable private fun TimerRing(seconds: Double, size: Dp) = Box(Modifier.size(size).testTag("roundTimer").semantics { contentDescription = "%.1f seconds remaining".format(seconds) }, contentAlignment = Alignment.Center) {
    Canvas(Modifier.fillMaxSize()) {
        val stroke = 5.dp.toPx(); drawCircle(Color.White.copy(alpha = .18f), style = Stroke(stroke))
        drawArc(if (seconds <= 3) Coral else Gold, -90f, (360 * seconds / 10).toFloat().coerceIn(0f,360f), false, style = Stroke(stroke, cap = StrokeCap.Round))
    }
    Column(horizontalAlignment = Alignment.CenterHorizontally) { Text("%.1f".format(seconds), fontSize = if (size >= 60.dp) 25.sp else 19.sp, fontWeight = FontWeight.Black); if (size >= 60.dp) Text("SECONDS", fontSize = 8.sp, letterSpacing = 1.sp, fontWeight = FontWeight.Bold) }
}
@Composable private fun PowerTray(game: GameSession) {
    if (!game.powerAllowed) { Text("Host has switched power-ups off", fontSize = 11.sp, color = Color.White.copy(alpha = .8f)); return }
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) { Assist.entries.forEach { assist ->
            Column(Modifier.weight(1f).background(Color.White.copy(alpha = .13f), RoundedCornerShape(9.dp))
                .clickable(enabled = !game.busy && !game.reading && !game.revealed && !game.power.used) { game.usePower(assist) }.testTag("power-${assist.key}")
                .semantics { contentDescription = "${assist.title}, ${if (game.online) "${assist.price} coins" else "practice"}" }.padding(vertical = 9.dp, horizontal = 2.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                Text(assist.title, fontSize = 10.sp, fontWeight = FontWeight.Bold, color = Color.White.copy(alpha = if (game.power.used) .45f else 1f))
                Row(horizontalArrangement = Arrangement.spacedBy(3.dp), verticalAlignment = Alignment.CenterVertically) { if (game.online) CoinSymbol(11.dp); Text(if (game.online) "${assist.price} coins" else "Practice", fontSize = 10.sp, color = Color.White.copy(alpha = if (game.power.used) .45f else 1f)) }
            }
        } }
        Text(if (game.power.used) "Power-up used · one per run" else "One power-up per run · clock keeps running", Modifier.fillMaxWidth(), fontSize = 9.sp, color = Color.White.copy(alpha = .8f), textAlign = TextAlign.Center)
    }
}
@Composable private fun GameError(game: GameSession) { game.error?.let { Text(it, color = Gold, fontSize = 12.sp); TextButton({ game.retry() }) { Text("Try again", color = Color.White) } } }

@Composable private fun PendingResult(game: GameSession, profile: (String) -> Unit) = Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(26.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(22.dp)) {
    Icon(Icons.Default.HourglassTop, null, Modifier.size(70.dp), tint = Gold)
    Text("YOUR RUN IS SAVED", fontSize = 28.sp, fontWeight = FontWeight.Black, textAlign = TextAlign.Center)
    Text("${game.score} points", fontSize = 45.sp, fontWeight = FontWeight.Bold)
    Text("Waiting for ${game.opponent}", fontSize = 20.sp, fontWeight = FontWeight.Bold)
    Text("They can accept and play the same seven questions later. The winner, topic XP and your head-to-head tally update when both of you finish.", textAlign = TextAlign.Center)
    Action(if (game.busy) "Checking…" else "Check result", enabled = !game.busy) { game.refreshResult() }
    game.opponentID?.let { id -> TextButton({ profile(id) }) { Text("View ${game.opponent}’s player card", color = Color.White) } }
    Action("Back to topics", color = Ink) { game.close() }
    GameError(game)
}
@Composable private fun ResultScreen(game: GameSession, profile: (String) -> Unit, rematch: () -> Unit) {
    val won = game.score > game.opponentScore; val tied = game.score == game.opponentScore
    val rivalry = if (!game.survival && game.opponentID != null) remote("rivalry-${game.opponentID}") { game.store.api("player", query = mapOf("id" to game.opponentID!!)) } else null
    Box(Modifier.fillMaxSize()) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(22.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(18.dp)) {
            Icon(if (!game.survival && tied) Icons.Default.PauseCircle else Icons.Default.EmojiEvents, null, Modifier.size(68.dp), tint = Gold)
            Text(if (game.survival) "RUN COMPLETE" else if (tied) "IT’S A DRAW" else if (won) "YOU WIN!" else "${game.opponent.uppercase()} WINS!", Modifier.testTag("winnerAnnouncement"), fontSize = 31.sp, fontWeight = FontWeight.Black, textAlign = TextAlign.Center)
            if (game.survival) {
                Text("${game.score}", fontSize = 62.sp, fontWeight = FontWeight.Black)
                Text("${game.streak} correct in a row", fontWeight = FontWeight.Bold, fontSize = 20.sp)
                Text("Your best run counts. The final leaderboard and podium prizes settle when the tournament closes.", textAlign = TextAlign.Center)
                CoinAmount(game.store.coins)
                Action("Back to tournament") { game.close() }
            } else {
                game.levelUp?.let { TopicLevelCelebration(game.topic, it) }
                Row(verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                    Podium(game.store.name, game.store.avatar, game.score, won, false, game.store.selfID, Modifier.weight(1f), profile)
                    Text("–", fontSize = 36.sp, modifier = Modifier.padding(top = 60.dp))
                    Podium(game.opponent, game.opponentAvatar, game.opponentScore, !won && !tied, !game.human, game.opponentID, Modifier.weight(1f), profile)
                }
                Column(Modifier.fillMaxWidth().background(Color.White.copy(alpha = .1f), RoundedCornerShape(18.dp)).padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(7.dp)) {
                    Text("+${Scoring.experience(game.score, game.opponentScore)} TOPIC XP", fontSize = 25.sp, fontWeight = FontWeight.Black)
                    Text("${game.score} score + 40 finish + ${if (won) 100 else if (tied) 50 else 0} ${if (tied) "draw" else "win"} bonus", fontSize = 12.sp)
                    Text(if (game.online) "Added to your ${game.topic.name} league" else "Offline practice · local XP only", fontSize = 12.sp, color = Color.White.copy(alpha = .7f))
                }
                rivalry?.value?.o("headToHead")?.let { tally -> QuizfolkTheme { Rivalry(tally) } }
                game.opponentID?.let { id -> TextButton({ profile(id) }) { Text("View ${game.opponent}’s player card", color = Color.White, fontWeight = FontWeight.Bold) } }
                if (game.opponentID != null || !game.human) Action("Rematch", enabled = !game.store.busy, tag = "rematchDuel", onClick = rematch)
                Action("Back to topics") { game.close() }
                Text("${game.rounds.count { it.points > 0 }} OF 7 CORRECT · DUEL REVIEW", fontSize = 11.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
                game.rounds.forEachIndexed { index, round -> QuizfolkTheme { Panel {
                    Row(verticalAlignment = Alignment.CenterVertically) { Icon(if (round.points > 0) Icons.Default.CheckCircle else Icons.Default.Cancel, null, tint = if (round.points > 0) Color(0xFF30A66B) else Coral); Text("QUESTION ${index+1}", Modifier.weight(1f).padding(start = 8.dp), fontSize = 10.sp, fontWeight = FontWeight.Bold); Text("+${round.points}", fontWeight = FontWeight.Bold) }
                    Text(round.question.prompt, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Text("Answer: ${round.question.answers.getOrNull(round.question.correctIndex) ?: "Unavailable"}", fontSize = 13.sp)
                } } }
            }
            GameError(game)
        }
        VictoryConfetti()
    }
}
@Composable private fun TopicLevelCelebration(topic: Topic, advancement: TopicLevelUp) {
    val motion = Settings.Global.getFloat(LocalContext.current.contentResolver, Settings.Global.ANIMATOR_DURATION_SCALE, 1f) > 0f
    val scale = remember { Animatable(if (motion) .85f else 1f) }
    LaunchedEffect(Unit) { if (motion) scale.animateTo(1f, androidx.compose.animation.core.spring(dampingRatio = .65f)) }
    Column(Modifier.fillMaxWidth().graphicsLayer { scaleX = scale.value; scaleY = scale.value }
        .background(Color(0xFF102640), RoundedCornerShape(22.dp)).border(2.dp, Gold, RoundedCornerShape(22.dp))
        .testTag("topicLevelUp").padding(22.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Icon(Icons.Default.ArrowCircleUp, null, tint = Gold)
            Text("LEVEL UP!", color = Gold, fontWeight = FontWeight.Bold, letterSpacing = 2.sp)
        }
        Text(topic.emoji, fontSize = 38.sp)
        Text("Level ${advancement.progress.level}", fontSize = 38.sp, fontWeight = FontWeight.Black)
        Text("${topic.name} · Level ${advancement.previousLevel} → ${advancement.progress.level}", fontWeight = FontWeight.Bold, textAlign = TextAlign.Center)
        Text("${advancement.progress.remainingXP} XP to your next level", fontSize = 12.sp)
    }
}
@Composable private fun Podium(name: String, avatar: String?, score: Int, winner: Boolean, bot: Boolean, id: String?, modifier: Modifier, profile: (String) -> Unit) = Column(modifier, horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(7.dp)) {
    Icon(Icons.Default.WorkspacePremium, null, tint = if (winner) Gold else Color.Transparent, modifier = Modifier.size(20.dp))
    Box(Modifier.testTag("resultProfile-${id ?: "bot"}")) { Avatar(name, avatar, bot, 66.dp, onClick = id?.let { target -> { profile(target) } }) }
    Text(name, fontSize = 12.sp, fontWeight = FontWeight.Bold, maxLines = 2, textAlign = TextAlign.Center)
    Text("$score", fontSize = 39.sp, fontWeight = FontWeight.Black)
}
@Composable private fun VictoryConfetti() {
    val context = LocalContext.current
    val enabled = remember { Settings.Global.getFloat(context.contentResolver, Settings.Global.ANIMATOR_DURATION_SCALE, 1f) > 0f }
    if (!enabled) return
    val fall = remember { Animatable(0f) }; LaunchedEffect(Unit) { fall.animateTo(1f, tween(2500, easing = LinearEasing)) }
    Canvas(Modifier.fillMaxWidth().height(480.dp).clearAndSetSemantics { }) {
        if (fall.value < 1f) (0 until 28).forEach { i ->
            val x = size.width * ((i * 37) % 100) / 100f
            val y = (size.height + 100) * fall.value - 50 - (i % 6) * 12
            rotate(i * 47f * fall.value, Offset(x,y)) { drawRoundRect(listOf(Coral, Gold, Color.White, Mint)[i % 4].copy(alpha = 1 - fall.value), Offset(x,y), Size(7.dp.toPx(),12.dp.toPx()), androidx.compose.ui.geometry.CornerRadius(2.dp.toPx())) }
        }
    }
}
