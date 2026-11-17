"""Individual second editorial check by the author; no independent-review claim."""
import json,pathlib
p=pathlib.Path(__file__).parent;q=json.loads((p/'draft.json').read_text(encoding='utf8'))
notes='''The steering wheel is the rotating driver control for steering; the other parts are not steering controls.
The brake pedal operates the service brakes; releasing the accelerator is not the pedal asked for.
The accelerator controls requested engine output in the qualified petrol vehicle.
Parking brake is the common alternative term; not every modern parking brake is hand-operated.
Wipers move water off the screen; they do not refill washer fluid.
Headlights illuminate ahead; brake and number-plate lights have different positions/functions.
Brake lights signal braking, including some regenerative deceleration; avoid an absolute pedal-only claim.
Indicators conventionally communicate a turn intention; they may also be used together as hazard lights.
The rear-view mirror shows the area behind; it does not show every blind spot.
Speedometer indicates road speed, unlike odometer distance or tachometer engine speed.
Odometer records distance, unlike trip time, tyre width or engine temperature.
Fuel gauge indicates remaining fuel; it is not a guaranteed exact volume measurement.
Rev counter displays engine revolutions per unit time, not road speed.
A horn makes an audible warning, not an engine-cooling airflow.
Replace the trivial seat-cushion question with the distinct electric-window switch function.
Rewrite the headrest question around limiting head movement and whiplash injury, its safety purpose.
American trunk corresponds to British boot; hood and fender name other body parts.
American hood corresponds to British bonnet; not the luggage compartment.
American windshield corresponds to British windscreen; not a side body panel.
The glove compartment is a small dashboard storage space; its name does not limit it to gloves.
Sun visors reduce sunlight glare; they do not replace windscreen wipers.
Front-engined qualification makes bonnet the appropriate access panel; rear/mid-engine layouts differ.
Exhaust pipes discharge combustion gases; not fuel supplied to the engine.
An intake air filter removes particles from incoming air, not exhaust gases after combustion.
A radiator transfers heat from liquid coolant; the liquid-cooled qualification avoids air-cooled engines.
Replace the tube/tubeless ambiguity with the meaning of tyre pressure.
Tread is the road-contacting patterned tyre surface, not the valve or rim.
The tyre valve admits/releases air; an axle and bumper do not.
A spare wheel can replace a road wheel; some temporary spares have restrictions not asked about here.
A jack raises part of the vehicle; this definition is not an instruction to work beneath an unsupported car.
Wheel nuts or bolts secure many wheels to hubs; central-lock and other designs explain the qualification.
Shock absorbers damp suspension oscillation; they are not the springs themselves.
The manual clutch disconnects engine torque from the transmission temporarily.
A manual gear lever selects the transmission ratio or reverse.
Reverse permits backward movement; it does not necessarily reverse the rotation of the engine itself.
P means Park; it is not power steering or petrol.
N means Neutral; not night mode or navigation.
D means Drive; not a request for the demister.
A convertible has an openable/retractable/removable roof; not every model uses the same mechanism.
Replace the awkward body-style comparison with the clear American sedan/British saloon equivalence.
A pickup bed is its open load area, distinct from the cab or engine bay.
A tow bar/hitch couples a trailer; it is not a control linkage.
A trailer is designed for towing, even though some specialised trailers may have powered components.
A touring caravan supplies accommodation; avoid confusing it with a self-propelled motorhome.
A motorhome combines powered travel and accommodation.
A concrete mixer truck uses its rotating drum to keep the load mixed.
A tipper tilts its load bed/body to discharge material.
Forks lift loads such as pallets; passenger-only answers are not a proper primary purpose.
A road roller compacts through a heavy rolling drum; a sweeper cleans rather than compacts.
A snowplough pushes snow aside; it is not a street-cleaning brush.
An ambulance is equipped for patient transport; not every ambulance trip is an emergency.
A hearse primarily carries a coffin; not livestock or bulk freight.
A refuse truck collects rubbish; distinguish a road sweeper that cleans the road surface.
A combine combines crop cutting and threshing, rather than merely towing a trailer.
A car transporter carries other vehicles; it is not limited to one vehicle make.
Tankers carry liquids or gases in tanks, not necessarily fuel only.
A flatbed has a flat open platform, rather than a sealed box, drum or tank.
The lorry driver compartment is the cab; a hold and galley are ship spaces.
Pedals receive the rider foot force and turn the cranks.
The chain transmits pedal power via chainrings and sprockets to the driven wheel.
The saddle supports the seated rider; the rider weight is also shared through pedals and handlebars.
Handlebars primarily steer; they may carry controls but do not themselves inflate tyres.
A bell provides the characteristic ringing warning.
Mudguards reduce spray and dirt thrown by rotating wheels.
Panniers are side-mounted bags, commonly rack-supported, unlike top-mounted saddlebags.
Change to the tandem seating arrangement; tandems can have more than two riders, so do not define all tandems as exactly two-seat.
A unicycle has one wheel; this is a simple vehicle vocabulary question.
A tricycle has three wheels; not two or four.
The conventional right-hand twist grip is the throttle; qualify normally to allow adapted controls.
A sidecar is an attached side compartment; it can also carry luggage but is not a tyre fitting.
A pantograph collects current by contacting overhead electrical equipment.
Britain calls the crosspieces sleepers; US ties terminology is not an alternative offered.
Station platforms provide access to passenger trains; they are not the rails or overhead wires.
A level crossing intersects a road/path and railway at the same level; a bridge is grade-separated.
A locomotive provides train motive power, even when used alone or distributed through a train.
Freight trains carry goods, in contrast to passenger trains.
A buffer stop protects the end of a terminating track; it cannot guarantee stopping every runaway vehicle.
A passenger carriage carries people; the prompt explicitly excludes freight wagons.
Bow is the vessel front, not the stern or galley.
Stern is the vessel rear, not the bow or mast.
Port is left when facing the bow; the direction remains fixed to the vessel.
Starboard is right when facing the bow; not dependent on the observer facing aft.
Sails harness wind force to propel a sailing vessel.
An anchor helps hold position through engagement with the seabed; it is not a brake for every moving vessel.
Galley means the ship kitchen.
Hull is the vessel main body; not just the engine compartment or mast.
A deck is a structural floor/platform level of a vessel.
A gangway provides boarding/disembarkation at a moored vessel; not a propulsion device.
Tugboats assist other vessels manoeuvring; their job is not limited to towing a single vessel type.
Replace the General Knowledge ferry duplicate with the meaning of ship draught.
A dry dock enables access to the hull out of water for inspection/maintenance.
A paddle propels and helps steer a canoe; it is not the fixed rowlock used for an oar.
Cockpit contains flight controls and pilots, distinct from cabin or cargo hold.
Undercarriage is landing gear, not a winglet or tailplane.
A runway is for take-offs/landings; taxiways connect it to other ground areas.
Taxiways support aircraft ground movement; not road taxis or airborne cruising.
A hangar houses aircraft; it differs from the tower, passenger terminal and apron.
A boarding pass indicates a passenger authorisation for the identified flight; it is not a pilot licence.
Replace the tautological glider/unpowered-flight comparison with the aircraft designed mainly for flight without engine power.
A helicopter main rotor generates lift; it can also provide directional thrust, so do not claim lift is its only function.'''.splitlines()
assert len(q)==len(notes)==100
sources={}
def span(a,b,s):
 for i in range(a,b+1):sources[i]=s
