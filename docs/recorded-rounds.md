Every new round belongs to one opponent. Random matchmaking pairs two waiting
players into a shared asynchronous duel; after six seconds with nobody available,
it assigns a fresh bot game. That assignment is never recycled or changed into
another player's opponent. Direct challenges also have one shared duel/result.

Completed human performances are no longer a matchmaking pool, including those
originally played against a bot. The insertion guard rejects a replay source ID
or the retired `human` match kind. Incomplete legacy replays cannot continue;
already completed history, earned XP and profiles are preserved.

Historical `human` records are labelled as saved-round comparisons. They used
the original person's own answers, not the original bot's answers, but were
one-sided comparisons rather than a shared head-to-head game. Their historical
display does not enable new replays.

New human duels use two participant records with one shared duel ID and the
same questions/answer order. Both result records settle together when both runs
finish. The waiting opponent receives the result notification according to their
preferences. Bots have a separate name list and no real-player opponent ID.
