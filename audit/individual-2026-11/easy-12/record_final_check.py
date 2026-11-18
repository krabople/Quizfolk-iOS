"""Explicit individual author second-pass judgments. No independent review claimed."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
D='https://dictionary.cambridge.org/dictionary/english/'
edits={
1:{'answers':['How fast or slowly the music moves','How high or low its notes are','How loud or quiet it is','How beats are grouped into bars']},
2:{'answers':['A sequence of notes forming a tune','The loudness of a performance','Several notes sounded as a chord','The instrument used to keep time']},
3:{'answers':['Notes sounding together','The speed of a piece','The words of a song','The length of each note']},
4:{'answers':['The pattern of sounds and silences in time','The range from lowest to highest pitch','The size of the orchestra','The sharps or flats in the key signature']},
5:{'answers':['A group of notes sounded together','One player performing alone','A tune played one note at a time','The words of a song']},
7:{'answers':['How high or low it sounds','How loud or quiet it sounds','How long it lasts','Which instrument makes it']},
8:{'answers':['Loudness and changes in loudness','The pattern of note pitches','The speed of the beat','The number of bars in the piece']},
11:{'answers':['The pitches represented by its lines and spaces','The number of beats in each bar','The words sung by the choir','The duration of each written note']},
14:{'answers':['Cancels a sharp or flat for the affected note','Makes every note louder','Adds an extra beat to a bar','Makes every note twice as long']},
17:{'prompt':'What does the musical instruction crescendo ask performers to do?','answers':['Gradually get louder','Gradually get quieter','Gradually speed up','Gradually slow down']},
23:{'sourceURL':'https://www.oxfordlearnersdictionaries.com/definition/english/presto_2'},
29:{'answers':['Return to the beginning','Skip to the last note','Repeat only the previous bar','Change to a different key']},
30:{'sourceURL':D+'quarter-note'},31:{'sourceURL':D+'eighth-note'},32:{'sourceURL':D+'half-note'},33:{'sourceURL':D+'whole-note'},
36:{'answers':['How beats are grouped into bars','Which sharps and flats belong to the key','How loudly the music should be played','Which instruments perform each part']},
37:{'answers':['The sharps or flats normally used in the music','The number of beats in each bar','The speed of the performance','The number of movements']},
38:{'answers':['Its words','Its main melody without words','Its chord changes alone','Its instructions for loudness']},
39:{'answers':['Written notation showing the music to be performed','A device that keeps a steady beat','The words of a song without its music','A method of tuning strings']},
40:{'answers':['Adjusting it to produce the intended pitches','Doubling the length of every note','Changing the written time signature','Removing bars from the score']},
41:{'prompt':'What is a capo used for on a guitar?','answers':['Clamping across the strings to raise their pitches','Amplifying sound through a speaker','Keeping a steady beat for practice','Bowing the strings instead of plucking them'],'sourceURL':D+'capo','rationale':'A capo clamps across the fingerboard, shortening the sounding strings and raising pitch; this is not a pickup, metronome or bow.'},
42:{'answers':['The distance between their pitches','The speed of the beat','The loudness of a chord','The number of players in an ensemble']},
43:{'sourceURL':'https://www.yamaha.com/en/musical_instrument_guide/piano/index.html'},
48:{'sourceURL':'https://philharmonia.co.uk/resources/instruments/tuba/'},
49:{'prompt':'Despite usually being made of brass, the saxophone belongs to which instrument family?','sourceURL':'https://hub.yamaha.com/winds/wood/the-woodwind-family-explained/'},
54:{'sourceURL':'https://philharmonia.co.uk/resources/instruments/viola/'},
70:{'sourceURL':'https://www.bate.ox.ac.uk/harpsichord'},
71:{'prompt':'In a standard four-part choir with soprano, alto, tenor and bass parts, which part is highest?'},
72:{'prompt':'In a standard four-part choir with soprano, alto, tenor and bass parts, which part is lowest?'},
75:{'answers':['A high, light vocal register','Singing with no lyrics at all','Singing as loudly as possible','Always singing below the normal range']},
78:{'prompt':'How many featured performers does a duet have?'},
79:{'prompt':'What does pizzicato tell string players to do?','answers':['Pluck the strings with their fingers','Bow the strings smoothly','Play every note as loudly as possible','Gradually slow down'],'sourceURL':D+'pizzicato','rationale':'Pizzicato means plucking with fingers rather than bowing; not a dynamic or tempo instruction.'},
83:{'prompt':'In choral music, what is a choir?','answers':['A group of singers','A group of brass players','A quartet of bowed string players','A group of drummers']},
84:{'answers':['Directs the performers during the music','Writes every piece performed','Performs every solo part','Plays all the percussion instruments']},
85:{'answers':['They perform the same melody together, at the same pitch or in octaves','They all play different tunes','They alternate one note each','They all stop at different times'],'rationale':'Common musical unison includes octave doubling as Cambridge states; the musicians perform the same line together, rather than independent different lines or alternating notes.'},
95:{'prompt':'A standard string quartet has two violins, a viola and which other instrument?','answers':['Cello','Double bass','Harp','Guitar'],'sourceURL':'https://www.berliner-philharmoniker.de/en/about-us/orchestra/ensembles/philharmonisches-streichquintett/','rationale':'The standard quartet is two violins, viola and cello; Berlin Philharmonic describes adding double bass to that quartet to form its distinctive quintet.'},
96:{'prompt':'What does vibrato add to a sustained musical note?','answers':['A slight, regular wavering','An abrupt silence','A second melody played backwards','A steady drumbeat'],'sourceURL':D+'vibrato','rationale':'Vibrato is a repeated slight wavering/shaking of the note, not a rest, separate tune or percussion beat.'},
100:{'prompt':'What does transposing a piece of music mean?','answers':['Playing or writing it in a different key','Reversing the order of its lyrics','Doubling the number of performers','Changing every rest into a loud note'],'sourceURL':D+'transpose','rationale':'Musical transpose means change key, not reorder lyrics, enlarge ensemble or change rests to notes.'},
}
notes='''1|Tempo is speed, not pitch, loudness or metre. Inspect musical rather than general-activity sense; replace unrelated distractors with those actual musical properties. Fast/slow wording accessible and correct.
2|Melody is ordered notes/tune. Volume,simultaneous chord and timekeeping instrument are different concepts. Replace off-topic programme/drumstick choices; sequence need not exclude accompaniment.
3|Harmony concerns notes together. Speed,lyrics,note lengths are different dimensions. Cambridge musical sense inspected; avoid requiring harmony always sound pleasant despite introductory definition wording.
4|Rhythm concerns sounds/silences in time. Pitch range,ensemble size,key signature do not define rhythm. Replace artificial only-colour/height choices with meaningful musical alternatives; duration organisation source also supported by music-education glossary.
5|Chord is notes together; solo player,successive melody,lyrics differ. Do not force exactly three because dyads/power chords complicate categorical counts. Musical not geometric chord sense inspected.
6|Arpeggio sounds chord notes successively. All at once is unarpeggiated; drummer-only/silence not definition. It need not always be fast, so no arbitrary speed restriction included.
7|Pitch high/low differs from volume,duration,source identity. Replace financial/practice/audience distractors. Cambridge sound sense inspected among many pitch senses.
8|Dynamics are loud/soft changes, unlike pitch patterns,tempo or bar count. Replace title/ownership/programme distractors; Cambridge musical dynamics definition directly supports.
9|Timbre distinguishes tone quality. Tempo speed,metre beat grouping,duration length do not answer distinctive tone colour. British metre spelling correct; no acoustic-frequency claim oversimplified.
10|Standard stave five lines, four spaces. Three/four/six lines wrong; standard excludes specialised one-line percussion/tab staves. Source explicitly states five lines and four spaces.
11|Clef maps pitches to staff positions. Time signature beat count,lyrics,note-value duration are other notation elements. More relevant wrong options added; no claim clef alone specifies every chromatic alteration.
12|Sharp normally raises written pitch a semitone. Lowering is flat; double duration and silence not pitch alteration. Musical noun sign sense inspected, not conversational sharpness or tuning sharp.
13|Flat lowers semitone. Raise opposite, doubled length and louder concern different dimensions. Musical sign sense inspected among many adjective/noun meanings.
14|Natural cancels applicable sharp/flat. Louder,extra beat,double length wrong. Affected-note phrase avoids claiming cancellation of the entire key signature; replace new-instrument distractor.
15|Forte means loud dynamics. Quiet opposite; slow tempo,detached articulation. Cambridge musical direction inspected, excluding personal strong point/fencing meanings.
16|Piano as score direction means quietly. Loudly opposite,quickly tempo,no pause articulation/continuity. Explicit instruction scope distinguishes instrument piano.
17|Crescendo asks gradual louder, not quieter/faster/slower. Rephrase from what happens during to the instruction's meaning, because musicians may independently accelerate too. No crescendo/accelerando conflation.
18|Diminuendo means gradual quieter. Louder opposite,immediate double speed and stop reading wrong. Gradual vs immediate distinction and correct Italian spelling checked.
19|Staccato short/detached. Smooth joined legato,maximum loudness dynamics,double slow tempo do not define it. Usually accommodates instrument/style variation without claiming precise fixed shortening.
20|Legato smooth connected, not detached,loud,fast. Source musical sense direct. No demand that notes overlap by a specified duration.
21|Adagio slow. Very quick,loud,a cappella are different. Cambridge adverb/adjective musical senses agree; no rigid metronome range invented.
22|Andante conventional walking/fairly slow pace. Presto,prestissimo,vivace faster. Cambridge says fairly slow; walking-pace common meaning fits and no exact BPM asserted.
23|Oxford explicitly gives musical presto very quickly. Very slow/quiet/without singing wrong. Replace Cambridge page that only supplied magical-exclamation meaning; source relevance actually corrected.
24|Ritardando gradual slower. Faster opposite; highest notes and wordless singing do not define it. No confusion with ritornello/repeat; spelling checked.
25|Accelerando gradual faster. Slower opposite,instant stop and abandoning steady beat wrong. Tempo can accelerate while pulse stays orderly; source explicitly increases speed.
26|Fermata lengthens note/rest beyond usual value. Repeating whole piece,instrument change,all quiet wrong. Includes a pause/rest as well as sounding note to avoid overrestriction.
27|Fortissimo very loud; very quiet/slow/short wrong dimensions. No claim absolute loudest possible sound; expressive dynamic relative to context.
28|Mezzo-forte moderately loud. Maximum loudness,silence,very slow not equivalent. Hyphenated Italian loan term and adverbial meaning checked.
29|Da capo return to beginning. Last note,previous bar only,key change different instructions. Replace nonsensical faster-instrument wording; return does not necessarily require playing entire piece to its end.
30|Cambridge quarter-note page explicitly labels UK crotchet. Eighth,half,whole other values. Link American headword so synonym appears directly; no universal one-beat assertion.
31|Cambridge eighth-note page explicitly labels UK quaver. Quarter,half,whole wrong. Musical noun sense, not trembling voice, inspected.
32|Cambridge half-note page explicitly labels UK minim. Quarter,eighth,whole wrong. Two crotchets relation also confirms; avoid implying every time signature gives two beats.
33|Cambridge whole-note page labels UK semibreve. Half,quarter,eighth shorter values. British/American terminology stated to avoid regional disagreement.
34|Rest is notated silence. Loud note,singer change,new key are different instructions. Musical rest sense inspected beyond relaxation/legal/verb meanings.
35|Bar/measure are regional synonyms for metric grouping. Verse lyrics section,chord simultaneous notes,octave pitch distance differ. Musical sense inspected beyond drinking venue/physical bar; no claim every bar always same actual duration under tempo changes.
36|Time signature indicates beat grouping/metre. Key sharps/flats,dynamics,instrument assignment other notation. Replace calendar/audience/intermission distractors; not necessarily a mathematical fraction despite stacked numerals.
37|Key signature supplies usual sharps/flats. Beat count,tempo,movement count not key. Normally-used phrase permits accidentals within piece and changes later.
38|Lyrics are song words. Melody without words,chord progression,dynamics not lyrics. Replace drumstick/ticket choices with meaningful musical concepts; apostrophe song's correct.
39|Score written music notation. Metronome,lyrics alone,tuning method not a score. Inspected written-music sense rather than sport score; full score can show all parts, but term also includes reduced scores.
40|Tuning adjusts intended pitches. Doubling note durations,altering time signature,removing bars changes score rather than tuning. Replace cosmetic/destructive distractors; tuning noun definition plus established tune verb meaning clear.
41|Original metronome question repeated Family Trivia's regular-beat fact. Replace with capo, whose Cambridge definition says clamp across guitar strings makes them sound higher. Amplifier,metronome,bow functions differ; source inspected before approval.
42|Interval difference between pitches. Beat speed,chord loudness,ensemble size other quantities. Musical sense inspected beyond intermission/time interval; exactly one pitch-distance option.
43|Yamaha explicitly says piano sound from hammers striking strings. Organ,accordion and harpsichord not hammer-struck-string instruments. Replace Cambridge definition that only described keys; question says usually so digital pianos not falsely excluded as pianos.
44|Cambridge standard guitar typically six strings. Four,five,eight are other/variant instruments. Standard/usually wording accommodates seven/twelve-string and bass guitars without making their counts competing answers.
45|Violin normally bowed. Trumpet/flute blown,cymbals struck. Bowing usual not exclusive because violin can be pizzicato; no other bowed instrument offered.
46|Flute blown across edge of mouth hole. Oboe/bassoon double reed,clarinet single. Orchestral qualifier targets transverse flute rather than broad duct-flute classification; source describes horizontal hole-blowing instrument.
47|Trombone long movable slide. Trumpet,tuba,horn normally valves; slide trumpet/valve trombone variants do not change familiar identification because especially-known qualifier used.
48|Philharmonia tuba guide describes deep bass role and orchestral register. It is normally lower than trumpet,horn,cornet among these options. No claim all possible brass instruments or extreme player ranges fit a rigid boundary.
49|Yamaha explicitly explains brass-made saxophone woodwind classification by single reed. Brass,strings,unpitched percussion wrong. Remove orchestral-family wording because saxophone is not a routine symphony-orchestra member.
50|Clarinet single reed. Oboe/bassoon double;flute no reed. Cambridge directly supports each mechanism through relevant entries; four mutually distinct options in this question.
51|Oboe double reed. Clarinet/sax single;flute none. Bassoon deliberately not offered, which would otherwise be a second correct double-reed answer.
52|Cambridge cello rests between legs while seated, played with bow. Violin/viola chin/shoulder;trumpet not bowed. Normally avoids claiming cellists can never stand or use unusual posture.
53|Double bass largest/lowest conventional bowed orchestra strings among cello/viola/violin. Source calls it very large and lowest line; no octobass option offered. Normally qualifier excludes unusual experimental orchestra instrumentation.
54|Philharmonia explicitly says viola larger than violin and lowest note fifth lower. Smaller/higher,no strings,blowing wrong. Replace size-only dictionary reference with source supporting both halves of correct answer.
55|Harp large frame with many finger-plucked strings. Oboe,trombone,snare drum do not fit. Triangular shape not unnecessarily made universal; correct answer clearly identified by mechanism.
56|Accordion bellows plus keys/buttons. Violin,trumpet,triangle different. Commonly played wording includes button accordions as well as piano-key models; Cambridge folding/bellows mechanism inspected.
57|Harmonica blow/draw through mouth holes. Tuba,harp,gong do not combine small mouth-held reed chambers and both air directions. No claim breathing technique applies to every extended performance method.
58|Standard ukulele four strings. Six/seven/eight variants exist but not ordinary standard model; qualifiers retained. Cambridge four-string definition matches.
59|Bagpipes air reservoir bag feeding pipes. Trombone,clarinet,harmonica lack bag. Different from previous bagpipe recording-identification question; no claim all bagpipes mouth-blown because bellows exist.
60|Traditional xylophone bars wood. Glass,stone,steel differ; modern synthetic bars acknowledged by traditional qualifier. Does not confuse all tuned percussion with xylophone.
61|Orchestral glockenspiel metal bars. Wood xylophone,leather/paper not bar material. Orchestral adjective avoids broader German term for carillons; source explicit metal bars.
62|Cymbals struck/clashed metal plates. Pipes,strings,bellows other families. Cambridge supports stick-hit and paired clash, so not restricted to only one method.
63|Snare wires vibrate against lower head. Plucked single string,reed,keyboard metal bars not snare mechanism. Characteristic rattling rather than all possible drum sounds queried.
64|Timpani are kettledrums. Maracas,castanets,cymbals different percussion. Source explicit synonym; both singular/plural agreement appropriate to timpani.
65|Maracas hand-shaken rattles. Bowed strings,valved brass,bellows keyboard wrong. Source describes filled hollow container/handle; not restricted to one traditional material.
66|Castanets sounded by clicking paired pieces. Bowing,blowing,piano pedals wrong. Shells here means shell-shaped pieces, often wood, not mandatory actual seashells; source wooden pieces knocked together supports.
67|Triangle bent metal rod with three sides struck with beater. Gong,tambourine,maraca different forms. Open corner does not stop instrument being triangular; wording does not require closed geometric polygon.
68|Gong suspended metal disc struck with mallet. Clarinet,violin,accordion not percussion discs. Cymbal deliberately not offered because suspended cymbals can also be mallet-struck.
69|Tambourine frame carries metal jingles. Tuba,bassoon,harp do not. Do not require a drumhead because headless tambourines exist; Cambridge frame/disc definition supports.
70|Oxford Bate Collection describes plectra plucking strings when keys pressed. Bow,air,spinning disc not mechanism. Replace Cambridge entry that did not explicitly explain plucking; contrasting piano mechanism verified separately with Yamaha.
71|Soprano highest in soprano-alto-tenor-bass four-part choir. Other parts lower. Expand SATB to words for accessibility; no claim every high voice is female or every choir uses same divisions.
72|Bass lowest among the named four standard parts. Tenor,alto,soprano higher. Expand acronym as above; source bass lowest range explicit.
73|Tenor conventionally above baritone/bass in usual male classical types. Bass/baritone lower,contrabass lowest. Usual scope excludes rare male sopranos/countertenors not offered.
74|Baritone lies between tenor/bass, directly in Cambridge. Soprano/contralto/treble not standard intermediate adult male type. No absolute frequency boundaries or gender restrictions imposed on all singers.
75|Falsetto high/light production relative to ordinary modal voice. Wordless,loudest,always-below-range do not define it. Improve answer to high/light rather than vague unusually high; not restricted to men despite older dictionary phrasing.
76|A cappella commonly unaccompanied singing. Solo drum,double speed,Latin-only wrong. Common-usage qualifier handles historical chapel-style usage and contemporary vocal percussion, which remains vocal.
77|Solo features one person even with accompaniment. Two/three/four not soloists count. Featured wording essential so backing orchestra is not counted as disproving one.
78|Duet features two performers. One/three/four wrong. Tighten to featured performers so accompaniment does not create apparent total-count ambiguity; source two-person musical work/ensemble inspected.
79|Original trio-three question duplicated General Knowledge. Replace with pizzicato, explicitly finger-plucking rather than bowing in Cambridge. Smooth bow,loudness,slowing are different techniques/instructions.
80|Quartet ensemble four performers. Three/five/six different sizes. Counting performers not movements; source ensemble sense inspected.
81|Quintet five. Four/six/seven other ensemble counts. Musical ensemble sense, not basketball or generic set, chosen from dictionary.
82|Sextet six. Four/five/seven other counts. Musical sense not hockey team; clear performer-count wording.
83|Choral choir is singers, not brass section,string quartet,drum group. Add choral context to distinguish instrumental choir metaphor; dictionary also has architectural choir meaning, not intended.
84|Conductor directs performance. Does not by definition compose all works,take all solos or play all percussion. More relevant musical distractors replace repairs/tickets; primarily distinguishes secondary roles a conductor may also hold.
85|Cambridge explicitly allows same pitch or one/more octaves apart for unison. Broaden answer to include octave doubling; different tunes,alternating notes,stopping times do not define it. Important correction to overly strict initial answer.
86|Lullaby soothes child to sleep. Battle signal,dance acceleration,sports announcement not usual purpose. Traditionally intended avoids asserting no adult can enjoy or sing one for other reasons.
87|Opera staged story mainly sung, with music. Mime,stand-up,silent cinema do not primarily tell story through sung drama. Primarily allows operas with spoken dialogue; instrumental accompaniment customary rather than absolute all works.
88|Cambridge says reggae from Jamaica. Sweden,Japan,Greece not origin. Strong lexical overlap with tiramisu-origin question is only template similarity, not same fact.
89|Cambridge identifies Spanish flamenco. Norway,Canada,Thailand wrong origin association. Country rather than strict universal performance location, acknowledging global practice.
90|Musical gospel definition explicitly Christian religious music. Greek epics,military calls,jousting not genre tradition. Inspected musical sense beyond Gospel books/absolute-truth idiom.
91|Rap rhythmic spoken/chanted delivery over beat. Gregorian chant normally sung/non-metric; wordless lullaby lacks words;solo flute not spoken. Especially features qualifies mixed rap/singing tracks rather than banning melody entirely.
92|Traditional waltz triple metre, three beats per bar. Two/four/five wrong for standard waltz. No claim every dance that modern performers call waltz must use a single tempo or fixed number of bars.
93|March strong regular beat for stepping. Lullaby,cadenza,recitative not designed for coordinated marching. Musical noun sense inspected beyond month/protest/verb; correct article choices.
94|Overture opening instrumental music. Final applause,cast list,after-show speech not it. Opera/musical scope excludes independent concert overtures, which source also mentions.
95|Original encore repeated Stage & Musicals' fact. Replace with standard string quartet composition: two violins,viola,cello. Berlin Philharmonic explicitly contrasts its added double bass quintet; double bass,harp,guitar not standard fourth quartet instrument.
96|Original audition repeated Stage & Musicals. Replace with vibrato's slight repeated wavering. Abrupt silence,backwards second melody,drumbeat wrong. Do not overrestrict dictionary's shaking to only pitch or only one instrumental mechanism.
97|Improvising creates musical material during performance. Only exact copying/fixed reproduction do not; audience absence irrelevant. Does not claim improvisation cannot use planned chord progressions or other structure.
98|Accompaniment supports main melody/performer. Audience exit,ticket prices,final silence not musical support. Relevant music sense inspected beyond food accompaniment/general simultaneous events.
99|In typical verse-chorus form, chorus repeats stable words/tune;verses change. Spoken intro only and applause do not. Typical qualifier allows songs with evolving choruses and exceptions; avoid claiming every chorus word forever identical.
100|Original rehearsal exactly duplicated General Knowledge. Replace with transpose, whose Cambridge musical sense explicitly changes key. Reversed lyrics,more performers,rests turned loud notes do not define transposition. No ordinary exchanging-position sense used.
'''
rows=[]
for line in notes.strip().splitlines():
 n,note=line.split('|',1);n=int(n)
 d={'row':n,'action':'edit' if n in edits else 'keep','prompt':draft[n-1]['prompt'],'note':note,
 'sourceReview':'Individual author second-pass review of meaning, all four options, sole correct answer, grammar, music relevance and the relevant musical dictionary sense or named instrument-maker/orchestra/museum reference. Not independent review.'}
 if n in edits:d['recommendedChanges']=edits[n]
 rows.append(d)
assert [x['row'] for x in rows]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'reviewer':'root (author second editorial pass)','independent':False,
 'sourceAccessNote':'Every candidate and all options inspected individually. Five repeated concepts (metronome,trio,encore,audition,rehearsal) replaced before publication with verified capo,pizzicato,string-quartet composition,vibrato,transposition facts. Polysemous musical senses inspected explicitly, including sharp/flat/natural/rest/bar/score/interval; presto reference replaced because Cambridge only gave the exclamation. American note-name aliases inspected in full reference text. Piano/saxophone/viola/harpsichord mechanisms checked with Yamaha, Philharmonia and Oxford Bate Collection rather than assuming a short dictionary definition proved them. Revised distractors to relevant music concepts, expanded SATB, clarified featured duet performers and included octave unison. Reference extracts remain private; these are author editorial decisions, not independent or automated approval.',
 'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('100 explicit author final checks recorded; apply edits before publication.')
