<?php
declare(strict_types=1);
require dirname(__DIR__).'/backend/notifications.php';
function check(bool $condition):void {if(!$condition)throw new RuntimeException('Push provider contract failed');}
function decode64(string $text):string {return base64_decode(strtr($text,'-_','+/'));}
$ec=openssl_pkey_new(['private_key_type'=>OPENSSL_KEYTYPE_EC,'curve_name'=>'prime256v1']);openssl_pkey_export($ec,$ecPem);
$rsa=openssl_pkey_new(['private_key_type'=>OPENSSL_KEYTYPE_RSA,'private_key_bits'=>2048]);openssl_pkey_export($rsa,$rsaPem);
foreach([['ES256',$ec,$ecPem],['RS256',$rsa,$rsaPem]] as [$alg,$key,$pem]) {
    $jwt=push_jwt(['iss'=>'test','iat'=>time()],$pem,$alg,'TESTKEY');[$h,$c,$signature]=explode('.',$jwt);$raw=decode64($signature);
    check(json_decode(decode64($h),true)['alg']===$alg);
    if($alg==='ES256') {
        check(strlen($raw)===64);$parts=[];
        foreach([substr($raw,0,32),substr($raw,32)] as $part){$part=ltrim($part,"\0");if(ord($part[0])&0x80)$part="\0".$part;$parts[]="\x02".chr(strlen($part)).$part;}
        $raw="\x30".chr(strlen($parts[0].$parts[1])).$parts[0].$parts[1];
    }
    check(openssl_verify($h.'.'.$c,$raw,openssl_pkey_get_details($key)['key'],OPENSSL_ALGO_SHA256)===1);
}
$dir=sys_get_temp_dir().'/quizfolk-push-'.bin2hex(random_bytes(6));mkdir($dir,0700);
try {
    file_put_contents($dir.'/apns.p8',$ecPem);chmod($dir.'/apns.p8',0600);
    file_put_contents($dir.'/firebase.json',json_encode(['project_id'=>'quizfolk-test','client_email'=>'push@quizfolk-test.iam.gserviceaccount.com','private_key'=>$rsaPem]));chmod($dir.'/firebase.json',0600);
    $config=['push'=>['apns_key_file'=>$dir.'/apns.p8','apns_key_id'=>'TESTKEY','apple_team_id'=>'TESTTEAM','fcm_service_account_file'=>$dir.'/firebase.json']];
    $job=['id'=>str_repeat('a',64),'platform'=>'ios','environment'=>'production','token'=>str_repeat('b',64),'expires'=>time()+3600,'title'=>'New challenge','body'=>'A player challenged you.','kind'=>'challenges','payload'=>json_encode(['kind'=>'challenges','id'=>'test-duel'])];
    $calls=[];$http=function($url,$headers,$body,$http2=false)use(&$calls){$calls[]=[$url,$headers,$body,$http2];return ['status'=>200,'body'=>str_contains($url,'oauth2')?['access_token'=>'test-only-access-token','expires_in'=>3600]:[]];};
    check(push_send($job,$config,$http)['status']===200);check($calls[0][0]==='https://api.push.apple.com/3/device/'.$job['token'] && $calls[0][3]);
    check(in_array('apns-topic: com.quizfolk.ios',$calls[0][1],true));check($calls[0][2]['aps']['alert']['title']==='New challenge');
    $job['platform']='android';check(push_send($job,$config,$http)['status']===200);
    check($calls[1][0]==='https://oauth2.googleapis.com/token');check($calls[2][0]==='https://fcm.googleapis.com/v1/projects/quizfolk-test/messages:send');
    check($calls[2][2]['message']['android']['priority']==='HIGH' && $calls[2][2]['message']['data']['id']==='test-duel');
    check(!isset($calls[2][2]['message']['notification']));
    echo "PASS: ES256/RS256 signatures, APNs headers/environment, FCM OAuth scope and data-message delivery contracts\n";
} finally {unlink($dir.'/apns.p8');unlink($dir.'/firebase.json');rmdir($dir);}
