"""Use only the runner's existing App Store Connect key; never print credentials."""
import os,time,json,pathlib,urllib.request,urllib.error,jwt,base64
from cryptography.hazmat.primitives.serialization import pkcs12,Encoding
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
 bundle=call('bundleIds',{'data':{'type':'bundleIds','attributes':{'identifier':'com.quizfolk.ios','name':'Quizfolk','platform':'IOS'}}})['data']
 print('Created Quizfolk bundle identifier')
else:bundle=existing['data'][0];print('Quizfolk bundle identifier already exists')
# Reuse the installed distribution certificate; never create or revoke certificates.
_,cert,_=pkcs12.load_key_and_certificates(base64.b64decode(os.environ['BUILD_CERTIFICATE_BASE64']),os.environ['P12_PASSWORD'].encode())
der=cert.public_bytes(Encoding.DER)
certificates=call('certificates?limit=200')['data']
match=next((c for c in certificates if base64.b64decode(c['attributes']['certificateContent'])==der),None)
if not match:raise SystemExit('The existing signing certificate is not registered with this Apple team')
profiles=call('profiles?filter[profileType]=IOS_APP_STORE&include=bundleId,certificates&limit=200')['data']
profile=next((p for p in profiles if p['attributes']['profileState']=='ACTIVE' and p['relationships']['bundleId']['data']['id']==bundle['id'] and any(c['id']==match['id'] for c in p['relationships']['certificates']['data'])),None)
if profile is None:
 profile=call('profiles',{'data':{'type':'profiles','attributes':{'name':'Quizfolk App Store','profileType':'IOS_APP_STORE'},'relationships':{'bundleId':{'data':{'type':'bundleIds','id':bundle['id']}},'certificates':{'data':[{'type':'certificates','id':match['id']}]}}}})['data']
dest=pathlib.Path.home()/'Library/MobileDevice/Provisioning Profiles';dest.mkdir(parents=True,exist_ok=True)
(dest/(profile['attributes']['uuid']+'.mobileprovision')).write_bytes(base64.b64decode(profile['attributes']['profileContent']))
with open(os.environ['GITHUB_ENV'],'a') as env:env.write('QUIZFOLK_PROFILE_NAME='+profile['attributes']['name']+'\n')
print('Installed dedicated Quizfolk App Store profile using existing certificate')
