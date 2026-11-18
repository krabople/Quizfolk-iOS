"""Explicit individual author second-pass records for the language batch."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
edits={
5:{'prompt':"Which pronoun can replace 'the girl' in 'The girl is reading'?"},
21:{'prompt':"Under the traditional rule for countable nouns, which word completes 'There are ___ books on this shelf than on that one'?"},
27:{'sourceURL':'https://dictionary.cambridge.org/dictionary/english/question-mark'},
28:{'sourceURL':'https://dictionary.cambridge.org/dictionary/english/exclamation-mark'},
29:{'sourceURL':'https://dictionary.cambridge.org/dictionary/english/colon'},
30:{'sourceURL':'https://dictionary.cambridge.org/dictionary/english/hyphen'},
44:{'answers':['Past simple','Present simple','Present continuous','Future simple']},
47:{'answers':['Cannot','Could not','Will not','Would not']},
50:{'prompt':"What does the idiom 'break the ice' mean when people meet?"},
51:{'prompt':"What does the expression 'it's raining cats and dogs' mean?"},
53:{'prompt':"What does the idiom 'feeling under the weather' mean?"},
54:{'prompt':"What does the idiom 'hit the books' mean?"},
55:{'prompt':"What does the idiom 'spill the beans' mean?"},
56:{'prompt':"If something 'costs an arm and a leg', what does that idiom mean?"},
57:{'prompt':"What does the idiom 'being on cloud nine' mean?"},
58:{'prompt':"How often does something happen if it happens 'once in a blue moon'?"},
59:{'prompt':"What does the idiom 'getting cold feet' mean before an important event?"},
60:{'prompt':"What does the idiom 'pulling your leg' mean?",'answers':['Joking or teasing you','Asking you to hurry','Making a serious promise','Giving you directions']},
}
for n,word in zip(range(9,21),['child','mouse','tooth','foot','thief','go','eat','write','see','bring','good','bad']):
    edits[n]={'sourceURL':'https://dictionary.cambridge.org/dictionary/english/'+word}
notes='''1|Rabbit is the only noun in this sentence. Hops is finite verb, quickly adverb and the article; capitalised answer labels do not change their classes.
2|Sing expresses the birds' action. Those is determiner, birds noun and beautifully adverb; all four appear in the sentence.
3|Bright describes star. A is article, star noun and shines verb; exactly one adjective.
4|Loudly modifies barked. The is article, dog noun and barked verb; exactly one adverb.
5|She is the subject form, unlike her/hers/herself. Replace name-only reference with explicit 'the girl' to keep the substitution clear.
6|Under is the spatial preposition. Keys/mat are nouns and are a verb; the sentence supplies a clear relationship.
7|And coordinates Sam and Jo. The two names and laughed do not join the names; punctuation and quoting checked.
8|An precedes apple's vowel sound. A is wrong in this position; plural these/those cannot qualify singular apple. Do not offer the, which would also fit grammatically.
9|Children is the standard plural. Childs, childes and childrens are incorrect; replace generic reference with child entry showing plural children.
10|Mice is animal plural. Mouses can occur for computer devices, explicitly excluded; mousees/mices are nonstandard. Use mouse's animal entry.
11|Teeth is noun plural. Tooths/toothes are wrong and teethe a verb; direct tooth headword confirms the form.
12|Feet is the body-part plural. Foots/footes/feets are not standard here; body-part context excludes special technical forms.
13|Thieves is the standard spelling. Thiefs/thiefes/thievs are wrong; exact thief headword inspected rather than a generic plurals page.
14|Went is simple past, gone a participle and going an ing-form. Goed is nonstandard; direct go entry confirms went/gone distinction.
15|Ate is simple past, eaten participle and eating ing-form. Eated is nonstandard; exact eat forms inspected.
16|Wrote is simple past. Written is participle, writing ing-form and writed nonstandard; headword gives wrote/written.
17|Saw is simple past. Seen and seeing are other forms; seed is not this verb's past. Direct headword inspected.
18|Brought is the standard past, not brang/bringed/bringing. Direct bring entry confirms brought for past and participle.
19|Better is good's comparative. Best is superlative; gooder/more good are not its normal standard comparative. Direct good entry confirms forms.
20|Worst is bad's superlative. Worse is comparative, baddest nonstandard in this ordinary sense and more bad not superlative. Direct bad entry inspected.
21|Fewer is traditionally preferred for countable books. Acknowledge colloquial less by specifying the traditional rule; least/little do not fit this comparative construction.
22|Their expresses possession. There/they're/they do not fill the possessive determiner slot; plural coats does not change their.
23|They're expands to they are. They were, their and there differ; apostrophe spelling checked.
24|It's is it is in this exact sentence. It has is a valid expansion elsewhere but cannot form 'It has cold today'; its/it was also wrong.
25|You're is you are. You were/you have are not this contraction and your is possessive; context fixes the phrase.
26|Cat's bowl shows singular ownership. Several cats would require cats'; neither shortening nor material is intended.
27|Question mark normally closes a direct question. Exclamation, comma and semicolon do not; change to exact dictionary entry so the source is not hidden deep in a long general punctuation article.
28|The displayed forceful-command mark is an exclamation mark. Question, comma and colon are different symbols; use exact entry.
29|Colon introduces a list after a complete clause. The other three marks terminate/question rather than introduce this same-sentence list; exact colon sense is the source.
30|Hyphen is the mark in well-known. Apostrophe, semicolon and comma are different marks; exact hyphen entry replaces a broad article.
31|Un- negates happy. It does not mark noun number, verb tense or a question; context avoids unrelated un- words.
32|-less means without in careless. Full of, before and again belong to other meanings; do not generalise every spelling ending less as an affix.
33|Re- makes reread 'read again'. Not/under/before do not describe this prefix in the chosen word.
34|-ful indicates having/full of hope in hopeful. Without/after/against are wrong in this word; 'suggest' avoids claiming a literal physical container.
35|Start is begin's synonym. Finish/stop/pause end or interrupt an activity, so none is a second close match.
36|Modern is closest opposite of ancient. Old/historic/aged all concern age or past times; relative wording avoids a rigid historical date boundary.
37|Fast is closest to rapid. Slow/late/quiet describe different speed, timing or sound qualities.
38|Stingy contrasts with generous. Charitable/giving/kind align with giving rather than its opposite; intended adjective senses are clear.
39|Huge matches enormous. Tiny/slight/narrow do not mean extremely large; all choices are adjectives.
40|Contract is opposite of expand. Grow/stretch/enlarge increase extent rather than reduce it.
41|Silent is closest to quiet among these choices. Loud/noisy/deafening all concern high noise; not a claim that quiet always means absolute silence.
42|Lend is temporary giving from the owner's perspective. Borrow is receiving, buy purchase and keep retaining; expecting return is explicit.
43|Sea and see are homophones. Cat/coat, pen/pan and ship/sheep have different vowels in ordinary standard pronunciation.
44|Walked is simple past with Yesterday. Use four parallel tense labels; present, continuous and future forms do not fit this finite verb phrase.
45|Bear can be the mammal or tolerate. Deer, fox and hare lack that second meaning; any unrelated verb senses do not answer it.
46|Toothbrush joins free words tooth and brush. Quickly/unkind/helpful use affixes, not two whole words; compound definition inspected.
47|Can't expands to cannot. Replace awkward 'can not ever' with standard negative phrases; could/will/would change the auxiliary.
48|Won't is will not. Would not, was not and want not are not its expansion.
49|Bat is both mammal and striking implement. Rat, hare and mole do not satisfy both descriptions.
50|Ice-breaking idiom relaxes first meetings. Make idiomatic sense explicit; ending a meeting, revealing secrets and staying silent are different meanings.
51|Cats-and-dogs expression means heavy rain. Light snow, sunshine and literal falling animals are not the figurative meaning; name it an expression.
52|Piece of cake means easy in a task context. Dangerous/impossible/expensive are not this idiom's meaning.
53|Under the weather means unwell. Energetic/hungry/proud are different states; explicitly ask for the idiom.
54|Hit the books means study. Damage is a literal decoy; sleep and shopping list do not fit. Add idiom wording to exclude a literal interpretation.
55|Spill the beans reveals a secret. Cooking, hiding the truth and losing are different; explicitly figurative.
56|Arm-and-leg cost means expensive. Free, portable and wooden are not the figurative meaning; explicitly identify idiom.
57|Cloud nine means very happy/excited. Illness, navigation confusion and hunger are wrong; make idiom context explicit.
58|Blue moon expression means rarely. Morning/hourly/weekend intervals are all frequent regular schedules, not rare occurrences.
59|Cold feet idiom is nervous hesitation. Growth, memorising a route and winning are different; exclude literal cold-temperature interpretation.
60|Pulling a leg means joking/teasing. Rewrite answer forms to fit the new explicit idiom question; hurry, serious promise and directions do not fit.
61|French fromage is cheese. Chicken/butter/bread have different names; bilingual entry gives cheese.
62|French pain is bread. Cheese/rice/meat are wrong; language qualifier excludes the English false friend.
63|Animal chien is dog. Cat/horse/rabbit are different animals; specifying animal excludes figurative derogatory senses.
64|Cheval is horse. Dog/cow/sheep differ; bilingual horse translation inspected.
65|Maison is house/home. School/shop/bridge are not offered synonyms; no second valid home answer.
66|Jardin is garden/yard. Kitchen/street/beach do not fit; not a claim that garden is the only translation in every context.
67|Colour rouge is red. Blue/green/yellow are wrong; colour qualifier excludes red-wine usage.
68|Colour bleu is blue. Red/black/white differ; colour qualifier excludes rare-cooked meat sense.
69|Colour vert is green. Purple/orange/pink are wrong; none duplicates a figurative sense offered.
70|Lundi is Monday. Tuesday/Friday/Sunday are different named days; day question is unambiguous.
71|Agua is water. Milk/bread/salt are distinct Spanish nouns; ordinary food/drink sense is clear.
72|Animal perro is dog. Cat/horse/duck differ; animal qualifier excludes colloquial insults.
73|Animal gato is cat. Dog/rabbit/goat are wrong; gato can mean a mechanical jack but that sense is excluded and not offered.
74|Casa means house/home. School/church/shop are different buildings; no alternate home translation offered.
75|Spanish pan is bread. Milk/rice/egg are wrong; explicitly Spanish avoids English cooking-pan sense.
76|Leche is milk. Water/salt/sugar differ; no second offered food translation fits.
77|Libro means book. Table/door/chair are distinct objects; ordinary noun sense tested.
78|Buenas noches is evening greeting/night farewell. Both senses are grouped in one answer; morning-only, thanks and please are incorrect.
79|Por favor means please. Thank you/goodbye/good morning are different social expressions.
80|Gracias means thank you/thanks. Hello/please/goodbye are not equivalents; only one thanks choice offered.
81|Italian grazie means thank you. Goodbye/hello/please differ; not confused with Spanish gracias spelling.
82|Prego has several uses, so specify a response to thanks. You're welcome fits; night/apology/farewell do not fit that conversational context.
83|Buongiorno is the daytime greeting. Group morning/day rather than force a single time-specific translation; night/thanks/goodbye are wrong.
84|Arrivederci means goodbye. Thanks/please/morning greeting are different; ordinary leave-taking sense used.
85|Acqua is water. Milk/wine/juice are other liquids with different Italian words.
86|Animal cane is dog. Cat/horse/bird differ; language qualifier avoids English cane walking-stick ambiguity.
87|Gatto is cat. Dog/mouse/fish differ; animal context pins the noun.
88|Pane is bread. Cheese/meat/salt are different foods; Italian qualifier excludes English pane of glass.
89|Luna is moon. Sun/star/cloud differ; ordinary sky-word meaning and capitalisation checked.
90|Sky context fixes sole as sun. Moon/star/cloud are other celestial/weather words; other grammatical forms of sole cannot make another choice correct.
91|Danke expresses thanks. Farewell/please/night greeting are distinct; no thanks synonym offered separately.
92|Bitte in a polite request means please. Its welcome sense exists but is excluded by context and not offered; other greetings are wrong.
93|Guten Morgen is good morning. Night/thanks/farewell differ; German phrase capitalisation correct.
94|Auf Wiedersehen is goodbye. Please/thanks/morning greeting differ; capitalised nominal Wiedersehen preserved.
95|Hund is dog. Cat/horse/rabbit differ; noun begins with a capital in German.
96|Katze is cat. Dog/cow/duck differ; noun capitalisation checked.
97|Haus is house/home. School/shop/bridge differ; Home not offered as a second correct translation.
98|Brot is bread. Cheese/milk/butter differ; noun begins with capital B.
99|Wasser is water. Milk/juice/wine differ; noun capitalisation preserved.
100|Milch is milk. Water/salt/sugar differ; noun capitalisation and ordinary literal sense checked.
'''
rows=[]
for line in notes.strip().splitlines():
    n,note=line.split('|',1);n=int(n);q=draft[n-1]
    d={'row':n,'action':'edit' if n in edits else 'keep','prompt':q['prompt'],'note':note,
       'sourceReview':'Individual author second pass of prompt, all four answers, contextual meaning, spelling/grammar and sole correct option. Relevant Cambridge grammar, exact headword/inflection or bilingual translation inspected; not independent review.'}
    if n in edits:d['recommendedChanges']=edits[n]
    rows.append(d)
assert [r['row'] for r in rows]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'reviewer':'root (author second editorial pass)','independent':False,
 'sourceAccessNote':'All source groups retrieved and inspected in small batches. Shared grammar pages reused rather than repeatedly read as new evidence; exact headword inflections checked separately for twelve irregular forms. Forty bilingual entries inspected, preserving animal/colour/conversation context where a word has multiple senses. Template-word overlap hits are different vocabulary items, not repeated facts. Source excerpts remain private; this file records explicit final-pass judgments and edits, not automated approval.',
 'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Recorded 100 explicit author final checks; apply edits before publication.')
