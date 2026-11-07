<?php
declare(strict_types=1);
// This URL has no bearer token and accepts only Google's signed query. Existing
// quiz API authentication remains unchanged.
if(($_SERVER['REQUEST_METHOD'] ?? '')!=='GET'){http_response_code(405);header('Allow: GET');exit;}
define('QUIZFOLK_REWARDED_CALLBACK',true);
require __DIR__.'/index.php';
try {
    $parsed=rewarded_parse_callback((string)($_SERVER['QUERY_STRING'] ?? ''));
    $key=rewarded_public_key($parsed['keyId'],$state,time());
    $params=rewarded_verify_callback($parsed,$key);
    rewarded_schema($db);out(rewarded_complete($db,$params,time()));
} catch(RewardedError $e) {out(['error'=>$e->getMessage()],$e->status);}
catch(Throwable) {error_log('Quizfolk rewarded verification temporarily unavailable.');out(['error'=>'Reward verification temporarily unavailable.'],503);}
