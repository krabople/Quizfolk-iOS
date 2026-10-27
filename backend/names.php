<?php
declare(strict_types=1);
function clean_name(string $name):string {
    if(class_exists('Normalizer')) $name=Normalizer::normalize($name,Normalizer::FORM_KC) ?: $name;
    $name=preg_replace('/\s+/u',' ',trim($name)) ?? '';
    if(!preg_match('/^[\p{L}\p{N} _-]{3,24}$/uD',$name)) fail('Use 3–24 letters or numbers; spaces, underscores and hyphens are allowed.');
    return $name;
}
function name_key(string $name):string {
    static $fold=null;
    if($fold===null)$fold=json_decode(file_get_contents(__DIR__.'/name-fold.json'),true,512,JSON_THROW_ON_ERROR);
    return strtr(preg_replace('/\s+/u',' ',trim($name)) ?? '',$fold);
}
function automatic_name():string {return 'Explorer-'.strtoupper(bin2hex(random_bytes(5)));}
function ensure_unique_names(PDO $db):void {
    $columns=array_column($db->query('PRAGMA table_info(players)')->fetchAll(),'name');
    if(in_array('name_key',$columns,true))return;
    // Take a consistent SQLite snapshot before changing an existing player table.
    $file=$db->query('PRAGMA database_list')->fetch()['file'];
    $backup=$file.'.before-player-cards-v2.sqlite';
    if($file && !is_file($backup) && (int)$db->query('SELECT COUNT(*) FROM players')->fetchColumn()>0) {
        try {$db->exec('VACUUM INTO '.$db->quote($backup));}
        catch(PDOException $e){if(!is_file($backup))throw $e;}
    }
    $db->exec('BEGIN IMMEDIATE');
    // Recheck after taking the lock: another request may already have migrated.
    $columns=array_column($db->query('PRAGMA table_info(players)')->fetchAll(),'name');
    if(!in_array('name_key',$columns,true)) {
        $db->exec('ALTER TABLE players ADD COLUMN name_key TEXT');$used=[];
        foreach($db->query('SELECT id,name FROM players ORDER BY created,id')->fetchAll() as $p) {
            $name=$p['name'];if(!preg_match('/^[\p{L}\p{N} _-]{3,24}$/uD',$name))$name=automatic_name();
            $key=name_key($name);
            if(isset($used[$key])) {$name='Explorer-'.strtoupper(substr($p['id'],-10));$key=name_key($name);}
            while(isset($used[$key])) {$name=automatic_name();$key=name_key($name);}
            $used[$key]=true;sql($db,'UPDATE players SET name=?,name_key=? WHERE id=?',[$name,$key,$p['id']]);
            sql($db,'UPDATE matches SET opponent=? WHERE opponent_match IN (SELECT id FROM matches WHERE player_id=?)',[$name,$p['id']]);
        }
        $db->exec('CREATE UNIQUE INDEX players_unique_name ON players(name_key)');
    }
    $db->exec('COMMIT');
}

function ensure_avatar_column(PDO $db):void {
    if(in_array('avatar',array_column($db->query('PRAGMA table_info(players)')->fetchAll(),'name'),true))return;
    $db->exec('BEGIN IMMEDIATE');
    if(!in_array('avatar',array_column($db->query('PRAGMA table_info(players)')->fetchAll(),'name'),true))$db->exec('ALTER TABLE players ADD COLUMN avatar TEXT');
    $db->exec('COMMIT');
}
