<?php
// Copy to config.php OUTSIDE public/. Use an absolute path outside every web root.
return ['state_dir' => dirname(__DIR__).'/backend/private',
    // Keep credentials outside every web root and out of Git. See docs/push-notifications.md.
    'push'=>[
        'apns_key_file'=>'', 'apns_key_id'=>'', 'apple_team_id'=>'',
        'fcm_service_account_file'=>'',
    ],
];
