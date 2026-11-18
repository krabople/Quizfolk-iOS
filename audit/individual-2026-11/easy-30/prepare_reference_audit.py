"""Publish access metadata only; retain copyrighted extracts privately."""
import json,pathlib
H=pathlib.Path(__file__).parent;W=H.parents[3]
d=json.loads((H/'draft.json').read_text(encoding='utf8'))
cache={}
for name in ['gadgets-definitions-private.json','gadgets-extra-private.json','gadgets-extra2-private.json']:
 for v in json.loads((W/name).read_text(encoding='utf8')).values():cache[v['url']]=v
refs=[]
for url in sorted({q['sourceURL'] for q in d}):
 v=cache.get(url)
 if v and v.get('definitions'):
  out={k:x for k,x in v.items() if k!='definitions'}
  out['inspectionMethod']='Relevant lexical sense inspected, excluding unrelated definitions; individual judgments identify scope.'
 else:
  out={'url':url,'status':'indexed_official_reference_passage_inspected','inspectionMethod':'Specific official support, manufacturer, standards or metrology passage inspected via web search. Full-page direct retrieval not claimed. Individual final judgments describe applicable fact and limits.'}
 out['questionRows']=[i for i,q in enumerate(d,1) if q['sourceURL']==url];refs.append(out)
failed=[{k:x for k,x in v.items() if k!='definitions'} for v in cache.values() if not v.get('definitions')]
(H/'source-access.json').write_text(json.dumps({'date':'2026-11-18','note':'Metadata is not editorial approval. All100 questions/options have separate explicit author judgments, not independent review. Dictionary text and indexed extracts retained privately, not republished. Initial failed/empty guesses preserved below.','references':refs,'initialUnsuccessfulDefinitionLookups':failed},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(len(refs),'specific reference records')
