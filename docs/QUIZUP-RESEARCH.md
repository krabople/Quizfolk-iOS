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
- Six rotating daily topics and three weekly topics. Daily events close at 00:00 UTC; weekly events close Monday 00:00 UTC. Every five days the daily rotation covers all 30 topics.
- Topic-only questions without repeats inside a run. Each question gets two seconds of reading before answers and its ten-second answer clock. Correct answers earn 11–20 speed points. There is no seventh-question limit or double-point final question. First mistake or timeout ends the run. Clearing the entire topic bank also completes it.
- Each player's **best individual run score** determines their event place. Repeated entries do not add together. Equal scores share the same competition rank. Players answer at different times; standings contain actual players only.
- Current beta entry tiers: free, 25 coins, or one ticket daily; two tickets weekly. Welcome supply: 100 coins and three tickets. Free daily supply: 50 coins and two tickets, once per UTC day. These prices and supply values are Quizfolk choices; they are not asserted to be exact QuizUp values.
- Final places 1/2/3 award 500/250/100 free game coins and public trophy badges. Ties share the corresponding prize. At least two entrants and a positive score are required for prizes. If only one person enters, their entry currency is refunded. No fabricated competitors fill the standings.
- No money purchase, cash value, cash redemption, ad SDK or payment integration. Credits support the entry/reward loop without creating a cost for the player or a live-service requirement for the owner.
- Retrying an entry uses an idempotency key. Wallet movements have unique ledger references. Retransmitted answers cannot score twice. Rewards and refunds settle once under a write transaction, on an ordinary request after the deadline; a background worker is unnecessary.
- Ending early or event closure retains already-earned points. Active runs can resume with their existing clock; resuming is not another charged entry. Tournament scores and trophies remain separate from duel wins, topic XP and head-to-head tallies.

## Scope and validation

The app uses original Quizfolk branding and assets, with an interface inspired by QuizUp's topic-first navigation, colour, player cards and short quizzes. It does not copy old account data, proprietary question banks, art or sounds. Existing licensed question content is unchanged in this update.

Contract tests cover challenges played at different times, identical packets, atomic result settlement, symmetric head-to-head results, search wait/bot fallback, independent topic progress, reading delay, tournament runs beyond seven questions, score accumulation, first-miss/timeout elimination, best-only standings, repeated requests, tied prizes, sparse-field refunds, expiry and account deletion. Native UI checks cover topic-league navigation, tournament discovery/rules, player cards/challenge composition, pictures and finished-duel closing.
