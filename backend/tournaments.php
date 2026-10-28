<?php
declare(strict_types=1);

// Survival tournaments use their own runs. They can never become duel replays,
// fabricated head-to-head wins, or an overall player level.
function tournament_schema(PDO $db):void {
    $db->exec('CREATE TABLE IF NOT EXISTS tournament_events(id TEXT PRIMARY KEY,topic TEXT NOT NULL,kind TEXT NOT NULL,starts INTEGER NOT NULL,ends INTEGER NOT NULL,coins INTEGER NOT NULL,tickets INTEGER NOT NULL,settled INTEGER NOT NULL DEFAULT 0);
      CREATE TABLE IF NOT EXISTS tournament_wallet(player_id TEXT PRIMARY KEY REFERENCES players(id) ON DELETE CASCADE,coins INTEGER NOT NULL CHECK(coins>=0),tickets INTEGER NOT NULL CHECK(tickets>=0));
      CREATE TABLE IF NOT EXISTS tournament_ledger(player_id TEXT REFERENCES players(id) ON DELETE CASCADE,reference TEXT NOT NULL,coins INTEGER NOT NULL,tickets INTEGER NOT NULL,created INTEGER NOT NULL,PRIMARY KEY(player_id,reference));
      CREATE TABLE IF NOT EXISTS tournament_runs(id TEXT PRIMARY KEY,event_id TEXT NOT NULL REFERENCES tournament_events(id),player_id TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,request_key TEXT NOT NULL UNIQUE,deck TEXT NOT NULL,turn INTEGER NOT NULL DEFAULT 0,score INTEGER NOT NULL DEFAULT 0,streak INTEGER NOT NULL DEFAULT 0,state TEXT NOT NULL DEFAULT "playing",preview REAL,started REAL,last_reply TEXT,created INTEGER NOT NULL);
      CREATE INDEX IF NOT EXISTS tournament_run_player ON tournament_runs(player_id,event_id);
      CREATE TABLE IF NOT EXISTS tournament_places(event_id TEXT REFERENCES tournament_events(id),player_id TEXT REFERENCES players(id) ON DELETE CASCADE,rank INTEGER NOT NULL,score INTEGER NOT NULL,streak INTEGER NOT NULL,reward INTEGER NOT NULL,PRIMARY KEY(event_id,player_id));');
}
function tournament_credit(PDO $db,string $pid,string $ref,int $coins,int $tickets):void {
    sql($db,'INSERT OR IGNORE INTO tournament_wallet VALUES(?,0,0)',[$pid]);
    $s=sql($db,'INSERT OR IGNORE INTO tournament_ledger VALUES(?,?,?,?,?)',[$pid,$ref,$coins,$tickets,time()]);
    if($s->rowCount())sql($db,'UPDATE tournament_wallet SET coins=coins+?,tickets=tickets+? WHERE player_id=?',[$coins,$tickets,$pid]);
}
function tournament_wallet(PDO $db,string $pid):array {
    tournament_credit($db,$pid,'welcome',100,3);
    $w=sql($db,'SELECT coins,tickets FROM tournament_wallet WHERE player_id=?',[$pid])->fetch();
    return ['coins'=>(int)$w['coins'],'tickets'=>(int)$w['tickets'],'dailyClaimed'=>(bool)sql($db,'SELECT 1 FROM tournament_ledger WHERE player_id=? AND reference=?',[$pid,'daily:'.gmdate('Y-m-d')])->fetch()];
}
function tournament_seed(PDO $db):void {
    $topics=json_decode(file_get_contents(dirname(__DIR__).'/data/categories.json'),true);$n=count($topics);$day=(int)floor(time()/86400);$start=$day*86400;
    for($i=0;$i<6;$i++) {
        $topic=$topics[($day*6+$i)%$n]['id'];$tier=$i%3;$id=gmdate('Ymd').':'.$topic;
        sql($db,'INSERT OR IGNORE INTO tournament_events(id,topic,kind,starts,ends,coins,tickets) VALUES(?,?,?,?,?,?,?)',[$id,$topic,'daily',$start,$start+86400,$tier===1?25:0,$tier===2?1:0]);
    }
    $week=strtotime('monday this week 00:00 UTC');
    for($i=0;$i<3;$i++) {
        $topic=$topics[((int)floor($week/604800)*3+$i)%$n]['id'];
        sql($db,'INSERT OR IGNORE INTO tournament_events(id,topic,kind,starts,ends,coins,tickets) VALUES(?,?,?,?,?,?,?)',['week:'.gmdate('Ymd',$week).':'.$topic,$topic,'weekly',$week,$week+604800,0,2]);
    }
}
function tournament_standings(PDO $db,string $id):array {
    $rows=sql($db,'SELECT r.player_id,MAX(r.score) score FROM tournament_runs r WHERE event_id=? GROUP BY r.player_id ORDER BY score DESC,player_id',[$id])->fetchAll();$rank=0;$last=null;
    foreach($rows as $i=>&$r) {
        if($last!==(int)$r['score']){$rank=$i+1;$last=(int)$r['score'];}$r['rank']=$rank;
        $r['streak']=(int)sql($db,'SELECT MAX(streak) FROM tournament_runs WHERE event_id=? AND player_id=? AND score=?',[$id,$r['player_id'],$r['score']])->fetchColumn();
    }unset($r);return $rows;
}
function tournament_settle(PDO $db):void {
    foreach(sql($db,'SELECT * FROM tournament_events WHERE settled=0 AND ends<=?',[time()])->fetchAll() as $e) {
        sql($db,'UPDATE tournament_runs SET state="closed",preview=NULL,started=NULL WHERE event_id=? AND state="playing"',[$e['id']]);
        $rows=tournament_standings($db,$e['id']);$competitive=count($rows)>=2;
        foreach($rows as $r) {
            $reward=$competitive && (int)$r['score']>0 ? ([1=>500,2=>250,3=>100][$r['rank']] ?? 0):0;
            sql($db,'INSERT OR IGNORE INTO tournament_places VALUES(?,?,?,?,?,?)',[$e['id'],$r['player_id'],$r['rank'],(int)$r['score'],$r['streak'],$reward]);
            if($reward)tournament_credit($db,$r['player_id'],'prize:'.$e['id'],$reward,0);
            if(!$competitive) {
                $attempts=(int)sql($db,'SELECT COUNT(*) FROM tournament_runs WHERE event_id=? AND player_id=?',[$e['id'],$r['player_id']])->fetchColumn();
                tournament_credit($db,$r['player_id'],'refund:'.$e['id'],$attempts*(int)$e['coins'],$attempts*(int)$e['tickets']);
            }
        }
        sql($db,'UPDATE tournament_events SET settled=1 WHERE id=?',[$e['id']]);
    }
}
function tournament_card(PDO $db,string $pid,array $e):array {
    $best=sql($db,'SELECT MAX(score) score,MAX(streak) streak,COUNT(*) attempts FROM tournament_runs WHERE event_id=? AND player_id=?',[$e['id'],$pid])->fetch();
    $active=sql($db,'SELECT id FROM tournament_runs WHERE event_id=? AND player_id=? AND state="playing" ORDER BY created DESC LIMIT 1',[$e['id'],$pid])->fetchColumn();
    $place=sql($db,'SELECT rank,reward FROM tournament_places WHERE event_id=? AND player_id=?',[$e['id'],$pid])->fetch();
    return ['id'=>$e['id'],'topicID'=>$e['topic'],'kind'=>$e['kind'],'starts'=>(int)$e['starts'],'ends'=>(int)$e['ends'],'coins'=>(int)$e['coins'],'tickets'=>(int)$e['tickets'],'closed'=>(bool)$e['settled'],'best'=>(int)$best['score'],'streak'=>(int)$best['streak'],'attempts'=>(int)$best['attempts'],'players'=>(int)sql($db,'SELECT COUNT(DISTINCT player_id) FROM tournament_runs WHERE event_id=?',[$e['id']])->fetchColumn(),'activeRun'=>$active ?: null,'rank'=>$place ? (int)$place['rank']:null,'reward'=>$place ? (int)$place['reward']:0];
}
function tournament_question(array $r):array {
    $deck=json_decode($r['deck'],true);$id=$deck[(int)$r['turn']] ?? null;if(!$id)fail('This run has no more questions',409);
    $qdb=new PDO('sqlite:'.dirname(__DIR__).'/data/question-bank.sqlite',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
    $q=json_decode((string)sql($qdb,'SELECT payload FROM questions WHERE id=?',[$id])->fetchColumn(),true);if(!$q)fail('This question is no longer available. End this run to save your score.',410);
    $order=[0,1,2,3];usort($order,fn($a,$b)=>strcmp(hash('sha256',$r['id'].$id.$a),hash('sha256',$r['id'].$id.$b)));$correct=$q['correctIndex'];$a=$q['answers'];$q['answers']=array_map(fn($i)=>$a[$i],$order);$q['correctIndex']=array_search($correct,$order,true);return $q;
}
function tournament_run_reply(array $r):array {return ['id'=>$r['id'],'eventID'=>$r['event_id'],'score'=>(int)$r['score'],'streak'=>(int)$r['streak'],'turn'=>(int)$r['turn'],'state'=>$r['state']];}
function tournament_routes(string $route,PDO $db,string $pid,array $body):void {
    if(!str_starts_with($route,'tournament'))return;
    $db->exec('BEGIN IMMEDIATE');tournament_seed($db);tournament_settle($db);tournament_wallet($db,$pid);
    if($route==='tournaments') {
        $events=sql($db,'SELECT * FROM tournament_events WHERE ends>? OR id IN(SELECT event_id FROM tournament_runs WHERE player_id=?) ORDER BY settled ASC,ends DESC,id LIMIT 60',[time(),$pid])->fetchAll();
        $reply=['events'=>array_map(fn($e)=>tournament_card($db,$pid,$e),$events),'wallet'=>tournament_wallet($db,$pid)];$db->exec('COMMIT');out($reply);
    }
    if($route==='tournament-daily') {tournament_credit($db,$pid,'daily:'.gmdate('Y-m-d'),50,2);$w=tournament_wallet($db,$pid);$db->exec('COMMIT');out($w);}
    if($route==='tournament-board') {
        $id=(string)($_GET['event'] ?? '');$e=sql($db,'SELECT * FROM tournament_events WHERE id=?',[$id])->fetch();if(!$e)fail('Tournament not found',404);
        $rows=$e['settled'] ? sql($db,'SELECT player_id,rank,score,streak,reward FROM tournament_places WHERE event_id=? ORDER BY rank,player_id',[$id])->fetchAll():tournament_standings($db,$id);
        $all=[];foreach($rows as $r) {if(blocked($db,$pid,$r['player_id']))continue;$p=sql($db,'SELECT name,avatar FROM players WHERE id=?',[$r['player_id']])->fetch();if($p)$all[]=['id'=>$r['player_id'],'name'=>$p['name'],'avatar'=>$p['avatar'],'rank'=>(int)$r['rank'],'score'=>(int)$r['score'],'streak'=>(int)$r['streak'],'reward'=>(int)($r['reward'] ?? 0)];}
        $reply=['event'=>tournament_card($db,$pid,$e),'entries'=>array_slice($all,0,100),'own'=>array_values(array_filter($all,fn($r)=>$r['id']===$pid)),'wallet'=>tournament_wallet($db,$pid)];$db->exec('COMMIT');out($reply);
    }
    if($route==='tournament-enter') {
        $event=(string)($body['event'] ?? '');$request=(string)($body['requestID'] ?? '');if(!preg_match('/^[a-zA-Z0-9-]{16,64}$/D',$request))fail('Invalid entry request');$key=$pid.':'.$request;
        $old=sql($db,'SELECT * FROM tournament_runs WHERE request_key=?',[$key])->fetch();if($old){if($old['event_id']!==$event)fail('This entry request was already used',409);$db->exec('COMMIT');out(tournament_run_reply($old));}
        $e=sql($db,'SELECT * FROM tournament_events WHERE id=? AND starts<=? AND ends>?',[$event,time(),time()+30])->fetch();if(!$e)fail('Entries have closed. Choose another tournament.',410);
        $active=sql($db,'SELECT * FROM tournament_runs WHERE event_id=? AND player_id=? AND state="playing"',[$event,$pid])->fetch();if($active){$db->exec('COMMIT');out(tournament_run_reply($active));}
        if((int)sql($db,'SELECT COUNT(*) FROM tournament_runs WHERE player_id=? AND created>?',[$pid,time()-3600])->fetchColumn()>=30)fail('Please wait before starting another tournament run',429);
        $w=tournament_wallet($db,$pid);if($w['coins']<(int)$e['coins'] || $w['tickets']<(int)$e['tickets'])fail('You need more coins or tickets. Claim your free daily supply.',409);
        $qdb=new PDO('sqlite:'.dirname(__DIR__).'/data/question-bank.sqlite');$ids=sql($qdb,'SELECT id FROM questions WHERE category_id=?',[$e['topic']])->fetchAll(PDO::FETCH_COLUMN);shuffle($ids);if(!$ids)fail('This topic is unavailable',410);
        $id=bin2hex(random_bytes(12));sql($db,'INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,created) VALUES(?,?,?,?,?,?)',[$id,$event,$pid,$key,json_encode($ids),time()]);
        tournament_credit($db,$pid,'entry:'.$id,-(int)$e['coins'],-(int)$e['tickets']);$r=sql($db,'SELECT * FROM tournament_runs WHERE id=?',[$id])->fetch();$db->exec('COMMIT');out(tournament_run_reply($r),201);
    }
    $id=(string)($body['run'] ?? '');$r=sql($db,'SELECT * FROM tournament_runs WHERE id=? AND player_id=?',[$id,$pid])->fetch();if(!$r)fail('Tournament run not found',404);
    if($route==='tournament-end') {if($r['state']==='playing'){sql($db,'UPDATE tournament_runs SET state="ended",started=NULL,preview=NULL WHERE id=?',[$id]);$r['state']='ended';}$db->exec('COMMIT');out(tournament_run_reply($r));}
    if($route==='tournament-answer' && isset($body['turn']) && is_int($body['turn']) && $body['turn']===(int)$r['turn']-1 && $r['last_reply']){$cached=json_decode($r['last_reply'],true);$db->exec('COMMIT');out($cached);}
    if($r['state']!=='playing'){$db->exec('COMMIT');out(tournament_run_reply($r));}
    $q=tournament_question($r);
    if($route==='tournament-round' || $route==='tournament-reveal') {
        $preview=$r['preview']===null ? microtime(true):(float)$r['preview'];$left=max(0,2-(microtime(true)-$preview));$reading=$r['started']===null && ($route==='tournament-round' || $left>0);
        if($r['preview']===null)sql($db,'UPDATE tournament_runs SET preview=? WHERE id=?',[$preview,$id]);
        if(!$reading && $r['started']===null){$r['started']=microtime(true);sql($db,'UPDATE tournament_runs SET started=? WHERE id=?',[$r['started'],$id]);}
        unset($q['correctIndex']);if($reading)$q['answers']=[];
        $reply=tournament_run_reply($r)+['question'=>$q,'remaining'=>$reading ? 10:max(0,10-(microtime(true)-(float)$r['started'])),'readingRemaining'=>$reading ? $left:0,'phase'=>$reading?'reading':'answer'];$db->exec('COMMIT');out($reply);
    }
    if($route==='tournament-answer') {
        $answer=$body['answer'] ?? null;if(!is_int($answer) || $answer<-1 || $answer>3 || !isset($body['turn']) || $body['turn']!==(int)$r['turn'] || $r['started']===null)fail('Invalid tournament answer',409);
        $elapsed=microtime(true)-(float)$r['started'];$right=$answer===$q['correctIndex'] && $elapsed>=0 && $elapsed<10;$points=points($right,$elapsed,0);
        $r['score']=(int)$r['score']+$points;$r['streak']=(int)$r['streak']+($right?1:0);$r['turn']=(int)$r['turn']+1;
        if(!$right || $r['turn']>=count(json_decode($r['deck'],true)))$r['state']=$right?'cleared':'finished';
        $reply=tournament_run_reply($r)+['correctIndex'=>$q['correctIndex'],'points'=>$points,'correct'=>$right];
        sql($db,'UPDATE tournament_runs SET turn=?,score=?,streak=?,state=?,preview=NULL,started=NULL,last_reply=? WHERE id=?',[$r['turn'],$r['score'],$r['streak'],$r['state'],json_encode($reply),$id]);$db->exec('COMMIT');out($reply);
    }
    fail('Tournament endpoint not found',404);
}
