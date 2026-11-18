"""Original accessible religion candidates; publication requires a final individual review."""
import json,pathlib
HERE=pathlib.Path(__file__).parent
sources={
'deities':'https://www.hinduamerican.org/wp-content/uploads/2019/12/WhoHindusWorship.pdf',
'sikh':'https://www.sikhcoalition.org/wp-content/uploads/2018/05/Sikh-Coalition-Letter-Colorado-Dept-of-Education.pdf',
}
rows='''pilgrimage|What is a journey made to a place for religious reasons called?|A pilgrimage|An ordination|A sermon|A fast|Pilgrimage is the journey; the other terms describe entering ministry, a talk and abstaining from food.
shrine|What is a shrine?|A place associated with a holy person or object|A list of religious holidays|A rule about food|A religious song|A shrine is a sacred place, not a calendar, dietary rule or song.
altar|In a place of worship, what is an altar?|A table or raised structure used for religious ceremonies|A book of hymns|A member of the congregation|A type of prayer bead|Altar denotes the ceremonial table or structure; the alternatives are different religious items or people.
relic|What does a religious relic usually consist of?|Physical remains or an object connected with a holy person|A newly written sermon|A list of annual festivals|An appointment to lead worship|Relics are physical remains or associated objects; the alternatives are not relics.
scripture|What does the word scripture refer to?|Sacred religious writings|Religious buildings|Members of a choir|A pilgrimage route|Scripture means sacred writings, not structures, singers or routes.
clergy|What is the collective term for people ordained for religious duties?|Clergy|Laity|Congregation|Pilgrims|Clergy denotes ordained religious ministers; the other terms identify different groups.
laity|In a church, who are the laity?|Members who are not clergy|Only the ordained priests|Only visiting bishops|Only the choir's professional singers|Laity are non-clergy members; the alternatives wrongly restrict the group.
chaplain|What is the role of a chaplain in a hospital?|Providing religious or spiritual care|Managing surgical instruments|Dispensing prescription medicines|Taking diagnostic X-rays|Chaplaincy concerns spiritual care; the other responsibilities belong to clinical staff.
monastery|What is a monastery?|A place where monks live as a religious community|A list of religious laws|A vessel used for incense|A special kind of hymn|Monastery names the community's residence; the other options are unrelated objects or texts.
convent|Which word commonly names a community or home of nuns?|Convent|Synod|Diocese|Parish|Convent fits the residence or community; the others name a council or church district.
abbot|What is the title of the male head of an abbey?|Abbot|Novice|Deacon|Cantor|An abbot heads an abbey; the other religious roles are distinct.
abbess|What is the title of the female head of an abbey?|Abbess|Novice|Cantor|Verger|Abbess is the female superior; the alternatives name other roles.
novice|In a religious community, what is a novice?|Someone beginning a period of training|The oldest member by definition|A visiting bishop by definition|The person who owns the building|A novice is a new trainee; age and ownership do not define it.
sermon|What is a sermon?|A talk giving religious teaching|A religious building|A string of prayer beads|A day without food|A sermon is a religious address; the other options describe a building, object and fast.
congregation|What is a congregation?|A group gathered for religious worship|A collection of sacred buildings|A set of ceremonial clothes|A list of permitted foods|Congregation denotes the people assembled to worship.
hymn|What is a hymn?|A song of religious praise|A place of pilgrimage|A type of prayer mat|A member of the clergy|Hymn is a religious song, not a place, mat or minister.
psalm|Which Bible book is especially known for sacred songs and prayers?|Psalms|Leviticus|Numbers|Nehemiah|Psalms collects songs and prayers; the other books have different principal forms.
incense|What is incense burned for in many religious ceremonies?|To produce a fragrant smell|To ring like a bell|To project written words|To measure the congregation's size|Incense releases fragrant smoke; the other actions do not describe its ceremonial use.
rosary|In Catholic practice, what is a rosary used for?|Keeping track of a sequence of prayers|Measuring the length of a sermon|Holding holy water|Lighting candles|Rosary beads count prayers; the other uses are not what the beads are designed for.
mantra|What is a mantra in religious practice?|A sacred word or phrase repeated in prayer or meditation|A building's main entrance|An item of ceremonial furniture|A list of festival dates|A mantra is repeated sacred utterance; the other options are not utterances.
monotheism|What does monotheism mean?|Belief in one God|Belief in many gods|The study of ancient languages|A rule requiring silence|Monotheism means belief in one deity; the alternatives differ.
polytheism|What does polytheism mean?|Belief in more than one god|Belief in exactly one god|The study of sacred buildings|A period of fasting|Polytheism is belief in multiple deities; the other options are distinct.
atheism|What does atheism refer to?|Absence of belief in gods|Belief in many gods|A particular kind of pilgrimage|The practice of singing hymns|Atheism involves lack of belief in deities; the alternatives do not define it.
agnostic|Which description best fits an agnostic position about God's existence?|It is unknown or cannot be known|There must be exactly twelve gods|Everyone must join the same religion|Only religious buildings can be sacred|Agnosticism concerns uncertainty or unknowability, not any of the other claims.
theology|What is theology the study of?|God and religious beliefs|The structure of rocks|The movement of planets alone|The classification of insects|Theology studies deity and religious belief; the other options are other fields.
interfaith|What does an interfaith event bring together?|People from different religions|Only people from one congregation|Only members of one choir|Only newly ordained ministers|Interfaith means involving different faiths, not restricting attendance to one religious group or role.
fast|What does fasting involve in a religious context?|Going without food for a period of time|Singing a hymn more quickly|Walking around a building|Changing the date of a festival|Fasting is abstention from food, sometimes drink too; alternatives do not define it.
offering|In worship, what is an offering?|Something given to honour a deity or support religious work|A list of clergy members|A room reserved for a choir|A rule about building height|An offering is a gift; the alternatives are not gifts.
worship|Which activity is an example of religious worship?|Praying to or honouring a deity|Measuring a building's floor area|Counting chairs for delivery|Repairing a broken window for payment|Prayer or reverence is worship; the alternatives are practical tasks without a stated devotional purpose.
blessing|In a religious setting, what is a blessing?|A prayer asking for divine favour or protection|A list of building repairs|A type of travel ticket|A measurement of time|A blessing invokes divine favour; the other options are not prayers.
genesis/6|According to Genesis, who builds the ark before the great flood?|Noah|Moses|David|Solomon|Genesis 6 names Noah as the builder; the other biblical figures belong to other stories.
daniel/6|According to the Book of Daniel, into which animals' den is Daniel thrown?|Lions|Wolves|Bears|Leopards|Daniel 6 describes a lions' den; the other animals are not named in this episode.
1samuel/17|In 1 Samuel, what is the name of the giant defeated by David?|Goliath|Saul|Samuel|Jonathan|Goliath is David's opponent; the other names identify different figures.
exodus/3|In the Exodus story, who is called to lead the Israelites out of Egypt?|Moses|Noah|Solomon|Daniel|Moses receives the commission; the other figures do not lead this departure.
numbers/26|According to Numbers 26, what is the name of Moses and Aaron's sister?|Miriam|Ruth|Esther|Deborah|Numbers 26:59 names Miriam as their sister; the other women are different biblical figures.
exodus/31|In Exodus, the Ten Commandments are written on tablets made of what?|Stone|Glass|Wax|Wood|Exodus 31:18 describes stone tablets; the other materials are not used in this passage.
exodus/3|In Exodus 3, what unusual sight draws Moses's attention?|A bush burning without being consumed|A river turning to ice|A mountain floating in the air|A tree covered in silver leaves|The burning bush is the sight in this chapter; the alternatives are not events in the account.
genesis/11|In the Tower of Babel story, what prevents the builders from understanding one another?|Their language is confused|They all lose their hearing|They all fall asleep|Their voices become too quiet|Genesis 11 attributes the confusion to language; the alternatives are not the narrative's explanation.
genesis/8|In Genesis 8, what does the dove bring back to Noah?|An olive leaf|A fig|A grape|A cedar cone|The dove returns with an olive leaf; the other objects are not described in this episode.
genesis/2|What is the name of the garden in which Genesis places Adam and Eve?|Eden|Gethsemane|Babylon|Jericho|Eden is the garden in Genesis; Gethsemane is another garden and the other names are cities.
luke/1|In the New Testament, what is the name of Jesus's mother?|Mary|Martha|Elizabeth|Ruth|Mary is named as Jesus's mother; the other women have different roles.
luke/6|How many apostles does Jesus choose in Luke 6?|Twelve|Seven|Ten|Forty|Luke 6:13 specifies twelve; the alternatives are different biblical numbers.
john/20|Which apostle is traditionally called 'Doubting' after questioning reports of Jesus's resurrection?|Thomas|Andrew|Philip|James|John 20 describes Thomas's doubt; the other apostles do not have this traditional nickname.
luke/22|In Luke's Gospel, what bird calls after Peter has denied knowing Jesus three times?|A rooster|A dove|A raven|An eagle|Luke 22 describes a rooster crowing; the other birds are not named in the denial scene.
matthew/9|In Matthew's Gospel, what is Matthew doing when Jesus calls him to follow?|Collecting taxes|Catching fish|Herding sheep|Making pottery|Matthew 9:9 places him at the tax booth; the alternatives are other occupations.
mark/1|In Mark's Gospel, in which river does John baptise Jesus?|The Jordan|The Nile|The Tigris|The Euphrates|Mark 1:9 names the Jordan; the other rivers are not the baptism location.
luke/10|In Jesus's Good Samaritan parable, whom does the Samaritan help?|A traveller attacked by robbers|A king seeking a new palace|A merchant seeking cheaper goods|A soldier looking for his sword|Luke 10 describes aid to the injured traveller; the alternatives are not the person helped.
luke/15|In the parable of the prodigal son, to whom does the younger son return?|His father|His army commander|His childhood teacher|His prison guard|Luke 15 describes the son's return to his father; the alternatives are absent from the parable.
john/6|In John's account of feeding the five thousand, how many loaves does the boy have?|Five|Two|Seven|Twelve|John 6:9 names five barley loaves and two fish; only five answers the loaf count.
john/11|According to John 11, whom does Jesus call out of a tomb?|Lazarus|Zacchaeus|Nicodemus|Bartimaeus|John 11 identifies Lazarus; the other people are associated with other episodes.
luke/19|In Luke 19, why does Zacchaeus climb a tree?|To see Jesus above the crowd|To escape a flood|To collect a bird's nest|To hide stolen coins|Luke 19 says he climbs to see Jesus because he is short and the crowd blocks him.
joshua/6|In Joshua 6, what happens to Jericho's walls after the people shout?|They collapse|They turn to gold|They grow taller|They float across a river|Joshua 6 describes the walls falling; the other outcomes are absent.
genesis/9|In Genesis 9, what is the sign of God's covenant after the flood?|A rainbow|A comet|A solar eclipse|A pillar of smoke|Genesis 9 names the bow in the clouds; the other phenomena are not this covenant sign.
1kings/3|In 1 Kings 3, what does Solomon ask God to give him so he can govern well?|Wisdom|A larger army|A longer coastline|More horses|Solomon asks for an understanding heart to judge rightly, commonly summarised as wisdom; the alternatives are not his request.
matthew/14|In Matthew 14, what does Jesus do on the lake as he approaches the disciples' boat?|Walks on the water|Builds a bridge|Freezes the water|Drains the lake|The passage describes walking on the water; the alternatives are not in the account.
synagogue|What is a Jewish place of communal worship called?|A synagogue|A mosque|A cathedral|A gurdwara|Synagogue is the Jewish worship building; the others belong to other religious traditions.
shabbat|Which day of the week is the Jewish Sabbath centred on?|Saturday|Sunday|Tuesday|Thursday|Shabbat runs from Friday evening to Saturday night; Saturday is the day among the options.
kosher|What does kosher food comply with?|Jewish dietary law|A rule that all food must be raw|A rule that every dish must be sweet|A ban on all fruit|Kosher refers to compliance with Jewish dietary law, not the invented dietary restrictions.
yom-kippur|Yom Kippur is commonly known in English as the Day of what?|Atonement|Harvest|Dedication|Liberation|Yom Kippur is the Day of Atonement; the alternatives are different festival concepts.
shofar|What kind of object is a shofar used in Jewish worship?|A horn blown as a trumpet|A prayer shawl|A scroll pointer|A candle holder|A shofar is an animal horn used as a wind instrument; the other ritual objects differ.
hanukkah|For how many nights is the Jewish festival of Hanukkah celebrated?|Eight|Three|Six|Twelve|Hanukkah lasts eight nights; the alternatives are not its duration.
hanukkah|How many candle positions does a Hanukkah lamp have, including the helper light?|Nine|Seven|Eight|Ten|There are eight festival lights and a separate shamash, totalling nine; specifying the helper removes ambiguity.
star-of-david|How many points does the Star of David have?|Six|Five|Seven|Eight|The six-pointed star is the symbol; the alternatives are different stars.
mezuzah|Where is a mezuzah traditionally attached in a Jewish home?|To a doorway's doorpost|To a dinner plate|To a prayer shawl|To a musical instrument|A mezuzah is affixed to the doorpost; the other locations are not the prescribed placement.
yarmulke|What is a kippah, also called a yarmulke?|A small skullcap|A prayer shawl|A candle holder|A ceremonial cup|Kippah and yarmulke name a head covering; the other objects differ.
deities|Ganesha is usually depicted with the head of which animal?|An elephant|A lion|A horse|An eagle|Ganesha's elephant head is his familiar identifying feature; the other heads belong to other imagery.
deities|Which Hindu deity is commonly depicted as a monkey and is devoted to Rama?|Hanuman|Ganesha|Indra|Agni|Hanuman is the monkey deity devoted to Rama; the other deities differ.
deities|Which Hindu goddess is especially associated with wealth and prosperity?|Lakshmi|Saraswati|Parvati|Kali|Lakshmi is the prosperity goddess; the other goddesses have different principal associations.
deities|Which Hindu goddess is especially associated with learning and the arts?|Saraswati|Lakshmi|Kali|Durga|Saraswati is associated with knowledge and the arts; the other goddesses differ.
deities|Which Hindu deity is particularly associated with a trident?|Shiva|Ganesha|Brahma|Hanuman|Shiva's trishula is a familiar attribute; the other options are not the deity identified by this attribute.
deities|Which Hindu deity is famously depicted playing a flute?|Krishna|Ganesha|Hanuman|Agni|Krishna's flute is a familiar iconographic feature; the alternatives differ.
deities|In the Bhagavad Gita, to which warrior does Krishna give his teaching?|Arjuna|Ravana|Hanuman|Bharata|Arjuna is Krishna's dialogue partner; the others belong to other narrative roles.
ramayana|Which Hindu epic tells the story of Rama and Sita?|The Ramayana|The Iliad|The Odyssey|The Aeneid|The Ramayana is their epic; the other epics are Greek or Roman.
deities|In the Ramayana, who is Rama's wife?|Sita|Radha|Rukmini|Draupadi|Sita is Rama's wife; the others are associated with other figures.
deities|Ravana is traditionally depicted with how many heads?|Ten|Two|Five|Seven|Ravana is ten-headed in the Ramayana tradition; the alternatives differ.
diwali|Which Hindu festival is widely known as the festival of lights?|Diwali|Holi|Navaratri|Raksha Bandhan|Diwali is the festival of lights; the other festivals have different central associations.
holi|Which Hindu festival is especially associated with throwing coloured powders?|Holi|Diwali|Janmashtami|Maha Shivaratri|Holi is the festival of colours; the alternatives do not name this festival.
deities|In Hindu art, which goddess is commonly shown riding a lion or tiger and defeating a buffalo demon?|Durga|Lakshmi|Saraswati|Sita|Durga's defeat of Mahishasura and lion/tiger mount distinguish this depiction.
deities|Which Hindu deity is commonly shown with four heads?|Brahma|Shiva|Ganesha|Hanuman|Brahma is commonly four-headed; the other deities are not identified by that feature.
deities|Which Hindu deity is commonly shown reclining on the serpent Shesha?|Vishnu|Brahma|Ganesha|Hanuman|Vishnu reclines on Shesha; the alternatives are different deities.
stupa|What is a stupa in Buddhism?|A sacred monument often containing relics|A type of prayer shawl|A religious wind instrument|A special food eaten at festivals|A stupa is a sacred monument or reliquary; the alternatives are different ritual items.
sangha|In Buddhism, what does sangha refer to?|The Buddhist community|A type of incense|A temple's roof|A festival meal|Sangha denotes the community, especially the monastic community; the objects and meal do not fit.
nirvana|In Buddhism, nirvana is associated with liberation from what?|Craving and suffering|The need to learn languages|The passing of the seasons|The pull of gravity|Nirvana is liberation associated with the extinguishing of craving and suffering, not a physical exemption.
meditation|Which activity is an example of meditation?|Training attention through focused awareness|Reciting a shopping list to a cashier|Counting seats for a ticket office|Measuring a window frame|Meditation trains attention and awareness; the alternatives lack the stated contemplative purpose.
wesak|Which Buddhist festival commemorates the Buddha's birth, enlightenment and death in many traditions?|Vesak|Diwali|Yom Kippur|Eid al-Fitr|Vesak, also spelled Wesak, marks those events in many Buddhist traditions; the others belong to different religions.
tripitaka|The Buddhist name Tripitaka is commonly translated into English as what?|Three baskets|Four rivers|Five mountains|Seven gates|Tripitaka means three baskets, referring to divisions of texts; other translations are wrong.
lama|In Tibetan Buddhism, what is a lama?|A religious teacher|A ceremonial drum|A temple gateway|A sacred lake|A lama is a spiritual teacher; the other options are not people.
bhikkhu|What is a bhikkhu in Buddhism?|A monk|A sacred tree|A prayer bell|A holy mountain|Bhikkhu is a fully ordained male monastic; the other options are objects or places.
mosque|What is a Muslim place of communal worship called?|A mosque|A synagogue|A gurdwara|A cathedral|Mosque names the Muslim worship building; the others belong to other faiths.
koran|What is Islam's central sacred text called?|The Quran|The Torah|The Vedas|The Guru Granth Sahib|The Quran is Islam's scripture; the other texts belong to other traditions.
allah|What is the Arabic word Allah commonly translated as in English?|God|Temple|Prophet|Pilgrim|Allah means God, and is also used by Arabic-speaking Christians; it does not mean the alternatives.
eid-al-fitr|Which Islamic festival marks the end of Ramadan?|Eid al-Fitr|Eid al-Adha|Ashura|Mawlid|Eid al-Fitr ends the fasting month; the other observances occur for different reasons.
halal|In Islamic dietary rules, what does halal mean?|Permitted|Forbidden|Always raw|Always sweet|Halal means lawful or permitted; haram is forbidden and the other terms do not define it.
muadhdhin|What is the role of a muezzin at a mosque?|Calling people to prayer|Writing every Friday sermon|Deciding every marriage dispute|Collecting every charitable donation|The muezzin gives the call to prayer; the other duties do not define the role.
mecca|Towards which city do Muslims face when performing the prescribed daily prayers?|Mecca|Cairo|Istanbul|Damascus|Muslims face the Kaaba in Mecca; the other cities are not the qibla destination.
kirpan|Which of the Sikh Five Ks is a ceremonial sword?|Kirpan|Kara|Kanga|Kachera|Kirpan names the sword; the other terms name bracelet, comb and shorts respectively.
guru|What does the word guru mean in a religious context?|A spiritual teacher|A prayer building|A ceremonial meal|A stringed instrument|Guru is a teacher or spiritual guide; the other items are not people.
turban|Which item of headwear is closely associated with Sikh identity?|A turban|A mitre|A zucchetto|A biretta|Sikh dastar is a turban; the other headwear belongs to different religious roles.
sikh|Which of the Sikh Five Ks is a special undergarment?|Kachera|Kanga|Kara|Kirpan|Kachera is the undergarment; the other terms name comb, bracelet and sword.
seva|In Sikh practice, what does seva mean?|Selfless service to others|A particular style of turban|A type of ceremonial sword|A fixed time of daily prayer|Seva concerns voluntary service; the other options do not define it.
'''

