<?php
declare(strict_types=1);
ini_set('display_errors','0');
header('Cache-Control: no-store, private');header('Pragma: no-cache');header('Referrer-Policy: no-referrer');
header('X-Content-Type-Options: nosniff');header('X-Frame-Options: DENY');header('X-Robots-Tag: noindex, nofollow');
header("Content-Security-Policy: default-src 'none'; style-src 'self'; font-src 'self'; img-src 'self'; script-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'");
if(isset($_GET['data']) || $_SERVER['REQUEST_METHOD']==='POST') {
    try {
        require dirname(__DIR__,2).'/quizfolk-service/download-tracking/metrics.php';
        $config=qf_metrics_stats();qf_metrics_json(qf_metrics_report($config));
    } catch(Throwable $e) {http_response_code(503);header('Content-Type: application/json');echo '{"error":"Download statistics are temporarily unavailable."}';}
    exit;
}
if($_SERVER['REQUEST_METHOD']!=='GET' && $_SERVER['REQUEST_METHOD']!=='HEAD'){http_response_code(405);header('Allow: GET, HEAD, POST');exit;}
?><!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="no-referrer"><title>Quizfolk download statistics</title><link rel="icon" href="logo.png"><link rel="stylesheet" href="stats.css"><script src="stats.js" defer></script></head>
<body><main class="wrap">
<header><div class="brand"><img src="logo.png" width="40" height="40" alt="">Quizfolk</div><span class="private">Private statistics</span></header>
<div class="heading"><div><p class="eyebrow">ANDROID DOWNLOADS</p><h1>Your downloads,<br><span>at a glance.</span></h1></div><div class="actions" hidden id="actions"><button id="refresh" type="button">Refresh</button><button id="signout" class="secondary" type="button">Sign out</button></div></div>
<p id="status" role="status">Opening your download statistics…</p>
<section id="dashboard" hidden aria-label="Download statistics">
<div class="totals"><article><p>Total requests</p><strong id="total">0</strong><small>Since tracking started</small></article><article><p>Today</p><strong id="today">0</strong><small>London time</small></article><article><p>Last 7 days</p><strong id="week">0</strong><small>Including today</small></article></div>
<div class="panels"><section class="panel"><h2>Daily requests</h2><p class="muted">The last 30 days · London time</p><div class="scroll"><table><thead><tr><th>Date</th><th>Requests</th></tr></thead><tbody id="days"></tbody></table></div></section>
<section class="panel"><h2>Recent clicks</h2><p class="muted">The latest 100 requests · London time</p><div class="scroll"><table><thead><tr><th>Time</th><th>App version</th></tr></thead><tbody id="recent"></tbody></table></div></section></div>
<p class="note">These are download-link requests, not completed downloads, installations or unique people. Repeat clicks count separately. HEAD requests, known prefetch requests and resumed range requests are excluded. Automated requests can still be included.</p>
<p class="note" id="since"></p><p class="note">The counter stores dates, times and app versions. It does not store IP addresses, visitor identifiers or referrers. Keep your private access link to yourself; the dashboard signs out after 30 minutes.</p>
</section>
<footer><a href="./">Open the download page</a><span>Quizfolk download statistics</span></footer>
</main></body></html>
