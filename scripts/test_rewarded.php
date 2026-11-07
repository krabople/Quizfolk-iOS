<?php
declare(strict_types=1);
require dirname(__DIR__).'/backend/tournaments.php';
require dirname(__DIR__).'/backend/rewarded.php';
function sql(PDO $db,string $query,array $args=[]):PDOStatement {$s=$db->prepare($query);$s->execute($args);return $s;}
function check(bool $ok,string $message):void {if(!$ok)throw new RuntimeException($message);}
function rejected(callable $fn,string $label):void {try{$fn();}catch(RewardedError){return;}throw new RuntimeException('Accepted '.$label);}
function atomic(PDO $db,callable $fn):mixed {$db->exec('BEGIN IMMEDIATE');try{$r=$fn();$db->exec('COMMIT');return $r;}catch(Throwable $e){if($db->inTransaction())$db->rollBack();throw $e;}}
function database(string $path=':memory:'):PDO {
    $db=new PDO('sqlite:'.$path,null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
    $db->exec('PRAGMA foreign_keys=ON;PRAGMA busy_timeout=5000;');
    return $db;
}
$settings=rewarded_settings(['rewarded'=>['enabled'=>true,'units'=>['ios'=>'ca-app-pub-1111111111111111/1111111111','android'=>'ca-app-pub-2222222222222222/2222222222']]]);
// Independent processes exercise SQLite's lock/unique constraints, rather than
// simulating concurrency with two sequential function calls.
if(($argv[1] ?? '')==='--worker') {
    [$script,$mode,$operation,$path,$input,$gate]=$argv;$db=database($path);
    $deadline=microtime(true)+10;while(!is_file($gate)){if(microtime(true)>$deadline)exit(2);usleep(10000);}
    $value=json_decode((string)file_get_contents($input),true,16,JSON_THROW_ON_ERROR);
    $reply=$operation==='complete'?rewarded_complete($db,$value['params'],$value['now']):atomic($db,fn()=>rewarded_start($db,'alice','ios',$settings,$value['now'],$value['requestKey']));
    echo json_encode($reply,JSON_THROW_ON_ERROR);exit;
}

$db=database();$db->exec('CREATE TABLE players(id TEXT PRIMARY KEY);INSERT INTO players VALUES("alice"),("bob");');
tournament_schema($db);rewarded_schema($db);rewarded_schema($db);
$now=strtotime('2026-11-07 12:00 UTC');
function start(PDO $db,array $settings,int $now,string $pid='alice',string $platform='ios'):array {
    return atomic($db,fn()=>rewarded_start($db,$pid,$platform,$settings,$now,bin2hex(random_bytes(16))));
}
$ec=openssl_pkey_new(['private_key_type'=>OPENSSL_KEYTYPE_EC,'curve_name'=>'prime256v1']);
check($ec!==false,'Could not create isolated signing fixture');$pem=openssl_pkey_get_details($ec)['key'];
function params(array $attempt,int $event):array {
    return ['ad_network'=>'5450213213286189855','ad_unit'=>$attempt['adUnitId'],'custom_data'=>$attempt['id'],
        'reward_amount'=>'5','reward_item'=>'coins','timestamp'=>(string)($event*1000),'transaction_id'=>bin2hex(random_bytes(16))];
}
function signed(array $p,OpenSSLAsymmetricKey $ec,string $id='12345'):string {
    ksort($p);$raw=http_build_query($p,'','&',PHP_QUERY_RFC3986);openssl_sign($raw,$signature,$ec,OPENSSL_ALGO_SHA256);
    return $raw.'&signature='.rtrim(strtr(base64_encode($signature),'+/','-_'),'=').'&key_id='.$id;
}
function complete(PDO $db,array $p,OpenSSLAsymmetricKey $ec,string $pem,int $now):array {
    return rewarded_complete($db,rewarded_verify_callback(rewarded_parse_callback(signed($p,$ec)),$pem),$now);
}
function setup(PDO $db,array $p,OpenSSLAsymmetricKey $ec,string $pem,array $config,int $now):?array {
    $parsed=rewarded_parse_callback(signed($p,$ec));$verified=rewarded_verify_callback($parsed,$pem);
    return rewarded_setup_probe($db,$verified,$parsed['signed'],$config,$now);
}

$disabled=atomic($db,fn()=>rewarded_status($db,'alice','ios',rewarded_settings([]),$now));
check(!$disabled['enabled'] && !$disabled['available'] && $disabled['reason']==='disabled','Unconfigured ads enabled');
check($disabled['dailyLimit']===null && $disabled['remainingToday']===null,'Unlimited fields not null');
check($disabled['reward']===5,'Reward is not exactly5 coins');
check(rewarded_unit(['units'=>['ios'=>'ca-app-pub-3940256099942544/1712485313']],'ios')===null,'Production accepted Google test unit');
rejected(fn()=>rewarded_platform('web'),'unsupported platform');
$key=bin2hex(random_bytes(16));$first=atomic($db,fn()=>rewarded_start($db,'alice','ios',$settings,$now,$key));$a=$first['attempt'];
$repeat=atomic($db,fn()=>rewarded_start($db,'alice','ios',$settings,$now+1,$key));
check($repeat['attempt']['id']===$a['id'],'Request retry allocated another attempt');
$blocked=start($db,$settings,$now+1,'alice','android');
check(isset($blocked['error']) && $blocked['attempt']['id']===$a['id'] && $blocked['reason']==='pending','Cross-platform pending guard failed');
$resume=atomic($db,fn()=>rewarded_status($db,'alice','android',$settings,$now+1));
check($resume['attempt']['id']===$a['id'],'Relaunch did not restore pending attempt');
rejected(fn()=>atomic($db,fn()=>rewarded_status($db,'bob','ios',$settings,$now,$a['id'])),'foreign account status');
rejected(fn()=>atomic($db,fn()=>rewarded_cancel($db,'bob','ios',$settings,$now,$a['id'])),'foreign account cancellation');
$p=params($a,$now+20);$query=signed($p,$ec);
$parsed=rewarded_parse_callback($query);check($parsed['signed']===substr($query,0,strpos($query,'&signature=')),'Changed raw signed query');
check(rewarded_verify_callback($parsed,$pem)===$p,'Valid ECDSA raw query failed');
rejected(fn()=>rewarded_verify_callback(rewarded_parse_callback(str_replace('reward_amount=5','reward_amount=10',$query)),$pem),'tampered amount');
rejected(fn()=>rewarded_parse_callback('reward_amount=5&'.$query),'duplicate query key');
rejected(fn()=>rewarded_parse_callback($query.'&unsigned=1'),'unsigned trailing fields');
rejected(fn()=>rewarded_parse_callback(str_replace('custom_data=','custom%5fdata=',$query)),'encoded field name');
rejected(fn()=>complete($db,$p+['user_id'=>'alice'],$ec,$pem,$now+30),'provider user identifier');
rejected(fn()=>rewarded_parse_callback(str_replace('&key_id=12345','&key_id=https://evil.invalid/key',$query)),'request-controlled key URL');
foreach(['ad_unit'=>'3333333333','reward_amount'=>'10','reward_item'=>'cash','custom_data'=>str_repeat('f',64),'timestamp'=>(string)(($now-100)*1000)] as $field=>$value) {
    $bad=$p;$bad[$field]=$value;rejected(fn()=>complete($db,$bad,$ec,$pem,$now+30),'signed wrong '.$field);
}
$future=$p;$future['timestamp']=(string)(($now+200)*1000);rejected(fn()=>complete($db,$future,$ec,$pem,$now),'future completion');
check(complete($db,$p,$ec,$pem,$now+30)['duplicate']===false,'Valid reward not granted');
check(complete($db,$p,$ec,$pem,$now+40)['duplicate']===true,'Callback replay not idempotent');
$after=atomic($db,fn()=>rewarded_status($db,'alice','ios',$settings,$now+40,$a['id']));
check($after['wallet']['coins']===105 && $after['attempt']['awardedCoins']===5 && $after['available'],'Verified reward/wallet/no cooldown incorrect');
$again=$p;$again['transaction_id']=bin2hex(random_bytes(16));rejected(fn()=>complete($db,$again,$ec,$pem,$now+40),'second transaction on same attempt');
atomic($db,fn()=>rewarded_cancel($db,'alice','ios',$settings,$now+41,$a['id']));
check(tournament_wallet($db,'alice')['coins']===105,'Cancellation removed earned coins');

// No-fill releases availability; a late event that actually happened before
// cancellation is still honoured. A post-cancellation event cannot earn.
$noFill=start($db,$settings,$now+50)['attempt'];
$cancel=atomic($db,fn()=>rewarded_cancel($db,'alice','ios',$settings,$now+60,$noFill['id']));
check($cancel['available'] && $cancel['attempt']['status']==='cancelled' && $cancel['wallet']['coins']===105,'No-fill cancellation did not release');
rejected(fn()=>complete($db,params($noFill,$now+65),$ec,$pem,$now+70),'completion after cancellation');
complete($db,params($noFill,$now+55),$ec,$pem,$now+80);
check(tournament_wallet($db,'alice')['coins']===110,'Delayed pre-cancel reward lost');

// Expiry stops a new presentation, not delivery of a previously earned reward.
$midnight=intdiv($now,86400)*86400+86400;
$late=start($db,$settings,$midnight-20)['attempt'];
$expired=atomic($db,fn()=>rewarded_status($db,'alice','ios',$settings,$midnight+1000,$late['id']));
check($expired['attempt']['status']==='expired' && $expired['available'],'Expired reservation blocked forever');
complete($db,params($late,$midnight+10),$ec,$pem,$midnight+1001);
$today=atomic($db,fn()=>rewarded_status($db,'alice','ios',$settings,$midnight+1002,$late['id']));
check($today['wallet']['coins']===115 && $today['earnedToday']===0,'Late callback did not preserve reservation UTC day');
$stale=start($db,$settings,$midnight+1100)['attempt'];
rejected(fn()=>complete($db,params($stale,$stale['expires']),$ec,$pem,$stale['expires']),'completion outside expiry');
rejected(fn()=>complete($db,params($stale,$midnight+1110),$ec,$pem,$stale['expires']+259201),'delivery beyond callback grace');
atomic($db,fn()=>rewarded_cancel($db,'alice','ios',$settings,$midnight+1200,$stale['id']));
for($i=0;$i<8;$i++){$unlimited=start($db,$settings,$midnight+1300+$i*20)['attempt'];complete($db,params($unlimited,$unlimited['created']+5),$ec,$pem,$unlimited['created']+6);}
$unlimitedStatus=atomic($db,fn()=>rewarded_status($db,'alice','android',$settings,$midnight+2000));
check($unlimitedStatus['earnedToday']===8 && $unlimitedStatus['available'] && $unlimitedStatus['dailyLimit']===null,'Unexpected daily cap');
$other=start($db,$settings,$midnight+2100,'bob','android')['attempt'];
$cross=params($other,$midnight+2105);$cross['transaction_id']=$p['transaction_id'];rejected(fn()=>complete($db,$cross,$ec,$pem,$midnight+2110),'transaction reused for another account');
check(tournament_wallet($db,'bob')['coins']===100,'Other account wallet changed');

// Dashboard setup is cryptographically verified and has a separate nonce,
// receipt and15-minute deadline. It can never become a coin-bearing attempt.
$probeToken=bin2hex(random_bytes(32));$probeConfig=['rewarded'=>['setup_probe'=>['token_sha256'=>hash('sha256',$probeToken),'issued'=>$now,'expires'=>$now+900]]];
$probe=params(['id'=>$probeToken,'adUnitId'=>'1234567890'],$now+20);$probe['transaction_id']='123456789';
$walletBefore=$db->query('SELECT * FROM tournament_wallet ORDER BY player_id')->fetchAll();
$ledgerBefore=(int)$db->query('SELECT COUNT(*) FROM tournament_ledger')->fetchColumn();
$setupReply=setup($db,$probe,$ec,$pem,$probeConfig,$now+30);
check($setupReply===['ok'=>true,'setupVerified'=>true,'credited'=>false,'duplicate'=>false],'Valid signed setup probe not accepted');
check(setup($db,$probe,$ec,$pem,$probeConfig,$now+31)['duplicate']===true,'Exact setup retry not idempotent');
$second=$probe;$second['timestamp']=(string)(($now+21)*1000);rejected(fn()=>setup($db,$second,$ec,$pem,$probeConfig,$now+32),'reused setup nonce with different signed event');
$wrongNonce=$probe;$wrongNonce['custom_data']=str_repeat('a',64);check(setup($db,$wrongNonce,$ec,$pem,$probeConfig,$now+30)===null,'Unknown nonce became setup probe');
foreach(['ad_unit'=>'1111111111','reward_amount'=>'10','reward_item'=>'cash','user_id'=>'alice'] as $field=>$value){$bad=$probe;$bad[$field]=$value;rejected(fn()=>setup($db,$bad,$ec,$pem,$probeConfig,$now+30),'wrong setup '.$field);}
rejected(fn()=>setup($db,$probe,$ec,$pem,$probeConfig,$now+901),'expired setup probe');
check(setup($db,$probe,$ec,$pem,[],$now+30)===null,'Unconfigured setup probe enabled');
$tampered=rewarded_parse_callback(str_replace('reward_amount=5','reward_amount=6',signed($probe,$ec)));rejected(fn()=>rewarded_verify_callback($tampered,$pem),'unsigned setup amount change');
check($db->query('SELECT * FROM tournament_wallet ORDER BY player_id')->fetchAll()===$walletBefore && (int)$db->query('SELECT COUNT(*) FROM tournament_ledger')->fetchColumn()===$ledgerBefore,'Setup probe touched wallets/ledger');
rejected(fn()=>complete($db,$probe,$ec,$pem,$now+30),'setup nonce as a normal reward attempt');
$productionWrong=params($other,$midnight+2105);$productionWrong['ad_unit']='1234567890';rejected(fn()=>setup($db,$productionWrong,$ec,$pem,$probeConfig,$midnight+2106) ?? complete($db,$productionWrong,$ec,$pem,$midnight+2106),'synthetic unit with real account attempt');

$testRoot=dirname(__DIR__).'/build';if(!is_dir($testRoot))mkdir($testRoot,0700);
$folder=$testRoot.'/quizfolk-reward-test-'.bin2hex(random_bytes(8));mkdir($folder,0700);
try {
    $diagnosticConfig=['rewarded'=>['diagnostic_until'=>$now+900]];
    rewarded_diagnostic($query,$folder,$diagnosticConfig,'reward',true,'Reward configuration mismatch.', $now);
    $log=(string)file_get_contents($folder.'/rewarded-diagnostic.jsonl');$record=json_decode(trim($log),true);
    check(!str_contains($log,$p['custom_data']) && !str_contains($log,$p['transaction_id']) && !str_contains($log,$parsed['signature']),'Diagnostic leaked reward identifiers');
    check($record['signatureValid']===true && $record['rewardAmount']==='5' && $record['transactionLength']===32,'Sanitized diagnostic lost useful shape');
    rewarded_diagnostic($query,$folder,$diagnosticConfig,'reward',true,null,$now+901);
    check(file_get_contents($folder.'/rewarded-diagnostic.jsonl')===$log,'Expired diagnostic still wrote data');
    $calls=0;$fetch=function()use(&$calls,$pem){$calls++;return json_encode(['keys'=>[['keyId'=>12345,'pem'=>$pem]]],JSON_THROW_ON_ERROR);};
    check(rewarded_public_key('12345',$folder,$now,$fetch)===$pem && $calls===1,'Initial verifier fetch failed');
    rewarded_public_key('12345',$folder,$now+10,$fetch);check($calls===1,'Public key cache missed');
    $rotated=function()use(&$calls,$pem){$calls++;return json_encode(['keys'=>[['keyId'=>67890,'pem'=>$pem]]],JSON_THROW_ON_ERROR);};
    check(rewarded_public_key('67890',$folder,$now+11,$rotated)===$pem && $calls===2,'Unknown key did not refresh rotation');
    rejected(fn()=>rewarded_public_key('999',$folder,$now+12,$rotated),'unknown verifier key');
    check($calls===2,'Unknown keys triggered unbounded downloads');
    $offline=static function(){throw new RuntimeException('Offline fixture');};
    check(rewarded_public_key('67890',$folder,$now+22000,$offline)===$pem,'Valid cached key unavailable during short outage');
    $failed=false;try{rewarded_public_key('67890',$folder,$now+90000,$offline);}catch(RuntimeException){$failed=true;}check($failed,'Keys cached longer than24 hours');
    $rsa=openssl_pkey_new(['private_key_type'=>OPENSSL_KEYTYPE_RSA,'private_key_bits'=>2048]);
    $invalid=false;try{rewarded_key_map(json_encode(['keys'=>[['keyId'=>1,'pem'=>openssl_pkey_get_details($rsa)['key']]]]));}catch(RuntimeException){$invalid=true;}check($invalid,'Accepted non-EC verifier key');

    $path=$folder.'/race.sqlite';$race=database($path);$race->exec('PRAGMA journal_mode=WAL; CREATE TABLE players(id TEXT PRIMARY KEY);INSERT INTO players VALUES("alice");');tournament_schema($race);rewarded_schema($race);
    function race(array $inputs,string $operation,string $folder,string $path):array {
        $gate=$folder.'/gate-'.$operation;$children=[];
        foreach($inputs as $index=>$value) {
            $file=$folder.'/input-'.$operation.'-'.$index.'.json';file_put_contents($file,json_encode($value));
            $cmd=[PHP_BINARY];if(PHP_OS_FAMILY==='Windows')$cmd=array_merge($cmd,['-d','extension_dir='.ini_get('extension_dir'),'-d','extension=pdo_sqlite','-d','extension=openssl']);
            $cmd=array_merge($cmd,[__FILE__,'--worker',$operation,$path,$file,$gate]);
            $proc=proc_open($cmd,[0=>['pipe','r'],1=>['pipe','w'],2=>['pipe','w']],$pipes);check(is_resource($proc),'Could not start concurrency worker');fclose($pipes[0]);$children[]=[$proc,$pipes];
        }
        touch($gate);$answers=[];
        foreach($children as [$proc,$pipes]){$out=stream_get_contents($pipes[1]);$err=stream_get_contents($pipes[2]);fclose($pipes[1]);fclose($pipes[2]);$code=proc_close($proc);check($code===0,'Concurrency worker failed: '.$err);$answers[]=json_decode($out,true,16,JSON_THROW_ON_ERROR);}
        return $answers;
    }
    $results=race([['now'=>$now,'requestKey'=>str_repeat('a',32)],['now'=>$now,'requestKey'=>str_repeat('b',32)]],'start',$folder,$path);
    check(count(array_filter($results,fn($r)=>isset($r['error'])))===1 && (int)$race->query('SELECT COUNT(*) FROM rewarded_attempts')->fetchColumn()===1,'Concurrent reservations created two active attempts');
    $candidate=array_values(array_filter($results,fn($r)=>!isset($r['error'])))[0]['attempt'];$verified=rewarded_verify_callback(rewarded_parse_callback(signed(params($candidate,$now+10),$ec)),$pem);
    $results=race([['now'=>$now+20,'params'=>$verified],['now'=>$now+20,'params'=>$verified]],'complete',$folder,$path);
    check(count(array_filter($results,fn($r)=>$r['duplicate']))===1 && tournament_wallet($race,'alice')['coins']===105,'Concurrent callback credited more than once');
    $race=null;
} finally {
    foreach(glob($folder.'/*') as $file)unlink($file);rmdir($folder);
}
$receiptCount=(int)$db->query('SELECT COUNT(*) FROM rewarded_receipts')->fetchColumn();
// Google documents transaction IDs as unique hex strings without a minimum
// length; dashboard examples use9 characters. Empty optional user_id is valid.
$short=start($db,$settings,$midnight+4000)['attempt'];$shortParams=params($short,$midnight+4001);$shortParams['transaction_id']='123456789';$shortParams['user_id']='';
$shortParams['ad_unit']='1111111111'; // Exact numeric suffix is Google's documented callback representation.
$substring=$shortParams;$substring['ad_unit']='111111111';rejected(fn()=>complete($db,$substring,$ec,$pem,$midnight+4002),'partial ad-unit suffix');
$beforeNumeric=tournament_wallet($db,'alice')['coins'];
complete($db,$shortParams,$ec,$pem,$midnight+4002);
check(tournament_wallet($db,'alice')['coins']===$beforeNumeric+5,'Exact numeric ad-unit suffix did not earn5 coins');
$receiptCount++;
$db->exec('DELETE FROM players WHERE id="alice"');
check((int)sql($db,'SELECT COUNT(*) FROM rewarded_attempts WHERE player_id="alice"')->fetchColumn()===0,'Account deletion left attempts');
check((int)$db->query('SELECT COUNT(*) FROM rewarded_receipts')->fetchColumn()===$receiptCount,'Deletion removed global replay protection');
check(complete($db,$p,$ec,$pem,$midnight+3000)['duplicate'],'Deleted-account duplicate was not harmless');
check((int)$db->query('SELECT COUNT(*) FROM tournament_wallet WHERE player_id="alice"')->fetchColumn()===0,'Deleted account recreated by callback');
echo "PASS: raw-query ECDSA, strict binding, key rotation/cache, idempotency, cross-platform reservation, no-fill/cancel races, expiry/late delivery/UTC rollover, unlimited rewards, parallel reservation+callback, account deletion\n";
