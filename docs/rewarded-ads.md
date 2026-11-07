# Optional rewarded ads

Rewarded ads are optional, initiated only from **Earn coins**, and award exactly 5 coins after the PHP server verifies AdMob's signed completion callback. Both platforms use the same account wallet. There is no daily cap and no client API that grants a reward.

## Client contract

Use the existing authenticated `index.php?r=...` API. All times below are Unix **seconds**, except AdMob's callback `timestamp` (milliseconds). The platform is `ios` or `android`.

* `GET rewarded-status&platform=ios[&attempt=<id>]`: eligibility and current/passed attempt; an attempt belonging to another account is rejected. Without `attempt`, returns the pending attempt for this account, including one created on the other platform, or its most recent completed/cancelled/expired attempt if none is pending.
* `POST rewarded-start`, body `{"platform":"ios","requestKey":"<random UUID>"}`: reserve an attempt before loading/presenting an ad. Persist the request key until a definite response; retries reuse it and never allocate another attempt. This returns the common response with `attempt`. When unavailable, returns HTTP409 with `error` plus the common response. No amount or ad unit is accepted from the client.
* `POST rewarded-cancel`, body `{"platform":"ios","attempt":"<id>"}`: release a failed-load, presentation-failure or closed-without-reward attempt. It cannot undo an awarded reward. **Do not cancel after the SDK reward callback:** keep polling instead, including after dismissal/relaunch.

Every successful response has this shape (nullable fields always present):

```json
{
  "enabled": true,
  "available": false,
  "reason": "pending",
  "reward": 5,
  "dailyLimit": null,
  "earnedToday": 0,
  "remainingToday": null,
  "resets": 1794096000,
  "nextAvailableAt": null,
  "wallet": {"coins": 150},
  "attempt": {
    "id": "64 lowercase hex characters",
    "platform": "ios",
    "status": "pending",
    "adUnitId": "ca-app-pub-…/…",
    "customData": "same opaque 64-character attempt ID",
    "created": 1794009600,
    "expires": 1794010200,
    "awardedCoins": 0
  }
}
```

`reason`: `ready`, `disabled`, `pending`, or `cooldown`. `dailyLimit` and `remainingToday` are always null: there is **no daily cap**. `earnedToday` counts completed rewards, not coins. `attempt.status`: `pending`, `awarded`, `cancelled`, or `expired`. An awarded attempt reports `awardedCoins:5`; other states report0. `nextAvailableAt` is the server UTC time for an optional private-config cooldown, otherwise null. The default cooldown is0: users can watch another ad once the previous one settles. The default attempt window is10 minutes. Eligibility is independent of advertising consent: clients must obtain UMP eligibility before requesting/displaying an ad.

Set the returned opaque `customData` as AdMob SSV custom data **before showing** the ad. Do not set AdMob `user_id`; never send the Quizfolk bearer token, name, email or internal player ID to AdMob. Load only the returned platform-specific `adUnitId`, and validate that it is appropriate for the installed app configuration. Never substitute a production unit into debug tests. An attempt restored from another platform must only be polled, not presented with the wrong SDK.

After the native SDK reports a reward, show “Checking your reward…” and poll `rewarded-status` with the attempt ID (e.g.2 seconds initially, then back off). Credit/update the UI only from `wallet.coins` and confirmed `attempt.status=awarded`. Persist pending IDs across relaunch. A closed ad without SDK reward may be cancelled only after callback ordering has settled. No-fill and consent refusal grant no coins and must leave the quiz usable. A pending callback can complete on a subsequent launch even if the visible polling period ends.

## Backend verification and deployment

Configuration is private: `backend/rewarded-config.php` beside `config.php`, outside `public/`, returns an array like `backend/rewarded-config.example.php`. Disabled unless explicitly enabled with real iOS/Android ad-unit IDs. Configure both AdMob units with reward amount5 and item `coins`, and the dedicated HTTPS callback URL `/quizfolk-api/rewarded-callback.php` with no pre-existing query string.

The callback accepts GET only. It verifies the original query bytes preceding `&signature=`, using Google's P-256 public key and ECDSA/SHA256 DER signature. It strictly validates parameter structure, key ID, unit, reward item/amount, timestamp, one-use opaque intent and original player. Keys are downloaded only from Google's fixed HTTPS verifier-key URL, cached privately for less than24 hours, refreshed on unknown key IDs, and never supplied by a request. No callback query/token is logged by application code.

SQLite `BEGIN IMMEDIATE`, globally unique provider transaction IDs, and one-use attempts protect concurrent callbacks and retries. The existing wallet ledger applies the5 coins once. Provider HTTP200 is returned for successful/repeated deliveries. Only one pending intent per account is permitted across devices. The reporting UTC day belongs to the original reservation. Completion must occur within the signed attempt time window; delivery may arrive later within the configured callback grace period (72 hours by default). Pending expiry permits a new ad, while a valid delayed callback for the old attempt remains eligible.

Cancellation releases eligibility but is not proof that an ad did not complete. A signed completion before cancellation can still be processed; a completion after cancellation is rejected. Clients must therefore never cancel a completed ad merely because server verification is slow. Account deletion cascades attempts; tombstoned provider transaction hashes contain no player information and cannot credit a new account.

The callback accepts either the configured full `ca-app-pub-…/…` unit or its exact numeric suffix, as Google documents the callback's numeric `ad_unit` representation. The attempt stores the configured unit and original account; neither is chosen by callback input. There is5 seconds of server clock tolerance at reservation start and120 seconds for a future signed provider clock, but completion cannot occur at/after the expiry. Cancellation uses the server second in which it was received.

Production activation requires configured units, working HTTPS callback, server OpenSSL/cURL, consent messages, current privacy disclosures, and provider test-mode end-to-end validation. This source change alone does not deploy or enable advertisements.

## References

* [Google's rewarded SSV guide](https://developers.google.com/admob/android/ssv): raw signed query content, ECDSA/SHA256 DER, callback fields, key rotation and delayed delivery.
* [Google's iOS SSV guide](https://developers.google.com/admob/ios/ssv): custom reward data and native callback setup.
* [Google/Tink verifier implementation](https://github.com/tink-crypto/tink-java-apps/blob/main/rewardedads/src/main/java/com/google/crypto/tink/apps/rewardedads/RewardedAdsVerifier.java): signature/key suffix extraction and SHA256/DER verification.
