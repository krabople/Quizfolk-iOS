<?php
declare(strict_types=1);

/** Progressive topic levels. Earned XP and match scores are never rescaled. */
function topic_level_progress(int $xp):array {
    $xp=max(0,$xp);$lower=0;$upper=intdiv($xp,1500)+1;
    while($lower<$upper) {
        $middle=$lower+intdiv($upper-$lower+1,2);
        if($middle<=intdiv(intdiv($xp,250),$middle+5))$lower=$middle;else $upper=$middle-1;
    }
    $into=$xp-250*$lower*($lower+5);$cost=1500+500*$lower;
    return ['level'=>$lower+1,'xpIntoLevel'=>$into,'xpForNextLevel'=>$cost,'remainingXP'=>$cost-$into];
}
