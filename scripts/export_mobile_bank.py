"""Export one validated data-only snapshot for both apps; no app-store release needed."""
import argparse,collections,hashlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--output',type=pathlib.Path,default=ROOT/'build/mobile-bank');parser.add_argument('--format',type=int,choices=[1,2],default=1);args=parser.parse_args()
subprocess.run([sys.executable,str(ROOT/'scripts/validate_bank.py')],check=True)
questions=json.loads((ROOT/'data/questions.json').read_text(encoding='utf8'))
categories=json.loads((ROOT/'data/categories.json').read_text(encoding='utf8'))
if args.format==1:
 questions=[q for q in questions if not q.get('imagePng')];categories=[c for c in categories if not c.get('requiresImages')]
fields=['id','categoryID','difficulty','prompt','answers','correctIndex','imagePng','imageSHA256','questionGroup']
snapshot={'format':args.format,'categories':categories,'questions':[{key:q[key] for key in fields if key in q} for q in questions]}
payload=json.dumps(snapshot,ensure_ascii=False,separators=(',',':')).encode('utf8')
revision=hashlib.sha256(payload).hexdigest();filename='bank-'+revision+'.json'
manifest={'format':args.format,'revision':revision,'file':filename,'bytes':len(payload),'questionCount':len(questions),'topicCount':len(categories)}
args.output.mkdir(parents=True,exist_ok=True)
(args.output/filename).write_bytes(payload)
(args.output/'manifest.json').write_text(json.dumps(manifest,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
(args.output/'.htaccess').write_text('''Options -Indexes
<IfModule mod_deflate.c>
 AddOutputFilterByType DEFLATE application/json
</IfModule>
<IfModule mod_headers.c>
 <Files "manifest.json">
  Header set Cache-Control "no-cache"
 </Files>
 <FilesMatch "^bank-[a-f0-9]{64}\\.json$">
  Header set Cache-Control "public, max-age=31536000, immutable"
 </FilesMatch>
</IfModule>
''',encoding='utf8',newline='\n')
print(json.dumps({'directory':str(args.output),**manifest}))
