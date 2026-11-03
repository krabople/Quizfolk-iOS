"""Verify processing and attach this exact build to the existing Quizfolk group.

Runs only in the signing workflow with its existing Apple key. Never prints
credentials, creates testers/groups, or submits an App Store production release.
"""
import base64,json,os,pathlib,re,time,urllib.parse,urllib.request,urllib.error
import jwt

APP='6827336209'
GROUP='384b2cea-b7a2-459c-ac2b-ac148304f1fb'
BUILD=os.environ.get('QUIZFOLK_BUILD_NUMBER',os.environ['GITHUB_RUN_NUMBER'])
VERSION=re.search(r'MARKETING_VERSION:\s*([\d.]+)',pathlib.Path('project.yml').read_text()).group(1)
KEY=base64.b64decode(os.environ['ASC_API_KEY_BASE64'])

def api(path,body=None,method=None):
    now=int(time.time())
    token=jwt.encode({'iss':os.environ['ASC_ISSUER_ID'],'iat':now-20,'exp':now+900,'aud':'appstoreconnect-v1'},KEY,algorithm='ES256',headers={'kid':os.environ['ASC_KEY_ID'],'typ':'JWT'})
    request=urllib.request.Request('https://api.appstoreconnect.apple.com/v1/'+path,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'},data=None if body is None else json.dumps(body).encode(),method=method)
    try:
        with urllib.request.urlopen(request,timeout=45) as r:
            content=r.read();return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        try:details='; '.join(x.get('detail',x.get('title','Apple API error')) for x in json.load(e).get('errors',[]))
        except Exception:details='Apple API error'
        raise RuntimeError(f'Apple API {e.code}: {details}') from None

group=api('betaGroups/'+GROUP)['data']
assert api('betaGroups/'+GROUP+'/relationships/app')['data']['id']==APP,'The selected group belongs to another app'
internal=bool(group['attributes'].get('isInternalGroup'))
print(json.dumps({'app':APP,'group':GROUP,'groupName':group['attributes'].get('name'),'internalGroup':internal}),flush=True)
deadline=time.monotonic()+1500
candidate=None;last=None
while time.monotonic()<deadline:
    query=urllib.parse.urlencode({'filter[app]':APP,'filter[version]':BUILD,'include':'preReleaseVersion','limit':200})
    response=api('builds?'+query)
    versions={x['id']:x['attributes']['version'] for x in response.get('included',[]) if x['type']=='preReleaseVersions'}
    candidate=next((x for x in response['data'] if versions.get(x['relationships']['preReleaseVersion']['data']['id'])==VERSION),None)
    state=candidate['attributes']['processingState'] if candidate else 'AWAITING_APPLE_PROCESSING'
    if state!=last:print(json.dumps({'version':VERSION,'build':BUILD,'processingState':state}),flush=True);last=state
    if state in ['FAILED','INVALID']:raise SystemExit('Apple rejected build processing; previous testing builds remain available.')
    if state=='VALID':break
    time.sleep(20)
else:raise SystemExit('Build uploaded, but Apple processing has not finished. Retry only this verification job later.')

identifier=candidate['id']
def linked():return any(x['id']==identifier for x in api('betaGroups/'+GROUP+'/relationships/builds?limit=200')['data'])
if not linked():
    try:api('betaGroups/'+GROUP+'/relationships/builds',{'data':[{'type':'builds','id':identifier}]},'POST')
    except (RuntimeError,urllib.error.URLError):
        if not linked():raise
assert linked(),'Apple did not confirm the build/group association'

report={'appID':APP,'buildID':identifier,'version':VERSION,'build':BUILD,'groupID':GROUP,'groupName':group['attributes'].get('name'),'processingState':'VALID','groupAssigned':True,'testing':False}
for _ in range(18):
    detail=api('builds/'+identifier+'/buildBetaDetail')['data']['attributes']
    report.update(internalBuildState=detail.get('internalBuildState'),externalBuildState=detail.get('externalBuildState'))
    report['testing']=detail.get('internalBuildState' if internal else 'externalBuildState')=='IN_BETA_TESTING'
    if report['testing']:break
    time.sleep(10)
pathlib.Path('testflight-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2),flush=True)
if not report['testing']:raise SystemExit('Build processed and assigned. Apple has not yet placed the selected group in Testing; inspect the reported state.')
