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
require dirname(__DIR__).'/names.php';
require dirname(__DIR__).'/social.php';
require dirname(__DIR__).'/tournaments.php';
require dirname(__DIR__).'/economy.php';
function earned_xp(int $score,int $other):int {return $score+40+($score>$other ? 100:($score===$other ? 50:0));}
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
    ensure_unique_names($db);
    ensure_avatar_column($db);
    social_schema($db);
    economy_schema($db);
    tournament_schema($db);
    $route=(string)($_GET['r'] ?? 'health');$method=$_SERVER['REQUEST_METHOD'];
    if((int)($_SERVER['CONTENT_LENGTH'] ?? 0)>24576) fail('Request is too large',413);
    $raw=file_get_contents('php://input');$body=$raw==='' ? []:json_decode($raw,true,32,JSON_THROW_ON_ERROR);
    if(!is_array($body)) fail('Expected a JSON object');
    $readRoutes=['health','categories','profile','leaderboard','people','player','duels','activity','tournaments','tournament-board','coins','prizes'];
    if(!in_array($route,$readRoutes,true) && $method!=='POST') fail('Use POST',405);
    if($route==='health') out(['ok'=>true,'version'=>'0.3.0']);
    if($route==='categories') out(['categories'=>json_decode(file_get_contents(dirname(__DIR__,2).'/data/categories.json'),true,512,JSON_THROW_ON_ERROR)]);
    $ipHash=hash('sha256',(string)($_SERVER['REMOTE_ADDR'] ?? 'unknown'));
    $bucket=($route==='register' ? 'register:':'request:').$ipHash;
    $window=(int)floor(time()/3600);$maximum=$route==='register' ? 10:3000;
    sql($db,'INSERT INTO limits(bucket,window,count) VALUES(?,?,1) ON CONFLICT(bucket) DO UPDATE SET count=CASE WHEN window=excluded.window THEN count+1 ELSE 1 END,window=excluded.window',[$bucket,$window]);
    $limit=sql($db,'SELECT count FROM limits WHERE bucket=?',[$bucket])->fetch();
    if((int)$limit['count']>$maximum) fail('Please try again later',429);
    sql($db,'DELETE FROM limits WHERE window<?',[$window-24]);
    if($route==='register') {
        $auto=!empty($body['automaticName']) || empty($body['name']) || ($body['name'] ?? '')==='Quiz explorer';
        $name=$auto ? automatic_name():clean_name((string)$body['name']);
        $id=bin2hex(random_bytes(12));$token=bin2hex(random_bytes(32));
        for($attempt=0;$attempt<8;$attempt++) {
            try {sql($db,'INSERT INTO players(id,token_hash,name,created,name_key) VALUES(?,?,?,?,?)',[$id,hash('sha256',$token),$name,time(),name_key($name)]);out(['token'=>$token,'name'=>$name],201);}
            catch(PDOException $e){if($e->getCode()!=='23000')throw $e;if(!$auto)fail('That player name is already in use. Please choose another.',409);$name=automatic_name();}
        }
        fail('Could not reserve a player name. Please try again.',503);
    }
    $auth=$_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '';
    if(!preg_match('/^Bearer ([a-f0-9]{64})$/D',$auth,$hit)) fail('Connect your player account first',401);
    $player=sql($db,'SELECT * FROM players WHERE token_hash=?',[hash('sha256',$hit[1])])->fetch();
    if(!$player) fail('Player key is invalid',401);
    $pid=$player['id'];
    economy_routes($route,$db,$pid,$body);
    tournament_routes($route,$db,$pid,$body);
    social_routes($route,$db,$pid,$player,$body,$config);
    if($route==='update-profile') {
        if(!in_array(($_SERVER['HTTP_X_QUIZFOLK_CLIENT'] ?? ''),['2','3'],true) && ($body['name'] ?? '')==='Quiz explorer')out(['ok'=>true,'name'=>$player['name']]);
        $name=clean_name((string)($body['name'] ?? ''));
        try {sql($db,'UPDATE players SET name=?,name_key=? WHERE id=?',[$name,name_key($name),$pid]);}
        catch(PDOException $e){if($e->getCode()==='23000')fail('That player name is already in use. Please choose another.',409);throw $e;}
        sql($db,'UPDATE matches SET opponent=? WHERE opponent_match IN (SELECT id FROM matches WHERE player_id=?)',[$name,$pid]);
        out(['ok'=>true,'name'=>$name]);
    }
    if($route==='update-avatar') {
        $avatar=$body['avatar'] ?? null;
        if($avatar!==null) {
            if(!is_string($avatar) || strlen($avatar)>22000)fail('Choose a smaller profile picture.');
            $bytes=base64_decode($avatar,true);$info=$bytes===false ? false:@getimagesizefromstring($bytes);
            if(!$info || $info['mime']!=='image/jpeg' || $info[0]>256 || $info[1]>256 || $info[0]<32 || $info[1]<32 || strlen($bytes)>16384)fail('Use a JPEG profile picture between 32 and 256 pixels.');
            // Decode and re-encode when GD is available; the app also strips metadata.
            if(function_exists('imagecreatefromstring')) {
                $image=@imagecreatefromstring($bytes);if(!$image)fail('This picture could not be opened.');
                ob_start();imagejpeg($image,null,82);$bytes=ob_get_clean();imagedestroy($image);
                if(strlen($bytes)>16384)fail('Choose a smaller profile picture.');
            }
            $avatar=base64_encode($bytes);
        }
        sql($db,'UPDATE players SET avatar=? WHERE id=?',[$avatar,$pid]);out(['ok'=>true]);
    }
    if($route==='delete-account') {
        $db->beginTransaction();delete_social_player($db,$pid);sql($db,'UPDATE matches SET opponent="Former player",opponent_match=NULL WHERE opponent_match IN (SELECT id FROM matches WHERE player_id=?)',[$pid]);sql($db,'DELETE FROM reports WHERE player_id=?',[$pid]);sql($db,'DELETE FROM players WHERE id=?',[$pid]);$db->commit();out(['ok'=>true]);
    }
    if($route==='profile') {
        $m=sql($db,'SELECT COUNT(*) matches,COALESCE(SUM(score>opponent_score),0) wins,COALESCE(SUM(score+40+CASE WHEN score>opponent_score THEN 100 WHEN score=opponent_score THEN 50 ELSE 0 END),0) xp FROM matches WHERE player_id=? AND completed IS NOT NULL',[$pid])->fetch();
        $answers=sql($db,'SELECT answers FROM matches WHERE player_id=? AND completed IS NOT NULL',[$pid])->fetchAll();$correct=0;$answered=0;
        foreach($answers as $a) foreach(json_decode($a['answers'],true) as $r){$answered++;if($r['correct'])$correct++;}
        out(['id'=>$pid,'socialVersion'=>1,'name'=>$player['name'],'avatar'=>$player['avatar'],'matches'=>(int)$m['matches'],'wins'=>(int)$m['wins'],'xp'=>(int)$m['xp'],'correct'=>$correct,'answered'=>$answered]);
    }
    if($route==='leaderboard') {
        $where='m.completed IS NOT NULL AND NOT EXISTS(SELECT 1 FROM blocks b WHERE (b.player_id=? AND b.target_id=m.player_id) OR (b.player_id=m.player_id AND b.target_id=?))';$args=[$pid,$pid];
        if(($_GET['scope'] ?? '')==='following'){$where.=' AND (m.player_id=? OR EXISTS(SELECT 1 FROM follows f WHERE f.player_id=? AND f.target_id=m.player_id))';$args[]=$pid;$args[]=$pid;}
        $topic=(string)($_GET['topic'] ?? '');
        $topics=json_decode(file_get_contents(dirname(__DIR__,2).'/data/categories.json'),true,512,JSON_THROW_ON_ERROR);
        if(!in_array($topic,array_column($topics,'id'),true))fail('Choose a topic to view its league table.');
        if(($_GET['period'] ?? 'month')==='month') {$where.=' AND m.completed>=?';$args[]=strtotime(gmdate('Y-m-01').' 00:00 UTC');}
        if(($_GET['period'] ?? 'month')==='week') {$where.=' AND m.completed>=?';$args[]=strtotime('monday this week 00:00 UTC');}
        if(!empty($_GET['topic'])) {$where.=' AND m.topic=?';$args[]=(string)$_GET['topic'];}
        $rows=sql($db,'SELECT p.id,p.name,p.avatar,SUM(m.score+40+CASE WHEN m.score>m.opponent_score THEN 100 WHEN m.score=m.opponent_score THEN 50 ELSE 0 END) xp,COUNT(*) matches FROM matches m JOIN players p ON p.id=m.player_id WHERE '.$where.' GROUP BY p.id,p.name ORDER BY xp DESC,matches ASC,p.id ASC LIMIT 100',$args)->fetchAll();
        out(['entries'=>array_map(fn($r)=>['id'=>$r['id'],'name'=>$r['name'],'avatar'=>$r['avatar'],'xp'=>(int)$r['xp'],'matches'=>(int)$r['matches']],$rows)]);
    }
    if($route==='report') {
        $reason=trim((string)($body['reason'] ?? ''));$qid=(string)($body['question'] ?? '');
        if(strlen($reason)<5 || strlen($reason)>1000 || !preg_match('/^[a-f0-9]{20}$/D',$qid)) fail('Provide a valid question and a reason of 5–1000 characters');
        sql($db,'INSERT INTO reports VALUES(?,?,?,?,?)',[bin2hex(random_bytes(12)),$pid,$qid,$reason,time()]);out(['ok'=>true]);
    }
    if($route==='match') {
        $db->exec('BEGIN IMMEDIATE');$reply=create_random_match($db,$pid,(string)($body['topic'] ?? ''),$config);$db->exec('COMMIT');out($reply,201);
    }
    if($route==='round' || $route==='reveal' || $route==='answer') {
        $id=(string)($body['match'] ?? '');$db->exec('BEGIN IMMEDIATE');
        $m=sql($db,'SELECT * FROM matches WHERE id=? AND player_id=?',[$id,$pid])->fetch();
        if(!$m) fail('Match not found',404);
        if((int)$m['created']<(int)($config['minimum_replay_created'] ?? 0)) fail('The question bank has been updated. Please start a new duel.',410);
        if($m['duel_id']) {$duel=sql($db,'SELECT * FROM duels WHERE id=?',[$m['duel_id']])->fetch();if(!$duel || !in_array($duel['status'],['invited','accepted','complete'],true))fail('This challenge is no longer available',410);}
        if((int)$m['created']<time()-($m['duel_id'] ? 1209600:86400)) fail('This duel has expired',410);
        $packet=json_decode($m['packet'],true);$answers=json_decode($m['answers'],true);$op=json_decode($m['opponent_points'],true);$round=count($answers);
        if($round<7 && !packet_is_current($packet))fail('A question in this duel has been corrected or withdrawn. Please start a new duel. Your completed results are kept.',410);
        if($route==='answer' && isset($body['round']) && is_int($body['round']) && $body['round']<$round && $body['round']>=0) {
            $i=$body['round'];$r=$answers[$i];$db->exec('COMMIT');out(['points'=>$r['points'],'correctIndex'=>$packet[$i]['correctIndex'],'opponentPoints'=>$op[$i],'finished'=>$round===7,'score'=>(int)$m['score'],'opponentScore'=>(int)$m['opponent_score'],'pending'=>$m['duel_id']!==null && $m['completed']===null]);
        }
        if($round>=7) fail('Match is complete',409);
        $q=$packet[$round];
        if($route==='round' || $route==='reveal') {
            $reading=($_SERVER['HTTP_X_QUIZFOLK_CLIENT'] ?? '')==='3';$preview=$m['preview_started']===null ? microtime(true):(float)$m['preview_started'];
            if($reading && $m['started']===null) {
                if($m['preview_started']===null)sql($db,'UPDATE matches SET preview_started=? WHERE id=?',[$preview,$id]);
                $left=max(0,2-(microtime(true)-$preview));
                if($route==='round' || $left>0) {$db->exec('COMMIT');out(['round'=>$round,'question'=>['id'=>$q['id'],'prompt'=>$q['prompt'],'answers'=>[],'difficulty'=>$q['difficulty'],'source'=>$q['source'] ?? 'Open trivia contributors','sourceURL'=>$q['sourceURL'] ?? null],'remaining'=>10,'readingRemaining'=>$left,'phase'=>'reading']);}
            }
            $started=$m['started']===null ? microtime(true):(float)$m['started'];
            if($m['started']===null)sql($db,'UPDATE matches SET started=? WHERE id=?',[$started,$id]);
            $db->exec('COMMIT');out(['round'=>$round,'question'=>['id'=>$q['id'],'prompt'=>$q['prompt'],'answers'=>$q['answers'],'difficulty'=>$q['difficulty'],'source'=>$q['source'] ?? 'Open Trivia Database','sourceURL'=>$q['sourceURL'] ?? 'https://opentdb.com/'],'remaining'=>max(0,10-(microtime(true)-$started)),'readingRemaining'=>0,'phase'=>'answer']);
        }
        if($m['started']===null || !isset($body['round']) || $body['round']!==$round || !isset($body['answer']) || !is_int($body['answer']) || $body['answer']<-1 || $body['answer']>3) fail('Invalid round or answer',409);
        $elapsed=microtime(true)-(float)$m['started'];$correct=$body['answer']===$q['correctIndex'];$score=points($correct,$elapsed,$round);
        $answers[]=['selected'=>$body['answer'],'elapsed'=>$elapsed,'correct'=>$correct && $elapsed<10,'points'=>$score];
        $total=(int)$m['score']+$score;$opTotal=(int)$m['opponent_score']+$op[$round];$finished=count($answers)===7;
        sql($db,'UPDATE matches SET answers=?,started=NULL,preview_started=NULL,score=?,opponent_score=?,completed=? WHERE id=?',[json_encode($answers),$total,$opTotal,$finished && !$m['duel_id'] ? time():null,$id]);
        if($finished) {
            sql($db,'UPDATE matches SET own_finished=COALESCE(own_finished,?) WHERE id=?',[time(),$id]);
            coin_trail_award($db,sql($db,'SELECT * FROM matches WHERE id=?',[$id])->fetch());
        }
        if($m['duel_id'] && $finished)settle_duel($db,$m['duel_id']);
        $latest=sql($db,'SELECT * FROM matches WHERE id=?',[$id])->fetch();$opTotal=(int)$latest['opponent_score'];$op=json_decode($latest['opponent_points'],true);$pending=$m['duel_id']!==null && $latest['completed']===null;
        $db->exec('COMMIT');
        out(['points'=>$score,'correctIndex'=>$q['correctIndex'],'opponentPoints'=>$op[$round],'finished'=>$finished,'score'=>$total,'opponentScore'=>$opTotal,'pending'=>$pending]);
    }
    fail('Endpoint not found',404);
} catch(JsonException $e) {fail('Malformed JSON',400);} catch(Throwable $e) {error_log('Quizfolk: '.$e->getMessage());fail('The quiz server is temporarily unavailable',503);}
