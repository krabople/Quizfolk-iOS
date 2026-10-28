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
check(tournament_prize_pool($db,'legacy-0')===25,'An already-entered legacy free event lost its minimum prize');
check(tournament_prize_pool($db,'legacy-2')===25,'Historical ticket entry was not included in the coin pool');
$schedule=$db->query('SELECT event_ids FROM tournament_daily_schedule')->fetchColumn();
// More play in an earlier event cannot replace today's visible topics.
sql($db,'INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,created) VALUES("later","legacy-4","alice","later-request","[]",?)',[time()]);
tournament_seed($db);tournament_schema($db);tournament_seed($db);
check($db->query('SELECT event_ids FROM tournament_daily_schedule')->fetchColumn()===$schedule,'Featured topics drifted during the day');
foreach([
    [25,[1],[25]], [75,[1,2],[45,30]], [150,[1,2,3],[75,45,30]],
    [150,[1,1,3],[60,60,30]], [100,[1,2,3,3],[50,30,10,10]], [101,[1,1,1],[33,33,33]]
] as [$pool,$ranks,$expected]) {
    $rows=array_map(fn($rank)=>['rank'=>$rank],$ranks);
    $rewards=array_map(fn($rank)=>tournament_prize($pool,$rows,$rank),$ranks);
    check($rewards===$expected,'Podium/tie prize split is incorrect');
    check(array_sum($rewards)<=$pool,'Prizes exceed the actual pool');
}
echo "PASS: three paid daily events, stable selection, ticket conversion, idempotent migration, paid runs preserved, legacy minimum prize, bounded podium and tie rewards\n";
