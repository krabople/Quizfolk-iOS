<?php
// Copy to rewarded-config.php beside config.php, OUTSIDE every public web root.
// Configure enabled AdMob units with amount 5, item "coins", and the dedicated
// HTTPS /quizfolk-api/rewarded-callback.php URL (no existing query parameters).
return [
    'enabled'=>false,
    // Temporary real-coin rewards from Google test videos, iOS allowlist only.
    // Keep live serving off while testing. Empty IDs disable test credits.
    'ios_test_enabled'=>false,
    'ios_test_player_ids'=>[],
    'units'=>['ios'=>'','android'=>''],
    // Rewards have no daily cap. Users may continue when the previous ad settles.
    'cooldown_seconds'=>0,
    'attempt_seconds'=>600,
    'callback_grace_seconds'=>259200,
];
