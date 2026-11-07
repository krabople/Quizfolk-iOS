# Hosted Android download

Public URL: https://www.ways2earn.com/quizfolk-download/

`package.py` checks the signed release APK against its verification report, copies
the existing Quizfolk logo and licensed font, and produces a deployment ZIP. Its
public targets are files inside `public_html/quizfolk-download/`. The anonymous
counter helper goes in `quizfolk-service/download-tracking/`, outside the web
root. Packages never contain access keys, counters, player data or site-root
configuration.

The APK and verification report are expected in the repository's parent `outputs`
directory. Build artifacts are distributed as release assets rather than added
to the source tree. For an update, use the new signed APK, update the version,
date, filename and size on the page, and update the packaging inputs together.
Build 15 is the current hosted release. Old build-11 through build-14 links route
to the latest tracked download. Packages use current file timestamps so PHP's
opcode cache notices code updates; preserve private configuration and counters.

## Click statistics

The download button uses `download.php`. The folder's rewrite rule also tracks
requests to the previous direct APK URL. A non-cacheable redirect records the
request and lets Apache serve the unchanged APK at `?file=1`, including range and
resume support. HEAD, known prefetch and resumed-range requests do not increment
the counter. A counter error leaves the download working. These are request
counts, not unique visitors, completed transfers or app installations. Automated
GET requests can still count. Counts begin when tracking is deployed; older
clicks cannot be inferred from this new counter.

An isolated SQLite database retains daily totals and the most recent 1,000
request timestamps/versions. It stores no IP address, referrer, visitor ID or
user-agent string, and has no link to player accounts. Day boundaries and display
times use Europe/London. The dashboard shows totals, today, seven days, up to 30
days of daily counts, and the latest 100 request times. Verification requests
authenticated by the private header are counted separately.

The owner opens `stats.php#key=…` using their private access link. This link is
never included in this repository or the public page. The browser sends its key
over HTTPS in a POST body, then removes the fragment. Only its SHA-256 hash is
stored in private `download-tracking/private/config.php`. A separate HttpOnly,
Secure, SameSite=Strict session cookie grants read-only access for 30 minutes;
sign-out or rotating the configured key hash invalidates access. Keep the access
link private and retain a copy outside the repository. The session directory is
mode 0700; the configuration and database are mode 0600.

Initial private configuration:

```php
<?php
return ['stats_key_hash'=>'SHA256_OF_RANDOM_256_BIT_ACCESS_KEY',
        'origin'=>'https://www.ways2earn.com','cookie_secure'=>true];
```

Do not replace the private configuration or SQLite database during normal page
updates. `test_metrics.py` runs redirect, authentication, concurrency, history
retention and outage checks in disposable local state; it never contacts hosting.
