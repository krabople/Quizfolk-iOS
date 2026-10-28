"""Survival competition contracts; isolated local service only."""
import json,urllib.request,urllib.error,pathlib,sqlite3,time,os,uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=os.environ.get('QUIZFOLK_TEST_URL','http://127.0.0.1:8770/index.php?r=')
STATE=pathlib.Path(os.environ.get('QUIZFOLK_STATE_DIR',ROOT/'backend/private'))/'quizfolk.sqlite'
BANK={q['id']:q for q in json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))}
def req(route,body=None,token=None,status=200):
 h={'Content-Type':'application/json','X-Quizfolk-Client':'3'}
 if token:h['Authorization']='Bearer '+token
 r=urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=h)
 try:
  with urllib.request.urlopen(r,timeout=20) as v:code=v.status;data=json.load(v)
 except urllib.error.HTTPError as e:code=e.code;data=json.load(e)
 assert code==status,(route,code,data);return data
a=req('register',{'name':'Tournament Alice'},status=201)['token']
b=req('register',{'name':'Tournament Bob'},status=201)['token']
aid=req('profile',token=a)['id'];bid=req('profile',token=b)['id']
listing=req('tournaments',token=a)
assert len([e for e in listing['events'] if e['kind']=='daily' and e['featured']])==3
assert len([e for e in listing['events'] if e['kind']=='weekly'])==3
assert listing['wallet']=={'coins':100,'tickets':0,'dailyClaimed':False}
assert sorted(e['coins'] for e in listing['events'] if e['kind']=='daily')==[25,50,75]
assert all(e['coins']==100 for e in listing['events'] if e['kind']=='weekly')
assert all(e['tickets']==0 for e in listing['events'])
assert 'Daily Trail' in req('tournament-daily',{},a,409)['error']
assert req('tournaments',token=a)['wallet']==listing['wallet']
event=next(e for e in listing['events'] if e['coins']==25)
# Rejected admission cannot create a run or deduct credits. The client can show
# this failure while still on the details page, including a stale-balance race.
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_wallet SET coins=0 WHERE player_id=?',(aid,))
failure=req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},a,409)
assert 'Not enough coins' in failure['error']
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT COUNT(*) FROM tournament_runs WHERE player_id=?',(aid,)).fetchone()[0]==0
 assert db.execute('SELECT coins FROM tournament_wallet WHERE player_id=?',(aid,)).fetchone()[0]==0
 db.execute('UPDATE tournament_wallet SET coins=100 WHERE player_id=?',(aid,))
key=str(uuid.uuid4());body={'event':event['id'],'requestID':key}
run=req('tournament-enter',body,a,201);assert run['score']==0 and run['streak']==0
assert req('tournament-enter',body,a)['id']==run['id']
assert req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},a)['id']==run['id']
assert req('tournaments',token=a)['wallet']['coins']==75
req('tournament-round',{'run':run['id']},b,404)
seen=set()
def answer(token,run_id,turn,right=True,elapsed=0.1):
 r=req('tournament-round',{'run':run_id},token)
 assert r['phase']=='reading' and r['question']['answers']==[] and r['remaining']==10
 assert 'correctIndex' not in r['question']
 assert req('tournament-reveal',{'run':run_id},token)['phase']=='reading'
 req('tournament-answer',{'run':run_id,'turn':turn,'answer':0},token,409)
 with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_runs SET preview=? WHERE id=?',(time.time()-3,run_id))
 shown=req('tournament-reveal',{'run':run_id},token);assert shown['remaining']>9
 q=shown['question'];original=BANK[q['id']]
 correct=q['answers'].index(original['answers'][original['correctIndex']])
 with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_runs SET started=? WHERE id=?',(time.time()-elapsed,run_id))
 body={'run':run_id,'turn':turn,'answer':correct if right else (correct+1)%4}
 result=req('tournament-answer',body,token)
 assert req('tournament-answer',body,token)==result
 return result,q['id']
# An actual run exceeds seven questions, accumulates points, then ends at the first miss.
for i in range(17):
 result,qid=answer(a,run['id'],i)
 assert qid not in seen;seen.add(qid)
 assert result['score']==(i+1)*20 and result['streak']==i+1 and result['state']=='playing'
result,_=answer(a,run['id'],17,False)
assert result['score']==340 and result['streak']==17 and result['state']=='finished'
assert req('tournament-round',{'run':run['id']},a)['state']=='finished'
# A timeout on a correct choice ends the run; it cannot earn points.
retry=req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},a,201)
with sqlite3.connect(STATE) as db:
 deck=json.loads(db.execute('SELECT deck FROM tournament_runs WHERE id=?',(retry['id'],)).fetchone()[0])
 previously_seen={row[0] for row in db.execute('SELECT question_id FROM question_seen WHERE player_id=?',(aid,))}
 assert set(deck[-len(previously_seen):])==previously_seen
 assert not set(deck[:-len(previously_seen)]).intersection(previously_seen)
