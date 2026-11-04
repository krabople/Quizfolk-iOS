package com.quizfolk.android

import android.content.Context
import android.net.Uri
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

interface Transport { suspend fun request(route: String, body: J? = null, query: Map<String, String> = emptyMap()): J }

/** Only the encrypted player key is persisted. The non-exportable AES key stays in Android Keystore. */
class PlayerVault(context: Context) {
    private val prefs = context.getSharedPreferences("encrypted_player", Context.MODE_PRIVATE)
    private val alias = "com.quizfolk.android.player"
    private fun key(): SecretKey {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        (store.getKey(alias, null) as? SecretKey)?.let { return it }
        return KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore").apply {
            init(KeyGenParameterSpec.Builder(alias, KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM).setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE).build())
        }.generateKey()
    }
    fun read(endpoint: String): String? {
        if (prefs.getString("endpoint", null) != endpoint) return null
        val stored = prefs.getString("value", null) ?: return null
        val raw = Base64.decode(stored, Base64.NO_WRAP)
        require(raw.size > 12) { "Saved player key is damaged. Please restore the original app data." }
        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(128, raw.copyOfRange(0, 12)))
        return String(cipher.doFinal(raw.copyOfRange(12, raw.size)), Charsets.UTF_8)
    }
    fun save(endpoint: String, token: String) {
        val cipher = Cipher.getInstance("AES/GCM/NoPadding"); cipher.init(Cipher.ENCRYPT_MODE, key())
        val stored = Base64.encodeToString(cipher.iv + cipher.doFinal(token.toByteArray(Charsets.UTF_8)), Base64.NO_WRAP)
        check(prefs.edit().putString("endpoint", endpoint).putString("value", stored).commit()) { "Could not securely save your player key." }
    }
    fun clear() { check(prefs.edit().clear().commit()) }
}

class HttpTransport(private val endpoint: () -> String, private val token: () -> String?) : Transport {
    override suspend fun request(route: String, body: J?, query: Map<String, String>): J {
        // Capture these together before dispatching IO; an endpoint change must not mix account keys and hosts.
        val requestEndpoint = endpoint(); val requestToken = token()
        return withContext(Dispatchers.IO) {
        val base = Uri.parse(requestEndpoint)
        require(base.scheme == "https" && !base.host.isNullOrEmpty()) { "Enter a valid HTTPS service address." }
        val uri = base.buildUpon().appendQueryParameter("r", route).apply { query.forEach { (k,v) -> appendQueryParameter(k,v) } }.build()
        val connection = URL(uri.toString()).openConnection() as HttpURLConnection
        try {
            connection.connectTimeout = 20000; connection.readTimeout = 20000
            connection.setRequestProperty("X-Quizfolk-Client", "3")
            connection.setRequestProperty("Accept", "application/json")
            requestToken?.let { connection.setRequestProperty("Authorization", "Bearer $it") }
            if (body != null) {
                connection.requestMethod = "POST"; connection.doOutput = true
                connection.setRequestProperty("Content-Type", "application/json; charset=utf-8")
                connection.outputStream.use { it.write(body.toString().toByteArray(Charsets.UTF_8)) }
            }
            val code = connection.responseCode
            val stream = if (code in 200..299) connection.inputStream else connection.errorStream
            val text = stream?.bufferedReader(Charsets.UTF_8)?.use { it.readText() } ?: "{}"
            val reply = try { J(text) } catch (_: Exception) { throw IllegalStateException("The service could not be reached. Please try again.") }
            if (code !in 200..299) throw IllegalStateException(reply.s("error", "Server request failed. Please try again."))
            reply
        } finally { connection.disconnect() }
        }
    }
}
