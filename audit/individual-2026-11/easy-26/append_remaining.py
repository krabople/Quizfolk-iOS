"""Append80 candidates from inspected biography passages; does not approve publication."""
import json,pathlib,urllib.parse
H=pathlib.Path(__file__).parent;d=json.loads((H/'draft.json').read_text(encoding='utf8'));assert len(d)==20,'Do not overwrite later edits.'
raw='''Jeremy Clarkson|Which BBC motoring programme did Jeremy Clarkson present with Richard Hammond and James May?|Top Gear|The Grand Tour|Fifth Gear|Wheeler Dealers
Graham Norton|For which annual music competition has Graham Norton provided BBC television commentary?|The Eurovision Song Contest|The X Factor|The Voice|Britain's Got Talent
Claudia Winkleman|Who presented the UK version of The Traitors when it launched in 2022?|Claudia Winkleman|Davina McCall|Dermot O'Leary|Holly Willoughby
Alex Horne|Which comedy game show was created by Alex Horne?|Taskmaster|Would I Lie to You?|Mock the Week|8 Out of 10 Cats
Greg Davies|Which school subject did Greg Davies teach before his comedy career?|Drama|Mathematics|Chemistry|Geography
Jo Brand|What job did Jo Brand have before becoming a stand-up comedian?|Nurse|Architect|Journalist|Accountant
Romesh Ranganathan|Which subject did Romesh Ranganathan teach before becoming a full-time comedian?|Mathematics|History|Chemistry|Music
Lee Mack|Who became the host of the original UK version of The 1% Club in 2022?|Lee Mack|Rob Brydon|Alan Carr|David Mitchell
Michael McIntyre|Who was the original host of the BBC game show The Wheel?|Michael McIntyre|Greg Davies|Lee Mack|Rob Brydon
Kevin McCloud|Which Channel 4 series began in 1999 with Kevin McCloud as its presenter?|Grand Designs|Homes Under the Hammer|DIY SOS|Location, Location, Location
George Clarke (television presenter)|What profession did George Clarke of Amazing Spaces train for?|Architect|Chef|Veterinarian|Accountant
Nick Knowles|Which home-renovation programme is Nick Knowles known for presenting?|DIY SOS|Grand Designs|Homes Under the Hammer|Location, Location, Location
Fiona Bruce|Which newsreader became the presenter of Question Time in 2019?|Fiona Bruce|Sophie Raworth|Emily Maitlis|Kirsty Wark
David Dickinson|David Dickinson is best known as a television expert in which field?|Antiques|Wildlife|Gardening|Motoring
Richard Osman|Which mystery novel series was created by Richard Osman?|The Thursday Murder Club|The No. 1 Ladies' Detective Agency|Jack Reacher|Cormoran Strike
Sandi Toksvig|Which television quiz did Sandi Toksvig take over from Stephen Fry in 2016?|QI|Would I Lie to You?|Mock the Week|Have I Got News for You
Emma Raducanu|Which Grand Slam tennis tournament did Emma Raducanu win in 2021?|The US Open|Wimbledon|The Australian Open|The French Open
Coco Gauff|In which sport did Coco Gauff become a star?|Tennis|Golf|Basketball|Athletics
Naomi Osaka|With which sport is Naomi Osaka most closely associated?|Tennis|Badminton|Table tennis|Squash
Ben Ainslie|In which sport did Sir Ben Ainslie win his Olympic gold medals?|Sailing|Rowing|Canoeing|Swimming
Tom Daley|In which Olympic sport did Tom Daley win gold?|Diving|Swimming|Water polo|Rowing
Adam Peaty|Which swimming stroke is Adam Peaty particularly known for?|Breaststroke|Backstroke|Butterfly|Freestyle
Rebecca Adlington|Which type of swimming event brought Rebecca Adlington her Olympic gold medals?|Freestyle|Breaststroke|Backstroke|Butterfly
Jade Jones (taekwondo)|In which sport did Jade Jones win Olympic gold in 2012 and 2016?|Taekwondo|Boxing|Judo|Fencing
Nicola Adams|In which combat sport did Nicola Adams become an Olympic champion?|Boxing|Judo|Taekwondo|Wrestling
Katie Taylor|In which sport did Katie Taylor win Olympic gold for Ireland in 2012?|Boxing|Judo|Taekwondo|Fencing
Simone Biles|In which sport is Simone Biles famous for her Olympic performances?|Gymnastics|Diving|Athletics|Swimming
Max Whitlock|On which gymnastics apparatus did Max Whitlock win Olympic gold in both 2016 and 2020?|Pommel horse|Parallel bars|Horizontal bar|Rings
Ellie Simmonds|In which sport did Ellie Simmonds win her Paralympic gold medals?|Swimming|Athletics|Cycling|Archery
Hannah Cockroft|Which activity is Hannah Cockroft particularly known for?|Wheelchair racing|Wheelchair tennis|Swimming|Archery
Ronnie O'Sullivan|In which cue sport is Ronnie O'Sullivan best known?|Snooker|Pool|Carom billiards|English billiards
Luke Littler|In which sport did Luke Littler become famous under the nickname 'the Nuke'?|Darts|Snooker|Boxing|Tennis
Luke Humphries|Which darts player is known as 'Cool Hand'?|Luke Humphries|Luke Littler|Gerwyn Price|Michael van Gerwen
Judd Trump|In which cue sport did Judd Trump become a world champion?|Snooker|Pool|English billiards|Carom billiards
Mark Cavendish|Which sport made Mark Cavendish famous?|Cycling|Motor racing|Rowing|Marathon running
Chris Hoy|In which Olympic discipline did Sir Chris Hoy win his gold medals?|Track cycling|Rowing|Sailing|Track athletics
Yo-Yo Ma|Which instrument is Yo-Yo Ma best known for playing?|Cello|Violin|Harp|Flute
Lang Lang|Which instrument is classical musician Lang Lang known for playing?|Piano|Cello|Trumpet|Harp
Nicola Benedetti|Which string instrument is Nicola Benedetti known for playing?|Violin|Cello|Double bass|Harp
Alison Balsom|Which instrument is Alison Balsom known for playing?|Trumpet|Oboe|Flute|Saxophone
André Rieu|Which violinist founded the waltz-playing Johann Strauss Orchestra?|André Rieu|Nigel Kennedy|Joshua Bell|Itzhak Perlman
Vanessa-Mae|In which Winter Olympic sport did violinist Vanessa-Mae compete in 2014?|Alpine skiing|Figure skating|Snowboarding|Bobsleigh
Nigel Kennedy|Which string instrument is Nigel Kennedy especially associated with?|Violin|Cello|Double bass|Harp
Katherine Jenkins|Which voice type is Katherine Jenkins known for?|Mezzo-soprano|Soprano|Contralto|Tenor
Darcey Bussell|Before becoming a Strictly Come Dancing judge, Darcey Bussell was best known for which dance form?|Ballet|Flamenco|Tap|Irish stepdance
Carlos Acosta|With which dance form is Carlos Acosta most closely associated?|Ballet|Tap|Flamenco|Irish stepdance
Misty Copeland|Which US company made Misty Copeland its first Black female principal dancer in 2015?|American Ballet Theatre|New York City Ballet|San Francisco Ballet|Boston Ballet
Michael Flatley|Which dancer created the show Lord of the Dance?|Michael Flatley|Carlos Acosta|Darcey Bussell|Matthew Bourne
Jean Butler|Which Irish dance show featured Jean Butler as its original principal female performer?|Riverdance|Lord of the Dance|Feet of Flames|Celtic Tiger
Jools Holland|Which instrument is Jools Holland best known for playing?|Piano|Flute|Trombone|Viola
Nile Rodgers|Which band did Nile Rodgers co-found with Bernard Edwards?|Chic|Earth, Wind & Fire|Kool & the Gang|The Commodores
Vivienne Westwood|Which youth style movement did Vivienne Westwood help bring into the mainstream?|Punk|Mod|Hippie|Preppy
Stella McCartney|Which sportswear brand began a collaboration with Stella McCartney in 2004?|Adidas|Nike|Puma|Reebok
Alexander McQueen|Which craft formed an important part of Alexander McQueen's training before fashion college?|Tailoring|Pottery|Bookbinding|Glassblowing
Donatella Versace|Who became Versace's creative director after Gianni Versace's death in 1997?|Donatella Versace|Vera Wang|Phoebe Philo|Stella McCartney
Vera Wang|Which type of clothing is Vera Wang particularly famous for designing?|Wedding gowns|School uniforms|Motorcycle leathers|Military uniforms
Christian Louboutin|What is the signature sole colour of Christian Louboutin shoes?|Red|Blue|Green|Gold
Jimmy Choo|Which fashion item originally made Jimmy Choo's name as a designer?|Shoes|Hats|Scarves|Watches
Manolo Blahnik|What type of fashion item is Manolo Blahnik particularly known for designing?|Shoes|Hats|Watches|Scarves
Diane von Fürstenberg|Which style of dress is Diane von Fürstenberg particularly known for?|Wrap dress|Ball gown|Shift dress|Halter dress
Phoebe Philo|Which designer was Céline's creative director from 2008 to 2017?|Phoebe Philo|Vera Wang|Stella McCartney|Donatella Versace
Antoni Porowski|What was Antoni Porowski's specialty in the original Netflix Queer Eye lineup?|Food and wine|Interior design|Fashion|Grooming
Tan France|Which area was Tan France's specialty in the original Netflix Queer Eye lineup?|Fashion|Food and wine|Grooming|Interior design
Jonathan Van Ness|What was Jonathan Van Ness's specialty in the original Netflix Queer Eye lineup?|Grooming|Food and wine|Interior design|Fashion
Bobby Berk|What was Bobby Berk's specialty on the Netflix series Queer Eye?|Interior design|Food and wine|Grooming|Fashion
Karamo Brown|Which area was Karamo Brown's specialty in the original Netflix Queer Eye lineup?|Culture|Food and wine|Grooming|Interior design
Gok Wan|Which makeover programme helped make Gok Wan widely known in 2006?|How to Look Good Naked|What Not to Wear|Ten Years Younger|Style Challenge
Trinny Woodall|Who formed the original presenting duo with Trinny Woodall on the BBC's What Not to Wear?|Susannah Constantine|Mary Portas|Kelly Hoppen|Gok Wan
Kelly Hoppen|With which design field is Kelly Hoppen particularly associated?|Interior design|Fashion design|Jewellery design|Automotive design
Nicky Clarke|What is Nicky Clarke's best-known profession?|Hairdresser|Makeup artist|Interior designer|Jeweller
Charlotte Tilbury|What type of beauty expert is Charlotte Tilbury best known as?|Makeup artist|Perfumer|Nail technician|Hair colourist
Derren Brown|Which performance art is Derren Brown particularly known for?|Mentalism and illusion|Opera|Ballet|Circus acrobatics
David Blaine|Which magician came to wide television attention with Street Magic in 1997?|David Blaine|Derren Brown|Criss Angel|David Copperfield
Penn Jillette|Which magician is Teller's speaking partner in their double act?|Penn Jillette|David Blaine|Derren Brown|David Copperfield
Teller (magician)|In which US city have Penn and Teller had a long-running residency at the Rio?|Las Vegas|Los Angeles|New York|San Francisco
Criss Angel|Which magician starred in the television series Mindfreak?|Criss Angel|David Blaine|Derren Brown|Penn Jillette
David Copperfield (illusionist)|Which illusionist made the Statue of Liberty appear to disappear in a 1983 television special?|David Copperfield|David Blaine|Derren Brown|Criss Angel
Brian Cox (physicist)|What is Professor Brian Cox's academic discipline?|Physics|Chemistry|Archaeology|Computer science
Maggie Aderin-Pocock|Which BBC astronomy programme did Maggie Aderin-Pocock join as a co-presenter in 2014?|The Sky at Night|Countryfile|Antiques Roadshow|University Challenge
Chris Packham|Who has been a regular presenter of both The Really Wild Show and Springwatch?|Chris Packham|Alan Titchmarsh|Monty Don|Charlie Dimmock'''
lines=raw.splitlines();assert len(lines)==80,len(lines)
for line in lines:
 name,prompt,*answers=line.split('|');assert len(answers)==4
 sourceName='Penn Jillette' if name=='Teller (magician)' else name
 d.append({'draftID':f'easy-26-{len(d)+1:03d}','categoryID':'26','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'sourceURL':'https://en.wikipedia.org/wiki/'+urllib.parse.quote(sourceName.replace(' ','_')),'rationale':'UNAPPROVED candidate; individual final wording, all four choices, accuracy, category, duplicate and reference checks pending.','reviewStatus':'draft_unreviewed'})
assert len(d)==100
(H/'draft.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('80 candidates appended without altering first20.100drafted; none approved or published.')
