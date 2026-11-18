Question reading time is separate from the ten-second answer clock. The server
controls online duels and tournament runs; both native apps use the same rule
for offline practice and as a fallback if an older response omits the duration.

Normalize whitespace, then count words and Unicode scalar values, not UTF-8
bytes. The allowance in seconds is:

`3 + ceil(max(0, (words - 12) / 3, (characters - 72) / 18))`

Short questions retain at least three seconds. Thirty ordinary short words
receive nine seconds; sixty receive nineteen. The character allowance also
protects prompts with long names, long tokens or languages without spaces.
There is no upper limit that would cut off exceptionally long valid questions.

Answers and power-ups stay unavailable during reading. The server refuses
early reveal requests; answer timing and speed scoring start only when answers
are actually revealed. The existing smooth question transition is unchanged.
