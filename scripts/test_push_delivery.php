<?php
// A disposable-local-state contract helper. It can never call a real push provider.
if(PHP_SAPI!=='cli' || !str_contains((string)getenv('QUIZFOLK_STATE_DIR'),'contract-state'))exit(2);
define('QUIZFOLK_PUSH_WORKER',true);require dirname(__DIR__).'/backend/public/index.php';
$mode=getenv('PUSH_TEST_MODE') ?: 'success';
$result=push_drain($db,[],100,function($job,$config)use($mode){
    if($mode==='retry')return ['status'=>429,'reason'=>'TooManyRequests','retryAfter'=>120];
    if($mode==='invalid')return ['status'=>410,'reason'=>'Unregistered','invalid'=>true];
    if($mode==='throw')throw new RuntimeException('A deliberately private transport failure');
    return ['status'=>200];
});echo json_encode($result,JSON_THROW_ON_ERROR);
