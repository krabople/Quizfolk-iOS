"""Download counter/auth/redirect checks in disposable local state; no production requests."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from http.cookiejar import CookieJar
import json
import os
from pathlib import Path
import secrets
import shutil
import sqlite3
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

repo=Path(__file__).resolve().parents[1]
php=os.environ.get('QUIZFOLK_PHP','php')
extensions=os.environ.get('QUIZFOLK_PHP_EXT')
command=[php]+(['-d','extension_dir='+extensions,'-d','extension=pdo_sqlite'] if extensions else [])

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args):return None

with tempfile.TemporaryDirectory(prefix='quizfolk-download-tests-') as folder:
    home=Path(folder);public=home/'public_html/quizfolk-download';public.mkdir(parents=True)
    private=home/'quizfolk-service/download-tracking/private';private.mkdir(parents=True)
    for name in ['download.php','stats.php','stats.js','stats.css']:
        shutil.copyfile(repo/'web-download'/name,public/name)
    shutil.copyfile(repo/'web-download/server/metrics.php',private.parent/'metrics.php')
    apk=b'isolated signed-package substitute for redirect transport checks'
    (public/'Quizfolk-Android-0.3.3-12.apk').write_bytes(apk)
    key=secrets.token_urlsafe(32);fingerprint=hashlib.sha256(key.encode()).hexdigest()
    (private/'config.php').write_text("<?php return ['stats_key_hash'=>'"+fingerprint+"','started_at'=>'2026-11-05T00:00:00Z','origin'=>'http://127.0.0.1:8784','cookie_secure'=>false];")
    log=(home/'server.log').open('w')
    server=subprocess.Popen(command+['-S','127.0.0.1:8784','-t',str(home/'public_html')],stdout=log,stderr=log)
    base='http://127.0.0.1:8784/quizfolk-download/'
    plain=urllib.request.build_opener(NoRedirect())
    cookies=CookieJar();owner=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies),NoRedirect())
    def request(path='download.php',method='GET',data=None,headers=None,client=plain):
        if data is not None: data=json.dumps(data).encode()
        try:r=client.open(urllib.request.Request(base+path,data=data,headers=headers or {},method=method),timeout=5)
        except urllib.error.HTTPError as error:r=error
        return r.status,r.headers,r.read()
    def total():
        result=request('stats.php?data=1',client=owner);assert result[0]==200,result
        return json.loads(result[2])
    try:
        for _ in range(50):
            try:
                if request('stats.php')[0]==200:break
            except OSError:time.sleep(.1)
        else:raise RuntimeError('Local PHP server failed to start')
        assert request('stats.php?data=1')[0]==401
        assert request('stats.php?data=1',method='POST',data={'action':'unlock','key':'wrong'},headers={'Content-Type':'application/json'},client=owner)[0]==401
        assert request('stats.php?data=1',method='POST',data={'action':'unlock','key':key},headers={'Content-Type':'application/json','Origin':'https://unrelated.example'},client=owner)[0]==403
        unlocked=request('stats.php?data=1',method='POST',data={'action':'unlock','key':key},headers={'Content-Type':'application/json'},client=owner)
        assert unlocked[0]==200 and total()['totals']['total']==0
        assert 'HttpOnly' in unlocked[1].get('Set-Cookie','') and 'SameSite=Strict' in unlocked[1].get('Set-Cookie','')
        for method,headers in [('HEAD',{}),('GET',{'Purpose':'prefetch'}),('GET',{'Sec-Purpose':'prefetch;prerender'}),('GET',{'Range':'bytes=100-'})]:
            response=request(method=method,headers=headers)
            assert response[0]==302 and response[1]['X-Quizfolk-Download-Recorded']=='ignored'
        assert total()['totals']['total']==0
        assert request(method='POST')[0]==405
        for _ in range(2):
            response=request();assert response[0]==302 and response[1]['X-Quizfolk-Download-Recorded']=='yes'
            assert response[1]['Location']=='Quizfolk-Android-0.3.3-12.apk?file=1'
        assert total()['totals']['total']==2 and len(total()['recent'])==2
        assert request(headers={'X-Quizfolk-Verification':key})[1]['X-Quizfolk-Download-Recorded']=='verification'
        assert total()['totals']['total']==2 and total()['totals']['checks']==1
        with urllib.request.urlopen(base+'Quizfolk-Android-0.3.3-12.apk?file=1') as response:assert response.read()==apk
        # Independent PHP processes exercise atomic increments against one SQLite database.
        action="require '"+str(private.parent/'metrics.php').replace('\\','/')+"'; for($i=0;$i<10;$i++)qf_metrics_record(false);"
        with ThreadPoolExecutor(max_workers=6) as executor:
            results=list(executor.map(lambda _:subprocess.run(command+['-r',action],capture_output=True),range(6)))
        assert all(p.returncode==0 for p in results),[p.stderr for p in results]
        report=total();assert report['totals']['total']==62 and len(report['recent'])==62
        assert sum(day['clicks'] for day in report['daily'])==62
        db=sqlite3.connect(private/'clicks.sqlite')
        assert [r[1] for r in db.execute('PRAGMA table_info(recent)')]==['id','requested_at','version']
        db.close()
        # Counter-storage failure must not block the APK redirect.
        (private/'config.php').rename(private/'config-disabled.php')
        assert request()[1]['X-Quizfolk-Download-Recorded']=='unavailable'
        (private/'config-disabled.php').rename(private/'config.php')
        assert total()['totals']['total']==62
        db=sqlite3.connect(private/'clicks.sqlite')
        db.executemany('INSERT INTO recent(requested_at,version) VALUES(?,?)',[(int(time.time()),'test history')]*1200);db.commit();db.close()
        assert subprocess.run(command+['-r',"require '"+str(private.parent/'metrics.php').replace('\\','/')+"';qf_metrics_record(false);"],capture_output=True).returncode==0
        db=sqlite3.connect(private/'clicks.sqlite');assert db.execute('SELECT COUNT(*) FROM recent').fetchone()[0]==1000;db.close()
        assert request('stats.php?data=1',method='POST',data={'action':'logout'},headers={'Content-Type':'application/json'},client=owner)[0]==200
        assert request('stats.php?data=1',client=owner)[0]==401
        print('PASS: private access, session security, ignored probes/resumes, repeat clicks, test exclusion, concurrent increments, anonymous schema, fail-open downloads and sign-out.')
    finally:
        server.terminate();server.wait(timeout=10);log.close()
