<?php
declare(strict_types=1);

const PUSH_KINDS=['challenges','duelResults','tournamentPrizes','friendsTournaments'];
function push_schema(PDO $db):void {
    $db->exec('CREATE TABLE IF NOT EXISTS push_settings(player_id TEXT PRIMARY KEY REFERENCES players(id) ON DELETE CASCADE,enabled INTEGER NOT NULL DEFAULT 0,challenges INTEGER NOT NULL DEFAULT 1,duelResults INTEGER NOT NULL DEFAULT 1,tournamentPrizes INTEGER NOT NULL DEFAULT 1,friendsTournaments INTEGER NOT NULL DEFAULT 1);
      CREATE TABLE IF NOT EXISTS push_devices(id TEXT PRIMARY KEY,player_id TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,platform TEXT NOT NULL,environment TEXT NOT NULL,token TEXT NOT NULL,enabled INTEGER NOT NULL,updated INTEGER NOT NULL,UNIQUE(platform,environment,token));
      CREATE TABLE IF NOT EXISTS push_jobs(id TEXT PRIMARY KEY,player_id TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,device_id TEXT NOT NULL REFERENCES push_devices(id) ON DELETE CASCADE,event_key TEXT NOT NULL,kind TEXT NOT NULL,actor TEXT,title TEXT NOT NULL,body TEXT NOT NULL,payload TEXT NOT NULL,status TEXT NOT NULL DEFAULT "pending",attempts INTEGER NOT NULL DEFAULT 0,due INTEGER NOT NULL,created INTEGER NOT NULL,expires INTEGER NOT NULL,last_error TEXT,UNIQUE(device_id,event_key));
      CREATE INDEX IF NOT EXISTS push_jobs_due ON push_jobs(status,due);');
}
function push_preferences(PDO $db,string $pid):array {
    sql($db,'INSERT OR IGNORE INTO push_settings(player_id) VALUES(?)',[$pid]);
    $r=sql($db,'SELECT * FROM push_settings WHERE player_id=?',[$pid])->fetch();
    $out=[];foreach(array_merge(['enabled'],PUSH_KINDS) as $key)$out[$key]=(bool)$r[$key];return $out;
}
function push_ready(array $config):array {
    $p=$config['push'] ?? [];
    return ['ios'=>!empty($p['apns_key_file']) && is_readable($p['apns_key_file']) && !empty($p['apns_key_id']) && !empty($p['apple_team_id']),
        'android'=>!empty($p['fcm_service_account_file']) && is_readable($p['fcm_service_account_file'])];
}
function push_routes(string $route,PDO $db,string $pid,array $body,array $config):void {
    if($route==='notification-settings')out(['preferences'=>push_preferences($db,$pid),'delivery'=>push_ready($config)]);
    if($route==='notification-preferences') {
        $values=$body['preferences'] ?? null;
        if(!is_array($values) || count(array_diff(array_keys($values),array_merge(['enabled'],PUSH_KINDS))))fail('Invalid notification preferences');
        foreach($values as $key=>$value)if(!is_bool($value))fail('Notification choices must be true or false');
        $db->exec('BEGIN IMMEDIATE');$prefs=array_replace(push_preferences($db,$pid),$values);
        sql($db,'UPDATE push_settings SET enabled=?,challenges=?,duelResults=?,tournamentPrizes=?,friendsTournaments=? WHERE player_id=?',array_merge(array_map(fn($key)=>(int)$prefs[$key],array_merge(['enabled'],PUSH_KINDS)),[$pid]));
        if(!$prefs['enabled'])sql($db,'UPDATE push_devices SET enabled=0 WHERE player_id=?',[$pid]);
        foreach(PUSH_KINDS as $kind)if(!$prefs['enabled'] || !$prefs[$kind])sql($db,'UPDATE push_jobs SET status="cancelled" WHERE player_id=? AND kind=? AND status="pending"',[$pid,$kind]);
        $db->exec('COMMIT');out(['preferences'=>$prefs,'delivery'=>push_ready($config)]);
    }
    if($route!=='notification-device')return;
    $install=$body['installation'] ?? ''; $platform=$body['platform'] ?? ''; $enabled=$body['enabled'] ?? false;
    if(!is_string($install) || !preg_match('/^[a-fA-F0-9-]{32,64}$/D',$install) || !in_array($platform,['ios','android'],true) || !is_bool($enabled))fail('Invalid notification device');
    $id=hash('sha256',$pid.':'.$install);
    if(!$enabled) {
        sql($db,'UPDATE push_devices SET enabled=0,updated=? WHERE id=? AND player_id=?',[time(),$id,$pid]);
        sql($db,'UPDATE push_jobs SET status="cancelled" WHERE device_id=? AND status="pending"',[$id]);out(['ok'=>true]);
    }
    $token=$body['token'] ?? ''; $environment=$platform==='ios' ? ($body['environment'] ?? 'production'):'production';
    if(!is_string($token) || !in_array($environment,['production','sandbox'],true) || ($platform==='ios' ? !preg_match('/^[a-fA-F0-9]{64,512}$/D',$token):!preg_match('/^[a-zA-Z0-9:_.~-]{32,4096}$/D',$token)))fail('Invalid push token');
    if($platform==='ios')$token=strtolower($token);
    $db->exec('BEGIN IMMEDIATE');$prefs=push_preferences($db,$pid);
    if(!$prefs['enabled']){$db->exec('ROLLBACK');fail('Enable notifications in your preferences first',409);}
    if(!sql($db,'SELECT 1 FROM push_devices WHERE id=?',[$id])->fetch() && (int)sql($db,'SELECT COUNT(*) FROM push_devices WHERE player_id=?',[$pid])->fetchColumn()>=5){$db->exec('ROLLBACK');fail('Too many notification devices',409);}
    // A physical token may only belong to one installation/account at a time.
    sql($db,'DELETE FROM push_devices WHERE platform=? AND environment=? AND token=? AND id<>?',[$platform,$environment,$token,$id]);
    sql($db,'INSERT INTO push_devices VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET token=excluded.token,environment=excluded.environment,enabled=1,updated=excluded.updated',[$id,$pid,$platform,$environment,$token,1,time()]);
    $db->exec('COMMIT');out(['ok'=>true]);
}
function push_enqueue(PDO $db,string $pid,string $event,string $kind,string $title,string $body,array $payload,?string $actor=null,int $ttl=86400):void {
    if(!in_array($kind,PUSH_KINDS,true))throw new InvalidArgumentException('Unknown notification type');
    if(!sql($db,'SELECT 1 FROM players WHERE id=?',[$pid])->fetch())return;
    $pref=push_preferences($db,$pid);if(!$pref['enabled'] || !$pref[$kind])return;
    if($actor && blocked($db,$pid,$actor))return;
    foreach(sql($db,'SELECT id FROM push_devices WHERE player_id=? AND enabled=1',[$pid])->fetchAll() as $device) {
        $id=hash('sha256',$device['id'].':'.$event);
        sql($db,'INSERT OR IGNORE INTO push_jobs(id,player_id,device_id,event_key,kind,actor,title,body,payload,due,created,expires) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',[$id,$pid,$device['id'],$event,$kind,$actor,$title,$body,json_encode($payload+['kind'=>$kind,'notificationID'=>$id]),time(),time(),time()+$ttl]);
    }
}
function push_cancel_between(PDO $db,string $a,string $b):void {
    sql($db,'UPDATE push_jobs SET status="cancelled" WHERE status="pending" AND ((player_id=? AND actor=?) OR (player_id=? AND actor=?))',[$a,$b,$b,$a]);
}
function push_b64(string $s):string {return rtrim(strtr(base64_encode($s),'+/','-_'),'=');}
function push_jwt(array $claims,string $key,string $algorithm,?string $kid=null):string {
    $header=['alg'=>$algorithm,'typ'=>'JWT'];if($kid)$header['kid']=$kid;
    $base=push_b64(json_encode($header)).'.'.push_b64(json_encode($claims));
    if(!openssl_sign($base,$signature,$key,OPENSSL_ALGO_SHA256))throw new RuntimeException('Push signing failed');
    if($algorithm==='ES256') {
        // OpenSSL emits an ASN.1 sequence; JOSE requires fixed-width R and S.
        $offset=2;if((ord($signature[1])&0x80)!==0)$offset+=ord($signature[1])&0x7f;
        if(ord($signature[$offset++])!==2)throw new RuntimeException('Invalid APNs signature');
        $n=ord($signature[$offset++]);$r=substr($signature,$offset,$n);$offset+=$n;
        if(ord($signature[$offset++])!==2)throw new RuntimeException('Invalid APNs signature');
        $n=ord($signature[$offset++]);$s=substr($signature,$offset,$n);
        $signature=str_pad(ltrim($r,"\0"),32,"\0",STR_PAD_LEFT).str_pad(ltrim($s,"\0"),32,"\0",STR_PAD_LEFT);
        if(strlen($signature)!==64)throw new RuntimeException('Invalid APNs signature length');
    }
    return $base.'.'.push_b64($signature);
}
function push_http(string $url,array $headers,array|string $body,bool $http2=false):array {
    if(!function_exists('curl_init'))throw new RuntimeException('PHP curl is required for push delivery');
    $c=curl_init($url);$retryAfter=null;
    curl_setopt_array($c,[CURLOPT_POST=>true,CURLOPT_POSTFIELDS=>is_array($body)?json_encode($body):$body,CURLOPT_HTTPHEADER=>$headers,CURLOPT_RETURNTRANSFER=>true,CURLOPT_TIMEOUT=>15,CURLOPT_CONNECTTIMEOUT=>5,CURLOPT_FOLLOWLOCATION=>false,
        CURLOPT_HEADERFUNCTION=>function($c,$line)use(&$retryAfter){if(stripos($line,'Retry-After:')===0){$v=trim(substr($line,12));$retryAfter=ctype_digit($v)?(int)$v:max(0,strtotime($v)-time());}return strlen($line);}]);
    if($http2) {
        if(!(curl_version()['features']&CURL_VERSION_HTTP2)){curl_close($c);throw new RuntimeException('APNs requires curl HTTP/2 support');}
        curl_setopt($c,CURLOPT_HTTP_VERSION,CURL_HTTP_VERSION_2_0);
    }
    $raw=curl_exec($c);$status=(int)curl_getinfo($c,CURLINFO_RESPONSE_CODE);curl_close($c);
    return ['status'=>$status,'body'=>is_string($raw)?(json_decode($raw,true)??[]):[],'retryAfter'=>$retryAfter];
}
function push_send(array $job,array $config,?callable $http=null):array {
    $http??='push_http';
    static $fcmTokens=[];$p=$config['push'] ?? [];
    if($job['platform']==='ios') {
        if(!push_ready($config)['ios'])return ['status'=>0,'reason'=>'ProviderNotConfigured'];
        $jwt=push_jwt(['iss'=>$p['apple_team_id'],'iat'=>time()-10],file_get_contents($p['apns_key_file']),'ES256',$p['apns_key_id']);
        $host=$job['environment']==='sandbox'?'api.sandbox.push.apple.com':'api.push.apple.com';
        $payload=json_decode($job['payload'],true)+['aps'=>['alert'=>['title'=>$job['title'],'body'=>$job['body']],'sound'=>'default','thread-id'=>$job['kind']]];
        $r=$http('https://'.$host.'/3/device/'.$job['token'],['authorization: bearer '.$jwt,'apns-topic: com.quizfolk.ios','apns-push-type: alert','apns-priority: 10','apns-expiration: '.$job['expires'],'apns-collapse-id: '.substr($job['id'],0,64),'content-type: application/json'],$payload,true);
        return $r+['reason'=>$r['body']['reason'] ?? 'ProviderError','invalid'=>in_array($r['body']['reason'] ?? '',['Unregistered','BadDeviceToken'],true)];
    }
    if(!push_ready($config)['android'])return ['status'=>0,'reason'=>'ProviderNotConfigured'];
    $account=json_decode(file_get_contents($p['fcm_service_account_file']),true,32,JSON_THROW_ON_ERROR);$project=$account['project_id'];
    if(!preg_match('/^[a-z][a-z0-9-]{4,62}$/D',$project))throw new RuntimeException('Invalid Firebase project');
    if(!isset($fcmTokens[$project]) || $fcmTokens[$project]['expires']<time()+60) {
        $jwt=push_jwt(['iss'=>$account['client_email'],'scope'=>'https://www.googleapis.com/auth/firebase.messaging','aud'=>'https://oauth2.googleapis.com/token','iat'=>time()-10,'exp'=>time()+3500],$account['private_key'],'RS256');
        $auth=$http('https://oauth2.googleapis.com/token',['Content-Type: application/x-www-form-urlencoded'],http_build_query(['grant_type'=>'urn:ietf:params:oauth:grant-type:jwt-bearer','assertion'=>$jwt]));
        if($auth['status']!==200 || empty($auth['body']['access_token']))return ['status'=>$auth['status'],'reason'=>'FirebaseAuthenticationFailed'];
        $fcmTokens[$project]=['value'=>$auth['body']['access_token'],'expires'=>time()+(int)($auth['body']['expires_in'] ?? 3600)];
    }
    // Data messages let the app re-check local choices and Android channels before displaying.
    $data=array_map('strval',json_decode($job['payload'],true)+['title'=>$job['title'],'body'=>$job['body']]);
    $r=$http('https://fcm.googleapis.com/v1/projects/'.$project.'/messages:send',['Authorization: Bearer '.$fcmTokens[$project]['value'],'Content-Type: application/json'],['message'=>['token'=>$job['token'],'data'=>$data,'android'=>['priority'=>'HIGH','ttl'=>max(0,$job['expires']-time()).'s','collapse_key'=>substr($job['id'],0,64)]]]);
    $invalid=false;foreach($r['body']['error']['details'] ?? [] as $detail)if(($detail['errorCode'] ?? '')==='UNREGISTERED')$invalid=true;
    return $r+['reason'=>$r['body']['error']['status'] ?? 'ProviderError','invalid'=>$invalid];
}
function push_drain(PDO $db,array $config,int $limit=50,?callable $send=null):array {
    $send??='push_send';$counts=['sent'=>0,'cancelled'=>0,'retry'=>0,'failed'=>0];
    // A crashed worker's lease expires. Network calls never hold a SQLite write lock.
    sql($db,'UPDATE push_jobs SET status="pending" WHERE status="sending" AND due<?',[time()-300]);
    foreach(sql($db,'SELECT id FROM push_jobs WHERE status="pending" AND due<=? ORDER BY created,id LIMIT ?', [time(),max(1,min(100,$limit))])->fetchAll() as $candidate) {
        $db->exec('BEGIN IMMEDIATE');
        $job=sql($db,'SELECT j.*,d.platform,d.environment,d.token,d.enabled device_enabled FROM push_jobs j JOIN push_devices d ON d.id=j.device_id WHERE j.id=? AND j.status="pending" AND j.due<=?',[$candidate['id'],time()])->fetch();
        if(!$job){$db->exec('COMMIT');continue;}
        $prefs=push_preferences($db,$job['player_id']);
        $cancel=!$job['device_enabled'] || !$prefs['enabled'] || !$prefs[$job['kind']] || $job['expires']<=time() || ($job['actor'] && blocked($db,$job['player_id'],$job['actor']));
        if(!$cancel && $job['kind']==='challenges') {
            $data=json_decode($job['payload'],true);$status=sql($db,'SELECT status FROM duels WHERE id=?',[$data['id'] ?? ''])->fetchColumn();
            $cancel=$status!=='invited';
        }
        if($cancel){sql($db,'UPDATE push_jobs SET status="cancelled" WHERE id=?',[$job['id']]);$db->exec('COMMIT');$counts['cancelled']++;continue;}
        sql($db,'UPDATE push_jobs SET status="sending",due=?,attempts=attempts+1 WHERE id=?',[time(),$job['id']]);$db->exec('COMMIT');
        try{$result=$send($job,$config);}catch(Throwable $e){$result=['status'=>0,'reason'=>'TransportError'];}
        $status=(int)$result['status'];$success=$status>=200 && $status<300;
        $retry=!$success && empty($result['invalid']) && ($status===0 || $status===401 || $status===403 || $status===429 || $status>=500) && (int)$job['attempts']<7;
        $state=$success?'sent':($retry?'pending':'failed');
        $delay=max(min(3600,30*(2**min(7,(int)$job['attempts']))),min(3600,(int)($result['retryAfter'] ?? 0)));
        sql($db,'UPDATE push_jobs SET status=?,due=?,last_error=? WHERE id=?',[$state,time()+$delay,$success?null:substr((string)($result['reason'] ?? 'ProviderError'),0,80),$job['id']]);
        if(!empty($result['invalid'])){sql($db,'UPDATE push_devices SET enabled=0 WHERE id=?',[$job['device_id']]);sql($db,'UPDATE push_jobs SET status="cancelled" WHERE device_id=? AND status="pending"',[$job['device_id']]);}
        $counts[$success?'sent':($retry?'retry':'failed')]++;
    }
    sql($db,'DELETE FROM push_jobs WHERE created<?',[time()-7*86400]);return $counts;
}
