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
listing=req('tournaments',token=a);assert len(listing['events'])>=9
assert listing['wallet']=={'coins':100,'tickets':3,'dailyClaimed':False}
daily=req('tournament-daily',{},a);assert daily=={'coins':150,'tickets':5,'dailyClaimed':True}
assert req('tournament-daily',{},a)==daily
event=next(e for e in listing['events'] if e['coins']==25)
key=str(uuid.uuid4());body={'event':event['id'],'requestID':key}
run=req('tournament-enter',body,a,201);assert run['score']==0 and run['streak']==0
assert req('tournament-enter',body,a)['id']==run['id']
assert req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},a)['id']==run['id']
assert req('tournaments',token=a)['wallet']['coins']==125
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
result,_=answer(a,retry['id'],0,True,11)
assert result['score']==0 and result['streak']==0 and result['state']=='finished'
board=req('tournament-board&event='+event['id'],token=a)
assert board['event']['best']==340 and board['event']['attempts']==2
assert board['entries'][0]['score']==340 and board['entries'][0]['rank']==1
assert board['wallet']['coins']==100
# Another human can play later, independently. Best scores are compared, never summed.
other=req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},b,201)
result,_=answer(b,other['id'],0,True,4.1);assert result['points']==16
result,_=answer(b,other['id'],1,False);assert result['score']==16
assert req('profile',token=a)['xp']==0
assert req('player&id='+bid,token=a)['headToHead']['games']==0
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(time.time()-1,event['id']))
board=req('tournament-board&event='+event['id'],token=a)
assert board['event']['closed'] and board['event']['reward']==500 and board['wallet']['coins']==600
assert req('tournament-board&event='+event['id'],token=a)['wallet']['coins']==600
assert req('tournament-board&event='+event['id'],token=b)['event']['reward']==250
req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},a,410)
# Equal scores share place and prize; an abandoned run keeps its already-earned score.
free=next(e for e in listing['events'] if not e['coins'] and not e['tickets'])
for token in [a,b]:
 r=req('tournament-enter',{'event':free['id'],'requestID':str(uuid.uuid4())},token,201)
 answer(token,r['id'],0)
 ended=req('tournament-end',{'run':r['id']},token);assert ended['score']==20
 assert req('tournament-end',{'run':r['id']},token)==ended
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(time.time()-1,free['id']))
rows=req('tournament-board&event='+free['id'],token=a)['entries']
assert len(rows)==2 and all(r['rank']==1 and r['reward']==500 for r in rows)
# Sparse fields do not fabricate players or winners: refund entry fees exactly once.
sparse=next(e for e in listing['events'] if e['tickets']==1)
before=req('tournaments',token=a)['wallet']['tickets']
r=req('tournament-enter',{'event':sparse['id'],'requestID':str(uuid.uuid4())},a,201)
assert req('tournaments',token=a)['wallet']['tickets']==before-1
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(time.time()-1,sparse['id']))
s=req('tournament-board&event='+sparse['id'],token=a)
assert s['wallet']['tickets']==before and s['event']['reward']==0
assert req('tournament-round',{'run':r['id']},a)['state']=='closed'
assert req('tournament-board&event='+sparse['id'],token=a)['wallet']['tickets']==before
for token in [a,b]:req('delete-account',{},token)
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT COUNT(*) FROM tournament_runs WHERE player_id IN (?,?)',(aid,bid)).fetchone()[0]==0
 assert db.execute('SELECT COUNT(*) FROM tournament_ledger WHERE player_id IN (?,?)',(aid,bid)).fetchone()[0]==0
print('PASS: survival beyond seven questions, speed points, first-miss and timeout elimination, hidden answers, reading phase, no repeated questions, atomic/idempotent credits and entry, private runs, best-only rankings, asynchronous players, tied prizes, one-time settlement, sparse-field refunds, no duel XP or fake head-to-head wins, and deletion')
