"""One explicit author second-pass decision per candidate; not independent review."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
D23='https://d23.com/'
HP='https://www.harrypotter.com/'
AFI='https://catalog.afi.com/Film/'
edits={
12:{'sourceURL':'https://movies.disney.com/monsters-inc'},
18:{'prompt':'In The Incredibles, what are the Parr family secretly?','answers':['Superheroes','Aliens','Pirates','Robots']},
21:{'prompt':"In Disney's animated The Lion King (1994), who is Simba's father?",'answers':['Mufasa','Scar','Rafiki','Zazu'],'rationale':'Mufasa is Simba\'s father; Scar is his uncle, Rafiki a mandrill adviser and Zazu a hornbill. Replace animal question cued by the title.'},
22:{'prompt':'In The Lion King (1994), what kind of bird is Zazu?','answers':['A hornbill','A parrot','An ostrich','A flamingo'],'sourceURL':'https://lionking.com/familynight/','rationale':'Zazu is a hornbill. Replace Scar/Mufasa relationship already covered by Stage & Musicals.'},
23:{'sourceURL':D23+'this-day/the-lion-kings-timon-and-pumbaa-debuts-in-syndication/'},
24:{'sourceURL':D23+'a-to-z/pumbaa/'},
25:{'sourceURL':D23+'a-to-z/aladdin-film/'},
26:{'prompt':"Who is the villainous royal adviser in Disney's animated Aladdin (1992)?",'answers':['Jafar','Gaston','Scar','Captain Hook'],'sourceURL':D23+'a-to-z/aladdin-film/','rationale':'Jafar is the evil vizier. The other offered villains belong to different Disney stories; replaces Jasmine fact already covered by Stage & Musicals.'},
27:{'sourceURL':D23+'a-to-z/aladdin-film/'},
33:{'prompt':"In Disney's animated The Little Mermaid (1989), what does Ariel give Ursula in exchange for becoming human?",'answers':['Her voice','Her crown','Her memories','Her hair'],'sourceURL':'https://disneyanimation.com/films/the-little-mermaid/','rationale':'Ariel trades her voice as part of Ursula\'s bargain. Her fins are transformed, not one of the offered payment options; replaces sea-witch identity already covered in Cartoons.'},
35:{'sourceURL':D23+'then-and-now-the-enchanting-cast-of-magical-objects-in-beauty-and-the-beast/'},
36:{'prompt':"In Disney's animated Beauty and the Beast (1991), Lumière takes the form of what object?",'answers':['A candelabrum','A clock','A teapot','A mirror'],'sourceURL':D23+'then-and-now-the-enchanting-cast-of-magical-objects-in-beauty-and-the-beast/','rationale':'Lumière is a branched candle holder, a candelabrum. Use precise singular rather than imprecise candlestick; other castle objects are different characters.'},
37:{'prompt':"In Disney's animated Mulan (1998), Mulan disguises herself as what to take her father's place?",'answers':['A male soldier','A royal princess','A merchant\'s wife','A foreign queen']},
39:{'sourceURL':D23+'a-to-z/cinderella-film/'},
41:{'sourceURL':'https://www.universalpicturesathome.com/movies/shrek'},
43:{'prompt':'What is the name of the panda hero of the Kung Fu Panda films?','sourceURL':'https://www.dreamworks.com/movies/kung-fu-panda'},
45:{'sourceURL':'https://d3ddkgxe55ca6c.cloudfront.net/assets/a/fc/31/madagascar1-spread-844944.pdf'},
46:{'sourceURL':'https://d3ddkgxe55ca6c.cloudfront.net/assets/a/fc/31/madagascar1-spread-844944.pdf'},
47:{'sourceURL':'https://d3ddkgxe55ca6c.cloudfront.net/assets/a/fc/31/madagascar1-spread-844944.pdf'},
48:{'sourceURL':'https://www.dreamworks.com/trolls'},
49:{'sourceURL':'https://nhm.org/press/universal-pictures-home-entertainment-launches-nationwide-camp-croods-partnership-la-brea-tar'},
50:{'prompt':'Who voices Megamind in the original English-language Megamind (2010)?','answers':['Will Ferrell','Brad Pitt','Jonah Hill','Ben Stiller'],'rationale':'DreamWorks explicitly credits Ferrell as Megamind; Pitt is Metro Man, Hill Hal. Replace colour question to rely on an explicit cast credit, rather than an uninspected illustration.'},
52:{'prompt':'In Jaws (1975), which seaside community is threatened by the shark?','answers':['Amity','Gotham City','Hill Valley','Springfield'],'sourceURL':'https://www.universalpicturesathome.com/movies/jaws','rationale':'Universal identifies Amity as the attacked community. Other fictional towns are unrelated; replaces Spielberg director fact already present.'},
53:{'prompt':'What is the first name of the boy who befriends E.T. in E.T. the Extra-Terrestrial (1982)?','answers':['Elliott','Kevin','Marty','Charlie'],'rationale':'Elliott befriends E.T.; other offered boy names are not his. Replace alien question made trivial by Extra-Terrestrial in title.'},
54:{'prompt':'In Back to the Future (1985), what speed must the DeLorean reach to travel through time?','answers':['88 miles per hour','55 miles per hour','100 miles per hour','120 miles per hour'],'sourceURL':'https://www.backtothefuture.com/news','rationale':'The required speed is 88 mph. Correct explicit units across choices and replaces car-maker fact already in Vehicles.'},
56:{'sourceURL':AFI+'7892-THE-WIZARD-OF-OZ'},
57:{'sourceURL':AFI+'7892-THE-WIZARD-OF-OZ'},
58:{'prompt':'In The Wizard of Oz (1939), Dorothy follows the Yellow Brick Road towards which city?','answers':['The Emerald City','Kansas City','Camelot','Narnia'],'sourceURL':AFI+'7892-THE-WIZARD-OF-OZ','rationale':'Glinda directs Dorothy along the road to the Emerald City. Kansas City is not that destination; Camelot and Narnia belong to other settings. Replaces courage question cued by Cowardly Lion.'},
59:{'sourceURL':AFI+'7892-THE-WIZARD-OF-OZ'},
61:{'sourceURL':AFI+'58544-HOME-ALONE'},62:{'sourceURL':AFI+'58544-HOME-ALONE'},
63:{'sourceURL':'https://www.paramountpictures.com/movies/titanic'},
65:{'prompt':'What agent number is James Bond famously known by?','sourceURL':'https://www.007.com/'},
66:{'sourceURL':'https://www.afi.com/afis-100-years-100-cheers/'},
67:{'sourceURL':AFI+'61230-THE-MATRIX'},
68:{'sourceURL':'https://silver.afi.com/movies/detail/0100004557/'},
70:{'prompt':'In Forrest Gump (1994), Forrest represents the United States in China in which sport?','answers':['Table tennis','Badminton','Fencing','Wrestling'],'sourceURL':AFI+'55201-FORREST-GUMP','rationale':'Forrest joins the US table-tennis team and visits China. Other sports do not describe that trip; excludes his separate American football and running achievements. Replaces exact duplicate Tom Hanks casting question.'},
72:{'sourceURL':HP+'features/web-harrys-relationship-with-scar'},
73:{'sourceURL':HP+'fact-file/characters-and-pets/hedwig'},
74:{'prompt':'Who plays Ron Weasley in the eight original Harry Potter films?','answers':['Rupert Grint','Daniel Radcliffe','Tom Felton','Matthew Lewis'],'sourceURL':HP+'features/actors-of-the-wizarding-world-part-one-the-stars-that-rose','rationale':'Grint plays Ron; Radcliffe Harry, Felton Draco, Lewis Neville. Replaces surname partly duplicated by existing full-name question.'},
75:{'prompt':'Who plays Hermione Granger in the eight original Harry Potter films?','sourceURL':HP+'features/actors-of-the-wizarding-world-part-one-the-stars-that-rose'},
76:{'prompt':'Who plays the adult Severus Snape in the eight original Harry Potter films?','answers':['Alan Rickman','Gary Oldman','Ralph Fiennes','Michael Gambon'],'sourceURL':HP+'features/actors-of-the-wizarding-world-part-three-the-household-names','rationale':'Rickman plays adult Snape; others Sirius, Voldemort, later Dumbledore. Adult qualifier excludes actors in childhood flashbacks. Replaces first-year headmaster fact already in Family Trivia.'},
77:{'sourceURL':HP+'fact-file/objects/the-sorting-hat'},
78:{'sourceURL':HP+'fact-file/magical-miscellany/quidditch'},
81:{'prompt':'Who plays Princess Leia in the original Star Wars film trilogy?','answers':['Carrie Fisher','Natalie Portman','Daisy Ridley','Felicity Jones'],'sourceURL':'https://www.starwars.com/news/carrie-fisher-our-princess-passes-away','rationale':'Fisher plays Leia; others Padmé, Rey, Jyn. Replaces Vader paternity fact already tested by existing reveal quotation.'},
89:{'prompt':'In Star Wars: A New Hope (1977), Obi-Wan Kenobi is also known by which first name?','answers':['Ben','Han','Luke','Bail'],'sourceURL':'https://www.starwars.com/databank/obi-wan-kenobi-biography-gallery','rationale':'Obi-Wan uses the alias Ben Kenobi on Tatooine. Other names are different characters. Replaces duplicate Darth Vader birth-name fact.'},
91:{'answers':['Camera work and visual photography','Writing the screenplay','Editing the soundtrack','Designing the costumes']},
92:{'answers':['Showing planned shots as a sequence of drawings','Listing the cast in billing order','Recording the dialogue as sound','Calculating the cinema ticket sales']},
93:{'prompt':'What is the hinged device snapped shut at the start of a film take called?','answers':['A clapperboard','A teleprompter','A boom microphone','A light meter'],'rationale':'The hinged board is a clapperboard; the other filmmaking tools prompt dialogue, capture sound and measure light. Revised to the directly verified dictionary definition rather than asserting unverified technical synchronisation detail.'},
94:{'answers':['A subject or detail filling much of the frame','An entire landscape seen from far away','Several complete buildings viewed from the air','A wide view of a large crowd']},
95:{'sourceURL':'https://screeningshorts.org.uk/teaching-activities/camera-movements/','answers':['Turning the camera horizontally from a fixed position','Tilting the camera vertically from a fixed position','Moving the whole camera towards the subject','Changing the lens focal length without turning the camera']},
96:{'prompt':'What does using a zoom lens allow a filmmaker to change without moving the camera closer to the subject?','answers':['How large the subject appears in the frame','How loudly the actors speak','How quickly the actors physically move','The actual colour of the actors\' costumes'],'sourceURL':'https://dictionary.cambridge.org/dictionary/english/zoom-lens'},
97:{'sourceURL':'https://lib-filmcollection.trin.cam.ac.uk/spotlight/silent-film/','answers':['Recorded spoken dialogue synchronised with the picture','Visible action on the screen','A story told through images','Musical accompaniment during a screening']},
98:{'answers':['Written words on screen representing dialogue','The list of production companies before the story','The settings displayed on a camera lens','Directions for the actors printed in a script']},
99:{'answers':['Moving objects slightly between photographed frames','Filming live actors continuously at normal speed','Recording actors\' dialogue before drawing backgrounds','Moving the camera continuously during one live-action take']},
100:{'answers':['A character\'s spoken performance','The design of the backgrounds','The movement of the camera','The editing of the finished scenes']},
}
# Resolve Pixar's actual film URLs, rather than the initial index-path guesses.
for n,q in enumerate(draft,1):
 if 'pixar.com/feature-films/' in q['sourceURL']:
  u=q['sourceURL'].replace('/feature-films/','/')
  if u.endswith('/up'):u+='film'
  edits.setdefault(n,{})['sourceURL']=u
notes='''1|Woody is the cowboy doll with a pull-string voice box. Soldier, robot and racing car are other toy types. Pixar character text checked, ordinary grammar and clear Film relevance.
2|Buzz believes he is a Space Ranger on a Star Command mission. Pirate, sheriff and driver are different roles. Pixar text distinguishes his belief from being an actual working ranger; question retains believes.
3|Nemo and Marlin are clownfish. Goldfish, swordfish and angelfish are different fish types. Pixar opening explicitly identifies clownfish; no taxonomic-species overprecision.
4|Marlin is Nemo's father, not brother, uncle or grandfather. Pixar character and synopsis text both support. Existing bank asks mother Coral and Marlin's voice, different target facts.
5|Dory experiences short-term memory loss. She swims and speaks, and fear of every fish is not her defining difficulty. Pixar character paragraph directly checked; retain hyphenated short-term modifier.
6|Remy is a rat; mouse, rabbit and squirrel are not interchangeable species. Pixar states rat in opening. Remy name spelling and article choices correct.
7|Paris is the main city setting, not Rome, London or Madrid. Pixar explicitly places Remy in Paris's sewers beneath restaurant. Most allows introductory countryside sequence rather than asserting entire film occurs there.
8|WALL-E cleans waste into cubes, hence compacts rubbish. Mail delivery, racing and restaurant cooking not his designed job. Pixar robot description checked; British rubbish wording natural.
9|Thousands of balloons lift Carl's house. Helicopter, dragons and rocket engine do not. Pixar synopsis explicitly gives balloons attached to roof; no invented exact balloon count.
10|Lightning McQueen is a racing car; fire engine, tractor, bus are different Cars vehicle roles. Pixar explicitly identifies rookie race car. No uncertain real-world make/model asserted.
11|Mater is a tow truck, not racing car, fire engine or bus. Pixar character description directly checked. Proper name rather than British mater word avoids ambiguity through film scope.
12|Mike has one eye, not two/three/four. Pixar page's one-eyed text actually describes Celia, so change citation to Disney Movies' Mike description, which explicitly says one-eyed green sphere. Do not pretend the first keyword match proved Mike.
13|Boo is a human child. Robot, cat and pet bird wrong. Pixar synopsis explicitly says little human girl; question identifies Boo rather than confusing her costume with her nature.
14|Joy and Sadness operate within Riley's mind. Andy, Miguel and Merida are other Pixar children. Pixar Inside Out synopsis states Riley guided by emotions; possessive answer forms fit whose mind.
15|Mexican Day of the Dead traditions underpin Coco. Italy/Japan/Greece wrong. Pixar production material describes research in Mexico and Día de Muertos; cultural scope rather than saying the tradition is exclusive to one country worldwide.
16|Miguel wants to be a musician, not racing driver, doctor or astronaut. Pixar opening and music production text support. Dream qualifier does not confuse his family's shoemaking work with his ambition.
17|Merida's characteristic sport is archery, not tennis, skating or swimming. Pixar identifies skilled archer/swordfighter. Especially avoids claiming it is her only physical skill.
18|The Parrs secretly are superheroes, not aliens, pirates or robots. Revise secret identity wording, which could ask for the family's ordinary civilian names instead. Pixar family/superhero descriptions support the new direct question.
19|Dash has super speed. Invisibility is Violet's; underwater breathing/stone transformation not his powers. Pixar Dash description explicitly says super-speed, clear unique offered answer.
20|Mei transforms into a giant red panda. Polar bear, tiger, fox wrong. Pixar opening and Red Panda Mei section checked. Red panda is the actual animal rather than a colour variant of a giant panda.
21|Replace Simba animal identification cued by Lion King title. Mufasa is his father; Scar uncle, Rafiki adviser, Zazu majordomo. Disney film page explicitly calls Mufasa his dad. Proper version excludes unrelated adaptation continuity.
22|Scar/Mufasa relationship repeats Stage & Musicals fact, so replace with Zazu bird type. Official Lion King character guide names hornbill; parrot, ostrich, flamingo wrong. Direct request blocked, indexed official guide inspected instead; failure retained.
23|Timon is a meerkat, not mongoose, otter or rabbit. D23 explicitly names meerkat in account of characters originating in Lion King. Existing bank's Shenzi hyena question concerns a different character.
24|Pumbaa is a warthog, not rhinoceros, hippopotamus or buffalo. Disney character PDF could not be retrieved, so replace with D23 Pumbaa entry explicitly saying warthog. No common-vs-desert-warthog taxonomic claim; Pumbaa spelling correct.
25|Film Genie emerges from a lamp. Mirror, ring and sword are wrong for the specified animated film; other Aladdin folklore sometimes has a ring genie. D23 synopsis explicitly links lamp and Genie.
26|Jasmine identification repeated Stage & Musicals, so replace with evil vizier Jafar. Gaston, Scar, Hook are villains in different films. D23 synopsis identifies Jafar's role; adviser British spelling and villainous qualifier unambiguous.
27|Abu is a monkey. Rajah tiger/Iago parrot differ; snake wrong for Abu's usual character. D23 explicitly names monkey Abu. No claim he never temporarily transforms into another creature.
28|Elsa's magic concerns ice and snow, not fire/lava, sand/dust, electricity/metal. Disney Frozen synopsis describes icy powers and winter. Especially avoids exhaustive scientific description of magic.
29|Anna's sister is Elsa, not Rapunzel, Ariel or Merida. Disney synopsis explicitly states sister. No ambiguity about adopted or metaphorical sisters introduced.
30|Olaf is a snowman, not reindeer/wolf/polar bear. Disney synopsis explicitly names hilarious snowman Olaf. Living snowman still a snowman in fictional context.
31|Sven is a reindeer, not moose, horse or wolf. Disney synopsis gives Kristoff's reindeer Sven. Correct article before reindeer and name spelling checked.
32|Ariel begins as a mermaid. Fairy/witch/human princess wrong at that stage. Beginning qualifier necessary because she becomes human later; Disney synopsis identifies mermaid princess.
33|Ursula identity was already in Cartoons. Replace with Ariel's payment: voice, not crown, memories or hair. Disney Animation synopsis explicitly gives bargain. Fins also change, so do not put fins among options and make two defensible answers.
34|Belle is heroine of the 1991 animation. Jasmine, Aurora, Ariel belong to other stories. Disney film page introduces Belle as central heroine; specify animation and year to delimit version.
35|Mrs Potts becomes a teapot; clock, candlestick and wardrobe are different characters. D23 compares animated/live-action enchanted objects and explicitly states 1991 teapot. Keep Mrs without unnecessary American full stop consistently.
36|Lumière becomes branched candle holder, precisely a candelabrum. Clock/teapot/mirror wrong. D23 explicit candelabra description checked; singular candelabrum and name accent corrected instead of imprecise plain candlestick.
37|Mulan impersonates male soldier Ping to replace father. Princess/merchant's wife/foreign queen wrong. Disney synopsis explicit; revise disguised as whom answer a man to natural disguised as what answer a male soldier.
38|Mushu is a dragon, not phoenix, tiger or crane. Disney synopsis identifies guardian dragon. Original animation/year qualifier prevents confusing remake's phoenix with Mushu.
39|Glass slippers, not gold/silver/silk. D23 Cinderella synopsis explicitly gives glass slipper. Film/year qualifier avoids footwear differences in other folk-tale versions.
40|Queen offers apple, not pear, peach or plum. Disney synopsis explicitly describes enchanted apple; poisoned fruit wording accurate in film. Existing bank asks Queen's misleading wishing-apple label, a distinct target rather than same question.
41|Shrek is an ogre, not troll, giant or goblin. DreamWorks page lacked explicit species, so use Universal's synopsis identifying ogre. No speculative biological definition of fictional species.
42|Eddie Murphy voices Donkey in original English Shrek. Myers Shrek, Lithgow Farquaad, Banderas later Puss do not answer. DreamWorks synopsis explicitly pairs actor/role; English qualification excludes translated casts.
43|Po is panda hero; Shifu, Tai Lung, Oogway other characters. DreamWorks URL now presents fourth film, and guessed original-film path404s. Frame question around film series, which current official synopsis explicitly identifies as Po's continuing adventures; do not pretend unavailable original-specific page was inspected.
44|Toothless is Hiccup's dragon, other named dragons belong to other riders. DreamWorks 2010 synopsis explicitly pairs Hiccup and Toothless. Year avoids live-action remake ambiguity.
45|Alex is lion, not tiger/zebra/giraffe. Authorised Madagascar reader character sheet explicitly labels Alex the lion. Original generic film synopsis alone did not establish species; citation made precise. Matching-game PDF retrieved but not used as text evidence of labels.
46|Melman is giraffe, not hippo/zebra/lion. Authorised Madagascar reader explicitly identifies Melman the giraffe. Name rather than actor question supplies accessible film knowledge.
47|Marty is zebra, not giraffe/lion/hippo. Authorised Madagascar reader character spread inspected. These three test different friends; none duplicates earlier bank facts or one another's target.
48|Poppy and Branch belong to Trolls. Shrek/Croods/Boss Baby feature other protagonists. Official franchise page identifies characters; use that rather than generic first-film synopsis omitting their names.
49|Croods family lives in fictional prehistoric world, not future station/modern office/medieval court. Natural History Museum/Universal partnership describes prehistoric Croods characters. No false claim fantasy creatures portray one scientifically accurate geological age.
50|Replace colour item with credited voice: Will Ferrell as Megamind, Pitt Metro Man, Hill rival, Stiller not character. DreamWorks synopsis explicitly pairs roles. Original English/version/year delimit alternate dubbing and later TV cast.
51|Jurassic Park is the 1993 cloned-dinosaur park film. Jaws shark, E.T. alien, Raiders archaeology wrong. Universal synopsis describes revived dinosaurs and theme park; familiar premise rather than obscure production detail.
52|Spielberg-director item duplicated earlier E.T. fact, so replace with Amity community in Jaws. Universal synopsis directly names Amity. Gotham, Hill Valley and Springfield are different fictional communities; existing filming-location Martha's Vineyard fact distinct.
53|Replace being-an-alien giveaway in Extra-Terrestrial title. Elliott is boy befriending E.T., not Kevin/Marty/Charlie. Universal synopsis explicitly names Elliott; existing deleted-principal casting question does not ask boy's name.
54|Replace DeLorean maker fact already in Vehicles. Time travel requires 88 mph, not 55/100/120. Official Back to Future news explicitly uses 88 miles per hour; same units in each answer. Speed necessary, not claimed alone sufficient without working time circuits/power.
55|Bill Murray plays Peter Venkman. Aykroyd Ray, Ramis Egon, Hudson Winston. Sony Ghostbusters synopsis explicitly pairs all four roles; original 1984 scope excludes remake characters.
56|Tin Man hopes for heart, not Scarecrow's brain, Lion's courage or wand. AFI synopsis describes requests. Hopes to receive avoids inaccurate claim Wizard literally provides a biological organ rather than testimonial/token.
57|Scarecrow seeks brain, not heart/courage/crown. AFI synopsis checked alongside Tin Man. Request, not literal proof he lacks reasoning; film deliberately shows existing intelligence.
58|Replace courage giveaway from Cowardly Lion. Yellow Brick Road leads towards Emerald City, not Kansas City/Camelot/Narnia. AFI explicit Glinda directions inspected. Towards allows adventures and interruptions on journey.
59|Dorothy's dog is Toto. Lassie/Snoopy/Pluto other fictional dogs. AFI opening identifies little dog Toto. Existing Dorothy Gale surname item targets different fact.
60|Mary Poppins is nanny, not police officer/doctor/headteacher. Disney synopsis explicitly calls nanny. Specify 1964 film; no need exact employment-contract claim.
61|Macaulay Culkin plays Kevin, not Wood/Radcliffe/Osment. AFI cast and character pairing checked. Home Alone 1990 excludes recasting in later sequels.
62|McCallisters fly to Paris; Rome/Madrid/Berlin wrong. AFI synopsis says family gathering for Paris trip, later telephone call from Paris confirms. Original-film qualifier avoids New York sequel.
63|Leonardo DiCaprio plays Jack Dawson, not Pitt/Damon/Depp. Paramount film page explicitly pairs DiCaprio and Jack. Direct request blocked but indexed studio page inspected; replace obsolete 20th Century URL that returned404.
64|Indiana Jones is archaeologist, not astronaut/marine biologist/journalist. Lucasfilm Raiders synopsis explicitly identifies profession. Does not claim all his adventures are scientifically realistic archaeology.
65|Bond is famously agent007;001/008/009 not his familiar number. Reword to famously known by because Nomi uses007 after Bond retires in No Time to Die. Official franchise homepage supports identification without insisting number is exclusive forever.
66|Rocky Balboa boxes, not wrestling/judo/fencing. AFI 100 Cheers Rocky synopsis explicitly boxer. Original film year and exact character avoid ambiguous Rocky nickname in other sports.
67|Neo chooses red pill;blue offered alternative,green/yellow not choices. AFI Matrix synopsis confirms which reveals truth. Question asks colour rather than whether later pill analogies are medical facts.
68|Jim Carrey plays Stanley Ipkiss, not Williams/Sandler/Stiller. AFI Silver synopsis explicitly pairs role and actor. Replace Warner landing page containing no relevant cast information.
69|Johnny Depp plays Jack Sparrow. Bloom Will,Rush Barbossa,Bardem later Salazar. Disney/D23 original-film cast reference checked; precise original title and year avoid generic all-franchise actor query.
70|Exact duplicate Forrest casting question replaced. US China visit is table tennis, not badminton/fencing/wrestling. AFI synopsis supports US team visit. Specify trip because Forrest also succeeds in football and running; neither is an alternative here.
71|Harry attends Hogwarts, not Durmstrang/Beauxbatons/Ilvermorny. Official Hogwarts description identifies his school/home. Other schools real within fictional world but not Harry's school.
72|Scar lightning bolt, not crescent/star/triangle. Initial Harry fact file omitted scar; official feature specifically describes thin lightning bolt. Change source instead of claiming generic character bio established visual detail.
73|Hedwig is Harry's owl; Errol/Pigwidgeon other owls, Fawkes phoenix. Official Hedwig biography explicitly gift/companion. Source changed to dedicated bird entry rather than incomplete Harry biography.
74|Replace Ron surname already inferable from existing full-name question. Rupert Grint plays Ron in original eight films; Radcliffe Harry,Felton Draco,Lewis Neville. Official cast feature checked, original-eight qualifier excludes new television or stage casting.
75|Emma Watson plays Hermione, not Roberts/Ronan/Fanning. Official actors feature explicitly associates Watson and Hermione. Original eight films qualifier protects against future television actor changes.
76|First-year Dumbledore headmaster was already in Family Trivia. Replace with adult Snape actor Alan Rickman. Oldman Sirius,Fiennes Voldemort,Gambon Dumbledore wrong. Adult and original-eight delimit flashback and television recast possibilities.
77|Sorting Hat assigns houses. Goblet selects tournament champions,map locates people,cloak conceals. Official object entry/ceremony reference identifies function. Wrong guessed magical-miscellany URL404 corrected to objects path.
78|Quidditch players ride broomsticks, not dragons/carpets/eagles. Official Quidditch fact file explicitly says broomsticks. Usually allows disrupted/unusual moments without forcing every player permanently on a broom.
79|Hagrid half human/half giant, not goblin/elf/centaur. Official character description explicitly half-man half-giant. No claim fictional ancestry is a real human taxonomy.
80|Dobby is house-elf, not goblin/troll/centaur. Official Dobby fact file explicitly identifies him. Hyphen and article a house-elf correct; different from existing question asking which elf warned Harry.
81|Vader paternity repeated existing reveal quote, so replace with Leia actor. Carrie Fisher plays Leia original trilogy; Portman Padmé,Ridley Rey,Jones Jyn. Official Lucasfilm memorial explicitly identifies casting; original trilogy avoids later digital/newer interpretations.
82|Jedi glowing blade weapon is lightsaber. Blaster projectile-energy gun,vibro-axe and bowcaster other weapons. Official Databank identifies energy blade; no claim only Jedi can ever use one.
83|Yoda trains Luke on Dagobah. Windu,Qui-Gon,Dooku are not that trainer. Official Yoda history supports Luke's training/exile; specific planet/film excludes Luke's earlier lessons with Obi-Wan.
84|Chewbacca is Wookiee, not Ewok/Hutt/Gungan. Official Databank opening explicit. Double-e Wookiee spelling correct and no human ethnic analogy.
85|R2-D2 is an astromech droid, not Wookiee/Jedi/Sith. Official Databank opening explicit. Character type rather than claim about Force sensitivity of every possible droid.
86|Han's ship is Millennium Falcon, not Star Destroyer/Razor Crest/Ghost. Official Databank explicitly links Falcon owners Han/Chewbacca. Famous ship qualifier rather than claim he only ever pilots one craft.
87|Death Star is space/battle station, not natural moon/planet/lightsaber. Databank explicitly moon-sized space station. Natural modifier prevents moon-sized nickname becoming second correct answer.
88|Leia is Luke's twin. Padmé mother,Rey/Ahsoka unrelated offered characters. Official Leia history identifies twins Luke and Leia; no adoptive-parent confusion.
89|Vader birth name exact duplicate removed. Obi-Wan adopts name Ben on Tatooine;Han/Luke/Bail different people. Official biography-gallery indexed caption inspected, while direct text extraction misses image captions; do not equate missing text with corroboration.
90|Luke grows up on Tatooine, not Naboo/Coruscant/Hoth. Databank identifies both Skywalkers calling it home; Luke history qualifies upbringing. Existing Anakin upbringing question concerns different person, but no birthplace claim about Luke.
91|Cinematography camera/visual photography, not screenplay/soundtrack/costumes. Cambridge definition explicitly film photography. Replace snack/ticket/lyrics distractors with real production departments; unique answer still easy.
92|Storyboard drawings plan shot/event sequence. Cast list/audio recording/ticket sales not storyboard. Cambridge definition checked. Replace shoe-cleaning/catering distractors with credible production artefacts.
93|Original clap synchronisation statement exceeded retrieved dictionary definition. Revise to identify hinged snapped device as clapperboard; teleprompter,boom microphone,light meter distinct. Cambridge describes two board parts hit together; no unsupported precise mechanism asserted.
94|Close-up frames subject/detail prominently, not wide landscape/aerial buildings/crowd. Relevant photographic sense checked. Remove title-card choice and small-subject requirement: subject can be a face or physically large object, so its actual size is not decisive.
95|Use Screen Scotland/Screening Shorts camera-movement teaching definition: horizontal swivel is pan;vertical tilt,physical dolly movement,lens focal-length change distinct. Cambridge uses pan more broadly including up/down, so replace with explicit filmmaking source rather than ignoring discrepancy.
96|Zoom lens changes subject's apparent frame size from fixed camera position. Actor loudness/physical speed/costume actual colour not controlled by lens focal length. Dedicated zoom-lens definition checked; bare zoom entry only cross-reference was insufficient alone.
97|Silent-film distinction is lack of synchronised recorded spoken dialogue, not absence of action/story/live music. Trinity Cambridge educational description explicitly explains music-only soundtracks and spoken dialogue transition. Retain typically and traditional for historical edge cases/part-talkies.
98|Film subtitles are written dialogue/translation on screen, not production-company opening logos,lens settings,script directions. Relevant Cambridge film sense inspected, distinct from a book's subtitle. Replace cinema-seat/music distractors with visual-production terms.
99|Stop-motion repositions objects between photographed frames. Continuous live action,voice prerecording,continuous camera move not defining technique. Cambridge definition explicit; remove silly no-images/entire-one-photo options, do not require all stop-motion be clay.
100|Animated character voice actor supplies spoken performance. Backgrounds,camera movement,scene editing other roles. Cambridge specifically includes character in animated film. Mainly allows actors occasionally holding other credits without making them additional correct job definitions.
'''
rows=[]
for line in notes.strip().splitlines():
 n,note=line.split('|',1);n=int(n)
 d={'row':n,'action':'edit' if n in edits else 'keep','prompt':draft[n-1]['prompt'],'note':note,'sourceReview':'Explicit author second pass of this question, all four options, sole correct answer, grammar, Film relevance and cited reference context. Not independent review.'}
 if n in edits:d['recommendedChanges']=edits[n]
 rows.append(d)
assert [x['row'] for x in rows]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'reviewer':'root (author second editorial pass)','independent':False,'sourceAccessNote':'One explicit judgment per question and all options. Repeated target facts and title giveaways replaced, exact versions specified, unrelated filmmaking distractors replaced. Sources inspected as actual studio/official character texts, specialist film references or educational definitions; retrieval alone never approves. Blocked requests and indexed web/caption inspection distinguished in source-access metadata. Private reference extracts are not republished.','rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('100 author second-pass judgments recorded; apply edits before publishing')
