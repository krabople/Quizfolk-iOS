"""Partial author pass only. This is not the 100-item publication approval."""
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
D='https://dictionary.cambridge.org/dictionary/english/'
edits={
3:{'answers':['Touching the display','Speaking into the microphone','Turning a separate control dial','Moving a mouse on a desk']},
5:{'prompt':'Which phone connection does aeroplane mode normally disable?','answers':['The cellular connection','The wired headphone connection','The USB charging connection','The wired microphone connection'],'sourceURL':'https://support.apple.com/en-la/108785'},
6:{'prompt':"Which iPhone component doubles as its torch?",'answers':['The LED camera flash','The microphone','The vibration motor','The speaker'],'sourceURL':'https://support.apple.com/en-ae/105001'},
8:{'answers':['How much light the screen gives off','How large text appears','How quickly the screen switches off','How loudly notifications sound']},
9:{'prompt':'Which phone accessory is fitted over the display to help prevent scratches?','answers':['A screen protector','A camera lens cap','A charging stand','A magnetic car mount'],'sourceURL':'https://www.belkin.com/uk/support-article/?articleNum=70911'},
10:{'prompt':'What does the screen-rotation lock on an iPhone prevent?','answers':['The display orientation changing when you turn the phone','The screen brightness adjusting automatically','The camera switching between lenses','The volume changing when you press its buttons'],'sourceURL':'https://support.apple.com/guide/iphone/rotate-your-iphone-screen-iph3badf94ec/ios'},
11:{'answers':['Taller than it is wide','Wider than it is tall','Equally wide and tall','Wider at the top than at the bottom']},
12:{'prompt':'Which iPhone camera does Apple recommend using to frame a selfie on the screen?','answers':['The front-facing camera','The rear ultra-wide camera','The rear telephoto camera','An external security camera'],'sourceURL':'https://support.apple.com/en-ca/guide/iphone/iph1b88429a6/ios'},
13:{'prompt':"What does the level shown in an iPhone's battery icon indicate?",'answers':['Its remaining charge','The mobile signal strength','The available storage space','The screen brightness'],'sourceURL':'https://support.apple.com/en-bn/guide/iphone/iph63eecc618/ios'},
14:{'answers':['Milliampere-hour','Megawatt-hour','Millivolt','Megahertz'],'sourceURL':'https://service.anker.com/uk/article-description/Why-is-the-Rated-Capacity-of-Power-Banks-Lower-Than-Expected'},
15:{'answers':['It can have its stored charge replenished','It generates energy without an external supply','Its capacity doubles every time it is used','Its chemical components never age']},
18:{'prompt':'What does a mains-powered USB charger do to supply a phone?','answers':['Converts alternating current to suitable direct current','Converts direct current to mains alternating current','Stores photographs transferred over USB','Increases the capacity of the phone battery'],'sourceURL':'https://www.anker.com/collections/30w-usb-c-power-adapter'},
19:{'answers':['It works without a power lead connected','It can only run while plugged into a wall socket','It receives all its power through a data cable','It needs a cable connected to a transformer throughout use']},
20:{'answers':['Towards zero from a set duration','Upwards from zero without a preset end','Through the current date and year','Through the hours of the current day'],'sourceURL':D+'countdown'},
22:{'answers':['Give a signal to alert you','Measure the time taken by a race','Show how far you have walked','Record changes in air pressure']},
23:{'answers':['Numbers','Rotating hour and minute hands','Moving shadows on a marked dial','Falling sand between two chambers']},
24:{'answers':['A stopwatch','An altimeter','A compass','A heart-rate monitor']},
28:{'answers':['Temperature','Humidity','Air pressure','Light level']},
29:{'answers':['A humidifier','A dehumidifier','An extractor fan','An electric radiator']},
30:{'answers':['A dehumidifier','A humidifier','An electric fan','A room thermostat']},
31:{'prompt':'What is an air filter designed to remove from the air?','answers':['Unwanted particles or harmful substances','All of the oxygen','All of the nitrogen','Every trace of water vapour'],'sourceURL':D+'air-filter'},
32:{'answers':['Remove air from an enclosed space','Measure the air temperature','Add moisture to the air','Heat water for radiators']},
34:{'answers':['Clean floors','Iron clothes','Wash dishes','Dry laundry'],'sourceURL':'https://www.irobot.com/en_US/irobot-braava-jet-m6-robot-mop/M611020.html'},
35:{'prompt':'A robotic mop is primarily designed to clean which surfaces?','answers':['Hard floors','Carpet pile','Upholstered sofas','Hanging curtains'],'sourceURL':'https://www.irobot.com/en_US/explore/us-braava.html'},
42:{'answers':['A whisk','A dough hook','A slicing disc','A mincer attachment']},
44:{'answers':['At a relatively low temperature over several hours','By circulating chilled water around the food','By exposing food to an open flame','By spinning food rapidly without heating it']},
45:{'prompt':'A pressure cooker normally cooks food at a pressure that is what, compared with the surrounding air?','answers':['Higher','Lower','Always identical','Exactly zero']},
46:{'answers':['Hot air','Microwaves','Cold water','An open gas flame']},
}
notes='''1|Portable stored-charge supply identifies a power bank; mouse, webcam and barcode scanner have other main functions. Cambridge explicitly supports portable recharging away from electricity. No claim that a power bank creates energy.
2|Stylus touchscreen writing/drawing sense inspected, distinct from phonograph stylus sense. Cooling, charging and amplification do not describe the tablet stylus. Grammar and tablet context clear.
3|Touching the display defines touchscreen input. Revised alternatives to real input methods rather than rotating a battery. Voice/dial/mouse alone do not define direct touch control.
4|Haptic means relating to touch, not smell, taste or hearing. Vibration can make noise but sensory target remains touch. Specific controller/phone context removes other meanings.
5|Replaced broad all-wireless-radios claim: Apple's guide permits Wi-Fi and Bluetooth and retains settings. Cellular disconnection is the intended usual behaviour; wired audio, USB charging and wired microphones are unaffected as connections. Normally avoids treating every unusual device state as universal.
6|Scoped to iPhone; Apple explicitly identifies LED flash as its flashlight. Microphone, motor and speaker are separate components. No unsupported claim about every phone model.
7|PIN is personal identification number. All alternatives are invented expansions, none standard in device-unlocking context. Cambridge abbreviation sense inspected beyond pin fastener/chess senses.
8|Brightness adjusts emitted light. New alternatives are distinct settings: text size, screen timeout and volume. No confusion with resolution or automatically changing ambient light.
9|Replaces exact Computers screenshot duplicate. Belkin describes a fitted protective layer reducing scratches; not guaranteed unbreakability. Lens cap, stand and mount do not cover the phone display for this purpose.
10|Replaces repeated landscape-orientation fact. Apple guide explicitly says lock prevents orientation changing as phone turns; brightness, camera lens and volume controls are separate. iPhone scope avoids device-specific naming generalisation.
11|Portrait view is taller than wide. Rectangular conventional phone screen context; square and tapered alternatives are false. Distinct from row10 rotation-lock function, though introductory same subject area.
12|Scoped to Apple's iPhone selfie instructions to avoid claiming rear cameras can never take selfies. Front camera recommended; neither specific rear lens nor external security camera matches that recommendation. Correct camera possessive/wording.
13|Apple battery-level icon reflects remaining charge, not radio signal, storage or brightness. Level qualifier distinguishes charging-status lightning symbol. Revised source supports actual icon, not generic battery definition alone.
14|Manufacturer explicitly expands mAh as milliampere-hour and distinguishes charge capacity from usable energy. Megawatt-hour, millivolt and megahertz are genuine other units. No claim mAh itself equals energy or power.
15|Rechargeable means charge can be replenished. Revised false claims are impossible perpetual supply, automatic doubling or no ageing. Reusability does not imply infinite service life.
16|Plus marks positive terminal, negative minus, neutral and earth do not. Fact and wording checked, but retrieved positive dictionary entry covers electrical charge rather than terminal marking. Keep pending supporting manufacturer reference; do not approve this item yet.
17|Mute audio output silences it, unlike speed change, echo or reversed playback. Output scope avoids microphone input mute ambiguity. Cambridge electronic sound-control sense inspected.
18|Replaced vague adaptor wording that could include plug-shape travel adaptors. USB mains charger converts mains AC to appropriate DC; reverse conversion, photo storage and increased battery capacity are false. Anker charger reference explicitly supports direction of conversion.
19|Cordless during operation needs no connected power lead. False options require cables for power. Avoid asserting every cordless appliance necessarily uses a particular battery chemistry.
20|Countdown moves from a preset duration towards zero. Upward stopwatch, calendar and ordinary clock displays are different. Dedicated countdown definition inspected instead of assuming timer generic definition proves direction.
21|Stopwatch measures elapsed time. Pressure, voltage and north direction require other instruments. No claim about timing precision or all devices needing mechanical hands.
22|Alarm preset-time alert is correct. Race duration, distance and pressure are other measurement tasks. Can signal audibly or otherwise; not restricted to ringing bells.
23|Digital clock displays time as numbers; analogue hands, sundial shadows and hourglass sand are different representations. Cambridge digital numbers sense inspected, not fingers/computing senses alone.
24|Chronograph watch provides stopwatch timing. Altimeter, compass and heart-rate monitor are not implied by chronograph, though combined models may add them. Removed repeated 'in every model' wording. Watch scope distinguishes unrelated chronograph speed-measurement devices.
25|Pedometer counts steps, not heartbeats, rain or photos. Cambridge explicit step-counting definition. No assumption every step count is perfectly accurate.
26|Smartwatch normally worn at wrist; eyewear, footwear and lens positions are not normal watch placement. Definition identifies watch; no claim all wearable computers are wrist watches.
27|Fitness tracker principal purpose physical activity. Printer ink, knife sharpness and camera focus unrelated devices. Cambridge includes activity/step counts; heart monitoring does not make all trackers medical instruments.
28|Thermostat regulates temperature by switching heating/cooling, not humidity, pressure or light. Room context avoids engine/system confusion while remaining true. Better same-domain alternatives.
29|Humidifier adds moisture. Dehumidifier removes it; fan circulates air; radiator supplies heat. Cambridge less-dry/add-water definitions support only one intended answer.
30|Dehumidifier removes moisture. Humidifier adds it; fan and thermostat do not have removal as intended purpose. Excess moisture wording allows ordinary indoor use without health claims.
31|Replaced unsupported air-purifier source with inspected air-filter definition. Filter removes unwanted particles/harmful substances, not all oxygen/nitrogen/water. No claim perfect removal of every pollutant or health outcome.
32|Extractor fan removes enclosed-space air; temperature measurement, moisture addition and radiator-water heating are different functions. Cambridge dust/smell removal description supports extraction purpose. No claim it is identical to an air-purifying recirculator.
33|Rotating blades move air in ordinary electric fan; casing, label and lettering do not. Relevant electric fan dictionary sense inspected rather than sports supporter. Typical qualifier allows bladeless-design exceptions.
34|Robot vacuum floor cleaning, not ironing, dishwashing or laundry drying. iRobot indexed product text explicitly describes automatic vacuum/mop floor-clean sequence. This is indexed corroboration, not claimed full-page direct retrieval.
35|iRobot describes robot mop for hard-surface floors; carpet pile, upholstered sofas and curtains are not its intended mopping surfaces. Narrowed generic floors to avoid carpet implication. Indexed manufacturer passage corroboration, not generic mop definition alone.
36|Electric kettle boils water for drinks. Grinder breaks beans; toaster browns bread; juicer extracts juice. Cambridge vessel-for-boiling-water sense checked, not police kettling sense.
37|Toaster browns bread by heat. Blender processes ingredients, fridge chills, processor chops. Dictionary 'making toast' plus ordinary toast meaning establishes one correct offered answer; no claim bread must be sliced in all possible uses.
38|Blender high-speed blades make smoothies. Toaster, kettle and slow cooker lack this food-blending function. Dedicated electrical kitchen-machine sense inspected, not professional blender of wine/perfume.
39|Juicer extracts fruit/vegetable juice. Grinder, toaster and whisk have other principal tasks. Cambridge explicit extraction definition, with no assertion every juicer handles every vegetable.
40|Coffee grinder crushes beans before brewing. Frother aerates milk; kettle boils water; toaster browns bread. Smaller particles allows coarse/fine grounds rather than requiring powder-fine output.
41|Milk frother creates milk foam. Ice, ground coffee and bread slices are distinct products; none describe aeration. Cambridge frothy-air-bubbles definition checked.
42|Whisk beats eggs/whips cream; dough hook, slicing disc and mincer have different intended actions. Removed 'only' from dough-hook alternative. Kitchen noun/verb senses inspected, not rapid transport idiom.
43|Food processor chops/processes ingredients. Dishwasher, freezer and kettle tasks do not define a food processor. Commonly qualifier accommodates additional processing functions and optional accessories.
44|Slow cooker low-temperature long-duration cooking supported explicitly by dictionary. Chilled water, open flame and unheated spinning are other/false processes. No specific unsafe temperature or cooking-time advice offered.
45|Pressure cooker operates above surrounding atmospheric pressure; lower, identical and zero are wrong under normal pressure-cooking operation. Added explicit comparison so raised pressure has a clear baseline. No claim sealing alone creates a vacuum.
46|Air fryer circulates hot air, not microwaves, cold water or open gas flame. Definition explicitly hot air. Does not claim every recipe needs no oil or guarantees particular health results.
47|Defrost thaws frozen food, not freezes, grinds or toasts. Appliance setting context removes windscreen defogging meaning. No food-storage or safe-thawing instructions implied.
48|Dishwasher washes plates/cups/cutlery. Dryer, processor and freezer main functions differ. Appliance qualifier avoids human dishwasher occupation. Dedicated machine definition inspected.
49|Washing machine washes fabric using water/detergent and movement. Dryer/fridge/air purifier are other appliances. Cambridge clothes/cloth definition supports core task, no universal claim about all wash cycles needing detergent.
50|Tumble dryer dries laundry in rotating drum; dishwasher, freezer and processor do not. Definition explicitly dries wet clothes by turning in hot air. No claim every clothes dryer tumbles or uses identical heating technology.
'''
out=[]
for line in notes.strip().splitlines():
 n,note=line.split('|',1);n=int(n)
 q=dict(draft[n-1]);q.update(edits.get(n,{}));q['rationale']=note
 # Leave all rows as drafts until the entire batch has its final publication pass.
 draft[n-1]=q
 fingerprint=hashlib.sha256(json.dumps({k:q[k] for k in ('prompt','answers','correctIndex','sourceURL')},ensure_ascii=False,sort_keys=True).encode()).hexdigest()
 out.append({'row':n,'note':note,'status':'pending_specific_reference' if n==16 else 'author_partial_pass_checked','fingerprint':fingerprint})
assert [x['row'] for x in out]==list(range(1,51))
(HERE/'draft.json').write_text(json.dumps(draft,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
(HERE/'partial-review.json').write_text(json.dumps({'independent':False,'status':'PARTIAL_ONLY_NOT_PUBLICATION_APPROVAL','checkedRows':50,'pendingReferenceRows':[16],'notYetCheckedRows':list(range(51,101)),'rows':out},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('50 explicit partial-pass judgments saved; row16 reference pending; no publication approval')
