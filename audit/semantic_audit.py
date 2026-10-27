import sys,pathlib,json,re,math,collections
r=pathlib.Path(__file__).resolve().parents[1]
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--source-bank',type=pathlib.Path,required=True);parser.add_argument('--work',type=pathlib.Path,required=True);args=parser.parse_args();work=args.work;sys.path.insert(0,str(work/'audit-libs'))
import numpy as np,onnxruntime as ort
from tokenizers import Tokenizer
a=r;data=a/'data';bank=json.loads(args.source_bank.read_text(encoding='utf-8'));cats=json.loads((data/'categories.json').read_text(encoding='utf-8'))
vectors=np.load(work/'question-embeddings.npy');assert len(vectors)==len(bank)
desc={
'9':'General knowledge trivia. Everyday objects, facts, traditions, society, inventions and miscellaneous knowledge.',
'10':'Books and literature trivia. Authors, novels, fiction, literary characters, poetry, book titles and stories.',
'11':'Cinema and film trivia. Movies, actors in film roles, directors, screenplays, movie characters and films.',
'12':'Music trivia. Songs, musicians, bands, albums, singers, musical instruments, concerts and composers.',
'13':'Stage and musicals trivia. Broadway, West End theatre, stage plays, actors, musicals and musical theatre.',
'14':'Television trivia. TV series, sitcoms, television characters, actors, episodes, television programmes and drama.',
'15':'Video game trivia. Console and computer games, gameplay, game characters, PlayStation, Nintendo and Xbox.',
'16':'Board game trivia. Chess, Monopoly, Scrabble, dice, tabletop games, card games and board game rules.',
'17':'Science and nature trivia. Biology, chemistry, physics, natural phenomena, astronomy, plants, anatomy and scientific discoveries.',
'18':'Computer science trivia. Computing, software, programming, computer hardware, operating systems, internet, data and computer networks.',
'19':'Mathematics trivia. Arithmetic calculations, numbers, factorial, fractions, algebra, geometry, equations, shapes, probability and mathematical symbols.',
'20':'Mythology trivia. Greek, Roman, Norse and Egyptian gods, ancient myths, legends, mythical creatures and heroes.',
'21':'Sports trivia. Football, basketball, tennis, cricket, Olympics, athletes, teams, tournaments, sports records and sports rules.',
'22':'Geography trivia. Countries, cities, capitals, rivers, mountains, oceans, continents, islands, flags, borders and places.',
'23':'History trivia. Historical events, wars, ancient civilizations, historical dates, monarchs, empires and past events.',
'24':'Politics trivia. Presidents, prime ministers, parliament, elections, political parties, government, laws and political leaders.',
'25':'Art trivia. Painting, painters, sculpture, visual artists, art movements, drawings, artistic works, galleries and museums.',
'26':'Famous people and celebrity trivia. Biographies, famous personalities, actors, celebrities, personal lives, births, achievements and people.',
'27':'Animal trivia. Mammals, birds, fish, reptiles, insects, wildlife species, animal behaviour, animal biology and pets.',
'28':'Vehicle trivia. Cars, motorcycles, engines, automobile manufacturers, airplanes, trains, ships and transport.',
'29':'Comic book trivia. Comics, graphic novels, Marvel, DC Comics, superheroes, Superman, Batman and comic characters.',
'30':'Gadget trivia. Phones, cameras, consumer electronics, devices, radio, television equipment and technological gadgets.',
'31':'Anime and manga trivia. Japanese animation, anime series, manga comics, Naruto, Dragon Ball, Sailor Moon and anime characters.',
'32':'Cartoon and animation trivia. Animated cartoons, Disney, Pixar, Simpsons, cartoon characters and animated films.',
'33':'Brain teasers. Riddles, logical puzzles, word puzzles, lateral thinking, reasoning and problems to solve.',
'34':'Hobbies trivia. Crafts, gardening, knitting, sewing, collecting, recreational activities, hobbies, toys and leisure.',
'35':'Language and culture trivia. Words, word meanings, idioms, languages, grammar, expressions, customs and cultures.',
'36':'World religion trivia. Bible, Christianity, Islam, Buddhism, Hinduism, religious texts, beliefs, religious customs and faith.',
'37':'Family trivia. General knowledge for children, fairy tales, nursery rhymes, children stories and elementary knowledge.',
'38':'Food and drink trivia. Cooking, cuisine, ingredients, recipes, dishes, drinks, cocktails, wine, fruit, vegetables, cheese and desserts.'}
tok=Tokenizer.from_file(str(work/'audit-model/tokenizer.json'));tok.enable_padding();tok.enable_truncation(max_length=128)
opts=ort.SessionOptions();opts.intra_op_num_threads=4
sess=ort.InferenceSession(str(work/'audit-model/model_quantized.onnx'),sess_options=opts,providers=['CPUExecutionProvider'])
def encode(texts):
 e=tok.encode_batch(texts);ids=np.array([x.ids for x in e],dtype=np.int64);m=np.array([x.attention_mask for x in e],dtype=np.int64)
 h=sess.run(None,{'input_ids':ids,'attention_mask':m,'token_type_ids':np.zeros_like(ids)})[0];v=(h*m[:,:,None]).sum(1)/m.sum(1)[:,None];return v/np.linalg.norm(v,axis=1,keepdims=True)
