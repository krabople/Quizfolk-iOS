"""Explicit individual author second-pass judgments; not independent review."""
import json,pathlib,urllib.parse
HERE=pathlib.Path(__file__).parent
draft=json.loads((HERE/'draft.json').read_text(encoding='utf8'))
def bible(s):return 'https://www.biblegateway.com/passage/?'+urllib.parse.urlencode({'search':s,'version':'KJV'})
deities='https://www.hinduamerican.org/wp-content/uploads/2019/12/WhoHindusWorship.pdf'
buddhist='https://www.edu.gov.mb.ca/k12/docs/support/world_religions/buddhism/texts-writings.pdf'
edits={
6:{'prompt':'In a church, what is the collective term for people ordained for religious duties?'},
13:{'answers':['Someone beginning a period of training','The longest-serving member','A visiting bishop','The owner of the building']},
31:{'sourceURL':bible('Genesis 6:13-22')},
33:{'sourceURL':bible('1 Samuel 17:4-50')},
34:{'sourceURL':bible('Exodus 3:4-10')},
37:{'answers':['A bush burning without being consumed','A river turning to blood','A staff turning into a snake','A sea dividing into two parts']},
59:{'sourceURL':'https://www.chabad.org/library/article_cdo/aid/177886/jewish/What-Is-Yom-Kippur.htm'},
71:{'prompt':'Which Hindu deity is commonly shown with a third eye in the middle of his forehead?','answers':['Shiva','Ganesha','Brahma','Hanuman'],'sourceURL':deities,'rationale':'Shiva is characteristically shown with a third eye; the other deities do not have this identifying attribute in their usual depictions.'},
75:{'prompt':'Which Hindu deity is associated with the Sun?','answers':['Surya','Indra','Agni','Varuna'],'sourceURL':deities,'rationale':'Surya is the Sun deity; Indra is associated with thunder and rain, Agni with fire and Varuna with waters and cosmic order.'},
78:{'prompt':'Which Hindu goddess is depicted defeating the buffalo demon Mahisha?','sourceURL':'https://www.metmuseum.org/art/collection/search/38273'},
81:{'answers':['A sacred Buddhist monument','A type of prayer shawl','A religious wind instrument','A special festival food']},
84:{'prompt':'Which practice involves training attention through focused awareness?','answers':['Meditation','Fasting','Pilgrimage','Ordination']},
86:{'sourceURL':buddhist},
88:{'sourceURL':buddhist},
92:{'sourceURL':'https://www.islamic-relief.org.uk/giving/islamic-giving/ramadan/memorable-ways-to-celebrate-eid-with-your-family/'},
94:{'answers':['Calling people to prayer','Issuing religious legal rulings','Leading the Friday sermon','Collecting charitable donations']},
95:{'sourceURL':'https://quran.com/12/2'},
}
notes='''1|Pilgrimage is the religious journey; ordination enters ministry, sermon is an address and fasting abstains from food. Complete question and parallel noun options checked against Cambridge.
2|Shrine is a holy place connected to a person or object. Calendar, dietary rule and song are not places. Religious sense distinguished from a memorial to a celebrity.
3|Altar is the ceremonial table or raised structure. Hymnbook, congregant and bead do not name that structure. Cambridge supports flat-topped ceremonial structure; both spellings altar/alter distinguished.
4|Relic covers bodily remains and possessions connected with a holy person. New sermon, calendar and appointment are not relics. Physical wording avoids claiming all old objects are religious relics.
5|Scripture is sacred writing. Buildings, choir members and route are not writings. Lower-case scripture permits multiple faiths; Cambridge's general religious sense inspected.
6|Clergy are religious ministers; laity, congregation and pilgrims are not the collective term for ordained ministers. Add church scope because not every religion structures its leadership through ordination.
7|Laity are church members outside clergy. Only priests/bishops would reverse the definition and only professional singers is too narrow. Apostrophe and plural agreement checked.
8|Hospital chaplains provide spiritual care. Surgical instruments, medicine dispensing and diagnostic radiography are distinct clinical tasks. This asks the chaplain's role rather than claiming clergy cannot have other qualifications.
9|Monastery is where monks live and worship. Religious-law list, incense vessel and hymn are not a residence. Singular article and relative clause read correctly.
10|Convent commonly means nuns' residence/community. Synod is council; diocese and parish are church districts. Commonly allows historical broader uses; Cambridge residence definition checked.
11|Abbot is male head of an abbey. Novice is trainee, deacon a different ordained role and cantor a singer. Male scope prevents abbess being another correct title.
12|Abbess is female head of an abbey. Novice, cantor and verger are distinct roles. Female scope and singular title checked against Cambridge.
13|Novice is a beginner in monastic training. Longest-serving member, visiting bishop and owner do not define the role. Remove clumsy 'by definition' distractor wording; age is not made a condition.
14|Sermon is a religious teaching talk. Building, beads and fast are not talks. Cambridge religious/moral address sense matches; grammar and articles checked.
15|Congregation is people gathered for worship. Buildings, clothes and foods are things rather than the gathered people. Singular collective noun takes is.
16|Hymn is a religious praise song. Pilgrimage destination, mat and minister are different categories. Cambridge religious song sense supports answer; no claim that hymns belong exclusively to Christianity.
17|Psalms is the Bible collection of sacred poems/songs. Leviticus, Numbers and Nehemiah contain other material; 'especially known' distinguishes principal character without denying prayers elsewhere. All book names spelled correctly.
18|Burning incense produces fragrant smell/smoke. Bells ring; incense does not project writing or count attendees. Relevant noun sense inspected, excluding verb incense meaning anger.
19|Rosary beads keep track of prayers. They are not a timer, water vessel or candle lighter. Catholic scope removes other everyday meanings; Cambridge explicitly says counting prayers.
20|Mantra is a sacred repeated word/sound/phrase. Entrance, furniture and calendar are not utterances. Religious context excludes figurative business slogan; relevant Cambridge sense inspected.
21|Monotheism is belief in one God, contrasted with multiple deities. Language study and silence rule do not define theism. Cambridge one-god definition and spelling checked.
22|Polytheism means belief in multiple gods, not exactly one. Architecture study and fasting are not this belief. More than one is a precise accessible paraphrase of the dictionary definition.
23|Atheism includes absence of belief in deities; many-god belief is polytheism. Pilgrimage and hymn singing do not define atheism. Answer avoids requiring every atheist to assert certainty that gods do not exist.
24|Agnostic concerns lack of knowledge or unknowability about God's existence. Twelve gods, compulsory religion and sacred-building restriction are not this position. Both ordinary uncertainty and philosophical unknowability are allowed by the correct answer.
25|Theology studies God/religious beliefs. Rocks, planets alone and insects describe other fields. 'Alone' prevents an astronomy topic being argued as theology of creation. Cambridge general definition inspected.
26|Interfaith involves different religions. One congregation, choir or class of clergy restricts it incorrectly. It does not require agreement or conversion; prompt simply asks who is brought together.
27|Fasting is refraining from food for a period. Singing speed, circling a building and rescheduling festivals are different practices. Cambridge noun/verb religious sense inspected among many fast senses.
28|Offering is a gift made in worship or support of religious work. Clergy list, choir room and height rule are not gifts. Answer permits both material gifts and religious donations.
29|Praying to or honouring a deity is religious worship. The other options explicitly describe measurement, logistics and paid repair without devotional context. Cambridge worship sense inspected; question asks for an example, not every possible form.
30|Blessing can be a prayer asking for divine favour/protection. Repair list, travel ticket and time measurement are not that prayer. Religious scope excludes lucky-event/approval meanings.
31|Noah is instructed to make the ark and does as commanded; Moses, David and Solomon are not builders in this story. Expand citation to Genesis 6:13-22 so it names Noah and records compliance, rather than citing only the command in verse 14.
32|Daniel 6 directly describes a den of lions. Wolves, bears and leopards are not the animals in this episode. Biblical attribution retained; plural possessive animals' is correct.
33|Goliath is the Philistine champion David defeats; Saul, Samuel and Jonathan are distinct people. Extend reference beyond the champion's name to include David's victory; title 1 Samuel and spelling checked.
34|Moses receives the Exodus commission. Noah, Solomon and Daniel are not the figure addressed. Extend passage to verse 4, which explicitly names Moses; contextual attribution avoids asserting the account as independently established history.
35|Numbers 26:59 identifies Miriam as Aaron and Moses's sister. Ruth, Esther and Deborah are different women. Shared possessive construction 'Moses and Aaron's sister' refers to one sister and is grammatical.
36|Exodus 31:18 says stone tablets. Glass, wax and wood are not the material specified. Tablets modernises KJV tables without changing the fact; capitalisation of Ten Commandments is standard.
37|Exodus 3 describes a bush burning yet not consumed. Replace invented spectacle distractors with other familiar Exodus motifs, which are not the sight in this episode. Moses's possessive is consistent with the app's English style.
38|Genesis 11 says their language is confounded, causing speech not to be understood. Deafness, sleep and low volume are not the explanation. The prompt explicitly frames the Tower of Babel story.
39|Genesis 8:11 gives an olive leaf. Fig, grape and cedar cone do not occur in this return. Leaf rather than branch follows the passage precisely; all options are singular items.
40|Genesis locates the first garden in Eden. Gethsemane is another biblical garden; Babylon and Jericho are different places. 'In which Genesis places' accurately describes the text's account, not a claim about a known modern location.
41|Luke names Mary as the woman who will bear Jesus. Martha, Elizabeth and Ruth are not his mother. New Testament scope and Jesus's apostrophe checked.
42|Luke 6:13 chooses twelve and names them apostles. Seven, ten and forty are other biblical numbers, not the count here. Distinguishes apostles from the broader group of disciples.
43|John 20 recounts Thomas's doubt and subsequent response. Andrew, Philip and James do not have this traditional nickname. 'Traditionally called' correctly distinguishes the later nickname from a literal title in the passage.
44|Luke 22 describes a rooster crowing as Peter's denials end. Dove, raven and eagle are different biblical birds. Luke scope avoids Mark's two-crow formulation; three denials and rooster remain correct.
45|Matthew 9:9 places Matthew at the tax office/receipt of custom. Fishing, shepherding and pottery are different occupations. 'Collecting taxes' is an ordinary paraphrase, not a claim about what a particular coin exchange looked like.
46|Mark 1:9 names the Jordan for Jesus's baptism by John. Nile, Tigris and Euphrates are other regional rivers. British baptise spelling and proper-name articles checked.
47|The Samaritan assists a traveller robbed and wounded on the road. King, bargain-seeking merchant and soldier are not the injured person in Luke 10. Traveller is British English; possessive Jesus's is correct.
48|Luke 15 says the younger son returns to his father. Commander, teacher and guard are absent alternatives. The parable title and pronoun referent are clear.
49|John 6:9 gives five barley loaves and two fish. Two therefore distracts through fish count; seven and twelve do not answer loaf count. Named Gospel removes variations between feeding narratives.
50|John 11:43-44 names Lazarus coming out of the tomb. Zacchaeus, Nicodemus and Bartimaeus belong to other episodes. Whom is the appropriate object form; biblical scope retained.
51|Luke 19 says Zacchaeus is short, the crowd blocks him and he climbs to see Jesus. Flood, nest and concealed coins are not his reason. Prompt asks the reason, not the tree species.
52|Joshua 6:20 describes the wall falling after the shout and trumpets. Gold, height increase and floating are not outcomes. Biblical account is explicitly identified; plural walls is an ordinary paraphrase of the city's wall.
53|Genesis 9:13 identifies the bow in the cloud as covenant sign. Comet, eclipse and smoke are different phenomena. Rainbow is the unambiguous modern term; after-the-flood context included.
54|Solomon asks for an understanding heart to judge, commonly paraphrased as wisdom. Army, coastline and horses are not his request. Purpose 'govern well' matches the passage rather than equating wisdom with wealth.
55|Matthew 14:25 says Jesus walks on the water to them. Bridge-building, freezing and draining the lake are not described. Gospel and chapter stated; singular action options have correct subject agreement.
56|Synagogue is a Jewish worship/study building. Mosque, cathedral and gurdwara are different traditions' buildings. Similar question template to Sikh place of worship asks a different fact, not a repeated answer.
57|Shabbat is centred on Saturday and extends from Friday evening to Saturday night. Sunday, Tuesday and Thursday are wrong. 'Centred on' avoids wrongly implying it starts at midnight Saturday.
58|Traditional bar mitzvah age is thirteen for a boy. Ten, sixteen and eighteen are not the standard age. This replaces a kosher-food candidate already present in Food & Drink; boy scope distinguishes bat mitzvah customs.
59|Yom Kippur means Day of Atonement. Harvest, Dedication and Liberation are other festival concepts. Cambridge's repentance description and Chabad's explicit English name agree; use canonical Chabad URL.
60|Shofar is an animal-horn trumpet, as Chabad explicitly describes. Shawl, pointer and candle holder are distinct Jewish ritual objects. Not limited to ram's horn because other eligible horns exist.
61|Hanukkah lasts eight nights. Three, six and twelve do not fit. Avoid carrying over Cambridge's imprecise always-in-December wording; no Gregorian month is asserted.
62|Eight Hanukkah lights plus the separate shamash make nine positions. Seven would describe another menorah form; eight excludes the helper and ten overcounts. Explicit inclusion of helper and 'positions' avoids counting the flames actually lit on early nights.
63|Star of David is six-pointed. Five, seven and eight describe other star shapes. Cambridge exact symbol definition inspected; capitalisation and singular points-count question checked.
64|Mezuzah is affixed to a doorpost, as Chabad's home ritual article explains. Plate, shawl and instrument are incorrect locations. Does not confuse the parchment itself with its decorative case.
65|Kippah/yarmulke is a skullcap. Shawl, candle holder and cup are other ritual items. No claim that all Jews or only men must wear one; the item itself is identified.
66|Ganesha's elephant head is explicit in HAF's deity guide. Lion, horse and eagle are different heads. 'Usually depicted' permits unusual artistic forms while identifying the familiar deity.
67|HAF's Hanuman article describes the Vanara monkey warrior devoted to Rama. Ganesha, Indra and Agni do not meet that description. Broad popular depiction wording is appropriate without reducing all Vanara traditions to modern zoology.
68|HAF identifies Lakshmi with prosperity. Saraswati, Parvati and Kali have different principal associations. 'Especially associated' respects overlapping divine qualities; all goddess names checked.
69|HAF associates Saraswati with learning, wisdom, speech and art. Lakshmi, Kali and Durga are not the intended goddess of learning. Grammar and consistent transliteration checked.
70|Museum guide explicitly identifies Shiva's trishul/trident. Ganesha, Brahma and Hanuman are not the deity characterised by this attribute in the options. Source is read via web because direct retrieval is blocked.
71|Replace flute candidate whose retrieved Smithsonian glossary did not support the attribute. HAF directly describes Shiva's third eye; Ganesha, Brahma and Hanuman are not the usual three-eyed depiction. This is different from the existing Shiva cosmic-function question.
72|Bhagavad Gita 2.7 commentary identifies Arjun/Arjuna seeking instruction from Krishna. Ravana, Hanuman and Bharata are not the dialogue partner. Standard English Arjuna spelling used; source inspected beyond a bare verse number.
73|HAF Hanuman article identifies Ramayana as the Rama/Sita rescue epic. Iliad, Odyssey and Aeneid are other epics. The failed Cambridge headword is replaced with relevant retrieved reference.
74|HAF identifies Sita with Rama; Radha/Rukmini relate to Krishna and Draupadi to the Pandavas. Explicit Ramayana scope makes the question about its narrative. Apostrophe in Rama's checked.
75|Replace ten-headed Ravana candidate whose assigned HAF PDF did not support that attribute. The inspected HAF deity guide directly calls Surya Sun God, contrasting Indra thunder/rain and the different Agni/Varuna associations. Sun capitalised as our star's name.
76|Cambridge/HAF identify Diwali as festival of lights. Holi, Navaratri and Raksha Bandhan are different festivals. It is a Hindu festival without claiming exclusive observance by Hindus.
77|HAF Holi page explicitly describes coloured powders/gulal and coloured water. Diwali, Janmashtami and Maha Shivaratri are different observances. British coloured spelling used; no claim that powder is mandatory everywhere.
78|Met museum object directly names Durga victorious over buffalo demon Mahisha. Lakshmi, Saraswati and Sita do not match. Simplify original mount-plus-victory wording to the clearly supported object subject.
79|HAF describes Brahma's four heads. Shiva, Ganesha and Hanuman are not commonly four-headed. Commonly qualifier allows exceptional forms without weakening the standard iconography question.
80|Museum guide and HAF's longer Hinduism PDF identify Vishnu reclining on Shesha. Brahma, Ganesha and Hanuman are different deities. Proper names and participle reclining checked.
81|Cambridge supports a sacred Buddhist monument with dome. Remove extra relic-content claim from answer because not needed to identify it; prayer shawl, wind instrument and festival food remain wrong object types.
82|Sangha is a Buddhist community or monastic order, as Merriam-Webster states. Incense, roof and meal are not communities. Buddhist scope avoids the term's Jain usage and does not restrict it only to lay followers.
83|Cambridge describes nirvana as freedom from suffering through removing craving/wishes. Language requirements, seasonal cycles and gravity are not the religious liberation described. No claim of a geographic heaven.
84|Replace arbitrary shopping/counting examples with a clear definition-recognition question. Meditation trains focused awareness; fasting abstains from food, pilgrimage is travel and ordination enters ministry. All four options are parallel religious-practice nouns.
85|UN Vesak material explicitly commemorates birth, enlightenment and passing away. Diwali, Yom Kippur and Eid al-Fitr are other faiths' festivals. 'In many traditions' acknowledges different Buddhist observance calendars.
86|Manitoba's Buddhist texts resource gives three baskets for Tipitaka/Tripitaka. Four rivers, five mountains and seven gates are not translations. Reference replaced after Merriam retrieval failed; Sanskrit/Pali variation is not offered as a competing answer.
87|Cambridge defines lama as Tibetan Buddhist spiritual teacher. Drum, gateway and lake are not the person/title. Lama spelling distinguishes the unrelated animal llama.
88|Manitoba resource explicitly labels monks bhikkhus and nuns bhikkhunis. Tree, bell and mountain are not monastics. Reference changed to actually inspected education PDF rather than inaccessible Merriam entry.
89|Mosque is Muslim communal worship building. Synagogue, gurdwara and cathedral belong to other traditions. Template similarity to the Sikh-building question is a different religious vocabulary item.
90|Quran is Islam's central sacred text. Torah, Vedas and Guru Granth Sahib belong to Judaism, Hinduism and Sikhism respectively. Cambridge Koran headword is an alternate English spelling, not a different book.
91|Allah translates as God; temple, prophet and pilgrim are different terms. Cambridge notes use by Arab Christians too, so prompt avoids saying it is an exclusively Muslim word.
92|Islamic Relief's actual Eid celebration page says Eid al-Fitr ends Ramadan. Eid al-Adha, Ashura and Mawlid have different occasions. Replace invented/non-working knowledge-base URL with the discovered relevant page.
93|Halal means permitted/lawful under Islamic rules. Forbidden is haram; raw and sweet are food properties rather than legal status. Dietary scope and Cambridge permitted-activity definition agree.
94|Muezzin gives the call to prayer. Rulings, Friday sermon and charity collection do not define the role. Remove repeated 'every' from distractors; someone holding multiple roles does not change the defining duty.
95|Quran 12:2 explicitly describes an Arabic Quran. Persian, Turkish and Urdu translations do not make them the original language. This replaces an already-covered Mecca prayer-direction fact; Islamic tradition qualifier retained.
96|Sikh Coalition names kirpan the religious sword. Kara is bracelet, kanga comb and kachera undergarment. Reference describes it directly; no claim about one mandatory blade length or sex of wearer.
97|Guru is a spiritual teacher/guide in the relevant Cambridge Hindu/Sikh sense. Building, meal and instrument are not a teacher. Religious context excludes modern marketing expert sense.
98|Sikh turban/dastar is the named head covering. Mitre, zucchetto and biretta are different religious headwear. Closely associated does not imply Sikhs are the only people who wear turbans.
99|Sikh Coalition identifies kachera as under-shorts. Kanga, kara and kirpan are comb, bracelet and sword. Special undergarment is an accessible accurate description; each option names one of the Five Ks.
100|Sikh Coalition explicitly calls seva selfless service and gives practical examples. Turban style, sword type and prayer time are not seva. Voluntary service is not restricted to a paid or caste-based role; final prompt/options read correctly.
'''
rows=[]
for line in notes.strip().splitlines():
 n,note=line.split('|',1);n=int(n)
 d={'row':n,'action':'edit' if n in edits else 'keep','prompt':draft[n-1]['prompt'],'note':note,
 'sourceReview':'Individual author second editorial pass: prompt, four answers, sole correct choice, grammar, relevance and the explicitly identified dictionary/scripture/faith/education reference inspected. Not an independent review.'}
 if n in edits:d['recommendedChanges']=edits[n]
 rows.append(d)
assert [x['row'] for x in rows]==list(range(1,101))
(HERE/'independent-review.json').write_text(json.dumps({'reviewer':'root (author second editorial pass)','independent':False,
 'sourceAccessNote':'Cambridge definitions and BibleGateway KJV passages inspected individually; relevant HAF PDF sections and named faith/education pages read. Direct retrieval failures were resolved through web sources or explicit replacement references, never counted as successful inspections. Two repeated concepts replaced before this final pass (kosher and Mecca prayer direction). Third eye/Surya replace attributes unsupported by the initially assigned references. Private reference excerpts remain outside the public repository. Per-item notes record author judgments, not an automated or independent approval.',
 'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('100 explicit author final decisions recorded; edits must be applied before publication.')
