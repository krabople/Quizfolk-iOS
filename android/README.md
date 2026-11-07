# Quizfolk for Android

Native Kotlin and Jetpack Compose implementation of Quizfolk 0.3.3 for Android 8.0
(API 26) and later, targeting Android 16 (API 36). The shared reviewed question
bank is copied into the app by Gradle; there is no separate Android question set.

## Phones and tablets

The same APK supports phones and tablets. Tablets use the full native window in
portrait and landscape, with adaptive topic and tournament grids, a navigation
rail in wide windows, and larger quiz controls. Landscape quizzes place the
question and player progress beside the four answers. Rotating preserves the
active match, question and score. Narrow and split-screen windows reflow to the
compact layout; phones retain their portrait presentation.

## Play with iPhone users

Both clients connect to the same production service:
`https://www.ways2earn.com/quizfolk-api/index.php`.
They use identical topic IDs, question IDs, four-option packets, version-3
reading/reveal requests, server clocks and scoring. Players can discover and
follow each other, send challenges in either direction, accept and play later,
share public tournaments and private friends tournaments, and appear in the same
topic leagues. No platform-specific matchmaking pool or ranking is created.

As in the current iOS version, a player account belongs to its device installation.
Cross-device sign-in/account recovery is not provided. Android creates a new,
globally unique player name; it does not silently transfer an existing iOS account.

## Included

| iOS feature | Android implementation |
| --- | --- |
| Topics, interests, random topic, Mixed topics | Same 30 topics plus virtual Mixed; search, favourites, counts and topic journey |
| Offline bot practice | Bundled bank, fresh content before repeats, no duplicate question in a match, local history |
| Human-first duels | Same six-second shared-service search, labelled recorded humans and bots |
| Delayed direct challenges | Same seven questions/order, immediate sender play, later acceptance and settlement |
| Scoring and pace | Three-second reading period, smoothly revealed 2×2 answers, ten-second clock, speed bonuses, double final round |
| Progress and results | Correct/incorrect markers for both players, shrinking time bar, win/draw announcement, confetti and answer review |
| Power-ups | Fifty Fifty 5, Double Choice 10, Right Answer 25; one per duel/run, server-owned deadlines and atomic automatic Right Answer submission |
| Social cards | Search, follow/unfollow, shared interests, titles, achievements, privacy/challenge settings, blocking and head-to-head results |
| Rematches | Fresh same-topic human invitations or bot games; links from finished games and saved history |
| Topic levels/leagues | Independent topic XP/levels; monthly/all-time and following filters; shared iOS/Android tables |
| Public survival tournaments | Three daily topics, weekly topics, paid entries, resume without another fee, first mistake ends run, best run counts |
| Fixed prizes | Daily 150/100/50 and weekly 500/250/125; shared server settlement, tie rules, receipt-backed congratulations |
| Friends tournaments | 2–8 players, 1–3 home/away cycles, chosen home topics, deadlines, host start/cancel, private boards, optional power-ups, free without prizes or paid |
| Coins and badges | 50 once-per-UTC-day opening reward, Daily Trail, gold coin icon, topic/event/rank badges, profile selection and persistent confirmation |
| Pictures and settings | Native Android photo picker, preview, cropped/metadata-free JPEG, name uniqueness and account deletion |
| Presentation | Shared Q logo, coral/ink/canvas colours, rounded Nunito type, matching navigation and profile action buttons; source names stay out of gameplay/review |

The backend already enforces the cross-platform rules. No new server or realtime
connection is required, and existing player data is preserved.

## Build

Use JDK 17 and an Android SDK with platform 36:

```sh
cd android
./gradlew :app:assembleDebug :app:testDebugUnitTest :app:lintDebug
./gradlew :app:connectedDebugAndroidTest
```

GitHub Actions runs isolated iOS/Android wire-contract tests, JVM scoring/deck
tests and separate phone and tablet emulator screen tests before producing a
signed APK and AAB. Tablet checks cover both orientations, native window sizing,
visible answer controls, rotation state, navigation and prize dialogs.
The emulator uses a debug-only service fixture and cannot create production
players or spend production coins. The fixture transport is absent from release
builds. Test screenshots and reports are uploaded as workflow artifacts.

The dedicated signing key is stored in encrypted GitHub secrets
`ANDROID_KEYSTORE_BASE64` and `ANDROID_STORE_PASSWORD`, with an encrypted local
backup outside the repository. Never replace or lose this key: updates must use
the same certificate. The public certificate digest is in
`signing-certificate.sha256`. Secrets and keystores are excluded from APK, AAB,
source packages and test artifacts. The APK is installable; the AAB is the Google
Play upload format.

Online account keys are encrypted with a non-exportable AES-GCM key in Android
Keystore. They are scoped to the configured HTTPS endpoint, excluded from backup
and never written to logs. Android's system picker is used instead of requesting
access to the whole photo library. Nunito's Open Font License is included in
`FONT-LICENSE.txt` and in the app assets.

## Optional notifications

The notification client and independent preference switches are implemented.
Actual push delivery requires the dedicated Firebase client configuration and
server provider credentials. The app reports unavailable delivery until configured.
See [push setup and verification](../docs/push-notifications.md).
