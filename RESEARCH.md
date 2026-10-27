# Quizfolk: original QuizUp research and design decisions

Research date: 26 October 2026. This references Plain Vanilla’s original 2013–2021 QuizUp, not the unrelated current quizup.app website.

## What to preserve

The original developer interview describes the appeal of specific interests rather than only broad general-knowledge genres: players get excited about a particular fictional world, sport or subject. It also describes an emphasis on reducing steps to play. Source: [Microsoft’s interview with Plain Vanilla’s COO, 26 June 2015](https://blogs.windows.com/devices/2015/06/26/quizups-plain-vanilla-games-developer-profile/).

The historical gameplay reference describes six normal rounds followed by a double-points seventh round, four answers, ten seconds, and scoring based on accuracy and speed, with 160 as the theoretical maximum. Source: [QuizUp Gameplay archive](https://quiz-up.fandom.com/wiki/QuizUp_Gameplay). This community reference is not an official specification. Quizfolk uses an explicit deadline: an answer arriving at or after 10 seconds scores zero; before the deadline a correct answer scores 20 minus whole elapsed seconds. The last round doubles that result.

The designer’s account highlights the final interface’s colourful palette, quick access to play, and simple shapes after extensive design iteration. Source: [Fast Company’s interview with chief designer Sveinn Davidsson, 8 January 2014](https://www.fastcompany.com/3024296/3-design-lessons-from-the-worlds-fastest-growing-quiz-app). Quizfolk uses its own name, icon, typography, layout and original UI code, drawing on the colourful topic-led structure.

The 2015 revision expanded the social experience and profile statistics. Source: [The Next Web, 21 May 2015](https://thenextweb.com/news/quizup-2-0-lands-with-a-new-design-focus-on-social-interaction-and-support-for-the-desktop). Quizfolk initially prioritises selecting interests, playing, reviewing answers and tracking topic progress; social feeds and messaging are outside this first build.

## Affordable asynchronous competition

There are no WebSockets, live rooms, persistent opponent connections, or polling loops. Each player gets seven questions one at a time via ordinary HTTPS requests. The backend stores a completed run’s questions, answer order, points and timing. A later player in the same category competes against that recorded human performance. The UI explicitly labels it a recorded run. Both players see the same questions and option order. When no eligible run is available, a named bot with difficulty-based accuracy provides the opposition. Bot decisions are made before the player answers, independently of the player’s score.

This is asynchronous competition against recorded performances; it is not a pending friend challenge and does not retroactively change the first player’s result. Friend invitations, mutual turn-based matches and push notifications can be added later. There are about 15 short requests per duel, not zero server costs. At substantial scale, shared CPU, I/O, storage and SQLite write contention still need monitoring.

## Question bank and limits

The shipped bank contains **24,834 screened four-answer questions across 30 categories**. The original 45,581-record import remains traceable through Git history and the audit ledger. The 27 October audit held 20,747 uncertain records out of play; these are retained in `audit/quarantined-questions.json`, outside the app and serving database. No generated distractors were added to inflate the count.

Every original record received automated structure, context, temporal wording, reading length, answer dependency and semantic topic-fit checks. Samples from every category were read for wording and topic fit; specific manual changes are marked in the ledger. This is **not an individual human factual verification of all 45,581 records**. Semantic similarity is a conservative screening aid, not a correctness guarantee. A later editorial pass is still needed. Actual active category counts are in `data/audit-report.json` and in the app. The importer is a raw-source staging tool; its output must not replace the screened serving bank without a new audit.

The reported “Calculate 6!” question was rewritten to explain factorial notation, independently calculated as 720, and moved to Mathematics. Records requiring absent images, missing sequences, ambiguous answer references or questionable topic assignment were held instead of guessed at.

Sources and licences:

- [Open Trivia Database](https://opentdb.com/) via [the Open Trivia Dataset snapshot](https://github.com/lipschultz/open-trivia-dataset), commit `77d8e3cb5c8e264d50220eee75cfe08d233b1910`. Its [API documentation](https://opentdb.com/api_config.php) publishes the data under CC BY-SA 4.0.
- [OpenTriviaQA contributors](https://github.com/uberspot/OpenTriviaQA), commit `dcc1cdf36c2985ed5c849d1f2265c5041ffcdfb9`, whose repository declares CC BY-SA 4.0.
- The adapted question bank is distributed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). A licence copy is included. Source and licence attribution appear inside the app and in the data. This does not apply the data licence to the original app code.

## Hosting choice

[123 Reg’s hosting page](https://www.123-reg.co.uk/web-hosting/) describes shared cPanel hosting and MySQL availability; that does not establish this account’s actual capacity. The supplied backend uses PHP 8.1+ and PDO SQLite, so it needs no existing MySQL database, credentials or website tables. Its persistent state belongs outside the public document root. A public wrapper loads the isolated code and data. No changes to the existing website’s index, root rewrite rules, DNS or databases are required.

## Build costs

GitHub documents free standard hosted runners for public repositories in its [runner guidance](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job). Larger runners and artifact storage have separate limits. The workflows use standard `macos-15` runners and bounded artifact retention.

## Before a public App Store launch

This initial TestFlight build needs wider device testing, editorial question review, expansion of small categories, account recovery, name/report moderation, operational backups, and load testing. The server checks question deadlines and calculates all online points; public question data, rooted devices and automated answer tools mean this is not a cheat-proof competitive platform. Offline practice never submits scores to the online leagues. Online bot duels count towards human players’ XP, but bots are not leaderboard accounts.

## Original QuizUp topic leagues and XP (27 October follow-up)

A contemporary player's [2014 GameBlast review](https://www.gameblast.com.br/2014/08/quizup-android-ios.html) describes XP consisting of match points and bonuses, and topic rankings that renewed monthly. The creator of a [historical QuizUp leaderboard recorder](https://hellession.com/projects.html) also describes monthly leaderboard history. This supports a monthly, topic-specific XP table rather than one cross-topic sum of raw match points.

An original results screenshot reproduced in [this research thesis](https://ela.kpi.ua/bitstreams/ee69a21c-d9e1-48be-b7c3-8e51235cd6c8/download) shows match score 70 + finish bonus 40 + victory bonus 100 = total XP 210. [A contemporary player's account](https://karlcrockets10.wordpress.com/category/german/) describes the 50 XP draw bonus. Quizfolk therefore awards score + 40 finish + 100 win / 50 draw / 0 loss, with separate monthly and all-time XP tables for every topic. Month boundaries use UTC. Historical completed duels are recalculated with these bonuses rather than losing player history. Paid XP multipliers are excluded. The app's simple level thresholds are its own design; the research does not establish an exact historical QuizUp level curve.

Player names are reserved by a case-folded unique database index. Existing collisions are resolved during a transactional migration, retaining player keys and history; a consistent private SQLite snapshot is taken first. Pictures use Apple's photo picker, are centre-cropped to 128 square pixels and re-encoded as JPEG without original metadata. The authenticated service stores at most 16 KiB per picture and supplies it on player cards, topic leagues and recorded-opponent introductions. Removing a picture clears the server copy. The main website is outside the deployed app paths.
