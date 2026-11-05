package com.quizfolk.android

import org.junit.Assert.*
import org.junit.Test

class NotificationPolicyTest {
    @Test fun newAccountsRequireOptInAndHaveSeparateCategories() {
        val prefs=defaultPushChoices();assertFalse(prefs.b("enabled"))
        assertEquals(setOf("challenges","duelResults","tournamentPrizes","friendsTournaments"),pushKinds.keys)
        pushKinds.keys.forEach { assertTrue(prefs.b(it)) }
    }
    @Test fun notificationTapsCannotNavigateToArbitraryLinksOrUnknownActions() {
        pushKinds.keys.forEach { assertNotNull(PushDestination.parse(mapOf("kind" to it,"id" to "week:20261105:22","topicID" to "22"))) }
        assertNull(PushDestination.parse(mapOf("kind" to "openURL","id" to "https://example.com")))
        assertNull(PushDestination.parse(mapOf("kind" to "challenges","id" to "../../private")))
        assertNull(PushDestination.parse(mapOf("kind" to "challenges","id" to "")))
    }
}
