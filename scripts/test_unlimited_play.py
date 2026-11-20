"""No hourly play quotas; exercise old boundaries in disposable local API state."""
import hashlib,json,os,pathlib,sqlite3,time,urllib.error,urllib.request,uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=os.environ['QUIZFOLK_TEST_URL']
STATE=pathlib.Path(os.environ['QUIZFOLK_STATE_DIR'])/'quizfolk.sqlite'
assert BASE.startswith('http://127.0.0.1:') and STATE.resolve().is_relative_to((ROOT/'build/contract-state').resolve())

def req(route,body=None,token=None,status=200):
 headers={'Content-Type':'application/json','X-Quizfolk-Client':'4'}
 if token:headers['Authorization']='Bearer '+token
 request=urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=headers)
 try:
  with urllib.request.urlopen(request,timeout=20) as response:code=response.status;data=json.load(response)
 except urllib.error.HTTPError as error:code=error.code;data=json.load(error)
 assert code==status,(route,code,data)
 return data

a=req('register',{'name':'Unlimited Alice'},status=201)['token']
b=req('register',{'name':'Unlimited Bob'},status=201)['token']
aid=req('profile',token=a)['id'];bid=req('profile',token=b)['id']
# Both challengers and recipients can keep playing beyond the former 30/hour cap.
for token in (a,b):
 for _ in range(35):
  match=req('match',{'topic':'16','botOnly':True},token,201)
  assert match['kind']=='bot'
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT COUNT(*) FROM matches WHERE player_id=? AND created>?',(aid,time.time()-3600)).fetchone()[0]==35
# No 15/hour invitation cap, and an already active recipient can accept normally.
for turn in range(16):
 challenge=req('challenge',{'player':bid,'topic':'16','requestID':str(uuid.uuid4())},a,201)
 if turn==15:
  accepted=req('duel-open',{'duel':challenge['duelID']},b)
  assert accepted['duelID']==challenge['duelID'] and accepted['opponentID']==aid
 else:req('duel-decline',{'duel':challenge['duelID']},b)
# Paid tournament runs remain paid, resumable and idempotent, without an hourly cap.
event=next(e for e in req('tournaments',token=a)['events'] if e['kind']=='daily' and e['featured'])
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_wallet SET coins=10000 WHERE player_id=?',(aid,))
for _ in range(35):
 body={'event':event['id'],'requestID':str(uuid.uuid4())}
 run=req('tournament-enter',body,a,201)
 assert req('tournament-enter',body,a)['id']==run['id']
 assert req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},a)['id']==run['id']
 assert req('tournament-end',{'run':run['id']},a)['state']=='ended'
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT COUNT(*) FROM tournament_runs WHERE player_id=?',(aid,)).fetchone()[0]==35
 assert db.execute('SELECT coins FROM tournament_wallet WHERE player_id=?',(aid,)).fetchone()[0]==10000-35*event['coins']
 # Old aggregate IP counters cannot block legitimate users sharing a connection.
 iphash=hashlib.sha256(b'127.0.0.1').hexdigest();window=int(time.time()//3600)
 db.execute('INSERT OR REPLACE INTO limits VALUES(?,?,?)',('request:'+iphash,window,5000))
assert req('profile',token=a)['id']==aid
assert req('profile',token=b)['id']==bid
req('profile',token='0'*64,status=401)
with sqlite3.connect(STATE) as db:db.execute('INSERT OR REPLACE INTO limits VALUES(?,?,?)',('register:'+iphash,window,10))
req('register',{'name':'Too Many New Accounts'},status=429)
req('delete-account',{},a);req('delete-account',{},b)
print('PASS: 35 duels per player, 16 direct challenges, recipient acceptance, 35 paid/idempotent tournament runs, shared-IP play, authentication and registration protection')