ids=[c['id'] for c in cats];prototypes=encode([desc[i] for i in ids]);scores=vectors@prototypes.T
byid={c['id']:c for c in cats};ledger=[];accepted=[];held=[];reasons=collections.Counter();changed=collections.Counter()
for n,original in enumerate(bank):
 q=dict(original);s=q['prompt'].strip();old=q['categoryID'];new=old;why=[];hold=[];manual=False
 top=int(scores[n].argmax());best=ids[top];bestScore=float(scores[n,top]);current=float(scores[n,ids.index(old)])
 # Every record gets a semantic score and explicit language/context checks.
 if len(re.findall(r"[A-Za-z]+",s))<4:hold.append('insufficient_standalone_wording')
 if len(s)>200 or len(s.split())>38 or sum(len(x.split()) for x in [s]+q['answers'])>70:hold.append('too_much_reading_for_ten_seconds')
 if re.search(r'\b(?:pictured|photograph|image below|diagram|picture|audio clip|sound clip|shown above|shown below|shown here|previous question|last question|previous answer|in this quiz|earlier question|following passage)\b',s,re.I):hold.append('missing_media_or_external_context')
 if re.search(r'\bwho (?:said|wrote) (?:this|that)\??$',s,re.I):hold.append('missing_quotation')
 if re.search(r'\b(?:currently|nowadays|today|at present|this year|most recent|latest)\b',s,re.I):hold.append('unbounded_time_dependency')
 if re.search(r'\bwho is\b.*\b(?:president|prime minister|wife|husband|spouse)\b',s,re.I) and not re.search(r'\b(?:1[0-9]{3}|20[0-9]{2})\b',s):hold.append('present_tense_fact_without_date')
 if any(re.search(r'\b(?:all|none) of (?:the above|these|them)\b|\b(?:both|either) [a-d] (?:and|or|&) [a-d]\b|\b(?:option|answer|choice) [a-d]\b',x,re.I) for x in q['answers']):hold.append('answer_position_dependency')
 f=re.fullmatch(r'\s*(?:calculate|what is|evaluate|find)?\s*(\d{1,2})\s*!\s*[?.]?\s*',s,re.I)
 if f:
  value=int(f[1]);expected=str(math.factorial(value));actual=q['answers'][q['correctIndex']].replace(',','').strip()
  if expected==actual and 2<=value<=12:
   q['prompt']=f'What is {value} factorial, the product of the whole numbers from 1 to {value}?';new='19';why.append('factorial_explained_and_mathematically_checked');manual=True;hold=[x for x in hold if x!='insufficient_standalone_wording']
  else:hold.append('unexplained_or_unverified_factorial')
 elif old in ('9','17','18','19','33','35','37') and re.search(r'\b(?:factorial|square root|cube root|algebra|trigonometry|cosine|sine|decimal places)\b|\b(?:calculate|evaluate)\s+[\d(\-]|\d\s*[+×÷^]\s*\d',s,re.I):
  new='19';why.append('explicit_mathematical_question')
 elif old=='17' and re.search(r'\b(?:CPU|RAM|HTML|operating system|computer|software|programming|internet protocol)\b',s,re.I):new='18';why.append('computing_specialist_topic')
 elif old=='17' and re.search(r'\b(?:telephone|smartphone|mobile phone|camera|gadget|ipod|iphone)\b',s,re.I):new='30';why.append('device_specialist_topic')
 elif best!=old and best not in ('9','37') and bestScore>=0.30 and bestScore-current>=0.07:
  # Similarity can confuse an animal in a film with zoology. Hold these proposals
  # for editorial review instead of silently making speculative category moves.
  hold.append('semantic_category_mismatch_requires_review')
 if s.endswith(':') or re.search(r'\b(?:following|this) (?:series|sequence|diagram|picture)\s*[?.:]?$',s,re.I):hold.append('incomplete_question_context')
 if any('\ufffd' in t for t in [s]+q['answers']):hold.append('damaged_character_encoding')
 # Broad topics can legitimately cover several domains; narrow topics need evidence of fit.
 if old not in ('9','37') and current<0.18:hold.append('uncertain_specialist_category_fit')
 if bestScore<0.16:hold.append('low_semantic_clarity')
 entry={'id':q['id'],'prompt':original['prompt'],'originalTopic':old,'suggestedTopic':new,'categorySimilarity':round(current,4),'bestSimilarity':round(bestScore,4),'bestSemanticTopic':best,'checks':['structure','standalone_wording','reading_length','media_context','temporal_context','answer_dependencies','topic_semantics'],'reasons':sorted(set(why+hold)),'action':'quarantined' if hold else ('rewritten' if manual else ('recategorised' if new!=old else 'retained')),'reviewMethod':'per-record automated semantic and language audit','verifiedByDerivation':manual,'manualReview':q['id']=='66b6a0317332fa97167e'}
 ledger.append(entry)
 if hold:held.append(original);reasons.update(set(hold));continue
 q['categoryID']=new;q['reviewStatus']='automated_semantic_screened';q['auditVersion']='2026-10-27-v2'
 if why:q['auditNotes']=why
 accepted.append(q)
 if new!=old:changed[(old,new)]+=1
counts=collections.Counter(q['categoryID'] for q in accepted)
report={'screened':len(bank),'retained':len(accepted),'quarantined':len(held),'actions':dict(collections.Counter(x['action'] for x in ledger)),'quarantineReasons':dict(reasons),'moves':[{'from':f,'to':t,'count':v} for (f,t),v in changed.most_common()],'categories':{byid[i]['name']:counts[i] for i in ids},'method':'Local MiniLM semantic similarity plus explicit context, time-dependence, mathematical notation and readability rules. Scores are heuristic similarities, not probabilities. Every source record has a ledger entry. This is not 45,581 individual human factual reviews.'}
(work/'audit-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False),encoding='utf-8');(work/'audit-accepted.json').write_text(json.dumps(accepted,ensure_ascii=False),encoding='utf-8');(work/'audit-quarantine.json').write_text(json.dumps(held,ensure_ascii=False),encoding='utf-8');(work/'audit-summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='moves'},indent=2))
