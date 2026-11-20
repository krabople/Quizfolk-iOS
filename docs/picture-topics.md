The November2026 expansion adds Biology150, Flags of the World197, Brand Logos215,
and World Capitals394 questions. Each of the197 covered countries has one flag
question and two capital questions, one in each direction. The country set is
the193 UN member states, Palestine, Vatican City, Kosovo and Taiwan. Constituent
countries and dependent territories are outside that explicitly defined set.

The author reviewed every new stem, answer and distractor and every displayed
image. This is an author review, not an independent expert audit. Biology has
50 easy,70 medium and30 hard entries. Country/capital reference data came from
UNESCO with explicitly qualified corrections for multiple capitals, governmental
seats, claimed capitals and the2026 Equatorial Guinea change. Indonesia's question
is explicitly dated2020 to avoid ambiguity during the Nusantara transition.
Afghanistan's tricolour flag question explicitly describes its pre2021 use.

PNG pixels are embedded in each data-only question. They do not load from a third
party during play. The same image appears during reading time, timed answers and
saved match review. Safe generic accessibility text does not disclose the answer.
Images are SHA256-verified, capped at64KiB and512x512 pixels. Flag aspect ratios
are preserved; brand vector geometry is rasterised without generative drawing.

Protocol4 adds image payloads to online duels and tournaments. Legacy protocols
receive text-only topic discovery and text-only newly created mixed packets.
Attempting a shared picture duel or picture tournament from a legacy app returns
an update-required error before starting the question clock or charging an entry.
Forward/reverse capital questions share a content group so the same country is
not repeated in one modern match or tournament deck. Distinct image questions can
share a stem without collapsing into one question. Image corrections invalidate
old saved packets and stale power reservations.

Export both public banks: scripts/export_mobile_bank.py produces format1 in
build/mobile-bank with25920 text questions/33 topics. Run it with --format2
(as two arguments: --format 2) --output build/mobile-bank-v2 for format2 with
26332 questions/35 topics. Updated apps read bank-v2 and use a separate cache.
Older apps continue to read bank and cannot silently receive blank picture rounds.
Deploy immutable snapshots before their manifests. Player state remains separate.

All additions have auditVersion2026-11-four-topics-v1 and a frozen ID/fingerprint
ledger in audit/four-topics-2026-11, so this batch can be removed independently.
Image rights and attributions are distributed in data/question-image-notices.txt.

During the TestFlight rollout, public daily/weekly rotations stay on text topics so current App Store clients retain three playable events. Private friends tournaments and direct picture duels work with protocol4. Once the picture-capable native release is public, private server configuration public_image_tournaments=true enables those subjects in the normal public rotation. Existing daily/weekly selections are preserved mid-period.
