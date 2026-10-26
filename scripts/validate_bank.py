import pathlib,json,collections
p=pathlib.Path(__file__).resolve().parents[1]/'data'
q=json.loads((p/'questions.json').read_text(encoding='utf-8'))
c=json.loads((p/'categories.json').read_text(encoding='utf-8'))
assert len(q)>=45000
assert len({x['id'] for x in q})==len(q)
assert len({x['prompt'].casefold() for x in q})==len(q)
counts=collections.Counter(x['categoryID'] for x in q)
for x in q:
 assert len(x['answers'])==4 and len({a.casefold() for a in x['answers']})==4
 assert 0<=x['correctIndex']<4 and x['license']=='CC BY-SA 4.0'
 assert x['categoryID'] in {a['id'] for a in c}
for x in c: assert x['questionCount']==counts[x['id']] and counts[x['id']]>=7
print(f'Validated {len(q):,} questions across {len(c)} categories')
