<?php
declare(strict_types=1);
require dirname(__DIR__).'/backend/tournaments.php';
require dirname(__DIR__).'/backend/economy.php';
function sql(PDO $db,string $query,array $args=[]):PDOStatement {$s=$db->prepare($query);$s->execute($args);return $s;}
function check(bool $ok,string $message):void {if(!$ok)throw new RuntimeException($message);}
$db=new PDO('sqlite::memory:',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
$db->exec('PRAGMA foreign_keys=ON; CREATE TABLE players(id TEXT PRIMARY KEY); INSERT INTO players VALUES("alice"); CREATE TABLE matches(id TEXT PRIMARY KEY);');
economy_schema($db);tournament_schema($db);economy_schema($db);
function completed(string $id,string $topic,int $time,int $correct=4):array {
    $packet=[];$answers=[];
    for($i=0;$i<7;$i++){$packet[]=['id'=>'question-'.$i];$answers[]=['correct'=>$i<$correct,'points'=>$i<$correct?20:0];}
    return ['id'=>$id,'player_id'=>'alice','topic'=>$topic,'own_finished'=>$time,'packet'=>json_encode($packet),'answers'=>json_encode($answers)];
}
$monday=strtotime('2026-10-26 00:00 UTC');
check(tournament_wallet($db,'alice')['coins']===100,'Welcome balance');
$failed=completed('poor','9',$monday,3);coin_trail_award($db,$failed);
$unfinished=completed('short','9',$monday);$unfinished['answers']='[]';coin_trail_award($db,$unfinished);
$timeout=completed('timeout','9',$monday);$timeout['answers']=json_encode(array_fill(0,7,['correct'=>true,'points'=>0]));coin_trail_award($db,$timeout);
$duplicate=completed('duplicates','9',$monday);$duplicate['packet']=json_encode(array_fill(0,7,['id'=>'same']));coin_trail_award($db,$duplicate);
check(tournament_wallet($db,'alice')['coins']===100,'Incomplete, insufficient, timed-out or duplicated answers earned coins');
for($day=0;$day<7;$day++) {
    for($topic=9;$topic<13;$topic++) {
        $m=completed("day-$day-topic-$topic",(string)$topic,$monday+$day*86400+86399);
        coin_trail_award($db,$m);coin_trail_award($db,$m);
        $m['id'].='-second-duel';coin_trail_award($db,$m);
    }
    $expected=100+($day+1)*45+($day>=4?50:0);
    check(tournament_wallet($db,'alice')['coins']===$expected,'Daily cap, same-topic retry, idempotence or weekly bonus failed');
}
check((int)$db->query('SELECT COUNT(*) FROM coin_trail_stamps')->fetchColumn()===21,'More than three stamps per day');
coin_trail_award($db,completed('next-week','9',$monday+604800));
check(tournament_wallet($db,'alice')['coins']===475,'Next UTC day/week did not reset');
coin_trail_award($db,completed('day-0-topic-9','9',$monday+604800));
check(tournament_wallet($db,'alice')['coins']===475,'A duel earned twice across days');
// A pending asynchronous match earns its trail reward at the player's own
// finish time. It does not need the opponent's completion or a claimed win.
$pending=completed('pending-opponent','10',$monday+604800);$pending['completed']=null;
coin_trail_award($db,$pending);
check(tournament_wallet($db,'alice')['coins']===485,'Asynchronous player completion did not earn its stamp');
$db->exec('DELETE FROM players WHERE id="alice"');
check((int)$db->query('SELECT COUNT(*) FROM coin_trail_stamps')->fetchColumn()===0,'Account deletion left coin trail data');
echo "PASS: completed play, four distinct correct answers, daily three-topic cap, repeat protection, weekly bonus, UTC rollover, asynchronous completion and deletion\n";
