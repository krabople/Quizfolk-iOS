"""Coin and prize contracts against an isolated local database, never production."""
import json,os,pathlib,sqlite3,time,urllib.request,urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=os.environ.get('QUIZFOLK_TEST_URL','http://127.0.0.1:8770/index.php?r=')
STATE=pathlib.Path(os.environ.get('QUIZFOLK_STATE_DIR',ROOT/'backend/private'))/'quizfolk.sqlite'
BANK={q['id']:q for q in json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))}
def req(route,body=None,token=None,status=200):
    headers={'Content-Type':'application/json','X-Quizfolk-Client':'2'}
    if token:headers['Authorization']='Bearer '+token
    request=urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=headers)
    try:
        with urllib.request.urlopen(request,timeout=20) as response:code=response.status;data=json.load(response)
    except urllib.error.HTTPError as e:code=e.code;data=json.load(e)
    assert code==status,(route,code,data)
    return data
# Each suite has its own players; previous contracts deliberately exercise the
# shared registration limit. Reset only that limit in this isolated test state.
with sqlite3.connect(STATE) as db:db.execute("DELETE FROM limits WHERE bucket LIKE 'register:%'")
a=req('register',{'name':'Coin Alice'},status=201)['token']
b=req('register',{'name':'Coin Bob'},status=201)['token']
aid=req('profile',token=a)['id'];bid=req('profile',token=b)['id']
req('coins',status=401)
initial=req('coins',token=a)
assert initial['wallet']['coins']==100 and initial['topics']==[]
assert req('coins',{'coins':999999,'completedDays':5},a)==initial
assert req('prizes',token=a)=={'pending':[],'earned':[],'selected':None}
for topic in ['18','19','20','21']:
    match=req('match',{'topic':topic},a,201)['id']
    for i in range(7):
        question=req('round',{'match':match},a)['question']
        stored=BANK[question['id']]
        right=question['answers'].index(stored['answers'][stored['correctIndex']])
        body={'match':match,'round':i,'answer':right if i<4 else -1}
        result=req('answer',body,a)
        assert req('answer',body,a)==result
    progress=req('coins',token=a)
    expected={'18':110,'19':120,'20':145,'21':145}[topic]
    assert progress['wallet']['coins']==expected,progress
assert progress['topics']==['18','19','20'] and progress['earnedToday']==45
assert req('coins',token=b)['wallet']['coins']==100
# Persisted results represent a tournament that closed while the winner was
# offline. Reading the inbox must not acknowledge it or credit it a second time.
with sqlite3.connect(STATE) as db:
    for index,rank in enumerate([1,2,3]):
        event='prize-test-'+str(index)
        db.execute('INSERT INTO tournament_events VALUES(?,?,?,?,?,?,?,?)',(event,'22','daily',1,int(time.time())-index-1,25,0,1))
        db.execute('INSERT INTO tournament_places VALUES(?,?,?,?,?,?)',(event,aid,rank,100-index,5,30-index))
inbox=req('prizes',token=a)
assert len(inbox['pending'])==3 and len(inbox['earned'])==3
assert req('prizes',token=a)==inbox
assert req('coins',token=a)['wallet']['coins']==145
assert inbox['selected']['rank']==1
assert req('player',token=a)['displayBadge']==inbox['selected']
req('prize-seen',{'event':'prize-test-0'},b,403)
req('select-badge',{'event':'prize-test-0'},b,403)
req('select-badge',{'event':123},a,400)
req('prize-seen',{},a,400)
req('select-badge',{'event':'prize-test-2'},a)
assert req('player&id='+aid,token=b)['displayBadge']['rank']==3
assert len(req('prizes',token=a)['pending'])==3  # wearing is not acknowledgement
req('prize-seen',{'event':'prize-test-0'},a)
req('prize-seen',{'event':'prize-test-0'},a)
assert len(req('prizes',token=a)['pending'])==2
assert len(req('prizes',token=a)['earned'])==3
req('select-badge',{'event':None},a)
assert req('player',token=a)['displayBadge'] is None
req('delete-account',{},a);req('delete-account',{},b)
with sqlite3.connect(STATE) as db:
    for table in ['coin_trail_stamps','coin_trail_days','tournament_prize_receipts','player_display_badge']:
        assert db.execute('SELECT COUNT(*) FROM '+table+' WHERE player_id=?',(aid,)).fetchone()[0]==0
print('PASS: automatic capped coin earnings, no client minting, all podium prizes persist until acknowledged, badge ownership/sharing/selection, idempotent receipts and deletion')
