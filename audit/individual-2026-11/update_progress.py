"""Recount actual completed local reviews; never infer deployment from a local file."""
import collections,json,pathlib
p=pathlib.Path(__file__).parent;root=p.parents[1]
progress=json.loads((p/'progress.json').read_text(encoding='utf8'))
bank=json.loads((root/'data/questions.json').read_text(encoding='utf8'))
counts=collections.Counter(q['categoryID'] for q in bank if q.get('auditVersion','').startswith('2026-11-easy-') or q.get('auditVersion')=='2026-11-plants-easy-v1')
for topic in progress['topics']:
 folder=p/('plants-easy' if topic['topicID']=='39' else 'easy-'+topic['topicID'])
 topic['authored']=len(json.loads((folder/'draft.json').read_text(encoding='utf8'))) if (folder/'draft.json').exists() else 0
 topic['reviewedAndValidated']=counts[topic['topicID']]
progress['reviewedAndValidated']=sum(counts.values())
progress['localBankCount']=len(bank)
progress['updated']='2026-11-17'
(p/'progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:progress[k] for k in ('reviewedAndValidated','localBankCount','liveBankCount')}))
