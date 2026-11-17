package com.quizfolk.android

import androidx.test.ext.junit.runners.AndroidJUnit4
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class BankUpdateTest {
    private fun fixture(): JSONObject = JSONObject().put("format",1)
        .put("categories",JSONArray().put(JSONObject().put("id","99").put("name","A new topic").put("color","008080").put("emoji","🌿").put("questionCount",7)))
        .put("questions",JSONArray((0..6).map { JSONObject().put("id","new-$it").put("categoryID","99").put("difficulty","easy").put("prompt","New question $it?").put("answers",JSONArray(listOf("A","B","C","D"))).put("correctIndex",0) }))
    private fun parse(value: JSONObject) = readMobileQuestionBank(value.toString().reader())
    @Test fun acceptsNewTopicAndQuestions() {
        val bank=parse(fixture());assertEquals("99",bank.categories.single().id);assertEquals(7,bank.questions.size)
    }
    @Test fun rejectsInvalidSnapshots() {
        var value=fixture();value.getJSONArray("categories").getJSONObject(0).put("questionCount",8)
        assertThrows(IllegalArgumentException::class.java) { parse(value) }
        value=fixture();value.getJSONArray("questions").getJSONObject(0).put("categoryID","missing")
        assertThrows(IllegalArgumentException::class.java) { parse(value) }
        value=fixture();value.getJSONArray("questions").getJSONObject(1).put("id","new-0")
        assertThrows(IllegalArgumentException::class.java) { parse(value) }
        value=fixture();value.getJSONArray("questions").getJSONObject(0).put("correctIndex",4)
        assertThrows(IllegalArgumentException::class.java) { parse(value) }
        value=fixture();value.getJSONArray("questions").getJSONObject(0).put("answers",JSONArray(listOf("A","A","C","D")))
        assertThrows(IllegalArgumentException::class.java) { parse(value) }
    }
    @Test fun usesStandardSha256() {
        assertEquals("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",QuestionBankUpdates.sha("abc".toByteArray()))
    }
}
