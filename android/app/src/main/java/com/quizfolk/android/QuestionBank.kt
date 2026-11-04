package com.quizfolk.android

import android.util.JsonReader
import java.io.Reader

/** Stream the shared bank so older phones do not retain a second, large JSONObject tree. */
fun readQuestionBank(input: Reader): List<Question> = JsonReader(input).use { reader ->
    val result = ArrayList<Question>(22000)
    reader.beginArray()
    while (reader.hasNext()) {
        var id = ""; var category = ""; var difficulty = "mixed"; var prompt = ""; var correct = -1
        val answers = ArrayList<String>(4)
        reader.beginObject()
        while (reader.hasNext()) when (reader.nextName()) {
            "id" -> id = reader.nextString()
            "categoryID" -> category = reader.nextString()
            "difficulty" -> difficulty = reader.nextString()
            "prompt" -> prompt = reader.nextString()
            "correctIndex" -> correct = reader.nextInt()
            "answers" -> { reader.beginArray(); while (reader.hasNext()) answers.add(reader.nextString()); reader.endArray() }
            else -> reader.skipValue()
        }
        reader.endObject()
        require(answers.size == 4 && correct in 0..3 && id.isNotEmpty() && prompt.isNotBlank()) { "A bundled question is damaged." }
        result.add(Question(id, category, difficulty, prompt, answers, correct))
    }
    reader.endArray(); result
}
