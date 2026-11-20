package com.quizfolk.android

import android.graphics.BitmapFactory
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.util.Base64
import java.nio.ByteBuffer

fun questionImageBytes(encoded: String?, sha: String?): ByteArray? = try {
    require(encoded != null && encoded.length <= 90000 && sha != null)
    val bytes = Base64.getDecoder().decode(encoded)
    require(bytes.size in 24..65536 && bytes.take(8) == listOf(137,80,78,71,13,10,26,10).map { it.toByte() })
    require(QuestionBankUpdates.sha(bytes) == sha)
    val header = ByteBuffer.wrap(bytes)
    require(header.getInt(16) in 1..512 && header.getInt(20) in 1..512)
    bytes
} catch (_: Exception) { null }

@Composable fun QuestionPicture(question: Question, modifier: Modifier = Modifier) {
    val image = remember(question.imageSHA256) { questionImageBytes(question.imagePng,question.imageSHA256)?.let { BitmapFactory.decodeByteArray(it,0,it.size)?.asImageBitmap() } }
    if(image != null) Image(image,"Question image",modifier.background(Color.White,RoundedCornerShape(12.dp)).border(1.dp,Color.LightGray,RoundedCornerShape(12.dp)).padding(10.dp).testTag("questionImage"),contentScale=ContentScale.Fit)
}

@Composable fun QuizQuestionContent(question: Question, size: Int = 25) {
    if(question.imagePng == null) AutoText(question.prompt,size,10,Color.White)
    else Column(Modifier.fillMaxSize(),horizontalAlignment=Alignment.CenterHorizontally,verticalArrangement=Arrangement.spacedBy(8.dp)) {
        Text(question.prompt,fontSize=minOf(size,22).sp,fontWeight=FontWeight.Bold,color=Color.White,textAlign=TextAlign.Center,maxLines=4)
        QuestionPicture(question,Modifier.fillMaxWidth().weight(1f))
    }
}
