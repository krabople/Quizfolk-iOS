"""Original accessible mythology candidates. Each still needs its final individual check."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
sources={
'olympians':'https://art.thewalters.org/object/23.40/',
'heroes':'https://www.theoi.com/greek-mythology/heroes.html',
'roman':'https://resources.metmuseum.org/resources/metpublications/pdf/Roman_Art_A_Resource_for_Educators.pdf',
'norse':'https://www.historiskmuseum.no/english/exhibitions/midgardr/index.html',
'odin':'https://historiska.se/en/explore-history/history-hub/odin-leader-of-the-gods/',
'egypt':'https://www.ucl.ac.uk/museums-static/digitalegypt/religion/deitiesplaces.html',
}
rows='''olympians|Which Greek goddess is especially associated with love and beauty?|Aphrodite|Demeter|Hestia|Artemis|Aphrodite is goddess of love and beauty; the other goddesses have different principal associations.
olympians|Which Greek goddess is especially associated with hunting?|Artemis|Aphrodite|Hestia|Demeter|Artemis is goddess of the hunt; the alternatives concern love, hearth and agriculture.
olympians|Which Greek goddess is especially associated with agriculture and the harvest?|Demeter|Hestia|Hera|Aphrodite|Demeter concerns agriculture; Hestia hearth, Hera marriage and Aphrodite love.
olympians|Which Greek goddess is associated with the hearth and home?|Hestia|Artemis|Aphrodite|Athena|Hestia is the hearth goddess; other goddesses differ.
olympians|Which Greek god is the messenger of the gods?|Hermes|Ares|Hephaestus|Dionysus|Hermes is the divine messenger; alternatives are war, metalworking and wine gods.
Khthonios/Haides|Which Greek god rules the underworld?|Hades|Zeus|Apollo|Hermes|Hades rules the underworld; Hermes guides souls but is not its ruler.
mount-olympus|Which mountain is traditionally the home of the Olympian gods?|Mount Olympus|Mount Etna|Mount Vesuvius|Mount Sinai|Olympus is their traditional home; other mountains are not the Olympian seat.
olympians|Which three-pronged weapon is a familiar attribute of Poseidon?|A trident|A bow|A sling|A spear with one point|Poseidon's trident has three prongs; other weapons do not match.
olympians|Which weapon is especially associated with Zeus in Greek art?|A thunderbolt|A trident|A bow|A hammer|Zeus wields a thunderbolt; the alternatives are associated with other deities or heroes.
olympians|Which bird is especially associated with Athena?|The owl|The swan|The peacock|The dove|Athena's familiar bird is the owl; other birds have other associations.
Olympios/Hermes|What feature of Hermes's sandals is often shown in Greek and Roman art?|Wings|Wheels|Claws|Hooves|Winged sandals indicate the messenger's speed; the other features do not describe the usual attribute.
Olympios/Hera|Which bird is especially associated with Hera in classical mythology?|The peacock|The owl|The eagle|The swallow|Hera is associated with the peacock, unlike Athena's owl and Zeus's eagle.
Olympios/Aphrodite|In a familiar account of Aphrodite's birth, she emerges from what?|Sea foam|A burning tree|A mountain cave|A rain cloud|The Hesiodic account has her arise from sea foam; variants of parentage are excluded by scope.
Olympios/Demeter|Who is Persephone's mother in Greek mythology?|Demeter|Hera|Hestia|Artemis|Demeter is Persephone's mother; the other goddesses are not.
Khthonios/Kharon|Who ferries souls across a river to the Greek underworld?|Charon|Chiron|Cronus|Cerberus|Charon is the ferryman; Chiron a centaur, Cronus a Titan and Cerberus the guard dog.
Potamos/Styx|Which of these rivers belongs to the Greek mythological underworld?|The Styx|The Thames|The Nile|The Tiber|Styx is an underworld river; the other rivers are real-world alternatives, not the named mythic boundary here.
Ther/Kerberos|In the most familiar depictions, how many heads does Cerberus have?|Three|One|Two|Seven|Cerberus commonly has three heads; ancient variants exist, so prompt qualifies the familiar depiction.
Pontios/Gorgones|In familiar Greek depictions, what grows on Medusa's head in place of hair?|Snakes|Feathers|Flowers|Antlers|Medusa has snake hair in familiar versions; the other features are not the traditional motif.
Pontios/Gorgones|What happens to people who look directly at Medusa in the familiar Greek story?|They turn to stone|They become invisible|They turn into birds|They lose their shadows|Medusa's gaze petrifies; the other magical effects are not hers.
Gigante/GigantesKyklopes|What is the distinctive eye arrangement of a Cyclops?|One eye in the centre of the forehead|Three eyes around the head|Two eyes on long stalks|No eyes at all|Cyclopes are one-eyed; other arrangements do not describe the mythic beings.
Ther/Hydra|What kind of monster is the Lernaean Hydra?|A many-headed serpent|A winged horse|A one-eyed giant|A half-human horse|Hydra is a many-headed serpent; Pegasus, Cyclops and centaur descriptions are alternatives.
heroes|Which Greek hero kills the Minotaur in the Labyrinth?|Theseus|Jason|Orpheus|Perseus|Theseus slays the Minotaur; the other heroes have different adventures.
heroes|In Greek legend, who is Icarus's father and the maker of their wings?|Daedalus|Minos|Theseus|Midas|Daedalus makes the wings and is Icarus's father; others are different figures.
heroes|In the story of Icarus, what happens when he flies too close to the Sun?|The wax holding his wings melts|His wings turn to stone|He becomes a god|The Sun stops moving|Heat melts the wax, causing the artificial wings to fail.
Heros/Midas|What does King Midas's famous touch turn things into?|Gold|Silver|Stone|Ice|The golden touch changes contacted objects to gold, not the other materials.
heroes|In Greek myth, Narcissus falls in love with whose reflection?|His own|His father's|Zeus's|Apollo's|Narcissus is captivated by his own reflected image; other people are wrong.
Nymphe/NympheEkho|What is the nymph Echo left able to repeat in the familiar Greek story?|The last words spoken by others|Only birdsong|Only her own name|Only the first word of a sentence|Echo can repeat another's final words, not freely speak complete new thoughts.
Heroine/Pandora|In the traditional story of Pandora's jar, what remains inside after its lid is closed?|Hope|Youth|Gold|Victory|Hope, Elpis, remains; interpretations of its meaning vary but the named thing is hope.
heroes|Into what creature is the weaver Arachne transformed?|A spider|A bee|A butterfly|A scorpion|Arachne becomes a spider, continuing the weaving association.
Titan/TitanAtlas|In classical Greek myth, what is Atlas condemned to hold up?|The sky|The Earth|The Moon|The sea|Atlas bears the heavens; popular pictures of a globe can cause the Earth misconception.
Titan/Phaethon|Which vehicle does Phaethon unsuccessfully try to drive in Greek myth?|The chariot of the Sun|Poseidon's boat|Hermes's wagon|Hades' coach|Phaethon drives the solar chariot and loses control; other vehicles are not his story.
nectar|In Greek mythology, what is nectar?|The drink of the gods|The gods' armour|A river in the underworld|A sacred weapon|Nectar is divine drink in the ordinary classical distinction; other categories are wrong.
ambrosia|In Greek mythology, what is ambrosia commonly described as?|The food of the gods|A king's crown|A hero's shield|A sea monster|Ambrosia is divine food in the familiar distinction from nectar.
Khthonios/Tartaros|What is Tartarus in Greek mythology?|A deep place of imprisonment and punishment|A mountain where the Muses sing|A flying horse|A magical cloak|Tartarus is the deep underworld prison, not a mountain, animal or garment.
Daimon/Hypnos|Which Greek deity personifies sleep?|Hypnos|Thanatos|Eros|Ares|Hypnos is sleep; Thanatos death, Eros love/desire and Ares war.
roman|Who is king of the gods in Roman mythology?|Jupiter|Mercury|Mars|Vulcan|Jupiter is the chief Roman deity; the others have different roles.
roman|Which Roman goddess is especially associated with marriage and is Jupiter's wife?|Juno|Venus|Diana|Minerva|Juno is Jupiter's consort and marriage goddess; alternatives differ.
roman|Which Roman god is especially associated with the sea?|Neptune|Jupiter|Mercury|Vulcan|Neptune is the sea god; the others concern sky, messages/trade and fire.
roman|Which Roman goddess is especially associated with love and beauty?|Venus|Minerva|Diana|Ceres|Venus is the love/beauty goddess; others concern wisdom, hunt and agriculture.
roman|Which Roman god is the messenger of the gods?|Mercury|Mars|Neptune|Vulcan|Mercury is the messenger; alternatives are other Roman deities.
roman|Which Roman goddess is especially associated with hunting?|Diana|Venus|Juno|Ceres|Diana is the hunt goddess; alternatives have different principal roles.
roman|Which Roman goddess is especially associated with wisdom?|Minerva|Venus|Diana|Juno|Minerva is wisdom and crafts goddess; the others differ.
roman|Which Roman goddess is especially associated with agriculture and grain?|Ceres|Diana|Juno|Venus|Ceres is the grain/agriculture goddess, linked with Demeter.
roman|Which Roman god is especially associated with wine?|Bacchus|Mercury|Mars|Neptune|Bacchus is the wine deity; the others have different domains.
vesta|Which Roman goddess is associated with the hearth and its sacred fire?|Vesta|Venus|Diana|Juno|Vesta is the hearth goddess, distinct from the alternatives.
pluto|Which Roman god is associated with ruling the underworld?|Pluto|Jupiter|Mercury|Mars|Pluto rules the underworld in the familiar Greco-Roman pairing; Mercury guides souls but does not rule.
cupid|Which weapons is Cupid commonly shown carrying?|A bow and arrows|A hammer and tongs|A trident and net|A sword and shield|Cupid's arrows inspire love; alternatives describe other symbolic equipment.
janus|How many faces is the Roman god Janus usually shown with?|Two|One|Three|Four|Janus is usually two-faced, looking in opposite directions.
saturn|Which Roman god is traditionally associated with sowing and agriculture?|Saturn|Mars|Mercury|Vulcan|Saturn is an agricultural deity; Ceres is deliberately not offered as another plausible agricultural answer.
aurora|Aurora is the Roman goddess of what?|The dawn|The deep sea|The hearth|The harvest|Aurora personifies dawn; the other domains belong to other deities.
flora|Flora is the Roman goddess especially associated with what?|Flowers and flowering plants|Storms at sea|Blacksmithing|Warfare|Flora is the flowering goddess; alternatives are other domains.
fortuna|Which Roman goddess personifies luck and fortune?|Fortuna|Diana|Juno|Vesta|Fortuna personifies fortune; the alternatives differ.
romulus|In the Roman foundation legend, which animal suckles Romulus and Remus?|A she-wolf|A lioness|A mare|A doe|A she-wolf nurses the twins in the familiar legend.
romulus|Which legendary twin is said to have founded Rome?|Romulus|Remus|Castor|Pollux|Romulus is the traditional founder; Remus dies in the foundation narrative, Castor/Pollux are other twins.
heroes|Which Trojan hero is the central figure of Virgil's Aeneid?|Aeneas|Achilles|Theseus|Jason|Aeneas is the epic's protagonist; the others belong to different Greek stories.
norse|In Norse mythology, Thor is especially associated with what?|Thunder|The harvest Moon|The underworld's dead|Writing laws|Thor is the thunder god; other options are not his defining association.
odin|In familiar Norse tradition, how many eyes does Odin have after his sacrifice for wisdom?|One|Two|Three|Four|Odin sacrifices one of his two eyes, leaving one.
norse|How many legs does Odin's horse Sleipnir have?|Eight|Four|Six|Ten|The museum describes Sleipnir as eight-legged; other counts are wrong.
norse|What kind of creature is Fenrir in Norse mythology?|A wolf|A horse|An eagle|A dragon|Fenrir is the giant wolf, not the other creatures.
norse|What kind of creature is Jormungandr, the Midgard Serpent?|A huge snake|A giant eagle|A three-headed dog|A winged horse|Jormungandr is the world serpent; the named epithet and standard description agree.
valhalla|In Norse mythology, Valhalla is especially associated with which people after death?|Warriors killed in battle|Only sailors lost at sea|Only children|Only farmers|Valhalla is Odin's hall of chosen battle-slain warriors; prompt avoids claiming all dead people go there.
valkyrie|What role do Valkyries have in Norse mythology?|Choosing warriors slain in battle|Guarding the apples of youth|Forging Thor's hammer|Holding up the sky|Valkyries choose the slain; other tasks belong elsewhere.
midgard|In Norse mythology, Midgard is the realm especially associated with whom?|Human beings|Only giants|Only dwarfs|Only dragons|Midgard is the human world; other beings inhabit other mythic places.
asgard|In Norse mythology, Asgard is the home of which group?|The Aesir gods|Only mortal kings|Only sea monsters|Only ordinary farmers|Asgard houses the Aesir; naming them avoids treating every divine group as exclusively based there.
loki|Which Norse figure is especially known as a trickster and shapeshifter?|Loki|Thor|Baldr|Heimdall|Loki is the familiar trickster/shapeshifter; the alternatives are not chiefly characterised that way.
tyr|In Norse myth, which god loses a hand when the wolf Fenrir is bound?|Tyr|Thor|Baldr|Njord|Tyr places his hand in Fenrir's mouth and loses it.
gungnir|What kind of weapon is Odin's Gungnir?|A spear|A hammer|A bow|An axe|Gungnir is Odin's spear; hammer is Thor's weapon instead.
freyja|In Norse mythology, which animals pull Freyja's chariot?|Cats|Goats|Wolves|Horses|Freyja's chariot is cat-drawn; Thor's is drawn by goats.
egypt|Which ancient Egyptian god is especially associated with the Sun?|Ra|Osiris|Anubis|Sobek|Ra/Re is the solar deity; other options have different main associations.
egypt|In the Egyptian Osiris myth, who is Osiris's wife?|Isis|Nut|Sekhmet|Bastet|Isis is his wife; alternatives are other Egyptian goddesses.
egypt|Which bird's head is Horus commonly shown with in Egyptian art?|A falcon's|An owl's|A swan's|A peacock's|Horus is falcon-headed in familiar imagery; other birds do not identify him.
sobek|Which animal is especially associated with the Egyptian god Sobek?|The crocodile|The cat|The ibis|The ram|Sobek is the crocodile deity, not the other animal associations.
taweret|The Egyptian goddess Taweret is commonly shown with the body of which animal?|A hippopotamus|A cow|A lioness|An eagle|Taweret is principally hippopotamus-shaped, with additional composite details; not purely one animal.
khepri|Which insect is especially associated with the Egyptian god Khepri?|The scarab beetle|The butterfly|The dragonfly|The mosquito|Scarab beetle represents Khepri, linked to the rising Sun.
egypt|Which Egyptian god is especially associated with ruling the realm of the dead?|Osiris|Sobek|Khnum|Bes|Osiris rules the dead; other deities are different even though some protect funerary rituals.
ankh|What does the ankh symbol represent in ancient Egyptian tradition?|Life|War|Silence|Winter|The ankh is the life sign; the other abstractions are not its meaning.
unicorn|How many horns does the unicorn of familiar European legend have?|One|Two|Three|Four|A unicorn has one horn, not the other counts.
phoenix|In familiar legend, what does a phoenix rise from after it dies?|Its own ashes|A block of ice|A stone egg buried underground|A whirlpool|Phoenix rebirth from ashes is the familiar later legendary account.
griffin|A griffin traditionally combines an eagle's head and wings with the body of which animal?|A lion|A horse|A bull|A deer|Griffin is eagle/lion composite, not the other mammals.
mermaid|A mermaid is commonly shown with a human upper body and the tail of what?|A fish|A horse|A lion|A bird|The familiar mermaid has a fish tail; other animal tails describe different creatures.
werewolf|In folklore, a werewolf changes between human form and which animal form?|Wolf|Bear|Fox|Bat|Werewolf is human/wolf shapeshifter; a bat belongs to some vampire lore instead.
vampire|What do vampires feed on in familiar European folklore?|Blood|Nectar|Tree sap|Honey|Vampire is a blood-drinking revenant in the familiar tradition.
dragon|What are many European dragons said to breathe?|Fire|Snow|Glass|Sand|Fire-breathing is familiar European dragon trait; not claimed universal to all world dragons.
kraken|The kraken is traditionally a monster of which environment?|The sea|The desert|A volcano|An underground mine|Kraken is a gigantic sea monster of northern folklore.
excalibur|What kind of object is Excalibur in Arthurian legend?|A sword|A crown|A shield|A cup|Excalibur is Arthur's sword, not the other royal or quest objects.
guinevere|In Arthurian legend, Guinevere is the wife of which king?|Arthur|Mark|Uther|Pellinore|Guinevere is Arthur's queen; other Arthurian kings have different roles.
round-table|Why is Arthur's Round Table commonly interpreted as a symbol of equality among his knights?|It has no privileged seat at its head|It is made of gold|It belongs to every king|It has only one chair|A circular table has no head seat, giving equal seating status in the traditional explanation.
robin-hood|Which English forest is especially associated with Robin Hood?|Sherwood Forest|The New Forest|Epping Forest|Ashdown Forest|Sherwood is the familiar legendary setting; other forests are not the conventional answer.
robin-hood|Which sheriff is Robin Hood's traditional enemy?|The Sheriff of Nottingham|The Sheriff of York|The Sheriff of Exeter|The Sheriff of Dover|The Nottingham sheriff is the familiar antagonist in Robin Hood tales.
golden-goose|In the familiar fable, what valuable objects does the goose lay?|Golden eggs|Silver apples|Diamond feathers|Bronze coins|The goose lays golden eggs; other treasures do not match the fable.
monkey-king|Which animal is Sun Wukong, the Monkey King of Chinese literature?|A monkey|A tiger|A dragon|A crane|Sun Wukong is the supernatural monkey hero of Journey to the West.
change|In Chinese legend, Chang'e is especially associated with which celestial body?|The Moon|Mars|Saturn|The Sun|Chang'e is the moon goddess; alternatives are different celestial bodies.
hou-yi|In Chinese legend, Hou Yi is famous for using which weapon?|A bow and arrows|A trident|A war hammer|A sling|Hou Yi is the legendary archer who shoots excess suns.
kitsune|In Japanese folklore, a kitsune is what kind of animal?|A fox|A badger|A cat|A crane|Kitsune are foxes, often supernatural shapeshifters in folklore.
kappa|In Japanese folklore, the kappa is especially associated with which habitat?|Rivers and ponds|Desert dunes|Volcanic craters|High mountain snowfields|Kappa are water beings, not creatures of the other environments.
kelpie|In Scottish folklore, what animal form does a kelpie commonly take?|A horse|A lion|An eagle|A wolf|Kelpie is a water spirit commonly taking horse form; shape-changing variants acknowledged.
selkie|In Scottish and Irish folklore, selkies change between human form and which animal form?|Seal|Dolphin|Otter|Whale|Selkies are seal folk who shed their skins to take human form.
baba-yaga|In familiar Russian tales, Baba Yaga's hut stands on what?|Chicken legs|Wagon wheels|Giant mushrooms|Golden pillars|Chicken-legged hut is a familiar Baba Yaga motif; other supports do not fit.
bunyip|The bunyip belongs to the traditional stories of Indigenous peoples of which country?|Australia|Norway|Japan|Peru|Bunyip is an Aboriginal Australian water-being tradition; alternatives are other regions.
quetzalcoatl|The name Quetzalcoatl is commonly translated as what?|Feathered serpent|Golden eagle|Jaguar king|Moon rabbit|Quetzalcoatl is the feathered/precious serpent; other phrases identify different symbolic animals.
'''
def source(key):
    if key in sources:return sources[key]
    if '/' in key:return 'https://www.theoi.com/'+key+'.html'
    return 'https://dictionary.cambridge.org/dictionary/english/'+key
if __name__=='__main__':
 q=[]
 for line in rows.strip().splitlines():
  key,prompt,correct,*tail=line.split('|');assert len(tail)==4
  q.append({'draftID':f'easy-20-{len(q)+1:03d}','categoryID':'20','difficulty':'easy','prompt':prompt,'answers':[correct,*tail[:3]],'correctIndex':0,'rationale':tail[3],'sourceURL':source(key),'reviewStatus':'draft_awaiting_author_final_check'})
 assert len(q)==100,len(q)
 (HERE/'draft.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('100 unapproved mythology candidates')
