import json, html, hashlib, pathlib, collections, sqlite3, argparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; DATA.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('source_json',type=pathlib.Path);args=parser.parse_args()
raw=json.loads(args.source_json.read_text(encoding='utf-8'))
META=[('General Knowledge','General Knowledge','sparkles','E8AB3B','🧠'),('Entertainment: Books','Books','books.vertical.fill','8464BD','📚'),('Entertainment: Film','Film','film.fill','DC645C','🎬'),('Entertainment: Music','Music','music.note','D85B96','🎵'),('Entertainment: Musicals & Theatres','Stage & Musicals','theatermasks.fill','C87055','🎭'),('Entertainment: Television','Television','tv.fill','667BC2','📺'),('Entertainment: Video Games','Video Games','gamecontroller.fill','6779CA','🎮'),('Entertainment: Board Games','Board Games','dice.fill','B47A57','🎲'),('Science & Nature','Science & Nature','atom','47A6A3','🔬'),('Science: Computers','Computers','desktopcomputer','5A8DAE','💻'),('Science: Mathematics','Mathematics','function','647CB2','➗'),('Mythology','Mythology','bolt.fill','AF8B50','⚡'),('Sports','Sport','sportscourt.fill','58A381','🏆'),('Geography','Geography','globe.europe.africa.fill','3D9F9F','🌍'),('History','History','building.columns.fill','B98253','🏛️'),('Politics','Politics','building.2.fill','7C899F','🗳️'),('Art','Art','paintpalette.fill','B96B9F','🎨'),('Celebrities','Celebrities','star.fill','C78F53','⭐'),('Animals','Animals','pawprint.fill','6FA267','🐾'),('Vehicles','Vehicles','car.fill','638AA3','🚗'),('Entertainment: Comics','Comics','bubble.left.fill','CA6C66','💥'),('Science: Gadgets','Gadgets','cpu.fill','7F92AD','📱'),('Entertainment: Japanese Anime & Manga','Anime & Manga','sparkles.tv.fill','A574BA','🌸'),('Entertainment: Cartoon & Animations','Cartoons','paintbrush.pointed.fill','D19C44','🧸')]
lookup={m[0]:(str(i+9),*m[1:]) for i,m in enumerate(META)}
questions=[]; seen=set(); rejected=collections.Counter()
for r in raw:
 if r['type']!='multiple': rejected['true_false']+=1; continue
 clean=lambda s:html.unescape(s).strip()
 text=clean(r['question']); key=' '.join(text.lower().split())
 opts=[clean(r['correct_answer'])]+[clean(s) for s in r['incorrect_answers']]
 if key in seen: rejected['duplicate']+=1;continue
 if len(opts)!=4 or len(set(s.casefold() for s in opts))!=4: rejected['invalid_options']+=1;continue
 cat=clean(r['category'])
 if cat not in lookup: rejected['unknown_category']+=1;continue
 seen.add(key)
 questions.append(dict(id=hashlib.sha256(key.encode()).hexdigest()[:20],categoryID=lookup[cat][0],difficulty=r['difficulty'],prompt=text,answers=opts,correctIndex=0,source='Open Trivia Database',sourceURL='https://opentdb.com/',license='CC BY-SA 4.0',reviewStatus='imported_unreviewed'))
counts=collections.Counter(q['categoryID'] for q in questions)
categories=[dict(id=v[0],name=v[1],symbol=v[2],color=v[3],emoji=v[4],questionCount=counts[v[0]]) for v in lookup.values()]
(DATA/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(DATA/'categories.json').write_text(json.dumps(categories,ensure_ascii=False,indent=2),encoding='utf-8')
report=dict(source='https://github.com/lipschultz/open-trivia-dataset',commit='77d8e3cb5c8e264d50220eee75cfe08d233b1910',raw=len(raw),accepted=len(questions),rejected=dict(rejected),categories=categories,notes='Structural validation only. Community questions have not been independently fact-checked. Smaller topics need expansion before launch.')
(DATA/'import-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
db=sqlite3.connect(DATA/'question-bank.sqlite');db.execute('CREATE TABLE IF NOT EXISTS questions(id TEXT PRIMARY KEY,category_id TEXT,difficulty TEXT,prompt TEXT,answers TEXT,correct_index INTEGER,source TEXT,license TEXT,review_status TEXT)')
db.executemany('INSERT OR REPLACE INTO questions VALUES(?,?,?,?,?,?,?,?,?)',[(q['id'],q['categoryID'],q['difficulty'],q['prompt'],json.dumps(q['answers'],ensure_ascii=False),0,q['source'],q['license'],q['reviewStatus']) for q in questions]);db.execute('CREATE INDEX IF NOT EXISTS category_idx ON questions(category_id)');db.commit();db.close()
print(json.dumps({'raw':len(raw),'accepted':len(questions),'rejected':dict(rejected),'counts':{c['name']:c['questionCount'] for c in categories}},indent=2))