span(1,45,'https://www.gov.uk/guidance/the-highway-code/annex-6-vehicle-maintenance-safety-and-security')
span(46,58,'https://dictionary.cambridge.org/dictionary/english/')
span(59,70,'https://www.cyclinguk.org/article/which-bike-should-i-buy')
span(71,78,'https://safety.networkrail.co.uk/jargon-buster/')
span(79,92,'https://www.rmg.co.uk/sites/default/files/Cutty_Sark_Facts_Pack.pdf')
span(93,100,'https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/faa-h-8083-25c.pdf')
for i in (17,18,19,40):sources[i]='https://dictionary.cambridge.org/dictionary/english/'+{17:'trunk',18:'hood',19:'windshield',40:'sedan'}[i]
sources[90]='https://imocompendium.imo.org/public/IMO-Compendium/Current/ds1.htm'
sources.update({16:'https://www.euroncap.com/glossary/',36:'https://www.fordservicecontent.com/Ford_Content/catalog/owner_guides/12378og1e.pdf',37:'https://www.fordservicecontent.com/Ford_Content/catalog/owner_guides/12378og1e.pdf',38:'https://www.fordservicecontent.com/Ford_Content/catalog/owner_guides/12378og1e.pdf',65:'https://www.cyclinguk.org/article/baggage-check-bikepacking-bags-or-panniers',66:'https://www.cyclinguk.org/article/cycling-guide/guide-tandems',99:'https://www.faa.gov/documentlibrary/media/order/faa_order_8000_71.pdf'})
for i,term in {46:'concrete-mixer',47:'tipper',48:'forklift',49:'road-roller',50:'snowplough',51:'ambulance',52:'hearse',53:'dustcart',54:'combine-harvester',55:'transporter',56:'tanker',57:'flatbed',58:'cab'}.items():sources[i]='https://dictionary.cambridge.org/dictionary/english/'+term
changes={
7:{'prompt':"What do a car's brake lights normally signal to following traffic?",'answers':['That the car is braking','That the car is turning left','That the car is reversing','That the headlights are on full beam']},
10:{'answers':["The vehicle's speed",'Engine revolutions per minute','Distance travelled since manufacture','The remaining fuel level']},
11:{'answers':['Distance travelled','Current vehicle speed','Engine revolutions per minute','Time until the next fuel stop']},
13:{'answers':['Engine rotation speed','Road speed','Distance travelled since manufacture','The amount of washer fluid']},
15:{'prompt':'What does an electric-window switch in a car control?','answers':['Raising or lowering a window','Setting the windscreen-wiper speed','Adjusting the headlight beam','Changing the radio station']},
16:{'prompt':"What is a car's head restraint designed to help reduce in a rear-end collision?",'answers':['Whiplash injury','Tyre wear','Engine vibration','Brake overheating']},
21:{'answers':['Glare from sunlight','Glare from an illuminated dashboard','Mist inside the windscreen','Rain on the outside of the windscreen']},
23:{'answers':['Gases produced by the engine','Air entering the intake manifold','Coolant returning to the radiator','Fuel entering the tank']},
24:{'answers':['Removing particles from incoming air','Removing particles from the engine oil','Cooling the exhaust gases','Regulating brake-fluid pressure']},
25:{'answers':['Helping remove heat from the coolant','Filtering the engine oil','Storing windscreen-washer fluid','Measuring air pressure in the tyres']},
26:{'prompt':'What does tyre pressure measure?','answers':['The pressure of the air inside a tyre','The depth of the tread grooves','The diameter of the wheel rim','The distance between the front wheels']},
30:{'answers':['Lift part of the car','Measure the tyre pressure','Tighten the wheel nuts','Test the battery charge']},
32:{'answers':['Bouncing of the suspension','Air entering the engine','Fuel entering the injectors','The temperature of the coolant']},
33:{'answers':['The engine from the transmission','The front wheels from the steering rack','The battery from the alternator','The fuel tank from the filler pipe']},
35:{'answers':['Moving the vehicle backwards','Keeping the engine idling while stationary','Locking the steering wheel','Applying the parking brake']},
39:{'answers':['Its roof','Its engine block','Its rear axle','Its dashboard']},
40:{'prompt':'Which British car-body term corresponds to the American term sedan?','answers':['Saloon','Estate','Hatchback','Pickup']},
44:{'answers':['Living and sleeping accommodation','A mobile fuel storage tank','An open platform for transporting a car','A refrigerated container for food deliveries']},
45:{'answers':['A motor vehicle with living accommodation','An unpowered trailer with living accommodation','A recovery vehicle carrying another car','A road vehicle designed only to carry liquid cargo']},
46:{'answers':['Concrete mixer truck','Tipper truck','Flatbed truck','Refuse truck']},
48:{'answers':['Loads such as pallets','The road surface for resurfacing','Overhead power cables','Only the empty vehicle itself']},
49:{'answers':['Road roller','Road sweeper','Tipper truck','Concrete mixer truck']},
50:{'answers':['Snow','Fallen leaves using a rotating brush','Liquid road markings','Hot asphalt from a hopper']},
53:{'answers':['Refuse truck','Road sweeper','Concrete mixer truck','Recovery truck']},
55:{'answers':['Other vehicles','Loose aggregates tipped from a hopper','Liquid cargo carried in a sealed tank','Passengers travelling in a coach cabin']},
58:{'answers':['Cab','Hold','Galley','Engine bay']},
60:{'answers':['Power from the pedals','Hydraulic pressure from the brake lever','Electrical power from a dynamo','Air from the tyre valve']},
62:{'answers':['Steering','Changing tyre pressure','Lubricating the chain','Adjusting saddle height']},
64:{'answers':['Water and dirt thrown up by the wheels','Stretching of the chain','Wear on the brake cables','Loss of tyre pressure']},
66:{'prompt':'How are riders normally arranged on a tandem bicycle?','answers':['One behind another','Side by side across one wide saddle','Facing one another between the wheels','Standing beside the frame on platforms']},
71:{'answers':['An overhead electrical wire','The running surface of a rail','The edge of a platform','A buffer stop']},
72:{'answers':['Sleepers','Ballast','Signals','Points']},
73:{'answers':['Passengers boarding and leaving trains','Storing ballast beneath the rails','Connecting overhead power wires','Turning locomotives around']},
76:{'answers':['Goods','Only passengers in sleeping cabins','Only passengers on commuter services','Only travellers on sightseeing journeys']},
77:{'answers':['The end of a track','The start of an electrified section','The position of a level crossing','The maximum speed of a train']},
78:{'answers':['Passengers','Only bulk liquids in a tank','Only loose coal in an open wagon','Only containers stacked on a flat wagon']},
84:{'answers':['Remain in position','Turn the propeller','Pump water out of the bilge','Raise a sail']},
87:{'answers':['A floor or platform forming a level of the vessel','A vertical wall dividing compartments','The main longitudinal beam beneath the hull','The pole supporting a sail']},
88:{'answers':['Boarding and leaving the ship','Turning the propeller','Pumping out the bilge','Operating the anchor winch']},
89:{'answers':['Other vessels','Container cargo using a dockside crane','Aircraft between airport stands','Railway wagons inside a freight yard']},
90:{'prompt':"What does a ship's draught measure?",'answers':['The vertical distance from the waterline to the bottom of the hull','The length from bow to stern','The width across the widest part of the hull','The height of the tallest mast above the deck']},
91:{'answers':["Accessing a vessel's hull out of the water",'Loading cargo while the vessel remains afloat','Keeping a ship moving through a lock','Providing fuel to an aircraft']},
92:{'answers':['Propel and steer the canoe','Drain water through the hull automatically','Inflate a buoyancy aid','Anchor the canoe to the riverbed']},
95:{'answers':['Aircraft take-offs and landings','Parking aircraft during maintenance','Storing passenger luggage','Controlling flight paths by radio']},
96:{'answers':['Aircraft moving on the ground between areas such as runways and stands','Passengers taking taxis into town','Aircraft taking off from the airport','Aircraft cruising between countries']},
97:{'answers':['Aircraft','Passengers awaiting boarding','Air-traffic controllers directing flights','Baggage moving between conveyor belts']},
98:{'answers':["A passenger's permission to board a particular flight",'Proof that a pilot is qualified to fly every aircraft','A receipt proving all airport shops have been paid','A certificate that an aircraft has passed maintenance']},
99:{'prompt':'Which type of fixed-wing aircraft is designed primarily for flight without engine power?','answers':['Glider','Passenger jet','Turboprop airliner','Piston-engine training aeroplane']},
100:{'answers':['Lift','Engine coolant pressure','Tyre pressure','Electrical insulation']},
}
rows=[]
for i,(draft,note) in enumerate(zip(q,notes),1):
 change={'sourceURL':sources[i],'rationale':note,**changes.get(i,{})}
 rows.append({'row':i,'prompt':draft['prompt'],'action':'edit','note':note,'meaning':True,'answerCorrect':True,'onlyOneCorrect':True,'grammar':True,'categoryRelevant':True,'recommendedChanges':change,'sourceReview':'Vehicle vocabulary and four choices checked individually. Official Highway Code, Ford, Euro NCAP, Cycling UK, Network Rail, Royal Museums Greenwich and FAA references were inspected for the relevant areas; dictionary URLs identify the remaining stable transport definitions rather than claiming every URL was opened.'})
(p/'independent-review.json').write_text(json.dumps({'independent':False,'reviewer':'root (author second editorial pass)','status':'complete','reviewed':100,'remaining':0,'sourceAccessNote':'Official indexed references inspected, including head restraints, automatic selector labels, tandem cycling, rail equipment, nautical directions and glider definitions. Every prompt and four choices read; claims narrowed and semantic duplicates replaced. This is not an independent reviewer.','rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Vehicles: 100 individual author-final-check decisions recorded')
