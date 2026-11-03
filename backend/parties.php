<?php
declare(strict_types=1);

function party_schema(PDO $db):void {
    $db->exec('CREATE TABLE IF NOT EXISTS parties(id TEXT PRIMARY KEY REFERENCES tournament_events(id),host TEXT NOT NULL,code TEXT NOT NULL UNIQUE,name TEXT NOT NULL,cycles INTEGER NOT NULL,days INTEGER NOT NULL,powers INTEGER NOT NULL,status TEXT NOT NULL,created INTEGER NOT NULL,request_key TEXT UNIQUE NOT NULL);
      CREATE TABLE IF NOT EXISTS party_members(party_id TEXT REFERENCES parties(id),player_id TEXT REFERENCES players(id) ON DELETE CASCADE,topic TEXT NOT NULL,run_id TEXT NOT NULL,PRIMARY KEY(party_id,player_id));
      CREATE TABLE IF NOT EXISTS party_fixtures(id TEXT PRIMARY KEY,party_id TEXT NOT NULL REFERENCES parties(id),a TEXT NOT NULL,b TEXT NOT NULL,topic TEXT NOT NULL,cycle INTEGER NOT NULL,home TEXT NOT NULL,duel_id TEXT UNIQUE);
      CREATE INDEX IF NOT EXISTS party_member_player ON party_members(player_id,party_id);
      CREATE INDEX IF NOT EXISTS party_fixture_room ON party_fixtures(party_id)');
}
function party_require(PDO $db,string $pid,string $id):array {
    $r=sql($db,'SELECT p.*,e.ends FROM parties p JOIN tournament_events e ON e.id=p.id JOIN party_members m ON m.party_id=p.id AND m.player_id=? WHERE p.id=?',[$pid,$id])->fetch();
    if(!$r)fail('Friends tournament not found',404);return $r;
}
function party_cancel(PDO $db,array $p):void {
    if($p['status']!=='lobby')return;
    foreach(sql($db,'SELECT * FROM party_members WHERE party_id=?',[$p['id']])->fetchAll() as $m)tournament_credit($db,$m['player_id'],'party-refund:'.$m['run_id'],10,0);
    sql($db,'UPDATE parties SET status="cancelled" WHERE id=?',[$p['id']]);
    sql($db,'UPDATE tournament_events SET settled=1,ends=? WHERE id=?',[time(),$p['id']]);
}
function party_table(PDO $db,string $id):array {
    $rows=[];
    foreach(sql($db,'SELECT m.*,p.name,p.avatar FROM party_members m JOIN players p ON p.id=m.player_id WHERE m.party_id=? ORDER BY p.id',[$id])->fetchAll() as $m) {
        $r=['id'=>$m['player_id'],'name'=>$m['name'],'avatar'=>$m['avatar'],'topicID'=>$m['topic'],'played'=>0,'wins'=>0,'draws'=>0,'losses'=>0,'points'=>0,'quizPoints'=>0];
        foreach(sql($db,'SELECT own.score,other.score opponent_score FROM party_fixtures f JOIN duels d ON d.id=f.duel_id JOIN matches own ON own.duel_id=d.id AND own.player_id=? JOIN matches other ON other.duel_id=d.id AND other.player_id<>? WHERE f.party_id=? AND d.status="complete"',[$r['id'],$r['id'],$id])->fetchAll() as $g) {
            $r['played']++;$r['quizPoints']+=(int)$g['score'];
            if($g['score']>$g['opponent_score']){$r['wins']++;$r['points']+=3;}
            elseif($g['score']===$g['opponent_score']){$r['draws']++;$r['points']++;}else{$r['losses']++;}
        }
        $rows[]=$r;
    }
    usort($rows,fn($a,$b)=>($b['points']<=>$a['points']) ?: strcmp($a['id'],$b['id']));
    $rank=0;$last=null;foreach($rows as $i=>&$r){if($last!==$r['points']){$rank=$i+1;$last=$r['points'];}$r['rank']=$rank;}unset($r);return $rows;
}
function party_sync(PDO $db,string $id):void {
    $p=sql($db,'SELECT p.*,e.ends FROM parties p JOIN tournament_events e ON e.id=p.id WHERE p.id=?',[$id])->fetch();
    if(!$p)return;
    if($p['status']==='lobby' && (int)$p['ends']<=time()){party_cancel($db,$p);return;}
    if($p['status']!=='playing')return;
    foreach(party_table($db,$id) as $r)sql($db,'UPDATE tournament_runs SET score=?,streak=? WHERE event_id=? AND player_id=?',[$r['points'],$r['wins'],$id,$r['id']]);
    $unfinished=(int)sql($db,'SELECT COUNT(*) FROM party_fixtures f LEFT JOIN duels d ON d.id=f.duel_id WHERE f.party_id=? AND (d.id IS NULL OR d.status<>"complete")',[$id])->fetchColumn();
    if($unfinished===0 || (int)$p['ends']<=time()) {
        sql($db,'UPDATE parties SET status="complete" WHERE id=?',[$id]);sql($db,'UPDATE tournament_runs SET state="finished" WHERE event_id=?',[$id]);
        sql($db,'UPDATE tournament_events SET ends=? WHERE id=?',[time(),$id]);
    }
}
function party_sync_duel(PDO $db,string $duel):void {
    $id=sql($db,'SELECT party_id FROM party_fixtures WHERE duel_id=?',[$duel])->fetchColumn();if($id){party_sync($db,$id);tournament_settle($db);}
}
function party_card(PDO $db,string $pid,array $p):array {
    return ['id'=>$p['id'],'name'=>$p['name'],'code'=>$p['code'],'hostID'=>$p['host'],'status'=>$p['status'],'cycles'=>(int)$p['cycles'],'days'=>(int)$p['days'],'powers'=>(bool)$p['powers'],'ends'=>(int)$p['ends'],'members'=>(int)sql($db,'SELECT COUNT(*) FROM party_members WHERE party_id=?',[$p['id']])->fetchColumn(),'entryCoins'=>10];
}
function party_add_member(PDO $db,string $id,string $pid,string $topic):void {
    if(!in_array($topic,array_column(play_topics(),'id'),true))fail('Choose a valid home topic.');
    if(tournament_wallet($db,$pid)['coins']<10)fail('Not enough coins. Joining costs 10 coins.',409);
    $run=bin2hex(random_bytes(12));sql($db,'INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,state,created) VALUES(?,?,?,?,?,?,?)',[$run,$id,$pid,'party:'.$id.':'.$pid,'[]','party',time()]);
    tournament_credit($db,$pid,'entry:'.$run,-10,0);sql($db,'INSERT INTO party_members VALUES(?,?,?,?)',[$id,$pid,$topic,$run]);
}
function party_routes(string $route,PDO $db,string $pid,array $body):void {
    if(!str_starts_with($route,'party-') && $route!=='parties')return;
    $db->exec('BEGIN IMMEDIATE');
    foreach(sql($db,'SELECT party_id FROM party_members WHERE player_id=?',[$pid])->fetchAll() as $m)party_sync($db,$m['party_id']);
    tournament_settle($db);
    if($route==='parties') {
        $rooms=sql($db,'SELECT p.*,e.ends FROM parties p JOIN tournament_events e ON e.id=p.id JOIN party_members m ON m.party_id=p.id AND m.player_id=? ORDER BY p.created DESC LIMIT 40',[$pid])->fetchAll();
        $cards=array_map(fn($p)=>party_card($db,$pid,$p),$rooms);$db->exec('COMMIT');out(['parties'=>$cards]);
    }
    if($route==='party-create') {
        $key=(string)($body['requestID'] ?? '');if(!preg_match('/^[A-Za-z0-9-]{16,64}$/D',$key))fail('A request identifier is required.');
        $old=sql($db,'SELECT p.*,e.ends FROM parties p JOIN tournament_events e ON e.id=p.id WHERE p.request_key=?',[$pid.':'.$key])->fetch();
        if($old){$card=party_card($db,$pid,$old);$db->exec('COMMIT');out($card,201);}
        $name=trim((string)($body['name'] ?? ''));$cycles=$body['cycles'] ?? 1;$days=$body['days'] ?? 7;$powers=$body['powers'] ?? false;
        if(strlen($name)<2 || strlen($name)>60 || preg_match('/[\p{C}]/u',$name))fail('Use a tournament name of 2–60 characters.');
        if(!is_int($cycles) || $cycles<1 || $cycles>3 || !in_array($days,[1,3,7,14],true) || !is_bool($powers))fail('Choose valid tournament settings.');
        if((int)sql($db,'SELECT COUNT(*) FROM parties WHERE host=? AND created>?',[$pid,time()-86400])->fetchColumn()>=3)fail('You can host up to three friends tournaments a day.',429);
        $id=bin2hex(random_bytes(12));$code=strtoupper(bin2hex(random_bytes(6)));$end=time()+86400;
        sql($db,'INSERT INTO tournament_events VALUES(?,?,?,?,?,?,?,0)',[$id,'mixed','party',time(),$end,10,0]);
        sql($db,'INSERT INTO parties VALUES(?,?,?,?,?,?,?,?,?,?)',[$id,$pid,$code,$name,$cycles,$days,(int)$powers,'lobby',time(),$pid.':'.$key]);
        party_add_member($db,$id,$pid,(string)($body['topic'] ?? ''));
        $p=party_require($db,$pid,$id);$card=party_card($db,$pid,$p);$db->exec('COMMIT');out($card,201);
    }
    if($route==='party-join') {
        $bucket='party-join:'.$pid;$window=(int)floor(time()/3600);
        sql($db,'INSERT INTO limits VALUES(?,?,1) ON CONFLICT(bucket) DO UPDATE SET count=CASE WHEN window=excluded.window THEN count+1 ELSE 1 END,window=excluded.window',[$bucket,$window]);
        if((int)sql($db,'SELECT count FROM limits WHERE bucket=?',[$bucket])->fetchColumn()>20){$db->exec('COMMIT');fail('Please wait before trying more invitation codes.',429);}
        $code=strtoupper(preg_replace('/[\s-]+/','',(string)($body['code'] ?? '')));
        $p=sql($db,'SELECT p.*,e.ends FROM parties p JOIN tournament_events e ON e.id=p.id WHERE code=?',[$code])->fetch();if(!$p) {$db->exec('COMMIT');fail('Invitation code not found.',404);}
        if(!sql($db,'SELECT 1 FROM party_members WHERE party_id=? AND player_id=?',[$p['id'],$pid])->fetch()) {
            if($p['status']!=='lobby' || (int)$p['ends']<=time())fail('This tournament is no longer accepting players.',409);
            $members=sql($db,'SELECT player_id FROM party_members WHERE party_id=?',[$p['id']])->fetchAll();if(count($members)>=8)fail('This tournament is full (eight players).',409);
            foreach($members as $m)if(blocked($db,$pid,$m['player_id']))fail('You cannot join this group.',403);
            party_add_member($db,$p['id'],$pid,(string)($body['topic'] ?? ''));
        }
        $card=party_card($db,$pid,$p);$db->exec('COMMIT');out($card);
    }
    $id=(string)($body['party'] ?? $_GET['id'] ?? '');$p=party_require($db,$pid,$id);
    if($route==='party-board') {
        $fixtures=[];
        foreach(sql($db,'SELECT f.*,d.status FROM party_fixtures f LEFT JOIN duels d ON d.id=f.duel_id WHERE f.party_id=? ORDER BY f.cycle,f.id',[$id])->fetchAll() as $f) {
            $own=$f['duel_id'] ? sql($db,'SELECT answers FROM matches WHERE duel_id=? AND player_id=?',[$f['duel_id'],$pid])->fetch():false;
            $fixtures[]=['id'=>$f['id'],'a'=>$f['a'],'b'=>$f['b'],'topicID'=>$f['topic'],'homeID'=>$f['home'],'cycle'=>(int)$f['cycle'],'status'=>$f['status'] ?? 'scheduled','ownFinished'=>$own?count(json_decode($own['answers'],true))===7:false];
        }
        $r=['party'=>party_card($db,$pid,$p),'standings'=>party_table($db,$id),'fixtures'=>$fixtures,'selfID'=>$pid,'coins'=>tournament_wallet($db,$pid)['coins']];$db->exec('COMMIT');out($r);
    }
    if($route==='party-topic') {
        if($p['status']!=='lobby')fail('Home topics are locked after the host starts.',409);
        $topic=(string)($body['topic'] ?? '');if(!in_array($topic,array_column(play_topics(),'id'),true))fail('Choose a valid topic.');
        sql($db,'UPDATE party_members SET topic=? WHERE party_id=? AND player_id=?',[$topic,$id,$pid]);$db->exec('COMMIT');out(['ok'=>true]);
    }
    if($route==='party-start' || $route==='party-cancel') {
        if($p['host']!==$pid)fail('Only the host can do this.',403);
        if($p['status']!=='lobby'){if($route==='party-start' && $p['status']==='playing'){$db->exec('COMMIT');out(['ok'=>true]);}fail('This lobby has already closed.',409);}
        if($route==='party-cancel'){party_cancel($db,$p);$db->exec('COMMIT');out(['ok'=>true]);}
        $members=sql($db,'SELECT * FROM party_members WHERE party_id=? ORDER BY player_id',[$id])->fetchAll();if(count($members)<2)fail('At least two players must join before you start.',409);
        foreach($members as $i=>$a)foreach(array_slice($members,$i+1) as $b)for($cycle=1;$cycle<=(int)$p['cycles'];$cycle++)foreach([$a,$b] as $home)sql($db,'INSERT INTO party_fixtures(id,party_id,a,b,topic,cycle,home) VALUES(?,?,?,?,?,?,?)',[bin2hex(random_bytes(12)),$id,$a['player_id'],$b['player_id'],$home['topic'],$cycle,$home['player_id']]);
        sql($db,'UPDATE parties SET status="playing" WHERE id=?',[$id]);sql($db,'UPDATE tournament_events SET starts=?,ends=? WHERE id=?',[time(),time()+(int)$p['days']*86400,$id]);$db->exec('COMMIT');out(['ok'=>true]);
    }
    if($route==='party-play') {
        if($p['status']!=='playing')fail('This tournament is not open for matches.',409);
        $f=sql($db,'SELECT * FROM party_fixtures WHERE id=? AND party_id=? AND (a=? OR b=?)',[(string)($body['fixture'] ?? ''),$id,$pid,$pid])->fetch();if(!$f)fail('Match not found',404);
        $other=$f['a']===$pid?$f['b']:$f['a'];visible_player($db,$pid,$other);
        if(!$f['duel_id']) {
            $a=visible_player($db,$pid,$f['a']);$b=visible_player($db,$pid,$f['b']);$packet=fresh_packet($db,$f['a'],$f['topic']);$duel=bin2hex(random_bytes(12));
            $am=insert_match($db,$a['id'],$f['topic'],'party',$b['name'],$b['id'],$packet,array_fill(0,7,0),$duel,null,true);
            $bm=insert_match($db,$b['id'],$f['topic'],'party',$a['name'],$a['id'],$packet,array_fill(0,7,0),$duel,null,true);
            sql($db,'INSERT INTO duels VALUES(?,?,?,?,?,?,?,?,?,?,?)',[$duel,$a['id'],$b['id'],$f['topic'],json_encode($packet),$am,$bm,'accepted',time(),(int)$p['ends'],'party:'.$f['id']]);
            sql($db,'UPDATE party_fixtures SET duel_id=? WHERE id=?',[$duel,$f['id']]);$f['duel_id']=$duel;
        }
        $m=sql($db,'SELECT * FROM matches WHERE duel_id=? AND player_id=?',[$f['duel_id'],$pid])->fetch();$reply=start_info($db,$m);$db->exec('COMMIT');out($reply);
    }
    fail('Friends tournament endpoint not found',404);
}
