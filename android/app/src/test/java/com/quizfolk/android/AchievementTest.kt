package com.quizfolk.android

import org.junit.Assert.*
import org.junit.Test

class AchievementTest {
    @Test fun legacyLockedPerfectExplainsTheRequirement() {
        val badge = json("id" to "perfect", "earned" to false)
        assertTrue(achievementRequirement(badge).contains("all seven questions correctly"))
        assertNull(achievementFraction(badge))
    }
    @Test fun lockedAndEarnedMilestonesKeepDescriptionsAndClampTheBar() {
        val badge = json("id" to "duels:1000", "description" to "Complete 1,000 online duels.", "progress" to 999, "target" to 1000, "earned" to false)
        assertEquals("Complete 1,000 online duels.", achievementRequirement(badge))
        assertEquals(.999f, achievementFraction(badge)!!, .0001f)
        badge.put("earned", true).put("progress", 1200)
        assertEquals(1f, achievementFraction(badge)!!, 0f)
        assertEquals("Complete 1,000 online duels.", achievementRequirement(badge))
    }
    @Test fun absentOrZeroTargetsDoNotProduceInvalidProgress() {
        assertNull(achievementFraction(json("target" to 0, "progress" to 20)))
        assertEquals(0f, achievementFraction(json("target" to 10, "progress" to -1))!!, 0f)
    }
}
