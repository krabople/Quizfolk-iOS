"""Continue the partial author pass without issuing publication approval."""
import hashlib,json,pathlib
H=pathlib.Path(__file__).parent
draft=json.loads((H/'draft.json').read_text(encoding='utf8'))
review=json.loads((H/'partial-review.json').read_text(encoding='utf8'))
edits={
51:{'answers':['Creases','Loose lint','Stains','Broken stitches']},
52:{'answers':['Steam','Compressed cold air','Ultraviolet light','Static electricity'],'sourceURL':'https://www.philips.com/c-p/GC507_63/easy-touch-garment-steamer'},
55:{'answers':['Heated plates','Rotating cutting blades','Cold rollers','High-pressure water jets'],'sourceURL':'https://www.ghdhair.com/za/hair-straighteners-c'},
56:{'answers':['Hair near the skin','Fingernails','Cuticles','Fabric fibres'],'sourceURL':'https://www.usa.philips.com/c-p/X3001_90/shaver-2400-wet-dry-electric-shaver'},
58:{'answers':['Heat','Air circulation','Moisture','Cooling']},
59:{'answers':['Heat','Cooling','Moisture','Filtered air']},
60:{'answers':['Localised warmth','Muscle stimulation through electrical pulses','A reading of skin temperature','Cooling through evaporation']},
63:{'answers':['Sound','Light','Heat as its intended output','A digital photograph']},
65:{'answers':['A short-range wireless link','An optical-fibre cable','A USB audio cable','An analogue headphone cable']},
66:{'prompt':'What is a pop filter placed in front of a recording microphone designed to reduce?','answers':['Popping sounds from bursts of breath','The recording file size','The length of the spoken words','The pitch of every sung note'],'sourceURL':'https://www.shure.com/en-US/docs/education/Microphone-Techniques-for-Recording'},
68:{'answers':['Carry more loudly over a distance','Become higher in pitch automatically','Be translated into another language','Be saved as an audio recording automatically']},
70:{'answers':['Hear or watch a baby from another room','Automatically prepare a milk feed','Measure the temperature of bathwater','Wash and dry baby clothes']},
71:{'prompt':'Which device receives television signals and supplies them to a TV as viewable programmes?','answers':['A set-top box','A games controller','A soundbar','A DVD writer'],'sourceURL':'https://dictionary.cambridge.org/dictionary/english/set-top-box'},
72:{'answers':['How sharply the subject appears','The printed magnification number','The actual distance to the subject','The spacing between the eyepieces']},
}
notes='''51|Clothes iron removes creases using heated flat base; lint removal, stain removal and stitch repair require other actions. Cambridge clothes-appliance sense inspected rather than chemical element/golf club. Removed bizarre all-colour/fibre/button alternatives.
52|Garment steamer uses steam to relax creases; cold air, UV and static electricity not its intended crease-removal mechanism. Philips indexed product passage explicitly continuous steam removes creases; dictionary steamer entry was boat/cooking and insufficient. No universal fabric-safety claim imported from advertising.
53|Hairdryer blows air to dry hair; clippers/shaver cut hair and fanless curling tong heats it. Dictionary explicitly electrical hot-air drying device. Question does not falsely require hot setting in every use.
54|Electric hair clippers cut hair. Blow-drying, plate straightening and automatic dyeing are distinct functions. Clipper dictionary includes hair cutting; no claim all clippers are electrical or only for hair.
55|Hair straightener heated plates supported by ghd heat-sensor/plate description. Replaced silly saw/blowup alternatives with actual grooming mechanisms. Does not claim every hair-straightening method uses this appliance design or specific temperature is safe.
56|Electric shaver cuts hair near skin. Philips product explicitly blades cut hair above skin; nail/cuticle/fabric tasks are different. Near-skin wording permits foil/rotary and above/below skin-level marketing variants without asserting blades touch skin.
57|Sewing machine forms stitches joining cloth. Iron, dryer and steamer do not sew. Cambridge needle-based machine definition inspected. Appliance label accommodates manual or electrical machines without claiming all are powered.
58|Electric blanket provides heat. Air circulation, adding moisture and cooling are not ordinary electric blanket functions. Cambridge internal heating wires definition inspected. No safety/use guidance or universal material assumption.
59|Portable room heater produces heat. Cooling, humidification and air filtering are other main functions, even if combination appliances exist. Dedicated heating-device definition used, not baseball heater slang.
60|Electric heating pad intended local warmth, not TENS stimulation, measurement or evaporative cooling. Revised distractors to actual personal-care mechanisms. Pending suitable manufacturer reference; existing guessed dictionary entry has no definition. Do not approve yet.
61|Headphones normally on/over ears for listening. Soundbar, projector and webcam not worn as personal audio transducers. Definition supports ear coverage; no claim absolutely no sound leaks to bystanders.
62|Earbuds small earphones at/in ear canal. Screens, camera supports and ink cartridges false. Near qualifier includes open-fit earbuds. Dedicated earbud definition inspected.
63|Loudspeaker converts electrical audio signal into sound. Light, intentional heat output and photographs not its principal output. Definition explicitly electrical-signal-to-sound conversion. Heat can be a by-product, hence intended-output qualifier on heat alternative.
64|Soundbar long speaker unit usually used with TV. Lens, charging cable and memory card not soundbar. Dedicated definition explicitly speaker-containing horizontal bar, allows computer use through often qualifier.
65|Bluetooth speaker uses short-range wireless audio; fibre/USB/analogue cable not Bluetooth transport. Revised silly alternatives to real audio connection types. Pending Bluetooth-specific supporting reference; guessed Bluetooth-speaker dictionary entry empty. Main wording does not deny optional wired inputs.
66|Replaces exact Computers microphone-purpose duplicate. Shure recording guide explicitly plosive p/t popping reduced with pop filter; file size, word duration and every note's pitch unaffected as intended function. Accessory function described without claiming all background noise removed.
67|Voice recorder specifically saves spoken audio, unlike pointer/frame/barcode scanner. Wording makes voice note purpose clear but does not claim exclusively speech. Pending actual recorder/audio definition; guessed voice-recorder dictionary entry empty.
68|Megaphone amplifies/project voice to distance. Does not inherently pitch-shift, translate or save recordings; combinations may exist but not defining feature. Cambridge cone-shaped voice amplification sense inspected. Removed surreal photo/page alternatives.
69|Walkie-talkie portable two-way radio sends/receives messages. Photo frame, vacuum and scale other gadgets. Definition supports both transmission/reception without claim simultaneous full-duplex operation.
70|Baby monitor lets carer hear/sometimes see baby in other room. Feed preparation, bath temperature and laundry separate devices. Cambridge explicit hear/sometimes see wording; not every model necessarily has video.
71|Replaces exact Computers projector duplicate. Proposed set-top box television receiver/decoder function, unlike game controller, soundbar or DVD writer. Pending dedicated set-top-box reference and semantic overlap recheck before approval; don't treat proposed replacement as verified yet.
72|Focusing wheel changes apparent sharpness, not nominal magnification, actual subject distance or eyepiece separation. Generic binocular dictionary only magnification and tubes, insufficient proof of wheel function. Pending actual binocular operating instructions; retrieved Nikon camera-focus source is not claimed direct binocular support.
73|Tripod three supporting legs; monopod, selfie stick and gimbal handle alone do not. Dedicated dictionary confirms three-legged support. Camera scope clear; no assertion every camera support needs three legs.
74|Standard monopod one leg; two/three/four not its defining single-support form. Pending manufacturer definition because guessed dictionary entry empty. Some monopods add a small folding foot, so final wording may need 'main supporting leg' to avoid foot/leg ambiguity before approval.
75|Selfie stick holds phone/camera farther away for self-portrait; no change in sensor size, inherent instant printing or battery replacement. Dedicated definition explicitly distance allowing more subjects. Not assuming every stick includes remote shutter or motor.
'''
review['rows']=[x for x in review['rows'] if x['row']<=50]
pending={16,60,65,67,71,72,74}
for line in notes.strip().splitlines():
 n,note=line.split('|',1);n=int(n);q=dict(draft[n-1]);q.update(edits.get(n,{}));q['rationale']=note;draft[n-1]=q
 fp=hashlib.sha256(json.dumps({k:q[k] for k in ('prompt','answers','correctIndex','sourceURL')},ensure_ascii=False,sort_keys=True).encode()).hexdigest()
 review['rows'].append({'row':n,'note':note,'status':'pending_specific_reference' if n in pending else 'author_partial_pass_checked','fingerprint':fp})
review.update(checkedRows=75,pendingReferenceRows=sorted(pending),notYetCheckedRows=list(range(76,101)))
assert [x['row'] for x in review['rows']]==list(range(1,76))
for name,obj in [('draft.json',draft),('partial-review.json',review)]:
 (H/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('75 partial judgments saved, seven reference checks pending; no publication approval')
