"""iOS/Android wire-contract interoperability, against disposable LOCAL state only."""
import json,os,pathlib,sqlite3,time,urllib.request,urllib.error,uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=os.environ.get('QUIZFOLK_TEST_URL','http://127.0.0.1:8773/index.php?r=')
assert BASE.startswith('http://127.0.0.1:'),'Cross-platform contracts must never run on production.'
STATE=pathlib.Path(os.environ['QUIZFOLK_STATE_DIR'])/'quizfolk.sqlite'
BANK={q['id']:q for q in json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))}

class Client:
    def __init__(self,platform):
        self.platform=platform;self.token=None
        self.token=self.request('register',{'name':'Cross-platform '+platform},201)['token']
        self.id=self.request('profile')['id']
    def request(self,route,body=None,status=200):
        headers={'Content-Type':'application/json','X-Quizfolk-Client':'3','User-Agent':'Quizfolk-'+self.platform+'/0.3.2'}
        if self.token:headers['Authorization']='Bearer '+self.token
        request=urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=headers)
        try:
            with urllib.request.urlopen(request,timeout=20) as response:code=response.status;reply=json.load(response)
        except urllib.error.HTTPError as e:code=e.code;reply=json.load(e)
        assert code==status,(self.platform,route,code,reply)
        return reply
    def question(self,mid):
        preview=self.request('round',{'match':mid});assert preview['phase']=='reading' and preview['question']['answers']==[]
        with sqlite3.connect(STATE) as db:db.execute('UPDATE matches SET preview_started=? WHERE id=?',(time.time()-4,mid))
        return self.request('reveal',{'match':mid})['question']
    def run_question(self,rid):
        preview=self.request('tournament-round',{'run':rid});assert preview['phase']=='reading' and preview['question']['answers']==[]
        with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_runs SET preview=? WHERE id=?',(time.time()-4,rid))
        return self.request('tournament-reveal',{'run':rid})['question']
def right(q):
    original=BANK[q['id']];return q['answers'].index(original['answers'][original['correctIndex']])

ios=Client('iOS');android=Client('Android')
try:
    for a,b in [(ios,android),(android,ios)]:
        a.request('social-settings',{'interests':['22','17']})
        a.request('follow',{'player':b.id,'enabled':True})
        assert any(p['id']==b.id for p in a.request('people&q=Cross-platform')['players'])
        assert a.request('daily-login',{})['awarded']==50
        assert a.request('daily-login',{})['awarded']==0
        assert a.request('player&id='+b.id)['following']
    # Android finishes before the iOS recipient accepts. Scores/XP wait for both.
    first=android.request('challenge',{'player':ios.id,'topic':'22','requestID':str(uuid.uuid4())},201)
    assert first['opponentID']==ios.id and first['duelID']
    packet=[]
    for turn in range(7):
        q=android.question(first['id']);packet.append(q)
        if turn==0:
            result=android.request('power',{'match':first['id'],'turn':turn,'type':'right','autoAnswer':True})['duelAnswer']
            assert result['selectedIndex']==right(q) and result['points']>0
        else:result=android.request('answer',{'match':first['id'],'round':turn,'answer':right(q)})
    assert result['finished'] and result['pending']
    assert android.request('profile')['xp']==0
    assert android.request('match-progress',{'match':first['id']})['opponentAnswered']==0
    second=ios.request('duel-open',{'duel':first['duelID']})
    assert second['opponentID']==android.id
    for turn in range(7):
        q=ios.question(second['id']);assert q==packet[turn], 'Both platforms must receive the same questions AND answer order.'
        result=ios.request('answer',{'match':second['id'],'round':turn,'answer':right(q) if turn==0 else (right(q)+1)%4})
    assert result['finished'] and not result['pending']
    assert android.request('profile')['wins']==1 and ios.request('profile')['wins']==0
    assert android.request('player&id='+ios.id)['headToHead']=={'games':1,'wins':1,'draws':0,'losses':0}
    assert ios.request('player&id='+android.id)['headToHead']=={'games':1,'wins':0,'draws':0,'losses':1}
    assert android.request('match-progress',{'match':first['id']})['opponentResults']==[True]+[False]*6
    assert ios.request('match-progress',{'match':second['id']})['opponentResults']==[True]*7
    for client in [ios,android]:assert {e['id'] for e in client.request('leaderboard&topic=22&period=all')['entries']}=={ios.id,android.id}
    rematch=ios.request('challenge',{'player':android.id,'topic':'22','requestID':str(uuid.uuid4())},201)
    assert android.request('duel-open',{'duel':rematch['duelID']})['opponentID']==ios.id
    # Both platforms enter the same public event; podium rewards are shared service state.
    event=min((e for e in ios.request('tournaments')['events'] if e['kind']=='daily' and not e['closed']),key=lambda e:e['coins'])
    assert any(e['id']==event['id'] for e in android.request('tournaments')['events'])
    for client in [android,ios]:
        run=client.request('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},201)
        q=client.run_question(run['id'])
        if client is android:
            r=client.request('tournament-power',{'run':run['id'],'turn':0,'type':'right','autoAnswer':True})['tournamentAnswer']
            assert r['correct'] and r['streak']==1
            q=client.run_question(run['id'])
        client.request('tournament-answer',{'run':run['id'],'turn':1 if client is android else 0,'answer':(right(q)+1)%4})
    standings=ios.request('tournament-board&event='+event['id'])['entries']
    assert [r['id'] for r in standings]==[android.id,ios.id]
    balances={client.id:client.request('coins')['wallet']['coins'] for client in [ios,android]}
    with sqlite3.connect(STATE) as db:db.execute('UPDATE tournament_events SET ends=? WHERE id=?',(int(time.time())-1,event['id']))
    for client,rank,coins in [(android,1,500),(ios,2,250)]:
        inbox=client.request('prizes');prize=next(p for p in inbox['pending'] if p['id']==event['id'])
        assert prize['rank']==rank and prize['coins']==coins
        assert inbox['wallet']['coins']==balances[client.id]+coins
    android.request('select-badge',{'event':event['id'],'acknowledge':True})
    assert ios.request('player&id='+android.id)['displayBadge']['id']==event['id']
    # A private room created on Android admits an iOS member with a different home topic.
    room=android.request('party-create',{'requestID':str(uuid.uuid4()),'name':'Cross-platform party','topic':'22','entryCoins':0,'cycles':1,'days':7,'powers':False},201)
    quote=ios.request('party-preview',{'code':room['code']});assert quote['entryCoins']==0
    ios.request('party-join',{'code':room['code'],'topic':'17','expectedEntryCoins':0})
    android.request('party-start',{'party':room['id']})
    a=android.request('party-board&id='+room['id']);b=ios.request('party-board&id='+room['id'])
    assert a['fixtures']==b['fixtures'] and sorted(f['topicID'] for f in a['fixtures'])==['17','22']
    fixture=a['fixtures'][0]
    am=android.request('party-play',{'party':room['id'],'fixture':fixture['id']});im=ios.request('party-play',{'party':room['id'],'fixture':fixture['id']})
    assert not am['powerAllowed'] and not im['powerAllowed']
    assert android.question(am['id'])==ios.question(im['id'])
finally:
    for client in [ios,android]:client.request('delete-account',{})
print('PASS: Android/iOS discovery, follows, delayed challenges, identical packets, atomic Right Answer, shared settlement/XP/head-to-head/leagues, rematches, public events/prizes/badges, private mixed-platform home/away tournaments and daily coin caps')
