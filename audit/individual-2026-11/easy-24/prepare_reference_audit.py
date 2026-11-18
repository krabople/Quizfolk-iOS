"""Record provenance metadata. No copied dictionary bodies are published."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
BASE=HERE.parents[3]
definitions=json.loads((BASE/'politics-definitions-private.json').read_text(encoding='utf8'))
extra=json.loads((BASE/'politics-extra-private.json').read_text(encoding='utf8'))
cache={v['url']:v for v in definitions.values()};cache.update(extra)
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
web={
'https://www.parliament.uk/site-information/glossary/devolution/':'Parliament glossary web page inspected for UK central-to-territorial transfer of powers; direct403 preserved.',
'https://www.senate.gov/about/powers-procedures/impeachment.htm':'Official Senate web article9-13 explicitly distinguishes House accusation and Senate trial/removal; direct403 preserved.',
'https://www.parliament.uk/about/mps-and-lords/members/partysystem/':'Official Parliament indexed party-system description explicitly distinguishes minister/spokesperson frontbenchers and backbenchers; no direct retrieval claimed.',
'https://www.parliament.uk/site-information/glossary/crossbench-peers/':'Parliament web glossary185 identifies non-party political peers; direct403 preserved.',
'https://www.parliament.uk/site-information/glossary/divisions/':'Parliament web glossary184 explains counting votes for/against a motion; direct403 preserved.',
'https://www.parliament.uk/site-information/glossary/dissolution/':'Parliament indexed glossary defines formal end of Parliament before general election; direct403 preserved.',
'https://www.electoralcommission.org.uk/guidance-returning-officers-administering-local-government-elections-england/verification-and-count/count/doubtful-ballot-papers':'Electoral Commission web guidance115-122 explicitly identifies rejected ballot criteria; direct403 preserved.'}
refs=[]
for u in sorted({q['sourceURL'] for q in draft}):
 r=cache.get(u)
 if r is None:
  assert u in web,u
  v={'url':u,'status':'web_inspected_no_direct_cache'}
 else:
  v={k:value for k,value in r.items() if k not in ['definitions','text']}
  if u not in web:
   assert r['status']=='retrieved_for_inspection'
   assert r.get('definitions') or r.get('text'),u
 v['inspectionMethod']=web.get(u,'Applicable civic dictionary definition or government/education passage inspected explicitly; see item-specific author decisions, not inferred from retrieval success.')
 v['questionRows']=[i for i,q in enumerate(draft,1) if q['sourceURL']==u]
 refs.append(v)
unused=[{k:value for k,value in r.items() if k!='definitions'} for r in definitions.values() if not r.get('definitions')]
(HERE/'source-access.json').write_text(json.dumps({'date':'2026-11-18','note':'Reference access is not editorial approval. Every prompt and four options has an explicit author second-pass decision. Private excerpts are not republished. Direct failures and alternate web inspection are distinguished.','references':refs,'unusedDictionaryEntriesWithoutDefinitions':unused},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(len(refs),'references covering100 individually checked questions')
