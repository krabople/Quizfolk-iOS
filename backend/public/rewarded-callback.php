<?php
declare(strict_types=1);
// This URL has no bearer token and accepts only Google's signed query. Existing
// quiz API authentication remains unchanged.
if(($_SERVER['REQUEST_METHOD'] ?? '')!=='GET'){http_response_code(405);header('Allow: GET');exit;}
define('QUIZFOLK_REWARDED_CALLBACK',true);
require __DIR__.'/index.php';
$query=(string)($_SERVER['QUERY_STRING'] ?? '');$stage='parse';$signatureValid=null;
try {
    $parsed=rewarded_parse_callback($query);$stage='key';
    $key=rewarded_public_key($parsed['keyId'],$state,time());
    $stage='signature';$signatureValid=false;$params=rewarded_verify_callback($parsed,$key);$signatureValid=true;$stage='setup';
    rewarded_schema($db);$reply=rewarded_setup_probe($db,$params,$parsed['signed'],$config,time());
    if($reply===null){$stage='reward';$reply=rewarded_complete($db,$params,time());}
    rewarded_diagnostic($query,$state,$config,$stage==='setup'?'accepted_setup':'accepted',$signatureValid);out($reply);
} catch(RewardedError $e) {rewarded_diagnostic($query,$state,$config,$stage,$signatureValid,$e->getMessage());out(['error'=>$e->getMessage()],$e->status);}
catch(Throwable) {rewarded_diagnostic($query,$state,$config,$stage,$signatureValid,'Service unavailable');error_log('Quizfolk rewarded verification temporarily unavailable.');out(['error'=>'Reward verification temporarily unavailable.'],503);}
