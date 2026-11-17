"""Unpublished everyday transport vocabulary; requires independent source review."""
import json
from pathlib import Path
data='''Which part of a car is turned by the driver to steer it?|Steering wheel|Exhaust pipe|Fuel cap|Seat belt
Which car pedal is used to slow the vehicle in ordinary driving?|Brake pedal|Accelerator pedal|Clutch pedal|Footrest
Which pedal increases engine power when pressed in a conventional petrol car?|Accelerator|Clutch|Brake|Footrest
What is a car's handbrake also commonly called?|Parking brake|Accelerator|Gearbox|Fuel injector
What is the purpose of a car's windscreen wipers?|Clearing water from the windscreen|Cooling the engine|Inflating the tyres|Charging the battery
Which lights illuminate the road ahead of a car at night?|Headlights|Brake lights|Interior reading lights|Number-plate lights
What do a car's brake lights signal to following traffic?|The driver is applying the brakes|The fuel tank is full|The radio is on|The bonnet is open
Which flashing lights normally signal a driver's intention to turn?|Indicators|Headlights|Fog lights|Reading lights
What is a car's rear-view mirror mainly used to see?|The area behind the car|The fuel inside its tank|The engine cylinders|The road directly underneath it
What does a speedometer show?|The vehicle's speed|The outside air pressure|The number of passengers|The fuel's temperature
What does a car's odometer record?|Distance travelled|Current engine temperature|Tyre width|Passenger weight
What does a car's fuel gauge normally indicate?|How much fuel remains|How fast the car is moving|How many doors are open|How loud the horn is
What does the rev counter in a car display?|Engine rotation speed|Distance travelled since manufacture|The number of passengers|The amount of washer fluid
What is a car's horn used to produce?|An audible warning|A cooling airflow|An electrical charge|A fuel spray
Which car component cushions the occupants' seating area?|Seats|Headlights|Exhaust pipes|Wheel nuts
What is a car's headrest designed to support?|An occupant's head|The front wheels|The engine oil sump|The fuel tank
What is the boot of a British car called in American English?|Trunk|Hood|Fender|Windshield
What is the bonnet of a British car called in American English?|Hood|Trunk|Windshield|Licence plate
What is the windscreen of a British car called in American English?|Windshield|Trunk|Hood|Fender
What is a car's glove compartment?|A small storage compartment in the dashboard|A fuel container under the engine|A section of the exhaust|A type of tyre
What does a car's sun visor help block?|Glare from sunlight|Fuel entering the engine|Air entering the radiator|Water entering the washer bottle
Which part of a car opens to give access to the engine bay on most front-engined cars?|Bonnet|Boot floor|Rear bumper|Glove compartment
What does a car's exhaust pipe carry away?|Gases produced by the engine|Fresh drinking water|Windscreen-washer fluid|Fuel entering the tank
What is the purpose of an engine's air filter?|Removing particles from incoming air|Heating the tyres|Measuring vehicle speed|Operating the horn
What is the main purpose of a car's radiator in a liquid-cooled engine?|Helping remove heat from the coolant|Storing petrol|Cleaning the windscreen|Operating the brakes
Which part of a vehicle contains the pressurised air in a conventional pneumatic wheel assembly?|Tyre|Exhaust pipe|Seat cushion|Rear-view mirror
What is tyre tread?|The patterned surface that contacts the road|The metal wheel nut|The air valve cap|The steering column
Which part of a tyre allows air to be added or released?|Valve|Axle|Bumper|Wiper blade
What is a spare wheel carried for?|Replacing a road wheel when needed|Steering the rear passengers|Cooling the engine|Holding extra fuel
What is a car jack used to do?|Lift part of the car|Refill the fuel tank|Clean the windscreen|Check the radio signal
What secures a car wheel to its hub on many vehicles?|Wheel nuts or bolts|Wiper clips|Seat buckles|Spark plugs
What does a shock absorber help control?|Bouncing of the suspension|The colour of the headlights|The radio volume|The fuel's chemical composition
What does a car's clutch allow the driver to disconnect temporarily in a conventional manual transmission?|The engine from the transmission|The headlights from the body|The tyres from the wheels|The seats from their cushions
Which control selects forward gears or reverse in a conventional manual car?|Gear lever|Indicator stalk|Bonnet release|Wiper switch
What is the purpose of reverse gear?|Moving the vehicle backwards|Increasing the fuel tank size|Switching on the horn|Defrosting the windows
What does the P position normally mean on an automatic car's gear selector?|Park|Power steering|Passenger|Petrol
What does the N position normally mean on a car's gear selector?|Neutral|Night driving|Navigation|New battery
What does the D position normally select on an automatic car?|Drive|Defrost|Dashboard lighting|Door locking
What does a convertible car have that can be opened or lowered?|Its roof|Its engine block|Its rear axle|Its fuel pump
Which car body style normally has a separate enclosed luggage compartment behind the passenger cabin?|Saloon|Convertible without a boot|Motorcycle|Open pickup
What is the open rear load-carrying area of a pickup truck called?|Bed|Cockpit|Cabin ceiling|Engine bay
What is a tow bar used to connect to a car?|A trailer|A windscreen wiper|A steering wheel|A radiator hose
What is a trailer?|A vehicle designed to be pulled by another vehicle|A bicycle pedal|An aircraft engine|A railway signal
What is a caravan designed to provide when towed to a campsite?|Living and sleeping accommodation|An aircraft landing strip|A railway power supply|A ship's engine room
What is a motorhome?|A motor vehicle with living accommodation|A house that can never be moved|A railway station|A petrol pump
Which vehicle is commonly fitted with a rotating drum to keep concrete mixed?|Concrete mixer truck|Ambulance|Motorcycle|Sailing dinghy
Which part of a tipper truck tilts to unload its contents?|Load bed|Steering wheel|Windscreen|Front bumper
What is a forklift's pair of long front prongs used to lift?|Loads such as pallets|Only passengers|Road markings|Aircraft wings
Which vehicle is designed to compact surfaces using a heavy roller?|Road roller|Fire engine|Snowmobile|Tram
What does a snowplough's front blade push aside?|Snow|Overhead power cables|Railway sleepers|Aircraft fuel
Which vehicle is specially equipped to transport patients?|Ambulance|Concrete mixer|Road roller|Grain combine
What is a hearse primarily used to transport?|A coffin|Loose grain|Wet concrete|Railway rails
Which vehicle's main job is collecting household rubbish?|Refuse truck|Ambulance|Taxi|Tractor unit without a trailer
Which farm vehicle combines cutting and threshing a grain crop?|Combine harvester|Road sweeper|Passenger coach|Forklift
What is a car transporter designed to carry?|Other vehicles|Only loose sand|Only fuel|Railway passengers
What is a tanker truck's large enclosed tank used to carry?|Liquids or gases|Open stacks of timber|Passengers seated in rows|Cars parked on decks
What is a flatbed truck's load platform like?|Flat and open|A sealed passenger cabin|A rotating concrete drum|A pressurised spherical tank
What is the driver's compartment of a lorry called?|Cab|Hold|Galley|Cockpit canopy
Which part of a bicycle is pressed with the feet to provide power?|Pedals|Handlebar grips|Brake levers|Bell
What does a bicycle chain normally transfer to the driven wheel?|Power from the pedals|Sound from the bell|Air from the tyre|Light from the reflector
Which bicycle component carries the rider's weight while seated?|Saddle|Chainring|Front mudguard|Bell
What is a bicycle's handlebar mainly used for?|Steering|Inflating the tyres|Lubricating the chain|Charging a light
Which bicycle fitting produces a ringing warning sound?|Bell|Saddle|Pedal|Mudguard
What do bicycle mudguards help reduce?|Water and dirt thrown up by the wheels|The number of gears|The pressure inside the tyres|The length of the chain
What is a bicycle pannier?|A bag carried beside a wheel, usually on a rack|A type of brake pad|A toothed gear wheel|A wheel bearing
What is a tandem bicycle designed to carry?|Two riders, one behind the other|Only luggage with no rider|Three riders side by side|A standing rider on one wheel
How many wheels does a unicycle have?|One|Two|Three|Four
How many wheels does a tricycle have?|Three|One|Two|Four
Which part of a motorcycle is normally twisted by the rider's right hand to control engine power?|Throttle grip|Clutch lever|Fuel cap|Rear footrest
What is a motorcycle sidecar?|A passenger compartment attached beside the motorcycle|A second fuel cap|A type of tyre valve|A luggage pocket inside a helmet
What is a rail vehicle's pantograph used to contact?|An overhead electrical wire|The platform edge|A neighbouring train's door|The driver's seat
What are the crosspieces supporting railway rails commonly called in Britain?|Sleepers|Sails|Rudders|Pedals
What is a railway platform used for?|Passengers boarding and leaving trains|Refuelling cars at motorway services|Launching sailing boats|Parking aircraft in flight
What is a railway level crossing?|A place where a road or path crosses railway tracks at the same level|A bridge carrying one railway over another|An underground train tunnel|A rack for storing bicycles
What is a locomotive designed to do?|Provide power to move a train|Serve as a railway platform|Collect tickets at a station entrance|Mark a pedestrian crossing
What is a freight train primarily used to carry?|Goods|Only tourists in sleeping cabins|Aircraft in flight|Passengers on a sightseeing bus
What is a railway buffer stop designed to mark or protect?|The end of a track|The top of a signal mast|The entrance to a dining car|The middle of a railway wheel
What is a railway carriage or passenger coach used to carry?|Passengers|Only engine coolant|Only loose coal in an open wagon|Road traffic across a junction
What is a ship's bow?|Its front end|Its rear end|Its kitchen|Its engine room
What is a ship's stern?|Its rear end|Its front end|Its highest mast|Its kitchen
What is the left side of a vessel called when facing towards its bow?|Port|Starboard|Stern|Keel
What is the right side of a vessel called when facing towards its bow?|Starboard|Port|Stern|Keel
Which part of a sailing boat catches the wind to help propel it?|Sail|Anchor|Rudder stock|Bilge pump
What is a boat's anchor designed to help it do?|Remain in position|Increase its passenger capacity|Heat its cabin|Generate drinking water
What is a ship's galley?|Its kitchen|Its anchor chain|Its steering blade|Its forward mast
What is a ship's hull?|Its main body|Its kitchen stove|Its radio antenna|Its anchor
What is a ship's deck?|A floor or platform forming a level of the vessel|A wheel fitted to the bottom of a mast|A propeller blade|An item of engine fuel
What is a gangway used for at a moored ship?|Boarding and leaving the ship|Turning the propeller|Filling the lifeboats with water|Operating the anchor winch
What is a tugboat designed to help move?|Other vessels|Only aircraft|Only bicycles|Only railway coaches
What is a ferry designed to do?|Carry people or vehicles between landing places|Work only beneath the sea|Travel only on railway tracks|Launch satellites
What is a dry dock used for?|Accessing a vessel's hull out of the water|Loading a passenger aircraft|Testing road traffic lights|Storing bicycles on a train
What is a canoe paddle used to do?|Propel and steer the canoe|Measure tyre pressure|Inflate a lifejacket automatically|Store drinking water
What is an aircraft's cockpit?|The area containing the pilots' controls|The passenger baggage carousel|The airport car park|The aircraft's fuel nozzle
What is an aircraft's undercarriage also called?|Landing gear|Tailplane|Fuselage|Winglet
What is a runway used for at an airport?|Aircraft take-offs and landings|Only baggage sorting|Only passport checks|Only car repairs
What is an airport taxiway used for?|Aircraft moving on the ground between areas such as runways and stands|Passengers taking taxis into town|Vehicles driving on public motorways|Aircraft cruising between countries
What is an airport hangar designed to house?|Aircraft|Only ships|Only railway tracks|Only grain silos
What is an aircraft boarding pass normally used to show?|A passenger's permission to board a particular flight|A pilot's permission to repair every aircraft|A ship's cargo weight|A car's engine size
What makes a glider different from a conventional powered aeroplane during unpowered flight?|It flies without using engine thrust|It has no wings|It can only travel underwater|It must remain on railway tracks
What is a helicopter's main rotor primarily designed to generate?|Lift|Engine coolant|Tyre pressure|Electrical insulation'''
rows=[]
for line in data.splitlines():
 prompt,*answers=line.split('|')
 assert len(answers)==4 and len(set(answers))==4
 rows.append({'categoryID':'28','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,
 'reviewStatus':'draft_awaiting_independent_source_review','authorReview':{'meaning':'Read as one everyday vehicle or transport question.','answer':answers[0],
 'grammar':'Prompt and each answer read individually for grammar and agreement.','category':'Vehicles, their parts and basic transport vocabulary.'}})
Path(__file__).with_name('draft.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(len(rows),'unpublished Vehicles candidates')
