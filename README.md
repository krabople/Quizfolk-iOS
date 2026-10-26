# Quizfolk for iPhone

A native SwiftUI trivia app inspired by the original QuizUp: follow topics, play seven-round timed duels, earn speed bonuses, practise against a labelled bot, review answers, track topic levels, and compete in weekly or all-time leagues.

## Included

- 45,581 bundled four-option questions across 30 categories. Actual per-topic counts appear in the app and `data/import-report.json`.
- Offline bot practice with persistent history, local XP, per-topic levels and accuracy.
- A PHP + SQLite backend for asynchronous duels against recorded human runs, with bot fallback when no run is available.
- Server-owned online deadlines and scoring, authenticated match ownership, replay-safe answer submissions, name-based player cards, weekly and all-time filtered leaderboards, question reports and account deletion.
- GitHub Actions for simulator tests, device archives, screenshots and signed TestFlight upload.

## Open in Xcode

Requires macOS, Xcode 26 or later for App Store upload, and XcodeGen. Deployment target is iOS 17.0, iPhone only.

```sh
brew install xcodegen
xcodegen generate
open Quizfolk.xcodeproj
```

Select your Apple team to run on a physical device. Offline practice needs no backend or account. The bundled server URL is `https://www.ways2earn.com/quizfolk-api/index.php`; it is editable on the player profile screen. A connection error is shown if the service is unavailable.

## Multiplayer model

Players do not need to be connected at the same time. A completed run supplies the opponent performance for a subsequent player on exactly the same questions and answer order. The later match labels the opponent **Recorded run**. If no eligible human run exists, **Pip · Bot** supplies an independent, precomputed performance. This does not create pending friend invitations or change the original player’s result later.

Online scores are calculated by the server from its own question start time. A correct answer before the 10-second deadline earns `20 - floor(elapsedSeconds)`. The seventh question doubles that. Wrong, late and missing answers score zero. The maximum is 160. Network transit counts against the online deadline; the client cannot submit its own elapsed time or score.

The account uses a random bearer key held in iOS Keychain. There is no password, cross-device sign-in or account recovery in this first version. Local stats and practice remain device-local. Online account deletion removes the player’s server history and anonymises references in other players’ recorded matches. Offline practice never enters the server league. Online bot duels do award XP to the human player; no bot account appears on the board.

## Isolated 123 Reg deployment

Required: PHP 8.1+ with PDO SQLite and a writable directory outside the web root. No MySQL setup or changes to an existing database are needed.

Recommended tree:

```text
home/
  quizfolk-service/
    backend/public/index.php
    backend/private/             # created by PHP; never web accessible
    data/question-bank.sqlite
    data/categories.json
  public_html/
    quizfolk-api/
      index.php                 # loads the service outside public_html
      .htaccess
```

The public wrapper is:

```php
<?php
require dirname(__DIR__, 2).'/quizfolk-service/backend/public/index.php';
```

Leave the website’s root index, rewrite rules, DNS, WordPress files and database untouched. In production, back up `backend/private/quizfolk.sqlite` consistently (SQLite backup API or `VACUUM INTO`; copying only the DB while WAL writes are active is insufficient). Monitor disk usage and load. Shared hosting still shares CPU and I/O with the website even though the files and data are separate. Rate limits help but are not a substitute for load testing or abuse protection.

Endpoints use the `r` query parameter: `health`, `categories`, `register`, `profile`, `update-profile`, `match`, `round`, `answer`, `leaderboard`, `report`, and `delete-account`. Mutations require POST JSON; player endpoints require `Authorization: Bearer ...`. Only registration returns the account key. The API sends no answer key before submission. Report handling currently stores reports for later editorial review; it does not automatically unpublish a question.

## Verification

```sh
python3 scripts/validate_bank.py
php -l backend/public/index.php
php -S 127.0.0.1:8770 -t backend/public
# In a second terminal, on an isolated local test database only:
python3 scripts/test_backend.py
```

The backend test creates two disposable players in the local service, exercises a full bot run and a human replay, verifies timing/idempotence/ownership/league filtering, then removes those two accounts. It requires a local SQLite file at `backend/private/quizfolk.sqlite` and must not be pointed at production.

GitHub’s iOS workflow builds and runs XCTest scoring, maximum-score, deadline, question-bank and shuffled-answer tests. Its artifact includes the simulator app, screenshot, test results and unsigned device archive. An unsigned archive is not directly installable on an iPhone.

The signed workflow requires `APPLE_TEAM_ID`, `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_API_KEY_BASE64`, `BUILD_CERTIFICATE_BASE64` and `P12_PASSWORD`. It reuses an existing distribution certificate, creates/reuses a dedicated Quizfolk App Store profile, builds a signed IPA and uploads it to App Store Connect. It never creates or revokes signing certificates. The initial signing invocation uses a separate manual-only workflow in the existing `ways2earn-ios` repository, so existing secret values stay there; that repository’s app build files are unchanged.

## Research, question quality and licence

See [RESEARCH.md](RESEARCH.md) for historical sources, product decisions and remaining release work. The bank is structurally validated community content, not independently fact-checked. Category sizes range from 70 to 10,175 questions; the smaller specialist categories still merit further expansion. It is not a complete clone of QuizUp’s historical content library.

Question data: [Open Trivia Database](https://opentdb.com/) and [OpenTriviaQA contributors](https://github.com/uberspot/OpenTriviaQA), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). See [THIRD-PARTY-NOTICES.txt](THIRD-PARTY-NOTICES.txt). The original Quizfolk app code and assets contain no QuizUp source code, logo or proprietary question collection.

## Rebuilding the expanded bank

Run `python3 scripts/import_bank.py /path/to/opentdb/all_questions.json`, followed by `python3 scripts/import_extended_bank.py /path/to/OpenTriviaQA`. The second importer rejects malformed answers, duplicates, time/context-dependent prompts, excessively long text and position-dependent answers. Source question difficulty is shown as Mixed where no difficulty was supplied. The server reads only the selected category through an indexed SQLite query, rather than decoding the entire 19 MB JSON bank for each match.
