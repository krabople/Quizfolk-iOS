"""First20 accessible celebrity candidates from inspected references, not approval."""
import json,pathlib,urllib.parse
H=pathlib.Path(__file__).parent;assert not (H/'draft.json').exists(),'Do not overwrite subsequent author edits.'
raw='''Jamie Oliver|Which chef rose to fame with the television series The Naked Chef?|Jamie Oliver|Gordon Ramsay|Rick Stein|James Martin
Gordon Ramsay|Which celebrity chef is associated with Hell's Kitchen and Kitchen Nightmares?|Gordon Ramsay|Jamie Oliver|Rick Stein|Paul Hollywood
Nigella Lawson|Which cookery writer published How to Eat?|Nigella Lawson|Mary Berry|Delia Smith|Prue Leith
Mary Berry|Which baking competition did Mary Berry judge between 2010 and 2016?|The Great British Bake Off|MasterChef|Ready Steady Cook|Great British Menu
Paul Hollywood|What trade did Paul Hollywood learn in his father's business?|Baking|Carpentry|Tailoring|Jewellery making
Nadiya Hussain|Which television competition did Nadiya Hussain win in 2015?|The Great British Bake Off|MasterChef|The Great British Sewing Bee|The Great Pottery Throw Down
Ainsley Harriott|Who hosted the BBC cooking shows Can't Cook, Won't Cook and Ready Steady Cook?|Ainsley Harriott|James Martin|Rick Stein|Marcus Wareing
Gino D'Acampo|Which cuisine is most closely associated with Gino D'Acampo's cooking?|Italian|Japanese|Indian|French
James Martin (chef)|Which BBC cookery programme did James Martin present from 2006 to 2016?|Saturday Kitchen|MasterChef|Great British Menu|Ready Steady Cook
Rick Stein|Which chef co-founded The Seafood Restaurant in Padstow with Jill Stein?|Rick Stein|Gordon Ramsay|Heston Blumenthal|Marco Pierre White
Dave Myers|Of which television cooking duo was Dave Myers a member?|The Hairy Bikers|The Fabulous Baker Brothers|Two Fat Ladies|The Tanner Brothers
Delia Smith|Which football club has Delia Smith famously supported and co-owned?|Norwich City|Ipswich Town|Nottingham Forest|Coventry City
Tom Kerridge|With which profession is television personality Tom Kerridge most closely associated?|Chef|Fashion designer|Physicist|Professional cyclist
Marcus Wareing|Which chef joined the judging panel of MasterChef: The Professionals in 2014?|Marcus Wareing|Michel Roux Jr.|Ainsley Harriott|Rick Stein
Michel Roux Jr.|Which chef led the London restaurant Le Gavroche for many years?|Michel Roux Jr.|Rick Stein|Ainsley Harriott|James Martin
Heston Blumenthal|Which chef became famous for unusual dishes such as bacon-and-egg ice cream and snail porridge?|Heston Blumenthal|Jamie Oliver|Rick Stein|Paul Hollywood
Prue Leith|Who replaced Mary Berry as a judge when The Great British Bake Off moved to Channel 4?|Prue Leith|Nigella Lawson|Delia Smith|Nadiya Hussain
Yotam Ottolenghi|Who wrote the cookbooks Plenty and Simple?|Yotam Ottolenghi|Heston Blumenthal|Paul Hollywood|Nigella Lawson
Angela Hartnett|With which profession is Angela Hartnett most closely associated?|Chef|Fashion designer|Professional swimmer|Magician
Samin Nosrat|What is the title of Samin Nosrat's cookbook and Netflix series?|Salt Fat Acid Heat|How to Eat|The Fat Duck Cookbook|The Naked Chef'''
d=[]
for i,line in enumerate(raw.splitlines(),1):
 name,prompt,*answers=line.split('|');assert len(answers)==4
 url='https://www.hairybikers.com/about' if name=='Dave Myers' else 'https://en.wikipedia.org/wiki/'+urllib.parse.quote(name.replace(' ','_'))
 d.append({'draftID':f'easy-26-{i:03d}','categoryID':'26','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'sourceURL':url,'rationale':'UNAPPROVED partial-batch candidate; individual final editorial and full-bank duplicate checks pending.','reviewStatus':'draft_unreviewed'})
assert len(d)==20
(H/'draft.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('20 celebrity candidates drafted; none final-approved or published.80 still to draft.')
