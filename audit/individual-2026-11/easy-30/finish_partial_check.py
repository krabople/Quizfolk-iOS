"""Finish preliminary judgments; unresolved references still block publication."""
import hashlib,json,pathlib
H=pathlib.Path(__file__).parent
draft=json.loads((H/'draft.json').read_text(encoding='utf8'))
r=json.loads((H/'partial-review.json').read_text(encoding='utf8'))
D='https://dictionary.cambridge.org/dictionary/english/'
edits={
77:{'answers':['The view from a vehicle while driving','Only the reversing view while parking',"Only the driver's pulse rate",'Only the car engine temperature']},
78:{'answers':['An action camera','A large studio view camera','A flatbed document scanner','An astronomical telescope']},
79:{'prompt':'What is a camcorder primarily designed to record?','answers':['Video','Printed photographs on paper','Sound without pictures','The temperature of a room'],'sourceURL':D+'camcorder'},
80:{'prompt':'What does a camera flash supply when taking a photograph?','answers':['A brief burst of light','A continuous stream of ink','A new frame of photographic film','A burst of compressed air'],'sourceURL':D+'flash'},
81:{'prompt':'A traditional linear barcode on a product represents information using what?','answers':['Parallel bars and spaces','A spiral groove','Embossed dots read by touch','A sequence of musical notes'],'sourceURL':'https://www.gs1.org/standards/barcodes'},
82:{'answers':['A digital photo frame','A flatbed scanner','A photo printer','An external hard drive']},
83:{'prompt':'What are wire strippers designed to remove from an electrical wire?','answers':['The insulating covering','The entire metal conductor','The plug pins','The colour of the metal'],'sourceURL':D+'wire-stripper'},
87:{'answers':['Metal objects','Changes in air pressure','Infrared heat patterns','Airborne smoke particles']},
88:{'answers':['Smoke that may indicate a fire','A build-up of carbon dioxide','A rise in humidity alone','A water leak on the floor']},
89:{'prompt':'Which household alarm is specifically designed to detect the poisonous gas CO?','answers':['A carbon monoxide alarm','A smoke alarm','A heat detector','A water-leak detector']},
90:{'answers':['A small spot of light','An image printed on paper','A physical arrow fired through the air','A stream of coloured ink']},
91:{'answers':['Distance to a target','The target surface temperature','The target chemical composition','The target mass']},
92:{'answers':['Local weather conditions','The progress of trains','The energy consumption of appliances','The number of nearby radio transmitters']},
93:{'prompt':'What does a photographer use a light meter to measure?','answers':['The amount of light','The distance to the subject','The weight of a camera','The temperature of a lens'],'sourceURL':D+'light-meter'},
94:{'prompt':'What can trigger a security light fitted with a motion sensor?','answers':['Nearby movement','A scheduled software update alone','A change in the Wi-Fi password alone','An incoming phone call alone']},
95:{'answers':['A camera to show visitors','A sensor to measure gas usage','A timer to control laundry cycles','A thermostat to control an oven']},
96:{'answers':['An immersive computer-generated environment','A physical paper map','A conventional radio programme without images','An unmodified optical view through binoculars']},
97:{'answers':['Digital information or images','A physical coat of paint','An unchanged optical reflection','An audio-only radio broadcast']},
98:{'answers':['A video game','A central-heating boiler','A refrigerator compressor','A printer ink supply']},
}
notes='''76|Camera gimbal helps stabilise camera orientation/reduce unwanted movement; not sensor pixels, memory storage or lens inventory. Cambridge rotating support keeping equipment in position supports mechanism. Does not promise elimination of all shake or motion.
77|Dashcam records vehicle road view. Reverse-only parking camera, pulse monitor and engine thermometer are other functions. Revised unrelated printer/space options; 'mainly' allows cabin and rear cameras in multi-camera dashcams.
78|Action camera intended mountable activity recording. Studio view camera, flatbed scanner and telescope not that camera type. Core fact plausible but guessed entry empty; pending actual manufacturer definition and global overlap check before approval.
79|Replaces exact Computers webcam purpose duplicate. Proposed camcorder primary video recording; printed paper output, audio-only recording and temperature measurement not defining task. Pending camcorder definition; do not claim webcam source supports this replacement. Can record sound alongside video, hence audio-only wording.
80|Replaces exact Computers scanner purpose duplicate. Camera flash provides brief light burst; not film, ink or air. Pending photographic flash dictionary sense rather than assuming lightning/computing senses. Proposed fact clear but final source check required.
81|Replaces barcode-reader question that supplied its answer in the name. Linear barcode encodes information in bars/spaces; groove, braille dots and musical notes different systems. Linear qualifier avoids QR/matrix formats. Pending actual GS1 passage before approval.
82|Digital photo frame displays changing photos on screen. Scanner digitises, printer makes prints, hard drive stores rather than displays on its own screen. Pending manufacturer/device-specific definition because guessed dictionary empty.
83|Replaces exact Science temperature/thermometer duplicate. Wire stripper removes insulation, not all conductor, plug pins or metal colour. Pending actual tool definition/manufacturer; no electrical-use instructions given.
84|Digital calipers measure dimensions; radio signal, step counts and battery charge other instruments. Dictionary calipers measuring widths/distances inspected, orthopaedic supports sense excluded. Pending digital caliper product reference because dictionary describes hinged form, not modern sliding electronic variant.
85|Electronic balance reports mass in ordinary calibrated use; direction, resolution and frequency unrelated. Dictionary retrieved mechanical two-pan balance, not electronic device. Pending manufacturer reference; do not treat mechanical definition as verification of electronic mechanism. No assertion balance is independent of gravity calibration.
86|Multimeter commonly measures voltage/current/resistance, not pedometer steps, barometer pressure or anemometer wind. Dedicated electronic-device dictionary explicitly lists all three. No hazardous electrical testing instructions included.
87|Metal detector locates metal. Pressure, heat patterns and smoke detectors use other sensing tasks. Dedicated definition supports metal detection; no guarantee every metal object at any depth detectable. Replaced irrelevant stars/text/audio alternatives.
88|Smoke alarm warns of smoke/possible fire, not carbon dioxide, humidity alone or leakwater. Definition explicitly possible-fire warning, allows false alarms. Single-purpose wording does not deny combination alarm products. Not an installation or safety recommendation.
89|Original CO-alarm/gas stem repeated correct answer directly. Revised gas formula asks to identify correct alarm, distinguish smoke, heat and leak alarms. Pending fire-service reference for CO identity/purpose; guessed dictionary empty. Combination alarms do not make generic smoke alarm alone an equivalent offered answer.
90|Pointer projects light spot; not paper, physical arrow or ink. Dedicated dictionary light beam pointing sense inspected. No use instructions or claim laser pointers safe to look into.
91|Rangefinder measures target distance, not temperature, chemistry or mass. Definition explicitly distance to photographic/shooting target. Electronic qualifier does not assert particular laser/radio/optical implementation.
92|Home weather station monitors local weather, not trains, appliance power or radio transmitter count. Retrieved dictionary defines building/site, insufficient support for gadget version. Pending consumer weather-station manufacturer reference; no claim forecasts are always correct.
93|Replaces exact Science anemometer/wind-speed duplicate. Light meter measures light, not target distance, camera weight or lens temperature. Pending photographic instrument reference and overlap recheck before approval; guessed new dictionary URL not yet fetched.
94|Motion-sensor security light can be triggered by movement. Software update/password change/phone call alone do not describe sensor stimulus. Pending actual security-light sensor manufacturer reference; empty motion-detector dictionary entry not support. Can rather than always avoids guaranteed operation irrespective of light/day settings.
95|Video doorbell adds camera/visitor viewing rather than gas meter, laundry timer or oven thermostat. Generic doorbell definition only establishes conventional bell; pending actual video-doorbell source before approval. Removed unrelated coffee/sewing alternatives.
96|VR presents immersive computer-created environment; physical map, audio-only radio and unmodified binocular optics not VR. Dedicated virtual-reality dictionary images/sounds simulated place inspected. No claim every VR experience must imitate a real location.
97|AR overlays computer-generated information/images on real view. Physical paint, unchanged reflection and audio-only ordinary broadcast not AR imagery. Dedicated dictionary explicitly computer-produced images with real-world view. No claim permanent physical object transformation.
98|Gamepad handheld buttons control video game, unlike boiler/fridge/printer systems as principal purpose. Dedicated gamepad definition inspected. Mainly accommodates accessibility/custom remote-control uses without pretending every possible repurposing impossible.
99|Joystick movable control lever. Battery, flat lens filter and speaker cable not levers. Relevant machine/game sense inspected; no false restriction only aircraft or only one axis.
100|Audio volume adjusts loudness, not screen colour, file count or plug shape. Dedicated sound-level/control sense inspected beyond geometry/book/trade meanings. Distinct technical control from Music dynamics notation; does not conflate volume with pitch.
'''
r['rows']=[x for x in r['rows'] if x['row']<=75]
pending=set(r['pendingReferenceRows'])|{78,79,80,81,82,83,84,85,89,92,93,94,95}
for line in notes.strip().splitlines():
 n,note=line.split('|',1);n=int(n);q=dict(draft[n-1]);q.update(edits.get(n,{}));q['rationale']=note;draft[n-1]=q
 fp=hashlib.sha256(json.dumps({k:q[k] for k in ('prompt','answers','correctIndex','sourceURL')},ensure_ascii=False,sort_keys=True).encode()).hexdigest()
 r['rows'].append({'row':n,'note':note,'status':'pending_specific_reference' if n in pending else 'author_partial_pass_checked','fingerprint':fp})
r.update(checkedRows=100,pendingReferenceRows=sorted(pending),notYetCheckedRows=[],publicationApproved=False,requiresWholeBatchFinalReview=True)
assert [x['row'] for x in r['rows']]==list(range(1,101))
for name,obj in [('draft.json',draft),('partial-review.json',r)]:
 (H/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('100 preliminary judgments saved; 20 specific references and final approval remain; NOT added to bank')
