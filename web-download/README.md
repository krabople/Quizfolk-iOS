# Hosted Android download

Public URL: https://www.ways2earn.com/quizfolk-download/

`package.py` checks the signed release APK against its verification report, copies
the existing Quizfolk logo and licensed font, and produces a deployment ZIP. Its
only targets are files inside `public_html/quizfolk-download/`. It contains no
backend, credentials, player data or site-root configuration.

The APK and verification report are expected in the repository's parent `outputs`
directory. Build artifacts are distributed as release assets rather than added
to the source tree. For an update, use the new signed APK, update the version,
date, filename and size on the page, and update the packaging inputs together.
