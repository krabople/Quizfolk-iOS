#!/usr/bin/env bash
set -u
status=0
test_class="${1:-com.quizfolk.android.QuizfolkScreenTest}"
./gradlew :app:connectedDebugAndroidTest "-Pandroid.testInstrumentationRunnerArguments.class=$test_class" --no-daemon --stacktrace || status=$?
mkdir -p build/screenshots
adb pull /sdcard/Pictures/Quizfolk-Screenshots/. build/screenshots/ || true
adb logcat -d > build/emulator-log.txt
exit "$status"
