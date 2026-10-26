"""Append structurally valid CC BY-SA OpenTriviaQA records; never invent answers."""
import argparse,pathlib,json,re,html,hashlib,collections,sqlite3
p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);args=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1];data=root/'data'
bank=json.loads((data/'questions.json').read_text(encoding='utf-8'))
cats=json.loads((data/'categories.json').read_text(encoding='utf-8'))
extra=[('33','Brain Teasers','puzzlepiece.fill','7F76B4','🧩'),('34','Hobbies','scissors','6FA28C','🧶'),('35','Language & Culture','text.bubble.fill','B46B8D','💬'),('36','World Religions','sun.max.fill','AA8C57','🕊️'),('37','Family Trivia','figure.2.and.child.holdinghands','D18B64','🪁'),('38','Food & Drink','fork.knife','C77959','🍋')]
for i,name,symbol,color,emoji in extra:
 if not any(c['id']==i for c in cats):cats.append(dict(id=i,name=name,symbol=symbol,color=color,emoji=emoji,questionCount=0))
mapping={'animals':'27','brain-teasers':'33','celebrities':'26','entertainment':'9','for-kids':'37','general':'9','geography':'22','history':'23','hobbies':'34','humanities':'35','literature':'10','movies':'11','music':'12','newest':'9','people':'26','rated':'9','religion-faith':'36','science-technology':'17','sports':'21','television':'14','video-games':'15','world':'9'}
def category(origin,text):
 s=text.lower()
 if origin in ('music','movies','entertainment','television') and re.search(r'\bbroadway\b|\bmusicals?\b|\bwest end\b|\bles mis[eé]rables\b|\bphantom of the opera\b',s):return '13'
 if origin in ('television','movies','entertainment','video-games'):
  if re.search(r'\banime\b|\bmanga\b|\bnaruto\b|\bsailor moon\b|\bdragon ball\b|\bgundam\b|\bghibli\b',s):return '31'
  if re.search(r'\bcartoon\b|\banimated\b|\bsimpsons\b|\bspongebob\b|\blooney tunes\b|\bscooby\b|\bdisney\b',s):return '32'
 if origin in ('hobbies','general','rated','newest','world','for-kids'):
  if re.search(r'\bchess\b|\bmonopoly\b|\bboard game\b|\bscrabble\b|\bbackgammon\b|\bcheckers\b|\bcluedo\b|\bcatan\b',s):return '16'
  if re.search(r'\bcook(?:ing|ed)?\b|\bcuisine\b|\bfood\b|\bcheese\b|\brecipe\b|\bculinary\b|\bchocolate\b|\bbeer\b|\bwine\b|\bcocktail\b|\bfruit\b|\bvegetable\b|\bpasta\b|\bcake\b|\bcoffee\b',s):return '38'
 if origin in ('science-technology','general','rated','newest','brain-teasers','for-kids'):
  if re.search(r'\balgebra\b|\bequation\b|\bmathematic|\bprime number\b|\bsquare root\b|\bfraction\b|\btriangle\b|\bpolygons?\b|\bgeometry\b|\bdecimal\b|\bmultiplied\b|\bdivided by\b',s):return '19'
  if re.search(r'\bcomputer\b|\bsoftware\b|\bprogramming\b|\bcpu\b|\boperating system\b|\binternet\b|\bhtml\b|\bmicrosoft\b|\blinux\b',s):return '18'
  if re.search(r'\btelephone\b|\bmobile phone\b|\biphone\b|\bcamera\b|\btelevision set\b|\btransistor\b|\bipod\b|\bgadget\b|\bradio\b',s):return '30'
 if origin in ('science-technology','general','rated','newest','world','hobbies') and re.search(r'\bautomobile\b|\bcars?\b|\baircraft\b|\bboeing\b|\bferrari\b|\bairbus\b|\bmotorcycle\b|\blocomo|\bvehicle\b',s):return '28'
 if origin in ('world','people','history','general','rated','newest'):
  if re.search(r'\bpresident\b|\bprime minister\b|\bsenator\b|\bparliament\b|\belection\b|\bcongress\b|\bpolitic',s):return '24'
  if origin=='world' and re.search(r'\bcapital\b|\bcountr|\bcontinent\b|\bmountain\b|\briver\b|\bisland\b|\bborder\b|\bocean\b|\bgeograph',s):return '22'
 if origin in ('humanities','general','rated','newest','people') and re.search(r'\bpainter\b|\bpainting\b|\bsculpture\b|\bsculptor\b|\bartist\b|\bpicasso\b|\bmonet\b|\bvan gogh\b|\bmuseum\b',s):return '25'
 if origin in ('religion-faith','humanities','general','rated','newest') and re.search(r'\bmytholog|\bzeus\b|\bposeidon\b|\bathena\b|\bthor\b|\bodin\b|\banubis\b|\bhercules\b',s):return '20'
 return mapping[origin]
