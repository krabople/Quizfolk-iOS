package com.quizfolk.android

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import com.google.firebase.FirebaseApp
import com.google.firebase.FirebaseOptions
import com.google.firebase.messaging.FirebaseMessaging
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import kotlinx.coroutines.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import java.util.UUID
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException
import kotlin.coroutines.suspendCoroutine

data class PushDestination(val kind: String, val id: String, val topicID: String = "") {
    companion object {
        fun parse(data: Map<String,String>): PushDestination? {
            val kind = data["kind"] ?: return null; val id = data["id"] ?: return null
            return if (kind in pushKinds && id.matches(Regex("[A-Za-z0-9:-]{1,160}"))) PushDestination(kind,id,data["topicID"].orEmpty()) else null
        }
    }
}
val pushKinds = linkedMapOf(
    "challenges" to ("New challenges" to "When another player challenges you to a duel."),
    "duelResults" to ("Duel results" to "When both players finish and the result is decided."),
    "tournamentPrizes" to ("Tournament prizes" to "Your final place, coin prize and badge after a tournament closes."),
    "friendsTournaments" to ("Friends tournaments" to "When a friends tournament starts or finishes.")
)
fun defaultPushChoices() = json("enabled" to false, "challenges" to true, "duelResults" to true, "tournamentPrizes" to true, "friendsTournaments" to true)

object PushNotifications {
    private val lock = Mutex()
    private val background = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    fun configured() = BuildConfig.FCM_APP_ID.isNotBlank() && BuildConfig.FCM_API_KEY.isNotBlank() && BuildConfig.FCM_PROJECT_ID.isNotBlank() && BuildConfig.FCM_SENDER_ID.isNotBlank()
    fun allowed(context: Context) = NotificationManagerCompat.from(context).areNotificationsEnabled() && (Build.VERSION.SDK_INT < 33 || ContextCompat.checkSelfPermission(context,Manifest.permission.POST_NOTIFICATIONS)==PackageManager.PERMISSION_GRANTED)
    private fun preferences(context: Context) = context.getSharedPreferences("push",Context.MODE_PRIVATE)
    fun clear(context: Context) {
        preferences(context).edit().remove("choices").remove("endpoint").remove("seen").apply()
        NotificationManagerCompat.from(context).cancelAll()
        if (FirebaseApp.getApps(context).any { it.name==FirebaseApp.DEFAULT_APP_NAME }) FirebaseMessaging.getInstance().apply { isAutoInitEnabled=false;deleteToken() }
    }
    fun installation(context: Context): String {
        val prefs=preferences(context);return prefs.getString("installation",null) ?: UUID.randomUUID().toString().also { prefs.edit().putString("installation",it).commit() }
    }
    fun cache(store: QuizStore) {
        preferences(store.getApplication()).edit().putString("choices",store.notificationChoices.toString()).putString("endpoint",store.endpoint).apply()
    }
    private fun firebase(context: Context): FirebaseMessaging? {
        if (!configured()) return null
        if (FirebaseApp.getApps(context).none { it.name == FirebaseApp.DEFAULT_APP_NAME }) FirebaseApp.initializeApp(context,FirebaseOptions.Builder()
            .setApplicationId(BuildConfig.FCM_APP_ID).setApiKey(BuildConfig.FCM_API_KEY).setProjectId(BuildConfig.FCM_PROJECT_ID).setGcmSenderId(BuildConfig.FCM_SENDER_ID).build())
        return FirebaseMessaging.getInstance()
    }
    private suspend fun token(messaging: FirebaseMessaging): String = suspendCoroutine { next ->
        messaging.token.addOnCompleteListener { result -> if (result.isSuccessful) next.resume(result.result) else next.resumeWithException(result.exception ?: IllegalStateException("Could not register notifications.")) }
    }
    suspend fun sync(store: QuizStore) = lock.withLock {
        val context=store.getApplication<android.app.Application>();store.pushPermission=allowed(context);cache(store)
        if (store.testing) return@withLock
        val enabled=store.notificationChoices.b("enabled") && store.pushDelivery && configured() && allowed(context)
        val body=json("platform" to "android","installation" to installation(context),"enabled" to enabled)
        if (enabled) {
            val messaging=requireNotNull(firebase(context));messaging.isAutoInitEnabled=true
            body.put("token",token(messaging))
        }
        store.api("notification-device",body)
        if (!store.notificationChoices.b("enabled")) {
            if (FirebaseApp.getApps(context).any { it.name==FirebaseApp.DEFAULT_APP_NAME }) FirebaseMessaging.getInstance().apply { isAutoInitEnabled=false; deleteToken() }
            NotificationManagerCompat.from(context).cancelAll()
        }
    }
    fun rotated(context: Context, token: String) {
        background.launch {
            lock.withLock {
                runCatching {
                    val prefs=preferences(context);val choices=J(prefs.getString("choices","{}")!!)
                    if (!choices.b("enabled") || !allowed(context) || !configured()) return@runCatching
                    val endpoint=prefs.getString("endpoint",null) ?: return@runCatching
                    val player=PlayerVault(context).read(endpoint) ?: return@runCatching
                    HttpTransport({endpoint},{player}).request("notification-device",json("installation" to installation(context),"platform" to "android","enabled" to true,"token" to token))
                }
            }
        }
    }
    fun display(context: Context, data: Map<String,String>) {
        val destination=PushDestination.parse(data) ?: return
        val prefs=preferences(context);val choices=runCatching { J(prefs.getString("choices","{}")!!) }.getOrDefault(json())
        if (!choices.b("enabled") || !choices.b(destination.kind) || !allowed(context)) return
        val notificationID=data["notificationID"] ?: return
        if (!notificationID.matches(Regex("[a-f0-9]{64}"))) return
        val seen=prefs.getStringSet("seen",emptySet())!!.toSet();if (notificationID in seen) return
        val manager=context.getSystemService(NotificationManager::class.java)
        pushKinds.forEach { (kind,description) -> manager.createNotificationChannel(NotificationChannel(kind,description.first,NotificationManager.IMPORTANCE_DEFAULT).apply { this.description=description.second }) }
        val intent=Intent(context,MainActivity::class.java).setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP)
            .setData(Uri.parse("quizfolk://notification/$notificationID")).putExtra("pushKind",destination.kind).putExtra("pushID",destination.id).putExtra("pushTopic",destination.topicID)
        val pending=PendingIntent.getActivity(context,notificationID.hashCode(),intent,PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
        val notification=NotificationCompat.Builder(context,destination.kind).setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(data["title"].orEmpty().take(100)).setContentText(data["body"].orEmpty().take(300))
            .setStyle(NotificationCompat.BigTextStyle().bigText(data["body"].orEmpty().take(300))).setContentIntent(pending).setAutoCancel(true).build()
        try { manager.notify(notificationID,0,notification);prefs.edit().putStringSet("seen",(seen.takeLastSet(99)+notificationID).toSet()).apply() } catch (_: SecurityException) { }
    }
    private fun Set<String>.takeLastSet(count: Int) = toList().takeLast(count)
}
class QuizfolkMessagingService:FirebaseMessagingService() {
    override fun onNewToken(token: String) { PushNotifications.rotated(this,token) }
    override fun onMessageReceived(message: RemoteMessage) { PushNotifications.display(this,message.data) }
}

