package com.quizfolk.android

import org.junit.Assert.*
import org.junit.Test

class TopicLevellingTest {
    @Test fun progressiveBoundariesAndFourPerfectWins() {
        listOf(0,1500,3500,6000,9000,12500,16500,21000,26000,31500).forEachIndexed { index, xp ->
            val progress = TopicLevelling.progress(xp)
            assertEquals(index+1,progress.level); assertEquals(0,progress.xpIntoLevel)
            assertEquals(1500+500*index,progress.xpForNextLevel)
            if (xp>0) { assertEquals(index,TopicLevelling.progress(xp-1).level); assertEquals(1,TopicLevelling.progress(xp-1).remainingXP) }
        }
        assertEquals(TopicLevelState(1,1200,1500),TopicLevelling.progress(4*Scoring.experience(160,100)))
        assertEquals(1,TopicLevelling.progress(-100).level)
        assertTrue(TopicLevelling.progress(Int.MAX_VALUE).remainingXP>0)
    }
    @Test fun onlyAnUpwardLevelBoundaryTriggersACelebration() {
        assertNull(TopicLevelling.levelUp(700,1000)); assertNull(TopicLevelling.levelUp(1600,1600)); assertNull(TopicLevelling.levelUp(1600,1000))
        val up = TopicLevelling.levelUp(1499,1700)!!
        assertEquals(1,up.previousLevel);assertEquals(2,up.progress.level);assertEquals(1800,up.progress.remainingXP)
    }
}