result,_=answer(a,retry['id'],0,True,11)
assert result['score']==0 and result['streak']==0 and result['state']=='finished'
board=req('tournament-board&event='+event['id'],token=a)
assert board['event']['best']==340 and board['event']['attempts']==2
assert board['entries'][0]['score']==340 and board['entries'][0]['rank']==1
assert board['wallet']['coins']==50
# Another human can play later, independently. Best scores are compared, never summed.
other=req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},b,201)
result,_=answer(b,other['id'],0,True,4.1);assert result['points']==16
result,_=answer(b,other['id'],1,False);assert result['score']==16
assert req('profile',token=a)['xp']==0
assert req('player&id='+bid,token=a)['headToHead']['games']==0
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(time.time()-1,event['id']))
board=req('tournament-board&event='+event['id'],token=a)
assert board['event']['closed'] and board['event']['reward']==45 and board['wallet']['coins']==95
assert board['event']['prizePool']==75
assert req('tournament-board&event='+event['id'],token=a)['wallet']['coins']==95
assert req('tournament-board&event='+event['id'],token=b)['event']['reward']==30
trophies=[x for x in req('player',token=a)['badges'] if x['id'].startswith('tournament:')]
assert trophies and trophies[0]['earned'] and '#1' in trophies[0]['name']
req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},a,410)
# Equal scores share place and prize; an abandoned run keeps its already-earned score.
second=next(e for e in listing['events'] if e['coins']==50)
for token in [a,b]:
 r=req('tournament-enter',{'event':second['id'],'requestID':str(uuid.uuid4())},token,201)
 answer(token,r['id'],0)
 if token==a:
  with sqlite3.connect(STATE) as db:
   deck=json.loads(db.execute('SELECT deck FROM tournament_runs WHERE id=?',(r['id'],)).fetchone()[0])
   db.execute('UPDATE tournament_runs SET deck=? WHERE id=?',(json.dumps([deck[0],'removed-question',deck[2]]),r['id']))
  repaired=req('tournament-round',{'run':r['id']},a)
  assert repaired['question']['id']==deck[2] and repaired['turn']==1 and repaired['score']==20 and repaired['phase']=='reading'
  # A question removed after display restarts the reading phase without charging
  # a wrong answer or losing the earned prefix.
  with sqlite3.connect(STATE) as db:
   db.execute('UPDATE tournament_runs SET deck=?,started=?,preview=? WHERE id=?',(json.dumps([deck[0],'removed-during-answer',deck[3]]),time.time(),time.time()-3,r['id']))
  changed=req('tournament-answer',{'run':r['id'],'turn':1,'answer':0},a)
  assert changed['questionChanged'] and changed['score']==20 and changed['turn']==1
  assert req('tournament-answer',{'run':r['id'],'turn':1,'answer':0},a)==changed
  with sqlite3.connect(STATE) as db:
   db.execute('UPDATE tournament_runs SET deck=? WHERE id=?',(json.dumps([deck[0],'last-removed-question']),r['id']))
  completed=req('tournament-round',{'run':r['id']},a)
  assert completed['state']=='cleared' and completed['score']==20 and completed['streak']==1
 ended=req('tournament-end',{'run':r['id']},token);assert ended['score']==20
 assert req('tournament-end',{'run':r['id']},token)==ended
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(time.time()-1,second['id']))
rows=req('tournament-board&event='+second['id'],token=a)['entries']
assert len(rows)==2 and all(r['rank']==1 and r['reward']==50 for r in rows)
# A sole entrant still receives first place and the actual entry pool once.
sparse=next(e for e in listing['events'] if e['coins']==75)
before=req('tournaments',token=a)['wallet']['coins']
r=req('tournament-enter',{'event':sparse['id'],'requestID':str(uuid.uuid4())},a,201)
assert req('tournaments',token=a)['wallet']['coins']==before-75
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(time.time()-1,sparse['id']))
s=req('tournament-board&event='+sparse['id'],token=a)
assert s['wallet']['coins']==before and s['event']['reward']==75 and s['event']['rank']==1
assert req('tournament-round',{'run':r['id']},a)['state']=='closed'
assert req('tournament-board&event='+sparse['id'],token=a)['wallet']['coins']==before
for token in [a,b]:req('delete-account',{},token)
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT COUNT(*) FROM tournament_runs WHERE player_id IN (?,?)',(aid,bid)).fetchone()[0]==0
 assert db.execute('SELECT COUNT(*) FROM tournament_ledger WHERE player_id IN (?,?)',(aid,bid)).fetchone()[0]==0
 assert db.execute('SELECT COUNT(*) FROM question_seen WHERE player_id IN (?,?)',(aid,bid)).fetchone()[0]==0
print('PASS: three paid daily topics, coins-only entry, balance checks, survival beyond seven questions, speed points, first-miss and timeout elimination, hidden answers, reading phase, fresh-before-seen questions, removed-question recovery, atomic/idempotent credits and entry, private runs, best-only rankings, asynchronous players, tied entry-pool prizes, one-time settlement, sole-player prizes, no duel XP or fake head-to-head wins, and deletion')
