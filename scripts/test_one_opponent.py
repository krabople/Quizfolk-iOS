"""A round belongs to one opponent, including bot and paired-human games."""
import json,os,pathlib,sqlite3,time,urllib.request,urllib.error,uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=os.environ['QUIZFOLK_TEST_URL'];assert BASE.startswith('http://127.0.0.1:')
STATE=pathlib.Path(os.environ['QUIZFOLK_STATE_DIR'])/'quizfolk.sqlite'
BANK={q['id']:q for q in json.loads((ROOT/'data/questions.json').read_text(encoding='utf8'))}
def req(route,body=None,token=None,status=200):
 h={'Content-Type':'application/json','X-Quizfolk-Client':'2'}
 if token:h['Authorization']='Bearer '+token
 request=urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=h)
 try:
  with urllib.request.urlopen(request,timeout=15) as response:code=response.status;reply=json.load(response)
 except urllib.error.HTTPError as e:code=e.code;reply=json.load(e)
 assert code==status,(route,code,reply)
 return reply
def user(name):return req('register',{'name':name},status=201)['token']
def finish(token,match,wrong=False):
 packet=[]
 for turn in range(7):
  q=req('round',{'match':match['id']},token)['question'];packet.append(q)
  original=BANK[q['id']];correct=q['answers'].index(original['answers'][original['correctIndex']])
  result=req('answer',{'match':match['id'],'round':turn,'answer':(correct+1)%4 if wrong and turn==0 else correct},token)
 return packet,result
a,b,c,d,e=[user('Single rival '+n) for n in ['A','B','C','D','E']]
original=req('match',{'topic':'22'},a,201);finish(a,original)
before=req('profile',token=a)
# An available completed bot game must not instantly become a human replay.
ckey=str(uuid.uuid4());search=req('match-search',{'topic':'22','requestID':ckey},c)
assert search['state']=='searching' and search['match'] is None
with sqlite3.connect(STATE) as db:db.execute('UPDATE searches SET created=? WHERE id=?',(time.time()-7,search['searchID']))
bot=req('match-search',{'topic':'22','requestID':ckey},c)['match'];assert bot['kind']=='bot' and bot['opponentID'] is None
# A later search cannot take a round already assigned to a bot.
dkey=str(uuid.uuid4());ds=req('match-search',{'topic':'22','requestID':dkey},d);assert ds['state']=='searching'
bkey=str(uuid.uuid4());bs=req('match-search',{'topic':'22','requestID':bkey},b)['match']
dm=req('match-search',{'topic':'22','requestID':dkey},d)['match']
assert bs['kind']==dm['kind']=='challenge' and bs['duelID']==dm['duelID']
assert req('match-search',{'topic':'22','requestID':ckey},c)['match']['id']==bot['id']
bp,pending=finish(b,bs,wrong=True);assert pending['pending']
dp,result=finish(d,dm);assert bp==dp and not result['pending']
duel_b=next(x for x in req('duels',token=b)['duels'] if x['id']==bs['duelID'])
duel_d=next(x for x in req('duels',token=d)['duels'] if x['id']==dm['duelID'])
assert duel_b['status']==duel_d['status']=='complete'
# Completed human challenges are not a reusable pool either.
assert req('match-search',{'topic':'22','requestID':str(uuid.uuid4())},e)['state']=='searching'
after=req('profile',token=a)
assert all(before[k]==after[k] for k in ['matches','wins','xp'])
with sqlite3.connect(STATE) as db:
 assert db.execute('SELECT COUNT(*) FROM matches WHERE opponent_match IS NOT NULL OR kind="human"').fetchone()[0]==0
 rows=db.execute('SELECT player_id,opponent_id FROM matches WHERE duel_id=?',(bs['duelID'],)).fetchall()
 assert len(rows)==2 and rows[0]==rows[1][::-1]
print('PASS: bot/completed-human rounds never recycled; bot assignment immutable; paired humans share one result and two match records.')
