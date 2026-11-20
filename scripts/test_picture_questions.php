<?php
require dirname(__DIR__).'/backend/social.php';
function sql(PDO $db,string $query,array $args=[]):PDOStatement {$s=$db->prepare($query);$s->execute($args);return $s;}
function fail(string $message,int $status=400):never {throw new RuntimeException($message,$status);}
function check(bool $condition,string $label):void {if(!$condition)throw new RuntimeException($label);}
$bank=json_decode(file_get_contents(dirname(__DIR__).'/data/questions.json'),true);
$flags=array_values(array_filter($bank,fn($q)=>$q['categoryID']==='41'));
$logos=array_values(array_filter($bank,fn($q)=>$q['categoryID']==='42'));
$caps=array_values(array_filter($bank,fn($q)=>$q['categoryID']==='43'));
check(count($flags)===197 && count($logos)>=150 && count($caps)===394,'New coverage incomplete');
check(count(unique_questions($flags))===197,'Same-stem pictures collapsed');
check(count(unique_questions($caps))===197,'Capital and reverse repeated the same country in a deck');
foreach($flags as $q) {
 check(hash('sha256',base64_decode($q['imagePng'],true))===$q['imageSHA256'],'Invalid flag hash');
 $pub=public_question($q,true);check($pub['answers']===[] && !isset($pub['correctIndex']) && !isset($pub['countryCode']) && !isset($pub['sourceURL']),'Preview leaked answers');
}
$_SERVER['HTTP_X_QUIZFOLK_CLIENT']='3';
check(count(visible_topics())===34,'Old clients should receive only text categories plus Mixed');
try{require_image_client($flags[0]);throw new RuntimeException('Legacy client received image');}catch(RuntimeException $e){check($e->getCode()===426,'Missing update message');}
$_SERVER['HTTP_X_QUIZFOLK_CLIENT']='4';require_image_client($flags[0]);check(count(visible_topics())===36,'Modern client missed new topics');
$db=new PDO('sqlite::memory:',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);$db->exec('CREATE TABLE questions(id TEXT PRIMARY KEY,payload TEXT)');
$q=$flags[0];sql($db,'INSERT INTO questions VALUES(?,?)',[$q['id'],json_encode($q)]);check(packet_is_current([$q],$db),'Current picture was rejected');
$changed=$q;$changed['imageSHA256']=str_repeat('0',64);check(!packet_is_current([$changed],$db),'A changed image did not invalidate a saved packet');
echo "PASS:197 countries, reverse-capital grouping, distinct same-stem pictures, preview secrecy, legacy update guard and image corrections\n";
