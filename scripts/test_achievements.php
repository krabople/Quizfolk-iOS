<?php
declare(strict_types=1);
require dirname(__DIR__).'/backend/social.php';
function sql(PDO $db,string $query,array $args=[]):PDOStatement {$s=$db->prepare($query);$s->execute($args);return $s;}
function check(bool $ok,string $message):void {if(!$ok)throw new RuntimeException($message);}
$db=new PDO('sqlite::memory:',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
$db->exec('CREATE TABLE tournament_events(id TEXT PRIMARY KEY,topic TEXT,kind TEXT,ends INTEGER,settled INTEGER);
 CREATE TABLE tournament_places(event_id TEXT,player_id TEXT,rank INTEGER);
 CREATE TABLE tournament_runs(id TEXT,player_id TEXT,event_id TEXT,streak INTEGER,score INTEGER);
 CREATE TABLE matches(id TEXT,player_id TEXT,answers TEXT,completed INTEGER,score INTEGER,opponent_score INTEGER);');
function event(PDO $db,string $id,string $topic,string $kind,int $rank,int $date,bool $settled=true):void {
 sql($db,'INSERT INTO tournament_events VALUES(?,?,?,?,?)',[$id,$topic,$kind,$date,(int)$settled]);
 sql($db,'INSERT INTO tournament_places VALUES(?,?,?)',[$id,'alice',$rank]);
}
$empty=['stats'=>['matches'=>0,'wins'=>0,'perfect'=>0,'correct'=>0],'topics'=>[]];$names=['18'=>'Computers','19'=>'Mathematics','22'=>'Geography'];
function indexed(array $rows):array{return array_column($rows,null,'id');}
$badges=indexed(player_achievements($db,'alice',$empty,$names));
check(count($badges)===65,'Catalogue must contain65 milestones before per-topic best finishes');
check(count(array_filter($badges,fn($b)=>$b['earned']))===0,'New account must not start with unlocked goals');
check(str_contains($badges['perfect']['description'],'all seven questions correctly'),'Seven of seven needs an explicit requirement while locked');
foreach($badges as $b)check($b['description']!=='' && $b['group']!=='' && $b['progressLabel']!=='' && $b['target']>0,'Every locked milestone needs meaning and progress');
// A rank1 older than the former20-result window must still win this topic.
event($db,'old-gold','18','daily',1,1);
for($i=0;$i<35;$i++)event($db,'new-silver-'.$i,'18','daily',2,100+$i);
event($db,'math-bronze','19','weekly',3,200);
event($db,'private-gold','22','party',1,300);
event($db,'unsettled-gold','19','daily',1,400,false);
$best=best_tournament_achievements($db,'alice',$names);
check(count($best)===2,'One best result per public topic, without private or unsettled results');
$best=indexed($best);check($best['tournament-best:18']['rank']===1 && $best['tournament-best:19']['rank']===3,'Never replace gold by newer silver/bronze');
event($db,'new-weekly-gold','18','weekly',1,500);
$again=indexed(best_tournament_achievements($db,'alice',$names));
check($again['tournament-best:18']['kind']==='weekly' && count($again)===2,'Tied-best representative deterministic without creating a duplicate');
check(str_contains($again['tournament-best:18']['name'],"Computers \u{00B7} Best #1"),'Best-place UTF-8 label must be clean');
// Lifetime progress is historical and exact; different topics/attempts cannot be added together for a single-run/level goal.
$card=['stats'=>['matches'=>9999,'wins'=>999,'perfect'=>249,'correct'=>99999],'topics'=>array_fill(0,20,['level'=>6])];
$before=indexed(player_achievements($db,'alice',$card,$names));
check(!$before['duels:10000']['earned'] && !$before['wins:1000']['earned'] && !$before['perfect:250']['earned'] && !$before['correct:100000']['earned'],'Long-term goals must not unlock a unit early');
check(!$before['topic-level:10']['earned'],'Topic levels cannot be summed');
$card['stats']=['matches'=>10000,'wins'=>1000,'perfect'=>250,'correct'=>100000];$card['topics'][0]['level']=50;
$after=indexed(player_achievements($db,'alice',$card,$names));
foreach(['duels:10000','wins:1000','perfect:250','correct:100000','topic-level:50'] as $id)check($after[$id]['earned'],'Exact threshold should unlock '.$id);
check(!$after['topic-level:75']['earned'] && !$after['topics:31']['earned'],'Higher goals stay locked');
sql($db,'INSERT INTO tournament_runs VALUES(?,?,?,?,?)',['r1','alice','old-gold',15,600]);
sql($db,'INSERT INTO tournament_runs VALUES(?,?,?,?,?)',['r2','alice','new-weekly-gold',15,600]);
sql($db,'INSERT INTO tournament_runs VALUES(?,?,?,?,?)',['r3','alice','private-gold',100,5000]);
$runs=indexed(player_achievements($db,'alice',$empty,$names));
check($runs['tournament-streak:10']['earned'] && !$runs['tournament-streak:25']['earned'] && !$runs['tournament-score:1000']['earned'],'Single-run targets must not sum attempts or include private tournaments');
check($runs['championships:1']['progress']===2 && $runs['podiums:1']['progress']===38,'Public settled prize history counts once per placing, without private/unsettled awards');
// Unfinished human challenges, or malformed8-answer packets with7 correct, are not perfect completed duels.
$right=array_fill(0,7,['correct'=>true]);$mixed=$right;$mixed[6]['correct']=false;
foreach([['finished',$right,1],['pending',$right,null],['six-right',$mixed,1],['malformed',array_merge($right,[['correct'=>false]]),1]] as [$id,$answers,$completed])sql($db,'INSERT INTO matches VALUES(?,?,?,?,?,?)',[$id,'alice',json_encode($answers),$completed,100,50]);
$stats=online_stats($db,'alice');check($stats['matches']===3 && $stats['perfect']===1 && $stats['correct']===20,'Only fully completed seven-answer duels are perfect; pending progress excluded');
$count=(int)$db->query('SELECT COUNT(*) FROM tournament_places')->fetchColumn();
player_achievements($db,'alice',['stats'=>$stats,'topics'=>[]],$names);
check((int)$db->query('SELECT COUNT(*) FROM tournament_places')->fetchColumn()===$count,'Achievements must preserve every tournament prize/history row');
echo "PASS:65 long-term milestones, exact boundaries, best per topic beyond20 results, descriptions, privacy, single-run progress, pending games and preserved prize history\n";
