<?php
declare(strict_types=1);
require dirname(__DIR__).'/backend/powers.php';
function sql(PDO $db,string $query,array $args=[]):PDOStatement {$s=$db->prepare($query);$s->execute($args);return $s;}
$db=new PDO('sqlite::memory:',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
$db->exec('PRAGMA foreign_keys=ON; CREATE TABLE players(id TEXT PRIMARY KEY); INSERT INTO players VALUES("player");
 CREATE TABLE power_uses(context TEXT PRIMARY KEY,player_id TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,turn INTEGER NOT NULL,type TEXT NOT NULL,hidden TEXT NOT NULL,highlight INTEGER,first_wrong INTEGER,created INTEGER NOT NULL);
 INSERT INTO power_uses VALUES("match:old","player",0,"double","[1]",NULL,1,123);');
power_schema($db);power_schema($db);
$old=$db->query('SELECT * FROM power_uses')->fetch();
if($old['first_wrong']!==1 || $old['created']!==123)throw new RuntimeException('Migration lost existing use');
$db->exec('INSERT INTO power_uses(context,player_id,turn,type,hidden,created) VALUES("match:old","player",1,"fifty","[2,3]",124)');
$state=power_state($db,'match:old',1);
if($state['usedTypes']!==['double','fifty'] || $state['hidden']!==[2,3])throw new RuntimeException('Per-type state is incorrect');
try{$db->exec('INSERT INTO power_uses(context,player_id,turn,type,hidden,created) VALUES("match:old","player",2,"fifty","[]",125)');throw new RuntimeException('Duplicate type accepted');}catch(PDOException $e){}
$db->exec('DELETE FROM players');
if((int)$db->query('SELECT COUNT(*) FROM power_uses')->fetchColumn()!==0)throw new RuntimeException('Account deletion did not cascade');
echo "PASS: legacy power uses preserved, migration idempotent, per-type uniqueness and deletion cascade\n";
