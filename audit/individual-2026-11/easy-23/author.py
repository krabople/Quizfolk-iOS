"""Accessible historical vocabulary and objects; drafts require individual review."""
import json,pathlib
H=pathlib.Path(__file__).parent
raw='''archaeology|What does archaeology mainly study?|The human past through physical remains|Future changes in the weather|The chemical composition of stars|The movement of ocean tides
artefact|In archaeology, what is an artefact?|An object made or modified by people|A prediction of future events|A naturally formed cloud|A type of volcanic eruption
excavation|What does an archaeological excavation involve?|Carefully uncovering and recording buried remains|Building a modern airport|Predicting tomorrow's weather|Repainting every object found
chronology|What does a chronology arrange in order?|Events by when they happened|Countries by their area|Rocks by their weight|Languages by their number of letters
archive|What is a historical archive mainly intended to preserve?|Records and documents|Live farm animals|Fresh fruit for sale|Fuel for aircraft
manuscript|What does manuscript literally suggest about an old book?|It was written by hand|It was printed by a laser|It was recorded on film|It was carved into a mountain
parchment|Traditional parchment for writing was made from what?|Prepared animal skin|Pressed glass|Woven copper wire|Baked clay alone
vellum|Vellum is a fine writing material traditionally made from what?|Prepared animal skin, especially calfskin|Spun glass|Coal dust|Woven steel
illuminated-manuscript|What is an illuminated manuscript decorated with?|Painted designs and often gold or silver|Electric light bulbs inside every page|Photographic film only|Modern computer screens
scribe|Before printing became widespread, what did a scribe do?|Wrote or copied documents by hand|Designed steam locomotives|Broadcast radio programmes|Developed colour photographs
cuneiform|Which shape is characteristic of cuneiform writing?|Wedge-shaped marks|Modern printed barcodes|Only perfect circles|Raised dots in six-dot cells
hieroglyph|Ancient Egyptian hieroglyphs were part of what?|A writing system using signs and pictures|A system of railway signals|An alphabet invented for computers|A form of modern shorthand only
papyrus|Ancient Egyptian papyrus sheets were made from what?|The papyrus plant|Sheep's wool|Iron filings|Ground diamonds
amphora|What was an ancient amphora?|A storage vessel with two handles|A soldier's metal helmet|A wheeled siege tower|A long-distance signalling flag
mosaic|A mosaic picture is usually made by arranging what?|Small pieces of stone, glass or similar material|Only long strands of wool|Only wet ink on paper|Only stretched animal skins
aqueduct|What was a Roman aqueduct built to carry?|Water|Mail bags on rails|Electric current|Coal gas
gladiator|What did a gladiator typically do in ancient Roman arenas?|Fight for public entertainment|Operate a printing press|Conduct a modern orchestra|Drive a steam train
obelisk|Which description fits an ancient Egyptian obelisk?|A tall, tapering stone pillar with a pointed top|A round wooden sailing ship|A low circular bread oven|A portable folding chair
sarcophagus|What is a sarcophagus?|A stone coffin|A bronze cooking pan|A woven fishing net|A leather writing case
mummy|In ancient Egyptian history, what is a mummy?|A body preserved after death|A person crowned as ruler|A record of annual taxes|A type of grain storage jar
suffrage|In political history, what does suffrage mean?|The right to vote|The right to inherit a crown automatically|A tax on imported goods|A formal declaration of war
abdication|What does a monarch do by abdicating?|Gives up the throne|Becomes ruler of an additional country|Appoints a court musician|Orders a national census
armistice|What does an armistice provide for?|An agreed suspension of fighting|The automatic unification of two countries|The coronation of a ruler|The founding of a new religion
treaty|What is a treaty?|A formal agreement between states|A private shopping list|An unofficial nickname for a ruler|A personal diary entry
abolition|What does the abolition of slavery mean?|Ending slavery by law|Increasing taxes on trade|Introducing hereditary monarchy|Building new military forts
serf|In medieval Europe, a serf was generally what?|A peasant bound to a lord's land|A ruler elected by all adults|A senior naval commander|A travelling royal ambassador
guild|What was a medieval craft guild?|An association of people in the same craft|A private army of foreign kings|A school for naval officers|A council of modern airline pilots
apprentice|How did an apprentice traditionally learn a craft?|By working under a skilled practitioner|By automatically inheriting a royal title|By serving only as a juror|By paying a tax on imported cloth
monarchy|What is a monarchy?|A system with a monarch as head of state|A system in which every citizen must be a soldier|A system without any head of state|A system ruled only by ship captains
republic|Which feature distinguishes a republic from a hereditary monarchy?|Its head of state is not a hereditary monarch|It must have only one political party|It must have no written laws|It must be ruled by a foreign king
dynasty|What is a ruling dynasty?|A succession of rulers from the same family|A group of unrelated weather events|An agreement to stop a naval battle|A tax imposed on ancient roads
regent|What does a regent do?|Rules on behalf of a monarch who cannot do so|Automatically becomes a country's chief judge|Counts only the votes in local elections|Commands every foreign army
heir|In a royal succession, who is an heir?|Someone entitled or expected to inherit the throne|Someone employed only to repair a palace|Someone who collects taxes at a port|Someone who translates old maps
coronation|What happens at a coronation?|A monarch is formally crowned|A parliament is permanently abolished|A war is formally declared|A city is granted a railway station
constitution|What does a country's constitution set out?|Basic principles and rules for its government|Only the daily weather forecast|Only the names of visiting tourists|Only a list of railway fares
census|What is the main purpose of a population census?|To count and record information about people|To elect a monarch|To declare a religious festival|To measure the height of every mountain
heraldry|Heraldry is especially concerned with which historical symbols?|Coats of arms|Railway timetables|Chemical formulae|Modern road speed limits
coat-of-arms|What is a coat of arms?|A heraldic design identifying a person, family or institution|A coat made entirely of metal sleeves|A list of weapons held by a soldier|A type of medieval bread
siege|What is a siege?|Surrounding and attacking a place to force its surrender|A ceremony for launching a ship|A journey made for religious reasons|An agreement to exchange royal marriages
rampart|What is a rampart?|A defensive wall or bank around a place|A small musical instrument|A market tax on imported wine|A royal marriage contract
moat|What is a castle moat?|A ditch around a castle, often filled with water|The highest room in a tower|The main dining table|A passage through a chimney
drawbridge|What could a castle drawbridge do?|Rise to prevent access across a ditch or moat|Rotate to tell the time of day|Lift water into the kitchens|Carry messages between distant castles
portcullis|What was a portcullis used for?|Closing a gateway with a heavy sliding grille|Carrying drinking water into a town|Lighting the inside of a tower|Measuring the depth of a harbour
battlement|What were battlements designed to provide?|Cover and gaps for defenders on top of a wall|Seats for people inside a theatre|Channels for irrigating fields|Storage bins beneath a ship
arrow-slit|Why did castles have narrow arrow slits?|To let defenders shoot while remaining partly protected|To allow cavalry to enter at full speed|To fill a moat with seawater|To hang large church bells
keep|In a medieval castle, what was the keep?|A strong central tower or building|A ditch filled with water|A bridge that could be raised|A removable roof made of canvas
bailey|In a medieval castle, what was a bailey?|An enclosed courtyard|A metal helmet|A narrow window in a dungeon|A royal hunting horn
motte|In a motte-and-bailey castle, what was the motte?|A mound supporting a fortified tower|A deep underground well|A wooden drawbridge|A stone dining table
tithe|A traditional tithe was based on what fraction?|One tenth|One half|One quarter|One hundredth
pilgrim|What is a pilgrim?|Someone making a journey to a holy place|Someone employed to repair ships|Someone elected to count votes|Someone appointed to guard a royal mint
relic|In religious history, what is a relic?|A sacred object or remains associated with a holy person|A tax paid on imported salt|A court order ending a marriage|A unit of distance used at sea
monastery|What is a monastery primarily associated with?|A religious community of monks|A parliament's elected members|A town's professional firefighters|A fleet's naval officers
abbey|What is an abbey?|A religious community led by an abbot or abbess, or its buildings|A fortified tax-collection post|A royal carriage with six wheels|A workshop for making cannonballs
scriptorium|In a medieval monastery, what was a scriptorium used for?|Writing and copying manuscripts|Smelting iron for swords|Training cavalry horses|Storing harvested grain
seal|Why was a wax seal attached to many historical documents?|To help authenticate or close the document|To make the writing invisible forever|To turn paper into metal|To measure the document's weight
wax-tablet|How could a wax writing tablet be reused?|By smoothing the wax surface|By developing it in photographic chemicals|By burning away a stone layer|By replacing a battery
chariot|What was an ancient chariot?|A wheeled vehicle usually drawn by horses|A sail-powered warship|A stone tower without doors|A long underground water tunnel
longbow|What powered an arrow shot from a traditional longbow?|The tension of the drawn bow|An electric motor|Compressed steam|A gunpowder explosion
crossbow|How is a crossbow's bow positioned?|Across a stock|Upright on a ship's mast|Inside a metal cannon barrel|Beneath a horse's saddle
chain-mail|Traditional mail armour was made mainly from what?|Interlinked metal rings|Solid sheets of glass|Woven paper strips|Carved blocks of stone
armour|What was the main purpose of armour in battle?|Protecting the wearer's body|Measuring the wind's direction|Carrying drinking water to a city|Sending messages over a telegraph
catapult|What was a military catapult designed to do?|Launch projectiles|Carry soldiers under water|Print orders on paper|Measure the angle of the Sun
battering-ram|What was a battering ram used to attack?|Gates or walls|Ships' navigation charts|A town's water supply by filtering it|A monarch's legal claim in court
trireme|What characterised an ancient trireme?|Three levels of rowers|Three steam engines|Three railway tracks|Three rotating gun turrets
galley|What mainly propelled a traditional rowing galley?|Oars worked by rowers|Jet engines|Underwater electric turbines|Steam pistons
galleon|What was a galleon?|A large sailing ship used for trade or war|An armoured railway wagon|A wheeled siege tower|A horse-drawn farming tool
caravel|A caravel was a type of what?|Sailing ship|Siege engine|Printed newspaper|Royal crown
compass|What did a traditional magnetic compass help sailors determine?|Direction|The exact age of a ship|The weight of its cargo|The chemical purity of its water
astrolabe|What could a historical astrolabe help measure?|The altitude of a celestial body above the horizon|The weight of a cannonball|The temperature inside an oven|The speed of a steam locomotive
hourglass|What flows through a traditional hourglass to mark time?|Sand|Mercury vapour|Molten iron|Steam
sundial|What does a sundial use to indicate the time?|The position of a shadow cast by sunlight|The sound of a bell underwater|The pressure of boiling water|The movement of an electric motor
spinning-wheel|What did a spinning wheel help produce?|Yarn or thread|Iron nails|Printed banknotes|Glass bottles
loom|What is a loom used to do?|Weave cloth|Grind grain into flour|Measure ocean depth|Cast metal coins
quill|A traditional writing quill was made from what?|A bird's feather|A copper pipe|A strip of window glass|A whale's tooth
printing-press|What does a printing press do?|Transfers text or images onto paper or another surface|Measures the height of buildings|Pumps water uphill|Separates gold from seawater
movable-type|What made movable type reusable in printing?|Individual letters or characters could be rearranged|Every page was carved into a new mountain|The ink erased itself before drying|Each letter was a live plant
telegraph|What did an electric telegraph transmit over wires?|Coded messages using electrical signals|Physical parcels pulled on cables|Only moving colour pictures|Only fresh drinking water
gramophone|What did a traditional gramophone play?|Sound recorded on discs|Live television broadcasts|Digital photographs|Printed newspapers
daguerreotype|What was a daguerreotype?|An early type of photograph|A medieval tax record|A Roman siege weapon|A prehistoric farming tool
sextant|What does a navigator's sextant measure?|The angle between two visible objects|The mass of the entire ship|The chemical salt content of water|The thickness of a wooden mast
abacus|What is an abacus used for?|Counting and arithmetic|Measuring wind direction|Sending radio signals|Grinding spices
stocks|What were the stocks used for as a historical punishment?|Restraining a person's feet in a wooden frame|Locking a ship's steering wheel|Preventing a printing press from turning|Closing the gates of a city
pillory|A pillory typically restrained which parts of a person's body?|Head and hands|Feet only|Waist and knees only|Shoulders and ankles only
workhouse|In Britain's Poor Law system, what was a workhouse?|An institution providing relief under rules requiring work from those able to do it|A workshop reserved for royal jewellers|A school only for naval officers|A private holiday house for factory owners
rationing|During wartime rationing, what did a ration book help control?|How much of certain goods a person could obtain|Which surname a person could use|How tall a person could grow|Which language a person could speak
blackout|Why were lights hidden during wartime blackouts?|To make places harder for enemy aircraft to locate|To help bombers identify targets|To increase the brightness of street lamps|To let ships see inland towns more clearly
evacuee|In wartime Britain, what was an evacuee?|Someone moved away from an area considered dangerous|Someone elected to command an army|Someone who collected customs duties|Someone who built aircraft engines
trench|What was a front-line trench mainly intended to give soldiers?|A protected fighting position below ground level|A clear road for passenger trains|A place to launch ocean-going ships|A raised platform for cavalry charges
propaganda|What is propaganda intended to influence?|People's opinions and behaviour|The gravitational pull of the Moon|The melting point of iron|The age of ancient rocks
cartouche|In Egyptian hieroglyphs, what did a cartouche often enclose?|A royal name|A map of all the oceans|A modern postal address|A printed railway timetable
terracotta|The word terracotta refers to what material?|Fired clay|Polished granite|Woven linen|Cast bronze
numismatics|What does numismatics study or collect?|Coins and related currency objects|Old weather maps only|Preserved insects only|Fossilised plants only
genealogy|What does genealogy study?|Family descent and relationships|The chemical makeup of rocks|The behaviour of ocean tides|The orbits of distant planets
palaeography|What does palaeography study?|Old handwriting|Ancient earthquakes|The movement of ocean currents|The composition of meteorites
epigraphy|What does epigraphy study?|Inscriptions|Weather forecasts|Animal migration routes|The composition of stars
oral-history|How are oral histories mainly recorded?|By collecting people's spoken memories and experiences|By measuring the depth of an ocean trench|By counting only the coins in a museum|By copying modern railway timetables
primary-source|Which is a primary source for studying a soldier's own wartime experience?|The soldier's diary written during the war|A modern novel about an imaginary soldier|A recent film with invented characters|A textbook chapter written centuries later
secondary-source|Which is a secondary source about a medieval battle?|A modern historian's analysis of earlier evidence|An eyewitness letter written just after the battle|A contemporary soldier's diary entry|An original order issued before the battle
prehistory|What does prehistory generally refer to?|The period before written records in the society being studied|Only the years after the invention of radio|Only the reign of one medieval king|Only the period after the Second World War
industrialisation|What change is central to industrialisation?|The growth of manufacturing using factories and machinery|The complete disappearance of all trade|The replacement of every city by farmland|The ending of all mining and production'''
d=[]
for i,line in enumerate(raw.splitlines(),1):
 term,prompt,*answers=line.split('|');assert len(answers)==4
 d.append({'draftID':f'easy-23-{i:03d}','categoryID':'23','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'rationale':'UNREVIEWED candidate; individual accuracy, options, grammar, topic fit, overlap and reference checks pending.','sourceURL':f'https://dictionary.cambridge.org/dictionary/english/{term}','reviewStatus':'draft_unreviewed'})
assert len(d)==100,len(d)
(H/'draft.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('100 History candidates drafted; none approved or published.')
