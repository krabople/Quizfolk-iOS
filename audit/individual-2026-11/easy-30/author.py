"""Everyday gadget candidates. These remain unapproved pending individual review."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
rows='''1|power-bank|Which portable device stores charge so you can recharge a phone away from a socket?|A power bank|A wireless mouse|A webcam|A barcode scanner
2|stylus|What is a stylus used for with a tablet?|Writing or drawing on its screen|Cooling its processor|Charging its battery|Amplifying its speakers
3|touchscreen|What lets you control a touchscreen device directly?|Touching the display|Turning the power cable|Covering the speaker|Rotating the battery
4|haptic|In a phone or game controller, haptic feedback mainly relates to which sense?|Touch|Smell|Taste|Hearing
5|airplane-mode|What is aeroplane mode on a phone designed to switch off initially?|Wireless radio connections|The screen's ability to show text|All stored photographs|The clock's ability to keep time
6|torch|A phone's torch feature normally uses which built-in component?|An LED light|Its microphone|Its vibration motor|Its speaker
7|pin|What does PIN stand for when unlocking an electronic device?|Personal Identification Number|Portable Internet Network|Private Image Name|Power Input Notification
8|brightness|What changes when you adjust a phone screen's brightness?|How much light the screen gives off|The number of apps installed|The phone's physical weight|The amount of storage built into it
9|screenshot|What is a screenshot?|An image of what is shown on a screen|A recording of every nearby sound|A printed list of phone contacts only|A new physical camera lens
10|landscape|In landscape orientation, a device's screen is generally what shape relative to the viewer?|Wider than it is tall|Taller than it is wide|Always circular|Always square
11|portrait|In portrait orientation, a phone's screen is generally what shape relative to the viewer?|Taller than it is wide|Wider than it is tall|Always circular|Always triangular
12|selfie|Which phone camera is usually the most convenient for framing a selfie while watching the screen?|The front-facing camera|The rear-facing camera|An external security camera|A camera facing the charging socket
13|battery|What does a phone's battery indicator mainly show?|Its remaining charge|The strength of the microphone|The number of saved photos|The screen's pixel count
14|milliampere-hour|The battery-capacity abbreviation mAh stands for what?|Milliampere-hour|Megawatt-hour|Metres above height|Millimetres at heat
15|rechargeable|What makes a rechargeable battery reusable after it runs down?|It can have its stored charge replenished|Its printed label changes colour permanently|It produces new metal inside indefinitely|It never needs energy from elsewhere
16|positive|A plus sign on a battery marks which terminal?|Positive|Negative|Neutral|Earth only
17|mute|What does a mute control normally do to audio output?|Silences it|Makes it twice as fast|Adds an echo|Reverses the recording
18|adaptor|What does a mains power adaptor commonly do for a small electronic device?|Converts the supply to a form the device can use|Adds more storage space|Changes the device's colour|Increases the number of camera lenses
19|cordless|What is a key feature of a cordless appliance during normal use?|It works without a power lead connected|It cannot contain a battery|It has no moving parts|It must be plugged into two sockets
20|timer|A countdown timer measures time in which direction?|Towards zero from a set duration|Only forwards from midnight|Only backwards from the current year|In circles without changing numbers
21|stopwatch|What is a stopwatch mainly used to measure?|Elapsed time|Air pressure|Electrical voltage|The direction of north
22|alarm-clock|What is an alarm clock designed to do at a chosen time?|Give a signal to alert you|Automatically change your address|Measure the humidity|Count the day's footsteps
23|digital|A digital clock commonly displays time in what form?|Numbers|Only rotating hands|Only compass directions|Only coloured dots with no numerical display
24|chronograph|What extra function does a chronograph watch provide?|A stopwatch|A compass in every model|A blood-pressure reading in every model|A built-in projector in every model
25|pedometer|What does a pedometer count?|Steps|Heartbeats|Raindrops|Photographs
26|smartwatch|Where is a smartwatch normally worn?|On the wrist|Over the eyes|Inside the shoe|Around the camera lens
27|fitness-tracker|What is a fitness tracker principally designed to monitor?|Physical activity|The ink level in a printer|The sharpness of a kitchen knife|The focus of a camera lens
28|thermostat|What does a room thermostat help regulate?|Temperature|The number of lights in the room|The size of the windows|The colour of the wallpaper
29|humidifier|Which device adds moisture to indoor air?|A humidifier|A dehumidifier|A paper shredder|A coffee grinder
30|dehumidifier|Which device removes excess moisture from indoor air?|A dehumidifier|A humidifier|A toaster|An electric whisk
31|air-purifier|What is an air purifier designed to reduce?|Unwanted particles or pollutants in indoor air|The number of electrical sockets|The room's floor area|The length of curtains
32|extractor-fan|What is an extractor fan mainly intended to do?|Remove air from an enclosed space|Print labels|Charge a phone|Record television programmes
33|fan|Which part of a typical electric fan moves the air?|The rotating blades|The plug's plastic casing|The printed instruction label|The power button's lettering
34|robot-vacuum|What job is a robot vacuum cleaner designed to do automatically?|Clean floors|Prepare coffee|Iron shirts|Water every garden plant
35|mop|A robotic mop is primarily designed to clean which surfaces?|Floors|Camera lenses|Computer processors|The inside of a kettle
36|kettle|Which appliance is primarily designed to boil water for hot drinks?|An electric kettle|A coffee grinder|A toaster|A juicer
37|toaster|Which appliance browns slices of bread using heat?|A toaster|A blender|A fridge|A food processor
38|blender|Which appliance commonly uses fast-spinning blades to blend ingredients into a smoothie?|A blender|A toaster|An electric kettle|A slow cooker
39|juicer|Which kitchen appliance extracts juice from fruit or vegetables?|A juicer|A coffee grinder|A toaster|An electric whisk
40|coffee-grinder|Which device breaks coffee beans into smaller particles before brewing?|A coffee grinder|A milk frother|An electric kettle|A toaster
41|frother|What is a milk frother designed to create?|Foam in milk|Ice cubes|Ground coffee|Slices of bread
42|whisk|Which attachment is commonly used with an electric mixer to beat eggs or whip cream?|A whisk|A dough hook only|A slicing disc|A can opener
43|food-processor|A food processor is commonly used for which kitchen task?|Chopping or processing ingredients|Washing the plates|Keeping food frozen|Boiling drinking water
44|slow-cooker|How does a slow cooker generally cook food?|At a relatively low temperature over several hours|By freezing it rapidly|Only with ultraviolet light|Without any source of heat
45|pressure-cooker|A pressure cooker cooks food inside a vessel with what condition?|Raised pressure|A complete vacuum|No lid|Only cold air
46|air-fryer|What does an air fryer circulate to cook food?|Hot air|Ice-cold water|Liquid nitrogen|Only steam from an open pan
47|defrost|What is a kitchen appliance's defrost setting intended to do?|Thaw frozen food|Freeze fresh food more quickly|Grind dry ingredients|Toast bread until brown
48|dishwasher|Which appliance is designed to wash plates, cups and cutlery?|A dishwasher|A tumble dryer|A food processor|A freezer
49|washing-machine|Which appliance washes clothes by moving them with water and detergent?|A washing machine|A tumble dryer|A fridge|An air purifier
50|tumble-dryer|Which appliance dries laundry by tumbling it in a rotating drum?|A tumble dryer|A dishwasher|A freezer|A food processor
51|iron|What is a clothes iron mainly used to remove from fabric?|Creases|All of its colour|The fabric's fibres|Its buttons automatically
52|steamer|A garment steamer uses what to help relax creases in clothes?|Steam|Sand|Dry ice|Ink
53|hairdryer|Which grooming appliance uses a stream of air to dry wet hair?|A hairdryer|Hair clippers|An electric shaver|A curling tong without a fan
54|clippers|What are electric hair clippers primarily used for?|Cutting hair|Drying hair with warm air|Straightening hair with heated plates|Dyeing hair automatically
55|hair-straightener|Hair straighteners commonly press hair between what?|Heated plates|Frozen rollers|Rotating saw blades|Water-filled balloons
56|electric-shaver|What is an electric shaver mainly designed to cut?|Hair near the skin|Paper|Wood|Fabric seams
57|sewing-machine|Which appliance forms stitches to join pieces of fabric?|A sewing machine|A steam iron|A tumble dryer|A clothes steamer
58|electric-blanket|What does an electric blanket provide when switched on?|Heat|Refrigeration|Extra oxygen|Automatic washing
59|heater|What is a portable electric room heater designed to produce?|Heat|Ice|Printed pages|Camera images
60|heating-pad|A reusable electric heating pad is mainly designed to provide what?|Localised warmth|A cooled storage compartment|A stronger radio signal|A printed photograph
61|headphones|Which audio device is normally worn over or on the ears for personal listening?|Headphones|A soundbar|A projector|A webcam
62|earbud|What are earbuds?|Small earphones worn in or near the ear canal|Large television screens|Camera supports|Printer ink containers
63|loudspeaker|What is a loudspeaker designed to produce from an audio signal?|Sound|A printed picture|A magnetic compass direction|An electrical measurement report
64|soundbar|What is a soundbar?|A long speaker unit often used with a television|A camera lens|A phone's charging cable|A type of computer memory card
65|bluetooth-speaker|A portable Bluetooth speaker receives audio from a compatible phone mainly through what?|A short-range wireless link|A paper cable|A film cartridge|A mechanical clock spring
66|microphone|Which device captures spoken sound for a call or recording?|A microphone|A projector|A monitor|A printer
67|voice-recorder|Which portable device is specifically designed to save spoken audio notes?|A voice recorder|A laser pointer|A photo frame|A barcode scanner
68|megaphone|What is a megaphone designed to help a person's voice do?|Carry more loudly over a distance|Become a written page automatically|Turn into a photograph|Stop making any sound
69|walkie-talkie|What is a walkie-talkie?|A portable two-way radio|A digital photo frame|A cordless vacuum cleaner|An electronic kitchen scale
70|baby-monitor|What is a baby monitor designed to help a carer do?|Hear or watch a baby from another room|Count the house's electrical sockets|Cool milk automatically|Wash baby clothes
71|projector|Which device displays a large image onto a separate wall or screen?|A projector|A webcam|A microphone|A barcode reader
72|binoculars|What does the central focusing wheel on many binoculars adjust?|How sharply the subject appears|The printed magnification number|The actual distance to the subject|The outside colour of the binoculars
73|tripod|Which camera support normally has three legs?|A tripod|A monopod|A selfie stick|A gimbal handle alone
74|monopod|How many supporting legs does a standard camera monopod have?|One|Two|Three|Four
75|selfie-stick|What does a selfie stick let a photographer do?|Hold a phone or camera farther away for a self-portrait|Increase the camera's sensor size|Print the photograph instantly by itself|Replace the battery automatically
76|gimbal|What is a camera gimbal designed to help reduce?|Unwanted camera movement|The number of pixels in the sensor|The amount of storage in a memory card|The number of lenses owned
77|dashcam|What is a dashcam mainly used to record?|The view from a vehicle while driving|Only underwater wildlife|Only the inside of a printer|Only distant stars
78|action-camera|Which type of camera is especially designed for recording activities while mounted on a helmet or equipment?|An action camera|A large studio view camera|A flatbed scanner|A document photocopier
79|webcam|Which type of camera is commonly used to send live video during an online call?|A webcam|A film-only disposable camera|A speed camera|A photographic enlarger
80|scanner|What does a document scanner create from a paper page?|A digital image|An audio-only song|A new sheet of blank paper only|A physical camera lens
81|barcode-reader|What information pattern is a barcode reader designed to scan?|A barcode|Only a handwritten signature|Only a person's fingerprints|Only the compass needle
82|digital-photo-frame|Which device can display a changing selection of photographs on its own screen while sitting on a shelf?|A digital photo frame|A microphone|A barcode scanner|A keyboard
83|thermometer|Which quantity does a digital thermometer measure?|Temperature|Wind direction|Electrical resistance|Sound volume
84|calipers|What are digital calipers commonly used to measure?|An object's dimensions|The strength of a radio station|The number of footsteps in a day|The amount of charge in a phone
85|balance|An electronic weighing balance is designed to measure what?|Mass|Compass direction|Screen resolution|Sound frequency
86|multimeter|Which instrument can commonly measure voltage, current and resistance?|A multimeter|A pedometer|A barometer|An anemometer
87|metal-detector|What is a metal detector designed to locate?|Metal objects|Only stars|Only printed text|Only sound recordings
88|smoke-detector|What is a smoke alarm designed to warn about?|Smoke that may indicate a fire|Low printer ink|A missed phone call|A camera's empty memory card
89|carbon-monoxide-detector|Which gas is a carbon monoxide alarm designed to detect?|Carbon monoxide|Nitrogen|Helium|Water vapour
90|laser-pointer|What does a laser pointer project to indicate something at a distance?|A small spot of light|A printed paper arrow|A stream of liquid ink|A physical ruler
91|rangefinder|What is an electronic rangefinder designed to measure?|Distance to a target|The target's name|The current time in every country|The amount of ink in a pen
92|weather-station|A home weather station usually monitors what?|Local weather conditions|The progress of every train|The size of a television audience|The contents of a fridge
93|anemometer|Which weather measurement is an anemometer used for?|Wind speed|Air temperature|Rainwater acidity|Cloud colour
94|motion-detector|What does a motion sensor detect?|Movement|Only the time of day|Only printer paper size|Only the colour of a cable
95|doorbell|A video doorbell adds which feature to a traditional ringing doorbell?|A camera to show visitors|A coffee grinder|A sewing needle|A camera-free printer
96|virtual-reality|What is a virtual-reality headset designed to present?|An immersive computer-generated environment|Only a printed paper timetable|Only an ordinary radio programme|A physical view through binocular lenses alone
97|augmented-reality|What does augmented reality add to a view of the real world?|Digital information or images|Only louder sound from a radio|Only a paper map placed in a drawer|A permanent physical change to every object
98|gamepad|What is a gamepad mainly used to control?|A video game|A household water supply|A fridge's coolant|A printer's ink chemistry
99|joystick|What is a joystick?|A movable lever used to control a device or game|A type of rechargeable battery|A flat camera filter|A speaker cable
100|volume|What does an audio volume control adjust?|How loud or quiet the sound is|The colour of the screen|The number of stored files|The shape of the plug
'''
if __name__=='__main__':
 out=[]
 for line in rows.strip().splitlines():
  n,key,prompt,*answers=line.split('|');assert int(n)==len(out)+1 and len(answers)==4
  out.append({'draftID':f'easy-30-{int(n):03d}','categoryID':'30','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'rationale':'Awaiting individual final check of wording, category, each option and supporting reference.','sourceURL':'https://dictionary.cambridge.org/dictionary/english/'+key,'reviewStatus':'draft_awaiting_author_final_check'})
 assert len(out)==100
 (HERE/'draft.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('100 unapproved Gadgets candidates')
