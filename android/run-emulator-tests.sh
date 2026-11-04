#!/usr/bin/env bash
set -u
status=0
./gradlew :app:connectedDebugAndroidTest --no-daemon --stacktrace || status=$?
mkdir -p build/screenshots
adb pull /sdcard/Pictures/Quizfolk-Screenshots/. build/screenshots/ || true
adb logcat -d > build/emulator-log.txt
exit "$status"
