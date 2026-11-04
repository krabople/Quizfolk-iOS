"""Verify the signed Android artifacts contain the exact reviewed bank, without debug service fixtures."""
import hashlib,json,os,pathlib,re,subprocess,zipfile
root=pathlib.Path(__file__).resolve().parents[1]
out=root/'android/app/build/outputs'
apk=out/'apk/release/app-release.apk';aab=out/'bundle/release/app-release.aab'
expected=(root/'data/questions.json').read_bytes()
with zipfile.ZipFile(apk) as package:
    bank=package.read('assets/questions.json');topics=json.loads(package.read('assets/categories.json'))
    assert bank==expected
    questions=json.loads(bank)
    assert len(questions)==21667 and len(topics)==30 and min(t['questionCount'] for t in topics)>=150
    assert all(b'emulator-only-token' not in package.read(f) for f in package.namelist() if re.fullmatch(r'classes\d*\.dex',f))
    assert not any(f.endswith(('.p12','.jks','.keystore')) for f in package.namelist())
with zipfile.ZipFile(aab) as bundle:assert bundle.read('base/assets/questions.json')==expected
badging=(out/'package.txt').read_text()
assert "package: name='com.quizfolk.android'" in badging and "sdkVersion:'26'" in badging and "targetSdkVersion:'36'" in badging
signature=(out/'signature.txt').read_text();assert 'certificate SHA-256 digest:' in signature
version=re.search(r"versionName='([^']+)'",badging).group(1)
code=re.search(r"versionCode='([^']+)'",badging).group(1)
report={'platform':'Android','applicationID':'com.quizfolk.android','version':version,'versionCode':int(code),'minimumAPI':26,'targetAPI':36,
    'questions':len(questions),'categories':len(topics),'mixedCategory':True,'minimumQuestionsPerTopic':min(t['questionCount'] for t in topics),
    'bankSHA256':hashlib.sha256(bank).hexdigest(),'apkSHA256':hashlib.sha256(apk.read_bytes()).hexdigest(),'aabSHA256':hashlib.sha256(aab.read_bytes()).hexdigest(),
    'sourceCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'signed':True,'debugFixturesExcluded':True,
    'signingCertificateSHA256':re.search(r'certificate SHA-256 digest: (\w+)',signature).group(1),'workflowRun':os.environ.get('GITHUB_RUN_ID')}
(out/'android-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
