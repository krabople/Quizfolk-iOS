<?php
declare(strict_types=1);
// Isolated fixture: preserve player IDs, tokens and matches while resolving old name collisions.
require dirname(__DIR__).'/backend/names.php';
function sql(PDO $db,string $query,array $args=[]):PDOStatement {$s=$db->prepare($query);$s->execute($args);return $s;}
function check(bool $ok,string $message):void {if(!$ok)throw new RuntimeException($message);}
$file=tempnam(sys_get_temp_dir(),'quizfolk-migration-');
try {
 $db=new PDO('sqlite:'.$file,null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
 $db->exec('CREATE TABLE players(id TEXT PRIMARY KEY,token_hash TEXT UNIQUE,name TEXT,created INTEGER);CREATE TABLE matches(id TEXT PRIMARY KEY,player_id TEXT,opponent TEXT,opponent_match TEXT)');
 foreach([['a','token-a','Sue',1],['b','token-b','SUE',2],['c','token-c','Bon',3]] as $row)sql($db,'INSERT INTO players VALUES(?,?,?,?)',$row);
 $db->exec("INSERT INTO matches VALUES('run-a','a','Bot',NULL),('run-b','b','Sue','run-a')");
 ensure_unique_names($db);ensure_avatar_column($db);ensure_unique_names($db);ensure_avatar_column($db);
 check((int)$db->query('SELECT COUNT(*) FROM players')->fetchColumn()===3,'Players lost');
 check((int)$db->query('SELECT COUNT(DISTINCT name_key) FROM players')->fetchColumn()===3,'Collision remains');
 check($db->query("SELECT name FROM players WHERE id='a'")->fetchColumn()==='Sue','First name not retained');
 check($db->query("SELECT token_hash FROM players WHERE id='b'")->fetchColumn()==='token-b','Account key changed');
 check((int)$db->query('SELECT COUNT(*) FROM matches')->fetchColumn()===2,'History lost');
 check(is_file($file.'.before-player-cards-v2.sqlite'),'Snapshot missing');
 $snapshot=new PDO('sqlite:'.$file.'.before-player-cards-v2.sqlite');
 check((int)$snapshot->query("SELECT COUNT(*) FROM players WHERE lower(name)='sue'")->fetchColumn()===2,'Snapshot not original');$snapshot=null;
 $duplicateRejected=false;try{sql($db,"UPDATE players SET name_key=? WHERE id='c'",[name_key('sue')]);}catch(PDOException $e){$duplicateRejected=$e->getCode()==='23000';}
 check($duplicateRejected,'Unique index not enforced');
 check(name_key('Straße')===name_key('STRASSE'),'Unicode folding differs');
 echo "PASS: repeatable migration, collision resolution, account/history preservation, consistent backup, Unicode folding and unique index\n";
} finally {$db=null;foreach([$file,$file.'.before-player-cards-v2.sqlite'] as $path)if(is_file($path))unlink($path);}
