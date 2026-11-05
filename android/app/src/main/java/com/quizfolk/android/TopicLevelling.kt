package com.quizfolk.android

data class TopicLevelState(val level: Int, val xpIntoLevel: Int, val xpForNextLevel: Int) {
    val remainingXP get() = xpForNextLevel - xpIntoLevel
}
data class TopicLevelUp(val previousLevel: Int, val progress: TopicLevelState)

object TopicLevelling {
    // Same integer curve as iOS and the service: 250 * (L-1) * (L+4).
    fun progress(xp: Int): TopicLevelState {
        val safeXP = xp.coerceAtLeast(0)
        var lower = 0
        var upper = safeXP / 1500 + 1
        while (lower < upper) {
            val middle = lower + (upper - lower + 1) / 2
            if (middle <= (safeXP / 250) / (middle + 5)) lower = middle else upper = middle - 1
        }
        return TopicLevelState(lower + 1, safeXP - 250 * lower * (lower + 5), 1500 + 500 * lower)
    }
    fun levelUp(beforeXP: Int, afterXP: Int): TopicLevelUp? {
        val before = progress(beforeXP)
        val after = progress(afterXP)
        return if (after.level > before.level) TopicLevelUp(before.level, after) else null
    }
}
