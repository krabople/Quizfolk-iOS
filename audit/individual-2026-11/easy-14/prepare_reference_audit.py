"""Access metadata only; copyrighted reference extracts remain private."""
import json,pathlib
H=pathlib.Path(__file__).parent;W=H.parents[3]
cache=json.loads((W/'tv-references-private.json').read_text(encoding='utf8'))
d=json.loads((H/'draft.json').read_text(encoding='utf8'));refs=[]
for url in sorted({q['sourceURL'] for q in d}):
 v=cache.get(url)
 if v and len(v.get('text',''))>700:
  out={k:x for k,x in v.items() if k not in ['text','definitions']}
  out['inspectionMethod']='Relevant actual definition, synopsis, character/cast or production-credit passage inspected. Netflix partial-response status retained; received-byte hash is not a full-page hash.'
 elif 'wikipedia.org' in url:
  out={'url':url,'status':'encyclopaedic_passages_inspected_via_web','inspectionMethod':'Arconia/Manhattan premise and adult Mabel/Selena casting paragraphs inspected; secondary corroboration alongside official Hulu plot. Not a primary-publisher biography claim.'}
 else:
  out={'url':url,'status':'indexed_official_passage_inspected','inspectionMethod':'Applicable official broadcaster/producer/standards/education/cultural passage inspected through web output. Full direct page retrieval not claimed.'}
  if v:
   out['directAccess']={k:x for k,x in v.items() if k not in ['text','definitions']}
   if v.get('text'):out['directAccess']['status']='returned_error_stub_not_article_evidence'
 out['questionRows']=[i for i,q in enumerate(d,1) if q['sourceURL']==url]
 if out['questionRows']==[77]:out['scopeNote']='UK host only. Producer awards association and UK-format description corroborate Claudia Winkleman; misleading US slug on a separate indexed producer page is not used to assert she hosts US edition.'
 if out['questionRows']==[80]:out['scopeNote']='Official US-format guide verifies generic RoundTable voting mechanic; UK-specific host/cast not inferred from US guide.'
 if out['questionRows']==[35]:out['scopeNote']='Publisher caption/product description explicitly calls tracksuit green; no claim of visual inspection of a source photograph.'
 refs.append(out)
unused=[{k:x for k,x in v.items() if k not in ['text','definitions']} for u,v in cache.items() if u not in {q['sourceURL'] for q in d} and (v['status']=='fetch_failed' or len(v.get('text',''))<700)]
(H/'source-access.json').write_text(json.dumps({'date':'2026-11-18','note':'100 explicit author editorial judgments, not independent review. Source retrieval itself never grants approval. Dictionary senses, official publisher/producer descriptions, partial HTML, indexed passages, inaccessible stubs, and three encyclopaedic corroborations differentiated. No private source extracts republished.','references':refs,'unusedFailedOrStubAccess':unused},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(len(refs),'reference records')
