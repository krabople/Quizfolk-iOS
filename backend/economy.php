<?php
declare(strict_types=1);

// Coins are earned from server-scored play, not from client claims or logins.
function economy_schema(PDO $db):void {
    $columns=array_column($db->query('PRAGMA table_info(matches)')->fetchAll(),'name');
    if(!in_array('own_finished',$columns,true)) {
        $file=$db->query('PRAGMA database_list')->fetch()['file'];$backup=$file.'.before-coins-v1.sqlite';
        if($file && !is_file($backup) && (int)$db->query('SELECT COUNT(*) FROM players')->fetchColumn()>0)$db->exec('VACUUM INTO '.$db->quote($backup));
        $db->exec('ALTER TABLE matches ADD COLUMN own_finished INTEGER');
    }
    $db->exec('CREATE TABLE IF NOT EXISTS coin_trail_stamps(player_id TEXT REFERENCES players(id) ON DELETE CASCADE,day INTEGER NOT NULL,topic TEXT NOT NULL,match_id TEXT NOT NULL UNIQUE,PRIMARY KEY(player_id,day,topic));
      CREATE TABLE IF NOT EXISTS coin_trail_days(player_id TEXT REFERENCES players(id) ON DELETE CASCADE,day INTEGER NOT NULL,PRIMARY KEY(player_id,day));
      CREATE TABLE IF NOT EXISTS tournament_prize_receipts(player_id TEXT REFERENCES players(id) ON DELETE CASCADE,event_id TEXT NOT NULL,seen INTEGER NOT NULL,PRIMARY KEY(player_id,event_id));
      CREATE TABLE IF NOT EXISTS player_display_badge(player_id TEXT PRIMARY KEY REFERENCES players(id) ON DELETE CASCADE,event_id TEXT);');
}

function coin_trail_award(PDO $db,array $match):void {
    if(!$match['own_finished'])return;
    $answers=json_decode($match['answers'],true);$packet=json_decode($match['packet'],true);
    if(count($answers)!==7 || count($packet)!==7)return;
    $correct=[];
    foreach($answers as $i=>$answer)if(!empty($answer['correct']) && (int)$answer['points']>0)$correct[$packet[$i]['id']]=true;
    if(count($correct)<4)return;
    $pid=$match['player_id'];$day=(int)floor((int)$match['own_finished']/86400)*86400;
    if((int)sql($db,'SELECT COUNT(*) FROM coin_trail_stamps WHERE player_id=? AND day=?',[$pid,$day])->fetchColumn()>=3)return;
    $insert=sql($db,'INSERT OR IGNORE INTO coin_trail_stamps VALUES(?,?,?,?)',[$pid,$day,$match['topic'],$match['id']]);
    if(!$insert->rowCount())return;
    tournament_wallet($db,$pid);
    tournament_credit($db,$pid,'trail:'.$day.':'.$match['topic'],10,0);
    if((int)sql($db,'SELECT COUNT(*) FROM coin_trail_stamps WHERE player_id=? AND day=?',[$pid,$day])->fetchColumn()===3) {
        sql($db,'INSERT OR IGNORE INTO coin_trail_days VALUES(?,?)',[$pid,$day]);
        tournament_credit($db,$pid,'trail-complete:'.$day,15,0);
        $week=strtotime('monday this week 00:00 UTC',$day);
        if((int)sql($db,'SELECT COUNT(*) FROM coin_trail_days WHERE player_id=? AND day>=? AND day<?',[$pid,$week,$week+604800])->fetchColumn()>=5)tournament_credit($db,$pid,'trail-week:'.$week,50,0);
    }
}

function coin_trail_progress(PDO $db,string $pid):array {
    $day=(int)floor(time()/86400)*86400;$week=strtotime('monday this week 00:00 UTC');
    $topics=sql($db,'SELECT topic FROM coin_trail_stamps WHERE player_id=? AND day=? ORDER BY rowid',[$pid,$day])->fetchAll(PDO::FETCH_COLUMN);
    $days=(int)sql($db,'SELECT COUNT(*) FROM coin_trail_days WHERE player_id=? AND day>=? AND day<?',[$pid,$week,$week+604800])->fetchColumn();
    return ['wallet'=>tournament_wallet($db,$pid),'topics'=>$topics,'earnedToday'=>count($topics)*10+(count($topics)===3?15:0),'dailyMaximum'=>45,'completedDays'=>$days,'weeklyBonusEarned'=>(bool)sql($db,'SELECT 1 FROM tournament_ledger WHERE player_id=? AND reference=?',[$pid,'trail-week:'.$week])->fetch(),'resets'=>$day+86400];
}

function prize_card(array $row):array {
    return ['id'=>$row['event_id'],'topicID'=>$row['topic'],'kind'=>$row['kind'],'rank'=>(int)$row['rank'],'coins'=>(int)$row['reward'],'date'=>(int)$row['ends'],'score'=>(int)$row['score']];
}
function earned_prizes(PDO $db,string $pid,bool $unseen=false):array {
    $where=$unseen?' AND NOT EXISTS(SELECT 1 FROM tournament_prize_receipts r WHERE r.player_id=p.player_id AND r.event_id=p.event_id)':'';
    $rows=sql($db,'SELECT p.*,e.topic,e.kind,e.ends FROM tournament_places p JOIN tournament_events e ON e.id=p.event_id WHERE p.player_id=? AND p.rank BETWEEN 1 AND 3'.$where.' ORDER BY e.ends DESC,p.rank LIMIT 100',[$pid])->fetchAll();
    return array_map('prize_card',$rows);
}
function display_badge(PDO $db,string $pid):?array {
    $selection=sql($db,'SELECT event_id FROM player_display_badge WHERE player_id=?',[$pid])->fetch();
    if($selection && !$selection['event_id'])return null;
    $query='SELECT p.*,e.topic,e.kind,e.ends FROM tournament_places p JOIN tournament_events e ON e.id=p.event_id WHERE p.player_id=? AND p.rank BETWEEN 1 AND 3';$args=[$pid];
    if($selection){$query.=' AND p.event_id=?';$args[]=$selection['event_id'];}
    $row=sql($db,$query.' ORDER BY p.rank,e.ends DESC LIMIT 1',$args)->fetch();
    return $row?prize_card($row):null;
}

function economy_routes(string $route,PDO $db,string $pid,array $body):void {
    if(!in_array($route,['coins','prizes','prize-seen','select-badge'],true))return;
    $db->exec('BEGIN IMMEDIATE');tournament_seed($db);tournament_settle($db);tournament_wallet($db,$pid);
    if($route==='coins'){$reply=coin_trail_progress($db,$pid);$db->exec('COMMIT');out($reply);}
    if($route==='prizes'){$reply=['pending'=>earned_prizes($db,$pid,true),'earned'=>earned_prizes($db,$pid),'selected'=>display_badge($db,$pid)];$db->exec('COMMIT');out($reply);}
    $event=$body['event'] ?? null;
    if($event!==null && !is_string($event))fail('Choose a tournament badge');
    if($event!==null && !sql($db,'SELECT 1 FROM tournament_places WHERE player_id=? AND event_id=? AND rank BETWEEN 1 AND 3',[$pid,$event])->fetch())fail('You have not earned this tournament badge',403);
    if($route==='prize-seen') {
        if($event===null)fail('Choose a tournament result');
        sql($db,'INSERT OR IGNORE INTO tournament_prize_receipts VALUES(?,?,?)',[$pid,$event,time()]);
    } else sql($db,'INSERT INTO player_display_badge VALUES(?,?) ON CONFLICT(player_id) DO UPDATE SET event_id=excluded.event_id',[$pid,$event]);
    $db->exec('COMMIT');out(['ok'=>true]);
}
