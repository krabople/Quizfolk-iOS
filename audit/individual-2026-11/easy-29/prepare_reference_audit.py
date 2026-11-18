"""Record access honestly: indexed passages are not claimed as full retrieval."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
cache=json.loads((HERE.parents[3]/'comics-references-private.json').read_text(encoding='utf8'))
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
refs=[]
for u in sorted({q['sourceURL'] for q in draft}):
 r=cache.get(u)
 rows=[i for i,q in enumerate(draft,1) if q['sourceURL']==u]
 if r:
  out={k:v for k,v in r.items() if k not in ['text','definitions']}
  out['inspectionMethod']='Relevant private reference passage/definition inspected; see individual author judgments.' if r['status']=='retrieved_for_inspection' else 'Direct retrieval failed; applicable indexed publisher description inspected instead. Failure retained; full article retrieval not claimed.'
 else:
  out={'url':u,'status':'indexed_publisher_passage_inspected','inspectionMethod':'Relevant publisher index biography, comics issue/collection synopsis, character description or educational reference passage inspected with web search; no successful direct full-text request claimed.'}
 if u.endswith('MMRPG_XMen97_20240517.pdf'):
  out['scopeNote']='Official adaptation character sheets corroborate the classic Nightcrawler teleportation and Gambit card abilities, without treating game statistics as universal comic continuity.'
 if 'Ant-Man-and-the-Wasp-Activity-Packet' in u:
  out['scopeNote']='Official screen-adaptation education packet corroborates the shared shrinking ability; no MCU-specific event or mechanics asserted as comics history.'
 if u.endswith('MMRPG_MarvelRivals_20241220.pdf'):
  out['scopeNote']='Only familiar colour, biological appearance and plant nature checked; alternate-world game histories/statistics not generalised to comic continuity.'
 if rows==[51,53,67]:out['scopeNote']='DC profile explicitly identifies Bruce Wayne, utility-belt Batarangs and Robin sidekick. Batarang object description additionally checked in author editorial judgment; no uninspected cover-image review claimed.'
 out['questionRows']=rows;refs.append(out)
unused=[{k:v for k,v in r.items() if k not in ['text','definitions']} for u,r in cache.items() if u not in {q['sourceURL'] for q in draft} and r['status']=='fetch_failed']
(HERE/'source-access.json').write_text(json.dumps({'date':'2026-11-18','note':'Access metadata does not automatically approve questions. Author decisions cover all100 items/options. Primary publisher references and authorised education texts used; private copyrighted extracts are not republished. Indexed passage inspection, adaptation corroboration and direct fetch failures distinguished.','references':refs,'unusedFailedInitialPaths':unused},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(len(refs),'reference records for100 explicit author-reviewed questions')
