"""End-to-end contract tests against an isolated local PHP server, never production."""
import base64,json,urllib.request,urllib.error,pathlib,sqlite3,time,os
BASE=os.environ.get('QUIZFOLK_TEST_URL','http://127.0.0.1:8770/index.php?r=')
ROOT=pathlib.Path(__file__).resolve().parents[1]
BANK={q['id']:q for q in json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))}
STATE=ROOT/'backend/private/quizfolk.sqlite'
def req(route,body=None,token=None,status=200):
 headers={'Content-Type':'application/json','X-Quizfolk-Client':'2'}
 if token:headers['Authorization']='Bearer '+token
 r=urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=headers)
 try:
  with urllib.request.urlopen(r,timeout=15) as v:code=v.status; data=json.load(v)
 except urllib.error.HTTPError as e:code=e.code;data=json.load(e)
 assert code==status,(route,code,data)
 return data
a=req('register',{'name':'Contract tester A'},status=201)['token']
b=req('register',{'name':'Contract tester B'},status=201)['token']
req('register',{'name':'contract TESTER a'},status=409)
req('update-profile',{'name':'Contract tester B'},a,409)
assert req('profile',token=a)['name']=='Contract tester A'
x=req('register',{'automaticName':True},status=201);y=req('register',{'automaticName':True},status=201)
assert x['name']!=y['name']
req('delete-account',{},x['token']);req('delete-account',{},y['token'])
req('profile',status=401)
req('update-profile',{'name':'Straße player'},a)
req('update-profile',{'name':'STRASSE   PLAYER'},b,409)
req('update-profile',{'name':'Updated tester A'},a)
assert req('profile',token=a)['name']=='Updated tester A'
m=req('match',{'topic':'22'},a,201)
assert m['kind']=='bot'
with sqlite3.connect(STATE) as db:assert db.execute('SELECT started FROM matches WHERE id=?',(m['id'],)).fetchone()[0] is None
req('update-avatar',{'avatar':'not-image-data'},a,400)
picture=base64.b64encode((ROOT/'scripts/test-avatar.jpg').read_bytes()).decode()
req('update-avatar',{'avatar':picture},a)
assert req('profile',token=a)['avatar'] is not None
req('round',{'match':m['id']},b,404)
first=[];total=0
for i in range(7):
 r=req('round',{'match':m['id']},a);q=r['question'];first.append(q)
 assert r['round']==i and 'correctIndex' not in q
 again=req('round',{'match':m['id']},a)
 assert again['question']==q and again['remaining']<=r['remaining']
 item=BANK[q['id']];right=q['answers'].index(item['answers'][item['correctIndex']])
 if i==1:
  with sqlite3.connect(STATE) as db:db.execute('UPDATE matches SET started=? WHERE id=?',(time.time()-11,m['id']))
 result=req('answer',{'match':m['id'],'round':i,'answer':right,'elapsed':0},a)
 assert result['points']==(0 if i==1 else (40 if i==6 else 20)),result
 repeat=req('answer',{'match':m['id'],'round':i,'answer':-1},a)
 assert repeat==result
 total+=result['points']
p=req('profile',token=a);assert p['matches']==1 and p['xp']==total+40+(100 if total>result['opponentScore'] else (50 if total==result['opponentScore'] else 0)) and p['correct']==6
req('round',{'match':m['id']},a,409)
ghost=req('match',{'topic':'22'},b,201);assert ghost['kind']=='human' and ghost['opponentAvatar'] is not None
for i in range(7):
 r=req('round',{'match':ghost['id']},b);assert r['question']==first[i]
 req('answer',{'match':ghost['id'],'round':i,'answer':-1},b)
board=req('leaderboard&topic=22&period=month',token=a)['entries'];assert len(board)==2
assert req('leaderboard&topic=11&period=all',token=a)['entries']==[]
req('leaderboard',token=a,status=400)
with sqlite3.connect(STATE) as db:
 db.execute('UPDATE matches SET completed=? WHERE id=?',(1,m['id']))
assert len(req('leaderboard&topic=22&period=month',token=a)['entries'])==1
assert len(req('leaderboard&topic=22&period=all',token=a)['entries'])==2
req('update-avatar',{'avatar':None},a)
assert req('profile',token=a)['avatar'] is None
req('report',{'question':first[0]['id'],'reason':'Contract test report'},a)
req('delete-account',{},a);req('delete-account',{},b)
req('profile',token=a,status=401)
print('PASS: authentication, ownership, seven rounds, answer secrecy, timing, timeout, idempotence, human replay, stats, monthly topic XP, unique names, avatar validation/sharing/removal, reports and account deletion')
