<?php
declare(strict_types=1);

function social_schema(PDO $db):void {
    $columns=array_column($db->query('PRAGMA table_info(matches)')->fetchAll(),'name');if(in_array('duel_id',$columns,true) && in_array('preview_started',$columns,true))return;
    $file=$db->query('PRAGMA database_list')->fetch()['file'];$backup=$file.'.before-social-v1.sqlite';
    if($file && !is_file($backup) && (int)$db->query('SELECT COUNT(*) FROM players')->fetchColumn()>0) {
        try{$db->exec('VACUUM INTO '.$db->quote($backup));}catch(PDOException $e){if(!is_file($backup))throw $e;}
    }
    $db->exec('BEGIN IMMEDIATE');
    if(!in_array('duel_id',array_column($db->query('PRAGMA table_info(matches)')->fetchAll(),'name'),true)) {
        $db->exec('ALTER TABLE matches ADD COLUMN duel_id TEXT; ALTER TABLE matches ADD COLUMN opponent_id TEXT;
        CREATE TABLE social_settings(player_id TEXT PRIMARY KEY REFERENCES players(id) ON DELETE CASCADE,interests TEXT NOT NULL DEFAULT "[]",title_id TEXT NOT NULL DEFAULT "newcomer",discoverable INTEGER NOT NULL DEFAULT 1,challenges_open INTEGER NOT NULL DEFAULT 1);
        CREATE TABLE follows(player_id TEXT REFERENCES players(id) ON DELETE CASCADE,target_id TEXT REFERENCES players(id) ON DELETE CASCADE,created INTEGER NOT NULL,PRIMARY KEY(player_id,target_id));
        CREATE INDEX follows_target ON follows(target_id);
        CREATE TABLE blocks(player_id TEXT REFERENCES players(id) ON DELETE CASCADE,target_id TEXT REFERENCES players(id) ON DELETE CASCADE,created INTEGER NOT NULL,PRIMARY KEY(player_id,target_id));
        CREATE TABLE duels(id TEXT PRIMARY KEY,creator_id TEXT,target_id TEXT,topic TEXT NOT NULL,packet TEXT NOT NULL,creator_match TEXT UNIQUE,target_match TEXT UNIQUE,status TEXT NOT NULL,created INTEGER NOT NULL,expires INTEGER NOT NULL,request_key TEXT UNIQUE);
        CREATE INDEX duels_creator ON duels(creator_id,created); CREATE INDEX duels_target ON duels(target_id,created);
        CREATE TABLE searches(id TEXT PRIMARY KEY,player_id TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,topic TEXT NOT NULL,created REAL NOT NULL,expires REAL NOT NULL,match_id TEXT,cancelled INTEGER NOT NULL DEFAULT 0);
        CREATE INDEX searches_waiting ON searches(topic,cancelled,expires);
        CREATE INDEX matches_duel ON matches(duel_id);');
        $db->exec('UPDATE matches SET opponent_id=(SELECT source.player_id FROM matches source WHERE source.id=matches.opponent_match) WHERE opponent_match IS NOT NULL');
    }
    if(!in_array('preview_started',array_column($db->query('PRAGMA table_info(matches)')->fetchAll(),'name'),true))$db->exec('ALTER TABLE matches ADD COLUMN preview_started REAL');
    $db->exec('COMMIT');
}
function blocked(PDO $db,string $a,string $b):bool {return (bool)sql($db,'SELECT 1 FROM blocks WHERE (player_id=? AND target_id=?) OR (player_id=? AND target_id=?)',[$a,$b,$b,$a])->fetch();}
function visible_player(PDO $db,string $viewer,string $id):array {
    $p=sql($db,'SELECT id,name,avatar,created FROM players WHERE id=?',[$id])->fetch();
    if(!$p || ($viewer!==$id && blocked($db,$viewer,$id)))fail('Player not found',404);return $p;
}
function settings(PDO $db,string $id):array {
    sql($db,'INSERT OR IGNORE INTO social_settings(player_id) VALUES(?)',[$id]);return sql($db,'SELECT * FROM social_settings WHERE player_id=?',[$id])->fetch();
}
function online_stats(PDO $db,string $id):array {
    $s=sql($db,'SELECT COUNT(*) matches,COALESCE(SUM(score>opponent_score),0) wins,COALESCE(SUM(score=opponent_score),0) draws,COALESCE(SUM(score+40+CASE WHEN score>opponent_score THEN 100 WHEN score=opponent_score THEN 50 ELSE 0 END),0) xp FROM matches WHERE player_id=? AND completed IS NOT NULL',[$id])->fetch();
    foreach($s as &$v)$v=(int)$v;unset($v);$s['correct']=0;$s['answered']=0;$s['perfect']=0;
    foreach(sql($db,'SELECT answers FROM matches WHERE player_id=? AND completed IS NOT NULL',[$id])->fetchAll() as $row) {
        $a=json_decode($row['answers'],true);$right=count(array_filter($a,fn($x)=>$x['correct']));$s['correct']+=$right;$s['answered']+=count($a);if($right===7)$s['perfect']++;
    }
    return $s;
}
function topic_stats(PDO $db,string $id):array {
    return array_map(fn($r)=>['topicID'=>$r['topic'],'xp'=>(int)$r['xp'],'level'=>1+(int)floor((int)$r['xp']/300),'matches'=>(int)$r['matches'],'wins'=>(int)$r['wins']],sql($db,'SELECT topic,COUNT(*) matches,SUM(score>opponent_score) wins,SUM(score+40+CASE WHEN score>opponent_score THEN 100 WHEN score=opponent_score THEN 50 ELSE 0 END) xp FROM matches WHERE player_id=? AND completed IS NOT NULL GROUP BY topic ORDER BY xp DESC',[$id])->fetchAll());
}
function earned_titles(array $topics):array {
    $all=[['id'=>'newcomer','name'=>'Newcomer']];$names=[];foreach(json_decode(file_get_contents(dirname(__DIR__).'/data/categories.json'),true) as $t)$names[$t['id']]=$t['name'];
    foreach($topics as $t)foreach([10=>'Scholar',20=>'Expert',30=>'Sage',40=>'Master',50=>'Legend'] as $level=>$label)if($t['level']>=$level)$all[]=['id'=>$t['topicID'].':'.$level,'name'=>($names[$t['topicID']] ?? 'Topic').' '.$label];return $all;
}
function player_summary(PDO $db,string $viewer,array $p):array {
    $pref=settings($db,$p['id']);$mine=settings($db,$viewer);$stats=online_stats($db,$p['id']);$topics=topic_stats($db,$p['id']);$titles=earned_titles($topics);$title='Newcomer';foreach($titles as $t)if($t['id']===$pref['title_id'])$title=$t['name'];
    $interest=json_decode($pref['interests'],true);$shared=array_values(array_intersect($interest,json_decode($mine['interests'],true)));
    return ['id'=>$p['id'],'name'=>$p['name'],'avatar'=>$p['avatar'],'title'=>$title,'interests'=>$interest,'sharedTopics'=>$shared,'following'=>(bool)sql($db,'SELECT 1 FROM follows WHERE player_id=? AND target_id=?',[$viewer,$p['id']])->fetch(),'followers'=>(int)sql($db,'SELECT COUNT(*) FROM follows WHERE target_id=?',[$p['id']])->fetchColumn(),'followingCount'=>(int)sql($db,'SELECT COUNT(*) FROM follows WHERE player_id=?',[$p['id']])->fetchColumn(),'canChallenge'=>$viewer!==$p['id'] && (bool)$pref['challenges_open'],'stats'=>$stats,'topics'=>$topics,'titles'=>$titles,'selectedTitle'=>$pref['title_id'],'discoverable'=>(bool)$pref['discoverable'],'challengesOpen'=>(bool)$pref['challenges_open']];
}
function fresh_packet(PDO $db,string $pid,string $topic):array {
    $qdb=new PDO('sqlite:'.dirname(__DIR__).'/data/question-bank.sqlite',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
    $bank=array_map(fn($r)=>json_decode($r['payload'],true),sql($qdb,'SELECT payload FROM questions WHERE category_id=?',[$topic])->fetchAll());if(count($bank)<7)fail('Unknown topic');
    $seen=[];foreach(sql($db,'SELECT packet FROM matches WHERE player_id=? AND topic=? ORDER BY created DESC LIMIT 100',[$pid,$topic])->fetchAll() as $old)foreach(json_decode($old['packet'],true) as $q)$seen[$q['id']]=true;
    shuffle($bank);usort($bank,fn($a,$b)=>(int)isset($seen[$a['id']])<=>(int)isset($seen[$b['id']]));$packet=array_slice($bank,0,7);
    foreach($packet as &$q){$i=[0,1,2,3];shuffle($i);$q['answers']=array_map(fn($n)=>$q['answers'][$n],$i);$q['correctIndex']=array_search($q['correctIndex'],$i,true);}unset($q);return $packet;
}
function match_limit(PDO $db,string $pid):void {if((int)sql($db,'SELECT COUNT(*) FROM matches WHERE player_id=? AND created>?',[$pid,time()-3600])->fetchColumn()>=30)fail('You have reached the hourly duel limit',429);}
function insert_match(PDO $db,string $pid,string $topic,string $kind,string $opponent,?string $otherID,array $packet,array $points,?string $duelID=null,?string $replayID=null):string {
    match_limit($db,$pid);$id=bin2hex(random_bytes(12));sql($db,'INSERT INTO matches(id,player_id,topic,kind,opponent,opponent_id,duel_id,opponent_match,packet,opponent_points,created) VALUES(?,?,?,?,?,?,?,?,?,?,?)',[$id,$pid,$topic,$kind,$opponent,$otherID,$duelID,$replayID,json_encode($packet,JSON_UNESCAPED_UNICODE),json_encode($points),time()]);return $id;
}
function start_info(PDO $db,array $m):array {
    $p=$m['opponent_id'] ? sql($db,'SELECT id,name,avatar FROM players WHERE id=?',[$m['opponent_id']])->fetch():false;
    $packet=json_decode($m['packet'],true);$a=json_decode($m['answers'],true);$op=json_decode($m['opponent_points'],true);$played=[];
    foreach($a as $i=>$r)$played[]=['question'=>$packet[$i],'selected'=>$r['selected'],'elapsed'=>$r['elapsed'],'points'=>$r['points'],'opponentPoints'=>$op[$i]];
    return ['id'=>$m['id'],'kind'=>$m['kind'],'opponent'=>$p ? $p['name']:$m['opponent'],'opponentID'=>$p ? $p['id']:null,'opponentAvatar'=>$p ? $p['avatar']:null,'duelID'=>$m['duel_id'],'pending'=>$m['duel_id']!==null && $m['completed']===null,'played'=>$played,'score'=>(int)$m['score'],'opponentScore'=>(int)$m['opponent_score']];
}
function replay_candidate(PDO $db,string $pid,string $topic,array $config):array|false {
    return sql($db,'SELECT m.*,p.name,p.avatar FROM matches m JOIN players p ON p.id=m.player_id WHERE m.topic=? AND m.player_id<>? AND m.completed>? AND m.created>=? AND NOT EXISTS(SELECT 1 FROM matches used WHERE used.player_id=? AND used.opponent_match=m.id) AND NOT EXISTS(SELECT 1 FROM blocks b WHERE (b.player_id=? AND b.target_id=p.id) OR (b.player_id=p.id AND b.target_id=?)) ORDER BY m.completed DESC LIMIT 1',[$topic,$pid,time()-2592000,(int)($config['minimum_replay_created'] ?? 0),$pid,$pid,$pid])->fetch();
}
function create_random_match(PDO $db,string $pid,string $topic,array $config,bool $humanOnly=false):?array {
    $replay=replay_candidate($db,$pid,$topic,$config);
    if($replay){$packet=json_decode($replay['packet'],true);$other=array_column(json_decode($replay['answers'],true),'points');$id=insert_match($db,$pid,$topic,'human',$replay['name'],$replay['player_id'],$packet,$other,null,$replay['id']);}
    else {
        if($humanOnly)return null;$packet=fresh_packet($db,$pid,$topic);$other=[];
        foreach($packet as $i=>$q){$chance=match($q['difficulty']){'easy'=>83,'hard'=>45,default=>65};$other[]=points(random_int(1,100)<=$chance,random_int(1200,9800)/1000,$i);}
        $id=insert_match($db,$pid,$topic,'bot','Pip · Bot',null,$packet,$other);
    }
    return start_info($db,sql($db,'SELECT * FROM matches WHERE id=?',[$id])->fetch());
}
function create_duel(PDO $db,string $creator,string $target,string $topic,string $requestKey,bool $paired=false):array {
    if($creator===$target)fail('Choose another player');$a=visible_player($db,$creator,$creator);$b=visible_player($db,$creator,$target);
    if(!$paired && !settings($db,$target)['challenges_open'])fail('This player is not accepting challenges',403);
    $old=sql($db,'SELECT * FROM duels WHERE request_key=?',[$requestKey])->fetch();if($old){if($old['target_id']!==$target || $old['topic']!==$topic)fail('This challenge request was already used',409);return $old;}
    if(!$paired && (int)sql($db,'SELECT COUNT(*) FROM duels WHERE creator_id=? AND created>?',[$creator,time()-3600])->fetchColumn()>=15)fail('Please wait before sending more challenges',429);
    if(!$paired && (int)sql($db,'SELECT COUNT(*) FROM duels WHERE creator_id=? AND target_id=? AND topic=? AND status IN ("invited","accepted")',[$creator,$target,$topic])->fetchColumn()>=2)fail('You already have open challenges with this player in this topic',409);
    $id=bin2hex(random_bytes(12));$packet=fresh_packet($db,$creator,$topic);$am=insert_match($db,$creator,$topic,'challenge',$b['name'],$target,$packet,array_fill(0,7,0),$id);
    $bm=$paired ? insert_match($db,$target,$topic,'challenge',$a['name'],$creator,$packet,array_fill(0,7,0),$id):null;
    sql($db,'INSERT INTO duels VALUES(?,?,?,?,?,?,?,?,?,?,?)',[$id,$creator,$target,$topic,json_encode($packet,JSON_UNESCAPED_UNICODE),$am,$bm,$paired?'accepted':'invited',time(),time()+1209600,$requestKey]);
    return sql($db,'SELECT * FROM duels WHERE id=?',[$id])->fetch();
}
function settle_duel(PDO $db,string $id):bool {
    $d=sql($db,'SELECT * FROM duels WHERE id=?',[$id])->fetch();if(!$d || $d['status']!=='accepted' || !$d['target_match'])return false;
    $a=sql($db,'SELECT * FROM matches WHERE id=?',[$d['creator_match']])->fetch();$b=sql($db,'SELECT * FROM matches WHERE id=?',[$d['target_match']])->fetch();
    if(!$a || !$b || count(json_decode($a['answers'],true))!==7 || count(json_decode($b['answers'],true))!==7)return false;
    foreach([[$a,$b],[$b,$a]] as [$own,$other])sql($db,'UPDATE matches SET opponent_score=?,opponent_points=?,completed=? WHERE id=?',[(int)$other['score'],json_encode(array_column(json_decode($other['answers'],true),'points')),time(),$own['id']]);
    sql($db,'UPDATE duels SET status="complete" WHERE id=?',[$id]);return true;
}
function duel_card(PDO $db,string $pid,array $d):array {
    $creator=$d['creator_id']===$pid;$otherID=$creator?$d['target_id']:$d['creator_id'];$other=$otherID ? sql($db,'SELECT id,name,avatar FROM players WHERE id=?',[$otherID])->fetch():false;
    $mid=$creator?$d['creator_match']:$d['target_match'];$opMid=$creator?$d['target_match']:$d['creator_match'];$m=$mid ? sql($db,'SELECT * FROM matches WHERE id=?',[$mid])->fetch():false;$o=$opMid ? sql($db,'SELECT * FROM matches WHERE id=?',[$opMid])->fetch():false;
    $done=$m && count(json_decode($m['answers'],true))===7;
    return ['id'=>$d['id'],'topicID'=>$d['topic'],'opponentID'=>$other?$other['id']:null,'opponent'=>$other?$other['name']:'Former player','avatar'=>$other?$other['avatar']:null,'status'=>$d['status'],'incoming'=>!$creator,'accepted'=>$d['status']!=='invited','ownFinished'=>(bool)$done,'opponentFinished'=>$o ? count(json_decode($o['answers'],true))===7:false,'score'=>$m?(int)$m['score']:0,'opponentScore'=>$d['status']==='complete' && $o ? (int)$o['score']:null,'created'=>(int)$d['created'],'expires'=>(int)$d['expires'],'matchID'=>$mid];
}
function delete_social_player(PDO $db,string $pid):void {
    sql($db,'UPDATE duels SET status=CASE WHEN status="complete" THEN status ELSE "cancelled" END,creator_id=CASE WHEN creator_id=? THEN NULL ELSE creator_id END,target_id=CASE WHEN target_id=? THEN NULL ELSE target_id END,request_key=NULL WHERE creator_id=? OR target_id=?',[$pid,$pid,$pid,$pid]);
    sql($db,'UPDATE matches SET opponent="Former player",opponent_id=NULL WHERE opponent_id=?',[$pid]);
}
function social_routes(string $route,PDO $db,string $pid,array $player,array $body,array $config):void {
    sql($db,'UPDATE duels SET status="expired" WHERE status IN ("invited","accepted") AND expires<?',[time()]);
    if($route==='people') {
        $mode=(string)($_GET['mode'] ?? 'discover');$needle=trim((string)($_GET['q'] ?? ''));$where='p.id<>?';$args=[$pid];if($mode==='discover'){$where.=' AND COALESCE(s.discoverable,1)=1';if($needle==='')$where.=" AND (COALESCE(s.interests,'[]')<>'[]' OR p.name NOT LIKE 'Explorer-%' OR EXISTS(SELECT 1 FROM matches m WHERE m.player_id=p.id AND m.completed IS NOT NULL))";}
        if($mode==='following'){$where.=' AND EXISTS(SELECT 1 FROM follows f WHERE f.player_id=? AND f.target_id=p.id)';$args[]=$pid;}
        if($mode==='followers'){$where.=' AND EXISTS(SELECT 1 FROM follows f WHERE f.target_id=? AND f.player_id=p.id)';$args[]=$pid;}
        if($mode==='blocked'){$where='p.id IN (SELECT target_id FROM blocks WHERE player_id=?)';$args=[$pid];}
        else {$where.=' AND NOT EXISTS(SELECT 1 FROM blocks b WHERE (b.player_id=? AND b.target_id=p.id) OR (b.player_id=p.id AND b.target_id=?))';$args[]=$pid;$args[]=$pid;}
        if($needle!==''){$key=name_key($needle);$where.=' AND p.name_key LIKE ? ESCAPE \'\\\'';$args[]='%'.strtr($key,['\\'=>'\\\\','%'=>'\\%','_'=>'\\_']).'%';}
        $rows=sql($db,'SELECT p.id,p.name,p.avatar FROM players p LEFT JOIN social_settings s ON s.player_id=p.id WHERE '.$where.' ORDER BY p.name_key LIMIT 40',$args)->fetchAll();
        $cards=array_map(fn($p)=>player_summary($db,$pid,$p),$rows);if($mode==='discover' && $needle==='')usort($cards,fn($a,$b)=>count($b['sharedTopics'])<=>count($a['sharedTopics']));
        out(['players'=>$cards]);
    }
    if($route==='player') {
        $id=(string)($_GET['id'] ?? $pid);$p=visible_player($db,$pid,$id);$card=player_summary($db,$pid,$p);
        $h=['games'=>0,'wins'=>0,'draws'=>0,'losses'=>0];
        if($id!==$pid) {
            $rows=sql($db,'SELECT a.score own,b.score other FROM duels d JOIN matches a ON a.duel_id=d.id AND a.player_id=? JOIN matches b ON b.duel_id=d.id AND b.player_id=? WHERE d.status="complete" UNION ALL SELECT CASE WHEN player_id=? THEN score ELSE opponent_score END own,CASE WHEN player_id=? THEN opponent_score ELSE score END other FROM matches WHERE kind="human" AND completed IS NOT NULL AND ((player_id=? AND opponent_id=?) OR (player_id=? AND opponent_id=?))',[$pid,$id,$pid,$pid,$pid,$id,$id,$pid])->fetchAll();
            foreach($rows as $v){$h['games']++;$h[$v['own']>$v['other']?'wins':($v['own']===$v['other']?'draws':'losses')]++;}
        }
        $card['headToHead']=$h;
        $st=$card['stats'];$card['badges']=[['id'=>'first','name'=>'First duel','symbol'=>'bolt.fill','earned'=>$st['matches']>=1],['id'=>'winner','name'=>'First victory','symbol'=>'trophy.fill','earned'=>$st['wins']>=1],['id'=>'perfect','name'=>'Seven of seven','symbol'=>'checkmark.seal.fill','earned'=>$st['perfect']>=1],['id'=>'ten','name'=>'Tenacious','symbol'=>'flame.fill','earned'=>$st['matches']>=10],['id'=>'explorer','name'=>'Topic explorer','symbol'=>'globe','earned'=>count($card['topics'])>=5]];
        $topicNames=array_column(json_decode(file_get_contents(dirname(__DIR__).'/data/categories.json'),true),'name','id');
        foreach(sql($db,'SELECT p.event_id,p.rank,e.topic,e.starts FROM tournament_places p JOIN tournament_events e ON e.id=p.event_id WHERE p.player_id=? AND p.reward>0 ORDER BY e.ends DESC LIMIT 20',[$id])->fetchAll() as $trophy) {
            $card['badges'][]=['id'=>'tournament:'.$trophy['event_id'],'name'=>($topicNames[$trophy['topic']] ?? 'Tournament').' · #'.$trophy['rank'].' · '.gmdate('j M Y',(int)$trophy['starts']),'symbol'=>'trophy.fill','earned'=>true];
        }
        out($card);
    }
    if($route==='social-settings') {
        $current=settings($db,$pid);$interests=$body['interests'] ?? json_decode($current['interests'],true);$ids=array_column(json_decode(file_get_contents(dirname(__DIR__).'/data/categories.json'),true),'id');
        if(!is_array($interests) || count($interests)>30 || array_diff($interests,$ids))fail('Choose valid topics');$interests=array_values(array_unique($interests));
        $title=(string)($body['titleID'] ?? $current['title_id']);if(!in_array($title,array_column(earned_titles(topic_stats($db,$pid)),'id'),true))fail('That title has not been earned',403);
        $discoverable=$body['discoverable'] ?? (bool)$current['discoverable'];$open=$body['challengesOpen'] ?? (bool)$current['challenges_open'];if(!is_bool($discoverable)||!is_bool($open))fail('Invalid preferences');
        sql($db,'UPDATE social_settings SET interests=?,title_id=?,discoverable=?,challenges_open=? WHERE player_id=?',[json_encode($interests),$title,(int)$discoverable,(int)$open,$pid]);out(['ok'=>true]);
    }
    if($route==='follow' || $route==='block') {
        $id=(string)($body['player'] ?? '');if($pid===$id)fail('Choose another player');$on=$body['enabled'] ?? true;if(!is_bool($on))fail('Invalid choice');
        if($route==='follow') {visible_player($db,$pid,$id);if($on)sql($db,'INSERT OR IGNORE INTO follows VALUES(?,?,?)',[$pid,$id,time()]);else sql($db,'DELETE FROM follows WHERE player_id=? AND target_id=?',[$pid,$id]);}
        else {
            if(!sql($db,'SELECT 1 FROM players WHERE id=?',[$id])->fetch())fail('Player not found',404);
            $db->exec('BEGIN IMMEDIATE');if($on){sql($db,'INSERT OR IGNORE INTO blocks VALUES(?,?,?)',[$pid,$id,time()]);sql($db,'DELETE FROM follows WHERE (player_id=? AND target_id=?) OR (player_id=? AND target_id=?)',[$pid,$id,$id,$pid]);sql($db,'UPDATE duels SET status="cancelled" WHERE status IN ("invited","accepted") AND ((creator_id=? AND target_id=?) OR (creator_id=? AND target_id=?))',[$pid,$id,$id,$pid]);}else sql($db,'DELETE FROM blocks WHERE player_id=? AND target_id=?',[$pid,$id]);$db->exec('COMMIT');
        }out(['ok'=>true]);
    }
    if($route==='activity') {
        $rows=sql($db,'SELECT m.id,m.player_id,p.name,p.avatar,m.topic,m.score,m.opponent_score,m.completed FROM matches m JOIN players p ON p.id=m.player_id JOIN follows f ON f.target_id=m.player_id AND f.player_id=? WHERE m.completed IS NOT NULL AND NOT EXISTS(SELECT 1 FROM blocks b WHERE (b.player_id=? AND b.target_id=p.id) OR (b.player_id=p.id AND b.target_id=?)) ORDER BY m.completed DESC LIMIT 30',[$pid,$pid,$pid])->fetchAll();
        out(['events'=>array_map(fn($r)=>['id'=>$r['id'],'playerID'=>$r['player_id'],'name'=>$r['name'],'avatar'=>$r['avatar'],'topicID'=>$r['topic'],'score'=>(int)$r['score'],'won'=>$r['score']>$r['opponent_score'],'draw'=>$r['score']===$r['opponent_score'],'date'=>(int)$r['completed']],$rows)]);
    }
    if($route==='challenge') {
        $key=(string)($body['requestID'] ?? '');if(!preg_match('/^[A-Za-z0-9-]{16,64}$/D',$key))fail('A request identifier is required');
        $db->exec('BEGIN IMMEDIATE');$d=create_duel($db,$pid,(string)($body['player'] ?? ''),(string)($body['topic'] ?? ''),$pid.':'.$key);$m=sql($db,'SELECT * FROM matches WHERE id=?',[$d['creator_match']])->fetch();$db->exec('COMMIT');out(start_info($db,$m),201);
    }
    if($route==='duels') {
        $rows=sql($db,'SELECT * FROM duels WHERE creator_id=? OR target_id=? ORDER BY created DESC,id DESC LIMIT 100',[$pid,$pid])->fetchAll();out(['duels'=>array_map(fn($d)=>duel_card($db,$pid,$d),$rows)]);
    }
    if($route==='duel-open' || $route==='duel-decline') {
        $db->exec('BEGIN IMMEDIATE');$d=sql($db,'SELECT * FROM duels WHERE id=? AND (creator_id=? OR target_id=?)',[(string)($body['duel'] ?? ''),$pid,$pid])->fetch();if(!$d)fail('Challenge not found',404);
        if(!in_array($d['status'],['invited','accepted','complete'],true))fail('This challenge is '.$d['status'],410);
        if($route==='duel-decline'){if($d['target_id']!==$pid || $d['status']!=='invited')fail('This challenge cannot be declined',409);sql($db,'UPDATE duels SET status="declined" WHERE id=?',[$d['id']]);$db->exec('COMMIT');out(['ok'=>true]);}
        $mine=$d['creator_id']===$pid?$d['creator_match']:$d['target_match'];
        if(!$mine){$other=visible_player($db,$pid,(string)$d['creator_id']);$mine=insert_match($db,$pid,$d['topic'],'challenge',$other['name'],$other['id'],json_decode($d['packet'],true),array_fill(0,7,0),$d['id']);sql($db,'UPDATE duels SET target_match=?,status="accepted" WHERE id=?',[$mine,$d['id']]);}
        $m=sql($db,'SELECT * FROM matches WHERE id=? AND player_id=?',[$mine,$pid])->fetch();$db->exec('COMMIT');out(start_info($db,$m));
    }
    if($route==='match-search') {
        $key=(string)($body['requestID'] ?? '');$topic=(string)($body['topic'] ?? '');if(!preg_match('/^[A-Za-z0-9-]{16,64}$/D',$key))fail('A request identifier is required');
        $id=substr(hash('sha256',$pid.':'.$key),0,24);$db->exec('BEGIN IMMEDIATE');$s=sql($db,'SELECT * FROM searches WHERE id=?',[$id])->fetch();
        if(!$s){fresh_packet($db,$pid,$topic);sql($db,'UPDATE searches SET cancelled=1 WHERE player_id=? AND match_id IS NULL',[$pid]);sql($db,'INSERT INTO searches(id,player_id,topic,created,expires) VALUES(?,?,?,?,?)',[$id,$pid,$topic,microtime(true),microtime(true)+90]);$s=sql($db,'SELECT * FROM searches WHERE id=?',[$id])->fetch();}
        if($s['topic']!==$topic)fail('Search topic changed',409);if($s['cancelled'] || (float)$s['expires']<microtime(true))fail('Search expired; please try again',410);
        $m=$s['match_id'] ? sql($db,'SELECT * FROM matches WHERE id=? AND player_id=?',[$s['match_id'],$pid])->fetch():null;
        if(!$m){
            $waiting=sql($db,'SELECT s.* FROM searches s WHERE s.topic=? AND s.player_id<>? AND s.cancelled=0 AND s.match_id IS NULL AND s.expires>? AND NOT EXISTS(SELECT 1 FROM blocks b WHERE (b.player_id=? AND b.target_id=s.player_id) OR (b.player_id=s.player_id AND b.target_id=?)) ORDER BY s.created LIMIT 1',[$topic,$pid,microtime(true),$pid,$pid])->fetch();
            if($waiting){$d=create_duel($db,$waiting['player_id'],$pid,$topic,'queue:'.$waiting['id'].':'.$id,true);sql($db,'UPDATE searches SET match_id=? WHERE id=?',[$d['creator_match'],$waiting['id']]);sql($db,'UPDATE searches SET match_id=? WHERE id=?',[$d['target_match'],$id]);$m=sql($db,'SELECT * FROM matches WHERE id=?',[$d['target_match']])->fetch();}
            else {$r=create_random_match($db,$pid,$topic,$config,true);if(!$r && microtime(true)-(float)$s['created']>=6)$r=create_random_match($db,$pid,$topic,$config);if($r){sql($db,'UPDATE searches SET match_id=? WHERE id=?',[$r['id'],$id]);$m=sql($db,'SELECT * FROM matches WHERE id=?',[$r['id']])->fetch();}}
        }
        $db->exec('COMMIT');out(['searchID'=>$id,'state'=>$m?'matched':'searching','elapsed'=>max(0,microtime(true)-(float)$s['created']),'match'=>$m?start_info($db,$m):null]);
    }
    if($route==='cancel-search'){sql($db,'UPDATE searches SET cancelled=1 WHERE id=? AND player_id=? AND match_id IS NULL',[(string)($body['searchID'] ?? ''),$pid]);out(['ok'=>true]);}
}
