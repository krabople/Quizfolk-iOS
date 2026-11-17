"""Assemble completed fingerprint-matched editorial reviews, never unreviewed drafts."""
import collections,hashlib,json,pathlib,re,sqlite3,sys
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'audit'))
from validate_supplements import fingerprint,reviewed_batch

def read(path):return json.loads(path.read_text(encoding='utf8'))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')

names=sys.argv[1:]
assert names and len(names)==len(set(names))
bank=read(ROOT/'data/questions.json');catalog=read(ROOT/'audit/supplements.json')
for name in names:
 assert re.fullmatch(r'easy-\d+',name)
 directory=HERE/name;drafts=read(directory/'draft.json');review=read(directory/'final-review.json')
 assert review['status']=='complete' and review['remaining']==0 and review['reviewed']==100
 assert len(drafts)==len(review['decisions'])==100
 decisions={d['draftID']:d for d in review['decisions']};assert len(decisions)==100
 version='2026-11-'+name+'-v1';questions=[];ledger=[]
 for index,draft in enumerate(drafts):
  decision=decisions[draft['draftID']]
  assert decision['decision'] in ['keep','edited'] and decision['prompt']==draft['prompt']
  assert decision['reviewedSHA256']==hashlib.sha256(json.dumps(draft,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
  assert draft['categoryID']==name.split('-')[1] and draft['difficulty']=='easy'
  assert len(draft['answers'])==len(set(draft['answers']))==4 and draft['sourceURL'].startswith('https://')
  correct=draft['answers'][draft['correctIndex']];rotation=index%4
  answers=draft['answers'][rotation:]+draft['answers'][:rotation]
  qid=hashlib.sha256(('Quizfolk '+version+'\0'+draft['prompt']).encode()).hexdigest()[:20]
  q={'id':qid,'categoryID':draft['categoryID'],'difficulty':'easy','prompt':draft['prompt'],
     'answers':answers,'correctIndex':answers.index(correct),'source':'Quizfolk original; primary-source fact check',
     'sourceURL':draft['sourceURL'],'license':'CC BY-SA 4.0','reviewStatus':'individually_reviewed','auditVersion':version}
  questions.append(q)
  ledger.append({'id':qid,'questionSHA256':fingerprint(q),'action':'keep','meaning':decision['meaning'],
   'answer':decision['answer'],'grammar':decision['grammar'],'category':decision['category'],
   'reviewer':decision['reviewer'],'sources':[draft['sourceURL']],'authorRationale':draft['rationale'],
   'independentDraftID':draft['draftID'],'sourceRelevance':decision['sourceRelevance']})
 write(directory/'questions.json',questions)
 (directory/'decisions.jsonl').write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in ledger),encoding='utf8',newline='\n')
 write(directory/'completion.json',{'auditVersion':version,'date':'2026-11-17','input':100,'reviewed':100,
  'remaining':0,'errors':[],'complete':True,'publishedCount':100,
  'publishedSHA256':hashlib.sha256((directory/'questions.json').read_bytes()).hexdigest(),
  'method':'Individually authored and independently reviewed prompts, all four options, answer uniqueness, grammar, category and source relevance; recorded edits applied and final drafts fingerprint-matched.',
  'sources':sorted({q['sourceURL'] for q in questions})})
 assert reviewed_batch(directory)==questions
 bank=[q for q in bank if q.get('auditVersion')!=version]+questions
 entry='individual-2026-11/'+name
 if entry not in catalog:catalog.append(entry)
assert len(bank)==len({q['id'] for q in bank})==len({q['prompt'].casefold() for q in bank})
counts=collections.Counter(q['categoryID'] for q in bank)
categories=read(ROOT/'data/categories.json')
for c in categories:c['questionCount']=counts[c['id']]
(ROOT/'data/questions.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')),encoding='utf8',newline='\n')
write(ROOT/'data/categories.json',categories);write(ROOT/'audit/supplements.json',catalog)
with sqlite3.connect(ROOT/'data/question-bank.sqlite') as db:
 for name in names:
  questions=read(HERE/name/'questions.json')
  db.executemany('INSERT OR REPLACE INTO questions(id,category_id,difficulty,prompt,answers,correct_index,source,license,review_status,payload) VALUES(?,?,?,?,?,?,?,?,?,?)',[
   (q['id'],q['categoryID'],q['difficulty'],q['prompt'],json.dumps(q['answers'],ensure_ascii=False),q['correctIndex'],q['source'],q['license'],q['reviewStatus'],json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'))) for q in questions])
print(json.dumps({'assembledBatches':names,'totalQuestions':len(bank),'note':'Local reviewed bank only; hosting and app builds require separate publication.'}))
