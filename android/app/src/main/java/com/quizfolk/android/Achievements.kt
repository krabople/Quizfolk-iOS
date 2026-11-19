package com.quizfolk.android

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

fun achievementRequirement(badge: J): String = badge.s("description").ifBlank {
    when (badge.s("id")) {
        "first" -> "Complete your first online duel."
        "winner" -> "Win your first completed online duel."
        "perfect" -> "Answer all seven questions correctly in one completed online duel."
        "ten" -> "Complete ten online duels."
        "explorer" -> "Complete online duels in five different topics."
        else -> if (badge.s("topicID").isEmpty()) "Complete this milestone through online play." else "Earn a podium finish in a tournament in this topic."
    }
}
fun achievementFraction(badge: J): Float? = if (badge.has("progress") && badge.n("target") > 0)
    (badge.n("progress").toFloat() / badge.n("target")).coerceIn(0f, 1f) else null
private fun achievementGroup(badge: J) = badge.s("group").ifBlank { if (badge.s("topicID").isEmpty()) "Milestones" else "Best tournament finishes" }

@Composable private fun AchievementIcon(badge: J, store: QuizStore) {
    if (badge.s("kind").isNotEmpty()) Medal(badge, store) else Icon(when (badge.s("symbol")) {
        "bolt.fill" -> Icons.Default.Bolt
        "target" -> Icons.Default.Adjust
        "flame.fill" -> Icons.Default.LocalFireDepartment
        "globe" -> Icons.Default.Public
        "checkmark.seal.fill", "checkmark.circle.fill" -> Icons.Default.CheckCircle
        "graduationcap.fill" -> Icons.Default.School
        else -> Icons.Default.EmojiEvents
    }, null, tint = if (badge.b("earned")) Coral else Color.Gray, modifier = Modifier.size(40.dp))
}
@Composable fun AchievementPanel(badges: List<J>, store: QuizStore) {
    var filter by remember { mutableStateOf("All") }
    var selected by remember { mutableStateOf<J?>(null) }
    val visible = badges.filter { filter == "All" || if (filter == "Unlocked") it.b("earned") else !it.b("earned") }
    Panel {
        Heading("Achievements")
        Text("${badges.count { it.b("earned") }} of ${badges.size} unlocked")
        Hint("Milestones to work towards, and your best public tournament finish in each topic. Tap any achievement to see its requirement and progress.")
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            listOf("All", "Unlocked", "Locked").forEach { option ->
                FilterChip(selected = filter == option, onClick = { filter = option }, label = { Text(option) }, modifier = Modifier.testTag("achievement-filter-$option"))
            }
        }
        if (visible.isEmpty()) Hint(if (filter == "Locked") "Every available achievement has been unlocked." else "No achievements in this section yet.")
        visible.map(::achievementGroup).distinct().forEach { group ->
            Text(group, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 9.dp))
            visible.filter { achievementGroup(it) == group }.forEach { badge ->
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(13.dp),
                    modifier = Modifier.fillMaxWidth().testTag("achievement-${badge.s("id")}").clickable { selected = badge }.padding(vertical = 9.dp)) {
                    AchievementIcon(badge, store)
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                        Text(badge.s("name"), fontWeight = FontWeight.SemiBold)
                        Text(achievementRequirement(badge), style = MaterialTheme.typography.bodySmall, color = Color.Gray, maxLines = 2)
                        if (badge.s("progressLabel").isNotBlank()) Hint(badge.s("progressLabel"))
                        achievementFraction(badge)?.let { progress -> LinearProgressIndicator(progress = { progress }, modifier = Modifier.fillMaxWidth(), color = if (badge.b("earned")) Color(0xFF30A66B) else Coral) }
                    }
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Hint(if (badge.b("earned")) "Unlocked" else "Locked")
                        Icon(Icons.Default.Info, "View achievement details", tint = Color.Gray)
                    }
                }
            }
        }
    }
    selected?.let { badge ->
        AlertDialog(onDismissRequest = { selected = null }, title = { Text(badge.s("name")) }, text = {
            Column(Modifier.heightIn(max = 460.dp).verticalScroll(rememberScrollState()), verticalArrangement = Arrangement.spacedBy(16.dp)) {
                AchievementIcon(badge, store)
                Text(if (badge.b("earned")) "Unlocked" else "Not unlocked yet", fontWeight = FontWeight.Bold)
                Text("How to unlock", fontWeight = FontWeight.Bold)
                Text(achievementRequirement(badge), Modifier.testTag("achievementRequirement"))
                if (badge.s("progressLabel").isNotBlank()) {
                    Text("Progress", fontWeight = FontWeight.Bold)
                    Text(badge.s("progressLabel"), Modifier.testTag("achievementProgress"))
                    achievementFraction(badge)?.let { progress -> LinearProgressIndicator(progress = { progress }, modifier = Modifier.fillMaxWidth(), color = Coral) }
                }
            }
        }, confirmButton = { TextButton({ selected = null }) { Text("Done") } })
    }
}
