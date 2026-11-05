# Optional push notifications

The clients and shared backend implement four independent categories: new direct
challenges, completed human duel results, final tournament prizes, and friends
tournament starts/finishes. The master switch defaults off. Preferences are saved
server-side; OS notification permission is requested only after the player opts in
and delivery is configured. No marketing, coin reminders, Analytics SDK or live
quiz connection is added.

## Activation status

Client and server code can be tested without provider credentials. The settings
screen explicitly reports that delivery is unavailable until configured. Building
the app or switching its preference on does not by itself activate push delivery.
An actual device delivery test is required after the following setup.
The shared-host backend and one-minute cron job have been deployed. On 5 November
2026 the production APNs credential was installed outside the web root, with
owner-only file permissions and a topic restriction to `com.quizfolk.ios`.
The hosting check reached APNs over HTTP/2 and received HTTP 400 `BadDeviceToken`
for a deliberately invalid token; this is a connectivity check, not a physical
device delivery test. TestFlight 0.3.3 (21) already contains the production push
entitlement and can use this server configuration without another iOS build.

The dedicated Firebase project `quizfolk-1aa86` and Android registration
`com.quizfolk.android` exist on the Spark no-cost plan, with Analytics and Gemini
disabled. Cloud Messaging API v1 is enabled. The owner approved both Firebase and
Google Cloud terms. A dedicated `quizfolk-push-sender` service account has only
the Firebase Cloud Messaging API Admin role on this project. Its private key is
installed outside the web root with mode 0600. The server received HTTP 200 from
Google's OAuth endpoint and HTTP 400 `INVALID_ARGUMENT` for an intentionally
invalid FCM registration token in a `validate_only` request. No real player
notification was sent by these checks.

All four public Firebase client identifiers are configured as GitHub repository
variables for Android builds. A disposable Firebase installation was created and
removed successfully (HTTP 200 for both requests), verifying that this app ID,
project and API key are accepted together. The Android 0.3.3 (10) preview predates that client
configuration; use a configured build numbered 11 or later. iOS 0.3.3 (21) can use
the live APNs configuration. Physical-device delivery still needs verification
after opting in in **You → Notifications**.

The uploaded FCM public certificate expires on 5 November 2027. Rotate its private
sender key before then; keep replacements outside the web root and never revoke
keys used by other apps. The local private backup is in an owner-only directory
outside this public repository.

1. Create a dedicated Firebase project named Quizfolk in the owner's Google
   account, with Analytics and Gemini assistance off. Firebase requires the owner
   to accept its terms for this project. Register `com.quizfolk.android`.
2. Add the Firebase Android public client configuration as repository variables
   `FCM_APP_ID`, `FCM_API_KEY`, `FCM_PROJECT_ID`, and `FCM_SENDER_ID`, or the same
   keys in ignored `android/firebase.properties` for a local build. These are
   Firebase client identifiers, not server credentials. Restrict the API key to
   the applicable Firebase APIs and Android application/certificate as appropriate.
3. Create a dedicated Google service account with only the Firebase Cloud
   Messaging API Admin role for the Quizfolk project. Store its JSON private key
   outside the web root, e.g. in `backend/private/push/firebase-service-account.json`.
   Do not commit it or ship it with a client app. Creating persistent credentials
   requires confirmation in the browser workflow.
4. In the owner's Apple Developer account, create an APNs key restricted to
   `com.quizfolk.ios` where available. Store the `.p8` outside the web root with
   mode 0600. Record its key ID and Apple team ID. An App Store Connect API key is
   not an APNs key. Signing into App Store Connect does not necessarily sign into
   the Apple Developer portal.
5. Put the following in ignored, private `backend/push-config.php`; existing
   `backend/config.php` and player state must be preserved:

   ```php
   <?php
   return [
       'apns_key_file'=>'/absolute/private/path/AuthKey.p8',
       'apns_key_id'=>'APPLE_APNS_KEY_ID',
       'apple_team_id'=>'APPLE_TEAM_ID',
       'fcm_service_account_file'=>'/absolute/private/path/firebase-service-account.json',
   ];
   ```

6. Install a cPanel cron job every minute using PHP 8.1+ with PDO SQLite, OpenSSL
   and curl (including HTTP/2 for APNs):

   ```text
   * * * * * /usr/local/bin/php /home/nxecei8fyf2u/quizfolk-service/backend/push_worker.php >/dev/null 2>>/home/nxecei8fyf2u/quizfolk-service/backend/private/push-worker-errors.log
   ```

7. Build Android with its Firebase client identifiers. The iOS project includes
   `aps-environment`; `scripts/apple_bundle.py` enables Push Notifications and
   chooses/creates a dedicated App Store profile containing the production push
   entitlement, using the existing distribution certificate. It does not create
   or revoke distribution certificates or reuse an API key for APNs delivery.
8. Install the new builds, opt in on two physical devices, and verify challenge,
   delayed result and closed-tournament notifications while the receiving app is
   backgrounded. Test taps and turning off each category. Simulators and mocked
   provider tests cannot prove actual APNs/FCM delivery.

## Delivery and privacy

Events and game changes are written in the same transaction. The scheduled worker
settles closed tournaments even when nobody has the app open. Jobs deduplicate
per event/device, re-check preferences/blocks before sending, cancel stale or
accepted challenge alerts, retry transient failures with bounded backoff and
disable invalid tokens. Network requests hold no SQLite write lock. The worker
uses a single-process lock; crashed job leases expire. Delivery is best effort;
provider acceptance does not prove a device displayed the notification.

Messages contain event identifiers and brief alerts, never answers or account
keys. Taps load the named event through authenticated API routes. Android uses
data messages, an unexported messaging service, immutable pending intents and
separate OS channels. Tokens and choices are removed on account deletion, and
delivery records expire after seven days. Credentials/tokens are not logged.

## Verification

`scripts/run_contracts.py test_notifications.py` runs against disposable local
state only. It covers authentication, opt-in, individual categories, retries,
blocks, final prize timing, idempotence, invalid tokens and deletion. The provider
helper always uses a mock sender. `scripts/test_push_crypto.php` verifies ES256
and RS256 JWT signatures and APNs/FCM request shapes without contacting either
provider. Native tests cover preference persistence, unavailable delivery messaging
and safe event destinations.
