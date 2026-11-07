package com.quizfolk.android

import android.os.Bundle
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    val store: QuizStore by viewModels()
    private var portraitPhone: Boolean? = null
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState); enableEdgeToEdge(); updateOrientation(resources.configuration)
        store.testing = BuildConfig.DEBUG && intent.getBooleanExtra("ui_test", false)
        acceptPush(intent)
        setContent { QuizfolkTheme { Root(store) } }
    }
    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig)
        updateOrientation(newConfig)
    }
    private fun updateOrientation(config: Configuration) {
        val lockPhone = config.smallestScreenWidthDp < 600 && !isInMultiWindowMode
        if (portraitPhone != lockPhone) {
            portraitPhone = lockPhone
            requestedOrientation = if (lockPhone) ActivityInfo.SCREEN_ORIENTATION_PORTRAIT else ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
        }
    }
    override fun onNewIntent(intent: android.content.Intent) { super.onNewIntent(intent);setIntent(intent);acceptPush(intent) }
    private fun acceptPush(intent: android.content.Intent) {
        store.pendingPush=PushDestination.parse(mapOf("kind" to intent.getStringExtra("pushKind").orEmpty(),"id" to intent.getStringExtra("pushID").orEmpty(),"topicID" to intent.getStringExtra("pushTopic").orEmpty()))
    }
}

