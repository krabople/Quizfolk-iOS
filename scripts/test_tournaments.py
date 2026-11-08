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
assert sorted(e['coins'] for e in listing['events'] if e['kind']=='daily')==[25,25,25]
assert all(e['coins']==50 for e in listing['events'] if e['kind']=='weekly')
assert all(e['tickets']==0 for e in listing['events'])
assert all(e['prizes']==([500,250,125] if e['kind']=='daily' else [1000,500,250]) and e['prizePool']==(875 if e['kind']=='daily' else 1750) and e['prizePolicy']=='fixed' for e in listing['events'])
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
assert board['event']['closed'] and board['event']['reward']==500 and board['wallet']['coins']==550
assert board['event']['prizePool']==875
assert req('tournament-board&event='+event['id'],token=a)['wallet']['coins']==550
assert req('tournament-board&event='+event['id'],token=b)['event']['reward']==250
trophies=[x for x in req('player',token=a)['badges'] if x['id'].startswith('tournament:')]
assert trophies and trophies[0]['earned'] and '#1' in trophies[0]['name']
req('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},a,410)
# Equal scores share place and prize; an abandoned run keeps its already-earned score.
second=next(e for e in listing['events'] if e['kind']=='daily' and e['id']!=event['id'])
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
assert len(rows)==2 and all(r['rank']==1 and r['reward']==375 for r in rows)
# A sole entrant receives the guaranteed first prize, independently of entry fees.
sparse=next(e for e in listing['events'] if e['kind']=='daily' and e['id'] not in [event['id'],second['id']])
before=req('tournaments',token=a)['wallet']['coins']
r=req('tournament-enter',{'event':sparse['id'],'requestID':str(uuid.uuid4())},a,201)
assert req('tournaments',token=a)['wallet']['coins']==before-25
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(time.time()-1,sparse['id']))
s=req('tournament-board&event='+sparse['id'],token=a)
assert s['wallet']['coins']==before-25+500 and s['event']['reward']==500 and s['event']['rank']==1
assert req('tournament-round',{'run':r['id']},a)['state']=='closed'
assert req('tournament-board&event='+sparse['id'],token=a)['wallet']['coins']==before-25+500
# Fixed weekly podiums, historical shortfalls, already-seen zero prizes and
# preservation of more generous old awards. Fixtures live only in this temp DB.
c=req('register',{'name':'Tournament Cara'},status=201)['token']
cid=req('profile',token=c)['id'];req('coins',token=c)
before_a=req('coins',token=a)['wallet']['coins'];before_b=req('coins',token=b)['wallet']['coins']
now=int(time.time())
with sqlite3.connect(STATE) as db:
 db.execute('INSERT INTO tournament_events VALUES(?,?,?,?,?,?,?,?)',('weekly-fixed','22','weekly',1,now-1,100,0,0))
 for i,pid in enumerate([aid,bid,cid]):
  db.execute('INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,score,streak,state,created) VALUES(?,?,?,?,?,?,?,?,?)',('fixed-run-'+str(i),'weekly-fixed',pid,'fixed-key-'+str(i),'[]',100-i,1,'finished',now-100))
 for name,pid,reward in [('short',aid,25),('zero',bid,0),('generous',cid,250)]:
  event_id='legacy-'+name
  db.execute('INSERT INTO tournament_events VALUES(?,?,?,?,?,?,?,?)',(event_id,'22','daily',1,now-2,0,0,1))
  db.execute('INSERT INTO tournament_places VALUES(?,?,?,?,?,?)',(event_id,pid,1,60,3,reward))
  db.execute('INSERT INTO tournament_prize_receipts VALUES(?,?,?)',(pid,event_id,now-1))
  if reward:
   db.execute('INSERT INTO tournament_ledger VALUES(?,?,?,?,?)',(pid,'prize:'+event_id,reward,0,now-2))
   db.execute('UPDATE tournament_wallet SET coins=coins+? WHERE player_id=?',(reward,pid))
assert req('coins',token=a)['wallet']['coins']==before_a+150+500
assert req('coins',token=b)['wallet']['coins']==before_b+150+250
assert req('coins',token=c)['wallet']['coins']==100+250+125
assert req('coins',token=a)['wallet']['coins']==before_a+150+500
prizes=req('prizes',token=a)
short=next(x for x in prizes['pending'] if x['id']=='legacy-short')
assert short['coins']==150 and short['adjustmentCoins']==125
assert any(x['id']=='legacy-zero' and x['coins']==150 for x in req('prizes',token=b)['pending'])
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT reward FROM tournament_places WHERE event_id=?',('legacy-generous',)).fetchone()[0]==250
 assert db.execute('SELECT COUNT(*) FROM tournament_ledger WHERE reference=?',('fixed-prizes-v1:legacy-short',)).fetchone()[0]==1
 assert [x[0] for x in db.execute('SELECT reward FROM tournament_places WHERE event_id=? ORDER BY rank',('weekly-fixed',))]==[500,250,125]

