# Quizfolk for iPhone, iPad and Android

Native SwiftUI (iPhone and iPad) and Kotlin/Jetpack Compose (Android) apps inspired by the original QuizUp: follow topics, play seven-round timed duels, earn speed bonuses, practise against a labelled bot, review answers, track topic levels, and compete in monthly or all-time leagues.

## Included

- 21,667 individually reviewed, bundled four-option questions across 30 categories, with at least 176 in every topic. Per-topic counts appear in the app and `data/categories.json`; the review result is in `audit/individual-2026-10/completion.json`.
- Offline bot practice with persistent history and accuracy; practice stays out of online XP and topic levels.
- A PHP + SQLite backend for asynchronous direct challenges, human-first search, follows, player discovery and recorded human runs, with a six-second bot fallback.
- Server-owned online deadlines and scoring, authenticated match ownership, replay-safe answer submissions, name-based player cards, monthly and all-time filtered leaderboards, question reports and account deletion.
- GitHub Actions for simulator tests, device archives, screenshots and signed TestFlight upload.

## Android and cross-platform play

The native Android client is in [android/](android/README.md). It uses the same
production service, reviewed questions, globally unique player names, human
matchmaking, challenges, follows, tournaments, topic XP and rankings as iOS.
Android phone and tablet users can play iPhone and iPad users, including accepting challenges later and
joining the same private friends tournament. No second server or platform-only
player pool is used. Existing device-specific account/recovery limitations are
unchanged; Android does not automatically sign into an existing iPhone account.

GitHub's Android workflow runs cross-platform API contracts, unit tests and
separate phone and tablet emulator screen tests, then builds a signed installable APK and a Play AAB.
The same Android package fills the native tablet window, supports portrait and
landscape, and adapts topic grids, navigation and quiz controls to the available
width. Rotation preserves the active match and score.
See [Android setup and parity notes](android/README.md).