suspend fun QuizStore.loadNotificationChoices() {
    val generation=notificationGeneration;val reply=api("notification-settings");if (generation!=notificationGeneration) return;notificationChoices=reply.o("preferences") ?: defaultPushChoices();pushDelivery=reply.o("delivery")?.b("android") == true
    PushNotifications.cache(this);notificationError=null
}
suspend fun QuizStore.syncNotifications() {
    try { loadNotificationChoices();PushNotifications.sync(this) } catch (e: Exception) { if (e is CancellationException) throw e;notificationError=e.message }
}
suspend fun QuizStore.saveNotificationChoices(choices: J) {
    notificationGeneration++
    val reply=api("notification-preferences",json("preferences" to choices));notificationChoices=reply.o("preferences") ?: choices
    pushDelivery=reply.o("delivery")?.b("android") == true;notificationError=null;PushNotifications.cache(this);PushNotifications.sync(this)
}
suspend fun QuizStore.openNotification(destination: PushDestination) {
    if (game != null) { pendingPush=destination;return }
    authenticated();pages.clear()
    when (destination.kind) {
        "challenges","duelResults" -> { tab=1; val start=api("duel-open",json("duel" to destination.id));game=GameSession(this,topic(destination.topicID),true,start=start) }
        "tournamentPrizes" -> { tab=2; val reply=api("tournament-board",query=mapOf("event" to destination.id));push(Page("event",destination.id,reply.getJSONObject("event"))) }
        "friendsTournaments" -> { tab=2; val reply=api("party-board",query=mapOf("id" to destination.id));push(Page("party",destination.id,reply.getJSONObject("party"))) }
    }
}
@Composable fun NotificationSettingsPage(store: QuizStore) {
    val context=LocalContext.current
    val permission=rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { store.perform { PushNotifications.sync(store) } }
    LaunchedEffect(Unit) { store.perform { store.loadNotificationChoices();store.pushPermission=PushNotifications.allowed(context) } }
    Body {
        Heading("Your notifications")
        Hint("Choose what you hear about. You can switch everything off at any time.")
        Panel {
            Row(verticalAlignment=Alignment.CenterVertically) { Text("Push notifications",Modifier.weight(1f),fontWeight=FontWeight.Bold)
                Switch(store.notificationChoices.b("enabled"), { enabled -> store.perform {
                    val choices=store.notificationChoices.copyJson().put("enabled",enabled);store.saveNotificationChoices(choices)
                    if (enabled && store.pushDelivery && PushNotifications.configured() && Build.VERSION.SDK_INT>=33 && !store.pushPermission) permission.launch(Manifest.permission.POST_NOTIFICATIONS)
                } },enabled=!store.busy,modifier=Modifier.testTag("push-enabled"))
            }
            if (!store.pushDelivery || !PushNotifications.configured()) Hint("Push delivery is not available yet. Your choices will be saved.")
            else if (!store.pushPermission) {
                Hint("Notifications are switched off in Android Settings. Your choices below are saved.")
                OutlinedButton({context.startActivity(Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS).putExtra(Settings.EXTRA_APP_PACKAGE,context.packageName))}) { Text("Open Android notification settings") }
            }
        }
        Heading("Notify me about")
        pushKinds.forEach { (kind,description) -> Panel {
            Row(verticalAlignment=Alignment.CenterVertically) { Text(description.first,Modifier.weight(1f),fontWeight=FontWeight.Bold)
                Switch(store.notificationChoices.b(kind), { enabled -> store.perform { store.saveNotificationChoices(store.notificationChoices.copyJson().put(kind,enabled)) } },enabled=!store.busy,modifier=Modifier.testTag("push-$kind"))
            };Hint(description.second)
        } }
        ErrorText(store.notificationError) { store.perform { store.syncNotifications() } }
    }
}
