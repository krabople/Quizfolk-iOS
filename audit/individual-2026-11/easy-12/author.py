"""Accessible music foundations; final individual review is required."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
rows='''1|tempo|In music, what does tempo describe?|How fast or slowly the music moves|How high the notes are|How many singers are present|Which language the lyrics use|Tempo is musical speed; pitch, ensemble size and lyric language are distinct.
2|melody|What is a melody?|A sequence of notes forming a tune|The loudness of a performance|A printed list of performers|A type of drumstick|Melody is a tune or succession of notes, not volume, programme or equipment.
3|harmony|In music, harmony especially concerns what?|Notes sounding together|The price of a concert ticket|The speed of the words alone|The number of pages in a score|Harmony concerns simultaneous pitches and their relationships; other options do not define it.
4|rhythm|What does musical rhythm concern?|The pattern of sounds and silences in time|Only the height of a singer|Only the colour of an instrument|Only the language of the lyrics|Rhythm concerns timing and duration patterns, not the alternatives.
5|chord|What is a musical chord?|A group of notes sounded together|One player performing alone|A pause between concerts|The words of a song|Chord is simultaneous notes; solo, interval between events and lyrics differ.
6|arpeggio|How are a chord's notes played in an arpeggio?|One after another|All at exactly the same time|Only by a drummer|Without making any sound|Arpeggiation sounds chord notes successively rather than simultaneously.
7|pitch|What does pitch describe about a musical note?|How high or low it sounds|How much the instrument costs|How long the musician has practised|How many people hear it|Pitch is perceived highness/lowness; cost, experience and audience size are unrelated.
8|dynamics|In music, what do dynamics concern?|Loudness and changes in loudness|The spelling of song titles|The number of instruments owned|The order of names in a programme|Dynamics concern volume levels and changes, not the other information.
9|timbre|Which musical term describes a sound's distinctive tone quality?|Timbre|Tempo|Metre|Duration|Timbre is the quality distinguishing sources at same pitch/loudness; other terms concern time/speed.
10|stave|How many lines are in a standard musical stave?|Five|Three|Four|Six|The ordinary Western staff/stave has five lines; spaces are not counted as lines.
11|clef|What does a clef help identify on a musical stave?|The pitches represented by its lines and spaces|The cost of the sheet music|The composer's nationality|The length of a concert|A clef assigns pitch meaning to the staff positions.
12|sharp|In standard Western notation, what does a sharp sign normally do to a note?|Raises it by a semitone|Lowers it by a semitone|Makes it twice as long|Makes it silent|A sharp raises pitch one semitone; other options confuse flat, rhythm and rest.
13|flat|In standard Western notation, what does a flat sign normally do to a note?|Lowers it by a semitone|Raises it by a semitone|Doubles its length|Makes it louder|A flat lowers pitch one semitone, not duration or volume.
14|natural|In music notation, what does a natural sign do?|Cancels a sharp or flat for the affected note|Makes every note louder|Adds an extra beat to a bar|Requires a new instrument|Natural returns note to unaltered form, cancelling accidental/key-signature alteration for it.
15|forte|What does the musical instruction forte mean?|Loud|Quiet|Slow|Detached|Forte indicates loud dynamics; other terms concern soft volume, speed and articulation.
16|piano|What does piano mean as an instruction in a musical score?|Quietly|Loudly|Quickly|With no pause|Piano is soft/quiet as dynamic instruction, distinct from the instrument with the same name.
17|crescendo|What happens during a crescendo?|The music gradually gets louder|The music gradually gets quieter|The music stops instantly|The singer changes language|Crescendo is increasing loudness, not necessarily increasing speed.
18|diminuendo|What does diminuendo ask musicians to do?|Gradually get quieter|Gradually get louder|Immediately double the speed|Stop reading the score|Diminuendo is decreasing volume; other options are not the instruction.
19|staccato|How are notes marked staccato usually played?|Short and detached|Smoothly joined together|As loudly as possible|Always twice as slowly|Staccato separates notes; legato joins them and neither volume nor fixed tempo follows.
20|legato|What does legato mean in music?|Smoothly joined|Short and detached|Very loud|Very fast|Legato is connected articulation, not detachedness, loudness or speed.
21|adagio|What does adagio generally mean as a tempo instruction?|Slowly|Very quickly|Loudly|Without instruments|Adagio is slow tempo; alternatives confuse dynamics or texture.
22|andante|Which tempo marking is commonly described as a walking pace?|Andante|Presto|Prestissimo|Vivace|Andante is walking/moderate pace; the others are faster markings.
23|presto|What does presto mean as a tempo instruction?|Very fast|Very slow|Very quiet|Without singing|Presto is very fast; other options describe another speed or other musical property.
24|ritardando|What does ritardando ask a performer to do?|Gradually slow down|Gradually speed up|Play only the highest notes|Sing without words|Ritardando is a gradual decrease in tempo; the alternatives differ.
25|accelerando|What does accelerando ask musicians to do?|Gradually speed up|Gradually slow down|Immediately stop|Play without a steady beat|Accelerando increases tempo, not a requirement to abandon pulse.
26|fermata|What does a fermata usually tell a musician to do?|Hold a note or pause longer than its written value|Play the whole piece twice|Change instruments|Play every note quietly|Fermata extends a note/rest beyond ordinary duration; other options unrelated.
27|fortissimo|What does fortissimo mean?|Very loud|Very quiet|Very slow|Very short|Fortissimo is very loud dynamics, not speed or duration.
28|mezzo-forte|What does mezzo-forte mean?|Moderately loud|As loud as possible|Completely silent|Extremely slow|Mezzo-forte is moderately loud, not maximum loudness or another property.
29|da-capo|What does da capo tell a musician to do?|Return to the beginning|Skip to the last note|Change to a faster instrument|Stop immediately|Da capo directs return to start; other actions not its meaning.
30|crotchet|In British musical terminology, what is the American name for a crotchet?|Quarter note|Eighth note|Half note|Whole note|Crotchet is quarter note; duration in beats depends on metre, not asserted here.
31|quaver|In British musical terminology, what is the American name for a quaver?|Eighth note|Quarter note|Half note|Whole note|Quaver is eighth note; other names correspond to different written values.
32|minim|In British musical terminology, what is the American name for a minim?|Half note|Quarter note|Eighth note|Whole note|Minim is half note; alternatives are different notation values.
33|semibreve|In British musical terminology, what is the American name for a semibreve?|Whole note|Half note|Quarter note|Eighth note|Semibreve is whole note; alternatives are shorter written values.
34|rest|What does a rest indicate in a musical score?|A period of silence|A louder note|A change of singer|The start of a new key|Rest is notated silence for its duration, not the other instructions.
35|bar|In musical notation, what is a bar also called in American English?|A measure|A verse|A chord|An octave|Bar and measure name the grouping separated by barlines; other terms differ.
36|time-signature|What does a time signature primarily indicate?|How beats are grouped into bars|The year a song was written|The number of musicians onstage|The length of the interval|Time signature indicates metre/beat grouping, not calendar date, ensemble size or intermission.
37|key-signature|What does a key signature show at the start of a stave?|The sharps or flats normally used in the music|The names of the singers|The price of the score|The number of movements|Key signature gives default alterations for pitches, not the other information.
38|lyrics|What are a song's lyrics?|Its words|Its drumsticks|Its chord changes alone|Its ticket sales|Lyrics are the words of a song, not instruments, harmony alone or business figures.
39|score|In music, what is a score?|Written notation showing the music to be performed|A count of audience members|A singer's stage name|The price of a recording|Musical score is written representation; sporting/numerical senses excluded by music context.
40|tuning|What does tuning an instrument involve?|Adjusting it to produce the intended pitches|Making its case heavier|Changing its colour|Removing all its strings|Tuning adjusts pitch; alternatives do not define the process.
41|metronome|What is a metronome used for?|Providing a steady beat for practice|Making an instrument louder electrically|Recording a singer's voice|Turning sheet-music pages|Metronome supplies regular pulse at chosen tempo; other devices have other uses.
42|interval|In music, what is an interval between two notes?|The distance between their pitches|The number of words in their title|The number of instruments playing them|The price difference between two tickets|Pitch interval is musical distance, not concert intermission or other counts.
43|piano|Which keyboard instrument usually makes sound when hammers strike strings?|Piano|Organ|Accordion|Harpsichord|Piano has hammer-struck strings; organ pipes/reeds, accordion reeds and harpsichord plucked strings differ.
44|guitar|How many strings does a standard guitar usually have?|Six|Four|Five|Eight|Ordinary standard guitar six strings, unlike variants acknowledged by usually.
45|violin|Which of these instruments is normally played with a bow drawn across strings?|Violin|Trumpet|Flute|Cymbals|Violin is bowed string instrument; alternatives are brass,woodwind,percussion.
46|flute|Which of these orchestral instruments is normally played by blowing across an opening rather than through a reed?|Flute|Oboe|Clarinet|Bassoon|Flute uses edge-tone opening, unlike reeds of the alternatives.
47|trombone|Which brass instrument is especially known for its long movable slide?|Trombone|Trumpet|Tuba|French horn|Slide trombone's movable slide familiar; others normally use valves.
48|tuba|Which of these is normally the lowest-pitched orchestral brass instrument?|Tuba|Trumpet|French horn|Cornet|Tuba normally lowest among these brass options; not an assertion about every unusual instrument variant.
49|saxophone|Despite usually being made of brass, the saxophone belongs to which orchestral family?|Woodwind|Brass|Strings|Unpitched percussion|Single-reed saxophone is classified woodwind despite material, unlike brass instruments' lip vibration.
50|clarinet|Which of these woodwind instruments uses a single reed?|Clarinet|Oboe|Bassoon|Flute|Clarinet single reed; oboe/bassoon double reeds and flute no reed.
51|oboe|Which of these woodwind instruments uses a double reed?|Oboe|Clarinet|Saxophone|Flute|Oboe double reed; clarinet/saxophone single and flute reedless.
52|cello|Which bowed string instrument is normally played seated, held between the player's knees?|Cello|Violin|Viola|Trumpet|Cello held between knees; violin/viola under chin, trumpet brass not bowed.
53|double-bass|Which is normally the largest and lowest-pitched instrument in an orchestra's bowed string section?|Double bass|Cello|Viola|Violin|Double bass has largest/lowest conventional orchestral string role among options.
54|viola|Compared with a violin, a viola is usually what?|Larger and lower-pitched|Smaller and higher-pitched|Made without strings|Played only by blowing|Viola slightly larger and tuned lower; alternatives false.
55|harp|Which instrument is played by plucking many strings stretched across a large frame?|Harp|Oboe|Trombone|Snare drum|Harp has frame and plucked strings; other instruments lack such strings.
56|accordion|Which instrument uses bellows and is commonly played with keys or buttons?|Accordion|Violin|Trumpet|Triangle|Accordion bellows feed reeds; alternatives not bellows/keyboard instruments.
57|harmonica|Which small instrument is played by blowing and drawing air through holes held to the mouth?|Harmonica|Tuba|Harp|Gong|Harmonica uses blow/draw reed chambers; other options do not fit.
58|ukulele|How many strings does a standard ukulele normally have?|Four|Six|Seven|Eight|Standard ukulele has four strings, with variants excluded by normal/standard wording.
59|bagpipes|Which instrument uses a bag of air to supply several pipes?|Bagpipes|Trombone|Clarinet|Harmonica|Bagpipes use reservoir feeding pipes; alternatives lack bag.
60|xylophone|What are the bars of a traditional xylophone made from?|Wood|Glass|Stone|Steel|Xylophone has wooden bars; metal-bar related instruments differ.
61|glockenspiel|What are the bars of an orchestral glockenspiel made from?|Metal|Wood|Leather|Paper|Glockenspiel uses metal bars rather than xylophone wood; alternatives wrong.
62|cymbal|What are cymbals?|Metal plates struck or clashed to make sound|Wooden pipes with finger holes|Strings bowed with horsehair|Bellows filled with air|Cymbals are percussion plates; alternatives describe other families.
63|snare-drum|What produces a snare drum's characteristic rattling sound?|Wires stretched against its lower drumhead|A single plucked string above it|Air blown through a reed|A keyboard striking metal bars|Snares are wires touching resonant head; other mechanisms differ.
64|timpani|What are timpani also commonly called?|Kettledrums|Maracas|Castanets|Cymbals|Timpani are tunable kettledrums; alternatives are different percussion types.
65|maraca|What kind of instruments are maracas?|Rattles shaken by hand|Bowed string instruments|Brass instruments with valves|Keyboard instruments with bellows|Maracas are hand-held shaken rattles; other instrument families differ.
66|castanets|How are castanets typically sounded?|By clicking small shells or pieces together|By bowing strings|By blowing across a mouth hole|By pressing piano pedals|Castanets click paired concave pieces, traditionally wood; alternatives not their mechanism.
67|triangle|Which percussion instrument is a metal rod bent into a three-sided shape and struck with a beater?|Triangle|Gong|Tambourine|Maraca|Triangle has triangular bent rod; other instruments differ.
68|gong|Which percussion instrument is typically a large metal disc suspended and struck with a mallet?|Gong|Clarinet|Violin|Accordion|Gong is suspended struck metal disc; other options different families.
69|tambourine|Which instrument has a hand-held frame with small metal jingles?|Tambourine|Tuba|Bassoon|Harp|Tambourine frame carries jingles, often also membrane; not always drumhead required.
70|harpsichord|Unlike a piano's hammers, what usually makes a harpsichord's strings sound?|A plucking mechanism|A player blowing across them|A bow moving along them|A spinning metal disc|Harpsichord strings are plucked by jacks/quills, not struck by hammers.
71|soprano|In a standard SATB choir, which voice part is the highest?|Soprano|Alto|Tenor|Bass|SATB ordered high to low soprano,alto,tenor,bass; gender not imposed.
72|bass|In a standard SATB choir, which voice part is the lowest?|Bass|Tenor|Alto|Soprano|Bass is lowest conventional part in SATB arrangement.
73|tenor|Among the usual adult male classical voice types, which is generally higher than baritone and bass?|Tenor|Bass|Baritone|Contrabass|Tenor is the higher conventional male range among options; exceptional voices excluded by usual.
74|baritone|Which adult male classical voice type normally lies between tenor and bass?|Baritone|Soprano|Contralto|Treble|Baritone intermediate conventional male voice; other terms concern different ranges/parts.
75|falsetto|What does falsetto describe in singing?|An unusually high vocal register|Singing with no lyrics at all|Singing as loudly as possible|Always singing below one's normal range|Falsetto is high light register relative to modal voice; not an indication of loudness or wordlessness.
76|a-cappella|What does a cappella mean in common musical usage?|Singing without instrumental accompaniment|Playing a solo drum|Playing twice as fast|Singing only in Latin|A cappella is unaccompanied singing; no language restriction.
77|solo|How many performers are featured in a solo?|One|Two|Three|Four|Solo is one featured performer, even when accompanied; not a claim whole ensemble absent.
78|duet|How many performers are in a duet?|Two|One|Three|Four|Duet involves two performers or parts; options are other counts.
79|trio|How many musicians make up a trio?|Three|Two|Four|Five|Trio ensemble has three musicians; not questioning an instrumental work's contrasting trio section.
80|quartet|How many performers make up a quartet?|Four|Three|Five|Six|Quartet ensemble has four performers; distinct from score pages/movements.
81|quintet|How many performers make up a quintet?|Five|Four|Six|Seven|Quintet has five performers; alternatives wrong counts.
82|sextet|How many performers make up a sextet?|Six|Four|Five|Seven|Sextet has six performers; root sext means six.
83|choir|What is a choir?|A group of singers|A type of brass instrument|A rhythm played only by drums|A single violin string|Choir is vocal ensemble in intended sense; no claim only religious choirs exist.
84|conductor|What does an orchestral conductor primarily do?|Directs the performers during the music|Repairs all the instruments while they play|Sells tickets during each piece|Writes every piece performed|Conductor coordinates musical performance; other duties do not define the role.
85|unison|What does it mean when musicians play the same melody in unison?|They play it together at the same pitch|They all play different tunes|They alternate one note each|They all stop at different times|Strict unison means same pitches simultaneously; octave unison sometimes colloquial, intended standard definition.
86|lullaby|What is a lullaby traditionally intended to do?|Soothe a child to sleep|Signal the start of a battle|Make dancers speed up|Announce a sports result|Lullaby is soothing sleep song, not the other purposes.
87|opera|Which art form tells a staged story primarily through singing with instrumental accompaniment?|Opera|Mime|Stand-up comedy|Silent cinema|Opera primarily sung drama, unlike alternatives; some works have spoken dialogue acknowledged by primarily.
88|reggae|Reggae originated in which country?|Jamaica|Sweden|Japan|Greece|Reggae developed in Jamaica; alternatives not origin.
89|flamenco|Flamenco music and dance are especially associated with which country?|Spain|Norway|Canada|Thailand|Flamenco chiefly Andalusian/Spanish tradition; country scope clear.
90|gospel|Gospel music is especially associated with which tradition?|Christian worship|Ancient Greek epic recitation|Traditional military bugle calls|Medieval court jousting|Gospel genre has Christian religious content and worship association; alternatives not genre definition.
91|rap|Which style especially features rhythmic spoken or chanted words over a beat?|Rap|Gregorian chant|A wordless lullaby|A solo flute piece|Rap is rhythmic spoken delivery over beat; alternatives do not normally match.
92|waltz|A traditional waltz is usually counted in groups of how many beats?|Three|Two|Four|Five|Waltz triple metre, normally3/4; other counts not standard traditional waltz.
93|march|Which type of music is traditionally written with a strong regular beat for people to walk in step?|A march|A lullaby|A free cadenza|A recitative|March music supports regular stepping; other genres/styles differ.
94|overture|What is an overture in an opera or musical?|An opening instrumental piece|The audience's final applause|The printed cast list|A solo speech after the show|Overture precedes the dramatic work; other options not musical introduction.
95|encore|What is an encore at a concert?|An extra performance after the planned programme|The first rehearsal|A tuning tool|A form of ticket refund|Encore is an additional performance typically after applause; other uses wrong.
96|audition|What is an audition for a musician?|A performance to seek selection for a role or place|A break between two halves of a concert|A payment for lost sheet music|A type of instrument case|Audition tests/selects performer, not intermission,fee or case.
97|improvise|What does improvising in music involve?|Creating music during the performance|Only copying a recording exactly|Only playing from a fully fixed score|Always performing without an audience|Improvisation creates spontaneously rather than reproducing every detail fixed in advance.
98|accompaniment|What is musical accompaniment?|Music supporting a main melody or performer|The audience leaving the hall|A list of ticket prices|The silence after the final note|Accompaniment supports lead part; alternatives are not that musical function.
99|chorus|In a typical verse-chorus song, which section returns with the same main words and tune?|The chorus|The changing verses|The spoken introduction only|The final applause|Chorus/refrain repeats stable main material while verses change; typical-form scope avoids universal rule.
100|rehearsal|What is a rehearsal?|A practice session before a performance|A request for extra applause|A type of musical clef|The sale of a finished recording|Rehearsal is preparation/practice, not encore request,notation or sales.
'''
if __name__=='__main__':
 q=[]
 for line in rows.strip().splitlines():
  n,key,prompt,correct,*tail=line.split('|');assert len(tail)==4 and int(n)==len(q)+1
  q.append({'draftID':f'easy-12-{int(n):03d}','categoryID':'12','difficulty':'easy','prompt':prompt,'answers':[correct,*tail[:3]],'correctIndex':0,'rationale':tail[3],
    'sourceURL':'https://dictionary.cambridge.org/dictionary/english/'+key,'reviewStatus':'draft_awaiting_author_final_check'})
 assert len(q)==100
 (HERE/'draft.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('100 unapproved music-foundation candidates')
