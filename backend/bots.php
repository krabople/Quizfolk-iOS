<?php
declare(strict_types=1);

function next_bot_name(PDO $db,string $player):string {
    $names=json_decode(file_get_contents(dirname(__DIR__).'/data/bots.json'),true,512,JSON_THROW_ON_ERROR);
    $recent=sql($db,'SELECT opponent FROM matches WHERE player_id=? AND kind="bot" ORDER BY created DESC,rowid DESC LIMIT 5',[$player])->fetchAll(PDO::FETCH_COLUMN);
    $available=array_values(array_diff($names,$recent));
    return $available[random_int(0,count($available)-1)];
}
