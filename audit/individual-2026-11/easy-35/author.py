"""Original accessible language candidates, awaiting their separate final check."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
GRAMMAR='https://dictionary.cambridge.org/grammar/british-grammar/'
sources={
'classes':GRAMMAR+'word-classes-and-phrase-classes',
'plurals':GRAMMAR+'nouns-singular-and-plural',
'past':GRAMMAR+'past-simple-i-worked',
'comparison':GRAMMAR+'adjectives-comparative-and-superlative',
'articles':GRAMMAR+'a-an-and-the',
'fewer':GRAMMAR+'less-or-fewer',
'their':GRAMMAR+'there-their-or-they-re',
'contractions':GRAMMAR+'contractions',
'apostrophe':GRAMMAR+'apostrophe',
'punctuation':GRAMMAR+'punctuation',
'prefixes':GRAMMAR+'prefixes',
'suffixes':GRAMMAR+'suffixes',
}
rows='''classes|Which word is a noun in 'The rabbit hops quickly'?|Rabbit|Hops|Quickly|The|Rabbit names the animal; hops is the verb, quickly an adverb and the an article.
classes|Which word is the verb in 'Those birds sing beautifully'?|Sing|Those|Birds|Beautifully|Sing states the action; those is a determiner, birds a noun and beautifully an adverb.
classes|Which word is the adjective in 'A bright star shines'?|Bright|A|Star|Shines|Bright describes the star; the other words are an article, noun and verb.
classes|Which word is the adverb in 'The dog barked loudly'?|Loudly|The|Dog|Barked|Loudly modifies how it barked; the other options are article, noun and verb.
classes|Which pronoun can replace Maya in 'Maya is reading'?|She|Her|Hers|Herself|The subject pronoun she fits; her, hers and herself are different pronoun forms.
classes|Which word is a preposition in 'The keys are under the mat'?|Under|Keys|Are|Mat|Under describes the spatial relationship; keys and mat are nouns and are is a verb.
classes|Which word joins the names in 'Sam and Jo laughed'?|And|Sam|Jo|Laughed|And is the coordinating conjunction; the names and verb do not join the names.
articles|Which indefinite article completes 'I ate ___ apple'?|An|A|These|Those|Apple begins with a vowel sound, so an fits; a is wrong here and plural demonstratives cannot modify singular apple.
plurals|What is the standard plural of child?|Children|Childs|Childes|Childrens|Children is the irregular plural; the other forms are not standard.
plurals|What is the usual plural of mouse when referring to the animal?|Mice|Mouses|Mousees|Mices|Animal mouse normally takes mice; computer-device variation is excluded explicitly.
plurals|What is the standard plural of tooth?|Teeth|Tooths|Toothes|Teethe|Teeth is the noun plural; teethe is a verb and other forms are nonstandard.
plurals|What is the standard plural of foot when referring to the body part?|Feet|Foots|Footes|Feets|Feet is the body-part plural; the other forms are wrong in this sense.
plurals|What is the standard plural of thief?|Thieves|Thiefs|Thiefes|Thievs|Thieves changes f to ves; the other spellings are not standard.
past|What is the simple past form of go?|Went|Gone|Going|Goed|Went is finite simple past; gone is a participle, going an ing-form and goed nonstandard.
past|What is the simple past form of eat?|Ate|Eaten|Eating|Eated|Ate is simple past; eaten is the past participle and the others are not the past form.
past|What is the simple past form of write?|Wrote|Written|Writing|Writed|Wrote is simple past; written participle and writing ing-form differ; writed is nonstandard.
past|What is the simple past form of see?|Saw|Seen|Seeing|Seed|Saw is simple past; seen is participle, seeing ing-form and seed not the past of see.
past|What is the simple past form of bring?|Brought|Brang|Bringed|Bringing|Brought is standard; brang/bringed are nonstandard and bringing is not simple past.
comparison|What is the standard comparative form of good?|Better|Best|Gooder|More good|Better compares; best is superlative and the other two are not the ordinary standard form.
comparison|What is the standard superlative form of bad?|Worst|Worse|Baddest|More bad|Worst is standard superlative; worse is comparative and other alternatives are nonstandard for the intended sense.
fewer|Which word completes 'There are ___ books on this shelf than on that one' in standard English?|Fewer|Less|Least|Little|Countable plural books takes fewer in the comparison; the other quantifiers do not fit standard usage here.
their|Which word completes '___ coats are hanging by the door' to show that the coats belong to them?|Their|There|They're|They|Their is the possessive determiner; there is a place word, they're means they are and they lacks the possessive form.
contractions|What does they're stand for?|They are|They were|Their|There|They're contracts they are; the other options are different forms/words.
contractions|In 'It's cold today', what does it's stand for?|It is|It has|Its|It was|In this sentence only it is fits; it has is another expansion in other contexts but not this one.
contractions|In 'You're welcome', what does you're stand for?|You are|You were|You have|Your|You're contracts you are; other forms are not the expansion in this phrase.
apostrophe|What does the apostrophe show in 'the cat's bowl'?|The bowl belongs to one cat|There are several cats|The word cat is shortened|The bowl is made from a cat|Singular possessive cat's indicates ownership; it is not plural or an abbreviation here.
punctuation|Which mark normally ends a direct written question?|?|!|,|;|The question mark signals a direct interrogative; the other punctuation marks do not normally end it.
punctuation|Which punctuation mark is used after Stop to show a forceful command, as in 'Stop!'?|An exclamation mark|A question mark|A comma|A colon|The mark shown is an exclamation mark and emphasises the command.
punctuation|Which mark normally follows a complete clause to introduce a list in the same sentence?|A colon|A question mark|An exclamation mark|A full stop|A colon introduces the following list; the other marks do not connect this clause and list in one sentence.
punctuation|What punctuation mark joins the two words in well-known?|A hyphen|An apostrophe|A semicolon|A comma|The linking mark is a hyphen; the other punctuation marks have different forms/functions.
prefixes|What does the prefix un- do to happy in the word unhappy?|Gives it the opposite meaning|Makes it a plural noun|Makes it past tense|Turns it into a question|Un- negates happy; it does not mark number, tense or interrogative form.
suffixes|What does -less mean in careless?|Without|Full of|Before|Again|Careless means without care; the other affix meanings are different.
prefixes|What does re- mean in reread?|Again|Not|Under|Before|Reread means read again; negation, location and before are different meanings.
suffixes|What does -ful suggest in hopeful?|Full of|Without|After|Against|The adjective means having hope; other meanings do not fit the suffix here.
begin|Which word is closest in meaning to begin?|Start|Finish|Stop|Pause|Start is the synonym; other verbs end or interrupt rather than begin.
ancient|Which word is closest to the opposite of ancient?|Modern|Old|Historic|Aged|Modern contrasts with ancient; other words refer to age or the past.
rapid|Which word is closest in meaning to rapid?|Fast|Slow|Late|Quiet|Rapid means fast; other adjectives describe low speed, timing or sound.
generous|Which word is closest to the opposite of generous?|Stingy|Charitable|Giving|Kind|Stingy means unwilling to give; the other qualities align with generosity.
enormous|Which word is closest in meaning to enormous?|Huge|Tiny|Slight|Narrow|Huge means very large; other options do not express the same size.
expand|Which word is closest to the opposite of expand?|Contract|Grow|Stretch|Enlarge|Contract reduces size; grow, stretch and enlarge move towards expansion.
quiet|Which word is closest in meaning to quiet?|Silent|Loud|Noisy|Deafening|Silent is closest to low/no sound; the others describe noise.
lend|Which verb means giving something to someone temporarily, expecting it back?|Lend|Borrow|Buy|Keep|Lend is from the giver's perspective; borrow is the recipient's perspective and buy/keep do not describe a loan.
homophone|Which pair of English words sounds the same in standard pronunciation?|Sea and see|Cat and coat|Pen and pan|Ship and sheep|Sea/see are homophones; the other pairs have different vowel sounds.
past|What tense is walked in 'Yesterday I walked home'?|Past tense|Present tense|Future tense|An instruction|The sentence places the walk yesterday and uses simple past; no future/present/imperative reading fits.
bear|Which word can mean both an animal and 'to tolerate'?|Bear|Deer|Fox|Hare|Bear has both senses; deer has no such verb and fox/hare verbs have different meanings.
compound|Which word is formed by joining two whole words?|Toothbrush|Quickly|Unkind|Helpful|Tooth plus brush forms a compound; ly, un and ful are affixes rather than free words here.
contractions|What does can't stand for?|Cannot|Can not ever|Could not|Will not|Cannot is the ordinary expansion; other alternatives change or add meaning.
contractions|What does won't stand for?|Will not|Would not|Was not|Want not|Won't is the contraction of will not; the other phrases are not equivalent.
bat|Which word can mean both a flying mammal and a piece of sports equipment?|Bat|Rat|Hare|Mole|Bat has the two requested senses; the other mammals do not name the striking implement.
break-the-ice|What does break the ice mean when people meet?|Make people feel more relaxed and start talking|End the meeting immediately|Reveal a secret|Refuse to speak to anyone|The social idiom concerns easing tension, not ending, disclosing or silence.
rain-cats-and-dogs|What does it's raining cats and dogs mean?|It is raining very heavily|It is snowing lightly|It is becoming sunny|Animals are falling from the sky|The idiom means heavy rain, not literal animals or another weather condition.
a-piece-of-cake|If someone says a task is a piece of cake, what do they mean?|It is easy|It is dangerous|It is impossible|It is very expensive|The idiom describes ease, not risk, impossibility or cost.
under-the-weather|What does feeling under the weather mean?|Feeling unwell|Feeling very energetic|Feeling extremely hungry|Feeling proud of a success|The idiom means somewhat ill; the other states differ.
hit-the-books|What does hit the books mean?|Study|Damage a book|Go to sleep|Write a shopping list|The idiom refers to studying; the literal book-hitting option is not the idiomatic meaning.
spill-the-beans|What does spill the beans mean?|Reveal a secret|Cook a meal|Hide the truth|Lose a race|The idiom is disclosure, not cooking, concealment or sporting loss.
cost-an-arm-and-a-leg|If something costs an arm and a leg, what does that mean?|It is very expensive|It is completely free|It is easy to carry|It is made of wood|The figurative cost is high, not a statement of price-free status, weight or material.
on-cloud-nine|What does being on cloud nine mean?|Being very happy|Being very ill|Being confused about directions|Being impatient for a meal|The idiom describes great happiness, not illness, navigation or hunger.
once-in-a-blue-moon|How often does something happen if it happens once in a blue moon?|Very rarely|Every morning|Several times an hour|Every weekend|The idiom means rarely, not any of the regular frequent intervals.
get-cold-feet|What does getting cold feet mean before an important event?|Becoming nervous and hesitant|Growing taller|Learning the route by heart|Winning a prize|The idiom is anxiety/reluctance, not growth, memorisation or success.
pull-someone-s-leg|If someone says 'I'm pulling your leg', what do they mean?|They are joking or teasing you|They are asking you to hurry|They are offering a serious promise|They are giving you directions|The idiom is playful deception/teasing, not instructions or sincere commitment.
fr:fromage|What does the French word fromage mean?|Cheese|Chicken|Butter|Bread|Fromage means cheese; the other foods have different French names.
fr:pain|What does the French word pain mean?|Bread|Cheese|Rice|Meat|French pain is bread, not the English word for discomfort; other foods are incorrect.
fr:chien|What animal does the French word chien mean?|Dog|Cat|Horse|Rabbit|Chien denotes a dog; the other animal names differ.
fr:cheval|What animal does the French word cheval mean?|Horse|Dog|Cow|Sheep|Cheval means horse, not the other farm/domestic animals.
fr:maison|What does the French word maison mean?|House|School|Shop|Bridge|Maison is a house; other places/structures have different words.
fr:jardin|What does the French word jardin mean?|Garden|Kitchen|Street|Beach|Jardin means garden; the other outdoor/household locations are wrong.
fr:rouge|Which colour does the French word rouge mean?|Red|Blue|Green|Yellow|Rouge is red; the three other colours differ.
fr:bleu|Which colour does the French word bleu mean?|Blue|Red|Black|White|Bleu is blue; other colour choices are wrong.
fr:vert|Which colour does the French word vert mean?|Green|Purple|Orange|Pink|Vert is green; the other colours have different French names.
fr:lundi|Which day is lundi in French?|Monday|Tuesday|Friday|Sunday|Lundi is Monday; the other days differ.
es:agua|What does the Spanish word agua mean?|Water|Milk|Bread|Salt|Agua is water; the three other everyday nouns have different Spanish words.
es:perro|What animal does the Spanish word perro mean?|Dog|Cat|Horse|Duck|Perro denotes a dog; no other offered animal fits.
es:gato|What animal does the Spanish word gato mean?|Cat|Dog|Rabbit|Goat|Gato means cat; the other animals have different names.
es:casa|What does the Spanish word casa mean?|House|School|Church|Shop|Casa is house, not the other buildings.
es:pan|What does the Spanish word pan mean?|Bread|Milk|Rice|Egg|Pan means bread, not the English cooking vessel; other food words are wrong.
es:leche|What does the Spanish word leche mean?|Milk|Water|Salt|Sugar|Leche is milk; other ingredients have different Spanish names.
es:libro|What does the Spanish word libro mean?|Book|Table|Door|Chair|Libro means book; the other household objects differ.
es:buenas-noches|What greeting can buenas noches express in Spanish?|Good evening or good night|Good morning only|Thank you|Please|The phrase covers evening greeting and nighttime farewell; both correct senses are kept together.
es:por-favor|What does the Spanish phrase por favor mean?|Please|Thank you|Goodbye|Good morning|Por favor is the polite request marker please; the other phrases differ.
es:gracias|What does the Spanish word gracias mean?|Thank you|Hello|Please|Goodbye|Gracias expresses thanks; the other greetings/request markers are distinct.
it:grazie|What does the Italian word grazie mean?|Thank you|Goodbye|Hello|Please|Grazie expresses thanks; the other expressions are not the translation.
it:prego|When someone replies prego after being thanked in Italian, what do they mean?|You're welcome|Good night|I'm sorry|Goodbye|Prego has several uses, so the reply-to-thanks context fixes you're welcome.
it:buongiorno|What greeting does the Italian word buongiorno express?|Good morning or good day|Good night|Thank you|Goodbye|Buongiorno covers daytime greeting, not night farewell or thanks.
it:arrivederci|What does the Italian word arrivederci mean?|Goodbye|Thank you|Please|Good morning|Arrivederci is a leave-taking expression; other social phrases differ.
it:acqua|What does the Italian word acqua mean?|Water|Milk|Wine|Juice|Acqua is water; the three other liquids have different words.
it:cane|What animal does the Italian word cane mean?|Dog|Cat|Horse|Bird|Italian cane means dog, not English walking stick; other animals are wrong.
it:gatto|What animal does the Italian word gatto mean?|Cat|Dog|Mouse|Fish|Gatto is cat; other animal nouns differ.
it:pane|What does the Italian word pane mean?|Bread|Cheese|Meat|Salt|Pane means bread, not English window glass; other food options are wrong.
it:luna|What does the Italian word luna mean?|Moon|Sun|Star|Cloud|Luna is moon; other sky objects/phenomena differ.
it:sole|What does the Italian word sole mean in the sky?|Sun|Moon|Star|Cloud|Sole has other senses, so the sky context fixes sun; other celestial words differ.
de:danke|What does the German word danke mean?|Thank you|Goodbye|Please|Good night|Danke expresses thanks; the other social phrases differ.
de:bitte|In a polite request, what does the German word bitte mean?|Please|Goodbye|Good morning|Good night|Bitte can also mean you're welcome, but a request context fixes please and that alternative is not offered.
de:guten-morgen|What does Guten Morgen mean in German?|Good morning|Good night|Thank you|Goodbye|The phrase is the morning greeting; the others have different German forms.
de:auf-wiedersehen|What does Auf Wiedersehen mean in German?|Goodbye|Please|Thank you|Good morning|It is a leave-taking phrase, not a request marker or thanks/morning greeting.
de:Hund|What animal does the German word Hund mean?|Dog|Cat|Horse|Rabbit|Hund is dog; the other animals differ. German nouns require initial capitals.
de:Katze|What animal does the German word Katze mean?|Cat|Dog|Cow|Duck|Katze is cat; the other animal names differ.
de:Haus|What does the German word Haus mean?|House|School|Shop|Bridge|Haus is house; the other structures differ.
de:Brot|What does the German word Brot mean?|Bread|Cheese|Milk|Butter|Brot means bread; the other foods have different German names.
de:Wasser|What does the German word Wasser mean?|Water|Milk|Juice|Wine|Wasser is water; other drink nouns are wrong.
de:Milch|What does the German word Milch mean?|Milk|Water|Salt|Sugar|Milch is milk; the other ingredients differ.
'''
def source(key):
    if key in sources:return sources[key]
    if ':' in key:
        language,word=key.split(':',1)
        return 'https://dictionary.cambridge.org/dictionary/'+{'fr':'french-english','es':'spanish-english','it':'italian-english','de':'german-english'}[language]+'/'+word
    return 'https://dictionary.cambridge.org/dictionary/english/'+key
def build():
    q=[]
    for line in rows.strip().splitlines():
        key,prompt,correct,*tail=line.split('|');assert len(tail)==4
        q.append({'draftID':f'easy-35-{len(q)+1:03d}','categoryID':'35','difficulty':'easy','prompt':prompt,'answers':[correct,*tail[:3]],'correctIndex':0,'rationale':tail[3],'sourceURL':source(key),'reviewStatus':'draft_awaiting_author_final_check'})
    return q
if __name__=='__main__':
    q=build();(HERE/'draft.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print(f'{len(q)} unapproved candidates')
