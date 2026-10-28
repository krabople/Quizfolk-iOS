"""Asynchronous social contracts. Run only against an isolated test service."""
import json,urllib.request,urllib.error,pathlib,sqlite3,time,os,uuid
ROOT=pathlib.Path(__file__).resolve().parents[1];BASE=os.environ.get('QUIZFOLK_TEST_URL','http://127.0.0.1:8770/index.php?r=');STATE=pathlib.Path(os.environ.get('QUIZFOLK_STATE_DIR',ROOT/'backend/private'))/'quizfolk.sqlite'
BANK={q['id']:q for q in json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))}
def req(route,body=None,token=None,status=200):
 h={'Content-Type':'application/json','X-Quizfolk-Client':'3'}
 if token:h['Authorization']='Bearer '+token
 r=urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=h)
 try:
  with urllib.request.urlopen(r,timeout=20) as v:code=v.status;data=json.load(v)
 except urllib.error.HTTPError as e:code=e.code;data=json.load(e)
 assert code==status,(route,code,data);return data
people=[]
for name in ['Social Alice','Social Bob','Social Eve']:
 a=req('register',{'name':name},status=201);p=req('profile',token=a['token']);people.append((a['token'],p['id']))
(a,aid),(b,bid),(e,eid)=people
req('social-settings',{'interests':['22','17']},a);req('social-settings',{'interests':['22']},b)
assert any(p['id']==bid and p['sharedTopics']==['22'] for p in req('people&q=SOCIAL%20BOB',token=a)['players'])
assert req('people&q=%25',token=a)['players']==[]
req('social-settings',{'titleID':'22:50'},a,403)
req('follow',{'player':bid,'enabled':True},a);req('follow',{'player':bid,'enabled':True},a)
assert req('player&id='+bid,token=a)['followers']==1
assert len(req('people&mode=following',token=a)['players'])==1
key=str(uuid.uuid4());m=req('challenge',{'player':bid,'topic':'22','requestID':key},a,201)
assert m['kind']=='challenge' and m['played']==[] and m['opponentID']==bid
assert req('challenge',{'player':bid,'topic':'22','requestID':key},a,201)['id']==m['id']
req('duel-open',{'duel':m['duelID']},e,404);req('round',{'match':m['id']},b,404)
with sqlite3.connect(STATE) as db:assert db.execute('SELECT started FROM matches WHERE id=?',(m['id'],)).fetchone()[0] is None
packets=[]
def finish(token,match,correct):
 total=0;questions=[]
 for i in range(7):
  r=req('round',{'match':match['id']},token)
  assert r['phase']=='reading' and r['question']['answers']==[] and r['remaining']==10
  early=req('reveal',{'match':match['id']},token);assert early['phase']=='reading'
  req('answer',{'match':match['id'],'round':i,'answer':0},token,409)
  with sqlite3.connect(STATE) as db:
   assert db.execute('SELECT started FROM matches WHERE id=?',(match['id'],)).fetchone()[0] is None
   db.execute('UPDATE matches SET preview_started=? WHERE id=?',(time.time()-3,match['id']))
  shown=req('reveal',{'match':match['id']},token);assert shown['phase']=='answer' and shown['remaining']>9
  q=shown['question'];assert q['prompt']==r['question']['prompt'];questions.append(q);assert 'correctIndex' not in q
  original=BANK[q['id']];right=q['answers'].index(original['answers'][original['correctIndex']]);choice=right if correct else (right+1)%4
  result=req('answer',{'match':match['id'],'round':i,'answer':choice},token);total+=result['points']
 return total,questions,result
score,packet,result=finish(a,m,True);assert result['pending'] is True
assert req('profile',token=a)['xp']==0
assert req('player&id='+bid,token=a)['headToHead']['games']==0
inbox=req('duels',token=b)['duels'][0];assert inbox['incoming'] and inbox['opponentFinished'] and inbox['opponentScore'] is None
# A different user can accept hours later without the challenger being connected.
with sqlite3.connect(STATE) as db:db.execute('UPDATE matches SET created=? WHERE id=?',(int(time.time())-90000,m['id']))
bm=req('duel-open',{'duel':m['duelID']},b);assert bm['id']!=m['id'] and bm['played']==[]
assert req('duel-open',{'duel':m['duelID']},b)['id']==bm['id']
other,packet2,result=finish(b,bm,False);assert packet2==packet and result['pending'] is False and result['opponentScore']==score
assert req('profile',token=a)['xp']==score+140 and req('profile',token=b)['xp']==40
ha=req('player&id='+bid,token=a)['headToHead'];hb=req('player&id='+aid,token=b)['headToHead'];assert ha=={'games':1,'wins':1,'draws':0,'losses':0} and hb['losses']==1
req('answer',{'match':bm['id'],'round':6,'answer':-1},b)
assert req('player&id='+bid,token=a)['headToHead']['games']==1
resolved=req('duel-open',{'duel':m['duelID']},a);assert len(resolved['played'])==7 and not resolved['pending'] and resolved['opponentScore']==0
assert len(req('activity',token=a)['events'])==1
assert len(req('leaderboard&topic=22&period=month&scope=following',token=a)['entries'])==2
# Declines, preferences and blocks are enforced on the server.
d=req('challenge',{'player':bid,'topic':'17','requestID':str(uuid.uuid4())},a,201);req('duel-decline',{'duel':d['duelID']},b)
req('duel-open',{'duel':d['duelID']},a,410)
req('social-settings',{'challengesOpen':False,'discoverable':False},b)
assert req('people&q=Social%20Bob',token=e)['players']==[]
req('challenge',{'player':bid,'topic':'17','requestID':str(uuid.uuid4())},a,403)
req('social-settings',{'challengesOpen':True,'discoverable':True},b)
req('block',{'player':bid,'enabled':True},a);req('player&id='+bid,token=a,status=404)
req('challenge',{'player':aid,'topic':'17','requestID':str(uuid.uuid4())},b,404)
assert req('people&mode=following',token=a)['players']==[]
req('block',{'player':bid,'enabled':False},a)
# Matching checks real runs, pairs two searchers, and enforces a genuine six-second bot wait.
k1=str(uuid.uuid4());s=req('match-search',{'topic':'38','requestID':k1},a);assert s['state']=='searching' and s['match'] is None
s2=req('match-search',{'topic':'38','requestID':str(uuid.uuid4())},b);assert s2['match']['kind']=='challenge'
s1=req('match-search',{'topic':'38','requestID':k1},a);assert s1['match']['duelID']==s2['match']['duelID']
k3=str(uuid.uuid4());s=req('match-search',{'topic':'16','requestID':k3},e);assert s['state']=='searching'
s=req('match-search',{'topic':'16','requestID':k3},e);assert s['state']=='searching'
with sqlite3.connect(STATE) as db:db.execute('UPDATE searches SET created=? WHERE id=?',(time.time()-7,s['searchID']))
s=req('match-search',{'topic':'16','requestID':k3},e);assert s['match']['kind']=='bot'
assert req('match-search',{'topic':'16','requestID':k3},e)['match']['id']==s['match']['id']
# Deleting one player cancels their pending challenges and preserves settled rival history.
req('delete-account',{},a);assert any(d['status']=='cancelled' for d in req('duels',token=b)['duels'])
assert req('profile',token=b)['xp']==40
for token,id in [(b,bid),(e,eid)]:req('delete-account',{},token)
print('PASS: people, interests, idempotent follows, private profiles, title validation, asynchronous invitations, delayed acceptance, identical questions, result settlement, XP, symmetric head-to-head, declines, blocks, feed, friend leagues, queued human pairing, six-second fallback and deletion')
