import pathlib,json,collections
p=pathlib.Path(__file__).resolve().parents[1]/'data'
q=json.loads((p/'questions.json').read_text(encoding='utf-8'))
c=json.loads((p/'categories.json').read_text(encoding='utf-8'))
report=json.loads((p/'audit-report.json').read_text(encoding='utf-8'))
assert len(q)==report['retained'] and len(q)>=20000
assert report['screened']==report['retained']+report['quarantined']
assert len({x['id'] for x in q})==len(q)
assert len({x['prompt'].casefold() for x in q})==len(q)
counts=collections.Counter(x['categoryID'] for x in q)
for x in q:
 assert len(x['answers'])==4 and len({a.casefold() for a in x['answers']})==4
 assert 0<=x['correctIndex']<4 and x['license']=='CC BY-SA 4.0'
 assert x['categoryID'] in {a['id'] for a in c}
for x in c: assert x['questionCount']==counts[x['id']] and counts[x['id']]>=7
print(f'Validated {len(q):,} questions across {len(c)} categories')

ledger=[json.loads(line) for line in (p.parent/'audit/question-ledger.jsonl').read_text(encoding='utf-8').splitlines()]
assert len(ledger)==report['screened']
active={x['id'] for x in q}
assert all((x['id'] in active)==(x['action']!='quarantined') for x in ledger)
f=next(x for x in q if x['id']=='66b6a0317332fa97167e')
assert f['categoryID']=='19' and 'factorial' in f['prompt'] and f['answers'][f['correctIndex']]=='720'
