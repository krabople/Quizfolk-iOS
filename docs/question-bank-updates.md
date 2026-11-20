Questions for online duels and tournaments are selected by the hosted service.
After the bank-update-capable app release, offline practice and the topic list also
refresh automatically from public data assets, without further app releases.

After editorial review, run `python scripts/export_mobile_bank.py`. It validates
the canonical bank and exports a single data-only JSON snapshot plus a tiny manifest
to `build/mobile-bank`. Deploy the immutable `bank-<SHA256>.json` file and `.htaccess`
to `public_html/quizfolk-api/bank/` first, then replace `manifest.json` last. Deploy
the matching three canonical files to private `quizfolk-service/data` for online play.
Keep the preceding immutable snapshot during rollout and retain private backups.

The apps check the manifest on launch and on foregrounding, at most once per
15 minutes within a running session. An unchanged hash avoids another bank download.
The app checks SHA-256, byte count, format, category counts, question ownership,
answer validity and uniqueness before replacing its cached snapshot atomically.
Network failures and invalid updates leave the last valid bank available offline;
the bundled bank is the fallback on a fresh installation. Player keys, history,
coins and topic XP are separate and are never replaced by a bank update.

The export contains questions and category metadata, not code, credentials or player
records. Requests for the public bank assets do not contain a player token. HTTP
compression is enabled only within the bank asset directory when supported by Apache.
Do not modify the Ways2Earn site's root configuration or files during publication.

Picture questions require the image-capable native release (protocol4) once. Thereafter picture questions can also change without another app update. Export BOTH compatibility feeds: python scripts/export_mobile_bank.py --format 1 writes build/mobile-bank (text-only, deployed to bank/); python scripts/export_mobile_bank.py --format 2 --output build/mobile-bank-v2 writes the full image bank (deployed to bank-v2/). Publish immutable snapshots before either manifest. The private canonical bank always contains all questions. Older clients keep the text feed and do not receive unrenderable image questions. New clients verify the inline PNG hashes and dimensions and keep images available offline.
