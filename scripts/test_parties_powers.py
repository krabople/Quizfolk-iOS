"""Run against isolated local state only. Never point this at production."""
import json, os, pathlib, sqlite3, time, urllib.request, urllib.error, uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=os.environ.get('QUIZFOLK_TEST_URL','http://127.0.0.1:8770/index.php?r=')
STATE=pathlib.Path(os.environ.get('QUIZFOLK_STATE_DIR',ROOT/'backend/private'))/'quizfolk.sqlite'
BANK={q['id']:q for q in json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))}
def req(route,body=None,token=None,status=200):
 h={'Content-Type':'application/json','X-Quizfolk-Client':'3'}
 if token:h['Authorization']='Bearer '+token
 try:
  with urllib.request.urlopen(urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=h),timeout=20) as r:code=r.status;data=json.load(r)
 except urllib.error.HTTPError as e:code=e.code;data=json.load(e)
 assert code==status,(route,code,data)
 return data
def user(name):
 token=req('register',{'name':name},status=201)['token'];return token,req('profile',token=token)['id']
(a,aid),(b,bid),(c,cid)=[user('New features '+x) for x in ['Alice','Bob','Eve']]
def wallet(t):return req('coins',token=t)['wallet']['coins']
def reveal(token,mid):
 r=req('round',{'match':mid},token);assert r['phase']=='reading' and r['question']['answers']==[]
 assert 2.8<r['readingRemaining']<=3
 req('power',{'match':mid,'turn':r['round'],'type':'right'},token,409)
 with sqlite3.connect(STATE) as db:db.execute('UPDATE matches SET preview_started=? WHERE id=?',(time.time()-4,mid))
 return req('reveal',{'match':mid},token)
def right(q):
 orig=BANK[q['id']];return q['answers'].index(orig['answers'][orig['correctIndex']])
def complete(token,mid,correct):
 for n in range(7):
  q=reveal(token,mid)['question'];i=right(q);r=req('answer',{'match':mid,'round':n,'answer':i if correct else (i+1)%4},token)
 return r
# A mixed match draws different categories and still has seven unique questions.
m=req('match',{'topic':'mixed'},a,201)
with sqlite3.connect(STATE) as db:packet=json.loads(db.execute('SELECT packet FROM matches WHERE id=?',(m['id'],)).fetchone()[0])
assert len({q['id'] for q in packet})==7 and len({q['categoryID'] for q in packet})==7
q=reveal(a,m['id'])['question'];n=right(q);coins=wallet(a)
p=req('power',{'match':m['id'],'turn':0,'type':'fifty'},a)
assert len(p['power']['hidden'])==2 and n not in p['power']['hidden'] and p['coins']==coins-5
assert req('power',{'match':m['id'],'turn':0,'type':'fifty'},a)['coins']==coins-5
assert req('reveal',{'match':m['id']},a)['power']['hidden']==p['power']['hidden']
req('power',{'match':m['id'],'turn':0,'type':'right'},a,409)
req('power',{'match':m['id'],'turn':0,'type':'fifty'},b,404)
req('answer',{'match':m['id'],'round':0,'answer':n},a)
reveal(a,m['id']);req('power',{'match':m['id'],'turn':1,'type':'fifty'},a,409)
# Double Choice preserves the original timer and hides only the first wrong pick.
d=req('match',{'topic':'22'},b,201);q=reveal(b,d['id'])['question'];n=right(q)
req('power',{'match':d['id'],'turn':0,'type':'double'},b)
with sqlite3.connect(STATE) as db:start=db.execute('SELECT started FROM matches WHERE id=?',(d['id'],)).fetchone()[0]
bad=(n+1)%4;r=req('answer',{'match':d['id'],'round':0,'answer':bad},b)
assert r['retry'] and r['correctIndex']==-1 and r['power']['hidden']==[bad]
assert req('answer',{'match':d['id'],'round':0,'answer':bad},b)['retry']
with sqlite3.connect(STATE) as db:assert db.execute('SELECT started FROM matches WHERE id=?',(d['id'],)).fetchone()[0]==start
assert req('answer',{'match':d['id'],'round':0,'answer':n},b)['points']>0
z=req('match',{'topic':'17'},c,201);q=reveal(c,z['id'])['question'];n=right(q)
p=req('power',{'match':z['id'],'turn':0,'type':'right'},c);assert p['power']['highlight']==n
with sqlite3.connect(STATE) as db:db.execute('UPDATE matches SET started=? WHERE id=?',(time.time()-11,z['id']))
assert req('answer',{'match':z['id'],'round':0,'answer':n},c)['points']==0
# Private, paid round-robin. Two home topics per pair per cycle, even if equal.
key=str(uuid.uuid4());room=req('party-create',{'requestID':key,'name':'Private game night','topic':'22','cycles':2,'days':7,'powers':False},a,201);rid=room['id']
assert req('party-create',{'requestID':key},a,201)['id']==rid
req('party-board&id='+rid,token=c,status=404)
req('tournament-board&event='+rid,token=c,status=403)
before=wallet(b);req('party-join',{'code':room['code'],'topic':'17'},b);req('party-join',{'code':room['code'],'topic':'17'},b);assert wallet(b)==before-10
req('party-start',{'party':rid},b,403);req('party-start',{'party':rid},a)
req('party-start',{'party':rid},a) # Retry creates no extra fixtures.
req('party-topic',{'party':rid,'topic':'12'},b,409)
board=req('party-board&id='+rid,token=a);assert len(board['fixtures'])==4
assert [f['topicID'] for f in board['fixtures']].count('17')==2
assert all(x['id']!=rid for x in req('tournaments',token=a)['events'])
req('party-play',{'party':rid,'fixture':board['fixtures'][0]['id']},c,404)
for f in board['fixtures']:
 am=req('party-play',{'party':rid,'fixture':f['id']},a);bm=req('party-play',{'party':rid,'fixture':f['id']},b)
 assert req('party-play',{'party':rid,'fixture':f['id']},a)['id']==am['id']
 q=reveal(a,am['id'])['question'];req('power',{'match':am['id'],'turn':0,'type':'right'},a,409)
 # Complete reuses the reading phase that has already been revealed.
 n=right(q);req('answer',{'match':am['id'],'round':0,'answer':n},a)
 for turn in range(1,7):
  q=reveal(a,am['id'])['question'];req('answer',{'match':am['id'],'round':turn,'answer':right(q)},a)
 assert req('match-progress',{'match':am['id']},a)['opponentAnswered']==0
 complete(b,bm['id'],False)
