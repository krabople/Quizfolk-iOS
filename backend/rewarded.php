<?php
declare(strict_types=1);
const QUIZFOLK_REWARDED_COINS=5;

final class RewardedError extends RuntimeException {
    public function __construct(string $message,public readonly int $status=400){parent::__construct($message);}
}

function rewarded_schema(PDO $db):void {
    $db->exec('CREATE TABLE IF NOT EXISTS rewarded_attempts(
        id TEXT PRIMARY KEY,player_id TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
        platform TEXT NOT NULL,ad_unit TEXT NOT NULL,request_key TEXT NOT NULL,
        created INTEGER NOT NULL,expires INTEGER NOT NULL,callback_deadline INTEGER NOT NULL,
        day INTEGER NOT NULL,state TEXT NOT NULL DEFAULT "pending",cancelled INTEGER,
        rewarded INTEGER,transaction_hash TEXT UNIQUE,UNIQUE(player_id,request_key));
        CREATE UNIQUE INDEX IF NOT EXISTS rewarded_one_pending ON rewarded_attempts(player_id) WHERE state="pending";
        CREATE INDEX IF NOT EXISTS rewarded_player_day ON rewarded_attempts(player_id,day,state);
        CREATE TABLE IF NOT EXISTS rewarded_receipts(transaction_hash TEXT PRIMARY KEY,attempt_hash TEXT NOT NULL,created INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS rewarded_setup_receipts(probe_hash TEXT PRIMARY KEY,payload_hash TEXT NOT NULL,created INTEGER NOT NULL);');
}

function rewarded_settings(array $config):array {
    $c=$config['rewarded'] ?? [];
    return ['enabled'=>($c['enabled'] ?? false)===true,'units'=>is_array($c['units'] ?? null)?$c['units']:[],
        'cooldown'=>max(0,min(3600,(int)($c['cooldown_seconds'] ?? 0))),
        'duration'=>max(60,min(3600,(int)($c['attempt_seconds'] ?? 600))),
        'grace'=>max(3600,min(604800,(int)($c['callback_grace_seconds'] ?? 259200)))];
}

function rewarded_platform(mixed $value):string {
    if(!is_string($value) || !in_array($value,['ios','android'],true))throw new RewardedError('Choose a supported app platform.');
    return $value;
}

function rewarded_unit(array $settings,string $platform):?string {
    $unit=$settings['units'][$platform] ?? '';
    if(!is_string($unit) || !preg_match('/^ca-app-pub-\d{16}\/\d{10}$/D',$unit) || str_starts_with($unit,'ca-app-pub-3940256099942544/'))return null;
    return $unit;
}

function rewarded_expire(PDO $db,string $pid,int $now):void {
    sql($db,'UPDATE rewarded_attempts SET state="expired" WHERE player_id=? AND state="pending" AND expires<=?',[$pid,$now]);
}

function rewarded_attempt_card(array|false $row):?array {
    if(!$row)return null;
    return ['id'=>$row['id'],'platform'=>$row['platform'],'status'=>$row['state'],
        'adUnitId'=>$row['ad_unit'],'customData'=>$row['id'],'created'=>(int)$row['created'],
        'expires'=>(int)$row['expires'],'awardedCoins'=>$row['state']==='awarded'?QUIZFOLK_REWARDED_COINS:0];
}

// Caller holds BEGIN IMMEDIATE. All coin balances come from the shared wallet.
function rewarded_status(PDO $db,string $pid,string $platform,array $settings,int $now,?string $attempt=null):array {
    rewarded_expire($db,$pid,$now);
    $pending=sql($db,'SELECT * FROM rewarded_attempts WHERE player_id=? AND state="pending"',[$pid])->fetch();
    if($attempt!==null) {
        if(!preg_match('/^[a-f0-9]{64}$/D',$attempt))throw new RewardedError('This ad attempt is invalid.');
        $selected=sql($db,'SELECT * FROM rewarded_attempts WHERE player_id=? AND id=?',[$pid,$attempt])->fetch();
        if(!$selected)throw new RewardedError('This ad attempt was not found.',404);
    } else $selected=$pending ?: sql($db,'SELECT * FROM rewarded_attempts WHERE player_id=? ORDER BY created DESC,rowid DESC LIMIT 1',[$pid])->fetch();
    $day=intdiv($now,86400)*86400;
    $earned=(int)sql($db,'SELECT COUNT(*) FROM rewarded_attempts WHERE player_id=? AND day=? AND state="awarded"',[$pid,$day])->fetchColumn();
    $last=(int)sql($db,'SELECT COALESCE(MAX(rewarded),0) FROM rewarded_attempts WHERE player_id=?',[$pid])->fetchColumn();
    $next=$last && $last+$settings['cooldown']>$now ? $last+$settings['cooldown']:null;
    $enabled=$settings['enabled'] && rewarded_unit($settings,$platform)!==null;
    $reason=!$enabled?'disabled':($pending?'pending':($next!==null?'cooldown':'ready'));
    $wallet=tournament_wallet($db,$pid);
    return ['enabled'=>$enabled,'available'=>$reason==='ready','reason'=>$reason,'reward'=>QUIZFOLK_REWARDED_COINS,
        'dailyLimit'=>null,'earnedToday'=>$earned,'remainingToday'=>null,'resets'=>$day+86400,
        'nextAvailableAt'=>$next,'wallet'=>['coins'=>$wallet['coins']],'attempt'=>rewarded_attempt_card($selected)];
}

function rewarded_start(PDO $db,string $pid,string $platform,array $settings,int $now,mixed $requestKey):array {
    if(!is_string($requestKey) || !preg_match('/^[A-Za-z0-9_-]{16,80}$/D',$requestKey))throw new RewardedError('Use a unique ad request key.');
    rewarded_expire($db,$pid,$now);
    $old=sql($db,'SELECT * FROM rewarded_attempts WHERE player_id=? AND request_key=?',[$pid,$requestKey])->fetch();
    if($old) {
        if($old['platform']!==$platform)throw new RewardedError('This request belongs to a different platform.',409);
        return rewarded_status($db,$pid,$platform,$settings,$now,$old['id']);
    }
    $status=rewarded_status($db,$pid,$platform,$settings,$now);
    if(!$status['available'])return ['error'=>$status['reason']==='pending'?'An ad reward is already pending.':'Rewarded ads are currently unavailable.']+$status;
    $id=bin2hex(random_bytes(32));$expires=$now+$settings['duration'];
    sql($db,'INSERT INTO rewarded_attempts(id,player_id,platform,ad_unit,request_key,created,expires,callback_deadline,day) VALUES(?,?,?,?,?,?,?,?,?)',
        [$id,$pid,$platform,rewarded_unit($settings,$platform),$requestKey,$now,$expires,$expires+$settings['grace'],intdiv($now,86400)*86400]);
    return rewarded_status($db,$pid,$platform,$settings,$now,$id);
}

function rewarded_cancel(PDO $db,string $pid,string $platform,array $settings,int $now,mixed $attempt):array {
    if(!is_string($attempt))throw new RewardedError('Choose an ad attempt.');
    rewarded_status($db,$pid,$platform,$settings,$now,$attempt); // Ownership check precedes mutation.
    sql($db,"UPDATE rewarded_attempts SET state='cancelled',cancelled=? WHERE id=? AND player_id=? AND state IN ('pending','expired')",[$now,$attempt,$pid]);
    return rewarded_status($db,$pid,$platform,$settings,$now,$attempt);
}

function rewarded_routes(string $route,PDO $db,string $pid,array $body,array $config):void {
    if(!in_array($route,['rewarded-status','rewarded-start','rewarded-cancel'],true))return;
    try {
        $platform=rewarded_platform($route==='rewarded-status'?($_GET['platform'] ?? null):($body['platform'] ?? null));
        $settings=rewarded_settings($config);rewarded_schema($db);$db->exec('BEGIN IMMEDIATE');$now=time();
        $reply=match($route){
            'rewarded-start'=>rewarded_start($db,$pid,$platform,$settings,$now,$body['requestKey'] ?? null),
            'rewarded-cancel'=>rewarded_cancel($db,$pid,$platform,$settings,$now,$body['attempt'] ?? null),
            default=>rewarded_status($db,$pid,$platform,$settings,$now,isset($_GET['attempt'])?(string)$_GET['attempt']:null),
        };
        $db->exec('COMMIT');out($reply,isset($reply['error'])?409:200);
    } catch(RewardedError $e) {if($db->inTransaction())$db->rollBack();out(['error'=>$e->getMessage()],$e->status);}
}

// Keep the signed bytes exactly as received. Do not parse_str/reorder/decode
// before verification: PHP's duplicate-key/name-normalisation rules are unsafe.
function rewarded_parse_callback(string $query):array {
    if(strlen($query)>8192 || preg_match('/[\x00-\x20\x7f]/',$query) || !preg_match('/^(.+)&signature=([A-Za-z0-9_\-%=]+)&key_id=([0-9]{1,20})$/D',$query,$m))throw new RewardedError('Invalid callback query.');
    $params=[];$required=['ad_network','ad_unit','custom_data','reward_amount','reward_item','timestamp','transaction_id'];$allowed=[...$required,'user_id'];
    foreach(explode('&',$m[1]) as $part) {
        $pair=explode('=',$part,2);
        if(count($pair)!==2 || !in_array($pair[0],$allowed,true) || isset($params[$pair[0]]) || preg_match('/%(?![0-9a-fA-F]{2})/',$pair[1]))throw new RewardedError('Invalid callback fields.');
        $params[$pair[0]]=rawurldecode($pair[1]);
    }
    if(array_diff($required,array_keys($params)))throw new RewardedError('Incomplete callback.');
    $encoded=rawurldecode($m[2]);
    if(!preg_match('/^[A-Za-z0-9_-]+={0,2}$/D',$encoded))throw new RewardedError('Invalid signature encoding.');
    $signature=base64_decode(strtr($encoded,'-_','+/'),true);
    if($signature===false || strlen($signature)<64 || strlen($signature)>80)throw new RewardedError('Invalid signature encoding.');
    return ['signed'=>$m[1],'signature'=>$signature,'keyId'=>$m[3],'params'=>$params];
}

function rewarded_validate_fields(array $params):void {
    if(!preg_match('/^[0-9]{1,24}$/D',$params['ad_network']) || !preg_match('/^[a-f0-9]{64}$/D',$params['custom_data']) ||
       !preg_match('/^[0-9]{13}$/D',$params['timestamp']) || !preg_match('/^[a-fA-F0-9]{1,128}$/D',$params['transaction_id']))throw new RewardedError('Invalid reward fields.');
    // Google documents user_id as optional. Empty dashboard fields are safe;
    // production clients use only opaque custom data and never a player ID.
    if(($params['user_id'] ?? '')!=='')throw new RewardedError('Unexpected reward user identifier.',403);
}

// Temporary opt-in observation of callback shape, never its token/signature or
// raw query. A private absolute expiry turns this off without a further deploy.
function rewarded_diagnostic(string $query,string $state,array $config,string $stage,?bool $signatureValid,?string $error=null,?int $now=null):void {
    $now ??= time();$until=(int)($config['rewarded']['diagnostic_until'] ?? 0);
    if($until<=$now || $until>$now+900)return;
    $known=['ad_network','ad_unit','custom_data','reward_amount','reward_item','timestamp','transaction_id','user_id','signature','key_id'];
    $keys=[];$values=[];
    foreach(explode('&',substr($query,0,8192)) as $part) {
        $pair=explode('=',$part,2);$key=$pair[0];
        if(!in_array($key,$known,true)){$keys[]='unknown';continue;}
        $keys[]=$key;
        if(in_array($key,['ad_unit','reward_amount','reward_item','timestamp','transaction_id'],true))$values[$key]=rawurldecode($pair[1] ?? '');
    }
    $safe=static fn(string $name,string $pattern):?string=>isset($values[$name])?(preg_match($pattern,$values[$name])?$values[$name]:'invalid'):null;
    $entry=['time'=>$now,'stage'=>$stage,'error'=>$error,'signatureValid'=>$signatureValid,'keys'=>$keys,
        'adUnit'=>$safe('ad_unit','/^(?:ca-app-pub-\d{16}\/)?\d{1,20}$/D'),
        'rewardAmount'=>$safe('reward_amount','/^[0-9]{1,10}$/D'),
        'rewardItem'=>$safe('reward_item','/^[A-Za-z _-]{1,48}$/D'),
        'timestamp'=>$safe('timestamp','/^[0-9]{10,16}$/D'),
        'transactionLength'=>isset($values['transaction_id'])?strlen($values['transaction_id']):null,
        'userIdPresent'=>in_array('user_id',$keys,true)];
    $file=$state.'/rewarded-diagnostic.jsonl';$handle=@fopen($file,'c+');if(!$handle)return;
    try {if(flock($handle,LOCK_EX)){if(fstat($handle)['size']<32768){fseek($handle,0,SEEK_END);fwrite($handle,json_encode($entry,JSON_UNESCAPED_SLASHES|JSON_THROW_ON_ERROR)."\n");}flock($handle,LOCK_UN);}}
    finally {fclose($handle);@chmod($file,0600);}
}

function rewarded_key_map(string $json):array {
    try {$data=json_decode($json,true,16,JSON_THROW_ON_ERROR);}catch(JsonException){throw new RuntimeException('Reward verifier keys unavailable.');}
    $result=[];
    foreach(($data['keys'] ?? []) as $entry) {
        $id=(string)($entry['keyId'] ?? '');$pem=$entry['pem'] ?? '';
        if(!preg_match('/^[0-9]{1,20}$/D',$id) || !is_string($pem) || strlen($pem)>4096)throw new RuntimeException('Invalid reward verifier keys.');
        $key=openssl_pkey_get_public($pem);$details=$key?openssl_pkey_get_details($key):false;
        if(!$details || $details['type']!==OPENSSL_KEYTYPE_EC || ($details['ec']['curve_name'] ?? '')!=='prime256v1')throw new RuntimeException('Invalid reward verifier key type.');
        $result[$id]=$pem;
    }
    if(!$result)throw new RuntimeException('Reward verifier keys unavailable.');
    return $result;
}

function rewarded_fetch_keys():string {
    if(!function_exists('curl_init'))throw new RuntimeException('Reward verifier transport unavailable.');
    $ch=curl_init('https://www.gstatic.com/admob/reward/verifier-keys.json');$body='';
    curl_setopt_array($ch,[CURLOPT_FOLLOWLOCATION=>false,CURLOPT_CONNECTTIMEOUT=>3,CURLOPT_TIMEOUT=>6,
        CURLOPT_SSL_VERIFYPEER=>true,CURLOPT_SSL_VERIFYHOST=>2,CURLOPT_PROTOCOLS=>CURLPROTO_HTTPS,
        CURLOPT_WRITEFUNCTION=>static function($handle,string $chunk)use(&$body):int{if(strlen($body)+strlen($chunk)>65536)return 0;$body.=$chunk;return strlen($chunk);}]);
    $ok=curl_exec($ch);$status=(int)curl_getinfo($ch,CURLINFO_RESPONSE_CODE);curl_close($ch);
    if($ok===false || $status!==200)throw new RuntimeException('Reward verifier keys unavailable.');
    return $body;
}

function rewarded_public_key(string $keyId,string $state,int $now,?callable $fetch=null):string {
    $file=$state.'/rewarded-verifier-keys.json';$lock=fopen($state.'/rewarded-verifier-keys.lock','c');
    if(!$lock || !flock($lock,LOCK_EX))throw new RuntimeException('Reward verifier lock unavailable.');
    try {
        $cache=is_file($file)?json_decode((string)file_get_contents($file),true):null;
        $age=$cache ? $now-(int)($cache['fetched'] ?? 0):PHP_INT_MAX;
        $keys=[];
        if($cache && $age>=0 && $age<86400){try{$keys=rewarded_key_map((string)($cache['json'] ?? ''));}catch(Throwable){$keys=[];}}
        if(isset($keys[$keyId]) && $age<21600)return $keys[$keyId];
        // Unknown IDs cannot force a fetch for every unauthenticated request.
        if(!isset($keys[$keyId]) && $keys && $now-(int)($cache['unknownRefreshed'] ?? 0)<60)throw new RewardedError('Unknown verification key.',403);
        try {
            $unknown=!isset($keys[$keyId]);
            $json=($fetch ?? 'rewarded_fetch_keys')();$fresh=rewarded_key_map($json);
            $temp=$file.'.'.bin2hex(random_bytes(6)).'.tmp';
            if(file_put_contents($temp,json_encode(['fetched'=>$now,'unknownRefreshed'=>$unknown && $keys?$now:0,'json'=>$json],JSON_THROW_ON_ERROR),LOCK_EX)===false)throw new RuntimeException('Reward verifier cache unavailable.');
            chmod($temp,0600);if(!rename($temp,$file)){@unlink($temp);throw new RuntimeException('Reward verifier cache unavailable.');}$keys=$fresh;
        } catch(RuntimeException $e) {if(!isset($keys[$keyId]))throw $e;}
        if(!isset($keys[$keyId]))throw new RewardedError('Unknown verification key.',403);
        return $keys[$keyId];
    } finally {flock($lock,LOCK_UN);fclose($lock);}
}

function rewarded_verify_callback(array $parsed,string $pem):array {
    $key=openssl_pkey_get_public($pem);$details=$key?openssl_pkey_get_details($key):false;
    if(!$details || $details['type']!==OPENSSL_KEYTYPE_EC || ($details['ec']['curve_name'] ?? '')!=='prime256v1' ||
       openssl_verify($parsed['signed'],$parsed['signature'],$key,OPENSSL_ALGO_SHA256)!==1)throw new RewardedError('Invalid reward signature.',403);
    return $parsed['params'];
}

// The AdMob dashboard sends a signed synthetic unit1234567890 when verifying
// the URL. A separately configured short-lived nonce can acknowledge that probe
// without ever touching an account, attempt, wallet or production receipt.
// Call only after Google's signature verification, exactly like completion.
function rewarded_setup_probe(PDO $db,array $p,string $signedContent,array $config,int $now):?array {
    $probe=$config['rewarded']['setup_probe'] ?? null;
    if(!is_array($probe) || !preg_match('/^[a-f0-9]{64}$/D',(string)($probe['token_sha256'] ?? '')))return null;
    if(!hash_equals($probe['token_sha256'],hash('sha256',(string)($p['custom_data'] ?? ''))))return null;
    rewarded_validate_fields($p);
    $issued=(int)($probe['issued'] ?? 0);$expires=(int)($probe['expires'] ?? 0);$event=(int)$p['timestamp'];
    if($issued<=0 || $expires<=$issued || $expires-$issued>900 || $now<$issued || $now>$expires ||
       $event<($issued-5)*1000 || $event>($now+120)*1000 || $event>=$expires*1000)throw new RewardedError('Setup verification has expired.',403);
    if($p['ad_unit']!=='1234567890' || $p['reward_amount']!==(string)QUIZFOLK_REWARDED_COINS || $p['reward_item']!=='coins')throw new RewardedError('Setup verification fields do not match.',403);
    $payloadHash=hash('sha256',$signedContent);$db->exec('BEGIN IMMEDIATE');
    try {
        $receipt=sql($db,'SELECT payload_hash FROM rewarded_setup_receipts WHERE probe_hash=?',[$probe['token_sha256']])->fetch();
        if($receipt && !hash_equals($receipt['payload_hash'],$payloadHash))throw new RewardedError('Setup verification has already been used.',409);
        if(!$receipt)sql($db,'INSERT INTO rewarded_setup_receipts VALUES(?,?,?)',[$probe['token_sha256'],$payloadHash,$now]);
        $db->exec('COMMIT');return ['ok'=>true,'setupVerified'=>true,'credited'=>false,'duplicate'=>(bool)$receipt];
    } catch(Throwable $e) {if($db->inTransaction())$db->rollBack();throw $e;}
}

// Only call with cryptographically verified fields. This transaction owns the
// unique provider receipt, attempt transition and shared wallet credit together.
function rewarded_complete(PDO $db,array $p,int $now):array {
    rewarded_validate_fields($p);
    $db->exec('BEGIN IMMEDIATE');
    try {
        $transaction=hash('sha256',strtolower($p['transaction_id']));$attemptHash=hash('sha256',$p['custom_data']);
        $receipt=sql($db,'SELECT attempt_hash FROM rewarded_receipts WHERE transaction_hash=?',[$transaction])->fetch();
        if($receipt) {
            if(!hash_equals($receipt['attempt_hash'],$attemptHash))throw new RewardedError('Reward transaction mismatch.',409);
            $db->exec('COMMIT');return ['ok'=>true,'duplicate'=>true];
        }
        $attempt=sql($db,'SELECT * FROM rewarded_attempts WHERE id=?',[$p['custom_data']])->fetch();
        if(!$attempt)throw new RewardedError('Reward attempt was not found.',404);
        $suffix=substr($attempt['ad_unit'],strrpos($attempt['ad_unit'],'/')+1);
        if(!in_array($p['ad_unit'],[$attempt['ad_unit'],$suffix],true) || $p['reward_amount']!==(string)QUIZFOLK_REWARDED_COINS || $p['reward_item']!=='coins')throw new RewardedError('Reward configuration mismatch.',403);
        $event=(int)$p['timestamp'];
        if($event<((int)$attempt['created']-5)*1000 || $event>=(int)$attempt['expires']*1000 || $event>($now+120)*1000 || $now>(int)$attempt['callback_deadline'])throw new RewardedError('Reward timestamp is outside its attempt window.',403);
        if($attempt['cancelled']!==null && $event>((int)$attempt['cancelled']+1)*1000-1)throw new RewardedError('Reward attempt was cancelled before completion.',403);
        if($attempt['state']==='awarded')throw new RewardedError('This attempt already has a reward.',409);
        sql($db,'INSERT INTO rewarded_receipts VALUES(?,?,?)',[$transaction,$attemptHash,$now]);
        sql($db,'UPDATE rewarded_attempts SET state="awarded",rewarded=?,transaction_hash=? WHERE id=?',[$now,$transaction,$attempt['id']]);
        tournament_credit($db,$attempt['player_id'],'rewarded-ad:'.$transaction,QUIZFOLK_REWARDED_COINS,0);
        $db->exec('COMMIT');return ['ok'=>true,'duplicate'=>false];
    } catch(Throwable $e) {if($db->inTransaction())$db->rollBack();throw $e;}
}
