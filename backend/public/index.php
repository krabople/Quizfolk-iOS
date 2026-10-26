<?php
declare(strict_types=1);
// Only this directory is public. Keep state, bank and configuration outside the document root.
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: no-referrer');
ini_set('display_errors','0');
function out(array $data,int $status=200):never {http_response_code($status);echo json_encode($data,JSON_UNESCAPED_UNICODE|JSON_THROW_ON_ERROR);exit;}
function fail(string $message,int $status=400):never {out(['error'=>$message],$status);}
function points(bool $correct,float $elapsed,int $round):int {return !$correct || $elapsed<0 || $elapsed>=10 ? 0:(20-(int)floor($elapsed))*($round===6 ? 2:1);}
function sql(PDO $db,string $query,array $args=[]):PDOStatement {$s=$db->prepare($query);$s->execute($args);return $s;}
try {
    $configFile=dirname(__DIR__).'/config.php';
    $config=is_file($configFile) ? require $configFile:[];
    $state=$config['state_dir'] ?? getenv('QUIZFOLK_STATE_DIR') ?: dirname(__DIR__).'/private';
    if(!is_dir($state) && !mkdir($state,0700,true)) throw new RuntimeException('Cannot create state directory');
    $db=new PDO('sqlite:'.$state.'/quizfolk.sqlite',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
    $db->exec('PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000; PRAGMA foreign_keys=ON');
    $db->exec('CREATE TABLE IF NOT EXISTS players(id TEXT PRIMARY KEY, token_hash TEXT UNIQUE NOT NULL,name TEXT NOT NULL,created INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS matches(id TEXT PRIMARY KEY,player_id TEXT NOT NULL,topic TEXT NOT NULL,kind TEXT NOT NULL,opponent TEXT NOT NULL,opponent_match TEXT,packet TEXT NOT NULL,opponent_points TEXT NOT NULL,answers TEXT NOT NULL DEFAULT "[]",started REAL,score INTEGER NOT NULL DEFAULT 0,opponent_score INTEGER NOT NULL DEFAULT 0,completed INTEGER,created INTEGER NOT NULL,FOREIGN KEY(player_id) REFERENCES players(id) ON DELETE CASCADE);
      CREATE INDEX IF NOT EXISTS match_player ON matches(player_id,created);
      CREATE INDEX IF NOT EXISTS match_replay ON matches(topic,completed);
      CREATE TABLE IF NOT EXISTS limits(bucket TEXT PRIMARY KEY,window INTEGER NOT NULL,count INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS reports(id TEXT PRIMARY KEY,player_id TEXT NOT NULL,question_id TEXT NOT NULL,reason TEXT NOT NULL,created INTEGER NOT NULL);');
    $route=(string)($_GET['r'] ?? 'health');$method=$_SERVER['REQUEST_METHOD'];
    if((int)($_SERVER['CONTENT_LENGTH'] ?? 0)>8192) fail('Request is too large',413);
    $raw=file_get_contents('php://input');$body=$raw==='' ? []:json_decode($raw,true,32,JSON_THROW_ON_ERROR);
    if(!is_array($body)) fail('Expected a JSON object');
    $readRoutes=['health','categories','profile','leaderboard'];
    if(!in_array($route,$readRoutes,true) && $method!=='POST') fail('Use POST',405);
    if($route==='health') out(['ok'=>true,'version'=>'0.1.0']);
    if($route==='categories') out(['categories'=>json_decode(file_get_contents(dirname(__DIR__,2).'/data/categories.json'),true,512,JSON_THROW_ON_ERROR)]);
    $ipHash=hash('sha256',(string)($_SERVER['REMOTE_ADDR'] ?? 'unknown'));
    $bucket=($route==='register' ? 'register:':'request:').$ipHash;
    $window=(int)floor(time()/3600);$maximum=$route==='register' ? 10:3000;
    sql($db,'INSERT INTO limits(bucket,window,count) VALUES(?,?,1) ON CONFLICT(bucket) DO UPDATE SET count=CASE WHEN window=excluded.window THEN count+1 ELSE 1 END,window=excluded.window',[$bucket,$window]);
    $limit=sql($db,'SELECT count FROM limits WHERE bucket=?',[$bucket])->fetch();
    if((int)$limit['count']>$maximum) fail('Please try again later',429);
    sql($db,'DELETE FROM limits WHERE window<?',[$window-24]);
    if($route==='register') {
        $name=trim((string)($body['name'] ?? 'Quiz explorer'));
        if($name==='' || strlen($name)>96 || preg_match('/[\x00-\x1F\x7F]/u',$name)) fail('Use a display name of 1–24 characters');
        $id=bin2hex(random_bytes(12));$token=bin2hex(random_bytes(32));
        sql($db,'INSERT INTO players VALUES(?,?,?,?)',[$id,hash('sha256',$token),$name,time()]);
        out(['token'=>$token],201);
    }
    $auth=$_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '';
    if(!preg_match('/^Bearer ([a-f0-9]{64})$/D',$auth,$hit)) fail('Connect your player account first',401);
    $player=sql($db,'SELECT * FROM players WHERE token_hash=?',[hash('sha256',$hit[1])])->fetch();
    if(!$player) fail('Player key is invalid',401);
    $pid=$player['id'];
    if($route==='update-profile') {
        $name=trim((string)($body['name'] ?? ''));
        if($name==='' || strlen($name)>96 || preg_match('/[\x00-\x1F\x7F]/u',$name)) fail('Use a display name of 1–24 characters');
        sql($db,'UPDATE players SET name=? WHERE id=?',[$name,$pid]);
        out(['ok'=>true]);
    }
    if($route==='delete-account') {
        $db->beginTransaction();sql($db,'UPDATE matches SET opponent="Former player",opponent_match=NULL WHERE opponent_match IN (SELECT id FROM matches WHERE player_id=?)',[$pid]);sql($db,'DELETE FROM reports WHERE player_id=?',[$pid]);sql($db,'DELETE FROM players WHERE id=?',[$pid]);$db->commit();out(['ok'=>true]);
    }
    if($route==='profile') {
        $m=sql($db,'SELECT COUNT(*) matches,COALESCE(SUM(score>opponent_score),0) wins,COALESCE(SUM(score),0) xp FROM matches WHERE player_id=? AND completed IS NOT NULL',[$pid])->fetch();
        $answers=sql($db,'SELECT answers FROM matches WHERE player_id=? AND completed IS NOT NULL',[$pid])->fetchAll();$correct=0;$answered=0;
        foreach($answers as $a) foreach(json_decode($a['answers'],true) as $r){$answered++;if($r['correct'])$correct++;}
        out(['name'=>$player['name'],'matches'=>(int)$m['matches'],'wins'=>(int)$m['wins'],'xp'=>(int)$m['xp'],'correct'=>$correct,'answered'=>$answered]);
    }
    if($route==='leaderboard') {
        $where='m.completed IS NOT NULL';$args=[];
        if(($_GET['period'] ?? 'week')==='week') {$where.=' AND m.completed>=?';$args[]=strtotime('monday this week 00:00 UTC');}
        if(!empty($_GET['topic'])) {$where.=' AND m.topic=?';$args[]=(string)$_GET['topic'];}
        $rows=sql($db,'SELECT p.id,p.name,SUM(m.score) xp,COUNT(*) matches FROM matches m JOIN players p ON p.id=m.player_id WHERE '.$where.' GROUP BY p.id,p.name ORDER BY xp DESC,matches ASC,p.id ASC LIMIT 100',$args)->fetchAll();
        out(['entries'=>array_map(fn($r)=>['id'=>$r['id'],'name'=>$r['name'],'xp'=>(int)$r['xp'],'matches'=>(int)$r['matches']],$rows)]);
    }
    if($route==='report') {
        $reason=trim((string)($body['reason'] ?? ''));$qid=(string)($body['question'] ?? '');
        if(strlen($reason)<5 || strlen($reason)>1000 || !preg_match('/^[a-f0-9]{20}$/D',$qid)) fail('Provide a valid question and a reason of 5–1000 characters');
        sql($db,'INSERT INTO reports VALUES(?,?,?,?,?)',[bin2hex(random_bytes(12)),$pid,$qid,$reason,time()]);out(['ok'=>true]);
    }
    if($route==='match') {
        $topic=(string)($body['topic'] ?? '');
        $questionDB=new PDO('sqlite:'.dirname(__DIR__,2).'/data/question-bank.sqlite',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
        $bank=array_map(fn($row)=>json_decode($row['payload'],true,512,JSON_THROW_ON_ERROR),sql($questionDB,'SELECT payload FROM questions WHERE category_id=?',[$topic])->fetchAll());
        if(count($bank)<7) fail('Unknown topic');
        $db->exec('BEGIN IMMEDIATE');
        $active=sql($db,'SELECT COUNT(*) n FROM matches WHERE player_id=? AND created>?',[$pid,time()-3600])->fetch();
        if((int)$active['n']>=30) fail('You have reached the hourly duel limit',429);
        $replay=sql($db,'SELECT m.*,p.name FROM matches m JOIN players p ON p.id=m.player_id WHERE m.topic=? AND m.player_id<>? AND m.completed>? AND NOT EXISTS(SELECT 1 FROM matches used WHERE used.player_id=? AND used.opponent_match=m.id) ORDER BY m.completed DESC LIMIT 1',[$topic,$pid,time()-2592000,$pid])->fetch();
        if($replay) {
            $packet=json_decode($replay['packet'],true);$other=array_column(json_decode($replay['answers'],true),'points');$kind='human';$opponent=$replay['name'];
        } else {
            // Prefer unseen questions from this topic before recycling the bank.
            $previous=sql($db,'SELECT packet FROM matches WHERE player_id=? AND topic=? ORDER BY created DESC LIMIT 100',[$pid,$topic])->fetchAll();$seen=[];
            foreach($previous as $old)foreach(json_decode($old['packet'],true) as $q)$seen[$q['id']]=true;
            shuffle($bank);usort($bank,fn($a,$b)=>(int)isset($seen[$a['id']])<=>(int)isset($seen[$b['id']]));$packet=array_slice($bank,0,7);$other=[];
            foreach($packet as $i=>&$q){$indices=[0,1,2,3];shuffle($indices);$answers=array_map(fn($n)=>$q['answers'][$n],$indices);$q['correctIndex']=array_search($q['correctIndex'],$indices,true);$q['answers']=$answers;$chance=match($q['difficulty']){'easy'=>83,'hard'=>45,default=>65};$other[]=points(random_int(1,100)<=$chance,random_int(1200,9800)/1000,$i);}unset($q);
            $kind='bot';$opponent='Pip · Bot';
        }
        $id=bin2hex(random_bytes(12));
        sql($db,'INSERT INTO matches(id,player_id,topic,kind,opponent,opponent_match,packet,opponent_points,created) VALUES(?,?,?,?,?,?,?,?,?)',[$id,$pid,$topic,$kind,$opponent,$replay ? $replay['id']:null,json_encode($packet,JSON_UNESCAPED_UNICODE),json_encode($other),time()]);
        $db->exec('COMMIT');out(['id'=>$id,'kind'=>$kind,'opponent'=>$opponent],201);
    }
    if($route==='round' || $route==='answer') {
        $id=(string)($body['match'] ?? '');$db->exec('BEGIN IMMEDIATE');
        $m=sql($db,'SELECT * FROM matches WHERE id=? AND player_id=?',[$id,$pid])->fetch();
        if(!$m) fail('Match not found',404);
        if((int)$m['created']<time()-86400) fail('This duel has expired',410);
        $packet=json_decode($m['packet'],true);$answers=json_decode($m['answers'],true);$op=json_decode($m['opponent_points'],true);$round=count($answers);
        if($route==='answer' && isset($body['round']) && is_int($body['round']) && $body['round']<$round && $body['round']>=0) {
            $i=$body['round'];$r=$answers[$i];$db->exec('COMMIT');out(['points'=>$r['points'],'correctIndex'=>$packet[$i]['correctIndex'],'opponentPoints'=>$op[$i],'finished'=>$round===7,'score'=>(int)$m['score'],'opponentScore'=>(int)$m['opponent_score']]);
        }
        if($round>=7) fail('Match is complete',409);
        $q=$packet[$round];
        if($route==='round') {
            $started=$m['started']===null ? microtime(true):(float)$m['started'];
            if($m['started']===null)sql($db,'UPDATE matches SET started=? WHERE id=?',[$started,$id]);
            $db->exec('COMMIT');out(['round'=>$round,'question'=>['id'=>$q['id'],'prompt'=>$q['prompt'],'answers'=>$q['answers'],'difficulty'=>$q['difficulty'],'source'=>$q['source'] ?? 'Open Trivia Database','sourceURL'=>$q['sourceURL'] ?? 'https://opentdb.com/'],'remaining'=>max(0,10-(microtime(true)-$started))]);
        }
        if($m['started']===null || !isset($body['round']) || $body['round']!==$round || !isset($body['answer']) || !is_int($body['answer']) || $body['answer']<-1 || $body['answer']>3) fail('Invalid round or answer',409);
        $elapsed=microtime(true)-(float)$m['started'];$correct=$body['answer']===$q['correctIndex'];$score=points($correct,$elapsed,$round);
        $answers[]=['selected'=>$body['answer'],'elapsed'=>$elapsed,'correct'=>$correct && $elapsed<10,'points'=>$score];
        $total=(int)$m['score']+$score;$opTotal=(int)$m['opponent_score']+$op[$round];$finished=count($answers)===7;
        sql($db,'UPDATE matches SET answers=?,started=NULL,score=?,opponent_score=?,completed=? WHERE id=?',[json_encode($answers),$total,$opTotal,$finished ? time():null,$id]);$db->exec('COMMIT');
        out(['points'=>$score,'correctIndex'=>$q['correctIndex'],'opponentPoints'=>$op[$round],'finished'=>$finished,'score'=>$total,'opponentScore'=>$opTotal]);
    }
    fail('Endpoint not found',404);
} catch(JsonException $e) {fail('Malformed JSON',400);} catch(Throwable $e) {error_log('Quizfolk: '.$e->getMessage());fail('The quiz server is temporarily unavailable',503);}
