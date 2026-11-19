# Achievements

Public player cards expose 65 progression milestones plus at most one best
public tournament placing per topic. These are achievements, rather than a
chronological list of tournament results. A first place replaces a second or
third place for the same topic. Daily and weekly events share this best placing;
the most recent event represents equal-best placings. There is no recent20-event
cutoff. Private friends tournament results are excluded from this public list.

All tournament places, prizes, receipts and wearable badges remain in their
original tables. The separate Tournament badges collection and selected profile
badge are unchanged. No database migration or destructive backfill is required.

Milestones include completed duels up to10,000; wins up to2,500; perfect duels
up to1,000; correct answers up to100,000; exploration across31 topics; a single
online topic level up to100; public podium finishes and tournament wins up to100;
single-run public streaks up to100; and single-run scores up to2,500. Existing
starter IDs (first,winner,perfect,ten,explorer) remain stable. Existing history
counts retroactively. No overall player level is introduced.

Every achievement includes description, progress, target, progressLabel and
group alongside the existing badge fields. Progress can exceed its target;
displayed fractions are clamped. Seven of seven explicitly requires all seven
questions correct in one completed online duel. Bot duels count; device-only
offline practice does not. Human challenges count only once settled. Tournament
answers are tracked through the separate tournament streak/score goals, rather
than the completed-duel correct-answer goal. Power-up-assisted answers count.

iOS and Android show grouped lists with All/Unlocked/Locked filters. Every row
exposes its requirement, progress and a details action for both earned and locked
achievements. The details sheet/dialog repeats the full condition and scope.
Both apps decode old-server responses and provide explanations for the five
legacy starter badges when description fields are absent.

Validation: scripts/test_achievements.php covers exact long-term thresholds,
old first places beyond20 recent results, stable best-per-topic IDs, public/private
scope, single-run rather than summed-attempt targets, completed versus pending
duels and preserved prize rows. The economy HTTP contract verifies one best
topic achievement while all three underlying prizes remain available. Native
unit and UI tests cover locked/unlocked meaning, progress, filters and details.