final=req('party-board&id='+rid,token=b)
assert final['party']['status']=='complete' and final['standings'][0]['id']==aid
assert final['standings'][0]['points']==12 and final['standings'][0]['played']==4
assert any(p['id']==rid and p['coins']==12 for p in req('prizes',token=a)['pending'])
assert any(p['id']==rid and p['coins']==8 for p in req('prizes',token=b)['pending'])
# Cancellation returns entry coins exactly once; lobby timeouts also refund.
before=wallet(a);r=req('party-create',{'requestID':str(uuid.uuid4()),'name':'Cancel lobby','topic':'22','cycles':1,'days':1,'powers':True},a,201)
req('party-cancel',{'party':r['id']},a);assert wallet(a)==before
req('party-cancel',{'party':r['id']},a,409);assert wallet(a)==before
r=req('party-create',{'requestID':str(uuid.uuid4()),'name':'Expire lobby','topic':'22','cycles':1,'days':1,'powers':True},a,201)
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(int(time.time())-1,r['id']))
req('prizes',token=a);assert wallet(a)==before
# Three players each host a leg against every opponent; identical home topics
# still yield two fixtures, rather than silently losing a home or away match.
three=req('party-create',{'requestID':str(uuid.uuid4()),'name':'Three friends','topic':'22','cycles':1,'days':1,'powers':True},c,201)
for token in [a,b]:req('party-join',{'code':three['code'],'topic':'22'},token)
req('party-start',{'party':three['id']},c)
fixtures=req('party-board&id='+three['id'],token=c)['fixtures']
assert len(fixtures)==6
assert len({tuple(sorted([f['a'],f['b']])) for f in fixtures})==3
for player in [aid,bid,cid]:assert sum(f['homeID']==player for f in fixtures)==2
active_fixture=next(f for f in fixtures if cid in [f['a'],f['b']])
active=req('party-play',{'party':three['id'],'fixture':active_fixture['id']},c)
reveal(c,active['id'])
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(int(time.time())-1,three['id']))
assert req('party-board&id='+three['id'],token=c)['party']['status']=='complete'
req('round',{'match':active['id']},c,410)
req('party-play',{'party':three['id'],'fixture':active_fixture['id']},c,410)
req('party-play',{'party':three['id'],'fixture':fixtures[0]['id']},c,404 if cid not in [fixtures[0]['a'],fixtures[0]['b']] else 410)
# Survival Double Choice grants exactly one extra pick, not an extra life after
# a second wrong answer; it cannot reset the run’s clock or score a retry.
event=min(req('tournaments',token=a)['events'],key=lambda x:x['coins'])
run=req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},a,201)
r=req('tournament-round',{'run':run['id']},a);assert r['question']['answers']==[] and r['readingRemaining']>2.8
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_runs SET preview=? WHERE id=?',(time.time()-4,run['id']))
q=req('tournament-reveal',{'run':run['id']},a)['question'];n=right(q)
req('tournament-power',{'run':run['id'],'turn':0,'type':'double'},a)
r=req('tournament-answer',{'run':run['id'],'turn':0,'answer':(n+1)%4},a)
assert r['retry'] and r['turn']==0 and r['state']=='playing'
r=req('tournament-answer',{'run':run['id'],'turn':0,'answer':(n+2)%4},a)
assert r['state']=='finished' and r['turn']==1 and r['score']==0
# Insufficient balance never creates a use record or a partial debit.
empty=req('match',{'topic':'17'},c,201);reveal(c,empty['id'])
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_wallet SET coins=0 WHERE player_id=?',(cid,))
req('power',{'match':empty['id'],'turn':0,'type':'fifty'},c,409)
with sqlite3.connect(STATE) as db:assert db.execute('SELECT COUNT(*) FROM power_uses WHERE context=?',('match:'+empty['id'],)).fetchone()[0]==0
assert wallet(c)==0
# Free private events stay free when public schedules migrate, admit a player
# with no coins, and produce neither a coin prize nor a tournament badge.
before=wallet(b)
free=req('party-create',{'requestID':str(uuid.uuid4()),'name':'Just for fun','topic':'22','cycles':1,'days':1,'powers':False,'entryCoins':0},b,201)
assert free['entryCoins']==0 and wallet(b)==before
quote=req('party-preview',{'code':free['code']},c);assert quote['entryCoins']==0 and not quote['alreadyMember']
req('party-join',{'code':free['code'],'topic':'17','expectedEntryCoins':10},c,409)
req('party-join',{'code':free['code'],'topic':'17','expectedEntryCoins':0},c)
req('tournaments',token=c);req('coins',token=c) # Public migration must not change a private fee.
assert req('party-board&id='+free['id'],token=c)['party']['entryCoins']==0 and wallet(c)==0
req('party-start',{'party':free['id']},b)
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(int(time.time())-1,free['id']))
req('prizes',token=b);req('party-board&id='+free['id'],token=c)
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT COUNT(*) FROM tournament_places WHERE event_id=?',(free['id'],)).fetchone()[0]==0
 assert db.execute('SELECT COUNT(*) FROM tournament_legacy_prize_floor WHERE event_id=?',(free['id'],)).fetchone()[0]==0
