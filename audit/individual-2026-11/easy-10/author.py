"""Original accessible Books candidates. Drafts require a separate final check."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
sources={
'matilda':'https://roalddahl.com/stories/matilda',
'charlie':'https://roalddahl.com/stories/charlie-and-the-chocolate-factory',
'bfg':'https://roalddahl.com/stories/the-bfg',
'james':'https://roalddahl.com/stories/james-and-the-giant-peach',
'fox':'https://roalddahl.com/stories/fantastic-mr-fox',
'twits':'https://roalddahl.com/stories/the-twits',
'witches':'https://roalddahl.com/stories/the-witches',
'gruffalo':'https://www.panmacmillan.com/authors/julia-donaldson/the-gruffalo/9781509804757',
'room':'https://www.panmacmillan.com/authors/julia-donaldson/room-on-the-broom/9781509804771',
'snail':'https://www.panmacmillan.com/authors/julia-donaldson/the-snail-and-the-whale/9781509812523',
'zog':'https://axelscheffler.com/books-with-julia-donaldson/zog',
'stick':'https://www.juliadonaldson.co.uk/books/picture-books/stick-man/',
'monkey':'https://axelscheffler.com/books-with-julia-donaldson/monkey-puzzle',
'rat':'https://www.juliadonaldson.co.uk/books/picture-books/the-highway-rat/',
'superworm':'https://shop.scholastic.co.uk/products/Superworm-9781407170725',
'peter':'https://peterrabbit.com/characters/peter-rabbit/',
'benjamin':'https://peterrabbit.com/characters/benjamin-bunny/',
'sisters':'https://peterrabbit.com/characters/flopsy-mopsy-and-cotton-tail/',
'jeremy':'https://peterrabbit.com/characters/mr-jeremy-fisher/',
'tiggy':'https://peterrabbit.com/characters/mrs-tiggy-winkle/',
'nutkin':'https://peterrabbit.com/characters/squirrel-nutkin/',
'jemima':'https://peterrabbit.com/characters/jemima-puddle-duck/',
'paddington':'https://shop.scholastic.co.uk/products/Paddington-9780007236336',
'brown':'https://paddingtonbearexperience.com/about-the-experience/',
'carle':'https://www.youtube.com/watch?v=Q_axsM983nY',
'wimpy':'https://wimpykid.com/about/',
'wimpyhome':'https://wimpykid.com/',
'dogman':'https://www.scholastic.ca/our-books/book/dog-man-a-graphic-novel-dog-man-1-from-the-creator-of-captain-underpants-9780545581639',
'spot':'https://www.penguin.co.uk/books/37420/wheres-spot-by-hill-eric/9780241426128',
'elmer':'https://www.penguin.co.uk/series/ELMER/elmer-picture-books',
'tiger':'https://harpercollinschildrensbooks.co.uk/products/the-tiger-who-came-to-tea-judith-kerr-9780007490967/',
'mog':'https://www.tigermogandfriends.com/',
'dearzoo':'https://www.panmacmillan.com/dear-zoo',
}
for term in 'index glossary appendix foreword prologue epilogue author illustrator translator narrator biography autobiography fiction anthology trilogy sequel ebook audiobook hardback paperback'.split():
    sources[term]='https://dictionary.cambridge.org/dictionary/english/'+term
rows='''matilda|Who wrote the children's novel Matilda?|Roald Dahl|Michael Bond|J. R. R. Tolkien|Enid Blyton|Dahl is the novelist; the other three are different children's authors.
matilda|In Roald Dahl's Matilda, which teacher becomes Matilda's kind ally?|Miss Honey|Miss Trunchbull|Mrs Wormwood|Miss Havisham|Honey is her class teacher; Trunchbull is the head and Wormwood her mother; Havisham belongs to Dickens.
matilda|Who is the bullying headmistress in Roald Dahl's Matilda?|Miss Trunchbull|Miss Honey|Mrs Tiggy-winkle|Miss Marple|Trunchbull runs Crunchem Hall; the others are a kind teacher and characters from other books.
matilda|What does Matilda's father sell in Roald Dahl's novel?|Second-hand cars|Antique clocks|Musical instruments|Garden plants|Mr Wormwood is a dishonest used-car dealer, not any of the other traders.
matilda|In Matilda, what kind of cake is Bruce Bogtrotter forced to eat?|Chocolate cake|Carrot cake|Lemon cake|Coffee cake|Trunchbull punishes Bruce with a whole chocolate cake; the other flavours do not fit.
matilda|Who illustrated the familiar Quentin Blake editions of Matilda?|Quentin Blake|Axel Scheffler|Eric Carle|E. H. Shepard|Blake's illustration credit is explicit; this draft wording needs a less revealing final prompt.
charlie|Who owns the factory in Charlie and the Chocolate Factory?|Willy Wonka|Mr McGregor|Mr Tumnus|Mr Bumble|Wonka is the chocolate maker; the other men belong to unrelated books.
charlie|What colour are the tickets that admit children to Willy Wonka's factory?|Gold|Silver|Blue|Red|They are Golden Tickets; no other ticket colour is correct.
charlie|How many Golden Tickets does Willy Wonka hide in chocolate bars?|Five|Three|Seven|Ten|There are five tickets in five bars; all numerical distractors differ.
charlie|Which workers sing songs in Willy Wonka's chocolate factory?|Oompa-Loompas|Hobbits|Moomins|Borrowers|Oompa-Loompas are the factory workers; the other groups are from different stories.
charlie|Which child is famous for chewing gum in Charlie and the Chocolate Factory?|Violet Beauregarde|Veruca Salt|Mike Teavee|Charlie Bucket|Violet is the record-breaking gum chewer; the other ticket holders have different traits.
charlie|Which child is especially obsessed with television in Charlie and the Chocolate Factory?|Mike Teavee|Augustus Gloop|Charlie Bucket|Veruca Salt|Mike's TV fixation motivates his television-room mishap; other children are not this character.
charlie|In Charlie and the Chocolate Factory, what flows through the factory's famous river?|Chocolate|Orange juice|Honey|Milk|The river is chocolate; the other liquids are not the river's contents.
bfg|What do the letters BFG stand for in Roald Dahl's novel?|Big Friendly Giant|Brave Flying Giant|Big Fearless Guardian|Best Forest Guide|The title abbreviates Big Friendly Giant; all alternative expansions are wrong.
bfg|What is the name of the girl who befriends the BFG?|Sophie|Matilda|Lucy|Wendy|Sophie is the BFG's friend; the other girls are protagonists of different stories.
bfg|Which of these does the BFG eat instead of children?|Snozzcumbers|Chocolate frogs|Turkish delight|Marmalade sandwiches|The BFG's diet includes snozzcumbers; the distractors are foods associated with other stories.
bfg|What is the BFG's fizzy drink called?|Frobscottle|Butterbeer|Lemonade|Pumpkin juice|Frobscottle is the named fictional drink; the other names do not identify it.
bfg|Which monarch helps Sophie and the BFG stop the other giants?|The Queen|The White Witch|The Queen of Hearts|King Arthur|They appeal to the human Queen; the other rulers are from different fictional settings.
james|Who are James's cruel aunts in James and the Giant Peach?|Aunt Sponge and Aunt Spiker|Aunt Petunia and Aunt Marge|Aunt Polly and Aunt Sally|Aunt Em and Aunt Lucy|Sponge and Spiker are the two aunts in this book; the other pairs are unrelated characters.
james|Which of James's travelling companions in James and the Giant Peach has many shoes?|The Centipede|The Earthworm|The Ladybird|The Glow-worm|The Centipede's many legs require many shoes; the other companions do not have this trait.
james|Which companion provides light inside the peach in James and the Giant Peach?|The Glow-worm|The Centipede|The Earthworm|The Grasshopper|The glowing character provides illumination; none of the others is the light source.
james|Which companion spins thread in James and the Giant Peach?|Miss Spider|The Ladybird|The Centipede|The Earthworm|Miss Spider supplies thread; excluding Silkworm from the options avoids a second correct answer.
fox|In Fantastic Mr Fox, what do Boggis, Bunce and Bean do for a living?|They are farmers|They are teachers|They are sailors|They are bakers|All three own farms; the other collective occupations are incorrect.
fox|How many young foxes live with Mr and Mrs Fox in Fantastic Mr Fox?|Four|Two|Six|Eight|The opening specifies four Small Foxes; the numerical options are distinct.
fox|Where does Mr Fox's family live at the beginning of Fantastic Mr Fox?|In a hole beneath a tree|In a lighthouse|In a castle tower|On a houseboat|The opening locates their hole under a huge tree; the other homes do not apply.
twits|What kind of animal is Muggle-Wump in Roald Dahl's The Twits?|A monkey|A rabbit|A badger|A fox|Muggle-Wump and his captive family are monkeys; no other animal option fits.
twits|Where does Mr Twit keep getting old bits of food stuck?|In his beard|In his boots|In his hat|In his pockets|The book's description singles out his dirty beard; the other locations do not answer this detail.
twits|Which bird helps the monkeys in Roald Dahl's The Twits?|The Roly-Poly Bird|Hedwig|The Dodo|The Raven|The Roly-Poly Bird helps Muggle-Wump's family; the other named birds are not the helper.
witches|Which relative helps the boy face the witches in Roald Dahl's The Witches?|His grandmother|His uncle|His older sister|His grandfather|His grandmother is the experienced witch-hunter and ally; the other relatives are not that character.
witches|What is the leader of the witches called in Roald Dahl's The Witches?|The Grand High Witch|The White Witch|The Wicked Witch of the West|The Sea Witch|The Grand High Witch leads Dahl's witches; other titles belong to different stories.
gruffalo|Who wrote the rhyming picture book The Gruffalo?|Julia Donaldson|Judith Kerr|Beatrix Potter|Shirley Hughes|Donaldson wrote it; the three other women are different picture-book authors.
gruffalo|Who illustrated Julia Donaldson's The Gruffalo?|Axel Scheffler|Quentin Blake|Raymond Briggs|Eric Hill|Scheffler is credited as illustrator; the other artists did not illustrate this original book.
gruffalo|Which small animal outwits the creatures in The Gruffalo?|A mouse|A rabbit|A hedgehog|A mole|The mouse is the quick-thinking protagonist; the three other small mammals are not.
gruffalo|Where does the mouse take its walk in The Gruffalo?|In a wood|In a desert|On a beach|Inside a castle|The story's walk is through woodland, not the three alternative settings.
room|What kind of person travels with a cat in Julia Donaldson's Room on the Broom?|A witch|A pirate|A knight|An astronaut|The central character is a witch; the other character types do not fit.
room|Which creature threatens the witch in Room on the Broom?|A dragon|A troll|A giant spider|A wolf|The greedy dragon wants a meal; the other creatures are not that threat.
room|In Room on the Broom, what breaks under the weight of the passengers?|The broomstick|A rowing boat|A ladder|A flying carpet|Their broom snaps under the load; other vehicles/objects do not describe the scene.
snail|In The Snail and the Whale, which part of the whale carries the snail?|Its tail|Its fin|Its tongue|Its blowhole|The snail rides the whale's tail; the other body parts are wrong.
snail|In The Snail and the Whale, what does the snail long to do?|Travel around the world|Build a bigger shell|Become a pirate captain|Find a buried crown|The little snail wants to explore; none of the other ambitions is the story's premise.
snail|Who illustrates Julia Donaldson's The Snail and the Whale?|Axel Scheffler|Nick Sharratt|Helen Oxenbury|Beatrix Potter|The author and publisher credit Scheffler; other children's illustrators are distractors.
zog|What kind of creature is Zog in Julia Donaldson's picture book?|A dragon|A dinosaur|A crocodile|A griffin|Zog attends dragon school; the other creature types are distinct and wrong.
zog|What is Zog learning to be at Madam Dragon's school?|A skilled dragon|A ship's captain|A circus acrobat|A royal chef|The school teaches dragon skills; alternative professions do not fit the book.
zog|Who teaches Zog and the other young dragons?|Madam Dragon|Miss Honey|Miss Trunchbull|Professor McGonagall|Madam Dragon is the dragon-school teacher; the others teach in unrelated books.
stick|Where does Stick Man live with his family?|In a tree|In a cave|In a castle|In a burrow|The family tree is his home; the other dwellings are not.
stick|How many children do Stick Man and his Stick Lady Love have?|Three|One|Five|Seven|The opening specifies three children; other odd-number options are wrong.
monkey|In Julia Donaldson's Monkey Puzzle, who is the little monkey trying to find?|His mother|His teacher|His brother|His father|The lost monkey seeks his mum; the other relationships are wrong.
monkey|Which creature tries to help the little monkey in Monkey Puzzle?|A butterfly|A dragonfly|A ladybird|A honeybee|Butterfly is the helper who misinterprets his descriptions; other insects do not fill that role.
rat|What does the greedy character in The Highway Rat steal from travellers?|Food|Books|Shoes|Jewellery|The robber takes others' food; other goods are not the defining theft in this story.
superworm|Which villain captures Superworm in Julia Donaldson's book?|Wizard Lizard|The Gruffalo|The Highway Rat|Madam Dragon|The publisher names Wizard Lizard; the other characters are from different Donaldson stories.
superworm|Who wrote Superworm, illustrated by Axel Scheffler?|Julia Donaldson|Michael Rosen|David McKee|Allan Ahlberg|Donaldson is the writer; the other children's authors are not credited for this book.
peter|Whose vegetable garden does Peter Rabbit sneak into in Beatrix Potter's story?|Mr McGregor's|Mr Brown's|Mr Tumnus's|Mr Wonka's|McGregor owns the garden; the other characters do not.
peter|What colour is Peter Rabbit's jacket in Beatrix Potter's original illustrations?|Blue|Red|Green|Purple|His jacket is blue; the colour options are mutually exclusive.
sisters|How are Flopsy, Mopsy and Cotton-tail related to Peter Rabbit?|They are his sisters|They are his cousins|They are his daughters|They are his aunts|The three rabbits are Peter's sisters, not the other relationships.
benjamin|How is Benjamin Bunny related to Peter Rabbit?|He is Peter's cousin|He is Peter's uncle|He is Peter's son|He is Peter's father|Benjamin is Peter's cousin; each distractor is a different relationship.
jeremy|What kind of animal is Beatrix Potter's Mr Jeremy Fisher?|A frog|A duck|An otter|A newt|Fisher is an anthropomorphic frog; the other pond animals do not describe him.
tiggy|What kind of animal is Beatrix Potter's Mrs Tiggy-winkle?|A hedgehog|A mouse|A squirrel|A rabbit|The washerwoman is a hedgehog; other mammals are wrong.
jemima|Which Beatrix Potter character is a duck?|Jemima Puddle-duck|Mrs Tiggy-winkle|Mrs Tittlemouse|Squirrel Nutkin|Jemima is the only duck among the four named characters.
nutkin|In Beatrix Potter's story, which animal is Nutkin?|A squirrel|A fox|A badger|A mouse|Nutkin is a red squirrel; the other woodland mammals are wrong.
paddington|Which author created Paddington Bear?|Michael Bond|A. A. Milne|Kenneth Grahame|Hugh Lofting|Bond is the creator; the others created Pooh, the riverbank animals and Doctor Dolittle.
paddington|Which London railway station gives Paddington Bear his name?|Paddington|Victoria|Waterloo|Euston|The bear is named after the station where he arrives; all four are different London stations.
brown|Which family takes Paddington Bear into their home?|The Browns|The Dursleys|The Weasleys|The Bankses|Paddington joins the Brown family; other fictional families do not take him in.
paddington|Which preserve is Paddington Bear particularly fond of?|Marmalade|Strawberry jam|Blackcurrant jelly|Lemon curd|Marmalade is his signature favourite; the other spreads are not.
carle|Who wrote and illustrated The Very Hungry Caterpillar?|Eric Carle|Eric Hill|Quentin Blake|Axel Scheffler|Carle is both writer and illustrator; Hill is the different Eric who created Spot.
carle|What does the caterpillar become at the end of The Very Hungry Caterpillar?|A butterfly|A bee|A beetle|A dragonfly|The story ends with metamorphosis into a butterfly; the other insects are wrong.
carle|Which fruit does the caterpillar eat on Monday in The Very Hungry Caterpillar?|An apple|A pear|A plum|An orange|Monday's food is one apple; the other fruits occur on different days.
carle|What does the caterpillar eat to feel better after its stomach ache in The Very Hungry Caterpillar?|A green leaf|A slice of cake|An ice cream|A lollipop|The following Sunday leaf relieves it; the other foods are from the previous feast.
wimpy|Who writes and illustrates the Diary of a Wimpy Kid books?|Jeff Kinney|Dav Pilkey|David Walliams|Rick Riordan|Kinney is the author and illustrator; the other writers created different series.
wimpyhome|Which schoolboy tells his story in Diary of a Wimpy Kid?|Greg Heffley|Harry Potter|Alex Rider|Percy Jackson|Greg is the narrator; the others are protagonists of different book series.
wimpy|Who is Greg Heffley's best friend in Diary of a Wimpy Kid?|Rowley Jefferson|Ron Weasley|Tom Gates|Rodrick Heffley|Rowley is his best friend; Rodrick is his brother and the other boys belong to other series.
wimpyhome|What dairy food gives its name to the dreaded playground touch in Diary of a Wimpy Kid?|Cheese|Butter|Yoghurt|Cream|The Cheese Touch is the named playground curse; the other dairy foods do not name it.
dogman|Who created the Dog Man books?|Dav Pilkey|Jeff Kinney|Jim Smith|David McKee|Pilkey created Dog Man; the other children's authors did not.
dogman|What is Dog Man's job in Dav Pilkey's books?|Police officer|Firefighter|Schoolteacher|Train driver|Dog Man is a crime-fighting police officer, not the other occupations.
dogman|Dog Man combines a human body with the head of which animal?|A dog|A cat|A rabbit|A bear|The origin joins a policeman's body to a dog's head; all other animals are wrong.
spot|Who created the picture-book puppy Spot?|Eric Hill|Eric Carle|Michael Bond|Allan Ahlberg|Hill created Spot; Carle is a separate author, and the others created different characters.
spot|Which feature lets young readers look behind objects in Eric Hill's Where's Spot?|Lift-up flaps|A built-in torch|A pair of 3D glasses|A rotating wheel on every page|The classic is a lift-the-flap book; the alternatives are not its defining feature.
elmer|Who created Elmer the patchwork elephant?|David McKee|David Walliams|Eric Hill|John Burningham|McKee created Elmer; the other children's authors are not the creator.
elmer|How is Elmer's skin patterned in David McKee's picture books?|Multicoloured patchwork|Black and white stripes|Blue spots on white|Plain grey all over|Elmer's multicoloured patches distinguish him from the grey elephants; each colour pattern differs.
tiger|Who wrote and illustrated The Tiger Who Came to Tea?|Judith Kerr|Julia Donaldson|Shirley Hughes|Helen Oxenbury|Kerr is both writer and illustrator; the other authors/artists did not create this book.
mog|What kind of pet is Mog in Judith Kerr's picture books?|A cat|A dog|A rabbit|A parrot|Mog is the forgetful family cat; other pets do not describe this character.
dearzoo|Who created the lift-the-flap book Dear Zoo?|Rod Campbell|Roddy Doyle|Michael Rosen|Anthony Browne|Campbell is the creator; the other children's authors did not write this book.
index|Which part of a non-fiction book lists subjects alphabetically with the pages where they appear?|The index|The contents page|The foreword|The dedication|An index organises subjects alphabetically; contents lists sections in order, foreword introduces and dedication honours someone.
glossary|Where in a book would you look for explanations of unfamiliar specialist words?|The glossary|The dedication|The title page|The acknowledgements|A glossary defines specialist vocabulary; none of the other three sections serves that purpose.
appendix|What is an appendix in a non-fiction book?|An extra section of supporting information|A list of bookshops selling it|The protective paper cover|The first sentence of each chapter|An appendix adds supporting material to the main text; the other options describe unrelated things.
foreword|What is a foreword in a book?|An introductory piece before the main text|A scene set after the story ends|A list of printing mistakes|A glossary of difficult words|The foreword introduces the work, unlike an epilogue, errata or glossary.
prologue|What is a prologue in a novel?|An opening section before the main story|A list of sources at the end|A short review on the cover|A summary of the final chapter|A prologue precedes the main narrative; the other options describe different book components.
epilogue|What is an epilogue in a novel?|A concluding section after the main story|A list of chapter titles|A note about the typeface|An introduction by a reviewer|An epilogue provides a final narrative section; none of the alternatives is that section.
author|What is the usual term for the person who writes a book?|Author|Illustrator|Bookseller|Librarian|An author writes the work; illustrations, retail and library roles are distinct functions.
illustrator|What does a book's illustrator create?|Its pictures|Its translation into another language|Its printed copies in a factory|Its sales receipts|Illustrators create images; translators, printers and shops perform the other tasks.
translator|What does a book translator do?|Renders its text in another language|Draws its cover picture|Binds its pages together|Sets its retail price|Translation changes language while conveying meaning; the other production tasks are not translation.
narrator|In a novel, what is the narrator's role?|To tell the story|To sell the finished book|To design the typeface|To repair damaged pages|The narrator is the storytelling voice, distinct from real-world retail, design and conservation roles.
biography|What is a biography?|An account of someone's life|A collection of maps|A list of unfamiliar words|A book of recipes|Biography concerns a person's life; the other options describe an atlas, glossary and cookbook.
autobiography|What distinguishes an autobiography from a biography written by someone else?|The subject writes about their own life|It must be written as poetry|It can contain only photographs|It must describe an imaginary person|Autobiography is a person's own life account; format and fictional-person restrictions are false.
fiction|Which book category is principally made up of invented stories?|Fiction|Biography|Travel reference|History reference|Fiction is imaginative narrative; the alternatives primarily present factual accounts or information.
anthology|What is a literary anthology?|A collection of selected writings|A writer's handwritten signature|A list of spelling corrections|A book's protective cover|An anthology collects works such as poems or stories; the others describe autograph, errata and cover.
trilogy|How many works make up a trilogy?|Three|Two|Four|Five|The term specifies three linked works; each alternative count differs.
sequel|What is a sequel to a novel?|A later work that continues its story|A translation of the same story|An earlier draft of the same book|A review written before publication|A sequel continues an earlier work; translation, draft and review are distinct.
ebook|What is an e-book?|A book in digital form|A book printed only in very large type|A book with no written words|A book with a metal cover|E-books are electronic digital books; the other formats are unrelated to electronic delivery.
audiobook|What is an audiobook?|A recording of a book being read aloud|A book containing only musical notation|A dictionary of rhyming words|A printed manual for repairing radios|Audiobooks present spoken readings, not sheet music, rhyming dictionaries or radio manuals.
hardback|What characterises a hardback book?|A rigid cover|A cover made only of folded paper|Pages that can only be read on a screen|A recording with no printed pages|Hardbacks have stiff covers; paper covers, digital pages and audio are different formats.
paperback|What characterises a paperback book?|A flexible paper or card cover|A rigid wooden cover|Pages carved into stone|A recording on a disc|A paperback has a flexible paper-based cover; the other alternatives do not define paperback binding.
'''

def build():
    out=[]
    for line in rows.strip().splitlines():
        source,prompt,answer,*rest=line.split('|')
        assert len(rest)==4
        out.append({'draftID':f'easy-10-{len(out)+1:03d}','categoryID':'10','difficulty':'easy','prompt':prompt,'answers':[answer,*rest[:3]],'correctIndex':0,'rationale':rest[3],'sourceURL':sources[source],'reviewStatus':'draft_awaiting_author_final_check'})
    return out
if __name__=='__main__':
    draft=build()
    (HERE/'draft.json').write_text(json.dumps(draft,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(f'{len(draft)} original candidates; none approved by this script.')
