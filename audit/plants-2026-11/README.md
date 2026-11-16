# Plants & flowers: initial category

Published 150 original questions for category `39`, named **Plants & flowers**.
The shared bank now contains 21,817 questions across 31 named categories; the
apps add Mixed topics separately.

The questions cover familiar flowers, cultivation, bulbs, remarkable plants,
anatomy, physiology, seeds, reproduction, ferns, mosses and conifers. Difficulty
was judged individually: 58 easy, 87 medium and 5 hard. Specialist terminology
has not been labelled easy to inflate that count.

Every prompt and all four choices were read individually by the author and by
an independent reviewer. The 90 gardening questions received 74 keep decisions
and 16 revisions for source precision, clearer wording or more credible wrong
answers. All 60 botany questions passed the independent check. Correct answer
positions are balanced and the game shuffles answers again when played.

- `garden-draft.json`, `botany-draft.json`: original authored candidates and
  concise fact rationales.
- `garden-independent-review.json`, `botany-independent-review.json`: individual
  second-pass judgments, including applied revisions.
- `questions.json`: the final frozen supplement.
- `decisions.jsonl`: a fingerprint and separate meaning, answer, grammar and
  category judgment for every published question.
- `completion.json`: coverage and SHA-256 evidence plus the primary source URLs.
- `publish.py`: assembles the reviewed wording into JSON and SQLite; it does not
  make editorial decisions. Run only for this initial batch, before subsequent
  supplements change the base bank.

Primary references include the RHS, Kew, university extension services,
botanic gardens and the Natural History Museum. They support the factual checks;
the quiz wording and alternatives were written for Quizfolk. Source references
remain in this audit and existing attribution metadata, not added to app screens.

The October audit is preserved unchanged. `audit/supplements.json` lists later
completed batches; `audit/validate_supplements.py` checks each independently.
`scripts/validate_bank.py` verifies the original audited bank plus all listed
supplements, per-topic minimums, answer shape, unique IDs/prompts and equality
between the mobile JSON and server SQLite payloads.

Validation: `python scripts/validate_bank.py` passes with 21,817 questions across
31 categories. Only the question-bank SQLite is rebuilt; no player database is
read or modified by these publication tools.
