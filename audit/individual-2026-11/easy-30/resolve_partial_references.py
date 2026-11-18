"""Record specifically inspected references; still no whole-batch approval."""
import hashlib,json,pathlib
H=pathlib.Path(__file__).parent
d=json.loads((H/'draft.json').read_text(encoding='utf8'));r=json.loads((H/'partial-review.json').read_text(encoding='utf8'))
refs={
16:('https://industrial.panasonic.com/cdbs/www-data/pdf/AAF4000/ast-ind-181246.pdf','Indexed Panasonic battery-terminal sheet identifies plus/positive and minus/negative. Specific terminal marking now corroborated, not merely dictionary electrical-charge meaning.'),
60:('https://pim.beurer.com/images/attribut/211.70_UHP24_2020-06-05_02_IM_BEU-USA-CAN.pdf','Indexed Beurer intended-use paragraph explicitly applying heat to body for warmth/comfort. Supports local warmth, no pain-relief or treatment claim added.'),
65:('https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core_v6.3/out/en/architecture%2C-change-history%2C-and-conventions/architecture.html','Bluetooth SIG architecture explicitly wireless cable-replacement communications. Radio/wireless connection also confirmed by Cambridge Bluetooth entry. Removed short-range label because SIG range article explains variable range; no particular range claimed.'),
71:('https://dictionary.cambridge.org/dictionary/english/set-top-box','Retrieved dedicated definitions explicitly viewing digital broadcasts and cable/satellite programmes on TV. Revised stem specifically digital broadcasts so not any generic video source.'),
79:('https://dictionary.cambridge.org/dictionary/english/camcorder','Retrieved dedicated definition small video camera records images/sound. Video answer correct; audio-only alternative explicitly excludes accompanying images. No reliance on obsolete videotape-only wording.'),
80:('https://dictionary.cambridge.org/dictionary/english/flash','Retrieved photographic flash sense explicitly bright light for brief time while taking photograph. Other flash meanings excluded. Confirms brief burst answer.'),
93:('https://dictionary.cambridge.org/dictionary/english/light-meter','Retrieved explicit device measuring amount of light especially photography. Confirms intended quantity, not distance/mass/temperature.')}
for n,(url,note) in refs.items():
 q=d[n-1];q['sourceURL']=url;q['rationale']+=' FOLLOW-UP: '+note
 if n==65:q['answers'][0]='A wireless radio link'
 if n==71:q['prompt']='Which device enables an ordinary television to receive digital broadcasts?'
 row=r['rows'][n-1];row.update(note=q['rationale'],status='author_partial_pass_checked',fingerprint=hashlib.sha256(json.dumps({k:q[k] for k in ('prompt','answers','correctIndex','sourceURL')},ensure_ascii=False,sort_keys=True).encode()).hexdigest())
r['pendingReferenceRows']=[x for x in r['pendingReferenceRows'] if x not in refs]
for name,obj in [('draft.json',d),('partial-review.json',r)]:
 (H/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Seven specific references resolved; remaining',r['pendingReferenceRows'],'; final batch approval still required')