@Composable fun Root(store: QuizStore) {
    val owner = LocalLifecycleOwner.current; val scope = rememberCoroutineScope()
    val keyboard = LocalSoftwareKeyboardController.current; val focus = LocalFocusManager.current
    val view = LocalView.current
    SideEffect {
        val bars = WindowCompat.getInsetsController((view.context as MainActivity).window, view)
        bars.isAppearanceLightStatusBars = store.game == null
        bars.isAppearanceLightNavigationBars = store.game == null
    }
    LaunchedEffect(store.pages.toList(), store.game?.id, store.tab) { focus.clearFocus(); keyboard?.hide() }
    LaunchedEffect(Unit) { store.initialize() }
    LaunchedEffect(store.ready,store.pendingPush,store.game?.id) {
        if (store.ready) store.pendingPush?.let { destination ->
            if (store.game != null) store.notice=Notice("Notification saved", "Finish or leave your current game first. We’ll then open this notification for you.")
            else { store.pendingPush=null;store.perform { store.openNotification(destination) } }
        }
    }
    DisposableEffect(owner, store) {
        val observer = LifecycleEventObserver { _, event -> if (event == Lifecycle.Event.ON_START && store.ready) scope.launch { store.resume() } }
        owner.lifecycle.addObserver(observer); onDispose { owner.lifecycle.removeObserver(observer) }
    }
    Surface(Modifier.fillMaxSize().testTag("appRoot"), color = CanvasColor) {
        if (!store.ready) Column(Modifier.fillMaxSize().safeDrawingPadding(), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
            BrandMark(84.dp); Spacer(Modifier.height(24.dp)); if (store.loadError == null) Busy("Opening Quizfolk…") else ErrorText(store.loadError)
        } else if (store.game != null) GameScreen(store.game!!)
        else {
            BackHandler(store.pages.isNotEmpty()) { store.back() }
            BoxWithConstraints(Modifier.fillMaxSize()) {
                val rail = maxWidth >= 840.dp && maxHeight >= 600.dp
                val labels = listOf("Discover", "Duels", "Tournaments", "People", "You")
                val icons = listOf(Icons.Default.GridView, Icons.Default.Bolt, Icons.Default.EmojiEvents, Icons.Default.People, Icons.Default.AccountCircle)
                val navigate: (Int) -> Unit = { store.tab = it; store.pages.clear() }
                Scaffold(containerColor = CanvasColor, bottomBar = {
                    if (!rail) NavigationBar(Modifier.testTag("bottomNavigation"), containerColor = ColorForNavigation, tonalElevation = 0.dp) {
                        labels.forEachIndexed { i,label -> NavigationBarItem(selected = store.tab == i, onClick = { navigate(i) },
                            icon = { Icon(icons[i], label) }, label = { Text(label, fontSize = 9.sp) }, modifier = Modifier.testTag("tab-$label"),
                            colors = NavigationBarItemDefaults.colors(selectedIconColor = Coral, selectedTextColor = Coral, indicatorColor = CanvasColor)) }
                    }
                }) { padding ->
                    Row(Modifier.padding(padding).fillMaxSize().consumeWindowInsets(padding)) {
                        if (rail) NavigationRail(Modifier.fillMaxHeight().width(112.dp).testTag("navigationRail"), containerColor = ColorForNavigation,
                            header = { BrandMark(44.dp); Spacer(Modifier.height(24.dp)) }) {
                            labels.forEachIndexed { i,label -> NavigationRailItem(selected = store.tab == i, onClick = { navigate(i) },
                                icon = { Icon(icons[i], label) }, label = { Text(label, fontSize = 11.sp) }, modifier = Modifier.testTag("tab-$label"),
                                colors = NavigationRailItemDefaults.colors(selectedIconColor = Coral, selectedTextColor = Coral, indicatorColor = Coral.copy(alpha = .12f))) }
                        }
                        Column(Modifier.weight(1f).fillMaxHeight()) {
                    val page = store.pages.lastOrNull()
                    if (page != null) TopBar(when (page.type) { "topic" -> store.topic(page.id).name; "player" -> "Player card"; "match" -> "Duel review"; "coins" -> "Daily Trail"; "badges" -> "Tournament badges"; "notifications" -> "Notifications"; "event" -> "Tournament"; "friends" -> "Friends tournaments"; "party" -> "Friends tournament"; "challenge" -> "Challenge"; else -> "Quizfolk" }, store::back)
                    if (page == null) when (store.tab) { 0 -> DiscoverPage(store); 1 -> DuelsPage(store); 2 -> TournamentsPage(store); 3 -> PeoplePage(store); else -> ProfilePage(store) }
                    else when (page.type) {
                        "topic" -> TopicPage(store, store.topic(page.id))
                        "player" -> PlayerPage(store, page.id)
                        "match" -> MatchPage(store, page.record!!)
                        "coins" -> CoinsPage(store)
                        "badges" -> BadgesPage(store)
                        "notifications" -> NotificationSettingsPage(store)
                        "event" -> TournamentPage(store, page.value!!)
                        "friends" -> FriendsPage(store)
                        "party" -> FriendsBoardPage(store, page.value!!)
                        "challenge" -> ChallengePage(store, page.id, page.value!!.s("name"), page.value!!.s("topic", "9"))
                    }
                        }
                    }
                }
            }
        }
        when {
            store.notice != null -> {
                val notice = store.notice!!
                AlertDialog(onDismissRequest = { store.notice = null }, title = { Text(notice.title) }, text = { Text(notice.message) },
                    confirmButton = { TextButton({ store.notice = null; notice.action?.invoke() }) { Text(notice.confirm) } },
                    dismissButton = if (notice.cancel) ({ TextButton({ store.notice = null }) { Text("Cancel") } }) else null)
            }
            store.ready && !store.choseInterests -> InterestsDialog(store)
            store.badgeApplied != null -> {
                val prize = store.badgeApplied!!
                Dialog(onDismissRequest = { }, properties = DialogProperties(usePlatformDefaultWidth = false)) {
                    Surface(Modifier.padding(22.dp).widthIn(max = 430.dp), shape = androidx.compose.foundation.shape.RoundedCornerShape(28.dp), color = CanvasColor) {
                        Column(Modifier.verticalScroll(androidx.compose.foundation.rememberScrollState()).padding(28.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(20.dp)) {
                            Icon(Icons.Default.CheckCircle, null, tint = androidx.compose.ui.graphics.Color(0xFF30C45B), modifier = Modifier.size(42.dp))
                            Avatar(store.name, store.avatar, size = 120.dp, badge = prize, store = store)
                            Text("Badge added!", fontSize = 29.sp, fontWeight = FontWeight.Bold)
                            Text("Your tournament badge is now displayed beside your profile picture.", textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                            Action("Done", tag = "badgeConfirmationDone") { store.badgeApplied = null }
                        }
                    }
                }
            }
            store.pendingPrizes.isNotEmpty() -> PrizeDialog(store, store.pendingPrizes.first())
        }
    }
}
private val ColorForNavigation = androidx.compose.ui.graphics.Color(0xFFF9F8F5)
