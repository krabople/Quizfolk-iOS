"""Notification choices, durable events and delivery policies, against local disposable state only."""
import json,os,pathlib,sqlite3,subprocess,time,urllib.request,urllib.error,uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=os.environ['QUIZFOLK_TEST_URL'];assert BASE.startswith('http://127.0.0.1:')
STATE=pathlib.Path(os.environ['QUIZFOLK_STATE_DIR'])/'quizfolk.sqlite'
def request(route,body=None,token=None,status=200):
    headers={'Content-Type':'application/json','X-Quizfolk-Client':'3'}
    if token:headers['Authorization']='Bearer '+token
    req=urllib.request.Request(BASE+route,data=None if body is None else json.dumps(body).encode(),headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=20) as r:code=r.status;reply=json.load(r)
    except urllib.error.HTTPError as e:code=e.code;reply=json.load(e)
    assert code==status,(route,code,reply);return reply
class Client:
    def __init__(self,name):
        self.token=request('register',{'name':name},status=201)['token'];self.id=self.get('profile')['id'];self.install=str(uuid.uuid4())
    def get(self,route,body=None,status=200):return request(route,body,self.token,status)
    def preferences(self,**values):return self.get('notification-preferences',{'preferences':values})
    def device(self,platform='ios',enabled=True):
        return self.get('notification-device',{'installation':self.install,'platform':platform,'enabled':enabled,'token':('ab'*32 if platform=='ios' else 'Android-token:'+self.id+'x'*32)})
    def challenge(self,other,topic='22',key=None):return self.get('challenge',{'player':other.id,'topic':topic,'requestID':key or str(uuid.uuid4())},201)
def rows(query,*args):
    with sqlite3.connect(STATE) as db:db.row_factory=sqlite3.Row;return [dict(r) for r in db.execute(query,args)]
def change(query,*args):
    with sqlite3.connect(STATE) as db:db.execute(query,args)
def drain(mode='success'):
    args=[os.environ.get('QUIZFOLK_PHP','php')]
    if os.environ.get('QUIZFOLK_PHP_EXT'):args+=['-d','extension_dir='+os.environ['QUIZFOLK_PHP_EXT'],'-d','extension=pdo_sqlite']
    out=subprocess.check_output(args+[str(ROOT/'scripts/test_push_delivery.php')],cwd=ROOT,env=dict(os.environ,PUSH_TEST_MODE=mode),text=True)
    return json.loads(out)
