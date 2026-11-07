package com.quizfolk.android

import android.graphics.BitmapFactory
import android.util.Base64
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.painter.Painter
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontVariation
import androidx.compose.ui.text.ExperimentalTextApi
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.*
import java.text.DateFormat
import java.util.Date
import kotlin.math.*

val Ink = Color(0xFF243449)
val CanvasColor = Color(0xFFF7F6F2)
val Coral = Color(0xFFE96959)
val Navy = Color(0xFF102640)
val Mint = Color(0xFF64D9B0)
val Gold = Color(0xFFFFD494)
@OptIn(ExperimentalTextApi::class)
val QuizFont = FontFamily(*listOf(400, 500, 600, 700, 800, 900).map { weight ->
    Font(R.font.nunito, FontWeight(weight), variationSettings = FontVariation.Settings(FontVariation.weight(weight)))
}.toTypedArray())
private val QuizTypography = Typography().let { base -> Typography(
    displayLarge = base.displayLarge.copy(fontFamily = QuizFont), displayMedium = base.displayMedium.copy(fontFamily = QuizFont), displaySmall = base.displaySmall.copy(fontFamily = QuizFont),
    headlineLarge = base.headlineLarge.copy(fontFamily = QuizFont), headlineMedium = base.headlineMedium.copy(fontFamily = QuizFont), headlineSmall = base.headlineSmall.copy(fontFamily = QuizFont),
    titleLarge = base.titleLarge.copy(fontFamily = QuizFont), titleMedium = base.titleMedium.copy(fontFamily = QuizFont), titleSmall = base.titleSmall.copy(fontFamily = QuizFont),
    bodyLarge = base.bodyLarge.copy(fontFamily = QuizFont), bodyMedium = base.bodyMedium.copy(fontFamily = QuizFont), bodySmall = base.bodySmall.copy(fontFamily = QuizFont),
    labelLarge = base.labelLarge.copy(fontFamily = QuizFont), labelMedium = base.labelMedium.copy(fontFamily = QuizFont), labelSmall = base.labelSmall.copy(fontFamily = QuizFont)) }
fun tint(hex: String) = runCatching { Color(android.graphics.Color.parseColor("#$hex")) }.getOrDefault(Coral)
fun date(seconds: Double): String = DateFormat.getDateTimeInstance(DateFormat.MEDIUM, DateFormat.SHORT).format(Date((seconds * 1000).toLong()))

