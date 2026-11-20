package com.quizfolk.android
import org.junit.Assert.*
import org.junit.Test

class QuestionImagesTest {
    @Test fun pictureAndFactIdentitySurviveHistoryAndShuffling() {
        val q=Question("one","41","easy","Which country?",listOf("Japan","France","Italy","Canada"),0,"png","abc")
        assertEquals(q,Question.parse(q.json()))
        assertEquals("abc",q.shuffled().imageSHA256)
        assertNotEquals(q.key,q.copy(imageSHA256="def").key)
        assertEquals(q.copy(questionGroup="capitals:JP").key,q.copy(prompt="Which capital?",questionGroup="capitals:JP").key)
        assertNull(questionImageBytes("broken","abc"))
        assertNull(questionImageBytes("x".repeat(100000),"abc"))
    }
}