# A weekly event advertised under v2 pays its persisted1000/500/250 terms.
weekly=next(e for e in listing['events'] if e['kind']=='weekly')
for index,token in enumerate([a,b,c]):
 before=req('coins',token=token)['wallet']['coins']
 entered=req('tournament-enter',{'event':weekly['id'],'requestID':str(uuid.uuid4())},token,201)
 assert req('coins',token=token)['wallet']['coins']==before-50
 with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_runs SET score=?,streak=1,state="finished" WHERE id=?',(100-index,entered['id']))
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(int(time.time())-1,weekly['id']))
weekly_board=req('tournament-board&event='+weekly['id'],token=a)
assert weekly_board['event']['prizes']==[1000,500,250] and weekly_board['event']['prizePool']==1750
assert [row['reward'] for row in weekly_board['entries']]==[1000,500,250]
assert req('tournament-board&event='+weekly['id'],token=a)['wallet']==weekly_board['wallet']

# Model an in-progress deployment: old entry prices and actual entry debits,
# including two differently priced attempts in one event. The ledger, rather
# than the event's advertised fee, determines each one-time excess refund.
now=int(time.time());day=now//86400*86400
with sqlite3.connect(STATE) as db:
 for eid,kind,fee,ends,settled in [('open-old-daily','daily',75,now+3600,0),('open-old-weekly','weekly',100,now+3600,0),('old-closed-daily','daily',75,now-1,1),('private-unchanged','party',10,now+3600,0)]:
  db.execute('INSERT INTO tournament_events VALUES(?,?,?,?,?,?,?,?)',(eid,'22',kind,day,ends,fee,0,settled))
 db.execute('INSERT INTO tournament_fixed_prizes_v1 VALUES(?,?)',('old-closed-daily',now))
 db.execute('INSERT INTO tournament_places VALUES(?,?,?,?,?,?)',('old-closed-daily',aid,1,77,5,150))
 db.execute('INSERT INTO tournament_prize_receipts VALUES(?,?,?)',(aid,'old-closed-daily',now))
 for rid,eid,paid in [('old-d1','open-old-daily',75),('old-d2','open-old-daily',50),('old-w1','open-old-weekly',100),('closed-no-refund','old-closed-daily',75),('private-no-refund','private-unchanged',10)]:
  db.execute('INSERT INTO tournament_runs(id,event_id,player_id,request_key,deck,turn,score,streak,state,created) VALUES(?,?,?,?,?,?,?,?,?,?)',(rid,eid,aid,rid+'-key','["answered","remaining"]',1,77,5,'finished',now-10))
  db.execute('INSERT INTO tournament_ledger VALUES(?,?,?,?,?)',(aid,'entry:'+rid,-paid,0,now-10))
  db.execute('UPDATE tournament_wallet SET coins=coins-? WHERE player_id=?',(paid,aid))
 old_runs=db.execute('SELECT * FROM tournament_runs WHERE id IN ("old-d1","old-d2","old-w1","closed-no-refund","private-no-refund") ORDER BY id').fetchall()
 old_schedule=db.execute('SELECT event_ids FROM tournament_daily_schedule WHERE day=?',(day,)).fetchone()[0]
 before_refund=db.execute('SELECT coins FROM tournament_wallet WHERE player_id=?',(aid,)).fetchone()[0]
 old_receipt=db.execute('SELECT * FROM tournament_prize_receipts WHERE event_id="old-closed-daily"').fetchall()
assert req('coins',token=a)['wallet']['coins']==before_refund+125
for _ in range(3):assert req('tournaments',token=a)['wallet']['coins']==before_refund+125
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT COUNT(*),SUM(coins) FROM tournament_ledger WHERE reference LIKE "public-entry-v2:%"').fetchone()==(3,125)
 assert db.execute('SELECT * FROM tournament_runs WHERE id IN ("old-d1","old-d2","old-w1","closed-no-refund","private-no-refund") ORDER BY id').fetchall()==old_runs
 assert db.execute('SELECT event_ids FROM tournament_daily_schedule WHERE day=?',(day,)).fetchone()[0]==old_schedule
 assert len(set(json.loads(old_schedule)))==3
 assert db.execute('SELECT coins FROM tournament_events WHERE id="old-closed-daily"').fetchone()[0]==75
 assert db.execute('SELECT coins FROM tournament_events WHERE id="private-unchanged"').fetchone()[0]==10
 assert db.execute('SELECT * FROM tournament_prize_receipts WHERE event_id="old-closed-daily"').fetchall()==old_receipt
 assert db.execute('SELECT reward FROM tournament_places WHERE event_id="old-closed-daily"').fetchone()[0]==150
for eid,fee,prizes in [('open-old-daily',25,[500,250,125]),('open-old-weekly',50,[1000,500,250]),('old-closed-daily',75,[150,100,50])]:
 card=req('tournament-board&event='+eid,token=a)['event']
 assert card['coins']==fee and card['prizes']==prizes
for token in [a,b,c]:req('delete-account',{},token)
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT COUNT(*) FROM tournament_runs WHERE player_id IN (?,?)',(aid,bid)).fetchone()[0]==0
 assert db.execute('SELECT COUNT(*) FROM tournament_ledger WHERE player_id IN (?,?)',(aid,bid)).fetchone()[0]==0
 assert db.execute('SELECT COUNT(*) FROM question_seen WHERE player_id IN (?,?)',(aid,bid)).fetchone()[0]==0
print('PASS:25/50 daily/weekly fees, v2 podium snapshots/settlement, excess-entry refunds once, preserved closed/private history, survival/ties, v1 historical repair, timing, hidden answers, question repair and deletion')
