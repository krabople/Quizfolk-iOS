"""100 accessible cartoon candidates; individual editorial review still required."""
import json,pathlib,urllib.parse
H=pathlib.Path(__file__).parent
groups=[('Bluey (TV series)','''What breed of dog is Bluey in the animated series Bluey?|Blue Heeler|Border Collie|Beagle|Poodle
What is Bluey's younger sister called?|Bingo|Muffin|Socks|Chloe
Who is Bluey's dad?|Bandit|Stripe|Radley|Pat
Who is Bluey's mum?|Chilli|Trixie|Frisky|Brandy
Which country's culture and setting are central to Bluey?|Australia|New Zealand|The United Kingdom|The United States'''),('The Owl House','''Which human girl becomes Eda's apprentice in The Owl House?|Luz Noceda|Anne Boonchuy|Mabel Pines|Star Butterfly
What is Eda's nickname in The Owl House?|The Owl Lady|The Raven Queen|The Swan Princess|The Falcon Knight
What are the islands where Luz arrives called in The Owl House?|The Boiling Isles|The Misty Isles|The Emerald Isles|The Floating Isles
The Boiling Isles in The Owl House are formed from what?|The remains of a dead titan|A fleet of abandoned ships|A chain of giant turtles|A collection of floating castles
What does Luz dream of becoming in The Owl House?|A witch|A royal astronomer|A pirate captain|A professional dancer'''),('Gravity Falls','''How are Dipper and Mabel related in Gravity Falls?|They are twins|They are cousins|They are stepsiblings|They are uncle and niece
How is Grunkle Stan related to Dipper and Mabel in Gravity Falls?|He is their great-uncle|He is their grandfather|He is their older brother|He is their cousin
What is Stan's tourist attraction called in Gravity Falls?|The Mystery Shack|The Wonder Barn|The Secret Cabin|The Curiosity Castle
In which US state is the fictional town of Gravity Falls?|Oregon|Florida|Maine|Texas
What does Dipper discover that helps him investigate Gravity Falls?|A journal about paranormal creatures|A set of naval signal flags|A royal family tree|An atlas of distant planets'''),('We Bare Bears','''In which US region do the bears live in We Bare Bears?|The San Francisco Bay Area|The Florida Keys|The Great Lakes region|The Rocky Mountains
Which young human friend of the bears is a child prodigy in We Bare Bears?|Chloe Park|Mabel Pines|Luz Noceda|Tilly Green
What kind of creature is Charlie in We Bare Bears?|A Bigfoot|A koala|A panda|A grizzly bear
What kind of animal is the internet celebrity Nom Nom in We Bare Bears?|A koala|A raccoon|A red panda|A sloth
How do the three bears often arrange themselves to travel in We Bare Bears?|Stacked one on top of another|Seated in a row on a bicycle|Linked together on roller skates|Inside a single giant costume'''),('Kipo and the Age of Wonderbeasts','''What are the mutated animals called in Kipo and the Age of Wonderbeasts?|Mutes|Goblins|Golems|Wraiths
Where do many humans live at the beginning of Kipo and the Age of Wonderbeasts?|Underground burrows|Cities floating above the clouds|Colonies on the Moon|Towns inside giant trees
Whom is Kipo searching for at the start of Kipo and the Age of Wonderbeasts?|Her father|Her younger brother|Her grandmother|Her schoolteacher
What kind of animal is Kipo's companion Dave?|An insect|A wolf|A pig|A mandrill
What kind of animal is Kipo's companion Mandu?|A pig|A cat|A fox|A rabbit'''),('Big City Greens','''At the beginning of Big City Greens, where has the Green family moved from?|A country farm|A seaside hotel|An overseas military base|A mountain ski resort
What is Cricket's sister called in Big City Greens?|Tilly|Nancy|Alice|Gloria
Who is Cricket and Tilly's father in Big City Greens?|Bill|Remy|Chip|Benny
What is the Green children's grandmother called in Big City Greens?|Alice|Nancy|Gloria|Tilly
Who is Cricket's best friend in Big City Greens?|Remy|Dipper|Greg|Marco'''),('Encanto','''Which Madrigal girl does not receive a magical gift at her ceremony in Encanto?|Mirabel|Luisa|Isabela|Dolores
What is Luisa's magical gift in Encanto?|Superhuman strength|Shapeshifting|Speaking with animals|Controlling the weather
What can Bruno see in his visions in Encanto?|Possible future events|Only events before his birth|Only places on the Moon|Only other people's dreams
What ability does Antonio receive in Encanto?|Communicating with animals|Healing people with food|Growing flowers|Changing his appearance
What is Casita in Encanto?|The Madrigals' magical house|The family horse|A nearby mountain|A village festival'''),('The Wild Robot','''What name does the robot use in the 2024 film The Wild Robot?|Roz|EVE|Baymax|WALL-E
What kind of bird does Roz raise in The Wild Robot?|A goose|A penguin|An owl|A flamingo
What kind of animal is Fink in The Wild Robot?|A fox|A wolf|A raccoon|A badger
Where does Roz wash ashore in The Wild Robot?|A remote island|A crowded shopping mall|A desert palace|A space colony
What must Brightbill learn to do before the geese migrate in The Wild Robot?|Fly|Hibernate|Climb trees|Dig a burrow'''),('The Bad Guys (film)','''Who leads the gang in the 2022 film The Bad Guys?|Mr. Wolf|Mr. Snake|Mr. Shark|Mr. Piranha
What kind of animal is Professor Marmalade in the 2022 film The Bad Guys?|A guinea pig|A rabbit|A hamster|A ferret
Which award does the gang try to steal in the 2022 film The Bad Guys?|The Golden Dolphin|The Silver Eagle|The Crystal Swan|The Bronze Lion
What is Diane Foxington's public role in the 2022 film The Bad Guys?|Governor|Police chief|Museum curator|Newspaper editor
What does Mr. Wolf unexpectedly begin to enjoy in the 2022 film The Bad Guys?|Doing good deeds|Collecting rare stamps|Training racing horses|Writing detective novels'''),('Nimona (film)','''What special ability does Nimona have in the 2023 animated film Nimona?|Shapeshifting|Stopping time|Reading every written language|Turning metal into gold
Which knight teams up with Nimona in the 2023 animated film?|Ballister Boldheart|Ambrosius Goldenloin|Joaquín Mondragon|Jacob Holland
What crime is Ballister falsely accused of in the 2023 film Nimona?|Murdering the queen|Stealing the royal crown|Burning down a library|Poisoning a dragon
What role does Nimona offer to take alongside Ballister?|His sidekick|His royal tutor|His prison guard|His official biographer
Which knight is Ballister's boyfriend in the 2023 film Nimona?|Ambrosius Goldenloin|Joaquín Mondragon|Jacob Holland|Bill Goodfellowe'''),('The Mitchells vs. the Machines','''What career does Katie hope to pursue in The Mitchells vs. the Machines?|Filmmaking|Marine biology|Professional tennis|Architecture
Where is the Mitchell family's road trip initially meant to take Katie?|To film school|To a space training centre|To a naval base|To a royal wedding
What kind of uprising threatens humanity in The Mitchells vs. the Machines?|A robot uprising|A zombie outbreak|A rebellion of sea monsters|An invasion of forest spirits
What breed is the Mitchells' dog Monchi?|Pug|Dalmatian|Greyhound|Border Collie
What is the AI virtual assistant behind the uprising called in The Mitchells vs. the Machines?|PAL|AVA|VERA|DORA'''),('Wolfwalkers','''In which country is Wolfwalkers mainly set?|Ireland|Scotland|England|Wales
What is Robyn's father's occupation in Wolfwalkers?|Hunter|Blacksmith|Schoolteacher|Fisherman
Which girl does Robyn befriend in Wolfwalkers?|Mebh|Saoirse|Parvana|Nimona
What happens when a Wolfwalker sleeps?|Their spirit roams as a wolf|Their body turns into stone|They lose all their memories|They become invisible to animals
What kind of bird is Robyn's pet Merlyn in Wolfwalkers?|A falcon|An owl|A raven|A swan'''),('Song of the Sea (2014 film)','''What kind of magical being is Saoirse in Song of the Sea?|A selkie|A banshee|A wolfwalker|A leprechaun
Who is Saoirse's older brother in Song of the Sea?|Ben|Greg|Callum|Cricket
What special garment does Saoirse need in Song of the Sea?|A sealskin coat|A feathered cloak|A suit of silver armour|A red riding hood
What is Conor's job in Song of the Sea?|Lighthouse keeper|Ship's captain|Village blacksmith|Schoolteacher
Which creatures serve Macha in Song of the Sea?|Owls|Wolves|Foxes|Ravens'''),('The Breadwinner (2017 film)','''Who is the young heroine of the 2017 animated film The Breadwinner?|Parvana|Saoirse|Robyn|Mebh
In which country is the 2017 film The Breadwinner set?|Afghanistan|India|Iran|Pakistan
Why does Parvana disguise herself as a boy in The Breadwinner?|So she can work and help support her family|So she can enter a royal fencing tournament|So she can join a travelling circus|So she can inherit a palace
What has happened to Parvana's father at the start of The Breadwinner?|He has been imprisoned|He has become a ship's captain|He has moved overseas to teach|He has joined a royal orchestra
In which city does Parvana live in The Breadwinner?|Kabul|Delhi|Tehran|Lahore'''),('The Sea Beast (2022 film)','''What is Jacob Holland's profession in the 2022 animated film The Sea Beast?|Sea-monster hunter|Royal astronomer|Village doctor|Mountain guide
Which young girl stows away aboard the hunters' ship in The Sea Beast?|Maisie Brumble|Katie Mitchell|Parvana|Robyn Goodfellowe
What is the hunters' ship called in the 2022 film The Sea Beast?|The Inevitable|The Endeavour|The Discovery|The Albatross
Which captain commands the Inevitable in The Sea Beast?|Captain Crow|Captain Flint|Captain Silver|Captain Drake
What nickname does Maisie give the Red Bluster in The Sea Beast?|Red|Scarlet|Ruby|Crimson'''),("Ron's Gone Wrong",'''What kind of device is Ron in Ron's Gone Wrong?|A B-Bot companion robot|A weather satellite|An underwater research drone|A mechanical printing press
Which boy befriends Ron in Ron's Gone Wrong?|Barney|Greg|Ben|Cricket
What makes Ron unusual compared with other B-Bots in Ron's Gone Wrong?|He is defective and glitchy|He is made entirely of wood|He has no physical body|He is an ancient family heirloom
Which technology company makes B-Bots in Ron's Gone Wrong?|Bubble|PAL Labs|Buy n Large|OmniCorp
What are B-Bots designed to help their users do in Ron's Gone Wrong?|Make friends|Learn to pilot ships|Grow crops|Forecast earthquakes'''),('The Book of Life (2014 film)','''What does Manolo dream of becoming in the 2014 film The Book of Life?|A musician|A naval officer|An architect|A doctor
Which festival is central to the story of The Book of Life?|The Day of the Dead|Christmas|Easter|New Year's Day
Who competes with Manolo for María's love in The Book of Life?|Joaquín|Ballister|Jacob|Callum
At the start of The Book of Life, who rules the Land of the Remembered?|La Muerte|Xibalba|The Candle Maker|Chakal
In which country is the town of San Angel in The Book of Life?|Mexico|Spain|Brazil|Peru'''),('The Dragon Prince','''What is the young dragon Azymondias usually called in The Dragon Prince?|Zym|Bait|Pip|Zubeia
What kind of elf is Rayla in The Dragon Prince?|Moonshadow Elf|Sunfire Elf|Skywing Elf|Earthblood Elf
What is the fantasy continent called in The Dragon Prince?|Xadia|Mewni|Westeros|Narnia
How are Callum and Ezran related in The Dragon Prince?|They are half-brothers|They are twins|They are cousins|They are stepbrothers
What do Callum, Ezran and Rayla initially try to return to its mother in The Dragon Prince?|A dragon's egg|A stolen wolf cub|A magic owl|An enchanted deer'''),('Over the Garden Wall','''How are Wirt and Greg related in Over the Garden Wall?|They are half-brothers|They are twins|They are cousins|They are stepbrothers
What is the mysterious forest realm called in Over the Garden Wall?|The Unknown|The Neverwood|The Shadowlands|The Wildwood
What kind of bird is Beatrice in Over the Garden Wall?|A bluebird|A robin|An owl|A raven
What kind of animal does Greg carry in Over the Garden Wall?|A frog|A mouse|A rabbit|A turtle
Which mysterious creature stalks the travellers in Over the Garden Wall?|The Beast|The Dragon|The Collector|The Red Bluster'''),('Star vs. the Forces of Evil','''What is Star Butterfly's home dimension in Star vs. the Forces of Evil?|Mewni|Xadia|The Unknown|Narnia
Which human boy becomes Star's friend and housemate in Star vs. the Forces of Evil?|Marco Diaz|Dipper Pines|Cricket Green|Barney Pudowski
What magical heirloom does Star receive in Star vs. the Forces of Evil?|A wand|A crown|A ring|A sword
What do Star and Marco use to open portals between dimensions?|Dimensional scissors|A silver compass|A glass key|A magic paintbrush
What is Star's mother called in Star vs. the Forces of Evil?|Queen Moon|Queen Sun|Queen Dawn|Queen Aurora''')]
d=[]
for title,raw in groups:
 lines=raw.splitlines();assert len(lines)==5
 for line in lines:
  prompt,*answers=line.split('|');assert len(answers)==4
  d.append({'draftID':f'easy-32-{len(d)+1:03d}','categoryID':'32','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'sourceURL':'https://en.wikipedia.org/wiki/'+urllib.parse.quote(title.replace(' ','_')),'rationale':'UNAPPROVED candidate; individual fact, sole correct option, grammar, scope, topic and duplicate checks pending.','reviewStatus':'draft_unreviewed'})
assert len(d)==100
(H/'draft.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('100 cartoon drafts created; none approved or published.')
