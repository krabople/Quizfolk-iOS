<?php
declare(strict_types=1);
require dirname(__DIR__).'/backend/tournaments.php';
function sql(PDO $db,string $query,array $args=[]):PDOStatement {$s=$db->prepare($query);$s->execute($args);return $s;}
function check(bool $ok,string $message):void {if(!$ok)throw new RuntimeException($message);}
function fixture():PDO {
    $db=new PDO('sqlite::memory:',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
    $db->exec('PRAGMA foreign_keys=ON; CREATE TABLE players(id TEXT PRIMARY KEY); INSERT INTO players VALUES("alice");');
    tournament_schema($db);return $db;
}
$db=fixture();tournament_seed($db);
check((int)$db->query('SELECT COUNT(*) FROM tournament_events WHERE kind="daily"')->fetchColumn()===3,'A fresh day must have three daily events');
check((int)$db->query('SELECT COUNT(*) FROM tournament_events WHERE kind="weekly"')->fetchColumn()===3,'Weekly schedule changed');
check((int)$db->query('SELECT COUNT(*) FROM tournament_events WHERE kind="daily" AND coins=25 AND tickets=0')->fetchColumn()===3,'All fresh daily entries must cost25 coins');
check((int)$db->query('SELECT COUNT(*) FROM tournament_events WHERE kind="weekly" AND coins=50 AND tickets=0')->fetchColumn()===3,'All fresh weekly entries must cost50 coins');
$freshSchedule=json_decode($db->query('SELECT event_ids FROM tournament_daily_schedule')->fetchColumn(),true);
check(count(array_unique($freshSchedule))===3,'Uniform daily prices produced duplicate featured IDs');
tournament_seed($db);check((int)$db->query('SELECT COUNT(*) FROM tournament_events')->fetchColumn()===6,'Repeat seed duplicated events');
$start=(int)floor(time()/86400)*86400;
$db=fixture();
for($i=0;$i<6;$i++) {
    $coins=$i%3===1?25:0;$tickets=$i%3===2?1:0;$id='legacy-'.$i;
    sql($db,'INSERT INTO tournament_events(id,topic,kind,starts,ends,coins,tickets) VALUES(?,?,"daily",?,?,?,?)',[$id,(string)(9+$i),$start,$start+86400,$coins,$tickets]);
    sql($db,'INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,turn,score,streak,created) VALUES(?,?,"alice",?,?,1,20,1,?)',['run-'.$i,$id,'request-'.$i,'["answered","remaining"]',time()]);
    sql($db,'INSERT INTO tournament_ledger VALUES("alice",?,?,?,?)',['entry:run-'.$i,-$coins,-$tickets,time()]);
}
$db->exec('INSERT INTO tournament_wallet VALUES("alice",50,1)');
sql($db,'INSERT INTO tournament_ledger VALUES("alice","welcome",100,3,?)',[time()]);
$wallet=tournament_wallet($db,'alice');$runs=$db->query('SELECT * FROM tournament_runs ORDER BY id')->fetchAll();
check($wallet['coins']===75 && $wallet['tickets']===0,'Ticket balance was not converted at 25 coins each');
check(tournament_wallet($db,'alice')===$wallet,'Ticket conversion was applied twice');
tournament_seed($db);
$cards=array_map(fn($e)=>tournament_card($db,'alice',$e),$db->query('SELECT * FROM tournament_events WHERE kind="daily" ORDER BY id')->fetchAll());
$featured=array_values(array_filter($cards,fn($e)=>$e['featured']));
check(count($featured)===3,'An old six-event day must feature exactly three');
check(count(array_filter($cards,fn($e)=>!$e['featured'] && $e['activeRun']!==null && $e['attempts']===1))>=3,'Earlier active entries must remain resumable');
check(tournament_wallet($db,'alice')===$wallet,'Migration changed credits');
check($db->query('SELECT * FROM tournament_runs ORDER BY id')->fetchAll()===$runs,'Migration changed paid runs');
check(tournament_prize_pool($db,'legacy-0')===875,'Open daily prizes must use the new guaranteed snapshot');
check(tournament_prize_pool($db,'legacy-2')===875,'Still-open legacy daily events must show the new fixed prize schedule');
$schedule=$db->query('SELECT event_ids FROM tournament_daily_schedule')->fetchColumn();
// More play in an earlier event cannot replace today's visible topics.
sql($db,'INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,created) VALUES("later","legacy-4","alice","later-request","[]",?)',[time()]);
tournament_seed($db);tournament_schema($db);tournament_seed($db);
check($db->query('SELECT event_ids FROM tournament_daily_schedule')->fetchColumn()===$schedule,'Featured topics drifted during the day');
check((int)$db->query('SELECT COUNT(*) FROM tournament_events WHERE kind="daily"')->fetchColumn()===6,'Legacy adoption created unnecessary daily events');

// Policy transition is scoped to current/upcoming public events. Refund actual
// excess coin debits for currently open entries only; keep every run and the
// previously published three-event selection unchanged.
$db=fixture();$now=time();$start=intdiv($now,86400)*86400;
$db->exec('CREATE TABLE tournament_prize_receipts(player_id TEXT,event_id TEXT,seen INTEGER,PRIMARY KEY(player_id,event_id));');
tournament_wallet($db,'alice');sql($db,'UPDATE tournament_wallet SET coins=1000 WHERE player_id="alice"');
$cases=[
 ['daily50','daily',50,$start,$start+86400,0,50],
 ['daily75','daily',75,$start,$start+86400,0,75],
 ['daily25','daily',25,$start,$start+86400,0,25],
 ['dailyfree','daily',0,$start,$start+86400,0,0],
 ['missing-payment','daily',75,$start,$start+86400,0,null],
 ['weekly100','weekly',100,$start-86400,$start+604800,0,100],
 ['private-paid','party',10,$start,$start+86400,0,10],
 ['private-free','party',0,$start,$start+86400,0,0],
 ['ended-daily','daily',75,$start-86400,$now-1,0,75],
 ['settled-weekly','weekly',100,$start-86400,$start+86400,1,100],
 ['future-daily','daily',75,$start+86400,$start+172800,0,75],
];
foreach($cases as [$id,$kind,$fee,$begins,$ends,$settled,$paid]) {
 sql($db,'INSERT INTO tournament_events VALUES(?,?,?,?,?,?,?,?)',[$id,'22',$kind,$begins,$ends,$fee,0,$settled]);
 sql($db,'INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,turn,score,streak,created) VALUES(?,?,"alice",?,?,1,20,1,?)',['paid-'.$id,$id,'request-'.$id,'["answered","remaining"]',$now-10]);
 if($paid!==null)tournament_credit($db,'alice','entry:paid-'.$id,-$paid,0);
}
$published=['daily75','daily25','daily50'];sql($db,'INSERT INTO tournament_daily_schedule VALUES(?,?)',[$start,json_encode($published)]);
$beforeRuns=$db->query('SELECT * FROM tournament_runs ORDER BY id')->fetchAll();
$beforeEntries=$db->query('SELECT * FROM tournament_ledger WHERE reference LIKE "entry:%" ORDER BY reference')->fetchAll();
$beforeCoins=tournament_wallet($db,'alice')['coins'];
$unchanged=$db->query('SELECT * FROM tournament_events WHERE id IN ("private-paid","private-free","ended-daily","settled-weekly") ORDER BY id')->fetchAll();
$db->exec('BEGIN IMMEDIATE');tournament_seed($db,$now);$db->exec('COMMIT');
check(tournament_wallet($db,'alice')['coins']===$beforeCoins+125,'Actual daily25/50 and weekly50 excess coins were not refunded');
check((int)$db->query('SELECT COUNT(*) FROM tournament_ledger WHERE reference LIKE "public-entry-v2:%"')->fetchColumn()===3,'Refund applied outside eligible paid entries');
check($db->query('SELECT * FROM tournament_runs ORDER BY id')->fetchAll()===$beforeRuns,'Price migration changed runs/scores/decks/IDs');
check($db->query('SELECT * FROM tournament_ledger WHERE reference LIKE "entry:%" ORDER BY reference')->fetchAll()===$beforeEntries,'Price migration rewrote entry history');
check($db->query('SELECT * FROM tournament_events WHERE id IN ("private-paid","private-free","ended-daily","settled-weekly") ORDER BY id')->fetchAll()===$unchanged,'Ended/settled/private entry terms changed');
check(json_decode(sql($db,'SELECT event_ids FROM tournament_daily_schedule WHERE day=?',[$start])->fetchColumn(),true)===$published,'Persisted daily selection changed');
check((int)sql($db,'SELECT coins FROM tournament_events WHERE id="future-daily"')->fetchColumn()===25,'Upcoming daily entry price not changed');
foreach([['daily50',[500,250,125]],['weekly100',[1000,500,250]],['ended-daily',[150,100,50]],['settled-weekly',[500,250,125]]] as [$id,$prizes]) {
 $event=sql($db,'SELECT * FROM tournament_events WHERE id=?',[$id])->fetch();
 check(tournament_event_prizes($db,$event)===$prizes,'Event prize history/snapshot mismatch for '.$id);
 check(tournament_card($db,'alice',$event)['prizes']===$prizes,'Displayed prizes disagree with event snapshot');
}
check((int)$db->query('SELECT COUNT(*) FROM tournament_prize_policies WHERE event_id LIKE "private-%"')->fetchColumn()===0,'Private prize rules were migrated');
$policies=$db->query('SELECT * FROM tournament_prize_policies ORDER BY event_id')->fetchAll();
for($i=0;$i<3;$i++){tournament_schema($db);$db->exec('BEGIN IMMEDIATE');tournament_seed($db,$now);$db->exec('COMMIT');}
check(tournament_wallet($db,'alice')['coins']===$beforeCoins+125,'Repeat policy migration refunded twice');
check($db->query('SELECT * FROM tournament_prize_policies ORDER BY event_id')->fetchAll()===$policies,'Snapshot/version timestamp drifted on repeated seed');

// Existing settled prizes and their acknowledgement remain unchanged. Newly
// closed v2 events settle from advertised snapshots, while legacy ended events
// keep v1 terms and v1 reconciliation never upgrades them to current values.
sql($db,'INSERT INTO tournament_places VALUES("settled-weekly","alice",1,20,1,500)');
tournament_credit($db,'alice','prize:settled-weekly',500,0);
sql($db,'INSERT INTO tournament_prize_receipts VALUES("alice","settled-weekly",?)',[$now]);
sql($db,'INSERT INTO tournament_fixed_prizes_v1 VALUES("settled-weekly",?)',[$now]);
$oldReceipt=$db->query('SELECT * FROM tournament_prize_receipts')->fetchAll();
foreach(['bob','cara'] as $pid){sql($db,'INSERT INTO players VALUES(?)',[$pid]);tournament_wallet($db,$pid);}
foreach(['daily50','weekly100'] as $event) {
 foreach(['bob'=>19,'cara'=>18] as $pid=>$score)sql($db,'INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,score,streak,state,created) VALUES(?,?,?,?,?,?,1,"finished",?)',[$event.'-'.$pid,$event,$pid,$event.'-request-'.$pid,'[]',$score,$now]);
 sql($db,'UPDATE tournament_events SET ends=? WHERE id=?',[$now-1,$event]);
}
$db->exec('BEGIN IMMEDIATE');tournament_settle($db);$db->exec('COMMIT');
foreach([['daily50',[500,250,125]],['weekly100',[1000,500,250]],['ended-daily',[150]]] as [$event,$rewards]) {
 check(array_map('intval',sql($db,'SELECT reward FROM tournament_places WHERE event_id=? ORDER BY rank',[$event])->fetchAll(PDO::FETCH_COLUMN))===$rewards,'Settlement ignored stored event terms');
}
check($db->query('SELECT * FROM tournament_prize_receipts')->fetchAll()===$oldReceipt,'New policy reopened a historical prize receipt');
$settledLedger=$db->query('SELECT * FROM tournament_ledger ORDER BY player_id,reference')->fetchAll();
$db->exec('BEGIN IMMEDIATE');tournament_seed($db,$now);tournament_settle($db);$db->exec('COMMIT');
check($db->query('SELECT * FROM tournament_ledger ORDER BY player_id,reference')->fetchAll()===$settledLedger,'Repeated settlement or v1 reconciliation changed credits');
check((int)sql($db,'SELECT reward FROM tournament_places WHERE event_id="settled-weekly"')->fetchColumn()===500,'Historical weekly prize was relabelled');

// Tomorrow adopts existing upcoming events without price tiers, then fills only
// missing slots. A second future seed must leave exactly3 unique persistedIDs.
$tomorrow=$start+86400+1;tournament_seed($db,$tomorrow);tournament_seed($db,$tomorrow);
$next=json_decode(sql($db,'SELECT event_ids FROM tournament_daily_schedule WHERE day=?',[$start+86400])->fetchColumn(),true);
check(count($next)===3 && count(array_unique($next))===3 && in_array('future-daily',$next,true),'Future day selection duplicated/lost an existing event');
check((int)sql($db,'SELECT COUNT(*) FROM tournament_events WHERE kind="daily" AND starts=?',[$start+86400])->fetchColumn()===3,'Future seed created duplicate daily events');
foreach([
    [25,[1],[25]], [75,[1,2],[45,30]], [150,[1,2,3],[75,45,30]],
    [150,[1,1,3],[60,60,30]], [100,[1,2,3,3],[50,30,10,10]], [101,[1,1,1],[33,33,33]]
] as [$pool,$ranks,$expected]) {
    $rows=array_map(fn($rank)=>['rank'=>$rank],$ranks);
    $rewards=array_map(fn($rank)=>tournament_prize($pool,$rows,$rank),$ranks);
    check($rewards===$expected,'Podium/tie prize split is incorrect');
    check(array_sum($rewards)<=$pool,'Prizes exceed the actual pool');
}
foreach([
 ['daily',[1],[150]],['daily',[1,2,3],[150,100,50]],['weekly',[1,2,3],[500,250,125]],
 ['daily',[1,1,3],[125,125,50]],['weekly',[1,2,2],[500,187,187]]
] as [$kind,$ranks,$expected]) {
 $rows=array_map(fn($rank)=>['rank'=>$rank],$ranks);
 check(array_map(fn($rank)=>tournament_fixed_reward(tournament_fixed_prizes($kind),$rows,$rank),$ranks)===$expected,'Fixed podium/tie awards changed');
}
echo "PASS:25/50 public entries, idempotent actual-debit refunds, stable three-event schedules, versioned current/legacy prizes and settlement, preserved runs/history/receipts, unchanged private pools\n";
