<?php
declare(strict_types=1);

// Read-only milestones derived from historical play. Prize rows remain intact.
function achievement_row(string $id,string $name,string $symbol,string $group,string $requirement,int $progress,int $target,string $scope):array {
    $progress=max(0,$progress);$target=max(1,$target);
    return ['id'=>$id,'name'=>$name,'symbol'=>$symbol,'group'=>$group,'description'=>$requirement.' '.$scope,
        'earned'=>$progress>=$target,'progress'=>$progress,'target'=>$target,
        'progressLabel'=>number_format(min($progress,$target)).' / '.number_format($target)];
}
function best_tournament_achievements(PDO $db,string $pid,array $topicNames):array {
    // Rank is ascending: an old first place must beat any number of newer seconds.
    // Group before limiting; a recent-results limit can hide someone's best finish.
    $rows=sql($db,'SELECT p.event_id,p.rank,e.topic,e.kind,e.ends FROM tournament_places p JOIN tournament_events e ON e.id=p.event_id WHERE p.player_id=? AND p.rank BETWEEN 1 AND 3 AND e.kind IN ("daily","weekly") AND e.settled=1 ORDER BY p.rank ASC,e.ends DESC,e.id ASC',[$pid])->fetchAll();
    $best=[];
    foreach($rows as $row) {
        $topic=(string)$row['topic'];if(isset($best[$topic]))continue;
        $rank=(int)$row['rank'];$ordinal=[1=>'1st',2=>'2nd',3=>'3rd'][$rank];$name=$topicNames[$topic] ?? 'Trivia';
        $best[$topic]=['id'=>'tournament-best:'.$topic,'name'=>$name." \u{00B7} Best #".$rank,'symbol'=>'trophy.fill','group'=>'Best tournament finishes',
            'description'=>'Finish '.$ordinal.' in a public '.$name.' tournament. This is the highest placing achieved in this topic across daily and weekly tournaments. Only the best placing is shown here; your complete badge collection is kept in Tournament badges.',
            'earned'=>true,'progress'=>1,'target'=>1,'progressLabel'=>'Best finish: '.$ordinal,'topicID'=>$topic,'kind'=>$row['kind'],'rank'=>$rank];
    }
    uasort($best,fn($a,$b)=>strnatcasecmp($a['name'],$b['name']));return array_values($best);
}
function player_achievements(PDO $db,string $pid,array $card,array $topicNames):array {
    $stats=$card['stats'];$topics=$card['topics'];$bestLevel=1;
    foreach($topics as $topic)$bestLevel=max($bestLevel,(int)$topic['level']);
    $podiums=sql($db,'SELECT COUNT(*) podiums,COALESCE(SUM(p.rank=1),0) championships FROM tournament_places p JOIN tournament_events e ON e.id=p.event_id WHERE p.player_id=? AND p.rank BETWEEN 1 AND 3 AND e.kind IN ("daily","weekly") AND e.settled=1',[$pid])->fetch();
    $run=sql($db,'SELECT COALESCE(MAX(r.streak),0) streak,COALESCE(MAX(r.score),0) score FROM tournament_runs r JOIN tournament_events e ON e.id=r.event_id WHERE r.player_id=? AND e.kind IN ("daily","weekly")',[$pid])->fetch();
    $duelScope='Only completed duels saved to the online profile count, including bot duels. Offline practice and tournament runs do not count. A human challenge counts after both players finish.';
    $tournamentScope='Public daily and weekly tournaments count; private friends tournaments do not count.';
    $badges=[];
    foreach([1,10,25,50,100,250,500,1000,2500,10000] as $n) {
        $id=$n===1?'first':($n===10?'ten':'duels:'.$n);$name=$n===1?'First duel':($n===10?'Tenacious':number_format($n).' duels');
        $badges[]=achievement_row($id,$name,'bolt.fill','Duels','Complete '.number_format($n).($n===1?' online duel.':' online duels.'),(int)$stats['matches'],$n,$duelScope);
    }
    foreach([1,10,25,50,100,250,500,1000,2500] as $n)$badges[]=achievement_row($n===1?'winner':'wins:'.$n,$n===1?'First victory':number_format($n).' victories','trophy.fill','Victories','Win '.number_format($n).($n===1?' online duel.':' online duels.'),(int)$stats['wins'],$n,$duelScope.' Draws are not victories.');
    foreach([1,5,10,25,50,100,250,1000] as $n)$badges[]=achievement_row($n===1?'perfect':'perfect:'.$n,$n===1?'Seven of seven':number_format($n).' perfect duels','checkmark.seal.fill','Perfect games',
        'Answer all seven questions correctly in '.($n===1?'one completed online duel.':number_format($n).' completed online duels.'),(int)$stats['perfect'],$n,$duelScope.' Power-up-assisted correct answers count.');
    foreach([100,500,1000,5000,10000,25000,100000] as $n)$badges[]=achievement_row('correct:'.$n,number_format($n).' correct answers','checkmark.circle.fill','Correct answers','Answer '.number_format($n).' questions correctly across completed online duels.',(int)$stats['correct'],$n,$duelScope);
    foreach([5,10,20,31] as $n)$badges[]=achievement_row($n===5?'explorer':'topics:'.$n,$n===5?'Topic explorer':number_format($n).' topics explored','globe','Exploration','Complete at least one online duel in '.number_format($n).' different topics.',count($topics),$n,$duelScope.' Mixed counts as its own topic.');
    foreach([10,20,30,40,50,75,100] as $n)$badges[]=achievement_row('topic-level:'.$n,'Level '.$n.' specialist','graduationcap.fill','Topic mastery','Reach level '.$n.' in any single online topic.',$bestLevel,$n,'Progress is your highest online topic level, not an overall player level. Device-only practice XP does not count.');
    foreach([1,5,10,25,50,100] as $n)$badges[]=achievement_row('podiums:'.$n,$n===1?'First podium':number_format($n).' podium finishes','medal.fill','Tournaments','Finish in the top three in '.number_format($n).($n===1?' public tournament.':' public tournaments.'),(int)$podiums['podiums'],$n,$tournamentScope.' Results count only after the tournament closes and prizes are settled.');
    foreach([1,5,10,25,50,100] as $n)$badges[]=achievement_row('championships:'.$n,$n===1?'Tournament champion':number_format($n).' tournament wins','crown.fill','Tournaments','Finish first in '.number_format($n).($n===1?' public tournament.':' public tournaments.'),(int)$podiums['championships'],$n,$tournamentScope.' Results count only after the tournament closes and prizes are settled.');
    foreach([10,25,50,100] as $n)$badges[]=achievement_row('tournament-streak:'.$n,number_format($n).' in a row','flame.fill','Tournaments','Reach a streak of '.number_format($n).' correct answers in one public tournament run.',(int)$run['streak'],$n,$tournamentScope.' Your highest saved streak counts, including a run still in progress.');
    foreach([250,500,1000,2500] as $n)$badges[]=achievement_row('tournament-score:'.$n,number_format($n).' tournament points','target','Tournaments','Score at least '.number_format($n).' points in one public tournament run.',(int)$run['score'],$n,$tournamentScope.' This is one run, not the sum of several attempts.');
    return array_merge($badges,best_tournament_achievements($db,$pid,$topicNames));
}