assert wallet(c)==0 and wallet(b)==before
cancel=req('party-create',{'requestID':str(uuid.uuid4()),'name':'Cancel free','topic':'22','cycles':1,'days':1,'powers':False,'entryCoins':0},b,201)
req('party-join',{'code':cancel['code'],'topic':'17'},c)
req('party-cancel',{'party':cancel['id']},b)
assert wallet(c)==0 and wallet(b)==before
paid=min(req('tournaments',token=c)['events'],key=lambda x:x['coins'])
req('tournament-enter',{'event':paid['id'],'requestID':str(uuid.uuid4())},c,409)
# Right Answer submits atomically. A lost response can be retried without a
# second debit, another answer, or moving the original answer deadline.
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_wallet SET coins=500 WHERE player_id=?',(aid,))
auto=req('match',{'topic':'22'},a,201);q=reveal(a,auto['id'])['question'];n=right(q)
before=wallet(a);body={'match':auto['id'],'turn':0,'type':'right','autoAnswer':True}
p=req('power',body,a);answer=p['duelAnswer']
assert answer['selectedIndex']==answer['correctIndex']==n and answer['points']>0
assert p['coins']==before-25 and req('power',body,a)['duelAnswer']==answer
assert req('answer',{'match':auto['id'],'round':0,'answer':(n+1)%4},a)==answer
with sqlite3.connect(STATE) as db:
 stored=json.loads(db.execute('SELECT answers FROM matches WHERE id=?',(auto['id'],)).fetchone()[0])
 assert len(stored)==1 and stored[0]['selected']==n
 assert db.execute('SELECT COUNT(*) FROM tournament_ledger WHERE player_id=? AND reference=?',(aid,'power:match:'+auto['id'])).fetchone()[0]==1
reveal(a,auto['id']);req('power',dict(body,turn=1),a,409)
# An expired request cannot buy a power-up or submit an answer.
late=req('match',{'topic':'22'},a,201);reveal(a,late['id']);before=wallet(a)
with sqlite3.connect(STATE) as db:db.execute('UPDATE matches SET started=? WHERE id=?',(time.time()-11,late['id']))
req('power',{'match':late['id'],'turn':0,'type':'right','autoAnswer':True},a,409)
assert wallet(a)==before
auto=req('tournament-enter',{'event':paid['id'],'requestID':str(uuid.uuid4())},a,201)
req('tournament-round',{'run':auto['id']},a)
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_runs SET preview=? WHERE id=?',(time.time()-4,auto['id']))
q=req('tournament-reveal',{'run':auto['id']},a)['question'];n=right(q);before=wallet(a)
body={'run':auto['id'],'turn':0,'type':'right','autoAnswer':True}
p=req('tournament-power',body,a);answer=p['tournamentAnswer']
assert answer['selectedIndex']==answer['correctIndex']==n and answer['correct'] and answer['streak']==1 and answer['turn']==1
assert p['coins']==before-25 and req('tournament-power',body,a)['tournamentAnswer']==answer
assert req('tournament-answer',{'run':auto['id'],'turn':0,'answer':-1},a)==answer
assert wallet(a)==before-25
print('PASS: private round-robin permissions, home/away cycles, results, prizes, refunds, mixed packets and atomic bounded power-ups')
