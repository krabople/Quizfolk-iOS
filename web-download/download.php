<?php
declare(strict_types=1);
ini_set('display_errors','0');
try {
    require dirname(__DIR__,2).'/quizfolk-service/download-tracking/metrics.php';
    qf_metrics_download(__DIR__);
} catch(Throwable $e) {
    // This fixed local redirect remains usable even if tracking is unavailable.
    header('Cache-Control: no-store');header('Location: Quizfolk-Android-0.3.3-11.apk?file=1',true,302);
}
