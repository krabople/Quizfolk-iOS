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
      CREATE TABLE IF NOT EXISTS tournament_places(event_id TEXT REFERENCES tournament_events(id),player_id TEXT REFERENCES players(id) ON DELETE CASCADE,rank INTEGER NOT NULL,score INTEGER NOT NULL,streak INTEGER NOT NULL,reward INTEGER NOT NULL,PRIMARY KEY(event_id,player_id));
      CREATE TABLE IF NOT EXISTS tournament_daily_schedule(day INTEGER PRIMARY KEY,event_ids TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS question_seen(player_id TEXT REFERENCES players(id) ON DELETE CASCADE,question_id TEXT NOT NULL,topic TEXT NOT NULL,PRIMARY KEY(player_id,question_id));
      CREATE TABLE IF NOT EXISTS tournament_legacy_prize_floor(event_id TEXT PRIMARY KEY REFERENCES tournament_events(id),coins INTEGER NOT NULL);');
}
function tournament_credit(PDO $db,string $pid,string $ref,int $coins,int $tickets):void {
    sql($db,'INSERT OR IGNORE INTO tournament_wallet VALUES(?,0,0)',[$pid]);
    $s=sql($db,'INSERT OR IGNORE INTO tournament_ledger VALUES(?,?,?,?,?)',[$pid,$ref,$coins,$tickets,time()]);
    if($s->rowCount())sql($db,'UPDATE tournament_wallet SET coins=coins+?,tickets=tickets+? WHERE player_id=?',[$coins,$tickets,$pid]);
}
function tournament_wallet(PDO $db,string $pid):array {
    tournament_credit($db,$pid,'welcome',100,0);
    $w=sql($db,'SELECT coins,tickets FROM tournament_wallet WHERE player_id=?',[$pid])->fetch();
    if((int)$w['tickets']>0) {
        tournament_credit($db,$pid,'ticket-conversion-v1',(int)$w['tickets']*25,-(int)$w['tickets']);
        $w=sql($db,'SELECT coins,tickets FROM tournament_wallet WHERE player_id=?',[$pid])->fetch();
    }
    return ['coins'=>(int)$w['coins'],'tickets'=>(int)$w['tickets'],'dailyClaimed'=>(bool)sql($db,'SELECT 1 FROM tournament_ledger WHERE player_id=? AND reference=?',[$pid,'daily:'.gmdate('Y-m-d')])->fetch()];
}
function tournament_seed(PDO $db):void {
    $topics=json_decode(file_get_contents(dirname(__DIR__).'/data/categories.json'),true);$n=count($topics);$day=(int)floor(time()/86400);$start=$day*86400;
    // Preserve a small promised prize for already-entered free legacy events.
    // New tournaments always have entry coins and never receive this subsidy.
    sql($db,'INSERT OR IGNORE INTO tournament_legacy_prize_floor SELECT id,25 FROM tournament_events e WHERE settled=0 AND coins=0 AND tickets=0 AND EXISTS(SELECT 1 FROM tournament_runs r WHERE r.event_id=e.id)');
    $db->exec('UPDATE tournament_events SET coins=CASE WHEN kind="weekly" THEN 100 WHEN coins+tickets*25<25 THEN 25 ELSE coins+tickets*25 END,tickets=0 WHERE settled=0');
    if(!sql($db,'SELECT 1 FROM tournament_daily_schedule WHERE day=?',[$start])->fetch()) {
        $featured=[];
        for($i=0;$i<3;$i++) {
            $coins=25*($i+1);$tickets=0;
            // Keep the most-used existing event in each entry tier when an older
            // release has already created six. Never delete or change paid runs.
            $existing=sql($db,'SELECT e.id FROM tournament_events e WHERE kind="daily" AND starts=? AND coins=? AND tickets=? ORDER BY (SELECT COUNT(*) FROM tournament_runs r WHERE r.event_id=e.id) DESC,e.id LIMIT 1',[$start,$coins,$tickets])->fetchColumn();
            if($existing){$featured[]=$existing;continue;}
            for($j=0;$j<$n;$j++) {
                $topic=$topics[($day*3+$i+$j)%$n]['id'];$id=gmdate('Ymd').':'.$topic;
                if(!sql($db,'SELECT 1 FROM tournament_events WHERE id=?',[$id])->fetch())break;
            }
            sql($db,'INSERT INTO tournament_events(id,topic,kind,starts,ends,coins,tickets) VALUES(?,?,?,?,?,?,?)',[$id,$topic,'daily',$start,$start+86400,$coins,$tickets]);
            $featured[]=$id;
        }
        // Persist the selection so rankings/activity never change today's topics.
        sql($db,'INSERT INTO tournament_daily_schedule VALUES(?,?)',[$start,json_encode($featured)]);
    }
    $week=strtotime('monday this week 00:00 UTC');
    for($i=0;$i<3;$i++) {
        $topic=$topics[((int)floor($week/604800)*3+$i)%$n]['id'];
        sql($db,'INSERT OR IGNORE INTO tournament_events(id,topic,kind,starts,ends,coins,tickets) VALUES(?,?,?,?,?,?,?)',['week:'.gmdate('Ymd',$week).':'.$topic,$topic,'weekly',$week,$week+604800,100,0]);
    }
}
function tournament_featured(PDO $db,array $e):bool {
    if($e['kind']!=='daily')return true;
    $ids=json_decode((string)sql($db,'SELECT event_ids FROM tournament_daily_schedule WHERE day=?',[(int)$e['starts']])->fetchColumn(),true) ?? [];
    return in_array($e['id'],$ids,true);
}
function tournament_seen_ids(PDO $db,string $pid,string $topic):array {
    $seen=array_fill_keys(sql($db,'SELECT question_id FROM question_seen WHERE player_id=? AND topic=?',[$pid,$topic])->fetchAll(PDO::FETCH_COLUMN),true);
    foreach(sql($db,'SELECT r.deck,r.turn,r.preview,r.started FROM tournament_runs r JOIN tournament_events e ON e.id=r.event_id WHERE r.player_id=? AND e.topic=?',[$pid,$topic])->fetchAll() as $r) {
        $shown=(int)$r['turn']+($r['preview']!==null || $r['started']!==null ? 1:0);
        foreach(array_slice(json_decode($r['deck'],true),0,$shown) as $id)$seen[$id]=true;
    }
    foreach(sql($db,'SELECT packet,answers,preview_started,started FROM matches WHERE player_id=? AND topic=?',[$pid,$topic])->fetchAll() as $m) {
        $shown=count(json_decode($m['answers'],true))+($m['preview_started']!==null || $m['started']!==null ? 1:0);
        foreach(array_slice(json_decode($m['packet'],true),0,$shown) as $q)$seen[$q['id']]=true;
    }
    return $seen;
}
function tournament_standings(PDO $db,string $id):array {
    $rows=sql($db,'SELECT r.player_id,MAX(r.score) score FROM tournament_runs r WHERE event_id=? GROUP BY r.player_id ORDER BY score DESC,player_id',[$id])->fetchAll();$rank=0;$last=null;
    foreach($rows as $i=>&$r) {
        if($last!==(int)$r['score']){$rank=$i+1;$last=(int)$r['score'];}$r['rank']=$rank;
        $r['streak']=(int)sql($db,'SELECT MAX(streak) FROM tournament_runs WHERE event_id=? AND player_id=? AND score=?',[$id,$r['player_id'],$r['score']])->fetchColumn();
    }unset($r);return $rows;
}
function tournament_prize_pool(PDO $db,string $id):int {
    $paid=(int)sql($db,'SELECT COALESCE(SUM(-l.coins-l.tickets*25),0) FROM tournament_runs r JOIN tournament_ledger l ON l.player_id=r.player_id AND l.reference="entry:"||r.id WHERE r.event_id=?',[$id])->fetchColumn();
    $legacy=(int)sql($db,'SELECT coins FROM tournament_legacy_prize_floor WHERE event_id=?',[$id])->fetchColumn();
    return max(0,$paid,$legacy);
}
function tournament_prize(int $pool,array $rows,int $rank):int {
    $n=count($rows);$shares=$n===1 ? [100]:($n===2 ? [60,40]:[50,30,20]);
    $tied=count(array_filter($rows,fn($r)=>(int)$r['rank']===$rank));$percentage=0;
    for($slot=$rank-1;$slot<$rank-1+$tied;$slot++)$percentage+=$shares[$slot] ?? 0;
    return $tied ? (int)floor($pool*$percentage/(100*$tied)):0;
}
function tournament_settle(PDO $db):void {
    foreach(sql($db,'SELECT * FROM tournament_events WHERE settled=0 AND ends<=?',[time()])->fetchAll() as $e) {
        sql($db,'UPDATE tournament_runs SET state="closed",preview=NULL,started=NULL WHERE event_id=? AND state="playing"',[$e['id']]);
        $rows=tournament_standings($db,$e['id']);$pool=tournament_prize_pool($db,$e['id']);
        foreach($rows as $r) {
            $reward=tournament_prize($pool,$rows,(int)$r['rank']);
            sql($db,'INSERT OR IGNORE INTO tournament_places VALUES(?,?,?,?,?,?)',[$e['id'],$r['player_id'],$r['rank'],(int)$r['score'],$r['streak'],$reward]);
            if($reward)tournament_credit($db,$r['player_id'],'prize:'.$e['id'],$reward,0);
        }
        sql($db,'UPDATE tournament_events SET settled=1 WHERE id=?',[$e['id']]);
    }
}
function tournament_card(PDO $db,string $pid,array $e):array {
    $best=sql($db,'SELECT MAX(score) score,MAX(streak) streak,COUNT(*) attempts FROM tournament_runs WHERE event_id=? AND player_id=?',[$e['id'],$pid])->fetch();
    $active=sql($db,'SELECT id FROM tournament_runs WHERE event_id=? AND player_id=? AND state="playing" ORDER BY created DESC LIMIT 1',[$e['id'],$pid])->fetchColumn();
    $place=sql($db,'SELECT rank,reward FROM tournament_places WHERE event_id=? AND player_id=?',[$e['id'],$pid])->fetch();
    return ['id'=>$e['id'],'topicID'=>$e['topic'],'kind'=>$e['kind'],'starts'=>(int)$e['starts'],'ends'=>(int)$e['ends'],'coins'=>(int)$e['coins'],'tickets'=>0,'closed'=>(bool)$e['settled'],'featured'=>tournament_featured($db,$e),'prizePool'=>tournament_prize_pool($db,$e['id']),'best'=>(int)$best['score'],'streak'=>(int)$best['streak'],'attempts'=>(int)$best['attempts'],'players'=>(int)sql($db,'SELECT COUNT(DISTINCT player_id) FROM tournament_runs WHERE event_id=?',[$e['id']])->fetchColumn(),'activeRun'=>$active ?: null,'rank'=>$place ? (int)$place['rank']:null,'reward'=>$place ? (int)$place['reward']:0];
}
function tournament_question(PDO $db,array &$r):?array {
    $deck=json_decode($r['deck'],true);$turn=(int)$r['turn'];$id=$deck[$turn] ?? null;
    $qdb=new PDO('sqlite:'.dirname(__DIR__).'/data/question-bank.sqlite',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
    $topic=(string)sql($db,'SELECT topic FROM tournament_events WHERE id=?',[$r['event_id']])->fetchColumn();
    $q=$id ? json_decode((string)sql($qdb,'SELECT payload FROM questions WHERE id=? AND category_id=?',[$id,$topic])->fetchColumn(),true):null;
    if(!$q) {
        // Editorial removals must not strand a paid run. Keep the answered prefix
        // and score, discard only unavailable future IDs, then continue normally.
        $valid=array_fill_keys(sql($qdb,'SELECT id FROM questions WHERE category_id=?',[$topic])->fetchAll(PDO::FETCH_COLUMN),true);
        $pending=array_values(array_filter(array_slice($deck,$turn),fn($qid)=>isset($valid[$qid])));
        $deck=array_merge(array_slice($deck,0,$turn),$pending);$r['deck']=json_encode($deck);$r['preview']=null;$r['started']=null;
        if(!$pending)$r['state']='cleared';
        sql($db,'UPDATE tournament_runs SET deck=?,preview=NULL,started=NULL,state=? WHERE id=?',[$r['deck'],$r['state'],$r['id']]);
        if(!$pending)return null;
        $id=$pending[0];$q=json_decode((string)sql($qdb,'SELECT payload FROM questions WHERE id=?',[$id])->fetchColumn(),true);
    }
    $order=[0,1,2,3];usort($order,fn($a,$b)=>strcmp(hash('sha256',$r['id'].$id.$a),hash('sha256',$r['id'].$id.$b)));$correct=$q['correctIndex'];$a=$q['answers'];$q['answers']=array_map(fn($i)=>$a[$i],$order);$q['correctIndex']=array_search($correct,$order,true);return $q;
}
function tournament_run_reply(array $r):array {return ['id'=>$r['id'],'eventID'=>$r['event_id'],'score'=>(int)$r['score'],'streak'=>(int)$r['streak'],'turn'=>(int)$r['turn'],'state'=>$r['state']];}
function tournament_routes(string $route,PDO $db,string $pid,array $body):void {
    if(!str_starts_with($route,'tournament'))return;
    $db->exec('BEGIN IMMEDIATE');tournament_seed($db);tournament_settle($db);tournament_wallet($db,$pid);
    if($route==='tournaments') {
        $events=sql($db,'SELECT * FROM tournament_events WHERE ends>? OR id IN(SELECT event_id FROM tournament_runs WHERE player_id=?) ORDER BY settled ASC,ends DESC,id LIMIT 60',[time(),$pid])->fetchAll();
        $cards=array_map(fn($e)=>tournament_card($db,$pid,$e),$events);
        $reply=['events'=>array_values(array_filter($cards,fn($e)=>$e['featured'] || $e['attempts']>0)),'wallet'=>tournament_wallet($db,$pid)];$db->exec('COMMIT');out($reply);
    }
    if($route==='tournament-daily') {$db->exec('COMMIT');fail('Coins are now earned through the Daily Trail. Update Quizfolk and open Earn coins to see your progress.',409);}
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
        if(!tournament_featured($db,$e))fail('New entries have closed for this earlier tournament. Your existing scores are kept. Choose one of today’s three tournaments.',410);
        if((int)sql($db,'SELECT COUNT(*) FROM tournament_runs WHERE player_id=? AND created>?',[$pid,time()-3600])->fetchColumn()>=30)fail('Please wait before starting another tournament run',429);
        $w=tournament_wallet($db,$pid);
        if($w['coins']<(int)$e['coins'])fail('Not enough coins. This entry costs '.$e['coins'].' coins and your balance is '.$w['coins'].'. Open Earn coins to complete your Daily Trail.',409);
        $qdb=new PDO('sqlite:'.dirname(__DIR__).'/data/question-bank.sqlite');$ids=sql($qdb,'SELECT id FROM questions WHERE category_id=?',[$e['topic']])->fetchAll(PDO::FETCH_COLUMN);if(!$ids)fail('This topic is unavailable',410);
        $seen=tournament_seen_ids($db,$pid,$e['topic']);$fresh=[];$repeated=[];
        foreach($ids as $qid){if(isset($seen[$qid]))$repeated[]=$qid;else $fresh[]=$qid;}
        shuffle($fresh);shuffle($repeated);$ids=array_merge($fresh,$repeated);
        $id=bin2hex(random_bytes(12));sql($db,'INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,created) VALUES(?,?,?,?,?,?)',[$id,$event,$pid,$key,json_encode($ids),time()]);
        tournament_credit($db,$pid,'entry:'.$id,-(int)$e['coins'],-(int)$e['tickets']);$r=sql($db,'SELECT * FROM tournament_runs WHERE id=?',[$id])->fetch();$db->exec('COMMIT');out(tournament_run_reply($r),201);
    }
    $id=(string)($body['run'] ?? '');$r=sql($db,'SELECT * FROM tournament_runs WHERE id=? AND player_id=?',[$id,$pid])->fetch();if(!$r)fail('Tournament run not found',404);
    if($route==='tournament-end') {if($r['state']==='playing'){sql($db,'UPDATE tournament_runs SET state="ended",started=NULL,preview=NULL WHERE id=?',[$id]);$r['state']='ended';}$db->exec('COMMIT');out(tournament_run_reply($r));}
    if($route==='tournament-answer' && isset($body['turn']) && is_int($body['turn']) && $body['turn']===(int)$r['turn']-1 && $r['last_reply']){$cached=json_decode($r['last_reply'],true);$db->exec('COMMIT');out($cached);}
    if($r['state']!=='playing'){$db->exec('COMMIT');out(tournament_run_reply($r));}
    $previousDeck=$r['deck'];$q=tournament_question($db,$r);
    if(!$q){$db->exec('COMMIT');out(tournament_run_reply($r));}
    if($route==='tournament-answer' && ($r['deck']!==$previousDeck || ($r['started']===null && $r['preview']===null && ($body['turn'] ?? null)===(int)$r['turn']))){$db->exec('COMMIT');out(tournament_run_reply($r)+['questionChanged'=>true]);}
    if($route==='tournament-round' || $route==='tournament-reveal') {
        sql($db,'INSERT OR IGNORE INTO question_seen VALUES(?,?,?)',[$pid,$q['id'],$q['categoryID']]);
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
