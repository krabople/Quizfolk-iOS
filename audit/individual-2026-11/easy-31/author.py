"""100 accessible anime candidates from inspected premises; not editorial approval."""
import json,pathlib,urllib.parse
H=pathlib.Path(__file__).parent
groups=[('The Apothecary Diaries','''Who is the young heroine of The Apothecary Diaries?|Maomao|Hina|Suzu|Natsume
Where does Maomao work after being sold into service in The Apothecary Diaries?|The imperial palace|A coastal lighthouse|A mountain monastery|A travelling circus
The fictional setting of The Apothecary Diaries is inspired mainly by which country?|China|France|Egypt|Brazil
Which field of knowledge helps Maomao solve mysteries in The Apothecary Diaries?|Medicine|Shipbuilding|Astronomy|Military engineering
Which influential palace figure takes notice of Maomao in The Apothecary Diaries?|Jinshi|Gabimaru|Hodaka|Tsuneo'''),('Bocchi the Rock!','''What is the name of the shy heroine nicknamed Bocchi in Bocchi the Rock!?|Hitori Gotoh|Ai Hoshino|Miyo Saimori|Maomao
Which instrument does Hitori play in Bocchi the Rock!?|Guitar|Trumpet|Harp|Accordion
What is Hitori's band called in Bocchi the Rock!?|Kessoku Band|B-Komachi|Sick Hack|Sideros
Which personal difficulty is central to Hitori's story in Bocchi the Rock!?|Social anxiety|Loss of all memory|Fear of the ocean|An inability to hear music
Who invites Hitori into her band in Bocchi the Rock!?|Nijika Ijichi|Ai Hoshino|Miyo Saimori|Hina Amano'''),('Oshi no Ko','''What is Ai Hoshino's profession in Oshi no Ko?|Pop idol|Police detective|Professional tennis player|Marine biologist
How are Aqua and Ruby related in Oshi no Ko?|They are twins|They are cousins|They are stepsiblings|They are aunt and nephew
Which Oshi no Ko character is also called Aqua?|Aquamarine Hoshino|Gorou Amamiya|Taiki Himekawa|Hikaru Kamiki
What career does Ruby pursue in Oshi no Ko?|Becoming an idol|Becoming a surgeon|Becoming a judge|Becoming an astronaut
What is the name of the idol group associated with Ai and later Ruby in Oshi no Ko?|B-Komachi|Kessoku Band|Sick Hack|Sideros'''),('Zom 100','''Who is the main character of Zom 100: Bucket List of the Dead?|Akira Tendo|Kafka Hibino|Denji|Yuji Itadori
What kind of job is Akira desperate to escape at the start of Zom 100?|An exploitative office job|A job as a lighthouse keeper|A job as a zookeeper|A job as a ski instructor
What disaster gives Akira an unexpected sense of freedom in Zom 100?|A zombie outbreak|A volcanic eruption|A meteor shower|A worldwide flood
What does Akira make to guide his adventures in Zom 100?|A bucket list|A royal family tree|A catalogue of rare coins|A map of imaginary planets
Which Zom 100 companion comes from Germany?|Beatrix|Shizuka|Kencho|Akira'''),('My Happy Marriage','''Who is the heroine of My Happy Marriage?|Miyo Saimori|Maomao|Hitori Gotoh|Hina Amano
To whom is Miyo engaged in My Happy Marriage?|Kiyoka Kudou|Jinshi|Hodaka Morishima|Gabimaru
What is Kiyoka's occupation in My Happy Marriage?|Military commander|Newspaper editor|Baker|Railway conductor
How is Miyo treated by her stepmother at the start of My Happy Marriage?|She is forced into servitude|She is appointed head of the household|She is crowned empress|She is trained as a naval captain
My Happy Marriage takes place in a fantasy version of which country?|Japan|Italy|India|Mexico'''),("Hell's Paradise: Jigokuraku",'''What is Gabimaru's occupation in Hell's Paradise?|Ninja|Merchant sailor|Court musician|Village blacksmith
Who accompanies Gabimaru as his executioner in Hell's Paradise?|Yamada Asaemon Sagiri|Miyo Saimori|Hina Amano|Anya Forger
What substance are the convicts sent to find in Hell's Paradise?|An elixir of immortality|A potion that turns metal into gold|A medicine that removes all memories|An ink that predicts the future
Where are the convicts sent to search in Hell's Paradise?|A mysterious island|An underground railway|A floating space station|A desert caravan route
What reward is offered to Gabimaru for completing the mission in Hell's Paradise?|A pardon for his crimes|A hereditary royal title|Command of a merchant fleet|Ownership of an imperial mint'''),('Suzume','''What object is Souta transformed into in Suzume?|A chair|An umbrella|A bicycle|A lantern
What must Suzume and Souta close to prevent disasters in Suzume?|Mysterious doors|Railway tunnels|Floodgates on a dam|Windows in a palace
What kind of disaster can the supernatural worm cause in Suzume?|Earthquakes|Avalanches|Blizzards|Volcanic eruptions
Who has raised Suzume after her mother's death?|Her aunt|Her older brother|Her grandfather|A family of travelling performers
Suzume's journey takes her across which country?|Japan|China|South Korea|Thailand'''),('Weathering with You','''To which city does Hodaka run away in Weathering with You?|Tokyo|Kyoto|Osaka|Sapporo
What unusual ability does Hina have in Weathering with You?|She can clear the rain and bring sunshine|She can talk to trees|She can travel into the past|She can turn stones into gold
What is Hina's younger brother called in Weathering with You?|Nagi|Aqua|Hibiki|Rudger
Which boy befriends Hina in Weathering with You?|Hodaka Morishima|Tsuneo Suzukawa|Kai Ashimoto|Akira Tendo
Who directed Weathering with You?|Makoto Shinkai|Hayao Miyazaki|Mamoru Hosoda|Masaaki Yuasa'''),('Belle (2021 film)','''What is Belle's real-world first name in the anime film Belle?|Suzu|Miyo|Hinako|Natsume
What is the virtual world called in the anime film Belle?|U|Eden|Oasis|Arcadia
What talent makes Belle famous in the virtual world?|Singing|Chess|Motor racing|Sword making
Which intimidating avatar does Belle try to understand?|The Dragon|The Phoenix|The Kraken|The Griffin
Who directed the 2021 anime film Belle?|Mamoru Hosoda|Makoto Shinkai|Hayao Miyazaki|Hiromasa Yonebayashi'''),('A Whisker Away','''What animal can Miyo become in A Whisker Away?|A cat|A fox|A rabbit|A bird
What magical object allows Miyo's transformation in A Whisker Away?|A mask|A ring|A comb|A bracelet
Which boy does Miyo hope to get closer to in A Whisker Away?|Kento Hinode|Hodaka Morishima|Hibiki|Tsuneo Suzukawa
What is Miyo called when she visits Hinode as a cat in A Whisker Away?|Tarō|Tib|Daijin|Zinzan
Which craft does Hinode practise in A Whisker Away?|Pottery|Glassblowing|Bookbinding|Metal engraving'''),('Josee, the Tiger and the Fish (2020 film)','''What is Tsuneo doing when he meets Josee in the 2020 anime film Josee, the Tiger and the Fish?|Studying at university|Serving as a police officer|Training as a ballet dancer|Working as a royal bodyguard
What mobility aid does Josee use in the 2020 anime film Josee, the Tiger and the Fish?|A wheelchair|A walking frame|A white cane|A prosthetic leg
Who does Tsuneo grow close to in the 2020 anime film Josee, the Tiger and the Fish?|Josee|Miyo|Hina|Maomao
What creative career does Josee hope to pursue in the 2020 anime film Josee, the Tiger and the Fish?|Storybook illustrator|Opera singer|Fashion photographer|Film composer
Which country does Tsuneo hope to study in in the 2020 anime film Josee, the Tiger and the Fish?|Mexico|Norway|Egypt|India'''),('Ride Your Wave','''Which water sport does Hinako love in Ride Your Wave?|Surfing|Rowing|Water polo|Competitive diving
What is Minato's job in Ride Your Wave?|Firefighter|Marine biologist|Chef|Architect
What emergency first brings Hinako and Minato together in Ride Your Wave?|A fire in her apartment building|A railway collision|A landslide on a mountain road|A ship running aground
In what does Hinako see Minato after his death in Ride Your Wave?|Water|Mirrors|Photographs|Clouds
What does Hinako do to make Minato appear in Ride Your Wave?|Sings their shared song|Rings a brass bell|Lights a candle|Plays a drum'''),('Words Bubble Up Like Soda Pop','''What type of poetry does Cherry write in Words Bubble Up Like Soda Pop?|Haiku|Sonnets|Limericks|Epic poetry
Why does Smile cover her mouth in Words Bubble Up Like Soda Pop?|She is self-conscious about her teeth and braces|She is hiding a royal birthmark|She is unable to speak|She is concealing a magical tattoo
Where do Cherry and Smile first meet in Words Bubble Up Like Soda Pop?|A shopping mall|An airport|A mountain shrine|A railway museum
What do Cherry and Smile accidentally swap in Words Bubble Up Like Soda Pop?|Their phones|Their bicycles|Their school uniforms|Their house keys
What lost item do Cherry and Smile help an older man find in Words Bubble Up Like Soda Pop?|A music record|A pocket watch|A wedding photograph|A signed baseball'''),('The Boy and the Heron','''What is the boy's first name in The Boy and the Heron?|Mahito|Souta|Hodaka|Rudger
Which studio made The Boy and the Heron?|Studio Ghibli|Studio Ponoc|Studio Colorido|Science Saru
Who directed The Boy and the Heron?|Hayao Miyazaki|Makoto Shinkai|Mamoru Hosoda|Masaaki Yuasa
What structure leads Mahito into a fantastical world in The Boy and the Heron?|A tower|A railway station|A lighthouse on a ship|A glass greenhouse
Which war forms the backdrop to the beginning of The Boy and the Heron?|The Pacific War during World War II|The Korean War|The First World War|The Napoleonic Wars'''),('The Imaginary (film)','''What is Rudger in the anime film The Imaginary?|An imaginary friend|A visiting prince|A robot servant|A young ghost hunter
Which girl creates Rudger in The Imaginary?|Amanda|Miyo|Hina|Suzu
What threatens an Imaginary's existence in The Imaginary?|Being forgotten by their human creator|Hearing music|Seeing the sea|Touching a mirror
What kind of building shelters other Imaginaries in The Imaginary?|A library|A railway depot|A sports stadium|A hospital laboratory
Which character hunts Imaginaries in The Imaginary?|Mr. Bunting|Jinshi|Kiyoka Kudou|Minato Hinageshi'''),('Drifting Home','''What kind of building drifts across the sea in Drifting Home?|An apartment block|A castle|A lighthouse|A shopping mall
How do Kosuke and Natsume know each other in Drifting Home?|They grew up together|They met on an overseas flight|They work for the same newspaper|They are rival professional athletes
What was planned for the old apartment complex in Drifting Home?|Demolition|Conversion into a royal palace|Use as an airport terminal|Expansion into a football stadium
What is the mysterious boy in the old complex called in Drifting Home?|Noppo|Nagi|Hibiki|Souta
What do the children build to leave the flooding building in Drifting Home?|A raft|A hot-air balloon|A submarine|A cable car'''),('Bubble (2022 film)','''Which city is the setting of the 2022 anime film Bubble?|Tokyo|Kyoto|Osaka|Sapporo
Which activity is central to the young people's competitions in Bubble?|Parkour|Sumo wrestling|Ice hockey|Horse racing
What is the name of the talented parkour boy in Bubble?|Hibiki|Hodaka|Akira|Kosuke
What does Hibiki call the mysterious girl in Bubble?|Uta|Hina|Miyo|Suzu
What do the bubbles disrupt in the 2022 anime film Bubble?|Gravity|The passing of the seasons only|The order of the days of the week|The spelling of people's names'''),("Mary and the Witch's Flower",'''What colour is Mary's hair in Mary and the Witch's Flower?|Red|Blue|Green|Silver
What gives Mary temporary magical powers in Mary and the Witch's Flower?|A rare flower|A silver crown|A pearl necklace|A crystal sword
What does Mary ride to Endor College in Mary and the Witch's Flower?|A broomstick|A flying carpet|A winged horse|A giant swan
What kind of school is Endor College in Mary and the Witch's Flower?|A school for witches|A naval academy|A ballet school|A school for royal guards
What kind of animal is Tib in Mary and the Witch's Flower?|A cat|A fox|An owl|A rabbit'''),('Penguin Highway','''Which boy investigates the penguin mystery in the anime film Penguin Highway?|Aoyama|Hibiki|Rudger|Hodaka
Where does the mysterious woman work in Penguin Highway?|A dental office|A railway ticket office|A bakery|A fire station
What everyday object does the woman turn into a penguin in Penguin Highway?|A soda can|A pencil|A wristwatch|A school bag
Where does Aoyama record his observations in Penguin Highway?|A notebook|A ship's log|A wall calendar|A collection of postcards
Which studio animated the film Penguin Highway?|Studio Colorido|Studio Ghibli|Studio Ponoc|Science Saru'''),('Lu Over the Wall','''What kind of creature is Lu in Lu Over the Wall?|A mermaid|A forest spirit|A dragon|A talking fox
Which boy becomes friends with Lu in Lu Over the Wall?|Kai|Hodaka|Hibiki|Rudger
What helps Lu's fish fin turn into human legs in Lu Over the Wall?|Music|Snow|Moonlight alone|A magic ring
What is dangerous to Lu in Lu Over the Wall?|Direct sunlight|The sound of singing|Sea water|The sight of a fishing boat
What is Kai's band called in Lu Over the Wall?|SEIRÈN|Kessoku Band|B-Komachi|Sick Hack''')]
d=[]
for title,raw in groups:
 rows=raw.splitlines();assert len(rows)==5
 for line in rows:
  prompt,*answers=line.split('|');assert len(answers)==4
  d.append({'draftID':f'easy-31-{len(d)+1:03d}','categoryID':'31','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'rationale':'UNAPPROVED candidate; all four choices, actual anime canon, scope, grammar, accuracy, duplicates and source checks pending.','sourceURL':'https://en.wikipedia.org/wiki/'+urllib.parse.quote(title.replace(' ','_')),'reviewStatus':'draft_unreviewed'})
assert len(d)==100
(H/'draft.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('100 anime candidates drafted, none approved or published.')
