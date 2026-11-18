"""Publish retrieval metadata only. The editor, not this script, approves facts."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
private=HERE.parents[3]/'film-references-private.json'
cache=json.loads(private.read_text(encoding='utf8'))
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
web={
 'https://lionking.com/familynight/':'Official Lion King character guide indexed passage explicitly identifies Zazu as hornbill; direct request403 retained.',
 'https://d23.com/a-to-z/pumbaa/':'D23 entry opened in web tool, explicit Pumbaa warthog description inspected; no direct-cache retrieval claimed.',
 'https://catalog.afi.com/Film/7892-THE-WIZARD-OF-OZ':'AFI web synopsis inspected at1880-1894: Toto, Yellow Brick Road/Emerald City and companions requests. Direct403 retained.',
 'https://catalog.afi.com/Film/58544-HOME-ALONE':'AFI web cast and synopsis inspected, including Christmas Paris trip at1303. Direct403 retained.',
 'https://catalog.afi.com/Film/55201-FORREST-GUMP':'AFI web synopsis2585-2587: ping-pong championship in China and US team. Direct403 retained.',
 'https://catalog.afi.com/Film/61230-THE-MATRIX':'AFI indexed synopsis explicitly pairs red pill with learning truth, blue with ordinary life. Supplemented by official Warner Bros red/blue scene reference; direct403 retained.',
 'https://www.paramountpictures.com/movies/titanic':'Paramount indexed film description explicitly pairs DiCaprio and Jack; direct403 retained.',
 'https://www.afi.com/afis-100-years-100-cheers/':'AFI indexed Rocky synopsis explicitly identifies Rocky Balboa as boxer; direct403 retained.',
 'https://www.007.com/':'Official James Bond007 brand identity inspected via web result; no readable article text returned. Used only for familiar agent number, not current casting or exclusivity.',
 'https://lib-filmcollection.trin.cam.ac.uk/spotlight/silent-film/':'Trinity Cambridge educational indexed description inspected: music-only soundtrack instead of dialogue, transition to synchronised spoken sound. Direct403 and web-open cache-miss retained; full article retrieval not claimed.',
 'https://www.starwars.com/databank/obi-wan-kenobi-biography-gallery':'Official indexed biography-gallery caption says Obi-Wan adopted Ben. Direct plain-text cache omits image captions; indexed caption inspection distinguished.',
}
refs=[]
for u in sorted({q['sourceURL'] for q in draft}):
 r=cache.get(u)
 if r is None:
  assert u in web,u
  out={'url':u,'status':'web_inspected_no_direct_cache'}
 else:out={k:v for k,v in r.items() if k not in ['text','definitions']}
 out['inspectionMethod']=web.get(u,'Relevant studio character/synopsis text, authorised character-reader extract or applicable film/photography dictionary sense inspected in private cache; see individual author decision.')
 out['questionRows']=[i for i,q in enumerate(draft,1) if q['sourceURL']==u]
 refs.append(out)
attempts=[{k:v for k,v in r.items() if k not in ['text','definitions']} for u,r in cache.items() if u not in {q['sourceURL'] for q in draft} and r['status']=='fetch_failed']
(HERE/'source-access.json').write_text(json.dumps({'date':'2026-11-18','note':'Retrieval is not editorial approval. Private copyrighted reference text is not republished. Indexed/caption inspection is distinguished from successful full-text retrieval. Individual decisions document corrections and option review.','references':refs,'unusedFailedRetrievalAttempts':attempts},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(len(refs),'reference metadata records for100 checked items')
