"""100 accessible Geography candidates. All remain unapproved until individual review."""
import json,pathlib
H=pathlib.Path(__file__).parent
terms='''archipelago|What is an archipelago?|A group of islands|A narrow strip of land joining larger land areas|A deep river valley|A flat-topped mountain
isthmus|What is an isthmus?|A narrow strip of land joining two larger land areas|A narrow channel of water joining two seas|A group of islands|A lake formed inside a volcano
strait|In geography, what is a strait?|A narrow passage of water connecting larger bodies of water|A strip of land connecting two continents|A broad plain above sea level|A ring-shaped coral island
tributary|What is a river tributary?|A river or stream that flows into another river|The place where a river enters the sea|An abandoned river bend|A barrier built across a river
estuary|What is a coastal estuary typically characterised by?|River water mixing with seawater|A river flowing entirely underground|A permanent layer of frozen ground|A steep cliff formed by a lava flow
delta|Which process mainly builds a river delta?|Deposition of sediment near the river's mouth|Wind carving an exposed mountain summit|A glacier cutting a deep valley|Lava cooling on a volcanic slope
fjord|What is a fjord?|A long, narrow sea inlet with steep sides, usually carved by glaciers|A shallow lake left by a cut-off river bend|A broad sand dune|A ring-shaped coral reef
atoll|What is an atoll?|A ring-shaped coral reef or island enclosing a lagoon|A steep-sided valley cut by a river|A flat plain beside a river|A narrow strip of land connecting two larger areas
lagoon|What is a coastal lagoon?|A shallow body of water separated from the sea by a barrier|A waterfall inside a deep gorge|A dry channel high on a mountainside|A large area of permanently frozen ground
plateau|What is a plateau?|A raised area of relatively flat land|A narrow sea passage|A bowl-shaped river bend|A long chain of coral islands
valley|What is a valley?|An area of low ground between hills or mountains|A narrow arm of the sea surrounded by coral|A flat area on top of every mountain|A ridge separating two oceans
plain|In physical geography, what is a plain?|A broad area of relatively flat land|A deep, narrow sea trench|A steep volcanic cone|A ring of coral surrounding water
dune|What is a sand dune?|A mound or ridge of sand shaped by the wind|A deep crack made by an earthquake|A lake trapped beneath a glacier|A steep cliff made entirely from coral
oasis|What is an oasis?|A place in a desert where water supports vegetation|A permanent ice sheet at a pole|A deep ocean trench|A mountain pass cut by a glacier
bay|What is a bay?|A part of a sea or lake partly enclosed by land|A narrow ridge between mountain peaks|A permanent snowfield above the clouds|A stream that flows into another stream
cape|In coastal geography, what is a cape?|A piece of land projecting into the sea|A shallow lake behind a sand barrier|An underwater valley cut by a river|A group of coral islands
confluence|What is a river confluence?|The place where rivers or streams meet|The point where a river begins underground|A dam built to generate electricity|A bend that has been cut off from a river
meander|What is a meander in a river?|A winding bend|A vertical waterfall|A river's underground source|A wall built across the channel
floodplain|What is a floodplain?|Relatively flat land beside a river that can be flooded|A high ridge between two drainage basins|A permanent layer of sea ice|A dry valley with no connection to a river
oxbow-lake|How does an oxbow lake typically form?|A river bend is cut off from the main channel|A volcano erupts beneath the sea|A glacier melts at the top of a mountain|Wind excavates a deep desert basin
rapids|What are rapids in a river?|Fast, turbulent stretches of water|Deep, completely still pools|The places where rivers enter the sea|Underground reservoirs below a desert
waterfall|What feature forms where a river drops over a steep edge?|A waterfall|An estuary|An atoll|A plateau
gorge|What is a gorge?|A deep, narrow valley with steep sides|A wide, shallow sea inlet|A flat-topped area of high land|A ring of coral islands
glacier|What is a glacier?|A large mass of ice that moves slowly under its own weight|A permanent cloud above a mountain|A layer of frozen seawater formed each winter|A river that only flows during a storm
moraine|What is a moraine associated with?|Rock and other debris carried or deposited by a glacier|Coral growing around a tropical island|Sand blown into a desert dune|Lava flowing from a volcanic crater
iceberg|What is an iceberg?|A large floating piece of ice broken from a glacier or ice shelf|A thin layer of seawater frozen in place|A permanently frozen layer of soil|A mound of snow blown across a road
permafrost|What does permafrost mean?|Ground that stays at or below freezing for at least two consecutive years|Snow that falls on a mountain every winter|Sea ice that melts every summer|A glacier that never moves
tundra|Which description best fits tundra?|A cold, largely treeless landscape with low-growing vegetation|A hot desert covered by tall palm trees|A dense tropical rainforest|A warm coral reef in shallow water
taiga|What is the taiga also known as?|The boreal forest|The tropical rainforest|The coastal salt marsh|The equatorial desert
savanna|Which landscape is typical of a savanna?|Grassland with scattered trees|A dense forest with no grassy areas|A permanently frozen polar ice sheet|A rocky seabed without plants
rainforest|Can rainforests occur outside the tropics?|Yes, temperate rainforests also exist|No, all rainforests lie on the equator|No, all rainforests lie between the tropics|Only if they are planted inside greenhouses
steppe|Which description best fits a steppe?|A broad, largely treeless temperate grassland|A dense tropical rainforest|A warm coral reef|A steep-sided glacial sea inlet
wetland|What is a wetland?|An area where water covers or saturates the ground for at least part of the time|A desert area with no groundwater|A mountain summit above the snow line|A bare rock plateau that never holds water
karst|What mainly creates a karst landscape?|Water dissolving soluble rock|Wind piling up loose sand|Lava spreading across a plain|Sea ice freezing onto a beach
sinkhole|What is a sinkhole?|A depression formed when the ground subsides or collapses into space below|A ridge of sand formed by the wind|A coral ring around a lagoon|A cliff projecting into the sea
geyser|What does a geyser do?|Erupts with hot water and steam|Permanently freezes the ground around it|Carries a river beneath the sea|Builds a reef from coral
hot-spring|What naturally heats the water in a geothermal hot spring?|Heat from inside Earth|Only the warmth of sunlight on the surface|Friction from ocean waves|The growth of nearby plants
continental-shelf|What is a continental shelf?|The shallow, submerged edge of a continent|The deepest part of an ocean trench|A mountain range in the middle of a continent|The ice floating around a pole
watershed|What does a drainage divide separate?|Neighbouring drainage basins|The two halves of a river channel|Freshwater fish from saltwater fish|The upper and lower parts of a waterfall
drainage-basin|What is a river drainage basin?|The area of land drained by a river and its tributaries|Only the deepest pool in the river|A single bend cut off from the river|The wall of a dam across the river
urbanization|What does urbanisation generally involve?|A growing share of people living in towns and cities|A growing share of people living only on farms|The permanent removal of every city road|The conversion of all farmland into forest
suburb|What is a suburb?|An outlying district of a town or city, often residential|The historic centre of every capital city|A narrow strip of land joining two islands|A lake inside a volcanic crater
population-density|Population density measures the number of people per what?|Unit of area|Hour of the day|Unit of height|Household income
landlocked|What does it mean for a country to be landlocked?|It has no coastline giving access to the open sea|It is entirely below sea level|It is made up only of islands|It has no rivers or lakes
land-reclamation|What does reclaiming land from the sea involve?|Creating usable land from an area previously covered by water|Allowing waves to erode the coastline|Making a river flow faster upstream|Moving a mountain closer to the coast
erosion|In geography, what does erosion involve?|Wearing away and moving rock or soil|Rock breaking down only in its original place|Coral growing into a reef|Water freezing beneath the ground
weathering|What does weathering do to rock?|Breaks it down in place|Always transports it to the sea immediately|Changes every rock into lava|Makes every rock harder
sediment|Which of these is an example of sediment?|Sand or silt deposited by water|Heat stored inside Earth's core|The direction of a compass needle|The speed of a moving glacier
geothermal|Geothermal energy comes from which source?|Heat inside Earth|Wind above the ocean|Sunlight reaching a desert|The gravitational pull of the Moon alone
reservoir|What is a water-supply reservoir mainly used for?|Storing water|Measuring wind speed|Recording earthquakes|Marking the boundary of a country'''
places='''373|In which part of the United Kingdom is Stonehenge?|England|Scotland|Wales|Northern Ireland
91|In which Italian city is the Colosseum?|Rome|Milan|Venice|Florence
404|Which Greek city is overlooked by the Acropolis and its Parthenon?|Athens|Thessaloniki|Patras|Heraklion
326|In which country is the ancient rock-cut city of Petra?|Jordan|Egypt|Greece|Morocco
447|In which country is Uluru?|Australia|New Zealand|South Africa|Canada
154|The Great Barrier Reef lies off the coast of which Australian state?|Queensland|Victoria|Western Australia|Tasmania
355|Iguazú Falls lie on the border between which two countries?|Argentina and Brazil|Chile and Peru|Bolivia and Paraguay|Ecuador and Colombia
156|In which country is Serengeti National Park?|Tanzania|Kenya|South Africa|Namibia
1|The Galápagos Islands belong to which country?|Ecuador|Peru|Chile|Colombia
934|The Madeira archipelago is part of which country?|Portugal|Spain|France|Italy
w:Shetland|The Shetland Islands form part of which UK nation?|Scotland|England|Wales|Northern Ireland
514|The Orkney Islands form part of which UK nation?|Scotland|England|Wales|Northern Ireland
551|Fiordland National Park is in which country?|New Zealand|Australia|Canada|Norway
w:Tuscany|Tuscany is a region of which country?|Italy|France|Spain|Greece
w:Bavaria|Bavaria is a state of which country?|Germany|Austria|Switzerland|Belgium
w:Andalusia|Andalusia is a region of which country?|Spain|Portugal|Italy|France
w:Provence|Provence is in which country?|France|Italy|Spain|Switzerland
672|Hạ Long Bay is in which country?|Vietnam|Thailand|Malaysia|Indonesia
592|The Borobudur temple complex is in which country?|Indonesia|Cambodia|Thailand|India
1264|Jeju Island belongs to which country?|South Korea|Japan|China|Vietnam
w:Baja_California_Peninsula|The Baja California Peninsula is in which country?|Mexico|United States|Guatemala|Costa Rica
483|The Maya site of Chichén Itzá is in which country?|Mexico|Peru|Bolivia|Brazil
715|Easter Island, also called Rapa Nui, is a territory of which country?|Chile|Peru|New Zealand|Australia
1317|Réunion is an overseas department of which country?|France|Portugal|United Kingdom|Netherlands
w:Bora_Bora|Bora Bora is part of which Pacific territory?|French Polynesia|New Caledonia|American Samoa|Guam
w:Atacama_Desert|On which continent is the Atacama Desert?|South America|Africa|Asia|Australia
w:Lake_Bled|Lake Bled is in which country?|Slovenia|Slovakia|Croatia|Austria
98|Plitvice Lakes National Park is in which country?|Croatia|Slovenia|Serbia|Montenegro
w:Banff_National_Park|Banff National Park is in which Canadian province?|Alberta|Ontario|Quebec|Manitoba
w:Yellowstone_National_Park|Most of Yellowstone National Park lies in which US state?|Wyoming|Montana|Idaho|Colorado
w:Aoraki_/_Mount_Cook|Aoraki / Mount Cook is in which country?|New Zealand|Australia|Canada|South Africa
w:Torres_del_Paine_National_Park|Torres del Paine National Park is in which country?|Chile|Peru|Brazil|Ecuador
w:Kruger_National_Park|Kruger National Park is in which country?|South Africa|Kenya|Tanzania|Botswana
w:Table_Mountain|Table Mountain overlooks which South African city?|Cape Town|Johannesburg|Durban|Pretoria
403|Mount Kilimanjaro is what kind of mountain?|A volcano|A sand dune|A coral atoll|An artificial earthwork
w:Mount_Elbrus|Mount Elbrus is in which country?|Russia|Georgia|Armenia|Azerbaijan
1427|Mount Etna is on which Italian island?|Sicily|Sardinia|Capri|Elba
w:Mount_Vesuvius|Vesuvius is near which Italian city?|Naples|Turin|Venice|Genoa
166|The Sydney Opera House is in which country?|Australia|New Zealand|United Kingdom|Canada
1100|The Christ the Redeemer statue overlooks which Brazilian city?|Rio de Janeiro|São Paulo|Brasília|Salvador
w:Sagrada_Família|In which Spanish city is the Sagrada Família basilica?|Barcelona|Madrid|Seville|Valencia
314|The Alhambra palace complex is in which Spanish city?|Granada|Madrid|Bilbao|Zaragoza
616|Charles Bridge crosses a river in which European capital?|Prague|Vienna|Budapest|Warsaw
w:Blue_Lagoon_(geothermal_spa)|The Blue Lagoon geothermal spa is in which country?|Iceland|Norway|Sweden|Finland
w:Santorini|Santorini lies in which sea?|Aegean Sea|Adriatic Sea|Baltic Sea|Black Sea
173|Zanzibar is part of which country?|Tanzania|Kenya|Mozambique|Madagascar
331|Marrakesh is in which country?|Morocco|Algeria|Tunisia|Egypt
95|Dubrovnik is a coastal city in which country?|Croatia|Slovenia|Albania|Greece
755|Porto is a city in which country?|Portugal|Spain|Italy|France
w:Matterhorn|The Matterhorn stands on the border between which two countries?|Switzerland and Italy|France and Spain|Austria and Germany|Norway and Sweden'''
if __name__=='__main__':
 out=[]
 for group,block in [('term',terms),('place',places)]:
  for line in block.splitlines():
   key,prompt,*answers=line.split('|');assert len(answers)==4
   url=('https://dictionary.cambridge.org/dictionary/english/'+key if group=='term' else 'https://en.wikipedia.org/wiki/'+key[2:] if key.startswith('w:') else 'https://whc.unesco.org/en/list/'+key+'/')
   out.append({'draftID':f'easy-22-{len(out)+1:03d}','categoryID':'22','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'rationale':'UNAPPROVED: each meaning, sole correct offered answer, grammar, category, source relevance and semantic overlap still needs individual review. URLs provisional; retrieval not approval.','sourceURL':url,'reviewStatus':'draft_awaiting_author_final_check'})
 assert len(out)==100,len(out)
 (H/'draft.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print('100 UNAPPROVED Geography candidates; no bank changes.')
