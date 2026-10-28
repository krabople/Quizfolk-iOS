# Original QuizUp research and Quizfolk decisions

Reviewed 28 October 2026. This research concerns Plain Vanilla / Glu's 2013–2021 game. New products that reuse its name, Sway, and Trivia Royale are different games. They are not evidence of original QuizUp rules.

## Topic leagues and levels

Original QuizUp placed Rankings inside the topic page, with monthly and lifetime rankings and geographic/friends scopes. Topic XP, rather than just the sum of raw answer scores or a universal player rating, determined progress. Contemporary accounts describe score plus a 40-point completion bonus and a 100-point victory bonus, halved for draws. Topic titles unlocked at ten-level milestones.

Sources checked:

- [Original 2014 hands-on review, GameBlast](https://www.gameblast.com.br/2014/08/quizup-android-ios.html): separate topic/monthly rankings and topic titles.
- [Original app instructions, Fastweb](https://www.fastweb.it/fastweb-plus/digital-magazine/come-si-gioca-a-quizup-l-app-per-trovare-amici/): enter the topic and open Rankings; following, national and global scopes.
- [2014 first-person account, Manila Red Nation](https://karlcrockets10.wordpress.com/category/k-smoove/page/2/): score/completion/victory/draw XP breakdown.
- [2014 first-person review, KMUW](https://www.kmuw.org/your-move/2014-03-13/show-off-your-knowledge-in-quizup): topic XP and title progression.
- [Archived original publisher Google Play listing](https://archive.li/P1maI): monthly topic leaderboards, individual-topic statistics, titles and achievements.

Quizfolk has a **League** section alongside **Play & progress** inside every topic. Month/all-time and everyone/following controls are visible together. Duels earn the documented XP bonuses after their result is determined. Each topic has its own level. Quizfolk currently uses 300 XP per level; this is our explicit beta progression curve, not a claim to have recovered QuizUp's full historical level curve. Geography and GPS collection are omitted; the friends scope is built from follows.

## People and asynchronous challenges

- [Plain Vanilla's May 2015 release](https://www.presseportal.ch/de/pm/100055995/100772979): discovery, shared interests, follows, richer player profiles and an activity stream.
- [Microsoft interview with Plain Vanilla's COO](https://blogs.windows.com/devices/2015/06/26/quizups-plain-vanilla-games-developer-profile/): social connections around common interests.
- [2014 firsthand review, QT Does Games](https://qtdoesgames.blogspot.com/2014/08/app-review-quizup.html): friend challenges could be played while the other person was away and completed later; achievements and topic titles.
- [2017 educational hands-on examination](https://creg.ac-versailles.fr/quizup-un-reseau-social-autour-des-quiz-au-service-de-la-competition): synchronous or asynchronous duels and topic-based XP.
- [2017 Educraft hands-on review](https://educraft.tech/quizup/): public pictures, followed interests, social discovery, achievements, topic levels and separate solo play.

Quizfolk implements name search, public player cards, shared interests, follows/followers, an activity feed, earned titles, achievement cards and blocks. Direct challenges save one immutable seven-question packet. The challenger may finish before acceptance. The recipient gets their own question clocks later. The result, topic XP and head-to-head record settle once both finish. Invitations last 14 days. Matching checks queued humans and recorded human runs before offering a labelled bot after six seconds. Ordinary HTTP requests and SQLite transactions support all of this; there is no live quiz server or presence claim.

## Tournaments: what can and cannot be established

The later original app had rotating topic tournaments, countdowns, daily challenges, coins, tickets, and a Blitz Quiz leaderboard. This is visible in original screenshots, separate from accounts of community-organised elimination brackets:

- [Original Glu iOS listing and screenshots, AppAdvice](https://appadvice.com/app/quizup/718421443): the original app ID is **718421443**; its challenge hub shows topic tournaments and entry currencies.
- [Original Android screenshots, Aptoide](https://quizup.en.aptoide.com/app): tournament topics with countdowns, daily challenges and followed topics.
- [2020 article containing the original Blitz hub screenshot, ID.nl](https://id.nl/huis-en-entertainment/mobiel/smartphone-en-tablet/gezellig-in-tijden-van-corona-deze-spelletjes-speel-je-met-je-vrienden-op-afstand): Blitz podium, rotating topic events, coins and tickets.
- [Original Glu publisher description and release history preserved by Soft112](https://quizup.soft112.com/description.html): daily tournaments; October 2019 release notes explicitly mention more ways to earn tickets.
- [2017 firsthand Educraft review](https://educraft.tech/quizup/): earned or purchased game currency used for some tournaments.
- [May/June 2019 players discussing the ticket change](https://www.reddit.com/r/QuizUp/comments/bqzed2): higher buy-ins needed tickets; lowest buy-in remained exempt; daily challenges and rewarded videos supplied tickets. This is contemporary player testimony, not a complete official rulebook.
- [March 2020 tournament players' accounts](https://www.reddit.com/r/QuizUp/comments/feqp70): tournament coin balances and ticket use; these accounts also complain about suspected bots, so they are not proof of human-only competition.
- [March 2021 player's record](https://www.reddit.com/r/QuizUp/comments/me9e9m): records first places in Battle of the Brains Blitz quizzes.
- [A community organiser's own archive](https://hellession.com/projects.html): a separate manually organised 2020 flag tournament with custom timing rules and an elimination bracket. This must not be confused with the built-in Blitz mode.
- [Original operator shutdown notice](https://glumobile.helpshift.com/hc/en/94-quizup/faq/9680-quizup-has-been-discontinued/): service ended in March 2021. Its old live rules and tournament service are no longer available.

The surviving sources do **not** reliably establish every historical Blitz scoring constant, exact entry price, prize table or rule change. Modern clone articles often invent incompatible rules. We do not present those as established facts. The product owner's clarified requirement is decisive: **accumulate points in the tournament topic until the first wrong answer**. The implemented format follows that requirement.

### Quizfolk survival tournament rules

- Dedicated Tournaments tab replaces the former standalone leagues tab.
- Three rotating daily topics and three weekly topics. Daily events close at 00:00 UTC; weekly events close Monday 00:00 UTC. Every ten days the daily rotation covers all 30 topics. Older paid entries remain under My entries when their topic is no longer featured.
- Topic-only questions without repeats inside a run. Each question gets two seconds of reading before answers and its ten-second answer clock. Correct answers earn 11–20 speed points. There is no seventh-question limit or double-point final question. First mistake or timeout ends the run. Clearing the entire topic bank also completes it.
- Each player's **best individual run score** determines their event place. Repeated entries do not add together. Equal scores share the same competition rank. Players answer at different times; standings contain actual players only.
- Current beta entry tiers: 25, 50 and 75 coins daily; 100 coins weekly. All tournaments require coins. New players receive 100 coins; remaining old tickets convert once at 25 coins each. Coins thereafter are earned through the bounded Daily Trail. These prices and earning rules are Quizfolk choices, not asserted historical QuizUp constants.
- Final places 1/2/3 receive coins and a profile badge. Entry coins form the prize pool, split 50%/30%/20% for at least three players, 60%/40% for two, and 100% for one. Tie groups share the combined shares of the positions they occupy, rounded down. A one-time 25-coin minimum preserves a prize for already-entered legacy free events. No fabricated competitors fill the standings.
- No money purchase, cash value, cash redemption, ad SDK or payment integration. Credits support the entry/reward loop without creating a cost for the player or a live-service requirement for the owner.
- Retrying an entry uses an idempotency key. Wallet movements have unique ledger references. Retransmitted answers cannot score twice. Rewards and refunds settle once under a write transaction, on an ordinary request after the deadline; a background worker is unnecessary.
- Ending early or event closure retains already-earned points. Active runs can resume with their existing clock; resuming is not another charged entry. Tournament scores and trophies remain separate from duel wins, topic XP and head-to-head tallies.

## Scope and validation

The app uses original Quizfolk branding and assets, with an interface inspired by QuizUp's topic-first navigation, colour, player cards and short quizzes. It does not copy old account data, proprietary question banks, art or sounds. The question expansion and individual editorial review are tracked separately in `audit/individual-2026-10`. Candidate questions and partial decisions are not yet published into the playable databases; the publication tool requires a decision for every input and at least 150 accepted questions per topic.

Contract tests cover challenges played at different times, identical packets, atomic result settlement, symmetric head-to-head results, search wait/bot fallback, independent topic progress, reading delay, tournament runs beyond seven questions without reusing a question ID, score accumulation, first-miss/timeout elimination, best-only standings, repeated requests, tied and sole-player prizes, expiry and account deletion. Coin-economy tests cover bounded Daily Trail earnings, repeat-request safety, prize acknowledgement and badge ownership. Native checks cover topic-league navigation, tournament entry and insufficient-balance handling, player cards, pictures, finished-duel closing, prize popups, portrait badges and Daily Trail navigation. Both backend and iOS validation workflows passed for code commit `c3ba442` on 28 October 2026; this was validation, not a TestFlight upload.

## Power-ups: direct gameplay evidence checked 28 October 2026

The claim that the original app's answer-assistance power-ups were restricted to single-player mode is **incorrect for the late original app**. A changelog describing their introduction in single-player mode cannot establish permanent exclusivity.

Provenance was checked by expanding the upload descriptions: 360Gaming TV's recording was published **20 April 2020** and explicitly links the Google Play package **com.quizup.core**, the original QuizUp. Superman's recording was published **1 February 2021**, before the original service closed, and describes saying goodbye to QuizUp. Its introductory player cards and later results show the Qluzo companions named in Glu's contemporary release notes. These are not recordings of the newer unrelated QuizUp app.

- [360Gaming TV, “QuizUp | Android Gameplay 367”, at 4:39](https://www.youtube.com/watch?v=f_kAG0MLLv8&t=279s): viewed directly in the browser. The screen shows Doli Debnath versus Don Ellery, scores 11 and 35, round 3 of 7, and a ten-second question. The bottom **POWER UPS** panel contains **Fifty Fifty**, marked **5 FREE**, and **Right Answer**, marked **3 FREE**. **MY GEMS 100** is visible. These are clearly controls inside a two-player duel. Local evidence image: `work/quizup-multiplayer-powerups-4m39.png` in the parent workspace, not shipped in the app.
- [Superman, “Playing QuizUp: Goodbye to the Greatest Trivia Game in the World”, at 2:52](https://www.youtube.com/watch?v=UA79m2FNgOQ&t=172s): viewed directly. The late original interface shows Superman versus sparrow. Its **Right Answer** button displays a gem icon and **25**; the balance is **541 gems**. Fifty Fifty has remaining free uses. At 3:14 the same recording shows Qluzo companions on the result screen, confirming this is the later original UI. Local evidence image: `work/quizup-right-answer-25-gems-2m52.png` in the parent workspace.
- [Glu release notes for 4.0.1 preserved by APKMirror](https://www.apkmirror.com/apk/glu/quizup/quizup-4-0-1-release/): names Fifty Fifty, Double Choice and Right Answer and describes their introduction in single-player mode. This establishes names and the initial mode described by the release, not their later exclusion from duels.
- [Glu release notes for 4.1.0 preserved by APKMirror](https://www.apkmirror.com/apk/glu/quizup/quizup-4-1-0-release/): introduces Qluzos, collectible mystery boxes, companion power-ups and Pop-Quiz. It does not specify each power's effect, timer interaction or complete price table.
- [Comboldam, “QuizUp #1 (official gameplay)”, at 1:03](https://www.youtube.com/watch?v=qIcvi4721s0&t=63s), published **24 June 2019**: Comboldam versus Nicolas Khodjaev, Name the Flag, fourth question. The panel shows **Fifty Fifty**, a gem icon and **1**, plus **Double Choice**, marked **4 FREE**; the balance is **450 gems**. This also establishes Double Choice's presence in a two-player duel in this earlier build. The upload title's word “official” is the uploader's wording, not evidence that the channel belongs to Glu. Local evidence image: `work/quizup-double-choice-duel-1m03.png` in the parent workspace.

The videos establish multiplayer availability, free-use counters, one observed **25-gem Right Answer price**, and a **1-gem Fifty Fifty price** in the 2019 recording. They do not establish that all versions charged the same amount, that gems were interchangeable with tournament coins, or how every power affected the countdown. No observed activation yet establishes whether a power paused time, submitted an answer automatically, or merely highlighted it. Double Choice's paid price remains unverified. Any Quizfolk choice on these remaining details must be described as an explicit product rule rather than an exact historical replica.

Research also checked other original gameplay recordings, contemporary publisher changelogs, the surviving operator Help Center, and later recollections. Modern apps sharing the QuizUp name and unsourced retrospective claims were excluded as evidence of the original mechanics.
