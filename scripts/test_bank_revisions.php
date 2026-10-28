<?php
declare(strict_types=1);
require dirname(__DIR__).'/backend/social.php';
function sql(PDO $db,string $query,array $args=[]):PDOStatement {$s=$db->prepare($query);$s->execute($args);return $s;}
function check(bool $condition,string $message):void {if(!$condition)throw new RuntimeException($message);}
$db=new PDO('sqlite::memory:',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
$db->exec('CREATE TABLE questions(id TEXT PRIMARY KEY,payload TEXT NOT NULL)');
$q=['id'=>'01234567890123456789','categoryID'=>'19','prompt'=>'What is 2 + 2?','answers'=>['4','3','5','6'],'correctIndex'=>0];
sql($db,'INSERT INTO questions VALUES(?,?)',[$q['id'],json_encode($q)]);
check(packet_is_current([$q],$db),'Unchanged questions must remain playable');
$shuffled=$q;$shuffled['answers']=['6','3','4','5'];$shuffled['correctIndex']=2;
check(packet_is_current([$shuffled],$db),'Equivalent shuffled choices must remain playable');
$changed=$q;$changed['prompt']='What is 2 + 3?';
check(!packet_is_current([$changed],$db),'A corrected prompt must not return through a replay');
$changed=$q;$changed['correctIndex']=1;
check(!packet_is_current([$changed],$db),'A corrected answer key must invalidate the old packet');
$changed=$q;$changed['answers'][1]='7';
check(!packet_is_current([$changed],$db),'Changed distractors invalidate the old question');
$changed=$q;$changed['categoryID']='17';
check(!packet_is_current([$changed],$db),'Recategorized questions must not return to the old topic');
sql($db,'DELETE FROM questions');
check(!packet_is_current([$q],$db),'Withdrawn questions must not be playable');
check(!packet_is_current([],$db),'Empty packets are invalid');
echo "PASS: stored duels preserve unchanged questions and exclude corrected or withdrawn content\n";
