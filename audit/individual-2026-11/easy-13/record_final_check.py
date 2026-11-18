"""Explicit, per-question author second-pass decisions, not automated approval."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
AQA='https://www.aqa.org.uk/resources/drama-and-performing-arts/gcse/drama/teach/subject-specific-vocabulary'
ABT='https://www.abt.org/explore/learn/ballet-dictionary/'
JOSEPH='https://www.concordtheatricals.com/p/44899/joseph-and-the-amazing-technicolor-dreamcoat'
edits={
3:{'prompt':"Which device picks up a singer's voice for a theatre's sound system?",'answers':['A microphone','A spotlight','A scenic flat','A backdrop'],'sourceURL':AQA,'rationale':'The microphone picks up live sound for amplification; the three other objects concern lighting or scenery.'},
9:{'answers':['Plays','Theatre reviews','Orchestral parts','Lighting plans']},
13:{'sourceURL':'https://filestore.aqa.org.uk/resources/drama/AQA-8261-SET-D-TG.PDF'},
15:{'answers':['Forgotten dialogue','Ticket prices','Costume repairs','Lighting colours']},
27:{'sourceURL':AQA},
33:{'sourceURL':'https://www.open.edu/openlearn/history-the-arts/literature/approaching-plays/content-section-7.2'},
35:{'answers':['Audience members','Costume staff working backstage','Musicians tuning before the show','Lighting staff working backstage'],'sourceURL':'https://www.vam.ac.uk/articles/the-story-of-pantomime'},
39:{'prompt':"In theatre, what is a cue?",'answers':['A signal to begin a particular action','A list of ticket prices','A type of stage curtain','A section of audience seating'],'sourceURL':AQA,'rationale':'A cue triggers a line, entrance or technical operation; the other objects do not define it.'},
40:{'answers':['Creating dialogue or action as the scene is performed','Following a fixed written script word for word','Watching silently from the auditorium','Practising a dance exactly as choreographed']},
44:{'sourceURL':'https://filestore.aqa.org.uk/resources/drama/AQA-8261-SET-D-TG.PDF'},
48:{'answers':['Its official first night, after any preview performances','The night of its final performance','The first day the building is cleaned','The night when the costumes are designed']},
49:{'answers':['The cast list and notes about the production','The complete rehearsal attendance register','The full backstage lighting cue sheet',"The theatre company's annual payroll"]},
50:{'sourceURL':'https://www.mtishows.com/sites/default/files/shelovesme_upstageguide_web.pdf'},
51:{'sourceURL':ABT,'answers':['A bending of the knees','A turn while airborne','A straight-leg kick to the front','A slide with the knees kept straight']},
53:{'answers':['A turn on one leg','A sideways step without turning','A jump taking off from both feet','A bend of both knees without turning']},
59:{'prompt':"What makes the characteristic clicking sounds in modern tap dancing?"},
60:{'prompt':'How many basic positions of the feet are there in classical ballet?','answers':['Five','Three','Four','Six'],'sourceURL':ABT,'rationale':'Classical ballet has five basic foot positions. The other offered counts are wrong.'},
86:{'prompt':"Which musical tells the story of Joseph being sold by his jealous brothers?",'answers':['Joseph and the Amazing Technicolor Dreamcoat','Jesus Christ Superstar','Godspell','Evita'],'sourceURL':JOSEPH,'rationale':'Joseph is the musical adapting the Genesis story of the brothers and his rise in Egypt; the other shows tell different stories.'},
87:{'sourceURL':JOSEPH},
90:{'sourceURL':'https://home.treasury.gov/about/history/prior-secretaries/alexander-hamilton-1789-1795'},
91:{'sourceURL':'https://home.treasury.gov/about/history/prior-secretaries/alexander-hamilton-1789-1795'},
92:{'sourceURL':'https://www.mtishows.com/disneys-aladdin-jr'},
93:{'sourceURL':'https://www.mtishows.com/disneys-aladdin-jr'},
97:{'sourceURL':'https://www.andrewlloydwebber.com/news/cats-returns-to-theatres-in-amsterdam-in-collaboration-with-the-rijksmuseum'},
98:{'prompt':"Which former Glamour Cat sings the main Memory solo in Cats?",'answers':['Grizabella','Jennyanydots','Rum Tum Tugger','Macavity'],'sourceURL':'https://www.andrewlloydwebber.com/news/the-iconic-female-leads-of-andrew-lloyd-webbers-musicals','rationale':'Grizabella is the principal Memory soloist. Other characters may join musical reprises, so the prompt specifies the main solo and excludes Jemima.'},
99:{'answers':['Racial segregation','A ban on audience applause','The use of a live orchestra','A rule requiring every dancer to sing']},
}
notes='''1|Understudy covers another performer, unlike a spectator, pit musician or reviewer. Definition and all role labels checked.
2|Audition is a casting assessment, not a closing show, pricing meeting or orchestra-only rehearsal.
3|Replace the rehearsal definition already represented in General Knowledge. A microphone picks up sound; spotlight, flat and backdrop do not.
4|Matinee is a daytime performance. Midnight, no-scenery and cast-only conditions do not define it.
5|British interval is the performance break, not speech, price or backstage area; regional qualifier is needed.
6|Curtain call acknowledges applause. The other choices describe different activities before/around a show.
7|Standing while applauding defines the ovation. Silence, stage invasion and singing for the cast do not.
8|Encore is an additional piece prompted by appreciation, not rehearsal, pricing or interval.
9|Playwright authors plays. Replace awkward 'only' alternatives with parallel writing products; reviews, orchestral parts and lighting plans do not define playwright.
10|Choreographer creates dances. Pricing, instrument-making and seat labels are distinct jobs.
11|Director guides acting and staging. The three front-of-house positions do not direct the production.
12|Costume designer plans clothing, not refreshments, seating or booking software. Clothing is a precise role description.
13|Set designer creates scenery; costume, sound and lighting roles are distinct. Use AQA's actual set-design guide rather than a general scenery definition.
14|Stage manager coordinates backstage running, unlike critic, collector or audience photographer. 'Normally' accommodates organisational variation.
15|Prompter supplies forgotten lines. Improve wrong options to relevant theatre tasks; prices, repairs and lighting colours are not dialogue.
16|Script contains written dialogue and instructions. Buyer list, review and car-park plan are not play texts.
17|Cast means the actors, not spectators, seats or lights. All four noun phrases have distinct meanings.
18|An actor-handled letter is a clear prop. Audience member, casting decision and newspaper review are not performance objects.
19|Scenery supplies the setting. Warm-up, applause and sales do not represent the fictional physical surroundings.
20|Wings are hidden offstage side areas, not vocal notes, front rows or public doors.
21|Backstage denotes working areas around/behind the playing space. Seating, foyer and pavement are audience/public spaces.
22|Auditorium houses the audience. Laundry room, ticket booth and prop workshop are different rooms.
23|Foyer is the entrance hall. Changing area, fly space and rehearsal room are distinct locations.
24|Box office is the normal ticket collection point. Pit, costume store and rig are inappropriate locations.
25|Pit houses musicians, usually below/in front of the stage. Script cupboard, critics' balcony and trapdoor are not equivalent spaces.
26|Spotlight illuminates a selected target. Amplification, scenery lifting and seat numbering are different functions.
27|A theatrical blackout removes stage light, not costume colour, sound or ticketing. General dictionary lacks this exact stage sense; replace with AQA's explicit definition.
28|Stage right is actor-relative while facing the audience. Left and front/back are distinct directions; viewpoint is explicit.
29|Upstage is away from an end-on audience. Left, right and nearest are incorrect; staging qualifier avoids in-the-round ambiguity.
30|Downstage is towards that audience. Far end, roof and below-floor positions do not fit the defined direction.
31|Fourth wall is an imaginary audience/performer boundary. It is not any actual building or scenic wall.
32|Soliloquy voices one character's thoughts. 'Often alone' avoids the inaccurate rule that nobody else can be on stage.
33|Aside is conventionally unheard by other characters though the audience hears it. Use Open University's theatrical account, not unrelated everyday meanings.
34|Monologue is an extended single-speaker speech. Four-speaker exchange, duet dance and wordless scene do not fit.
35|Panto invites audience participation. Replace strained 'only' answers and cite V&A's theatre history; backstage staff and tuning musicians are not the participating audience.
36|Puppeteer manipulates a puppet. Prices, seating and accounts are unrelated administrative functions.
37|Mime communicates through silent movement. Radio, opera and spoken poetry primarily use sound; silent wording does not exclude music accompaniment.
38|Ventriloquist creates a displaced-voice illusion with minimal lip movement. Tightrope, fire-eating and juggling are distinct acts.
39|Replace the weakly supported dummy detail with the technical cue term. A cue signals an action; prices, curtain and seating are distinct.
40|Improvisation creates material during performance. Replace an irrelevant ticket-data distractor with a plausible but fixed choreographed activity.
41|Dress rehearsal runs in costume as performance preparation. Shoe-only fitting, audience attire and dialogue ban are false definitions; distinct from a generic rehearsal.
42|Read-through is a group script reading. Reviews, barcode checks and orchestra-only playing are different activities.
43|Blocking plans performer positions/movements. Ticket refusal, muting sound and scenic painting are not blocking in acting.
44|Thrust staging normally has three audience sides. One, two and four describe other configurations; use the exam board's explicit set-design guide.
45|In-the-round surrounds the actors. One side, rear only and below-stage seating do not define it.
46|Raked means sloped. Gravel, unlit and outdoor restrictions are wrong; the architectural sense is clear.
47|Revival is a new production of a previously performed work. Premiere, lightbulb and actorless rehearsal are not revivals.
48|Opening night is the official first night. Clarify that preview performances may precede it; closing, cleaning and costume planning are wrong.
49|Programme provides cast/production information. Replace silly private-data distractors with plausible internal documents, none normally supplied as a programme.
50|Book means the dramatic script/story structure, not financial ledger, bookings or requests. Replace generic dictionary citation with the theatre publisher's musical-writing guide.
51|Plié bends knees. Replace the missing dictionary entry with ABT and improve alternatives to parallel dance movements; no second knee-bend option.
52|Arabesque's working leg extends behind. Front, across the knee and floor positions do not describe the basic position.
53|Pirouette is a one-leg turn. Replace frivolous wrong options with three recognisable but non-turning dance actions.
54|Barre gives balance/support in exercises. Amplification, lights and curtain fastening are not its function.
55|En pointe is on toe tips, with supportive pointe shoes in normal practice. Seated, heel-only and music-free alternatives are wrong.
56|Tutu is a ballet skirt. Tap shoes, safety net and lighting stand are different pieces of performance equipment.
57|Pas de deux is for two. One, three and four are distinct counts; term and accents checked.
58|Ballerina means a female ballet dancer. Ticketing, reviewing and instrument-making are different professions.
59|Modern tap shoes have metal taps. Add 'modern' to avoid historical wooden-soled styles; bells, whistles and sticks are not the standard mechanism.
60|Replace the unsupported French-language draft with the five basic classical foot positions, explicitly documented by ABT; three, four and six are wrong.
61|Oliver! adapts Dickens's Oliver Twist. Austen, Carroll and Stevenson wrote different novels; punctuation around the exclamation mark checked.
62|Fagin teaches pickpockets. Brownlow is Oliver's benefactor, Bumble a workhouse official and grandfather not their gang leader.
63|Lionel Bart wrote all three credits. Lloyd Webber, Sondheim and Schwartz are different theatre writers; not a shared-credit ambiguity.
64|Javert is police inspector. Teacher, mechanic and baker are different occupations; preserve French name spelling.
65|Valjean begins as a released prisoner, not student, monk or hospital patient. Story opening qualification is precise.
66|Main story is in France. Italy, Spain and Germany are not alternative principal settings.
67|Fantine sings I Dreamed a Dream. Cosette, Éponine and Madame Thénardier do not sing its principal solo in the standard stage score.
68|Mamma Mia! uses ABBA songs. Queen, Beatles and Beach Boys are different catalogues; do not imply a new original band score.
69|Main setting is a Greek island. Castle, hotel and ranch are different locations, not alternate descriptions.
70|Three men are invited as possible fathers. Two, four and five are wrong; 'possible' avoids falsely declaring three biological fathers.
71|Billy discovers ballet after boxing, not flamenco, salsa or Irish step. Asking a familiar plot point rather than specialist casting trivia.
72|The backdrop is the miners' strike. Teachers, railway workers and dockworkers are different industries; no ambiguous dates required.
73|Elton John wrote the score. Collins, Sting and McCartney are different musicians; Lee Hall is not offered as a composer alternative.
74|Mary is the nanny. Cook, gardener and dressmaker are other household roles, none her job in the Banks home.
75|Bert is associated with chimney sweeping. He also has other trades, so 'especially associated' avoids claiming only one occupation; none of the offered others is his iconic job.
76|Jane and Michael are Banks. Brown, Darling and Potts are different fictional-family names.
77|Elphaba has green skin. Blue, red and purple do not describe her; rights-holder's character profile confirms it.
78|Wicked is in Oz. Narnia, Neverland and Middle-earth are other fantasy worlds; fictional land qualifier is clear.
79|Defying Gravity belongs to Wicked. Other songs are from Cats, Annie and Mamma Mia!, each distinct.
80|Phantom is in Paris. Rome, Vienna and Madrid are wrong opera-city alternatives.
81|His mask conceals part of his face. Crown, helmet and monocle do not fill that role; do not claim the mask covers his entire face.
82|Christine is a soprano/opera singer. Detective, acrobat and teacher are different professions; role is a story fact, not an actor biography.
83|SIX depicts Henry VIII's wives. Other offered monarchs are not their husband; this is the show's premise, not an entry-fee or numerical title riddle.
84|Danny and Sandy are Grease's central couple. Other pairs belong to three separate musicals, making one correct answer.
85|Rydell is its high school. East High, Shiz and Horace Green belong to other fictional schools; not confused with the film's football-team question.
86|Remove the coat question that reveals its answer in the title. Joseph's jealous brothers sell him; Jesus Christ Superstar, Godspell and Evita tell different stories. Use the actual licensor's synopsis URL.
87|Joseph interprets dreams. Invisibility, underwater breathing and animal speech are not his gifts; corrected to the verified licensor page.
88|Train performers skate on roller skates. Ice skates, snowshoes and flippers are wrong; wording excludes the unskated human Control role.
89|Racing roles represent trains/railway stock. Aircraft, cars and boats are different vehicles.
90|Hamilton first held Treasury Secretary. Washington, Jefferson and Jay first held the three alternative offices. Use Treasury's direct biography instead of unavailable musical-page URL.
91|Story concerns United States founding. Canada, Australia and New Zealand are not the setting; corrected primary historical reference supplements the theatre premise.
92|Genie comes from a lamp. Teapot, perfume bottle and jewellery box are wrong. Use the verified stage-edition licensing page.
93|Jasmine is the princess. Ariel, Belle and Aurora come from other Disney stories; verified stage-edition page replaces unavailable general URL.
94|Anna and Elsa are sisters, not cousins, mother/daughter or aunt/niece. The stage synopsis explicitly confirms sisterhood.
95|Olaf is a snowman. Sven is the reindeer; troll and wolf are other kinds of creature, not Olaf.
96|Scar is Mufasa's brother. Jafar, Gaston and Frollo are villains from different stories; a precise family relation rather than a vague 'bad character'.
97|Gathering is the Jellicle Ball. Emerald, Snowflake and Royal are wrong names; use the rights-holder's explicit story description.
98|Grizabella sings the main Memory solo. Qualify the solo and replace Jemima with Macavity because Jemima can sing related passages; all remaining offered names are other cats.
99|Tracy opposes racial segregation. Replace unrelated theatre-fee answers with clearly different show practices; neither applause, live orchestra nor compulsory singing is the injustice in the plot.
100|Annie starts in an orphanage. Palace, lighthouse and Kansas farm are not her starting home; existing Warbucks/Sandy questions ask different facts.
'''
review=[]
for line in notes.strip().splitlines():
    number,note=line.split('|',1);n=int(number);q=draft[n-1]
    row={'row':n,'action':'edit' if n in edits else 'keep','prompt':q['prompt'],'note':note,
      'sourceReview':'Prompt and every option individually checked in an author second pass using the cited dictionary, theatre education, primary licensor, rights-holder or official historical source. Failed/provisional citations corrected as recorded; not an independent review.'}
    if n in edits:row['recommendedChanges']=edits[n]
    review.append(row)
assert [r['row'] for r in review]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'independent':False,'reviewer':'root (author second editorial pass)',
 'sourceAccessNote':'Cambridge definition entries were retrieved in four small groups and individually inspected. Missing or overly general definitions were replaced with AQA, ABT, V&A, Open University and MTI references actually inspected. Primary MTI/Concord/rights-holder story and credit pages were inspected for musical facts; Treasury confirms Hamilton\'s office. Original author rationale is separate from these final-pass decisions. Automated structure/overlap checks are not editorial approval.',
 'rows':review},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Recorded 100 explicit author second-pass decisions; edits still need application.')