a=Client('Notification Android');b=Client('Notification iPhone')
try:
    initial=b.get('notification-settings');assert not initial['preferences']['enabled'] and not any(initial['delivery'].values())
    request('notification-settings',status=401)
    b.get('notification-preferences',{'preferences':{'enabled':1}},400)
    b.get('notification-preferences',{'preferences':{'marketing':True}},400)
    b.device(enabled=False);b.get('notification-device',{'installation':b.install,'platform':'ios','enabled':True,'token':'ab'*32},409)
    a.challenge(b);assert not rows('SELECT * FROM push_jobs')
    a.preferences(enabled=True);b.preferences(enabled=True);a.device('android');b.device()
    b.get('notification-device',{'installation':b.install,'platform':'ios','enabled':True,'token':'wrong'},400)
    key=str(uuid.uuid4());duel=a.challenge(b,'17',key);a.challenge(b,'17',key)
    jobs=rows('SELECT * FROM push_jobs');assert len(jobs)==1 and jobs[0]['kind']=='challenges'
    payload=json.loads(jobs[0]['payload']);assert payload['id']==duel['duelID'] and payload['topicID']=='17'
    assert set(payload)=={'kind','id','topicID','notificationID'}
    assert drain('retry')['retry']==1
    job=rows('SELECT * FROM push_jobs')[0];assert job['attempts']==1 and job['due']>=time.time()+115 and job['status']=='pending'
    b.preferences(challenges=False);assert rows('SELECT status FROM push_jobs')[0]['status']=='cancelled'
    assert drain()['sent']==0
    b.preferences(challenges=True)
    accepted=b.get('duel-open',{'duel':duel['duelID']})
    # Complete the local packet deterministically to exercise settlement notification hooks.
    answers=json.dumps([{'selected':0,'elapsed':1,'correct':True,'points':19}]*6)
    b.preferences(duelResults=False)
    for client,mid,score in [(a,duel['id'],114),(b,accepted['id'],60)]:
        change('UPDATE matches SET answers=?,score=? WHERE id=?',answers,score,mid)
        client.get('round',{'match':mid});change('UPDATE matches SET preview_started=? WHERE id=?',time.time()-4,mid)
        client.get('reveal',{'match':mid})
        packet=json.loads(rows('SELECT packet FROM matches WHERE id=?',mid)[0]['packet'])
        client.get('answer',{'match':mid,'round':6,'answer':packet[6]['correctIndex']})
    results=rows('SELECT * FROM push_jobs WHERE kind="duelResults"');assert len(results)==1 and results[0]['player_id']==a.id
    assert drain()['sent']==1;assert drain()['sent']==0
    queued=a.challenge(b,'9');assert len(rows('SELECT * FROM push_jobs WHERE status="pending"'))==1
    b.get('block',{'player':a.id,'enabled':True});assert drain()['cancelled']==1
    b.get('block',{'player':a.id,'enabled':False})
    room=a.get('party-create',{'requestID':str(uuid.uuid4()),'name':'Notification friends','topic':'22','entryCoins':0,'cycles':1,'days':7,'powers':True},201)
    b.get('party-join',{'code':room['code'],'topic':'17','expectedEntryCoins':0});a.get('party-start',{'party':room['id']})
    assert len(rows('SELECT * FROM push_jobs WHERE kind="friendsTournaments" AND status="pending"'))==1
    assert drain()['sent']==1
    change('UPDATE tournament_events SET ends=? WHERE id=?',int(time.time())-1,room['id']);a.get('prizes')
    assert len(rows('SELECT * FROM push_jobs WHERE kind="friendsTournaments" AND status="pending"'))==2
    assert drain()['sent']==2
    # Real public prize settlement: neither provisional leads nor repeat inbox reads send twice.
    event=next(e for e in a.get('tournaments')['events'] if not e['closed'] and e['kind']=='daily' and e['coins']==25)
    run=a.get('tournament-enter',{'event':event['id'],'requestID':str(uuid.uuid4())},201)
    change('UPDATE tournament_runs SET score=40,streak=2,state="wrong" WHERE id=?',run['id'])
    assert not rows('SELECT * FROM push_jobs WHERE kind="tournamentPrizes"')
    change('UPDATE tournament_events SET ends=? WHERE id=?',int(time.time())-1,event['id']);a.get('prizes');a.get('prizes')
    prize=rows('SELECT * FROM push_jobs WHERE kind="tournamentPrizes"');assert len(prize)==1 and '150 coins' in prize[0]['body']
    assert drain('invalid')['failed']==1
    assert rows('SELECT enabled FROM push_devices WHERE player_id=?',a.id)[0]['enabled']==0
    a.device('android');b.preferences(enabled=False)
    assert not b.get('notification-settings')['preferences']['enabled']
    assert rows('SELECT enabled FROM push_devices WHERE player_id=?',b.id)[0]['enabled']==0
    # Account deletion cascades preferences, device tokens and queued/sent jobs.
finally:
    for client in [a,b]:client.get('delete-account',{})
assert not rows('SELECT * FROM push_devices') and not rows('SELECT * FROM push_settings') and not rows('SELECT * FROM push_jobs')
print('PASS: push opt-in, individual categories, auth, token validation/rotation, idempotent challenge and result events, private updates, final prizes only, retry/backoff, blocks, invalid tokens, opt-out and deletion')
