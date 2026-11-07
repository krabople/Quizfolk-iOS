"""Exercise the actual authenticated API and public SSV URL in disposable state."""
import json, os, pathlib, secrets, sqlite3, subprocess, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = os.environ['QUIZFOLK_TEST_URL']
STATE = pathlib.Path(os.environ['QUIZFOLK_STATE_DIR'])
DB = STATE / 'quizfolk.sqlite'
CALLBACK = BASE.split('index.php?', 1)[0] + 'rewarded-callback.php'

def request(url, body=None, token=None, status=200):
    headers = {'Content-Type': 'application/json'}
    if token: headers['Authorization'] = 'Bearer ' + token
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            code, raw = response.status, response.read()
    except urllib.error.HTTPError as error:
        code, raw = error.code, error.read()
    value = json.loads(raw) if raw else None
    assert code == status, (url.split('?')[0], code, value)
    return value

def api(route, body=None, token=None, status=200):
    return request(BASE + route, body, token, status)

alice = api('register', {'name': 'Ad Alice'}, status=201)['token']
bob = api('register', {'name': 'Ad Bob'}, status=201)['token']
aid = api('profile', token=alice)['id']
bid = api('profile', token=bob)['id']
api('rewarded-status&platform=ios', status=401)
api('rewarded-start&platform=ios', token=alice, status=405)
disabled = api('rewarded-status&platform=ios', token=alice)
assert disabled['reason'] == 'disabled' and disabled['dailyLimit'] is None and disabled['remainingToday'] is None
assert disabled['reward'] == 5
assert disabled['wallet']['coins'] == 100
api('rewarded-start', {'platform': 'ios', 'requestKey': secrets.token_hex(16), 'reward': 999999}, alice, 409)
api('rewarded-status&platform=web', token=alice, status=400)

# The isolated server remains disabled for new ads. Seed a pending reservation
# exactly as a previously enabled server would have persisted it; it must still
# honour a cryptographically valid callback after ads have been switched off.
now = int(time.time())
attempt = secrets.token_hex(32)
unit = 'ca-app-pub-1111111111111111/1111111111'
with sqlite3.connect(DB) as db:
    db.execute('INSERT INTO rewarded_attempts(id,player_id,platform,ad_unit,request_key,created,expires,callback_deadline,day) VALUES(?,?,?,?,?,?,?,?,?)',
               (attempt, aid, 'ios', unit, secrets.token_hex(16), now, now + 600, now + 259800, now // 86400 * 86400))
pending = api('rewarded-status&platform=android', token=alice)
assert pending['attempt']['id'] == attempt and pending['attempt']['platform'] == 'ios'
api('rewarded-status&platform=ios&attempt=' + attempt, token=bob, status=404)
api('rewarded-cancel', {'platform': 'ios', 'attempt': attempt}, bob, 404)

params = {'ad_network': '5450213213286189855', 'ad_unit': unit, 'custom_data': attempt,
          'reward_amount': '5', 'reward_item': 'coins', 'timestamp': str(now * 1000), 'transaction_id': secrets.token_hex(16)}
signer = r'''
$p=json_decode(stream_get_contents(STDIN),true,16,JSON_THROW_ON_ERROR);
$key=openssl_pkey_new(['private_key_type'=>OPENSSL_KEYTYPE_EC,'curve_name'=>'prime256v1']);
if(!$key)throw new RuntimeException('Could not create isolated test key');
ksort($p);$raw=http_build_query($p,'','&',PHP_QUERY_RFC3986);
openssl_sign($raw,$signature,$key,OPENSSL_ALGO_SHA256);
echo json_encode(['query'=>$raw.'&signature='.rtrim(strtr(base64_encode($signature),'+/','-_'),'=').'&key_id=12345','pem'=>openssl_pkey_get_details($key)['key']],JSON_THROW_ON_ERROR);
'''
cmd = [os.environ.get('QUIZFOLK_PHP', 'php')]
if os.environ.get('QUIZFOLK_PHP_EXT'): cmd += ['-d', 'extension_dir=' + os.environ['QUIZFOLK_PHP_EXT'], '-d', 'extension=openssl']
signed = json.loads(subprocess.run(cmd + ['-r', signer], input=json.dumps(params), text=True, check=True, capture_output=True).stdout)
cache = {'fetched': now, 'json': json.dumps({'keys': [{'keyId': 12345, 'pem': signed['pem']}]})}
(STATE / 'rewarded-verifier-keys.json').write_text(json.dumps(cache), encoding='utf-8')
request(CALLBACK, {}, status=405)
request(CALLBACK + '?' + signed['query'].replace('reward_amount=5', 'reward_amount=10'), status=403)
first = request(CALLBACK + '?' + signed['query'])
second = request(CALLBACK + '?' + signed['query'])
assert first == {'ok': True, 'duplicate': False} and second == {'ok': True, 'duplicate': True}
earned = api('rewarded-status&platform=ios&attempt=' + attempt, token=alice)
assert earned['wallet']['coins'] == 105 and earned['attempt']['status'] == 'awarded' and earned['attempt']['awardedCoins'] == 5
assert api('coins', token=bob)['wallet']['coins'] == 100
api('rewarded-cancel', {'platform': 'ios', 'attempt': attempt}, alice)
assert api('coins', token=alice)['wallet']['coins'] == 105
api('delete-account', {}, alice)
assert request(CALLBACK + '?' + signed['query'])['duplicate'] is True
with sqlite3.connect(DB) as db:
    assert db.execute('SELECT COUNT(*) FROM rewarded_attempts WHERE player_id=?', (aid,)).fetchone()[0] == 0
    assert db.execute('SELECT COUNT(*) FROM tournament_wallet WHERE player_id=?', (aid,)).fetchone()[0] == 0
print('PASS: authenticated rewarded routes, disabled defaults, no client credit, cross-platform restore, account isolation, real signed callback HTTP, replay, deletion')
