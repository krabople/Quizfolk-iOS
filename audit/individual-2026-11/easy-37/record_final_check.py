"""Persist explicit author second-pass decisions for all 100 Family candidates."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
edits={
2:{'sourceURL':'https://dictionary.cambridge.org/dictionary/english/masher'},
4:{'sourceURL':'https://www.merriam-webster.com/dictionary/baster'},
20:{'prompt':"Which object is designed to carry cups and dishes together from the kitchen?",'answers':['A serving tray','A chopping board','A sieve','A breadbin']},
26:{'sourceURL':'https://dictionary.cambridge.org/dictionary/english/hanger','answers':['Clothing','Books','Curtains','Umbrellas']},
31:{'prompt':"Which small clothing fastener is usually sewn on and passed through a matching hole?",'answers':['A button','A zip','A buckle','A hook-and-loop strip'],'sourceURL':'https://dictionary.cambridge.org/dictionary/english/button','rationale':'A sewn-on button passes through a buttonhole; the other fasteners do not work this way. Replaces an existing zip concept.'},
33:{'sourceURL':'https://dictionary.cambridge.org/dictionary/english/eyelet'},
40:{'answers':['The head and neck','The hands and wrists','The feet and ankles','The waist and hips'],'rationale':'A balaclava is a close-fitting head-and-neck covering; face coverage varies with its design.'},
44:{'prompt':'Which marks does an ordinary eraser remove from paper most easily?','answers':['Pencil marks','Ballpoint ink','Permanent-marker ink','Printer toner']},
46:{'answers':['Small metal staples','Strips of adhesive tape','Loops of string','Plastic cable ties']},
49:{'prompt':"Which stationery item provides a firm portable writing surface and holds loose sheets in place?",'answers':['A clipboard','A pencil case','A hole punch','A set square']},
63:{'sourceURL':'https://www.merriam-webster.com/dictionary/diabolo'},
77:{'sourceURL':'https://www.museumofplay.org/toys/slinky/'},
80:{'sourceURL':'https://dictionary.cambridge.org/dictionary/english/spinning-top'},
84:{'prompt':'What is the pom-pom on top of a woolly hat?'},
85:{'sourceURL':'https://www.museumofplay.org/toys/play-doh/'},
87:{'prompt':'How is traditional non-woven felt formed?','answers':['By matting and pressing fibres together','By weaving threads over and under each other','By knitting loops of yarn into rows','By crocheting stitches with a hook']},
90:{'answers':['The clothing underneath it','The furniture nearby','The floor beneath the table','The utensils being used']},
94:{'prompt':'Which fittings allow a normal door to pivot open and closed?'},
96:{'answers':['Above the curtain to hide its fittings','Along the bottom hem of the curtain','In the centre of the window glass','Below the window sill']},
97:{'answers':['A soft filled bed covering','A fitted sheet around a mattress','A case for one pillow','A cover made for a sofa']},
98:{'answers':['Long and cylindrical','Flat and triangular','Round and disc-shaped','Square with four equal sides']},
99:{'answers':['An ottoman','A coat stand','A dressing mirror','A dining table']},
}
notes='''1|Colander's holes drain pasta. Bowl/jug retain liquid and rolling pin is solid; no second draining utensil offered.
2|Masher is purpose-built for potatoes. Peeler, brush and ladle perform different tasks; correct failed source slug to masher.
3|Citrus press extracts juice. Pips, dried peel and slices are not its designed output; all words are grammatical.
4|A baster draws and ejects cooking liquid. Bread, peppercorns and pastry are solids; replace absent Cambridge entry with Merriam-Webster's explicit utensil definition.
5|Grater has sharp-edged cutting holes. Board, teapot and strainer lack that cutting function; strainer's holes do not make it a second answer.
6|Peeler removes skin, not specifically seeds, stalk or whole centre. Use designed purpose rather than claiming no other possible use.
7|Ladle's deep bowl and handle fit soup service. Knife, fish slice and masher do not have this bowl structure.
8|Tongs have paired gripping arms. Whisk, ladle and sieve are structurally different utensils.
9|Flat spatula turns pancakes. The other tools are liquid scoop, shredder and peeler, not flat turners.
10|Mortar is the crushing bowl paired with pestle. Sieve, colander and measuring jug are not the traditional grinding vessel.
11|Trivet supports a hot vessel on the surface. Cutting, measuring and locking are not its purpose; no unsafe cooking instruction is implied.
12|Teapot brews/serves tea. Coffee grinding, freezing juice and flour measuring are different tasks.
13|Kettle normally boils water. Flour, butter and oil are wrong contents for its intended use; 'normally' is precise.
14|Vacuum insulation slows temperature change. It does not create instant ice, desalinate or measure sugar; no claim of indefinite heat retention.
15|Can opener cuts/removes a can lid. Vegetable skin, bottle cork and melon rind are other removal tasks, not its purpose.
16|Pop-up toaster browns sliced bread. Soup bowls, potatoes and pasta are not its intended food form.
17|Oven gloves protect hands. Shoe, hair and hearing protection are different equipment; answer concerns designed use, not a guarantee against burns.
18|Baking tray is the flat metal oven holder. Colander, kettle and teapot are different vessels.
19|British tea towel dries washed kitchenware. Hair, soil and wall paint do not describe its principal role.
20|Replace awkward 'only' wrong answers with real kitchen objects. Serving tray is purpose-built for transport; chopping board cuts, sieve strains and breadbin stores.
21|Dustpan receives swept dirt. Watering can, washing basket and paint tray are different-purpose containers.
22|Mop's absorbent head washes floors. Rake, feather duster and squeezer perform different tasks.
23|Duster removes surface dust. Opening, measuring and sharpening are wrong tasks; cleaning context excludes the clothing sense.
24|Vacuum cleaner uses suction to collect dirt. Toaster, heater and sewing machine do not; this asks the whole-appliance purpose, unlike existing cyclone-component questions.
25|Clothes peg holds laundry on a line. Tiles, curtains and hinges are different household items, not line-hung washing.
26|Hanger supports garments in storage. Replace silly folded-leg answer and correct the citation to the full hanger definition; books, curtains and umbrellas are not its conventional wardrobe role.
27|Ironing board supplies a pressing surface. Chopping, television support and dining are not its design functions.
28|Thimble protects the pushing finger. Ankle, ear and elbow are not covered by that small sewing cap.
29|Seam is a line of joined fabric. Button, reel and needle eye are separate sewing items, not joins.
30|Needle's thread hole is the eye. Heel, wing and lip are not its normal term; sewing context avoids anatomical ambiguity.
31|Replace the zip-tooth question already in General Knowledge. Button is sewn to clothing and passed through a buttonhole; zip, buckle and hook-and-loop operate differently.
32|Velcro is a hook-and-loop brand. Metal zip, press stud and belt buckle are distinct mechanisms; brand capitalisation retained.
33|Laces pass through eyelets. Sole, heel and insole are other shoe parts; use the actual eyelet definition as source.
34|Buckle is a belt fastening. Thimble, peg and paper clip have other uses; 'commonly' permits other belt styles.
35|Umbrella gives shelter from rain. It does not heat, measure wind or emit light; no claim of total waterproof enclosure.
36|Anorak is a hooded jacket. Sock, belt and sleeveless vest are different garments; clothing context excludes slang meaning.
37|Wellington boots keep feet dry. Hands, neck and head are wrong body locations; use boot sense only, not the source's unrelated city definition.
38|Mitten groups four fingers and separates thumb. Wrist-only, separate-each-finger and metal requirements are false.
39|Neck is the conventional warm scarf location. Ankles, elbows and knees are not the usual winter scarf placement; 'commonly' allows head scarves.
40|Tighten coverage to head and neck, because balaclava face openings vary. Other choices are body regions covered by different garments.
41|Centimetre scale measures length, not weight, temperature or time. Specifying markings excludes drawing-only use.
42|Protractor measures angles. Rain, weight and temperature are different quantities measured by other tools.
43|Set square is a triangular right-angle guide. Compasses, rubber and sharpener do not have this design.
44|Ordinary eraser removes graphite most readily. Use parallel mark types rather than a long conditional print distractor; ballpoint, permanent ink and toner are not its intended marks.
45|Sharpener makes a pointed pencil tip. Brush, loop and cap are not products of sharpening.
46|Stapler inserts staples. Replace invented elastic paint and weak alternatives with real fastening materials; it does not dispense tape, string or cable ties.
47|Paper clip grips without puncturing. Pin, needle and staple pierce the paper, so there is only one non-piercing answer.
48|Hole punch makes binder holes. Pencil points, printed envelopes and paper boats are different outputs.
49|Rewrite the near-tautological clipboard description into identification of a portable writing support. Pencil case, punch and set square lack the board-and-clip function.
50|Pencil case stores stationery. Drying, rain measurement and refrigeration are unrelated functions; no claim it can contain only pencils.
51|Magnifier enlarges nearby visual detail. Sound, smell and viewing through solid opaque walls are different/impossible functions for it.
52|Binoculars have a tube for each eye. Screens, compasses and motors are not universal features, which the alternatives explicitly claim.
53|Kaleidoscope gives changing mirrored patterns. Road map, pressure measurement and voice recording are different observations.
54|Periscope redirects the line of sight from above an obstacle. Hearing through walls, weighing and salinity measurement are not its functions.
55|Eyepieces are the viewing lenses. Lens caps block the view; strap and case support/protect the instrument rather than form the image.
56|Magnetic compass gives direction. Temperature, weight and rainfall are different measurements; do not equate magnetic north with true north.
57|Traditional hourglass transfers sand. Pendulum, hand and beads are different time/counting mechanisms.
58|Stopwatch measures elapsed time. Pressure, map distance and roof angle are different quantities.
59|Metronome supplies a regular beat. Lamp, network signal and review are unrelated outputs; it does not write the music.
60|Thermostat regulates temperature. Calendar date, wall colour and TV volume are not heating-system controlled quantities.
61|Ordinary picture jigsaw assembles a complete image. Clock, audio recording and scales are not its result; existing border-piece question is a different fact.
62|Yo-yo travels on its attached string. Stringless top, marbles and hoop do not match that mechanism.
63|Diabolo spins on string between two handsticks. Other offered toys differ; replace missing Cambridge entry with Merriam-Webster's explicit definition.
64|Only returning boomerangs are designed to curve back, and the prompt requires correct throwing. Hovering, ground penetration and straight-only flight are not the intended behaviour.
65|Kite is tethered by a line/string. Rigid sky pole, mains lead and boat chain do not describe the conventional hand-flown kite.
66|Flying disc is the flat throwing toy. Yo-yo, rope and pogo stick are other toys; avoid using the Frisbee trademark as a generic product claim.
67|Traditional marbles are small balls. Cards, rings and paper planes are distinct play pieces.
68|Hopscotch uses a ground-marked hopping course. Hiding, rope-pulling and musical chairs do not fit.
69|Skipping involves jumping over the rotating rope. Chairs, bench and bicycle are different obstacles, not normal rope-skipping.
70|Seesaw rocks about a central pivot. Wheels, straps and overhead ropes are different support mechanisms.
71|Playground roundabout rotates. Pure vertical, sloping and fixed-bouncing movements describe different equipment; playground qualifier excludes road traffic.
72|Slide descends along a chute. Spinning, spring bouncing and hanging-seat swinging are different play motions; the playground definition occurs later among the source's many senses.
73|Swing seat hangs from above on ropes/chains. Spring, wheeled track and balanced board are different mechanisms; relevant noun definition inspected beyond initial verb senses.
74|Hula hoop spins around the waist. Diabolo, yo-yo and marbles are not body hoops.
75|Pogo stick has handles, footrests and a spring for upright bouncing. Scooter, skateboard and balance bike use wheels instead.
76|Trampoline's stretched surface rebounds. Seesaw, climbing frame and roundabout do not have that flexible bed.
77|Original Slinky was a metal coil spring. Ball, cube and doll are different forms; replace the unrelated dictionary adjective with the National Toy Hall of Fame's original toy account.
78|Jack-in-the-box contains a springing figure. Ramp ball, flying disc and colour-changing marbles are different mechanisms.
79|Nesting dolls fit smaller inside larger. Larger-than-container, string-linked and glass-only restrictions are false.
80|A top spins on a narrow tip. Square base, two wheels and hanging seat do not describe it; cite the dedicated spinning-top entry rather than the ambiguous general word.
81|Concertina folding alternates pleats. Rolling, tearing and spiral cutting are not folds; instrument bellows/verb sense support the term.
82|Sticker adheres by a sticky backing. Sand, hinge and buckle are not its adhesive mechanism; ordinary excludes purely digital stickers.
83|Craft pipe cleaner's wire core allows bending. Glass, solid wood and stone cores are wrong; soft covering is distinct from core.
84|Correct the missing punctuation/ambiguous question to ask what the hat pom-pom is. Fibre ball is correct; zip, strap and glass disc are different objects.
85|Malleable modelling dough forms shapes by hand. Pencil sharpening, photo printing and window polishing are wrong functions; replace missing entry with the museum's Play-Doh account.
86|Glue stick is adhesive. Angle measurement, sharpening and cutting are different stationery tasks; the question does not require a particular dispenser.
87|Specify non-woven felt and use four genuine textile processes. Matting/pressing is correct; weaving, knitting and crocheting alone do not form this non-woven structure.
88|Wax crayon draws coloured marks. Metal fastening, circle cutting and measuring need other tools.
89|Carbon sheet copies writing onto the lower sheet by pressure. Sharpening, waterproofing and audio recording are different outcomes.
90|Apron protects the clothes beneath it. Replace implausible ceiling/wiring distractors with nearby objects that it is not worn to cover.
91|Doorstop limits movement or holds a door open. Lock operation, polishing and speech alarm are unrelated functions.
92|Doormat cleans dirt from shoes. Dish drying, coat hanging and height measuring do not define it.
93|Draught excluder reduces unwanted airflow through the gap. It is not perfect soundproofing, a pipe valve or a window blackout.
94|Remove the giveaway word hinged from the question. Hinges allow the pivot; letterbox, paint and doormat do not.
95|Venetian blind has adjustable horizontal slats. Brick, bead curtain and paint are different window treatments/materials.
96|Pelmet goes above curtains. Replace unrelated room locations with other plausible window positions; hem, glass centre and sill are wrong.
97|Duvet is a soft filled bed cover. Replace absurd furniture/tile alternatives with bedding/furnishing covers; fitted sheet, pillowcase and sofa cover are not duvets.
98|Traditional bolster is a long cylinder. Replace material-mismatched distractors with parallel geometric shapes; triangle, disc and square differ.
99|Storage ottoman has a padded lift-up top. Replace potentially storage-capable dining chair with a coat stand, mirror and dining table, none the intended upholstered storage seat.
100|Footstool supports feet while seated. Beam, curtain and roof tile are other support jobs, not what a footstool is designed for.
'''
rows=[]
for line in notes.strip().splitlines():
    number,note=line.split('|',1);n=int(number);q=draft[n-1]
    row={'row':n,'action':'edit' if n in edits else 'keep','prompt':q['prompt'],'note':note,
         'sourceReview':'Individual author second pass of the question and all four options against the cited primary dictionary definition or museum toy record; relevant senses selected explicitly, failed entries corrected. Not an independent review.'}
    if n in edits:row['recommendedChanges']=edits[n]
    rows.append(row)
assert [r['row'] for r in rows]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'reviewer':'root (author second editorial pass)','independent':False,
 'sourceAccessNote':'One hundred candidate references retrieved in five bounded groups; the individual definitions were inspected. Failed masher/baster/diabolo/playdough entries and the non-toy slinky sense were replaced using correct dictionary lemmas, Merriam-Webster and National Toy Hall of Fame records. Full polysemous slide/swing/top definitions inspected and four additional corrected entries retrieved. Original rationale is not counted as this second editorial pass. Overlap search found the zip concept, which was replaced. Source excerpts kept private; public access records contain hashes only.',
 'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('100 explicit second-pass decisions recorded; apply before assembly.')
