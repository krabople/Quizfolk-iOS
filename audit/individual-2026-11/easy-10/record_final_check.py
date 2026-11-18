"""Record the explicitly written author second-pass decisions below."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
edits={
6:{'prompt':'Which artist illustrated the well-known Puffin editions of Roald Dahl\'s Matilda?'},
10:{'prompt':"Which animal does Veruca Salt demand as a pet inside Willy Wonka's factory?",'answers':['A squirrel','A hamster','A guinea pig','A pony'],'rationale':'Veruca demands a trained squirrel in the nut room. The other animals are not the pet she demands here.'},
38:{'sourceURL':'https://www.gov.uk/government/news/go-on-a-coastal-adventure-with-the-snail-and-the-whale'},
39:{'sourceURL':'https://www.juliadonaldson.co.uk/books/picture-books/the-snail-and-the-whale/'},
40:{'sourceURL':'https://www.juliadonaldson.co.uk/books/picture-books/the-snail-and-the-whale/'},
42:{'prompt':"What reward does Zog hope to win at dragon school?",'answers':['A gold star','A silver crown','A bronze cup','A diamond ring'],'rationale':'Zog aims to earn a gold star at school; the other prizes are not his goal.'},
43:{'sourceURL':'https://www.juliadonaldson.co.uk/books/picture-books/zog/'},
57:{'prompt':"Which Beatrix Potter character leaves the farm to find a place to hatch her own eggs?",'sourceURL':'https://etc.usf.edu/lit2go/148/peter-rabbit-and-other-stories/4905/the-tale-of-jemima-puddle-duck/','rationale':'Jemima wants to hatch her own eggs away from the farmer\'s wife. None of the other three named characters is a bird.'},
73:{'prompt':"What is the name of the troublesome cat in Dav Pilkey's Dog Man books?",'answers':['Petey','Garfield','Crookshanks','Tom Kitten'],'sourceURL':'https://www.scholastic.com/site/dav-pilkey-books/dog-man-books/dog-man-tale-of-two-kitties.html','rationale':'Petey the Cat is a Dog Man character; the other cats are from unrelated series.'},
75:{'prompt':"Which interactive feature is central to Eric Hill's original Where's Spot?",'answers':['Lift-up flaps','Pop-up buildings','Scratch-and-sniff patches','Sound buttons']},
76:{'sourceURL':'https://www.elmer.co.uk/about-elmer/'},
77:{'sourceURL':'https://www.elmer.co.uk/about-elmer/'},
79:{'sourceURL':'https://collins.co.uk/products/9780007171347'},
91:{'prompt':"What is a biography?",'answers':["An account of someone's life written by another person",'A collection of maps','A list of unfamiliar words','A book of recipes'],'rationale':'A biography recounts another person\'s life, unlike the atlas, glossary and cookbook distractors.'},
}
notes='''1|Dahl wrote Matilda. Bond, Tolkien and Blyton are distinct authors; no title or answer ambiguity.
2|Miss Honey is Matilda's kind teacher. Trunchbull is the bully, Wormwood her mother and Havisham a Dickens character.
3|Trunchbull is the headmistress. Honey is not head; neither other fictional woman runs Matilda's school.
4|Wormwood sells used cars. Clocks, instruments and plants are different goods; wording and hyphenation checked.
5|Bruce's punishment involves chocolate cake. The three alternative cake flavours are not that cake.
6|Remove the answer Quentin Blake from the question itself. Specify Puffin editions to allow for other editions and adaptations.
7|Wonka owns this factory. McGregor, Tumnus and Bumble are unrelated fictional men, not alternate owners.
8|Golden Tickets are gold. Silver, blue and red are separate wrong colours; four parallel colour labels.
9|There are five tickets, not three, seven or ten. The prompt specifies the original chocolate-bar contest.
10|Replace the Oompa-Loompa concept already asked in Film. Veruca's requested squirrel is supported by the rights-holder's character description; none of hamster, guinea pig or pony is that pet.
11|Violet is the gum chewer. Veruca, Mike and Charlie are other named ticket holders, making a fair single-answer set.
12|Mike Teavee is the TV enthusiast. Augustus, Charlie and Veruca have different defining traits.
13|The river contains chocolate, not juice, honey or milk. Question concerns the fictional factory, not manufacture generally.
14|BFG expands to Big Friendly Giant. The three alternative expansions are invented and grammatically parallel.
15|Sophie is his companion. Matilda, Lucy and Wendy belong to other tales; no second correct girl.
16|The official story summary names snozzcumbers as his food. Chocolate frogs, Turkish delight and marmalade sandwiches do not answer his diet here.
17|Frobscottle is the fictional drink. Butterbeer, lemonade and pumpkin juice are not its name; spelling checked.
18|The human Queen helps the pair. The other three rulers belong to different fictional settings and cannot be mistaken for her in this novel.
19|Sponge and Spiker are James's aunts. All offered pairs are distinct; possessive James's is grammatical.
20|Centipede has the many shoes. Earthworm, Ladybird and Glow-worm are different companions without that detail.
21|Glow-worm supplies light. Other offered companions do not glow; this is a story detail rather than a zoology claim.
22|Miss Spider supplies thread. Silkworm also spins silk in the book but is deliberately absent from the four options, leaving one correct answer.
23|Boggis, Bunce and Bean are farmers. The other collective occupations are wrong and all four options complete the question naturally.
24|The opening specifies four Small Foxes. Two, six and eight are unambiguously different counts.
25|Their hole is under a tree. Lighthouse, castle tower and houseboat are wrong settings; initial scene specified to avoid later changes.
26|Muggle-Wump is a monkey. Rabbit, badger and fox are distinct animal distractors; hyphenation checked.
27|Mr Twit's defining dirty feature is food caught in his beard. The other locations do not answer the described running detail.
28|Roly-Poly Bird helps the captive monkeys. Hedwig, Dodo and Raven are unrelated named birds; one correct helper.
29|Grandmother is the boy's ally. Uncle, sister and grandfather do not occupy that role in Dahl's novel.
30|Grand High Witch is the title. The other three witch titles come from different stories; no interchangeable title here.
31|Donaldson wrote the text. Kerr, Potter and Hughes are plausible authors but did not write The Gruffalo.
32|Scheffler drew The Gruffalo. Blake, Briggs and Hill are different illustrators; author versus illustrator distinction is clear.
33|The small protagonist is a mouse. Rabbit, hedgehog and mole are different animals, absent as this protagonist.
34|The walk occurs in woodland. Desert, beach and castle are different settings, not additional correct descriptions.
35|The central traveller is a witch with her cat. Pirate, knight and astronaut are distinct wrong character types.
36|The danger is a hungry dragon. Troll, spider and wolf do not name the threat in this story.
37|The broom snaps. Boat, ladder and carpet are not their vehicle; the title does not itself reveal that it breaks.
38|The snail rides on the tail, not fin, tongue or blowhole. Replace the provisional ISBN URL with the verified official partnership account.
39|The snail wants to explore the world; the other proposed ambitions are not its aim. Use the author's actual story page.
40|Scheffler is credited on the author's page. Sharratt, Oxenbury and Potter are distinct illustrators, not co-illustrators here.
41|Zog is a dragon, not dinosaur, crocodile or griffin. Fictional species question remains clear despite dinosaur-like artwork.
42|Replace the redundant question about learning dragon skills with his gold-star goal. Other metal/jewel prizes are not that goal.
43|Madam Dragon teaches the class. Honey, Trunchbull and McGonagall belong to other schools; use the author's explicit Madam Dragon description.
44|The family tree is Stick Man's home. Cave, castle and burrow are wrong; plain 'tree' avoids copying the original couplet.
45|The opening specifies three children. One, five and seven differ; his partner is not counted as a child.
46|Little Monkey seeks his mum. Teacher, brother and father are not the object of the search; father later appears but is not whom he originally seeks.
47|Butterfly offers help. Dragonfly, ladybird and honeybee are different insects; no helper ambiguity.
48|The rat steals others' food. Books, shoes and jewellery are not the defining theft; avoid asking an answer already contained in the title.
49|Wizard Lizard captures him. Crow assists but is not offered; Gruffalo, Highway Rat and Madam Dragon do not capture Superworm.
50|Donaldson wrote Superworm; Rosen, McKee and Ahlberg did not. The illustrator attribution is correct and not an author alternative.
51|McGregor owns the vegetable garden. Brown, Tumnus and Wonka are unrelated owners/characters; possessives consistent.
52|Peter's original illustrated jacket is blue. Red, green and purple are wrong; specify original art to exclude redesigns.
53|The three are his sisters. Cousins, daughters and aunts are different relationships and incorrect here.
54|Benjamin is Peter's cousin. Uncle, son and father are mutually distinct alternatives.
55|Jeremy Fisher is a frog. Duck, otter and newt are different pond animals; none describes him.
56|Tiggy-winkle is a hedgehog. Mouse, squirrel and rabbit are distinct wrong mammals.
57|Replace a name-gives-away-the-duck question with Jemima's search for a nesting place. Primary story opening confirms her wish to hatch eggs; other choices are mammals.
58|Nutkin is a squirrel, not fox, badger or mouse. The prompt uses only his name, not the giveaway full book title.
59|Michael Bond created Paddington. Milne, Grahame and Lofting created different fictional animals; same first name is not a second creator.
60|The London station is Paddington. Victoria, Waterloo and Euston are distinct stations, not alternative names for the same place.
61|The Browns welcome him. Dursleys, Weasleys and Bankses are other fictional families; none is Paddington's host family.
62|Marmalade is the bear's signature preserve. Strawberry jam, blackcurrant jelly and lemon curd are different spreads.
63|Carle wrote and illustrated the Caterpillar. Hill is a different Eric; Blake and Scheffler have no creator credit here.
64|The caterpillar ends as a butterfly. Bee, beetle and dragonfly are distinct insects and incorrect outcomes in this book.
65|Monday is the single apple day. Pears, plums and oranges are assigned other days; grammatical articles match each fruit.
66|The leaf follows the overeating and relieves the ache. Cake, ice cream and lollipop belong to the earlier feast, so only one offered remedy fits.
67|Kinney writes and illustrates Wimpy Kid. Pilkey, Walliams and Riordan are distinct authors of other series.
68|Greg Heffley is its central schoolboy narrator. Potter, Rider and Jackson belong to unrelated books.
69|Rowley Jefferson is Greg's best friend. Rodrick is family; Ron and Tom Gates are other series' characters.
70|The playground curse is Cheese Touch. Butter, yoghurt and cream do not name that fictional curse; not a real hygiene claim.
71|Dav Pilkey created Dog Man. Kinney, Smith and McKee are plausible contemporary authors but not this creator.
72|Dog Man works as a police officer. Firefighter, teacher and train driver are different occupations; publisher corroborates police force.
73|Replace the animal-head question whose answer is obvious from the series title. Petey is the troublemaking cat; Garfield, Crookshanks and Tom Kitten are other fictional cats.
74|Eric Hill created Spot, not Eric Carle. Bond and Ahlberg also did not; names and puppy description checked.
75|Use concise, parallel interactive-format distractors and specify the original book. Its lift-up flaps, not pop-ups, scent patches or buttons, reveal the hiding places.
76|McKee created Elmer. Walliams, Hill and Burningham are different authors; use the official Elmer rights-holder page.
77|His skin is multicoloured patchwork. Stripes, blue spots and solid grey are other patterns, not equivalent descriptions.
78|Kerr wrote and illustrated Tiger. Donaldson, Hughes and Oxenbury are not its creators; avoid requiring publication-year trivia.
79|Mog is a cat, not dog, rabbit or parrot. Replace the timing-out homepage citation with the publisher's actual book page.
80|Rod Campbell created Dear Zoo. Roddy Doyle is a different writer despite the similar given name; Rosen and Browne did not create it.
81|Alphabetic subject-and-page lookup is the index. Contents follows chapter order; foreword and dedication have different purposes.
82|Glossary explains specialist words. Dedication, title page and acknowledgements are not definition lists.
83|Appendix adds supporting information. Bookshops, protective wrapper and chapter-first-sentence options are not appendices; book context excludes anatomy.
84|Foreword is introductory material before the text. After-story scene, error list and word definitions describe other sections.
85|Prologue is an opening section. Source list, jacket review and last-chapter summary are not prologues; novel context is explicit.
86|Epilogue concludes after the main narrative. Contents list, typeface note and reviewer introduction are distinct sections.
87|Author is the role for writing the book. A person can hold several jobs, but the question asks the usual role term, not identity, so illustrator/bookseller/librarian are not equivalent answers.
88|Illustrator supplies images. Translation, factory printing and receipts concern different roles; pronoun refers unambiguously to the book.
89|Translator conveys text in another language. Artwork, binding and pricing do not describe translation.
90|Narrator tells the story. Selling, type design and page repair are external book-production roles, not narrative functions.
91|Tighten biography's answer to distinguish it from autobiography. Maps, vocabulary and recipes are different book types; all options are complete noun phrases.
92|Autobiography is the subject's own account. No requirement for poetry, photos only or imaginary people; self-authorship is the sole distinguishing choice.
93|Fiction primarily presents invented stories. The reference/biography alternatives are factual categories; 'principally' allows invented stories to incorporate real facts.
94|Literary anthology collects selected writings. Signature, errata and cover are different things; do not impose an incorrect one-author restriction.
95|Trilogy has three works. Two, four and five are wrong; 'works' allows books, plays and films without changing the number.
96|Sequel continues an earlier story. Translation, draft and advance review are not sequels; 'later' distinguishes a prequel's earlier story setting.
97|An e-book is digital. Large print, wordless and metal-cover formats are not definitions of an e-book; no device-specific limitation.
98|Audiobook is a spoken reading. Sheet music, rhyme dictionary and radio repair manual are different books, not audio format definitions.
99|Hardback has a stiff cover. Flexible folded paper, screen-only pages and audio describe other formats; 'characterises' concerns binding.
100|Paperback has flexible paper/card covers. Wood, stone and recorded disc are not paperback bindings; British usage and parallel nouns checked.
'''
review=[]
for line in notes.strip().splitlines():
    n,note=line.split('|',1); n=int(n); q=draft[n-1]
    row={'row':n,'action':'edit' if n in edits else 'keep','prompt':q['prompt'],'note':note,
         'sourceReview':'Individual author second pass of prompt and all four options against the cited primary author/publisher story account, original story, official partnership account or Cambridge definition. This record is not an independent review.'}
    if n in edits:row['recommendedChanges']=edits[n]
    review.append(row)
assert [r['row'] for r in review]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'reviewer':'root (author second editorial pass)','independent':False,
 'sourceAccessNote':'Primary rights-holder, author, illustrator and publisher pages inspected in web tools. All twenty dictionary definition pages were retrieved and their definitions inspected individually; dictionary-access.json records access, not editorial approval. The original Potter story was inspected via the University of South Florida edition. Provisional URLs corrected as recorded. Automated checks never substitute for these per-row editorial decisions.',
 'rows':review},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Recorded 100 explicit second-pass decisions; apply_review.mjs must apply edits before publication.')
