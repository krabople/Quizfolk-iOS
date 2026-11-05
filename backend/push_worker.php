<?php
declare(strict_types=1);
if(PHP_SAPI!=='cli'){http_response_code(404);exit;}
define('QUIZFOLK_PUSH_WORKER',true);
require __DIR__.'/public/index.php';
$lock=fopen($state.'/push-worker.lock','c');
if(!$lock || !flock($lock,LOCK_EX|LOCK_NB))exit;
try {
    $db->exec('BEGIN IMMEDIATE');tournament_seed($db);tournament_settle($db);$db->exec('COMMIT');
    echo json_encode(push_drain($db,$config),JSON_THROW_ON_ERROR).PHP_EOL;
} catch(Throwable $e) {
    if($db->inTransaction())$db->rollBack();
    // Credentials, payloads and device tokens never appear in cron logs.
    fwrite(STDERR,"Quizfolk notification worker failed; inspect provider configuration and PHP extensions.\n");exit(1);
} finally {flock($lock,LOCK_UN);fclose($lock);}