@Composable fun QuizfolkTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = lightColorScheme(primary = Coral, onPrimary = Color.White, secondary = Ink, background = CanvasColor,
        surface = Color.White, onSurface = Ink, onBackground = Ink, outline = Ink.copy(alpha = .15f)),
        typography = QuizTypography) { CompositionLocalProvider(LocalContentColor provides Ink, content = content) }
}
@Composable fun BrandHeader(title: String, subtitle: String) {
    Column(verticalArrangement = Arrangement.spacedBy(9.dp), modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp)) {
        Text("quizfolk", fontSize = 28.sp, fontWeight = FontWeight.Black, color = Coral, letterSpacing = (-1).sp)
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(title, fontSize = 31.sp, fontWeight = FontWeight.ExtraBold, lineHeight = 35.sp, modifier = Modifier.weight(1f))
            BrandMark(54.dp)
        }
        Text(subtitle, fontSize = 16.sp, color = Ink.copy(alpha = .58f))
    }
}
@Composable fun BrandMark(size: Dp = 48.dp) = Image(painterResource(R.drawable.brand_mark), "Quizfolk logo", Modifier.size(size).clip(RoundedCornerShape(size * .23f)))
@Composable fun Body(modifier: Modifier = Modifier, maxWidth: Dp = 900.dp, content: @Composable ColumnScope.() -> Unit) {
    Box(modifier.fillMaxSize(), contentAlignment = Alignment.TopCenter) {
        Column(Modifier.widthIn(max = maxWidth).fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(18.dp), content = content)
    }
}
@Composable fun Panel(modifier: Modifier = Modifier, content: @Composable ColumnScope.() -> Unit) = Column(modifier.fillMaxWidth().background(Color.White, RoundedCornerShape(18.dp)).padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp), content = content)
@Composable fun Action(text: String, modifier: Modifier = Modifier, color: Color = Coral, enabled: Boolean = true, tag: String = text, onClick: () -> Unit) {
    Button(onClick, modifier.fillMaxWidth().heightIn(min = 52.dp).testTag(tag), enabled = enabled,
        shape = RoundedCornerShape(16.dp), colors = ButtonDefaults.buttonColors(containerColor = color), contentPadding = PaddingValues(horizontal = 18.dp, vertical = 14.dp)) {
        Text(text, fontSize = 16.sp, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center)
    }
}
@Composable fun Hint(text: String, color: Color = Ink.copy(alpha = .62f)) = Text(text, fontSize = 13.sp, color = color, lineHeight = 19.sp)
@Composable fun Heading(text: String) = Text(text, fontSize = 22.sp, fontWeight = FontWeight.Bold)
@Composable fun ErrorText(error: String?, retry: (() -> Unit)? = null) {
    if (error != null) { Text(error, color = Coral, fontSize = 14.sp); if (retry != null) TextButton(retry) { Text("Try again") } }
}
@Composable fun Busy(text: String = "Loading…") = Row(Modifier.fillMaxWidth().padding(22.dp), horizontalArrangement = Arrangement.spacedBy(14.dp), verticalAlignment = Alignment.CenterVertically) { CircularProgressIndicator(Modifier.size(24.dp), strokeWidth = 2.dp); Text(text, fontSize = 14.sp) }
@Composable fun TopBar(title: String, back: () -> Unit, refresh: (() -> Unit)? = null) {
    Row(Modifier.fillMaxWidth().heightIn(min = 56.dp).padding(horizontal = 8.dp), verticalAlignment = Alignment.CenterVertically) {
        IconButton(back, Modifier.testTag("back")) { Icon(Icons.Default.ArrowBack, "Back") }
        Text(title, Modifier.weight(1f), fontSize = 19.sp, fontWeight = FontWeight.Bold)
        if (refresh != null) IconButton(refresh) { Icon(Icons.Default.Refresh, "Refresh") } else BrandMark(30.dp)
        Spacer(Modifier.width(8.dp))
    }
}
@Composable fun Segments(labels: List<String>, selected: Int, action: (Int) -> Unit) {
    Row(Modifier.fillMaxWidth().background(Ink.copy(alpha = .07f), RoundedCornerShape(12.dp)).padding(3.dp), horizontalArrangement = Arrangement.spacedBy(2.dp)) {
        labels.forEachIndexed { i,label ->
            Box(Modifier.weight(1f).clip(RoundedCornerShape(10.dp)).background(if (i == selected) Color.White else Color.Transparent)
                .clickable(role = Role.Tab) { action(i) }.semantics { this.selected = i == selected }.testTag("segment-$label").padding(horizontal = 5.dp, vertical = 11.dp), contentAlignment = Alignment.Center) {
                Text(label, fontSize = 12.sp, fontWeight = if (i == selected) FontWeight.Bold else FontWeight.Medium, textAlign = TextAlign.Center)
            }
        }
    }
}
@Composable fun CoinSymbol(size: Dp = 22.dp) {
    Box(Modifier.size(size).background(Brush.linearGradient(listOf(Color(0xFFFFE29A), Color(0xFFD99824))), CircleShape)
        .border((size.value * .06f).dp, Color(0xFFA76B11), CircleShape).padding((size.value * .15f).dp).border(1.dp, Color(0xFFFFF0BC), CircleShape), contentAlignment = Alignment.Center) {
        Text("Q", color = Color(0xFFA66B17), fontSize = (size.value * .5f).sp, fontWeight = FontWeight.Black)
    }
}
@Composable fun CoinAmount(coins: Int, large: Boolean = false) = Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(7.dp), modifier = Modifier.semantics(mergeDescendants = true) { }) {
    CoinSymbol(if (large) 26.dp else 20.dp); Text("$coins coins", fontSize = if (large) 23.sp else 16.sp, fontWeight = FontWeight.Bold)
}
@Composable fun Avatar(name: String, avatar: String? = null, bot: Boolean = false, size: Dp = 52.dp, badge: J? = null, store: QuizStore? = null, onClick: (() -> Unit)? = null) {
    val image = remember(avatar) { runCatching { if (avatar.isNullOrBlank() || avatar.length > 50000) null else BitmapFactory.decodeByteArray(Base64.decode(avatar, Base64.NO_WRAP), 0, Base64.decode(avatar, Base64.NO_WRAP).size)?.asImageBitmap() }.getOrNull() }
    Box(Modifier.size(size).then(if (onClick != null) Modifier.clickable(role = Role.Button, onClickLabel = "View $name's profile", onClick = onClick) else Modifier)
        .semantics { contentDescription = if (onClick != null) "View $name's profile" else if (badge != null) "$name profile picture, tournament place ${badge.n("rank")} badge" else "$name profile picture" }) {
        Box(Modifier.fillMaxSize().clip(CircleShape).background(Coral).border(3.dp, Color.White.copy(alpha = .8f), CircleShape), contentAlignment = Alignment.Center) {
            if (image != null) Image(image, null, Modifier.fillMaxSize(), contentScale = androidx.compose.ui.layout.ContentScale.Crop)
            else Icon(if (bot) Icons.Default.Memory else Icons.Default.Person, null, tint = Color.White, modifier = Modifier.size(size * .52f))
        }
        if (badge != null) Box(Modifier.align(Alignment.BottomEnd).offset(3.dp, 3.dp)) { Medal(badge, store, size * .46f) }
    }
}
@Composable fun Medal(prize: J, store: QuizStore?, size: Dp = 48.dp) {
    val rank = prize.n("rank", 1); val kind = prize.s("kind", "daily")
    val metal = when (rank) { 1 -> Color(0xFFC8952C); 2 -> Color(0xFF7C8DA3); else -> Color(0xFFB66F47) }
    val topic = store?.topics?.firstOrNull { it.id == prize.s("topicID") }
    val shape = remember(kind) { GenericShape { w, _ ->
        val width = w.width; val height = w.height
        if (kind == "weekly") { moveTo(0f, 0f); lineTo(width, 0f); lineTo(width * .9f, height * .65f); lineTo(width * .5f, height); lineTo(width * .1f, height * .65f); close() }
        else {
            val count = if (kind == "party") 6 else 24
            for (i in 0 until count) { val angle = (i * 2 * PI / count - PI/2); val radius = if (kind == "daily" && i % 2 == 1) .44 else .5
                val x = width * (.5 + radius * cos(angle)).toFloat(); val y = height * (.5 + radius * sin(angle)).toFloat()
                if (i == 0) moveTo(x,y) else lineTo(x,y)
            }; close()
        }
    } }
    Box(Modifier.size(size).background(metal, shape).padding(size * .13f).semantics { contentDescription = "${topic?.name ?: "Trivia"}, $kind tournament, place $rank badge" }, contentAlignment = Alignment.Center) {
        Box(Modifier.fillMaxSize().background(topic?.let { tint(it.color) } ?: Ink, CircleShape), contentAlignment = Alignment.Center) {
            Text(if (kind == "party") "👥" else topic?.emoji ?: "🏆", fontSize = (size.value * .35f).sp, modifier = Modifier.offset(y = -size * .07f))
        }
        Text("🏆$rank", fontSize = (size.value * .18f).coerceAtLeast(7f).sp, fontWeight = FontWeight.Black, color = Color.White,
            modifier = Modifier.align(Alignment.BottomCenter).offset(y = size * .12f).background(metal, RoundedCornerShape(4.dp)).padding(horizontal = 3.dp))
    }
}
@Composable fun Metric(value: String, label: String, modifier: Modifier = Modifier) = Column(modifier, horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(5.dp)) { Text(value, fontSize = 26.sp, fontWeight = FontWeight.ExtraBold); Hint(label) }
@Composable fun TopicLevel(topic: Topic, xp: Int) {
    val progress = TopicLevelling.progress(xp)
    Column(verticalArrangement = Arrangement.spacedBy(7.dp)) {
        Row { Text("${topic.emoji} ${topic.name}", Modifier.weight(1f), fontWeight = FontWeight.SemiBold); Text("Level ${progress.level}", fontWeight = FontWeight.Bold, color = tint(topic.color)) }
        LinearProgressIndicator(progress = { progress.xpIntoLevel.toFloat() / progress.xpForNextLevel }, modifier = Modifier.fillMaxWidth().height(7.dp).clip(CircleShape), color = tint(topic.color), trackColor = tint(topic.color).copy(alpha = .13f))
        Hint("${progress.remainingXP} XP to level ${progress.level + 1} · $xp topic XP")
    }
}
@Composable fun TopicTile(topic: Topic, store: QuizStore, modifier: Modifier = Modifier, click: () -> Unit) {
    Column(modifier.clip(RoundedCornerShape(18.dp)).background(Color.White).clickable(onClick = click).testTag("topic-${topic.id}").padding(17.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
        Text(topic.emoji, fontSize = 31.sp)
        Text(topic.name, fontSize = 17.sp, fontWeight = FontWeight.Bold, minLines = 2)
        Hint("Level ${TopicLevelling.progress(store.topicXP(topic.id)).level} · Play & league")
        Text("%,d questions".format(topic.count), color = tint(topic.color), fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
    }
}
class RemoteState {
    var value by mutableStateOf<J?>(null)
    var error by mutableStateOf<String?>(null)
    var loading by mutableStateOf(false)
    var revision by mutableIntStateOf(0)
    fun refresh() { revision++ }
}
@Composable fun remote(key: Any, load: suspend () -> J): RemoteState {
    val state = remember(key) { RemoteState() }
    LaunchedEffect(key, state.revision) {
        state.loading = true; state.error = null
        try { state.value = load() } catch (e: Exception) { if (e is kotlinx.coroutines.CancellationException) throw e; state.error = e.message }
        finally { state.loading = false }
    }
    return state
}
