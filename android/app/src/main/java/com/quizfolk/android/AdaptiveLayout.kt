package com.quizfolk.android

import androidx.compose.foundation.layout.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import kotlin.math.floor

/** Uses the available window width, including split-screen and desktop resizing. */
@Composable fun <T> AdaptiveCards(
    items: List<T>,
    minWidth: Dp = 320.dp,
    compactColumns: Int = 1,
    gap: Dp = 16.dp,
    content: @Composable (T, Modifier) -> Unit
) {
    BoxWithConstraints(Modifier.fillMaxWidth()) {
        val columns = if (maxWidth < 600.dp) compactColumns else
            floor((maxWidth.value + gap.value) / (minWidth.value + gap.value)).toInt().coerceAtLeast(compactColumns)
        Column(verticalArrangement = Arrangement.spacedBy(gap)) {
            items.chunked(columns).forEach { row ->
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(gap)) {
                    row.forEach { item -> content(item, Modifier.weight(1f)) }
                    repeat(columns - row.size) { Spacer(Modifier.weight(1f)) }
                }
            }
        }
    }
}
