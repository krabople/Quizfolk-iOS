"""Original accessible Comics drafts. Each requires an individual final check."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
rows='''1|m:spider-man-peter-parker|Which Marvel superhero is Peter Parker?|Spider-Man|Iron Man|Daredevil|Hawkeye
2|m:captain-america-steve-rogers|Which Marvel superhero is Steve Rogers best known as?|Captain America|Doctor Strange|Ant-Man|Black Panther
3|m:daredevil-matthew-murdock|Which Marvel superhero uses the civilian name Matt Murdock?|Daredevil|Iron Fist|Luke Cage|Moon Knight
4|m:ant-man-hank-pym|Which scientist was Marvel's original Ant-Man?|Hank Pym|Bruce Banner|Reed Richards|Tony Stark
5|m:hawkeye-clint-barton|Which Marvel archer is Clint Barton?|Hawkeye|Falcon|Vision|Quicksilver
6|m:black-widow-natasha-romanoff|Natasha Romanoff is best known by which superhero name?|Black Widow|Scarlet Witch|Wasp|Invisible Woman
7|m:falcon-sam-wilson|Before becoming Captain America, Sam Wilson was best known as whom?|Falcon|Hawkeye|Ant-Man|Black Bolt
8|m:winter-soldier-bucky-barnes|Bucky Barnes is associated with which identity after his time as Captain America's wartime partner?|Winter Soldier|Silver Surfer|Doctor Strange|Ghost Rider
9|m:punisher-frank-castle|Which Marvel vigilante is Frank Castle?|The Punisher|Daredevil|Moon Knight|Iron Fist
10|m:moon-knight-marc-spector|Which of these names is one of Moon Knight's identities?|Marc Spector|Matt Murdock|Clint Barton|Reed Richards
11|m:wolverine-james-howlett|Besides his claws, Wolverine is especially known for which ability?|Rapid healing|Breathing underwater|Turning into sand|Controlling the weather
12|m:magneto-max-eisenhardt|Magneto's powers especially involve controlling what?|Magnetic fields and metal|Dreams|Fire|Ocean tides
13|m:professor-x|Which X-Men founder is especially known for telepathy?|Professor X|Cyclops|Colossus|Iceman
14|m:mystique|What is Mystique's signature ability in Marvel Comics?|Changing her appearance|Producing ice|Generating earthquakes|Breathing fire
15|m:nightcrawler|What is Nightcrawler especially known for doing?|Teleporting|Controlling the weather|Becoming a giant|Shooting arrows
16|m:colossus|Colossus can transform his body into a form resembling what?|Metal|Glass|Sand|Wood
17|m:iceman|The X-Man Bobby Drake is best known by which superhero name?|Iceman|Cyclops|Beast|Gambit
18|m:gambit|Which objects does Gambit famously charge with energy and throw?|Playing cards|Chess pieces|Tennis balls|Paper money
19|m:ant-man-scott-lang|What size-changing ability gives Ant-Man his name?|Shrinking to a tiny size|Always growing taller than skyscrapers|Turning into a flat picture|Splitting into hundreds of identical people
20|m:wasp-janet-van-dyne|Janet van Dyne is best known by which superhero name?|The Wasp|Storm|Black Widow|Captain Marvel
21|m:captain-america-steve-rogers|What symbol appears at the centre of Captain America's familiar round shield?|A star|A crescent moon|A lightning bolt|A skull
22|m:hawkeye-clint-barton|What weapon is Hawkeye most closely associated with?|A bow and arrows|A trident|A hammer|A sword
23|m:spider-man-peter-parker|What does Spider-Man's spider-sense chiefly warn him about?|Danger|Changes in the stock market|The exact time of sunset|Which food is freshest
24|m:black-panther-t-challa|Which rare metal is especially associated with Wakanda in Marvel Comics?|Vibranium|Adamantium|Uru|Promethium
25|m:daredevil-matthew-murdock|Which sense did Matt Murdock lose in the accident in Daredevil's origin?|Sight|Hearing|Smell|Touch
26|m:hulk-bruce-banner|What colour is Bruce Banner's Hulk form most commonly depicted as?|Green|Blue|Pink|Purple
27|m:invisible-woman-susan-storm|Which Fantastic Four heroine is especially known for becoming invisible?|Sue Storm|Jean Grey|Natasha Romanoff|Ororo Munroe
28|m:human-torch-johnny-storm|Johnny Storm's powers allow him to cover his body in what?|Flames|Ice|Stone|Sand
29|m:thing-benjamin-grimm|The Thing's familiar orange skin resembles what material?|Rock|Glass|Wood|Water
30|m:doctor-strange-stephen-strange|Doctor Strange's Cloak of Levitation most directly helps him do what?|Fly|Shrink to insect size|Become a werewolf|Turn objects into gold
31|m:wong|Which character is a longstanding ally of Doctor Strange in Marvel Comics?|Wong|Alfred Pennyworth|Commissioner Gordon|J. Jonah Jameson
32|m:star-lord-peter-quill|Peter Quill uses which superhero name?|Star-Lord|Silver Surfer|Nova|Moon Knight
33|m:groot|What kind of being is Groot in Marvel Comics?|A tree-like alien|A human astronaut|A talking robot|An underwater king
34|m:rocket|Rocket of the Guardians of the Galaxy resembles which animal?|A raccoon|A fox|An otter|A badger
35|m:gamora|Which villain raised Gamora as his adopted daughter in Marvel Comics?|Thanos|Doctor Doom|Magneto|Kingpin
36|m:drax|Which title is closely associated with the Guardians character Drax?|The Destroyer|The Sorcerer Supreme|The Man Without Fear|The King of Atlantis
37|m:vision|Which Avenger is an android with a synthetic body?|Vision|Hawkeye|Falcon|Ant-Man
38|m:quicksilver|What is Quicksilver's best-known superpower?|Super speed|Controlling plants|Turning into metal|Breathing underwater
39|m:scarlet-witch-wanda-maximoff|Quicksilver and Scarlet Witch are related in what way?|They are twin siblings|They are father and daughter|They are uncle and niece|They are married
40|m:silver-surfer|Which Marvel cosmic hero travels on a silvery board?|Silver Surfer|Nova|Star-Lord|Adam Warlock
41|m:galactus|Galactus is especially known for consuming what?|Planets|Only ordinary sandwiches|Only books|Only musical instruments
42|m:doctor-doom-victor-von-doom|Doctor Doom rules which fictional country in Marvel Comics?|Latveria|Wakanda|Genosha|Sokovia
43|m:loki|In Marvel's Thor stories, Loki is Thor's what?|Adopted brother|Biological father|Son|Grandfather
44|m:green-goblin-norman-osborn|Who is the original Green Goblin in the Spider-Man comics?|Norman Osborn|Otto Octavius|Wilson Fisk|Curt Connors
45|m:doctor-octopus-otto-octavius|Doctor Octopus is especially known for having what mechanical equipment?|Four robotic tentacles|A pair of feathered wings|A single giant boxing glove|A wheeled suit with no arms
46|m:kingpin|What is the civilian name of the Marvel crime boss Kingpin?|Wilson Fisk|Norman Osborn|Victor von Doom|Eddie Brock
47|m:venom-eddie-brock|Which of these characters is famously a host of the Venom symbiote?|Eddie Brock|Alfred Pennyworth|Commissioner Gordon|Clark Kent
48|m:ghost-rider-johnny-blaze|The stunt rider Johnny Blaze is associated with which Marvel identity?|Ghost Rider|Moon Knight|Iron Fist|Daredevil
49|m:luke-cage|Luke Cage is especially known for super strength and what other physical feature?|Extremely tough, nearly unbreakable skin|Feathered wings|A body made of sand|A tail that shoots arrows
50|m:iron-fist-danny-rand|Which Marvel martial artist is Danny Rand?|Iron Fist|Luke Cage|Daredevil|The Punisher
51|dc:batman|Which billionaire is Batman's best-known civilian identity?|Bruce Wayne|Clark Kent|Oliver Queen|Lex Luthor
52|dc:batman|What is Batman's famous customised car called?|The Batmobile|The Invisible Jet|The Quinjet|The Spider-Mobile
53|dc:batman|A batarang is Batman's version of which kind of weapon?|A throwing weapon shaped like a bat|A submarine torpedo|A laser cannon|A ceremonial sword
54|dc:superman|Which fictional mineral is Superman famously vulnerable to?|Kryptonite|Quartz|Granite|Diamond
55|dc:superman|Superman can produce intense heat beams from which part of his body?|His eyes|His ears|His knees|His feet
56|dc:supergirl|Kara Zor-El is best known as which DC superhero?|Supergirl|Wonder Woman|Batgirl|Black Canary
57|dc:supergirl|In the usual DC Comics continuity, Kara Zor-El is Superman's what?|Cousin|Mother|Daughter|Grandmother
58|dc:wonder-woman|What is Wonder Woman's famous truth-compelling rope called?|The Lasso of Truth|The Golden Web|The Rope of Dreams|The Silver Snare
59|dc:the-flash|Barry Allen is best known as which DC superhero?|The Flash|Green Lantern|Green Arrow|Aquaman
60|dc:green-arrow|Roy Harper first became Green Arrow's sidekick under which name?|Speedy|Robin|Kid Flash|Aqualad
61|dc:the-joker|Which Batman villain is nicknamed the Clown Prince of Crime?|The Joker|The Penguin|Two-Face|Bane
62|dc:the-penguin|Which Batman villain is Oswald Cobblepot?|The Penguin|The Joker|The Riddler|Scarecrow
63|dc:mr-freeze|Which Batman villain uses the civilian name Victor Fries?|Mr. Freeze|Two-Face|Bane|The Penguin
64|dc:poison-ivy|Which Batman villain is Pamela Isley?|Poison Ivy|Harley Quinn|Catwoman|Talia al Ghul
65|dc:red-hood|Which former Robin is best known for taking the identity Red Hood?|Jason Todd|Dick Grayson|Tim Drake|Damian Wayne
66|dc:batgirl|Barbara Gordon is closely associated with which costumed identity?|Batgirl|Supergirl|Wonder Woman|Starfire
67|dc:robin|What is Robin's usual role alongside Batman?|His crime-fighting partner|His biological father|The mayor of Metropolis|His chief newspaper editor
68|dc:blue-beetle|Which DC superhero identity is associated with Jaime Reyes?|Blue Beetle|Booster Gold|The Atom|Plastic Man
69|dc:plastic-man|Plastic Man's signature power allows him to do what?|Stretch and reshape his body|Control the weather|Speak only to sea creatures|Create ice from the air
70|dc:justice-league|Superman, Batman and Wonder Woman are closely associated with which superhero team?|The Justice League|The Fantastic Four|The X-Men|The Guardians of the Galaxy
71|a:asterix|Asterix is a member of which ancient people?|The Gauls|The Vikings|The Aztecs|The Spartans
72|a:asterix|What gives Asterix temporary superhuman strength?|A magic potion|A radioactive spider bite|A robotic suit|A power ring
73|a:obelix|Why does Obelix normally not need a dose of the strength-giving potion?|He fell into a cauldron of it as a baby|He invents a new potion every morning|His helmet is electrically powered|He is secretly a Roman god
74|a:obelix|Obelix is especially associated with carrying which large stone objects?|Menhirs|Obelisks covered in gold|Marble bathtubs|Millstones on wheels
75|a:dogmatix|What is the English name of Obelix's small dog?|Dogmatix|Snowy|Gnasher|Snoopy
76|a:getafix|Which druid brews the magic potion in the English-language Asterix books?|Getafix|Cacofonix|Vitalstatistix|Unhygienix
77|a:cacofonix|What is Cacofonix's role in Asterix's village?|Bard|Blacksmith|Fishmonger|Chief
78|a:vitalstatistix|Who is the chief of Asterix's village in the English-language books?|Vitalstatistix|Getafix|Cacofonix|Unhygienix
79|s:smurfs|What colour are the Smurfs usually depicted as?|Blue|Green|Orange|Purple
80|s:papa-smurf|What colour are Papa Smurf's familiar hat and trousers?|Red|Blue|Yellow|Black
81|s:gargamel|Who is the wizard who repeatedly tries to capture the Smurfs?|Gargamel|Merlin|Getafix|Doctor Strange
82|s:azrael|What is the name of Gargamel's cat in the Smurfs stories?|Azrael|Garfield|Felix|Tom
83|s:smurfette|Which Smurf is especially associated with long blonde hair and a white dress?|Smurfette|Papa Smurf|Brainy Smurf|Hefty Smurf
84|b:dennis|In the British Beano comic, what is Dennis's dog called?|Gnasher|Snowy|Snoopy|Odie
85|b:dennis|What colours are Dennis's familiar striped jumper in the British Beano comic?|Red and black|Blue and white|Green and yellow|Purple and orange
86|b:minnie|Which Beano character is known as Minnie the what?|Minx|Magician|Mermaid|Mechanic
87|b:roger|Which Beano character is famous for inventing dodges to avoid chores?|Roger the Dodger|Dennis's Dad|Plug|Calamity James
88|b:bash-street-kids|The Bash Street Kids are especially associated with which setting?|A school|A spaceship|A pirate ship|A royal palace
89|l:lucky-luke|What is the name of Lucky Luke's horse?|Jolly Jumper|Black Beauty|Silver|Bucephalus
90|l:lucky-luke|Lucky Luke's adventures are mainly set in which kind of world?|The American Old West|Ancient Egypt|A futuristic space empire|Medieval Japan
91|d:graphic-novel|What is a graphic novel?|A book-length story told through sequential artwork and text|A book containing only recipes|A list of newspaper prices|A soundtrack without pictures
92|d:comic-strip|What is a comic strip?|A sequence of drawings telling a story|A single uncaptioned political speech|A book's index alone|An actor's spoken audition
93|d:speech-bubble|In comics, what does a speech bubble usually contain?|A character's spoken words|Only the publisher's postal address|Only the price of the comic|Only the barcode
94|d:thought-bubble|In comics, what does a thought bubble usually show?|What a character is thinking|Only the date of publication|Only the name of the printer|Only the bookshop's opening hours
95|d:panel|In a comic, what is a panel?|One framed picture or section in the sequence|The entire publishing company|A character's legal name|The shop where the comic is sold
96|d:ink|What does a comic-book inker traditionally add to pencilled artwork?|Finished ink lines|Only the shipping labels|Only the retail price|Only the music
97|d:lettering|In comics, lettering mainly concerns what?|The written words and their visual presentation|Only the binding glue|Only the paper's thickness|Only the delivery route
98|d:onomatopoeia|Words such as BANG and SPLASH in a comic are examples of what?|Onomatopoeia|Anagrams|Palindromes|Acronyms
99|d:anthology|A comics anthology is typically what?|A collection of different comic stories or works|A single speech with no illustrations|A catalogue of printing machines only|A film soundtrack
100|d:manga|What is manga?|Japanese comics|Traditional Greek theatre|Spanish opera|French ballet
'''
def source(key):
 kind,term=key.split(':',1)
 return {'m':'https://www.marvel.com/characters/','dc':'https://www.dc.com/characters/','a':'https://asterix.com/en/characters/','s':'https://www.smurf.com/characters/','b':'https://www.beano.com/characters/','l':'https://www.lucky-luke.com/en/','d':'https://dictionary.cambridge.org/dictionary/english/'}[kind]+term+('/in-comics/profile' if kind=='m' else '')
if __name__=='__main__':
 out=[]
 for line in rows.strip().splitlines():
  n,key,prompt,*answers=line.split('|');assert int(n)==len(out)+1 and len(answers)==4
  out.append({'draftID':f'easy-29-{int(n):03d}','categoryID':'29','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'rationale':'Awaiting individual final question/options and reference review.','sourceURL':source(key),'reviewStatus':'draft_awaiting_author_final_check'})
 assert len(out)==100
 (HERE/'draft.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('100 unapproved Comics candidates')
