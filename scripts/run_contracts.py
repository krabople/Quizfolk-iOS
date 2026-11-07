"""Run every HTTP contract in disposable state; never touch a deployed database."""
import os,pathlib,subprocess,sys,tempfile,time,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
PHP=os.environ.get('QUIZFOLK_PHP','php')
if (ROOT/'backend/config.php').exists():raise SystemExit('Use a clean checkout without backend/config.php for isolated tests.')
TEMP_ROOT=ROOT/'build'/'contract-state'
TEMP_ROOT.mkdir(parents=True,exist_ok=True)
allowed=['test_backend.py','test_social.py','test_tournaments.py','test_economy.py','test_parties_powers.py','test_cross_platform.py','test_notifications.py','test_rewarded.py']
suites=sys.argv[1:] or allowed
if any(suite not in allowed for suite in suites):raise SystemExit('Choose a known isolated contract suite.')
for suite in suites:
 with tempfile.TemporaryDirectory(prefix='quizfolk-contract-',dir=TEMP_ROOT) as folder:
  assert pathlib.Path(folder).resolve().is_relative_to(TEMP_ROOT.resolve())
  env=dict(os.environ,QUIZFOLK_STATE_DIR=folder,QUIZFOLK_TEST_URL='http://127.0.0.1:8773/index.php?r=')
  log=pathlib.Path(folder)/'server.log'
  with log.open('w',encoding='utf-8') as stream:
   server=subprocess.Popen([PHP,'-d','extension_dir='+os.environ['QUIZFOLK_PHP_EXT'],'-d','extension=pdo_sqlite','-d','extension=openssl','-S','127.0.0.1:8773','-t',str(ROOT/'backend/public')],env=env,stdout=stream,stderr=stream) if os.environ.get('QUIZFOLK_PHP_EXT') else subprocess.Popen([PHP,'-S','127.0.0.1:8773','-t',str(ROOT/'backend/public')],env=env,stdout=stream,stderr=stream)
   try:
    for _ in range(40):
     try:
      with urllib.request.urlopen(env['QUIZFOLK_TEST_URL']+'health',timeout=2):break
     except Exception:time.sleep(.15)
    else:raise RuntimeError('Local test server did not start')
    result=subprocess.run([sys.executable,str(ROOT/'scripts'/suite)],env=env,cwd=ROOT)
    if result.returncode:
     raise RuntimeError(suite+' failed; local server log: '+log.read_text(encoding='utf-8')[-5000:])
   finally:server.terminate();server.wait(timeout=10)
print('All isolated HTTP contracts passed.')
