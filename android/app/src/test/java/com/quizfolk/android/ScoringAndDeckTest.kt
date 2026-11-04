package com.quizfolk.android

import org.junit.Assert.*
import org.junit.Test

class ScoringAndDeckTest {
    @Test fun speedDeadlinesAndFinalRoundMatchIOS() {
        assertEquals(20, Scoring.points(true,0.0,0)); assertEquals(17, Scoring.points(true,3.7,0))
        assertEquals(11, Scoring.points(true,9.99,0)); assertEquals(40, Scoring.points(true,0.0,6))
        for (elapsed in listOf(10.0, -1.0, Double.NaN, Double.POSITIVE_INFINITY)) assertEquals(0, Scoring.points(true,elapsed,0))
        assertEquals(0, Scoring.points(false,0.0,6)); assertEquals(160, (0..6).sumOf { Scoring.points(true,0.0,it) })
        assertEquals(300,Scoring.experience(160,100)); assertEquals(190,Scoring.experience(100,100)); assertEquals(90,Scoring.experience(50,100))
    }
    private fun q(id: String, text: String, topic: String = "22") = Question(id,topic,"easy",text,listOf("Correct","Wrong one","Wrong two","Wrong three"),0)
    @Test fun promptKeysPreserveMathematicalMeaning() {
        assertEquals(promptKey("  What’s Éarth? "),promptKey("WHAT'S   ÉARTH!!!")); assertEquals(promptKey("Straße?"),promptKey("STRASSE"))
        for ((a,b) in listOf("2+2" to "2×2", "2-3" to "23", "1.2" to "12", "2/3" to "23", "6!" to "6", "2^3" to "23", "−2" to "2", "3%" to "3", "2 ≤ 3" to "2 < 3", "now here" to "nowhere")) assertNotEquals(promptKey("Calculate $a?"),promptKey("Calculate $b?"))
    }
    @Test fun packetExcludesDuplicateIdsAndTypographyAndPrefersUnseenQuestions() {
        val old = q("old","What’s Earth?")
        val bank = listOf(old,q("copy","WHAT'S EARTH!!!"))+(0..8).map { q("fresh-$it","Fresh question $it?") }
        val history = listOf(MatchRecord("played","22",0,20,0,"Bot","practice",listOf(Round(old,0,0.0,20,0))))
        repeat(30) {
            val packet = freshPacket(bank,history,"22")
            assertEquals(7,packet.size); assertEquals(7,packet.map { it.id }.toSet().size); assertEquals(7,packet.map { it.key }.toSet().size)
            assertTrue(packet.all { it.id.startsWith("fresh-") && it.answers[it.correctIndex] == "Correct" })
        }
        assertEquals(6,freshPacket(listOf(old,q("copy","WHAT'S EARTH!!!"))+(0..4).map { q("fresh-$it","Fresh $it?") },emptyList(),"22").size)
    }
    @Test fun mixedPacketUsesDifferentTopicsAndNeverRepeatsContent() {
        val bank = (0..29).flatMap { topic -> (0..9).map { q("$topic-$it","Topic $topic question $it?",topic.toString()) } }
        repeat(20) { val packet = freshPacket(bank,emptyList(),"mixed"); assertEquals(7,packet.size); assertEquals(7,packet.map { it.categoryID }.toSet().size); assertEquals(7,packet.map { it.key }.toSet().size) }
    }
    @Test fun pendingResultsDoNotAwardPrematureWinsOrXPAndHistoryRoundTrips() {
        val record = MatchRecord("pending","22",1793836800,100,0,"Rival","challenge",listOf(Round(q("q","A question?"),0,1.0,19,0)),"duel",true,"rival")
        assertFalse(record.won); assertFalse(record.tied); assertEquals(0,record.xp)
        assertEquals(record,MatchRecord.parse(record.json()))
        assertEquals(240,record.copy(pending=false).xp)
    }
    @Test fun powersRemainConsumedAcrossQuestionsAndPodiumsAreGuaranteed() {
        val used = Power(true,"double",setOf(1)); assertEquals(Power(true),used.next())
        assertEquals(listOf(150,100,50),podium(json("kind" to "daily")))
        assertEquals(listOf(500,250,125),podium(json("kind" to "weekly")))
    }
}
