package com.quizfolk.android

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.net.Uri
import android.util.Base64
import androidx.exifinterface.media.ExifInterface
import java.io.ByteArrayOutputStream

object PhotoProcessor {
    fun make(context: Context, uri: Uri): String {
        val resolver = context.contentResolver
        val options = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        resolver.openInputStream(uri).use { BitmapFactory.decodeStream(it, null, options) }
        require(options.outWidth > 0 && options.outHeight > 0) { "Choose a valid photo." }
        var sample = 1
        while (maxOf(options.outWidth, options.outHeight) / sample > 1024) sample *= 2
        options.inJustDecodeBounds = false; options.inSampleSize = sample
        val input = resolver.openInputStream(uri).use { BitmapFactory.decodeStream(it, null, options) } ?: error("That photo could not be opened.")
        val orientation = runCatching { resolver.openInputStream(uri).use { ExifInterface(requireNotNull(it)).getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL) } }.getOrDefault(ExifInterface.ORIENTATION_NORMAL)
        val matrix = Matrix().apply {
            when (orientation) {
                ExifInterface.ORIENTATION_FLIP_HORIZONTAL -> setScale(-1f, 1f)
                ExifInterface.ORIENTATION_ROTATE_180 -> setRotate(180f)
                ExifInterface.ORIENTATION_FLIP_VERTICAL -> setScale(1f, -1f)
                ExifInterface.ORIENTATION_TRANSPOSE -> { setRotate(90f); postScale(-1f, 1f) }
                ExifInterface.ORIENTATION_ROTATE_90 -> setRotate(90f)
                ExifInterface.ORIENTATION_TRANSVERSE -> { setRotate(270f); postScale(-1f, 1f) }
                ExifInterface.ORIENTATION_ROTATE_270 -> setRotate(270f)
            }
        }
        val rotated = Bitmap.createBitmap(input, 0, 0, input.width, input.height, matrix, true)
        val edge = minOf(rotated.width, rotated.height)
        val crop = Bitmap.createBitmap(rotated, (rotated.width - edge)/2, (rotated.height - edge)/2, edge, edge)
        val photo = Bitmap.createScaledBitmap(crop, 128, 128, true)
        var quality = 90; var output: ByteArray
        do { val stream = ByteArrayOutputStream(); photo.compress(Bitmap.CompressFormat.JPEG, quality, stream); output = stream.toByteArray(); quality -= 10 } while (output.size > 16384 && quality >= 40)
        require(output.size <= 16384) { "Please choose a simpler photo." }
        return Base64.encodeToString(output, Base64.NO_WRAP)
    }
}
