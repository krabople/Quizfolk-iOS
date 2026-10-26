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

The initial snapshot contains **4,018 distinct four-answer questions across 24 categories**, imported from 4,738 source records. 717 true/false questions and 3 duplicates were excluded. Every included record has a stable ID, source, licence and an `imported_unreviewed` label. HTML entities were decoded. The importer validates structure, not factual accuracy. No claim is made that the bank is fully fact-checked or comparable in size to QuizUp’s historical hundreds of thousands of questions.

The category sizes are intentionally visible in the app and [data/import-report.json](data/import-report.json). Video Games has 945 questions; Gadgets has only 28. The smaller categories need editorial expansion before a broad launch. Avoid manufacturing four-answer trivia by merely expanding true/false prompts or generating unverified distractors.

Source snapshot: [lipschultz/open-trivia-dataset](https://github.com/lipschultz/open-trivia-dataset), commit `77d8e3cb5c8e264d50220eee75cfe08d233b1910`. Underlying source: [Open Trivia Database](https://opentdb.com/), whose [API documentation](https://opentdb.com/api_config.php) publishes the data under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Attribution and licence links are present inside the app. The adapted question data is distributed under the same licence; this statement does not apply that licence to the original app code.

## Hosting choice

[123 Reg’s hosting page](https://www.123-reg.co.uk/web-hosting/) describes shared cPanel hosting and MySQL availability; that does not establish this account’s actual capacity. The supplied backend uses PHP 8.1+ and PDO SQLite, so it needs no existing MySQL database, credentials or website tables. Its persistent state belongs outside the public document root. A public wrapper loads the isolated code and data. No changes to the existing website’s index, root rewrite rules, DNS or databases are required.

## Build costs

GitHub documents free standard hosted runners for public repositories in its [runner guidance](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job). Larger runners and artifact storage have separate limits. The workflows use standard `macos-15` runners and bounded artifact retention.

## Before a public App Store launch

This initial TestFlight build needs wider device testing, editorial question review, expansion of small categories, account recovery, name/report moderation, operational backups, and load testing. The server checks question deadlines and calculates all online points; public question data, rooted devices and automated answer tools mean this is not a cheat-proof competitive platform. Offline practice never submits scores to the online leagues. Online bot duels count towards human players’ XP, but bots are not leaderboard accounts.
