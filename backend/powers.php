<?php
declare(strict_types=1);

// Coins and the once-per-type cap are Quizfolk rules. Surviving QuizUp
// recordings establish the names, not a reliable historical cap/coin tariff.
function power_schema(PDO $db):void {
    $db->exec('CREATE TABLE IF NOT EXISTS power_uses(context TEXT PRIMARY KEY,player_id TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,turn INTEGER NOT NULL,type TEXT NOT NULL,hidden TEXT NOT NULL,highlight INTEGER,first_wrong INTEGER,created INTEGER NOT NULL)');
    if(!in_array('question_key',array_column($db->query('PRAGMA table_info(power_uses)')->fetchAll(),'name'),true)) {
        try{$db->exec('ALTER TABLE power_uses ADD COLUMN question_key TEXT');}
        catch(PDOException $e){if(!in_array('question_key',array_column($db->query('PRAGMA table_info(power_uses)')->fetchAll(),'name'),true))throw $e;}
    }
    if(count(array_filter($db->query('PRAGMA table_info(power_uses)')->fetchAll(),fn($c)=>(int)$c['pk']>0))===1) {
        $db->exec('BEGIN IMMEDIATE');
        try {
            // Recheck after locking: another request may already have migrated it.
            if(count(array_filter($db->query('PRAGMA table_info(power_uses)')->fetchAll(),fn($c)=>(int)$c['pk']>0))===1) {
                $db->exec('CREATE TABLE power_uses_next(context TEXT NOT NULL,player_id TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,turn INTEGER NOT NULL,type TEXT NOT NULL,hidden TEXT NOT NULL,highlight INTEGER,first_wrong INTEGER,created INTEGER NOT NULL,question_key TEXT,PRIMARY KEY(context,type));
                    INSERT INTO power_uses_next SELECT context,player_id,turn,type,hidden,highlight,first_wrong,created,question_key FROM power_uses;
                    DROP TABLE power_uses; ALTER TABLE power_uses_next RENAME TO power_uses;');
            }
            $db->exec('COMMIT');
        } catch(Throwable $e) { $db->exec('ROLLBACK');throw $e; }
    }
}
function power_question_key(array $q):string {$parts=[$q['id'],$q['prompt'],$q['answers'],$q['correctIndex']];if(isset($q['imageSHA256']))$parts[]=$q['imageSHA256'];return hash('sha256',json_encode($parts));}
function power_state(PDO $db,string $context,int $turn,?array $q=null):array {
    $uses=sql($db,'SELECT * FROM power_uses WHERE context=? ORDER BY created,rowid',[$context])->fetchAll();
    $active=array_values(array_filter($uses,fn($p)=>(int)$p['turn']===$turn && (!$q || $p['question_key']===power_question_key($q))));
    $hidden=[];$highlight=null;$type=null;
    foreach($active as $p){$hidden=array_merge($hidden,json_decode($p['hidden'],true));$type=$p['type'];if($p['highlight']!==null)$highlight=(int)$p['highlight'];}
    return ['used'=>(bool)$uses,'usedTypes'=>array_column($uses,'type'),'activeTypes'=>array_column($active,'type'),'type'=>$type,'hidden'=>array_values(array_unique($hidden)),'highlight'=>$highlight];
}
function power_activate(PDO $db,string $pid,string $context,int $turn,array $q,?float $started,array $body,bool $allowed=true):array {
    if(!$allowed)fail('Power-ups are switched off for this friends tournament.',409);
    $elapsed=$started===null?10:microtime(true)-$started;
    if($elapsed<0 || $elapsed>=10)fail('Use a power-up while the answer clock is running.',409);
    if(($body['turn'] ?? null)!==$turn)fail('That question has already ended.',409);
    $type=(string)($body['type'] ?? '');$prices=['fifty'=>5,'double'=>10,'right'=>25];
    if(!isset($prices[$type]))fail('Choose a valid power-up.');
    $old=sql($db,'SELECT * FROM power_uses WHERE context=? AND type=?',[$context,$type])->fetch();
    if($old) {
        if($old['player_id']!==$pid || (int)$old['turn']!==$turn || $old['question_key']!==power_question_key($q))fail('Each power-up can be used once per duel or tournament run.',409);
    } else {
        $wallet=tournament_wallet($db,$pid);$price=$prices[$type];
        if($wallet['coins']<$price)fail('Not enough coins. This power-up costs '.$price.' coins.',409);
        $wrong=array_values(array_diff([0,1,2,3],[$q['correctIndex']]));shuffle($wrong);
        $hidden=$type==='fifty' ? array_slice($wrong,0,2):[];
        sql($db,'INSERT INTO power_uses(context,player_id,turn,type,hidden,highlight,created) VALUES(?,?,?,?,?,?,?)',[$context,$pid,$turn,$type,json_encode($hidden),$type==='right'?$q['correctIndex']:null,time()]);
        sql($db,'UPDATE power_uses SET question_key=? WHERE context=? AND type=?',[power_question_key($q),$context,$type]);
        tournament_credit($db,$pid,'power:'.$context.':'.$type,-$price,0);
    }
    return ['power'=>power_state($db,$context,$turn,$q),'remaining'=>max(0,10-(microtime(true)-$started)),'acceptedElapsed'=>$elapsed,'coins'=>tournament_wallet($db,$pid)['coins']];
}
// A first wrong Double Choice pick is hidden, not a submitted answer. Its
// original server clock keeps running; neither a retry nor a reload resets it.
function power_second_chance(PDO $db,string $context,int $turn,int $answer,int $correct,float $elapsed,array $q):bool {
    $p=sql($db,'SELECT * FROM power_uses WHERE context=? AND turn=? AND type="double"',[$context,$turn])->fetch();
    if(!$p || $p['question_key']!==power_question_key($q) || $answer<0 || $answer===$correct || $elapsed>=10)return false;
    if($p['first_wrong']!==null)return (int)$p['first_wrong']===$answer;
    sql($db,'UPDATE power_uses SET first_wrong=?,hidden=? WHERE context=? AND type="double"',[$answer,json_encode([$answer]),$context]);return true;
}
