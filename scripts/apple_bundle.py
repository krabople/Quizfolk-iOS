"""Use only the runner's existing App Store Connect key; never print credentials."""
import os,time,json,pathlib,urllib.request,urllib.error,jwt
key=pathlib.Path.home()/'.appstoreconnect/private_keys'/('AuthKey_'+os.environ['ASC_KEY_ID']+'.p8')
token=jwt.encode({'iss':os.environ['ASC_ISSUER_ID'],'iat':int(time.time()),'exp':int(time.time())+1100,'aud':'appstoreconnect-v1'},key.read_text(),algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'})
def call(path,body=None):
 req=urllib.request.Request('https://api.appstoreconnect.apple.com/v1/'+path,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'},data=None if body is None else json.dumps(body).encode())
 try:
  with urllib.request.urlopen(req) as response:return json.load(response)
 except urllib.error.HTTPError as exc:
  print(exc.read().decode());raise SystemExit('Apple API request failed: '+str(exc.code))
existing=call('bundleIds?filter[identifier]=com.quizfolk.ios')
if not existing['data']:
 call('bundleIds',{'data':{'type':'bundleIds','attributes':{'identifier':'com.quizfolk.ios','name':'Quizfolk','platform':'IOS'}}})
 print('Created Quizfolk bundle identifier')
else:print('Quizfolk bundle identifier already exists')
