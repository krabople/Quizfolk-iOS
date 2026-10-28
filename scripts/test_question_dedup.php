<?php
declare(strict_types=1);
require dirname(__DIR__).'/backend/social.php';
require dirname(__DIR__).'/backend/tournaments.php';
function sql(PDO $db,string $query,array $args=[]):PDOStatement {$s=$db->prepare($query);$s->execute($args);return $s;}
function check(bool $ok,string $message):void {if(!$ok)throw new RuntimeException($message);}
function fail(string $message,int $status=400):never {throw new RuntimeException($message,$status);}
function memory_db():PDO {return new PDO('sqlite::memory:',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);}
function question(string $id,string $prompt):array {return ['id'=>$id,'categoryID'=>'17','difficulty'=>'easy','prompt'=>$prompt,'answers'=>['Right','Wrong one','Wrong two','Wrong three'],'correctIndex'=>0];}
check(question_prompt_key('  What’s Éarth? ' )===question_prompt_key("WHAT'S   ÉARTH!!!"),'Case, whitespace and apostrophe style must not create a distinct question');
check(question_prompt_key('Straße?')===question_prompt_key('STRASSE'),'Unicode case folding must cover multi-character folds');
check(question_prompt_key('What is 2 + 2?')!==question_prompt_key('What is 2 × 2?'),'Different mathematical symbols must remain distinct');
foreach([['2-3','23'],['1.2','12'],['2/3','23'],['6!','6'],['2^3','23'],['−2','2'],['3%','3'],['2 ≤ 3','2 < 3'],['now here','nowhere']] as [$left,$right])
    check(question_prompt_key('Calculate '.$left.'?')!==question_prompt_key('Calculate '.$right.'?'),'Normalization collapsed meaningful punctuation or word boundaries: '.$left);
$db=memory_db();$db->exec('CREATE TABLE players(id TEXT PRIMARY KEY);INSERT INTO players VALUES("alice");CREATE TABLE matches(player_id TEXT,topic TEXT,packet TEXT,answers TEXT,preview_started REAL,started REAL);');
tournament_schema($db);tournament_schema($db);
$qdb=memory_db();$qdb->exec('CREATE TABLE questions(id TEXT PRIMARY KEY,category_id TEXT,payload TEXT)');
$a=question('a','What’s Earth?');$copy=question('copy',"WHAT'S EARTH!!!");$bank=[$a,$copy];
for($i=0;$i<6;$i++)$bank[]=question('fresh-'.$i,'Fresh question '.$i.'?');
foreach($bank as $q)sql($qdb,'INSERT INTO questions VALUES(?,?,?)',[$q['id'],'17',json_encode($q)]);
sql($db,'INSERT INTO question_seen VALUES("alice","a","17")');
for($try=0;$try<10;$try++) {
    $deck=question_deck($bank,['a'=>true]);
    check(count($deck)===7 && count(unique_questions($deck))===7,'Deck must contain one representative per prompt');
    check(question_prompt_key($deck[6]['prompt'])===question_prompt_key($a['prompt']),'All copies of previously seen content must follow unseen content');
    $packet=fresh_packet($db,'alice','17',$qdb);
    check(count($packet)===7 && count(unique_questions($packet))===7,'Duel packet contains repeated content');
    foreach($packet as $q)check($q['answers'][$q['correctIndex']]==='Right','Option shuffling corrupted the answer key');
}
check(!packet_is_current([$a,$copy],$qdb),'Different IDs with duplicate content must not enter historical replays');
check(!packet_is_current([$a,$a],$qdb),'Repeated IDs must not enter historical replays');
sql($qdb,'DELETE FROM questions WHERE id="fresh-5"');
try {fresh_packet($db,'alice','17',$qdb);throw new RuntimeException('An undersized topic was accepted');}
catch(RuntimeException $e){check($e->getCode()===410 && str_contains($e->getMessage(),'seven different'),'Exhaustion must fail clearly instead of refilling with repeats');}
sql($db,'INSERT INTO tournament_events(id,topic,kind,starts,ends,coins,tickets) VALUES("event","17","daily",0,9999999999,25,0)');
function run_fixture(PDO $db,string $id,array $deck,int $turn,array $keys=[]):array {
    sql($db,'INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,turn,score,streak,preview,started,created,question_keys) VALUES(?,"event","alice",?,?,?, ?,?,100,102,0,?)',[$id,$id,json_encode($deck),$turn,$turn*20,$turn,json_encode($keys)]);
    return sql($db,'SELECT * FROM tournament_runs WHERE id=?',[$id])->fetch();
}
$r=run_fixture($db,'legacy',['a','copy','fresh-0','fresh-0','removed','fresh-1'],1);
$q=tournament_question($db,$r,$qdb);
check($q['id']==='fresh-0' && json_decode($r['deck'],true)===['a','fresh-0','fresh-1'],'Legacy run did not skip repeated and removed future content');
check($r['score']===20 && $r['turn']===1 && $r['preview']===null && $r['started']===null && $r['_questionChanged'],'Replacing the current duplicate must restart reading without changing earned progress');
$saved=sql($db,'SELECT * FROM tournament_runs WHERE id="legacy"')->fetch();
check($saved['deck']===$r['deck'] && $saved['question_keys']===$r['question_keys'],'Pruned selection and prompt fingerprints must persist');
check(tournament_question($db,$saved,$qdb)===$q,'Resuming must preserve question and answer ordering');
// Removing a duplicate later in the deck must not reset the current timer.
$tail=run_fixture($db,'tail',['a','fresh-0','copy'],1);
tournament_question($db,$tail,$qdb);
check(!$tail['_questionChanged'] && $tail['started']===102.0 && $tail['preview']===100.0,'Pruning only the tail reset a live question timer');
// Saved fingerprints prevent a removed answered ID returning under another ID.
$keys=['a'=>question_prompt_key($a['prompt'])];sql($qdb,'DELETE FROM questions WHERE id="a"');
$removed=run_fixture($db,'removed',['a','copy','fresh-1'],1,$keys);
check(tournament_question($db,$removed,$qdb)['id']==='fresh-1','Withdrawn answered content returned via a duplicate ID');
$exhausted=run_fixture($db,'exhausted',['a','copy','missing'],1,$keys);
check(tournament_question($db,$exhausted,$qdb)===null,'Exhausted run refilled with a repeat');
check($exhausted['state']==='cleared' && $exhausted['score']===20 && $exhausted['turn']===1,'Exhaustion must retain earned points and end normally');
check(sql($db,'SELECT state FROM tournament_runs WHERE id="exhausted"')->fetchColumn()==='cleared','Exhaustion was not persisted');
$unknown=run_fixture($db,'unknown',['withdrawn-before-upgrade','fresh-1'],1);
check(tournament_question($db,$unknown,$qdb)===null && $unknown['score']===20,'An unverifiable legacy prefix must end safely with earned score');
check((int)$db->query('SELECT COUNT(*) FROM tournament_ledger')->fetchColumn()===0,'Repair must not charge or grant coins');
echo "PASS: content-unique duel and tournament selection, Unicode formatting duplicates, freshness, answer shuffling, clear exhaustion, replay exclusion, durable legacy repair and preserved scores/timers\n";
