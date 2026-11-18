"""Explicit item-by-item author checks. No independent reviewer claimed."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
M='https://www.marvel.com/'
AV=M+'teams-and-groups/avengers/in-comics'
FF=M+'teams-and-groups/fantastic-four/in-comics'
XM=M+'teams-and-groups/x-men/in-comics'
CAP=M+'comics/discover/2376/captain-americas-of-the-multiverse'
RPG='https://cdn.marvel.com/u/prod/marvel/i/pdf/'
SCH='https://www.scholastic.com/content/dam/scholastic/educators/discussion-guides/guide-to-using-graphic-novels.pdf'
edits={
7:{'prompt':'Under which superhero name was Sam Wilson best known before becoming Captain America?'},
18:{'prompt':"What are Gambit's most famous energy-charged throwing weapons?",'answers':['Playing cards','Chess pieces','Tennis balls','Paper money']},
19:{'answers':['Shrinking to a tiny size','Passing through solid walls','Turning completely invisible','Reading other people\'s thoughts']},
21:{'prompt':"What gives Steve Rogers his enhanced abilities in Captain America's classic comic-book origin?",'answers':['A super-soldier treatment','A radioactive spider bite','Exposure to cosmic rays','An alien symbiote'],'rationale':'The super-soldier programme enhances Rogers. Spider bite, cosmic rays and symbiote are other Marvel origins; replaces shield-art detail not established by retrieved textual references.'},
23:{'answers':['Danger','Other people\'s private thoughts','Whether any speaker is lying','The precise distance to every object in space']},
30:{'prompt':'Which Marvel superhero is Stephen Strange?','answers':['Doctor Strange','Hawkeye','Iron Man','Captain America']},
35:{'prompt':'Gamora is best known as a member of which Marvel superhero team?','answers':['The Guardians of the Galaxy','The Fantastic Four','The X-Men','The New Mutants']},
41:{'prompt':'Which Marvel character is famously known as the Devourer of Worlds?','answers':['Galactus','Doctor Doom','Kingpin','Green Goblin']},
45:{'answers':['Four mechanical tentacles','A pair of powered mechanical wings','A giant armoured wheel','A robotic spider-shaped vehicle']},
49:{'answers':['Extremely tough, bullet-resistant skin','Elastic limbs','Retractable claws','Electrically charged skin']},
53:{'answers':['A bat-shaped throwing weapon','An explosive submarine missile','A laser cannon worn on the wrist','A ceremonial sword']},
73:{'answers':['He fell into a cauldron of it as a small boy','He invents a new potion every morning','His helmet supplies his strength','He is secretly a Roman god']},
80:{'prompt':'Which Smurf is the wise elder who leads the village?','answers':['Papa Smurf','Brainy Smurf','Hefty Smurf','Clumsy Smurf']},
83:{'prompt':'Which Smurf did Gargamel originally create?','answers':['Smurfette','Papa Smurf','Brainy Smurf','Hefty Smurf']},
85:{'prompt':"Which two colours feature on Dennis's striped jumper in the British Beano comic?"},
87:{'prompt':'Which company publishes the Beano comic?','answers':['DC Thomson','Marvel Comics','Panini','Rebellion']},
91:{'answers':['A book-length story told through sequential artwork and text','A prose novel with no illustrations','A book made entirely of screenplay instructions','An audio performance without pictures']},
92:{'answers':['A sequence of drawings telling a story','A prose-only newspaper editorial','A single scene performed on stage','An audio-only dramatisation']},
93:{'answers':["A character's spoken words",'A list of the production credits','The space between two panels','Only the publisher\'s address']},
94:{'answers':['What a character is thinking','Words spoken aloud to another character','Only the author\'s name','Only the comic\'s retail price']},
95:{'answers':['One individual picture or section of the sequence','The empty space between pictures','A character\'s spoken words alone','The entire series of published issues']},
96:{'prompt':'What is a caption box usually used for in a comic?','answers':['Narration or descriptive text','The empty space separating panels','The outline around the whole page','Only the retail price']},
97:{'answers':['The written words and their visual presentation','The pencilled character drawings','The colours added to the artwork','The physical binding of the book']},
99:{'prompt':'What is the space between panels in a comic called?','answers':['A gutter','A speech balloon','A caption','A splash page']},
100:{'answers':['Japanese comics','Japanese animated television programmes','Korean live-action dramas','Chinese martial arts']},
}
sources={
1:M+'characters/spider-man-peter-parker/in-comics',2:CAP,
3:'https://latency.marvel.com/comics/discover/877/daredevil-legacy',4:AV,
5:M+'articles/games/marvel-rivals-announces-hawkeye-joining-launch-roster-new-map-wakanda',
6:M+'characters/black-widow-natasha-romanova/in-comics',7:CAP,8:M+'characters/namor/in-comics',
9:M+'characters/nick-fury-sr',10:AV,11:M+'items/adamantium',12:XM,13:XM,14:M+'characters/mystique',
15:RPG+'MMRPG_XMen97_20240517.pdf',16:'https://share.marvel.com/comics/discover/445/colossus',
17:M+'characters/Iceman',18:RPG+'MMRPG_XMen97_20240517.pdf',
19:'https://impact.disney.com/app/uploads/2022/01/Ant-Man-and-the-Wasp-Activity-Packet-Final.pdf',
20:M+'articles/comics/an-oral-history-of-secret-invasion',21:CAP,
22:M+'articles/games/marvel-rivals-announces-hawkeye-joining-launch-roster-new-map-wakanda',
23:M+'characters/spider-man-peter-parker/in-comics',24:M+'articles/comics/the-villains-of-black-panther',
25:'https://latency.marvel.com/comics/discover/877/daredevil-legacy',26:RPG+'MMRPG_MarvelRivals_20241220.pdf',
27:'https://share.marvel.com/comics/discover/2509/sue-storms-coolest-powers',
28:M+'characters/human-torch-johnny-storm/in-comics/profile/',29:FF,30:AV,
31:M+'characters/wong/in-comics',32:M+'comics/characters/1010733/starlord_peter_quill',
33:RPG+'MMRPG_MarvelRivals_20241220.pdf',34:RPG+'MMRPG_MarvelRivals_20241220.pdf',
35:M+'articles/comics/10-greatest-guardians-of-the-galaxy',36:M+'comics/issue/56862/drax-2015-1',
37:AV,38:M+'teams-and-groups/young-avengers',39:M+'articles/comics/pietro-maximoff-quicksilver-comics-history?linkId=112067650',
40:M+'comics/issue/48333/silver_surfer_2014_6',41:M+'characters/galactus/',
42:M+'comics/issue/123518/one_world_under_doom_2025_1_variant/variant',43:M+'characters/loki/in-comics',
44:'https://share.marvel.com/comics/discover/984/green-goblin',45:M+'characters/doctor-octopus-otto-octavius/in-comics',
46:M+'characters/kingpin/',47:'https://share.marvel.com/comics/discover/713/venom-eddie-brock',
48:M+'teams-and-groups/spirits-of-vengeance',49:'https://share.marvel.com/comics/discover/433/luke-cage',
50:M+'comics/issue/22628/iron_fist_1975_2',
52:'https://www.dc.com/blog/2014/07/22/batman-at-75-highlights-in-the-life-of-the-caped-crusader',
54:'https://www.dc.com/blog/2025/05/29/crushed-by-color-a-kryptonite-catalogue',
55:'https://www.dc.com/blog/2023/05/10/ask-the-question-when-did-superman-get-his-heat-vision',
56:'https://www.dc.com/graphic-novels/supergirl-2005/supergirl-vol-1-the-girl-of-steel',
57:'https://www.dc.com/graphic-novels/supergirl-2005/supergirl-vol-1-the-girl-of-steel',
58:'https://www.dc.com/blog/2026-10-21/all-the-world-s-waiting-twelve-moments-that-defined-wonder-woman',
60:'https://www.dc.com/characters/arsenal',63:'https://www.dc.com/characters/mister-freeze',
64:'https://www.dc.com/graphic-novels/poison-ivy-thorns',
67:'https://www.dc.com/characters/batman',
74:'https://asterix.com/en/characters/getafix',
79:'https://www.smurf.com/',80:'https://www.smurf.com/',81:'https://www.smurf.com/',82:'https://www.smurf.com/',83:'https://www.smurf.com/',
84:'https://schools.beano.com/lesson-plans/dennis-gnasher-custard-caper/',
85:'https://schools.beano.com/lesson-plans/dennis-and-the-washing-machine/',
86:'https://d3ddkgxe55ca6c.cloudfront.net/assets/t1426862669/a/c0/65/dennis-resourcepack-teacher-resource-1341480.pdf',
87:'https://www.dcthomson.co.uk/brands/beano/',88:'https://schools.beano.com/lesson-plans/battle-of-bash-street-school/',
89:'https://www.dargaud.com/bd/lucky-luke',90:'https://www.cinebook.co.uk/uploads/files/catalogues/Catalogue_36_web.pdf',
95:SCH,96:SCH,99:SCH,
}
for n,u in sources.items():edits.setdefault(n,{})['sourceURL']=u
notes='''1|Peter Parker is Spider-Man. Stark's Iron Man,Murdock's Daredevil,Barton's Hawkeye wrong. Comics identity differs from prior question about radioactive origin. Publisher Spider-Man biography inspected through index.
2|Steve Rogers is Captain America, not Strange,Ant-Man,Panther. Familiar identity, not claim only Rogers ever carries title. Publisher multiverse guide explicitly identifies original Steve Rogers.
3|Matt Murdock is Daredevil. Iron Fist,Luke Cage,Moon Knight different people. Publisher Daredevil Legacy names blind lawyer; distinct from existing hair-colour and nickname questions.
4|Hank Pym original Ant-Man; Banner Hulk,Richards Mister Fantastic,Stark Iron Man. Original qualifier needed because Scott Lang also Ant-Man. Avengers history explicitly pairs Hank Pym/Ant-Man.
5|Clint Barton is Hawkeye. Falcon,Vision,Quicksilver other heroes. Publisher reveal names archer; no claim Kate Bishop cannot also use title.
6|Natasha Romanoff is Black Widow, not Wanda's Scarlet Witch,Janet's Wasp,Sue's Invisible Woman. Actual Comics biography uses Romanova/Romanoff variants; supplied familiar form is valid.
7|Sam Wilson originally Falcon before Captain America; others unrelated identities. Publisher Captain Americas guide explicitly former Falcon. Does not imply Wilson never returns to Falcon identity later.
8|Bucky Barnes later Winter Soldier. Surfer,Strange,Rider other characters. Namor comics biography explicitly Bucky later Winter Soldier; no claim this was his only later identity, since he also became Captain America.
9|Frank Castle is Punisher. Murdock,Spector,Rand other offered vigilantes. Publisher Nick Fury biography identifies Frank Castle AKA Punisher; term vigilante avoids debating superhero vs antihero.
10|Marc Spector one Moon Knight identity. Matt,Clint,Reed not his other identities. One of qualifier respects Steven Grant/Jake Lockley rather than falsely reducing dissociative identity to one alias.
11|Wolverine healing factor supports rapid recovery. Underwater breathing,sand transformation,weather control not signature abilities. Publisher adamantium account and character sheet healing factor checked; not invulnerability to every injury.
12|Magneto magnetic powers/metal. Dreams,fire,tides not principal power. X-Men official history explicitly mastery of magnetism; does not assert only ferromagnetic real-world physics applies in fiction.
13|Professor X telepathic founder. Cyclops optic blasts,Colossus metal,Iceman ice do not provide this answer. X-Men official history identifies Xavier's telepathy/founding role.
14|Mystique shapeshifts appearance, not ice,earthquakes,fire. Publisher biography explicitly shape-shifting mutant. No appearance-only limit asserted on every continuity or current expanded powers.
15|Nightcrawler teleportation, not Storm's weather control,growinggiant,archery. Publisher X-Men character sheet explicitly Teleport; classic ability rather than invented maximum distance.
16|Colossus metal form, not glass,sand,wood. Publisher Colossus introduction explicitly describes steel; metal keeps accessible and avoids overtechnical organic-steel mechanism.
17|Bobby Drake Iceman, not Scott's Cyclops,Hank's Beast,Remy's Gambit. Publisher Iceman biography explicitly names Bobby. Different from a general superhero ice-power prompt.
18|Gambit charges playing cards;chess pieces,tennis balls,paper money not iconic thrown objects. Publisher X-Men character sheet charged cards checked. Famously allows his power to charge other objects too.
19|Ant-Man shrinks. Intangibility,invisibility,mind-reading are other powers, replacing always-growing and bizarre flat-picture options. Official Disney/Marvel activity account explicitly describes Lang shrinking; not claim he cannot grow too.
20|Janet van Dyne Wasp. Storm,Natasha's Widow,Carol's Captain Marvel wrong. Publisher oral history explicitly Janet AKA Wasp; no universal claim no other Wasps exist.
21|Shield-star detail replaced with text-verified origin: super-soldier treatment. Spider bite,cosmic rays,symbiote other Marvel mechanisms. Captain Americas publisher guide explicitly Steve recipient of serum. Avoid treating uninspected cover artwork as reviewed visual evidence.
22|Hawkeye bow/arrows;trident,hammer,sword not signature archery equipment. Publisher reveal quiver/arrows and official RPG Hawkeye arrow discussion support. Most closely associated allows occasional use of other weapons.
23|Spider-sense warns impending danger. Not general mind-reading,lie detection or exact universal-distance measurement. Publisher biography explicit; replace stock-market/food-freshness joke options with distinguishable powers.
24|Wakanda vibranium, not Wolverine's adamantium,Asgardian uru,DC promethium. Publisher Panther villains account explicitly stolen precious vibranium in Wakanda. No claim found nowhere else in every later continuity.
25|Murdock loses sight, retains enhanced other senses. Hearing,smell,touch not lost in origin. Publisher Daredevil first-issue description explicitly blinded; not a real-world medical claim about radiation.
26|Banner Hulk most commonly green. Blue,pink,purple wrong for familiar form. Most commonly necessary because original grey Hulk and other incarnations exist. Publisher sheet explicitly green; no false always-green claim.
27|Sue Storm Invisible Woman. Jean,Natasha,Ororo other heroines. Publisher powers guide checked; no claim invisibility is her only ability, since force fields also central.
28|Johnny's body aflame, not ice,stone,sand. Official Human Torch flame-form profile. Human Torch name given but question asks power, not a physics assertion human skin can safely burn.
29|Thing rock-like skin, not glass,wood,water. Fantastic Four publisher history explicitly rock-like body. Resembles avoids uncertain literal geological composition.
30|Cloak flight claim replaced with straightforward identity: Stephen Strange is Doctor Strange. Hawkeye,Iron Man,Cap different people. Publisher Avengers roster explicitly pairs identity; distinct from existing former-surgeon question.
31|Wong longstanding Strange ally. Alfred,Gordon DC;Jameson Spider-Man editor. Official Wong comics history describes joint adventures. No servant-only stereotype or current office assumed.
32|Peter Quill Star-Lord. Surfer,Nova,Moon Knight different identities. Publisher character comics listing explicitly pairs name. Hyphen in Star-Lord correct.
33|Groot tree-like alien/Flora colossus, not human,robot,undersea king. Publisher character sheet explicitly PlanetX plant-being/regrowth. Avoid claiming ordinary Earth tree.
34|Rocket resembles raccoon, not fox,otter,badger. Publisher Rocket Raccoon character sheet. Resembles avoids conflating engineered extraterrestrial origin with ordinary terrestrial animal.
35|Adoptive-daughter prompt changed to readily verifiable team membership: Gamora best known as Guardian. FF,X-Men,New Mutants wrong core association. Official top-ten Guardians explicitly lists her; no claim exclusive membership in every story.
36|Drax the Destroyer, not Strange's Sorcerer Supreme,Daredevil's Man Without Fear,Aquaman's king title. Publisher Drax issue description explicitly Destroyer. No MCU literal-idiom personality generalisation.
37|Vision android/syntheticbody, other offered heroes human. Publisher Avengers history explicitly creation of android Vision. No claim every subsequent reconstructed body identical.
38|Quicksilver super speed, not plants,metalbody,underwater breathing. Publisher Young Avengers compares Speed's powers to Pietro. Best-known qualifier accommodates unusual temporary powers.
39|Pietro/Wanda twins, not fatherdaughter/uncleniece/married. Publisher Quicksilver fast facts explicitly Wanda's twin. Avoid disputed/retconned parentage entirely.
40|Silver Surfer cosmic surfboard, not Nova,Quill,Warlock's characteristic transport. Publisher Silver Surfer issue describes Dawn joining his board to explore universe and facsimile specifically his board. No numeric speed claim.
41|Galactus Devourer of Worlds, not Doom,Kingpin,Goblin. Replace diet question with silly only-books/sandwiches alternatives. Official Galactus/world-devouring publisher account supports title; no physical cosmology claim.
42|Doom Latveria, not Wakanda,Genosha,Sokovia. Publisher Doom2025 issue places his rule behind Latverian borders; classic fictional-country association not claim he never rules other territories.
43|Loki adopted brother, not biological father,son,grandfather. Publisher Loki comics history explicit adopted sibling; scope Marvel Thor, not inconsistent real-world myth genealogy.
44|Norman Osborn original Green Goblin. Octavius DocOck,Fisk Kingpin,Connors Lizard. Original qualifier avoids Harry/other later Goblins. Publisher Goblin reading guide and history checked.
45|Doctor Octopus four mechanical tentacles;wing harness,wheel,robotspider other gear. Publisher bio explicitly four mechanical tentacle-like arms. Distinguish mechanical count from his four natural limbs; better alternatives replace joke glove option.
46|Kingpin Wilson Fisk, not Osborn,Doom,Brock. Publisher Kingpin profile explicitly identity. Question not nickname-of-every-crime-boss terminology.
47|Eddie Brock famous Venom host. Alfred,Gordon,Clark different DC characters. Publisher Venom reading guide explicitly Eddie bond; not first living thing or only host, since Peter and others also hosted symbiote.
48|Johnny Blaze Ghost Rider, not MoonKnight,IronFist,Daredevil. Publisher Spirits of Vengeance history calls him motorcycle stunt rider and Rider. Multiple Ghost Riders permitted, no unique-only claim.
49|Cage strength and tough skin. Elasticlimbs,claws,electric skin other abilities. Publisher reading guide explicit strength/unbreakable skin; bullet-resistant rather than absolute immunity keeps reasonable fictional qualification.
50|Danny Rand Iron Fist. Luke,Murdock,Castle different martial/street heroes. Publisher IronFist1975 issue explicitly Danny AKA Iron Fist. No claim Rand only historical bearer.
51|Bruce Wayne Batman, not Kent,Queen,Luthor. DC biography and history explicit. Best-known qualifier accommodates other Batmen/continuities.
52|Batmobile car;InvisibleJet aircraft,Quinjet aircraft,SpiderMobile another hero. DC history explicitly customised Batmobile. Not falsely named every vehicle used by Batman.
53|Batarang bat-shaped thrown weapon, not torpedo,wristlaser,sword. DC Batman biography identifies utility-belt Batarangs; distinct from ordinary biological bat. No claim every version returns like a real boomerang.
54|Kryptonite famous vulnerability, not quartz/granite/diamond. Official DC kryptonite discussion inspected. No colour-specific claim that could confuse green/gold/red variants or other weaknesses such as magic.
55|Heat vision from eyes;ears,knees,feet wrong. DC heat-vision history explicit eye-based visual power. No false claim actual x-rays work this way.
56|Kara Zor-El Supergirl, not WonderWoman,Batgirl,Canary. DC Supergirl comics description explicitly names Kara. Proper spelling excludes Kara Zor-L/Power Girl of another Earth.
57|Kara usual Superman cousin, not mother/daughter/grandmother. DC Girl of Steel collection explicit cousin. Usual continuity avoids unrelated Supergirl versions and different origin timelines.
58|Lasso of Truth correct;GoldenWeb,RopeDreams,SilverSnare wrong. DC defining WonderWoman moments explicitly iconic Lasso of Truth. Traditional name, not claim she cannot own other ropes/artifacts.
59|Barry Allen Flash, not Lantern,Arrow,Aquaman. DC Flash biography explicitly Jay,Barry,Wally as title bearers. No only-Flash or first-Flash assertion.
60|Roy's first sidekick identity Speedy. Robin/KidFlash/Aqualad belong elsewhere. DC Arsenal biography explicitly former Speedy,Arrow sidekick; later Arsenal/Red Arrow not offered.
61|Joker Clown Prince of Crime, not Penguin,TwoFace,Bane. DC biography uses epithet. Fictional criminal title, not real formal royal rank.
62|Oswald Cobblepot Penguin, not Joker,Riddler,Scarecrow. Official DC Penguin biography explicit. Comic scope avoids altered surname in some screen adaptations.
63|Victor Fries Mr.Freeze, not Dent's TwoFace,Bane,Cobblepot. Initial mr-freeze URL wrong; actual DC entry mister-freeze checked. Fries spelling correct, not Fries/Freeze conflation.
64|Pamela Isley Poison Ivy. Harleen,Selina,Talia other characters. DC PoisonIvyThorns publisher description explicitly Pamela. No assertion current stories always define her purely villain rather than antihero.
65|Former Robin JasonTodd RedHood;Dick Nightwing,Tim/ Damian otherRobins. DC RedHood biography explicit. Best-known avoids claiming nobody else ever wore RedHood identity, including Joker predecessor.
66|Barbara associated Batgirl, not Supergirl,Diana,Starfire. DC Batgirl description explicitly Barbara. Associated allows her Oracle role and Cassandra/Stephanie as other Batgirls.
67|Robin usually Batman crime-fighting partner, not father,Metropolis mayor,editor. DC Batman history original sidekick. Not claim every Robin biologically related or always a child.
68|Jaime Reyes BlueBeetle, not BoosterGold,Atom,PlasticMan. DC biography explicitly thirdBlueBeetle. No mistake calling Jaime first, given Garrett/Kord predecessors.
69|PlasticMan stretches/reshapes, not weather/sea-onlyspeech/iceproduction. DC biography and original archive collection explicit. Does not reduce all his transformations to one body size.
70|Trinity closely associated JusticeLeague. FF,XMen,Guardians Marvel groups. Official DC League introduction names Superman,Batman,WonderWoman. Not an assertion every era has identical founders or membership.
71|Asterix a Gaul;Viking,Aztec,Spartan different ancient peoples. Official character biography citizenship Gaul. Fictional story not historical claim he actually existed.
72|Strength comes from magic potion;spiderbite,armour,ring other superhero mechanisms. Official Asterix/Getafix text confirms potion. Temporary distinguishes Asterix from Obelix's sustained effect.
73|Official Obelix bio says small boy, so correct too-specific baby to small boy. Potioncauldron explains persistent strength;newrecipe,poweredhelmet,Romangod false. Normally accounts for special-story exceptions.
74|Obelix famous menhir deliverer;goldobelisks,bathtubs,wheeledmillstones wrong iconic carried objects. Official Getafix text explicitly menhir deliverer and Asterix author-page menhirs. No conflation menhir vs obelisk despite punning name.
75|Dogmatix Obelix dog, not Tintin's Snowy,BeanoGnasher,PeanutsSnoopy. Official Dogmatix history explicitly Obelixwelcominglittle dog. English qualifier distinguishes French Idéfix.
76|Getafix potion-brewing druid;Cacofonix bard,Vitalstatistix chief,Unhygienix fishmonger. Official Getafix druid/potion biography. English-name qualification avoids Panoramix translations.
77|Cacofonix bard, not blacksmith,fishmonger,chief. Official bio calls bard and schoolteacher; question does not deny his second role. No qualitative opinion that music bad posed as fact.
78|Vitalstatistix chief, not other named villagers. Official character bio explicitly chief. English-language names and spelling checked.
79|Smurfs normally blue, not green/orange/purple. Official Smurf homepage explicitly blue and small. Usually accommodates purple/black transformations without pretending exceptions never exist.
80|Replace colour requiring uninspected picture with verified role. Papa wise elder/leader;Brainy,Hefty,Clumsy not village leader. Official homepage oldest/wisest/bigcheese description checked; no exact-age question.
81|Gargamel wizard pursuingSmurfs;Merlin,Getafix,Strange different fictionalmagicians. Official Smurf character text explicitly obsession with capture. Repeatedly allows failures and other story motives.
82|Gargamel cat Azrael, not Garfield,Felix,Tom. Official homepage explicitly Azraelthecat companion. No spelling confusion with DC Azrael hero due Smurf scope.
83|Replace uninspected costume detail with Smurfette created by Gargamel, not Papa,Brainy,Hefty. Official bio explicitly creation then Papa magic. Does not confuse creator with later transformation into kind Smurf.
84|British Dennis dog Gnasher, not Snowy,Snoopy,Odie. Official Beano Schools CustardCaper explicitly DoggyBFF. British qualifier essential because American Dennis different character and dog.
85|Dennis red/black stripedjumper. Bluewhite,greenyellow,purpleorange wrong. Official Beano WashingMachine description explicitly colours. Fix grammar by asking which two colours feature rather than what colours are jumper.
86|Minnie the Minx, not Magician,Mermaid,Mechanic. Authorised Beano educator resource character list explicitly name. Proper title, no factual judgment about a child's behaviour.
87|Roger chores reference missing, replace with verified publisher DCThomson. Marvel,Panini,Rebellion other comics publishers. DCThomson own Beano brand page checked; distinguish DCThomson from DC Comics.
88|BashStreetKids schoolsetting, not space,pirates,royalcourt. Official Beano school lesson and character education pack. Especiallyassociated avoids asserting adventures never leave school.
89|JollyJumper LuckyLukehorse. BlackBeauty,Silver,Bucephalus other horses. Original publisher Dargaud explicitly sonchevalJollyJumper; exact source replaces unavailable guessed English official URL.
90|LuckyLuke OldWest, not ancientEgypt,futurespace,medievalJapan. Licensed English publisher Cinebook catalogue explicitly classicWestern/OldWest. Mainly allows travel stories and historical fantasy humour.
91|Graphic novel book-length sequentialart/textstory, not prose-only,script-only,audio. Cambridge explicit longstorymostlypictures with writing. No false requirement all graphic novels fiction or originally one volume.
92|Comicstrip sequentialdrawingsstory, not proseeditorial,stage scene,audiodrama. Cambridge definition checked, but don't require all strips funny despite introductory wording. Replace unrelated pricing/index alternatives with actual narrative formats.
93|Speechbubble usuallyspokenwords, not credits,gutter,address. Dictionary and Scholasticdialogue examples checked; usually allows nonstandard artistic usage. Distinct from thoughtballoon94.
94|Thoughtbubble thoughts, not spokenaloud,authorname,price. Dedicated Cambridge definition checked rather than ordinary thought-bubble politicalidea meaning. No claim thoughts must be voiced to audience.
95|Panel individualpicture/section. Gutter,dialoguewords,entireseries otherunits. Generic panel dictionary lacked comic sense, so use Scholastic educatorguide; remove framed requirement because guide explicitly notes borderless panels.
96|Inker mechanism not established by ink dictionary. Replace with caption narration/descriptivebox using Scholastic text explicitly wordsinboxesnotspoken. Gutter,pageoutline,retailprice not usualcaption purpose. Usually allows internalmonologue/othercaption conventions.
97|Lettering words/visualstyle. Pencilart,colour,binding distinctproductionaspects. Cambridge lettering writing in particularstyle/colour; no assertion letterer necessarilyauthorsscript.
98|BANG/SPLASH imitate sounds, so onomatopoeia;anagram,palindrome,acronym do not define these examples. Actual Cambridge sound-imitation definition. Original prompt remains clear with both examples ordinary English soundwords.
99|Anthology repeated Books definition, replace with gutter betweenpanels. Speechballoon,caption,splashpage differentcomic elements. Scholastic explicitly defines spacesbetweenpanels as gutters. Space need not white or uniformlywide.
100|Manga Japanesecomics, unlike animeJapaneseanimation,Koreandrama,Chinesemartialarts. Cambridge Japanesecomicbooks definition checked. Distinguishes manga from anime without claiming all manga published in English remain in Japanese language.
'''
out=[]
for line in notes.strip().splitlines():
 n,note=line.split('|',1);n=int(n)
 edits.setdefault(n,{})['rationale']=note
 out.append({'row':n,'prompt':draft[n-1]['prompt'],'action':'edit','note':note,'recommendedChanges':edits[n],'sourceReview':'Explicit author second pass of the question, all four options, single correct offered answer, grammar, comic continuity/translation scope and category relevance. Source retrieval failures are retained; applicable indexed publisher passages or retrieved reference text identified in source-access metadata. Not independent review.'})
assert [x['row'] for x in out]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'reviewer':'root (author second editorial pass)','independent':False,'sourceAccessNote':'100 explicit author judgments. Original profile-path guesses blocked or obsolete; actual publisher biographies, indexed comics descriptions, official character sheets and authorised educational references used as applicable. Indexed passages are not claimed to be full-text retrieval. Revised several questions to text-verifiable alternatives; corrected Obelix small-boy age, Dennis jumper grammar, borderless panels, and repeated Books anthology concept. Private excerpts not republished.','rows':out},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('100 explicit author checks recorded; drafts still require applying changes and validation')
