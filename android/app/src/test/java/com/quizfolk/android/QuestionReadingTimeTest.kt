package com.quizfolk.android

import org.junit.Assert.assertEquals
import org.junit.Test

class QuestionReadingTimeTest {
    @Test fun longerQuestionsGetMoreTimeAndUnicodeDoesNotCountAsBytes() {
        assertEquals(3.0, QuestionReadingTime.seconds("Which planet is known as the Red Planet?"), 0.0)
        assertEquals(3.0, QuestionReadingTime.seconds("word ".repeat(12)), 0.0)
        assertEquals(9.0, QuestionReadingTime.seconds("word ".repeat(30)), 0.0)
        assertEquals(19.0, QuestionReadingTime.seconds("word ".repeat(60)), 0.0)
        assertEquals(4.0, QuestionReadingTime.seconds("🌿".repeat(90)), 0.0)
        assertEquals(3.0, QuestionReadingTime.seconds("  one\t two\nthree\u00a0four  "), 0.0)
    }
}
