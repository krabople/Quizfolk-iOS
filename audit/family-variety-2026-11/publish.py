"""Assemble the explicitly completed Family Trivia author reviews."""
import collections,datetime,hashlib,json,pathlib,re,sqlite3,sys
H=pathlib.Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(R/'audit'))
from validate_supplements import fingerprint,reviewed_batch
VERSION='2026-11-family-variety-v1'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
d=read(H/'draft.json');baseline=read(H/'baseline.json');assert len(d)==359
review={}
for p in sorted(H.glob('author-review-*.json')):
 v=read(p);assert v['independent'] is False and v['reviewed']==len(v['decisions'])
 for row in v['decisions']:
  assert row['draftID'] not in review;review[row['draftID']]=row
assert len(review)==359
bank=read(R/'data/questions.json');old={q['id']:q for q in bank if q['categoryID']=='37' and q.get('auditVersion')!=VERSION}
assert len(old)==baseline['originalCount']==359 and set(old)==set(baseline['originalQuestionIDs'])
assert {k:fingerprint(v) for k,v in old.items()}==baseline['originalFingerprints']
unrelated=[q for q in bank if q.get('auditVersion')!=VERSION];assert len(unrelated)==25017
assert len({q['prompt'].casefold() for q in d})==359
assert not ({q['prompt'].casefold() for q in d}&{q['prompt'].casefold() for q in unrelated})
questions=[];ledger=[];listing=['# Added Family Trivia questions','','Batch: `'+VERSION+'`. Exactly359 additions. Original359 category questions preserved.','', '| Question ID | Theme | Question | Correct answer |','|---|---|---|---|']
for i,q in enumerate(d):
 row=review[q['draftID']];assert row['decision']=='keep_after_author_review' and row['prompt']==q['prompt']
 assert q['reviewStatus']=='author_final_checked' and row['reviewedSHA256']==hashlib.sha256(json.dumps(q,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
 assert q['categoryID']=='37' and q['difficulty'] in ['easy','medium'] and len(q['answers'])==len(set(q['answers']))==4 and q['correctIndex']==0
 assert not re.search(r'harry potter|narnia|hogwarts|voldemort|pevensie|dumbledore|hermione|aslan',q['prompt']+' '+' '.join(q['answers']),re.I)
 rotation=i%4;answers=q['answers'][rotation:]+q['answers'][:rotation];correct=q['answers'][0]
 qid=hashlib.sha256(('Quizfolk '+VERSION+'\0'+q['prompt']).encode()).hexdigest()[:20]
 final={'id':qid,'categoryID':'37','difficulty':q['difficulty'],'prompt':q['prompt'],'answers':answers,'correctIndex':answers.index(correct),'source':'Quizfolk original; author fact-checked','sourceURL':q['sourceURL'],'license':'CC BY-SA 4.0','reviewStatus':'individually_reviewed','auditVersion':VERSION}
 questions.append(final)
 ledger.append({'id':qid,'questionSHA256':fingerprint(final),'action':'keep','meaning':row['meaning'],'answer':row['answer'],'grammar':row['grammar'],'category':row['category'],'reviewer':row['reviewer'],'sources':[q['sourceURL']],'authorRationale':q['authorConsideration'],'draftID':q['draftID'],'sourceRelevance':row['sourceRelevance'],'theme':q['theme']})
 esc=lambda s:s.replace('|','\\|').replace('\n',' ')
 listing.append('| '+' | '.join(map(esc,[qid,q['theme'],q['prompt'],correct]))+' |')
assert len({q['id'] for q in questions})==359 and not ({q['id'] for q in questions}&{q['id'] for q in unrelated})
write(H/'questions.json',questions)
(H/'decisions.jsonl').write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in ledger),encoding='utf8',newline='\n')
(H/'added-questions.md').write_text('\n'.join(listing)+'\n',encoding='utf8',newline='\n')
write(H/'added-question-ids.json',{'batchID':VERSION,'categoryID':'37','count':359,'questionIDs':[q['id'] for q in questions]})
write(H/'completion.json',{'auditVersion':VERSION,'date':datetime.date.today().isoformat(),'input':359,'reviewed':359,'remaining':0,'errors':[],'complete':True,'publishedCount':359,'publishedSHA256':hashlib.sha256((H/'questions.json').read_bytes()).hexdigest(),'independentReview':False,'method':'Individual author checks of each question, all four options, answer uniqueness, grammar, family suitability and fact/reference relevance. Final question fingerprints matched before assembly. Exact existing stems replaced; original Family Trivia set unchanged. Author review, not independent review.','themes':dict(collections.Counter(q['theme'] for q in d)),'difficulty':dict(collections.Counter(q['difficulty'] for q in d)),'correctOptionPositions':dict(collections.Counter(q['correctIndex'] for q in questions))})
assert reviewed_batch(H)==questions
bank=unrelated+questions;assert len(bank)==25376 and len({q['id'] for q in bank})==len(bank)==len({q['prompt'].casefold() for q in bank})
(R/'data/questions.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')),encoding='utf8',newline='\n')
counts=collections.Counter(q['categoryID'] for q in bank);assert counts['37']==718
categories=read(R/'data/categories.json')
for c in categories:c['questionCount']=counts[c['id']]
write(R/'data/categories.json',categories)
catalog=read(R/'audit/supplements.json');entry='family-variety-2026-11'
if entry not in catalog:catalog.append(entry)
write(R/'audit/supplements.json',catalog)
with sqlite3.connect(R/'data/question-bank.sqlite') as db:
 db.executemany('INSERT OR REPLACE INTO questions(id,category_id,difficulty,prompt,answers,correct_index,source,license,review_status,payload) VALUES(?,?,?,?,?,?,?,?,?,?)',[(q['id'],q['categoryID'],q['difficulty'],q['prompt'],json.dumps(q['answers'],ensure_ascii=False),q['correctIndex'],q['source'],q['license'],q['reviewStatus'],json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'))) for q in questions])
write(H/'progress.json',{'batchID':VERSION,'target':359,'drafted':359,'approved':359,'localBankIncluded':True,'deployed':0,'originalFamilyCount':359,'localFamilyCount':718,'localBankCount':25376})
print(json.dumps({'added':359,'familyBefore':359,'familyAfter':718,'bank':25376,'batch':VERSION,'originalQuestionsUnchanged':True,'live':False}))
