#!/usr/bin/env bash
set -u
status=0
./gradlew :app:connectedDebugAndroidTest --no-daemon --stacktrace || status=$?
mkdir -p build/screenshots
adb pull /sdcard/Android/data/com.quizfolk.android.debug/files/screenshots/. build/screenshots/ || true
adb logcat -d > build/emulator-log.txt
exit "$status"
