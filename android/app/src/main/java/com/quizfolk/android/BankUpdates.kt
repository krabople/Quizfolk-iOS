package com.quizfolk.android

import android.content.Context
import android.util.AtomicFile
import android.util.JsonReader
import android.util.JsonToken
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.Reader
import java.net.HttpURLConnection
import java.net.URI
import java.security.MessageDigest

data class MobileQuestionBank(val categories: List<Topic>, val questions: List<Question>)

fun readMobileQuestionBank(input: Reader): MobileQuestionBank = JsonReader(input).use { reader ->
    var format = 0; var questions: List<Question> = emptyList(); val topics = ArrayList<Topic>()
    reader.beginObject()
    while (reader.hasNext()) when (reader.nextName()) {
        "format" -> format = reader.nextInt()
        "questions" -> questions = readQuestionArray(reader)
        "categories" -> {
            reader.beginArray()
            while (reader.hasNext()) {
                var id=""; var name=""; var color=""; var emoji=""; var count=0
                reader.beginObject()
                while (reader.hasNext()) when (reader.nextName()) {
                    "id" -> id=reader.nextString(); "name" -> name=reader.nextString()
                    "color" -> color=reader.nextString(); "emoji" -> emoji=reader.nextString()
                    "questionCount" -> count=reader.nextInt(); else -> reader.skipValue()
                }
                reader.endObject(); topics.add(Topic(id,name,color,emoji,count))
            }
            reader.endArray()
        }
        else -> reader.skipValue()
    }
    reader.endObject()
    require(questions.all { it.imagePng == null || questionImageBytes(it.imagePng,it.imageSHA256) != null })
    val ids=topics.map { it.id }.toSet(); val counts=questions.groupingBy { it.categoryID }.eachCount()
    require(reader.peek()==JsonToken.END_DOCUMENT && (format==1 || format==2) && ids.isNotEmpty() && ids.size==topics.size && "mixed" !in ids)
    require(questions.map { it.id }.toSet().size==questions.size)
    require(questions.all { it.categoryID in ids && it.answers.size==4 && it.answers.toSet().size==4 && it.answers.all { answer -> answer.isNotBlank() } && it.correctIndex in 0..3 })
    require(topics.all { it.id.isNotBlank() && it.name.isNotBlank() && it.count>=7 && counts[it.id]==it.count })
    MobileQuestionBank(topics,questions)
}

object QuestionBankUpdates {
    fun sha(data: ByteArray): String = MessageDigest.getInstance("SHA-256").digest(data).joinToString("") { "%02x".format(it.toInt() and 255) }
    private fun cache(context: Context, endpoint: String): AtomicFile {
        val root=File(context.noBackupFilesDir,"question-banks")
        check(root.isDirectory || root.mkdirs())
        return AtomicFile(File(root,sha((endpoint+"|images-v2").toByteArray(Charsets.UTF_8))+".json"))
    }
    fun cached(context: Context, endpoint: String): MobileQuestionBank? = try {
        cache(context,endpoint).openRead().bufferedReader(Charsets.UTF_8).use(::readMobileQuestionBank)
    } catch (_: Exception) { null }
    private fun download(uri: URI, maximum: Int): ByteArray {
        require(uri.scheme=="https" && !uri.host.isNullOrEmpty())
        val connection=uri.toURL().openConnection() as HttpURLConnection
        try {
            connection.connectTimeout=15000; connection.readTimeout=15000
            connection.setRequestProperty("Accept","application/json")
            connection.useCaches=false
            // No player token or other personal information is sent for public bank assets.
            require(connection.responseCode==200 && connection.url.protocol=="https" && connection.url.host==uri.host)
            require(connection.contentLengthLong<=maximum)
            return connection.inputStream.use { stream ->
                val output=ByteArrayOutputStream(); val buffer=ByteArray(8192)
                while (true) { val count=stream.read(buffer); if(count<0) break; require(output.size()+count<=maximum); output.write(buffer,0,count) }
                output.toByteArray()
            }
        } finally { connection.disconnect() }
    }
    fun fetch(context: Context, endpoint: String): MobileQuestionBank? {
        val api=URI(endpoint);require(api.scheme=="https" && !api.host.isNullOrEmpty())
        val directory=api.resolve("bank-v2/")
        val manifest=J(String(download(directory.resolve("manifest.json"),65536),Charsets.UTF_8))
        val revision=manifest.s("revision"); val filename=manifest.s("file"); val bytes=manifest.n("bytes")
        require(manifest.n("format") in 1..2 && revision.matches(Regex("[a-f0-9]{64}")) && filename=="bank-$revision.json" && bytes in 1..50_000_000)
        val file=cache(context,endpoint)
        val saved=try { file.openRead().use { it.readBytes() } } catch (_: Exception) { null }
        if(saved!=null && sha(saved)==revision && cached(context,endpoint)!=null) return null
        val data=download(directory.resolve(filename),bytes)
        require(data.size==bytes && sha(data)==revision)
        val bank=data.inputStream().reader(Charsets.UTF_8).use(::readMobileQuestionBank)
        require(bank.questions.size==manifest.n("questionCount") && bank.categories.size==manifest.n("topicCount"))
        val stream=file.startWrite()
        try { stream.write(data); file.finishWrite(stream) } catch (error: Exception) { file.failWrite(stream); throw error }
        return bank
    }
}
