"""Retrieve short definition excerpts for editorial inspection, not approval."""
import html,json,pathlib,re,sys,urllib.request
from author import sources
HERE=pathlib.Path(__file__).parent
terms='index glossary appendix foreword prologue epilogue author illustrator translator narrator biography autobiography fiction anthology trilogy sequel ebook audiobook hardback paperback'.split()
path=HERE/'dictionary-access.json'
records=json.loads(path.read_text(encoding='utf8')) if path.exists() else {}
for term in terms[int(sys.argv[1]):int(sys.argv[2])]:
    try:
        request=urllib.request.Request(sources[term],headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(request,timeout=8) as response:
            body=response.read().decode('utf8')
        matches=re.findall(r'<div[^>]*class="def ddef_d db"[^>]*>(.*?)</div>',body,re.S)
        text=[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in matches]
        records[term]={'url':sources[term],'definitions':text[:7],'status':'retrieved_for_human_inspection' if text else 'no_definition_extracted'}
    except Exception as error:
        records[term]={'url':sources[term],'error':str(error),'status':'fetch_failed'}
    print(json.dumps({term:records[term]},ensure_ascii=False))
    path.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
