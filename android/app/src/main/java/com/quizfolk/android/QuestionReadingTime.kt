package com.quizfolk.android

import kotlin.math.ceil

object QuestionReadingTime {
    fun seconds(prompt: String): Double {
        val words = prompt.split(Regex("[\\p{Z}\\s]+")).filter { it.isNotEmpty() }
        val normal = words.joinToString(" ")
        val characters = normal.codePointCount(0, normal.length)
        return 3.0 + ceil(maxOf(0.0, (words.size - 12) / 3.0, (characters - 72) / 18.0))
    }
}
