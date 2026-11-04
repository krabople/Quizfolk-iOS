package com.quizfolk.android

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
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
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState); enableEdgeToEdge()
        store.testing = BuildConfig.DEBUG && intent.getBooleanExtra("ui_test", false)
        setContent { QuizfolkTheme { Root(store) } }
    }
}

@Composable fun Root(store: QuizStore) {
    val owner = LocalLifecycleOwner.current; val scope = rememberCoroutineScope()
    val keyboard = LocalSoftwareKeyboardController.current; val focus = LocalFocusManager.current
    LaunchedEffect(store.pages.toList(), store.game?.id, store.tab) { focus.clearFocus(); keyboard?.hide() }
    LaunchedEffect(Unit) { store.initialize() }
    DisposableEffect(owner, store) {
        val observer = LifecycleEventObserver { _, event -> if (event == Lifecycle.Event.ON_START && store.ready) scope.launch { store.resume() } }
        owner.lifecycle.addObserver(observer); onDispose { owner.lifecycle.removeObserver(observer) }
    }
    Surface(Modifier.fillMaxSize(), color = CanvasColor) {
        if (!store.ready) Column(Modifier.fillMaxSize().safeDrawingPadding(), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
            BrandMark(84.dp); Spacer(Modifier.height(24.dp)); if (store.loadError == null) Busy("Opening Quizfolk…") else ErrorText(store.loadError)
        } else if (store.game != null) GameScreen(store.game!!)
        else {
            BackHandler(store.pages.isNotEmpty()) { store.back() }
            Scaffold(containerColor = CanvasColor, bottomBar = {
                NavigationBar(containerColor = ColorForNavigation, tonalElevation = 0.dp) {
                    val labels = listOf("Discover", "Duels", "Tournaments", "People", "You")
                    val icons = listOf(Icons.Default.GridView, Icons.Default.Bolt, Icons.Default.EmojiEvents, Icons.Default.People, Icons.Default.AccountCircle)
                    labels.forEachIndexed { i,label -> NavigationBarItem(selected = store.tab == i, onClick = { store.tab = i; store.pages.clear() },
                        icon = { Icon(icons[i], label) }, label = { Text(label, fontSize = 9.sp) }, modifier = Modifier.testTag("tab-$label"),
                        colors = NavigationBarItemDefaults.colors(selectedIconColor = Coral, selectedTextColor = Coral, indicatorColor = CanvasColor)) }
                }
            }) { padding ->
                Column(Modifier.padding(padding).fillMaxSize().consumeWindowInsets(padding)) {
                    val page = store.pages.lastOrNull()
                    if (page != null) TopBar(when (page.type) { "topic" -> store.topic(page.id).name; "player" -> "Player card"; "match" -> "Duel review"; "coins" -> "Daily Trail"; "badges" -> "Tournament badges"; "event" -> "Tournament"; "friends" -> "Friends tournaments"; "party" -> "Friends tournament"; "challenge" -> "Challenge"; else -> "Quizfolk" }, store::back)
                    if (page == null) when (store.tab) { 0 -> DiscoverPage(store); 1 -> DuelsPage(store); 2 -> TournamentsPage(store); 3 -> PeoplePage(store); else -> ProfilePage(store) }
                    else when (page.type) {
                        "topic" -> TopicPage(store, store.topic(page.id))
                        "player" -> PlayerPage(store, page.id)
                        "match" -> MatchPage(store, page.record!!)
                        "coins" -> CoinsPage(store)
                        "badges" -> BadgesPage(store)
                        "event" -> TournamentPage(store, page.value!!)
                        "friends" -> FriendsPage(store)
                        "party" -> FriendsBoardPage(store, page.value!!)
                        "challenge" -> ChallengePage(store, page.id, page.value!!.s("name"), page.value!!.s("topic", "9"))
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
                        Column(Modifier.padding(28.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(20.dp)) {
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