The published Android push testing release is
[0.3.3 (15)](https://github.com/krabople/Quizfolk-iOS/releases/tag/android-v0.3.3-15-preview).
It uses the existing signing certificate and the same service as iOS TestFlight
0.3.3. Further Android publication and advertising work are currently paused. In **You → Notifications**, players can independently choose challenge,
duel result, tournament prize and friends tournament alerts. Both server providers
are configured; physical-device delivery remains to be checked after opting in.
See [push activation and verification](docs/push-notifications.md).

## Open in Xcode

Requires macOS, Xcode 26 or later for App Store upload, and XcodeGen. Deployment target is iOS/iPadOS 17.0. The universal app supports portrait on iPhone and portrait, landscape and resizable windows on iPad.

```sh
brew install xcodegen
xcodegen generate
open Quizfolk.xcodeproj
```

Select your Apple team to run on a physical device. Offline practice needs no backend or account. The bundled server URL is `https://www.ways2earn.com/quizfolk-api/index.php`; it is editable on the player profile screen. A connection error is shown if the service is unavailable.

## Multiplayer model

Direct challenges let the sender finish immediately and the recipient accept later. Both get the same seven questions with independent clocks. The winner, topic XP and head-to-head tally settle once both finish. Invitations last 14 days. People supports name search, player cards, follows, shared interests, titles and blocking. Queued human searchers can also be paired this way.

Players do not need to be connected at the same time. A completed run supplies the opponent performance for a subsequent player on exactly the same questions and answer order. The later match labels the opponent **Recorded run**. If no eligible human run exists, **Pip · Bot** supplies an independent, precomputed performance. This does not create pending friend invitations or change the original player’s result later.

The question appears alone for three seconds before answers and the countdown. Online scores use the server's answer-choice reveal time. A correct answer before the 10-second deadline earns `20 - floor(elapsedSeconds)`. The seventh question doubles that. Wrong, late and missing answers score zero. The maximum is 160. Network transit counts against the online deadline; the client cannot submit its own elapsed time or score.

The account uses a random bearer key held in iOS Keychain. There is no password, cross-device sign-in or account recovery in this first version. Local stats and practice remain device-local. Online account deletion removes the player’s server history and anonymises references in other players’ recorded matches. Offline practice never enters the server league. Online bot duels do award XP to the human player; no bot account appears on the board.

## Isolated 123 Reg deployment

Required: PHP 8.1+ with PDO SQLite and a writable directory outside the web root. No MySQL setup or changes to an existing database are needed.

Recommended tree:

```text
home/
  quizfolk-service/
    backend/public/index.php
    backend/social.php
    backend/tournaments.php
    backend/names.php
    backend/name-fold.json
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
python3 scripts/test_social.py
python3 scripts/test_tournaments.py
```

The backend test creates two disposable players in the local service, exercises a full bot run and a human replay, verifies timing/idempotence/ownership/league filtering, then removes those two accounts. It requires a local SQLite file at `backend/private/quizfolk.sqlite` and must not be pointed at production.

GitHub’s iOS workflow builds and runs XCTest scoring, maximum-score, deadline, question-bank and shuffled-answer tests. Its artifact includes the simulator app, screenshot, test results and unsigned device archive. An unsigned archive is not directly installable on an iPhone.

The signed workflow requires `APPLE_TEAM_ID`, `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_API_KEY_BASE64`, `BUILD_CERTIFICATE_BASE64` and `P12_PASSWORD`. It reuses an existing distribution certificate, creates/reuses a dedicated Quizfolk App Store profile, builds a signed IPA and uploads it to App Store Connect. It never creates or revokes signing certificates. The initial signing invocation uses a separate manual-only workflow in the existing `ways2earn-ios` repository, so existing secret values stay there; that repository’s app build files are unchanged.

## Research, question quality and licence

The October 28 social and survival revision is documented in [docs/QUIZUP-RESEARCH.md](docs/QUIZUP-RESEARCH.md), including sources and deliberate differences from the historical app. Leagues now live inside topic pages, with visible period and following controls. Levels are independent by topic, finished duels close without an unfinished warning, and every question has a reading phase before the timer starts.

The dedicated Tournaments tab has three rotating daily topic events and weekly events. Earn speed points until the first wrong answer or timeout; there is no seven-question limit. Only the best run counts per event. Public events require earned coins. The top three places receive coin prizes and profile badges after closure; ties share the relevant prize shares. Private friends tournaments may instead use free entry without prizes. Tournament points are separate from duel XP. Coins have no cash value; no real-time server is involved.

## Optional rewarded ads on iOS

The iPhone and iPad client offers an optional video in **You → Earn coins** for **5 coins** per completed ad, with no daily cap or cooldown. AdMob supplies the ad after UMP privacy choices; only a signed, verified Google server callback credits the shared wallet. Cancelled or unavailable ads do not award coins. Pending verification survives relaunch, and repeated callbacks cannot duplicate a reward.

Debug UI tests use a local fixture. Physical TestFlight testing uses the production iOS unit with AdMob's app-level test mode enabled for marketing version **0.3.3**, so that version earns no advertising revenue. Do not disable test mode or submit a public App Store release until the owner has tested and approved it. Live ad serving also requires the linked store listing and AdMob readiness approval. Android advertising is not enabled on the server.

Release builds require the repository variables `QUIZFOLK_ADMOB_IOS_APP_ID` and `QUIZFOLK_ADMOB_IOS_REWARDED_UNIT_ID`; these are public SDK configuration, not authentication secrets. See [reward verification and deployment](docs/rewarded-ads.md) and the deployed [privacy policy](https://www.ways2earn.com/quizfolk-api/privacy.html).

See [RESEARCH.md](RESEARCH.md) for historical sources and product decisions. All 24,541 expanded candidate questions received individual editorial decisions covering meaning, answer accuracy and uniqueness, grammar and category relevance. The published bank contains 21,667 accepted questions across 30 base topics, with at least 176 per topic. The decision ledger and completion checks are in `audit/individual-2026-10`; these record editorial judgments rather than a guarantee that no errors remain.

Question data: [Open Trivia Database](https://opentdb.com/) and [OpenTriviaQA contributors](https://github.com/uberspot/OpenTriviaQA), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). See [THIRD-PARTY-NOTICES.txt](THIRD-PARTY-NOTICES.txt). The original Quizfolk app code and assets contain no QuizUp source code, logo or proprietary question collection.

## Rebuilding the expanded bank

Run `python3 scripts/import_bank.py /path/to/opentdb/all_questions.json`, followed by `python3 scripts/import_extended_bank.py /path/to/OpenTriviaQA`. The second importer rejects malformed answers, duplicates, time/context-dependent prompts, excessively long text and position-dependent answers. Source question difficulty is shown as Mixed where no difficulty was supplied. The server reads only the selected category through an indexed SQLite query, rather than decoding the entire 19 MB JSON bank for each match.

## October 27 revision

Topic-specific monthly/all-time XP leagues, reserved unique player names, profile photo selection and removal, animated matchup countdown and winner screen, prominent timer and correct/incorrect progress markers. See `RESEARCH.md` for the historical QuizUp scoring evidence and `audit/README.md` for question review scope. The individual pass reviewed all 24,541 expanded candidates: 18,530 edited, 3,137 kept and 2,874 excluded, leaving 21,667 active questions. Every decision records separate meaning, answer, grammar and category judgments.

The additional temporal screen in audit/time_rules.py holds undated superlatives, records, changing quantities and personal/demographic claims for editorial review. It intentionally holds some valid stable facts as well. The population question exposed in screenshot review was held with its census source recorded in the ledger.


## Friends tournaments and quiz controls (3 November 2026)

Private code-only round robins support 2–8 members, one to three home/away
cycles, a 1/3/7/14-day deadline and optional power-ups. The host chooses free entry without prizes, or a 10-coin entry per member. Unstarted lobbies refund after 24 hours or host cancellation.
Each pair plays both home topics in every cycle. Win/draw/loss awards 3/1/0
league points; tied points share a place. Only completed duels count. Paid entry
pools award podium coins and profile badges using the existing prize system.
The board and fixtures require membership; public survival boards reject
private events. Settings and membership lock at the start. No live server is
needed. All matches retain the existing asynchronous seven-question rules.

Mixed topics is a virtual category over the reviewed bank, sampling seven
different categories per duel. Random topic chooses one of the 30 base topics.
The bank itself remains 21,667 individually reviewed questions.

Questions have a three-second reading period followed by the answer clock.
Two-by-two answer tiles slide into place with reduced-motion support. Progress
shows saved answer counts for each player; asynchronous rivals are not shown
as if they were live. One power-up per duel/survival run is enforced by the
server: Fifty Fifty (5 coins), Double Choice (10), Right Answer (25). The clock
keeps running. These tariffs and the cap are Quizfolk rules, not established
historical QuizUp constants. See docs/QUIZUP-RESEARCH.md.

Deploy backend/powers.php and backend/parties.php alongside the other service
files. Do not overwrite backend/private/quizfolk.sqlite. The new tables are
additive and created automatically. Run `python3 scripts/run_contracts.py`
against a clean checkout for all isolated HTTP tests. A matching iOS release
and backend deployment are both required before these features are live.

## Guaranteed prizes and clearer quiz feedback (4 November 2026)

The 4 November policy fixed daily podium prizes at 150 / 100 / 50 coins and
weekly podiums at 500 / 250 / 125. Those historical terms remain attached to
events closed before the 8 November change below. Prizes do not depend on entries. Ties share the combined
prizes for their occupied positions; a sole entrant receives first prize.
Closed public tournaments receive a one-time reconciliation of any unpaid
shortfall. Existing larger awards are preserved. The migration takes a SQLite
snapshot first, uses unique ledger references and reopens the prize notice when
it credits a shortfall. Private friends tournaments keep their chosen free or
paid rules.

Both quiz modes show a shrinking answer-time bar immediately above the prompt,
turning red for the last three seconds. Rival markers use actual correct/wrong
results; asynchronous results stay neutral until both players answer that round.
Tournament badges combine the topic icon/colour, a daily seal or weekly shield,
and a gold/silver/bronze placing ribbon. Friends badges use a group icon.

## Public tournament prices and prizes (8 November 2026)

Every public daily tournament costs 25 coins to enter and awards 500 / 250 / 125
coins to the podium. Every public weekly tournament costs 50 coins and awards
1000 / 500 / 250. These prices and prizes apply to current and future open
events. Closed events retain their historical entry terms, prizes and results.
The server supplies each event's prize table to both apps; private friends
tournaments retain their free-entry or 10-coin rules. Ties continue to share
the combined prizes for their occupied positions.


## Daily opening reward and profile polish (4 November 2026)

Opening or returning to the app automatically earns 50 coins once per UTC day,
resetting at 00:00 UTC. The server ledger makes retries and multiple launches
idempotent. Existing clients also claim this reward through their launch/resume
prize-inbox request. Daily Trail earnings remain an additional 45 coins per day.
Right Answer now selects and submits the correct option in the same server
transaction as its purchase, using the original answer clock. A retry returns
the saved answer without another debit. Older clients keep their highlight-and-tap
behaviour. Wearing a prize badge saves and acknowledges it atomically, followed
by a persistent confirmation popup. Wallets use a gold coin symbol, and profile
shortcuts are aligned buttons.


Finished duels now have an explicit Rematch action. Human rematches send a new
idempotent challenge to the same player in the same topic; bot rematches keep
the bot label and online/practice mode, using a fresh question packet. Saved
human-match reviews link to the opponent's public profile. Results portraits,
topic leagues, survival standings and private friends standings open player
cards, including follow controls. Source labels were removed from gameplay and
review screens; adapted-data attribution is consolidated at You > Credits &
licences and records the individual editorial corrections.

## Progressive topic levels (5 November 2026)

Topic levels now start at 1,500 XP for level 2. Each subsequent step costs
500 XP more: level 3 starts at 3,500 total XP, level 4 at 6,000, and level 5
at 9,000. Earned XP, scores and match history are preserved; the displayed
levels and title eligibility are recalculated from the new curve. Four perfect
duel wins give 1,200 XP and therefore stay at level 1. Levels remain independent
for every topic, and practice does not count toward online topic progression.

The backend, iOS and Android use the same integer calculation and exact boundary
tests. Topic progress bars show the actual remaining XP. Newly settled duels
show a prominent animated level-up card on the result screen when their XP
crosses a level boundary, including when a pending result is checked in that
session. Reopening a settled match does not celebrate it again. Reduced-motion
settings suppress the entrance animation.

Online fallback and offline practice draw from the same 32 named bots, avoiding
the last five selections. An online match keeps its chosen name on retries and
in history. The bot intro explains that no human opponent could be found before confirming the bot match.
