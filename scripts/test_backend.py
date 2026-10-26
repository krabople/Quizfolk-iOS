"""End-to-end contract tests against an isolated local PHP server, never production."""
import json,urllib.request,urllib.error,pathlib,sqlite3,time
BASE='http://127.0.0.1:8766/index.php?r='
ROOT=pathlib.Path(__file__).resolve().parents[1]
BANK={q['id']:q for q in json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))}
STATE=ROOT/'backend/private/quizfolk.sqlite'
def req(route,body=None,token=None,status=200):
 headers={'Content-Type':'application/json'}
 if token:headers['Authorization']='Bearer '+token
 r=urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=headers)
 try:
  with urllib.request.urlopen(r) as v:code=v.status; data=json.load(v)
 except urllib.error.HTTPError as e:code=e.code;data=json.load(e)
 assert code==status,(route,code,data)
 return data
a=req('register',{'name':'Contract tester A'},status=201)['token']
b=req('register',{'name':'Contract tester B'},status=201)['token']
req('profile',status=401)
m=req('match',{'topic':'22'},a,201)
assert m['kind']=='bot'
req('round',{'match':m['id']},b,404)
first=[];total=0
for i in range(7):
 r=req('round',{'match':m['id']},a);q=r['question'];first.append(q)
 assert r['round']==i and 'correctIndex' not in q
 again=req('round',{'match':m['id']},a)
 assert again['question']==q and again['remaining']<=r['remaining']
 right=q['answers'].index(BANK[q['id']]['answers'][0])
 if i==1:
  with sqlite3.connect(STATE) as db:db.execute('UPDATE matches SET started=? WHERE id=?',(time.time()-11,m['id']))
 result=req('answer',{'match':m['id'],'round':i,'answer':right,'elapsed':0},a)
 assert result['points']==(0 if i==1 else (40 if i==6 else 20)),result
 repeat=req('answer',{'match':m['id'],'round':i,'answer':-1},a)
 assert repeat==result
 total+=result['points']
p=req('profile',token=a);assert p['matches']==1 and p['xp']==total and p['correct']==6
req('round',{'match':m['id']},a,409)
ghost=req('match',{'topic':'22'},b,201);assert ghost['kind']=='human'
for i in range(7):
 r=req('round',{'match':ghost['id']},b);assert r['question']==first[i]
 req('answer',{'match':ghost['id'],'round':i,'answer':-1},b)
board=req('leaderboard&topic=22&period=week',token=a)['entries'];assert len(board)==2
assert req('leaderboard&topic=11&period=all',token=a)['entries']==[]
req('report',{'question':first[0]['id'],'reason':'Contract test report'},a)
req('delete-account',{},a);req('delete-account',{},b)
req('profile',token=a,status=401)
print('PASS: authentication, ownership, seven rounds, answer secrecy, timing, timeout, idempotence, human replay, stats, filtered leagues, reports and account deletion')