def source(key):
    if key in sources:return sources[key]
    if '/' in key:return 'https://bible.usccb.org/bible/'+key
    return 'https://dictionary.cambridge.org/dictionary/english/'+key

if __name__=='__main__':
    q=[]
    for line in rows.strip().splitlines():
        key,prompt,correct,*tail=line.split('|');assert len(tail)==4
        q.append({'draftID':f'easy-36-{len(q)+1:03d}','categoryID':'36','difficulty':'easy','prompt':prompt,'answers':[correct,*tail[:3]],'correctIndex':0,'rationale':tail[3],'sourceURL':source(key),'reviewStatus':'draft_awaiting_author_final_check'})
    q[57].update(prompt='At what age does a Jewish boy traditionally become bar mitzvah?',answers=['Thirteen','Ten','Sixteen','Eighteen'],sourceURL='https://dictionary.cambridge.org/dictionary/english/bar-mitzvah',rationale='Traditional bar mitzvah age is thirteen; the other ages are not the standard age.')
    q[94].update(prompt='According to Islamic tradition, in which language was the Quran originally revealed?',answers=['Arabic','Persian','Turkish','Urdu'],sourceURL='https://www.islamic-relief.org.uk/resources/knowledge-base/quran/',rationale='The Quran was revealed in Arabic; the other languages have translations but are not the original language.')
    (HERE/'draft.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(f'{len(q)} unapproved candidates')
