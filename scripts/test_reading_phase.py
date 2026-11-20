"""Variable reading time must not expose answers early or consume answer time."""
import json,math,os,pathlib,sqlite3,time,urllib.request,urllib.error,uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=os.environ['QUIZFOLK_TEST_URL'];assert BASE.startswith('http://127.0.0.1:')
STATE=pathlib.Path(os.environ['QUIZFOLK_STATE_DIR'])/'quizfolk.sqlite'
bank=json.loads((ROOT/'data/questions.json').read_text(encoding='utf8'))
token=None
def req(route,body=None,status=200):
 h={'Content-Type':'application/json','X-Quizfolk-Client':'3'}
 if token:h['Authorization']='Bearer '+token
 request=urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=h)
 try:
  with urllib.request.urlopen(request,timeout=15) as response:code=response.status;reply=json.load(response)
 except urllib.error.HTTPError as e:code=e.code;reply=json.load(e)
 assert code==status,(route,code,reply)
 return reply
def allowance(prompt):
 words=prompt.split();return 3+math.ceil(max(0,(len(words)-12)/3,(len(' '.join(words))-72)/18))
token=req('register',{'name':'Reading clock contract'},201)['token']
q=max(bank,key=lambda q:allowance(q['prompt']));duration=allowance(q['prompt']);assert duration>5
m=req('match',{'topic':q['categoryID']},201)['id']
with sqlite3.connect(STATE) as db:
 packet=json.loads(db.execute('SELECT packet FROM matches WHERE id=?',(m,)).fetchone()[0])
 packet=[q]+[item for item in packet if item['id']!=q['id'] and item['prompt']!=q['prompt']][:6]
 assert len(packet)==7
 db.execute('UPDATE matches SET packet=? WHERE id=?',(json.dumps(packet),m))
r=req('round',{'match':m});assert duration-.5<r['readingRemaining']<=duration and r['question']['answers']==[]
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT started FROM matches WHERE id=?',(m,)).fetchone()[0] is None
 db.execute('UPDATE matches SET preview_started=? WHERE id=?',(time.time()-4,m))
r=req('reveal',{'match':m});assert r['phase']=='reading' and r['remaining']==10 and not r['question']['answers']
req('answer',{'match':m,'round':0,'answer':q['correctIndex']},409)
with sqlite3.connect(STATE) as db:db.execute('UPDATE matches SET preview_started=? WHERE id=?',(time.time()-duration-1,m))
r=req('reveal',{'match':m});assert r['phase']=='answer' and len(r['question']['answers'])==4 and r['remaining']>9.8
assert req('answer',{'match':m,'round':0,'answer':q['correctIndex']})['points']==20
# An isolated event in the already-selected long-question topic makes this
# reading-clock contract independent of today's rotating tournament subjects.
req('tournaments');e={'id':'reading-clock-fixture','topicID':q['categoryID']}
with sqlite3.connect(STATE) as db:
 db.execute('INSERT INTO tournament_events(id,topic,kind,starts,ends,coins,tickets) VALUES(?,?,"weekly",?,?,50,0)',(e['id'],e['topicID'],int(time.time())-10,int(time.time())+3600))
duration=allowance(q['prompt']);assert duration>5
run=req('tournament-enter',{'event':e['id'],'requestID':str(uuid.uuid4())},201)['id']
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_runs SET deck=?,question_keys=? WHERE id=?',(json.dumps([q['id']]),'{}',run))
r=req('tournament-round',{'run':run});assert duration-.5<r['readingRemaining']<=duration and not r['question']['answers']
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_runs SET preview=? WHERE id=?',(time.time()-4,run))
r=req('tournament-reveal',{'run':run});assert r['phase']=='reading' and r['remaining']==10
req('tournament-answer',{'run':run,'turn':0,'answer':q['correctIndex']},409)
with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_runs SET preview=? WHERE id=?',(time.time()-duration-1,run))
r=req('tournament-reveal',{'run':run});assert r['phase']=='answer' and len(r['question']['answers'])==4 and r['remaining']>9.8
correct=r['question']['answers'].index(q['answers'][q['correctIndex']])
assert req('tournament-answer',{'run':run,'turn':0,'answer':correct})['points']==20
print('Long duel/tournament previews hide answers, resist early reveal and preserve full answer time/scoring.')
