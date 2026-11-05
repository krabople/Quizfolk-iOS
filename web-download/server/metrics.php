<?php
declare(strict_types=1);

const QF_DOWNLOAD_FILE='Quizfolk-Android-0.3.3-12.apk';
const QF_DOWNLOAD_VERSION='0.3.3 (12)';

function qf_metrics_config():array {
    $config=require __DIR__.'/private/config.php';
    if(!is_array($config) || !preg_match('/^[a-f0-9]{64}$/D',$config['stats_key_hash'] ?? ''))throw new RuntimeException('Invalid metrics configuration');
    return $config;
}
function qf_metrics_key_valid(string $key,array $config):bool {
    return strlen($key)>=40 && strlen($key)<=128 && hash_equals($config['stats_key_hash'],hash('sha256',$key));
}
function qf_metrics_db():PDO {
    $path=__DIR__.'/private/clicks.sqlite';
    $db=new PDO('sqlite:'.$path,null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
    chmod($path,0600);
    $db->exec('PRAGMA busy_timeout=3000; PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS daily(day TEXT NOT NULL,version TEXT NOT NULL,clicks INTEGER NOT NULL DEFAULT 0,checks INTEGER NOT NULL DEFAULT 0,PRIMARY KEY(day,version));
        CREATE TABLE IF NOT EXISTS recent(id INTEGER PRIMARY KEY AUTOINCREMENT,requested_at INTEGER NOT NULL,version TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS metadata(name TEXT PRIMARY KEY,value TEXT NOT NULL);');
    $started=$db->prepare('INSERT OR IGNORE INTO metadata(name,value) VALUES(?,?)');$started->execute(['started_at',gmdate('c')]);
    return $db;
}
function qf_metrics_record(bool $verification):void {
    $db=qf_metrics_db();$now=time();$day=(new DateTimeImmutable('@'.$now))->setTimezone(new DateTimeZone('Europe/London'))->format('Y-m-d');
    $db->beginTransaction();
    $s=$db->prepare('INSERT INTO daily(day,version,clicks,checks) VALUES(?,?,?,?) ON CONFLICT(day,version) DO UPDATE SET clicks=clicks+excluded.clicks,checks=checks+excluded.checks');
    $s->execute([$day,QF_DOWNLOAD_VERSION,$verification?0:1,$verification?1:0]);
    if(!$verification) {
        $s=$db->prepare('INSERT INTO recent(requested_at,version) VALUES(?,?)');$s->execute([$now,QF_DOWNLOAD_VERSION]);
        $db->exec('DELETE FROM recent WHERE id<=(SELECT id FROM recent ORDER BY id DESC LIMIT 1 OFFSET 1000)');
    }
    $db->commit();
}
function qf_metrics_download(string $publicDirectory):never {
    header('Cache-Control: no-store, private');header('Referrer-Policy: no-referrer');header('X-Content-Type-Options: nosniff');
    $method=$_SERVER['REQUEST_METHOD'] ?? 'GET';
    if(!in_array($method,['GET','HEAD'],true)){header('Allow: GET, HEAD');http_response_code(405);exit;}
    if(!is_readable($publicDirectory.'/'.QF_DOWNLOAD_FILE)){http_response_code(404);exit('Download unavailable.');}
    $purpose=strtolower(($_SERVER['HTTP_PURPOSE'] ?? '').' '.($_SERVER['HTTP_SEC_PURPOSE'] ?? '').' '.($_SERVER['HTTP_X_PURPOSE'] ?? ''));
    $recorded='ignored';
    if($method==='GET' && empty($_SERVER['HTTP_RANGE']) && !str_contains($purpose,'prefetch') && !str_contains($purpose,'preview')) {
        try {
            $config=qf_metrics_config();
            $verification=qf_metrics_key_valid((string)($_SERVER['HTTP_X_QUIZFOLK_VERIFICATION'] ?? ''),$config);
            qf_metrics_record($verification);$recorded=$verification?'verification':'yes';
        } catch(Throwable $e) {
            // A metrics outage must never prevent downloading the app. Do not log visitor details.
            error_log('Quizfolk download counter unavailable.');$recorded='unavailable';
        }
    }
    header('X-Quizfolk-Download-Recorded: '.$recorded);
    // Apache serves the actual file, including resumable/range transfers, without recording it twice.
    header('Location: '.QF_DOWNLOAD_FILE.'?file=1',true,302);exit;
}
function qf_metrics_json(array $body,int $status=200):never {
    header('Content-Type: application/json; charset=utf-8');http_response_code($status);
    echo json_encode($body,JSON_THROW_ON_ERROR|JSON_UNESCAPED_SLASHES);exit;
}
function qf_metrics_session(array $config):void {
    $dir=__DIR__.'/private/sessions';if(!is_dir($dir) && !mkdir($dir,0700,true))throw new RuntimeException('Session storage unavailable');
    ini_set('session.use_strict_mode','1');ini_set('session.use_only_cookies','1');ini_set('session.gc_maxlifetime','1800');
    session_name('QFDownloadStats');session_save_path($dir);
    session_set_cookie_params(['lifetime'=>0,'path'=>'/quizfolk-download/','secure'=>$config['cookie_secure'] ?? true,'httponly'=>true,'samesite'=>'Strict']);
    if(!session_start())throw new RuntimeException('Session unavailable');
}
function qf_metrics_stats():array {
    $config=qf_metrics_config();qf_metrics_session($config);
    $method=$_SERVER['REQUEST_METHOD'] ?? 'GET';
    if(!in_array($method,['GET','POST'],true)){header('Allow: GET, POST');qf_metrics_json(['error'=>'Method not allowed'],405);}
    if($method==='POST') {
        if((int)($_SERVER['CONTENT_LENGTH'] ?? 0)>1024)qf_metrics_json(['error'=>'Request too large'],413);
        if(!str_starts_with(strtolower($_SERVER['CONTENT_TYPE'] ?? ''),'application/json'))qf_metrics_json(['error'=>'JSON required'],415);
        $origin=$_SERVER['HTTP_ORIGIN'] ?? '';
        if($origin!=='' && $origin!==$config['origin'])qf_metrics_json(['error'=>'Invalid origin'],403);
        $body=json_decode(file_get_contents('php://input'),true,8,JSON_THROW_ON_ERROR);
        if(($body['action'] ?? '')==='unlock') {
            if(!qf_metrics_key_valid(is_string($body['key'] ?? null)?$body['key']:'',$config))qf_metrics_json(['error'=>'Use your private stats link to open this dashboard.'],401);
            session_regenerate_id(true);$_SESSION=['key_hash'=>$config['stats_key_hash'],'expires'=>time()+1800];
        } elseif(($body['action'] ?? '')==='logout') {
            $_SESSION=[];session_write_close();qf_metrics_json(['signedOut'=>true]);
        } else qf_metrics_json(['error'=>'Unknown action'],400);
    }
    $allowed=isset($_SESSION['key_hash'],$_SESSION['expires']) && (int)$_SESSION['expires']>time() && hash_equals($config['stats_key_hash'],(string)$_SESSION['key_hash']);
    session_write_close();if(!$allowed)qf_metrics_json(['error'=>'Use your private stats link to open this dashboard.'],401);
    return $config;
}
function qf_metrics_report(array $config):array {
    $db=qf_metrics_db();$now=new DateTimeImmutable('now',new DateTimeZone('Europe/London'));
    $today=$now->format('Y-m-d');$week=$now->modify('-6 days')->format('Y-m-d');
    $s=$db->prepare('SELECT COALESCE(SUM(clicks),0) total,COALESCE(SUM(CASE WHEN day=? THEN clicks ELSE 0 END),0) today,COALESCE(SUM(CASE WHEN day>=? THEN clicks ELSE 0 END),0) week,COALESCE(SUM(checks),0) checks FROM daily');$s->execute([$today,$week]);$totals=array_map('intval',$s->fetch());
    $startedAt=$db->query("SELECT value FROM metadata WHERE name='started_at'")->fetchColumn();
    $firstDay=(new DateTimeImmutable($startedAt))->setTimezone(new DateTimeZone('Europe/London'))->format('Y-m-d');
    $days=[];$s=$db->prepare('SELECT day,SUM(clicks) clicks FROM daily WHERE day>=? GROUP BY day');$s->execute([$now->modify('-29 days')->format('Y-m-d')]);$counts=array_column($s->fetchAll(),'clicks','day');
    for($i=29;$i>=0;$i--){$day=$now->modify('-'.$i.' days')->format('Y-m-d');if($day<$firstDay)continue;$days[]=['day'=>$day,'clicks'=>(int)($counts[$day] ?? 0)];}
    $recent=$db->query('SELECT requested_at,version FROM recent ORDER BY id DESC LIMIT 100')->fetchAll();
    foreach($recent as &$row)$row['requested_at']=gmdate('c',(int)$row['requested_at']);unset($row);
    return ['totals'=>$totals,'daily'=>$days,'recent'=>$recent,'startedAt'=>$startedAt,'timezone'=>'Europe/London','generatedAt'=>gmdate('c')];
}
