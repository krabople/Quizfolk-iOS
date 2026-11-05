<?php
require __DIR__.'/../backend/levels.php';
function check(bool $ok):void {if(!$ok)throw new RuntimeException('Topic level contract failed');}
foreach([0,1500,3500,6000,9000,12500,16500,21000,26000,31500] as $index=>$xp) {
    $p=topic_level_progress($xp);check($p['level']===$index+1 && $p['xpIntoLevel']===0 && $p['xpForNextLevel']===1500+500*$index);
    if($xp>0){$before=topic_level_progress($xp-1);check($before['level']===$index && $before['remainingXP']===1);}
}
check(topic_level_progress(1200)===['level'=>1,'xpIntoLevel'=>1200,'xpForNextLevel'=>1500,'remainingXP'=>300]);
check(topic_level_progress(-100)['level']===1);check(topic_level_progress(PHP_INT_MAX)['remainingXP']>0);
echo "PASS: progressive topic levels, exact boundaries, four perfect wins, invalid and maximum XP\n";