seen={' '.join(q['prompt'].casefold().split()):q for q in bank};reject=collections.Counter();accepted=0;raw=0
clean=lambda s:html.unescape(s).strip()
for file in sorted((args.source/'categories').iterdir()):
 if not file.is_file() or file.name not in mapping:continue
 for block in re.split(r'(?m)^#Q\s+',file.read_text(encoding='utf-8-sig',errors='replace'))[1:]:
  raw+=1;lines=block.strip().splitlines();text=clean(lines[0]);correct=[clean(s[2:]) for s in lines[1:] if s.startswith('^ ')]
  opts=[clean(s[2:]) for s in lines[1:] if re.match(r'^[A-Z] ',s)]
  if len(correct)!=1 or len(opts)!=4 or correct[0] not in opts or len({s.casefold() for s in opts})!=4:reject['non_four_or_invalid']+=1;continue
  if len(text)>300 or any(len(s)>100 for s in opts) or '\ufffd' in text or any('\ufffd' in s for s in opts):reject['length_or_encoding']+=1;continue
  if any(re.search(r'\b(?:all|none) of the above\b|\b(?:both|either) [a-d] and [a-d]\b|\b(?:answer|option) [a-d]\b',s,re.I) for s in opts):reject['position_dependent_answers']+=1;continue
  if re.search(r'\bcurrently\b|\bat present\b|\bthis year\b|\btoday\b|\blast question\b|\bprevious question\b|\bnext question\b|\bmost recent\b|\bnowadays\b',text,re.I):reject['time_or_context_dependent']+=1;continue
  key=' '.join(text.casefold().split())
  if key in seen:reject['duplicate_prompt']+=1;continue
  q=dict(id=hashlib.sha256(key.encode()).hexdigest()[:20],categoryID=category(file.name,text),difficulty='mixed',prompt=text,answers=opts,correctIndex=opts.index(correct[0]),source='OpenTriviaQA contributors',sourceURL='https://github.com/uberspot/OpenTriviaQA',license='CC BY-SA 4.0',reviewStatus='imported_unreviewed')
  bank.append(q);seen[key]=q;accepted+=1
# Remove existing position-dependent options too: answer shuffling must preserve meaning.
bank=[q for q in bank if not any(re.search(r'\b(?:all|none) of the above\b|\b(?:both|either) [a-d] and [a-d]\b',s,re.I) for s in q['answers'])]
counts=collections.Counter(q['categoryID'] for q in bank)
for c in cats:c['questionCount']=counts[c['id']]
(data/'questions.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(data/'categories.json').write_text(json.dumps(cats,ensure_ascii=False,indent=2),encoding='utf-8')
db=sqlite3.connect(data/'question-bank.sqlite')
columns={r[1] for r in db.execute('PRAGMA table_info(questions)')}
if 'payload' not in columns:db.execute('ALTER TABLE questions ADD COLUMN payload TEXT')
db.execute('DELETE FROM questions')
db.executemany('INSERT INTO questions(id,category_id,difficulty,prompt,answers,correct_index,source,license,review_status,payload) VALUES(?,?,?,?,?,?,?,?,?,?)',[(q['id'],q['categoryID'],q['difficulty'],q['prompt'],json.dumps(q['answers'],ensure_ascii=False),q['correctIndex'],q['source'],q['license'],q['reviewStatus'],json.dumps(q,ensure_ascii=False)) for q in bank]);db.commit();db.execute('VACUUM');db.close()
report={'accepted':len(bank),'categoryCount':len(cats),'sources':{'OpenTDB':{'snapshot':'77d8e3cb5c8e264d50220eee75cfe08d233b1910'},'OpenTriviaQA':{'url':'https://github.com/uberspot/OpenTriviaQA','snapshot':'dcc1cdf36c2985ed5c849d1f2265c5041ffcdfb9','raw':raw,'added':accepted,'rejected':dict(reject)}},'categories':cats,'notes':'Structural validation and conservative context filters only; not independent fact checking. Mixed difficulty means the source did not supply difficulty ratings.'}
(data/'import-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(data/'CC-BY-SA-4.0.txt').write_text((args.source/'LICENSE').read_text(encoding='utf-8'),encoding='utf-8')
print(json.dumps({'accepted':len(bank),'added':accepted,'rejected':dict(reject),'categories':{c['name']:c['questionCount'] for c in cats}},indent=2))
