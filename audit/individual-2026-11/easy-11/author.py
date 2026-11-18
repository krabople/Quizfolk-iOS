"""Original accessible film candidates. Final individual checks still required."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
sources={
'toy-story':'https://www.pixar.com/feature-films/toy-story',
'finding-nemo':'https://www.pixar.com/feature-films/finding-nemo',
'ratatouille':'https://www.pixar.com/feature-films/ratatouille',
'wall-e':'https://www.pixar.com/feature-films/wall-e',
'up':'https://www.pixar.com/feature-films/up',
'cars':'https://www.pixar.com/feature-films/cars',
'monsters-inc':'https://www.pixar.com/feature-films/monsters-inc',
'inside-out':'https://www.pixar.com/feature-films/inside-out',
'coco':'https://www.pixar.com/feature-films/coco',
'brave':'https://www.pixar.com/feature-films/brave',
'incredibles':'https://www.pixar.com/feature-films/the-incredibles',
'turning-red':'https://www.pixar.com/feature-films/turning-red',
'lion-king':'https://movies.disney.com/the-lion-king',
'aladdin':'https://movies.disney.com/aladdin',
'frozen':'https://movies.disney.com/frozen',
'little-mermaid':'https://movies.disney.com/the-little-mermaid',
'beauty-beast':'https://movies.disney.com/beauty-and-the-beast',
'mulan':'https://movies.disney.com/mulan',
'cinderella':'https://movies.disney.com/cinderella',
'snow-white':'https://movies.disney.com/snow-white-and-the-seven-dwarfs',
'shrek':'https://www.dreamworks.com/movies/shrek',
'kung-fu-panda':'https://www.dreamworks.com/movies/kung-fu-panda',
'dragon':'https://www.dreamworks.com/movies/how-to-train-your-dragon',
'madagascar':'https://www.dreamworks.com/movies/madagascar',
'trolls':'https://www.dreamworks.com/movies/trolls',
'croods':'https://www.dreamworks.com/movies/the-croods',
'megamind':'https://www.dreamworks.com/movies/megamind',
'jurassic':'https://www.universalpicturesathome.com/movies/jurassic-park',
'et':'https://www.universalpicturesathome.com/movies/et-the-extra-terrestrial',
'back-future':'https://www.universalpicturesathome.com/movies/back-to-the-future',
'ghostbusters':'https://www.sonypictures.com/movies/ghostbusters',
'oz':'https://www.warnerbros.com/movies/wizard-oz',
'mary-poppins':'https://movies.disney.com/mary-poppins',
'home-alone':'https://www.20thcenturystudios.com/movies/home-alone',
'titanic':'https://www.20thcenturystudios.com/movies/titanic',
'indy':'https://www.lucasfilm.com/productions/raiders-of-the-lost-ark/',
'bond':'https://www.007.com/the-films/',
'rocky':'https://www.mgm.com/movies/rocky',
'matrix':'https://www.warnerbros.com/movies/matrix',
'mask':'https://www.warnerbros.com/movies/mask',
'pirates':'https://movies.disney.com/pirates-of-the-caribbean-the-curse-of-the-black-pearl',
'forrest':'https://www.paramountmovies.com/movies/forrest-gump',
'harry':'https://www.harrypotter.com/fact-file/characters-and-pets/harry-potter',
'hermione':'https://www.harrypotter.com/fact-file/characters-and-pets/hermione-granger',
'hogwarts':'https://www.harrypotter.com/fact-file/locations/hogwarts',
'dumbledore':'https://www.harrypotter.com/fact-file/characters-and-pets/albus-dumbledore',
'hagrid':'https://www.harrypotter.com/fact-file/characters-and-pets/rubeus-hagrid',
'dobby':'https://www.harrypotter.com/fact-file/characters-and-pets/dobby',
}
rows='''1|toy-story|In Toy Story, what kind of toy is Woody?|A cowboy doll|A toy soldier|A robot|A racing car|Woody is a pull-string cowboy doll; alternatives describe other toy types.
2|toy-story|In Toy Story, Buzz Lightyear believes he is what?|A Space Ranger|A pirate captain|A cowboy sheriff|A racing driver|Buzz believes he is an actual Space Ranger rather than a toy.
3|finding-nemo|In Finding Nemo, what kind of fish is Nemo?|Clownfish|Goldfish|Swordfish|Angelfish|Nemo is a clownfish, not the other fish types.
4|finding-nemo|In Finding Nemo, what is Marlin's relationship to Nemo?|His father|His brother|His uncle|His grandfather|Marlin is Nemo's father; other family relations are wrong.
5|finding-nemo|What difficulty does Dory famously have in Finding Nemo?|Short-term memory loss|An inability to swim|A fear of every fish|An inability to speak|Dory has short-term memory loss, not the alternatives.
6|ratatouille|In Ratatouille, what kind of animal is Remy?|A rat|A mouse|A rabbit|A squirrel|Remy is a rat and aspiring chef; mouse is a plausible but wrong near alternative.
7|ratatouille|In which city is most of Ratatouille set?|Paris|Rome|London|Madrid|The restaurant adventure takes place in Paris.
8|wall-e|In WALL-E, what task was the title robot built to do?|Compact rubbish|Deliver the mail|Pilot racing cars|Cook restaurant meals|WALL-E compacts abandoned waste on Earth.
9|up|In Up, what lifts Carl's house into the sky?|Thousands of balloons|A giant helicopter|A team of dragons|A rocket engine|Balloons lift the house; the alternatives do not cause its flight.
10|cars|What kind of vehicle is Lightning McQueen in Cars?|A racing car|A fire engine|A farm tractor|A school bus|Lightning McQueen is a racing car, not the other vehicle types.
11|cars|In Cars, what kind of vehicle is Mater?|A tow truck|A racing car|A fire engine|A bus|Mater is a rusty tow truck, not the alternatives.
12|monsters-inc|In Monsters, Inc., how many eyes does Mike Wazowski have?|One|Two|Three|Four|Mike has one large central eye.
13|monsters-inc|In Monsters, Inc., what is Boo?|A human child|A robot|A talking cat|A monster's pet bird|Boo is a young human girl who enters the monster world.
14|inside-out|In Inside Out, Joy and Sadness are emotions inside whose mind?|Riley's|Andy's|Miguel's|Merida's|Riley is the child whose emotions drive the film; the others belong to other Pixar stories.
15|coco|Coco draws especially on the Day of the Dead traditions of which country?|Mexico|Italy|Japan|Greece|Coco is rooted in Mexican Dia de los Muertos traditions.
16|coco|In Coco, what does Miguel dream of becoming?|A musician|A racing driver|A doctor|An astronaut|Miguel dreams of being a musician despite the family's music ban.
17|brave|In Brave, Princess Merida is especially skilled at which sport?|Archery|Tennis|Ice skating|Swimming|Merida's signature skill is archery.
18|incredibles|What secret identity does the Parr family share in The Incredibles?|They are superheroes|They are aliens|They are pirates|They are robots|The Parr family are superheroes living under ordinary identities.
19|incredibles|In The Incredibles, what is Dash's main superpower?|Super speed|Invisibility|Breathing underwater|Turning into stone|Dash can run at superhuman speed; invisibility belongs to Violet.
20|turning-red|In Turning Red, Mei transforms into a giant version of which animal?|Red panda|Polar bear|Tiger|Fox|Mei transforms into a giant red panda when strongly emotional.
21|lion-king|In Disney's animated The Lion King (1994), what kind of animal is Simba?|A lion|A tiger|A leopard|A cheetah|Simba is the lion cub/prince, not another big cat.
22|lion-king|In The Lion King (1994), how is Scar related to Mufasa?|He is Mufasa's brother|He is Mufasa's son|He is Mufasa's father|He is Mufasa's grandson|Scar is Mufasa's brother, therefore Simba's uncle.
23|lion-king|In The Lion King (1994), what kind of animal is Timon?|A meerkat|A mongoose|An otter|A rabbit|Timon is a meerkat; other small mammals are wrong.
24|lion-king|In The Lion King (1994), what kind of animal is Pumbaa?|A warthog|A rhinoceros|A hippopotamus|A buffalo|Pumbaa is a warthog, not the other large African mammals.
25|aladdin|In Disney's animated Aladdin (1992), the Genie is released from what object?|A lamp|A mirror|A ring|A sword|The Genie featured in the film emerges from the magic lamp; ring-genies in other tales are excluded.
26|aladdin|What is the name of the princess in Disney's animated Aladdin (1992)?|Jasmine|Ariel|Aurora|Belle|Jasmine is Agrabah's princess; others are different Disney heroines.
27|aladdin|In Disney's animated Aladdin (1992), what kind of animal is Abu?|A monkey|A tiger|A parrot|A snake|Abu is Aladdin's monkey companion; Rajah is tiger and Iago parrot.
28|frozen|In Frozen, Elsa has magical powers especially involving what?|Ice and snow|Fire and lava|Sand and dust|Electricity and metal|Elsa controls ice and snow; alternatives not her powers.
29|frozen|In Frozen, who is Anna's sister?|Elsa|Rapunzel|Ariel|Merida|Elsa is Anna's older sister; other Disney princesses are different characters.
30|frozen|In Frozen, what is Olaf?|A snowman|A reindeer|A wolf|A polar bear|Olaf is an animated snowman, not an animal.
31|frozen|In Frozen, what kind of animal is Sven?|A reindeer|A moose|A horse|A wolf|Sven is Kristoff's reindeer companion.
32|little-mermaid|In Disney's animated The Little Mermaid (1989), what is Ariel at the beginning of the story?|A mermaid|A fairy|A witch|A human princess|Ariel begins as mermaid and later becomes human; timing qualifier necessary.
33|little-mermaid|Who is the sea witch in Disney's animated The Little Mermaid (1989)?|Ursula|Maleficent|Cruella de Vil|The Queen of Hearts|Ursula is the sea witch; other names are different Disney villains.
34|beauty-beast|What is the name of the heroine in Disney's animated Beauty and the Beast (1991)?|Belle|Jasmine|Aurora|Ariel|Belle is the heroine, not other Disney princesses.
35|beauty-beast|In Disney's animated Beauty and the Beast (1991), what enchanted object is Mrs Potts?|A teapot|A clock|A candlestick|A wardrobe|Mrs Potts is the teapot; other object characters are distinct.
36|beauty-beast|In Disney's animated Beauty and the Beast (1991), Lumiere takes the form of what object?|A candlestick|A clock|A teapot|A mirror|Lumiere is the enchanted candelabrum/candlestick, not other castle objects.
37|mulan|In Disney's animated Mulan (1998), Mulan joins the army disguised as whom?|A man|A royal princess|A merchant's wife|A foreign queen|Mulan disguises herself as a male soldier to serve in her father's place.
38|mulan|In Disney's animated Mulan (1998), what kind of creature is Mushu?|A dragon|A phoenix|A tiger|A crane|Mushu is the small dragon guardian, not the other creatures.
39|cinderella|In Disney's animated Cinderella (1950), what are Cinderella's famous slippers made of?|Glass|Gold|Silver|Silk|Glass slippers are the film's iconic footwear; other Cinderella traditions can differ so version specified.
40|snow-white|In Disney's Snow White and the Seven Dwarfs (1937), which poisoned fruit does the Queen offer Snow White?|An apple|A pear|A peach|A plum|The poisoned apple is the Queen's device in the specified animated film.
41|shrek|In the Shrek films, what kind of creature is Shrek?|An ogre|A troll|A giant|A goblin|Shrek is an ogre, not the related fantasy creatures.
42|shrek|Who voices Donkey in the original English-language Shrek (2001)?|Eddie Murphy|Mike Myers|Antonio Banderas|John Lithgow|Eddie Murphy voices Donkey; Myers Shrek, Banderas later Puss and Lithgow Farquaad.
43|kung-fu-panda|What is the name of the panda hero in Kung Fu Panda (2008)?|Po|Shifu|Tai Lung|Oogway|Po is the panda protagonist; alternatives name other characters.
44|dragon|What is the name of Hiccup's dragon in How to Train Your Dragon (2010)?|Toothless|Stormfly|Hookfang|Meatlug|Toothless is Hiccup's Night Fury; other dragons belong to other riders.
45|madagascar|In Madagascar (2005), what kind of animal is Alex?|A lion|A tiger|A zebra|A giraffe|Alex is the Central Park lion, not the other zoo animals.
46|madagascar|In Madagascar (2005), what kind of animal is Melman?|A giraffe|A hippopotamus|A zebra|A lion|Melman is a giraffe; other types identify his friends.
47|madagascar|In Madagascar (2005), what kind of animal is Marty?|A zebra|A giraffe|A lion|A hippopotamus|Marty is the zebra; other animals are his friends.
48|trolls|Which DreamWorks film features the characters Poppy and Branch?|Trolls|Shrek|The Croods|The Boss Baby|Poppy and Branch are the central Trolls characters.
49|croods|The Croods (2013) follows a family living in which kind of setting?|A prehistoric world|A futuristic space station|A modern office block|A medieval royal court|The Croods are a prehistoric cave-dwelling family; other settings wrong.
50|megamind|What colour is Megamind's skin in the animated film Megamind (2010)?|Blue|Green|Red|Orange|Megamind is blue-skinned, not the other colours.
51|jurassic|Which 1993 film features a theme park stocked with cloned dinosaurs?|Jurassic Park|Jaws|E.T. the Extra-Terrestrial|Raiders of the Lost Ark|Jurassic Park's central premise is cloned-dinosaur theme park.
52|jurassic|Who directed Jaws, E.T. the Extra-Terrestrial and Jurassic Park?|Steven Spielberg|James Cameron|George Lucas|Tim Burton|Spielberg directed all three; the other directors did not.
53|et|In E.T. the Extra-Terrestrial (1982), what kind of being is E.T.?|An alien visitor|A human astronaut|A robot|A dinosaur|E.T. is extraterrestrial alien stranded on Earth; title supports but not literally says animal/type among alternatives.
54|back-future|Which car model is turned into a time machine in Back to the Future (1985)?|DeLorean|Ford Mustang|Volkswagen Beetle|Mini Cooper|Doc's time machine is a DeLorean, not other models.
55|ghostbusters|Who plays Peter Venkman in Ghostbusters (1984)?|Bill Murray|Dan Aykroyd|Harold Ramis|Ernie Hudson|Murray plays Venkman; others play Ray, Egon, Winston.
56|oz|In The Wizard of Oz (1939), what does the Tin Man hope to receive?|A heart|A brain|Courage|A magic wand|Tin Man seeks heart; Scarecrow brain,Lion courage.
57|oz|In The Wizard of Oz (1939), what does the Scarecrow hope to receive?|A brain|A heart|Courage|A crown|Scarecrow wants brain; other companions' requests differ.
58|oz|In The Wizard of Oz (1939), what does the Cowardly Lion hope to gain?|Courage|A heart|A brain|Wings|Lion seeks courage; other wishes are not his.
59|oz|What is the name of Dorothy's dog in The Wizard of Oz (1939)?|Toto|Lassie|Snoopy|Pluto|Toto is Dorothy's dog; others different famous fictional dogs.
60|mary-poppins|What job does Mary Poppins do in the 1964 Disney film?|Nanny|Police officer|Doctor|School headteacher|Mary Poppins is the magical nanny of the Banks children.
61|home-alone|Who plays Kevin McCallister in Home Alone (1990)?|Macaulay Culkin|Elijah Wood|Daniel Radcliffe|Haley Joel Osment|Culkin plays Kevin; other child actors did not.
62|home-alone|In Home Alone (1990), Kevin's family flies to which city for Christmas?|Paris|Rome|Madrid|Berlin|The family holiday destination is Paris; film later New York sequel excluded.
63|titanic|Who plays Jack Dawson in Titanic (1997)?|Leonardo DiCaprio|Brad Pitt|Matt Damon|Johnny Depp|DiCaprio plays Jack; other actors wrong.
64|indy|What is Indiana Jones's profession?|Archaeologist|Astronaut|Marine biologist|Journalist|Indiana Jones is archaeology professor/adventurer; alternatives wrong profession.
65|bond|What is James Bond's agent number?|007|001|008|009|Bond is agent007; other numbers refer to other possible agents, not Bond.
66|rocky|In Rocky (1976), Rocky Balboa competes in which sport?|Boxing|Wrestling|Judo|Fencing|Rocky is a boxer; other combat sports wrong.
67|matrix|In The Matrix (1999), which coloured pill does Neo choose to learn the truth?|Red|Blue|Green|Yellow|Neo takes red pill; blue would return him to apparent ordinary life.
68|mask|Who plays Stanley Ipkiss in The Mask (1994)?|Jim Carrey|Robin Williams|Adam Sandler|Ben Stiller|Carrey stars as Stanley; other comic actors wrong.
69|pirates|Who plays Captain Jack Sparrow in Pirates of the Caribbean: The Curse of the Black Pearl (2003)?|Johnny Depp|Orlando Bloom|Geoffrey Rush|Javier Bardem|Depp plays Jack; Bloom Will,Rush Barbossa,Bardem later Salazar.
70|forrest|Who plays the title character in Forrest Gump (1994)?|Tom Hanks|Tom Cruise|Robin Williams|Kevin Costner|Hanks plays Forrest, not the other actors.
71|hogwarts|What is the name of the school Harry attends in the Harry Potter films?|Hogwarts|Durmstrang|Beauxbatons|Ilvermorny|Harry attends Hogwarts; other wizard schools not his school.
72|harry|What shape is Harry Potter's scar in the films?|A lightning bolt|A crescent moon|A star|A triangle|Lightning-shaped scar identifies Harry, not other symbols.
73|harry|What is the name of Harry Potter's owl in the films?|Hedwig|Errol|Pigwidgeon|Fawkes|Hedwig is Harry's snowy owl; others different magical birds.
74|harry|What is Ron's surname in the Harry Potter films?|Weasley|Malfoy|Longbottom|Diggory|Ron Weasley, not other wizard families.
75|hermione|Who plays Hermione Granger in the Harry Potter films?|Emma Watson|Emma Roberts|Saoirse Ronan|Dakota Fanning|Emma Watson plays Hermione; others did not.
76|dumbledore|Who is Hogwarts's headmaster in Harry Potter and the Philosopher's Stone (2001)?|Albus Dumbledore|Severus Snape|Sirius Black|Rubeus Hagrid|Dumbledore is headmaster in first film; later headmasters excluded by film scope.
77|hogwarts|Which magical item assigns new Hogwarts pupils to houses in the Harry Potter films?|The Sorting Hat|The Goblet of Fire|The Marauder's Map|The Invisibility Cloak|Sorting Hat allocates houses; other magical objects have different functions.
78|hogwarts|In the Harry Potter films, what do Quidditch players usually ride?|Broomsticks|Dragons|Flying carpets|Giant eagles|Quidditch is played on broomsticks; other fantasy transport not game equipment.
79|hagrid|In the Harry Potter films, Hagrid is half human and half what?|Giant|Goblin|Elf|Centaur|Hagrid is half-giant; alternatives wrong ancestry.
80|dobby|What kind of magical creature is Dobby in the Harry Potter films?|A house-elf|A goblin|A troll|A centaur|Dobby is a house-elf, not the other beings.
81|sw:darth-vader|In The Empire Strikes Back (1980), Darth Vader reveals that he is whose father?|Luke Skywalker's|Han Solo's|Obi-Wan Kenobi's|Yoda's|Vader reveals his paternity to Luke; alternatives not his sons.
82|sw:lightsaber|What is the glowing-bladed weapon used by Jedi in the Star Wars films called?|A lightsaber|A blaster|A vibro-axe|A bowcaster|Lightsaber is the energy-bladed Jedi weapon; other Star Wars weapons differ.
83|sw:yoda|Which Jedi Master trains Luke Skywalker on Dagobah in The Empire Strikes Back?|Yoda|Mace Windu|Qui-Gon Jinn|Count Dooku|Yoda trains Luke on Dagobah; other Jedi/Sith not that trainer.
84|sw:chewbacca|What species is Chewbacca in the Star Wars films?|Wookiee|Ewok|Hutt|Gungan|Chewbacca is a Wookiee, not the other species.
85|sw:r2-d2|In Star Wars, what kind of character is R2-D2?|A droid|A Wookiee|A Jedi Knight|A Sith Lord|R2-D2 is an astromech droid, not organic species or Force order title.
86|sw:millennium-falcon|What is the name of Han Solo's famous ship in the original Star Wars trilogy?|Millennium Falcon|Star Destroyer|Razor Crest|Ghost|Han flies Millennium Falcon; others are different classes/ships.
87|sw:death-star|What is the Death Star in Star Wars: A New Hope?|A space station|A natural moon|A desert planet|A lightsaber|Death Star is an armed battle station; famously mistaken for moon but artificial.
88|sw:leia-organa|Which Star Wars character is Luke Skywalker's twin sister?|Leia Organa|Padme Amidala|Rey|Ahsoka Tano|Leia is Luke's twin; Padme mother, others different characters.
89|sw:darth-vader|What was Darth Vader's name before he became a Sith Lord?|Anakin Skywalker|Luke Skywalker|Obi-Wan Kenobi|Bail Organa|Anakin becomes Vader; alternatives are other people.
90|sw:tatooine|On which desert planet does Luke Skywalker grow up?|Tatooine|Naboo|Coruscant|Hoth|Luke raised on Tatooine; Naboo verdant,Coruscant city,Hoth ice.
91|d:cinematography|Cinematography mainly concerns which aspect of filmmaking?|Camera work and visual photography|Writing song lyrics only|Selling cinema tickets|Choosing snacks for the audience|Cinematography is motion-picture photography/camera-lighting craft, not other duties.
92|d:storyboard|What is a storyboard used for when planning a film?|Showing planned shots as a sequence of drawings|Keeping the actors' shoes clean|Counting ticket sales|Recording catering orders|Storyboard visually plans scenes/shots before filming.
93|d:clapperboard|What is a clapperboard's clap especially useful for in filmmaking?|Synchronising separately recorded picture and sound|Making actors speak louder|Changing a camera's lens automatically|Writing dialogue during filming|Clap gives visible/audible sync point for separate audio/image recordings.
94|d:close-up|What does a close-up shot usually show?|A small subject or detail filling much of the frame|An entire landscape from far away|Only the film's title card|Several complete buildings from the air|Close-up frames a subject/detail closely, not wide establishing landscape.
95|d:pan|In camera work, what is a pan?|Turning the camera horizontally from a fixed position|Turning it vertically only|Replacing the soundtrack|Changing the actor's costume|Pan rotates horizontally, not tilt vertical or unrelated departments.
96|d:zoom|What does zooming a camera lens do?|Changes how large the subject appears without moving the camera closer|Makes the actors move faster|Changes every colour to black and white|Records dialogue automatically|Optical zoom changes focal length/image size without camera-position change.
97|d:silent-film|A traditional silent film typically lacks what?|Recorded spoken dialogue synchronised with the picture|Any visible actors|Any story|Any possible musical accompaniment|Silent films lack synchronised recorded spoken dialogue, not all sounds in exhibition.
98|d:subtitle|What are subtitles in a film?|Written words on screen representing dialogue|The names of the cinema seats|Only the opening music|The camera's lens settings|Subtitles display dialogue/translation on screen; other options unrelated.
99|d:stop-motion|How is stop-motion animation made?|Moving objects slightly between photographed frames|Filming live actors without any editing|Recording only sound and no images|Showing an entire film as one still photograph|Frame-by-frame repositioning creates apparent movement.
100|d:voice-actor|What does a voice actor mainly provide for an animated film?|A character's spoken performance|The design of every background|The sale of cinema tickets|The manufacture of camera lenses|Voice actor provides vocal character performance, not the other production/commercial tasks.
'''
def source(key):
 if key.startswith('sw:'):return 'https://www.starwars.com/databank/'+key[3:]
 if key.startswith('d:'):return 'https://dictionary.cambridge.org/dictionary/english/'+key[2:]
 return sources[key]
if __name__=='__main__':
 q=[]
 for line in rows.strip().splitlines():
  n,key,prompt,correct,*tail=line.split('|');assert len(tail)==4 and int(n)==len(q)+1
  q.append({'draftID':f'easy-11-{int(n):03d}','categoryID':'11','difficulty':'easy','prompt':prompt,'answers':[correct,*tail[:3]],'correctIndex':0,'rationale':tail[3],'sourceURL':source(key),'reviewStatus':'draft_awaiting_author_final_check'})
 assert len(q)==100
 (HERE/'draft.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('100 unapproved film candidates')
