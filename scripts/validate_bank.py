import pathlib,json,collections,hashlib,sys,base64,struct
p=pathlib.Path(__file__).resolve().parents[1]/'data'
q=json.loads((p/'questions.json').read_text(encoding='utf-8'))
c=json.loads((p/'categories.json').read_text(encoding='utf-8'))
completion=p.parent/'audit/individual-2026-10/completion.json'
assert len(q)>=20000
if completion.exists():
 report=json.loads(completion.read_text(encoding='utf-8'))
 assert report['complete'] and report['remaining']==0 and not report['errors']
 sys.path.insert(0,str(p.parent/'audit'))
 from individual_review import decisions,read
 from validate_supplements import reviewed_supplements
 frozen=read(p.parent/'audit/individual-2026-10/input.json')
 reviewed,errors=decisions(frozen)
 assert not errors and len(reviewed)==len(frozen)==report['reviewed']==report['input']
 expected={}
 for original in frozen:
  decision=reviewed[original['id']]
  if decision['action']=='reject':continue
  final=dict(decision.get('replacement',original))
  final['reviewStatus']='individually_reviewed'
  final['auditVersion']='2026-10-individual-v1'
  expected[final['id']]=final
 # Preserve the completed October audit; later additions have their own frozen
 # questions, fingerprints and individual editorial decisions.
 baseline=list(expected.values())
 assert report['publishedCount']==len(baseline)
 assert report['publishedSHA256']==hashlib.sha256(json.dumps(baseline,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
 for added in reviewed_supplements(p.parent):
  assert added['id'] not in expected
  expected[added['id']]=added
 assert {x['id']:x for x in q}==expected
 minimum=150
else:
 report=json.loads((p/'audit-report.json').read_text(encoding='utf-8'))
 assert len(q)==report['retained']
 assert report['screened']==report['retained']+report['quarantined']
 ledger=[json.loads(line) for line in (p.parent/'audit/question-ledger.jsonl').read_text(encoding='utf-8').splitlines()]
 assert len(ledger)==report['screened']
 active={x['id'] for x in q}
 assert all((x['id'] in active)==(x['action']!='quarantined') for x in ledger)
 minimum=7
assert len({x['id'] for x in q})==len(q)
assert len({(x['prompt'].casefold(),x.get('imageSHA256')) for x in q})==len(q)
counts=collections.Counter(x['categoryID'] for x in q)
for x in q:
 assert len(x['answers'])==4 and len({a.casefold() for a in x['answers']})==4
 assert 0<=x['correctIndex']<4 and x['license']=='CC BY-SA 4.0'
 assert x['categoryID'] in {a['id'] for a in c}
 if 'imagePng' in x:
  raw=base64.b64decode(x['imagePng'],validate=True)
  assert len(raw)<=65536 and raw[:8]==b'\x89PNG\r\n\x1a\n'
  assert all(1<=n<=512 for n in struct.unpack('>II',raw[16:24]))
  assert hashlib.sha256(raw).hexdigest()==x['imageSHA256']
for x in c: assert x['questionCount']==counts[x['id']] and counts[x['id']]>=minimum
# The server's SQLite copy must be the same reviewed bank as the mobile assets.
import sqlite3
with sqlite3.connect(p/'question-bank.sqlite') as db:
 rows=db.execute('SELECT id,category_id,payload FROM questions').fetchall()
 assert len(rows)==len(q)
 assert {qid:json.loads(payload) for qid,category,payload in rows}=={x['id']:x for x in q}
 assert all(json.loads(payload)['categoryID']==category for qid,category,payload in rows)
print(f'Validated {len(q):,} questions across {len(c)} categories')

f=next(x for x in q if x['id']=='66b6a0317332fa97167e')
assert f['categoryID']=='19' and 'factorial' in f['prompt'] and f['answers'][f['correctIndex']]=='720'
