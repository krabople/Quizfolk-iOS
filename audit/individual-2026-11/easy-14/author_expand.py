"""Add80 unapproved TV candidates to the existing20; final checks still required."""
import json,pathlib
H=pathlib.Path(__file__).parent
sources={
'ted':'https://tv.apple.com/us/show/ted-lasso/umc.cmc.vtoh0mn0xn7t3c643xqonfzy',
'severance':'https://www.apple.com/tv-pr/originals/severance/',
'wednesday':'https://www.netflix.com/tudum/articles/wednesday-character-cast-guide-season-1',
'squid':'https://www.netflix.com/tudum/articles/squid-game-season-2-cast',
'bridgerton':'https://www.netflix.com/tudum/articles/meet-bridgerton-cast-season-1',
'goodplace':'https://www.peacocktv.com/stream-tv/the-good-place',
'heartstopper':'https://www.netflix.com/tudum/articles/heartstopper-movie-alice-oseman-plot-news',
'derry':'https://www.channel4.com/press/news/channel-4-commissions-sitcom-set-nineties-northern-ireland',
'abbott':'https://abc.com/shows/abbott-elementary/about-the-show/1000',
'bear':'https://www.fxnetworks.com/shows/the-bear/cast',
'brooklyn':'https://www.peacocktv.com/stream-tv/brooklyn-nine-nine',
'murders':'https://press.hulu.com/shows/only-murders-in-the-building/',
'lupin':'https://www.netflix.com/tudum/articles/lupin-part-4-release-date-photos-news',
'taskmaster':'https://www.channel4.com/press/press-pack/taskmaster-series-22-press-pack',
'traitors':'https://studiolambert.com/project/take-part-the-traitors-uk/',
'crown':'https://www.netflix.com/tudum/articles/the-crown-season-1-recap',
'lastofus':'https://press.wbd.com/na/media-release/hbo-0/hbo-original-drama-series-last-us-debuts-january-15',
'moneyheist':'https://about.netflix.com/en/news/netflix-announces-that-the-world-of-money-heist-continues',
'downton':'https://www.peacocktv.com/watch-online/tv/downton-abbey/7560296579355862112/seasons/1',
'mando':'https://www.starwars.com/databank/the-mandalorian',
}
rows='''ted|Who plays the title character in Ted Lasso?|Jason Sudeikis|Steve Carell|Paul Rudd|Will Ferrell
ted|Before moving to England in Ted Lasso, Ted coached which sport in the United States?|American football|Ice hockey|Baseball|Basketball
ted|Which sport does AFC Richmond play in Ted Lasso?|Football (soccer)|Rugby union|Cricket|Basketball
ted|What is the name of the fictional club Ted is hired to manage at the start of Ted Lasso?|AFC Richmond|AFC Wimbledon|West Ham United|Crystal Palace
severance|Which company employs Mark Scout in Severance?|Lumon Industries|Waystar Royco|Dunder Mifflin|Pied Piper
severance|Who plays Mark Scout in Severance?|Adam Scott|Paul Rudd|Jason Bateman|Bill Hader
severance|In Severance, the severance procedure separates employees' memories of which two parts of life?|Work and personal life|Childhood and adulthood|Dreams and nightmares|Weekdays and weekends
severance|What type of workplace is the main setting of Severance?|An office|A hospital|A police station|A hotel
wednesday|Who plays Wednesday Addams in Netflix's Wednesday?|Jenna Ortega|Millie Bobby Brown|Sadie Sink|Anya Taylor-Joy
wednesday|Which school does Wednesday attend in Netflix's Wednesday?|Nevermore Academy|Hogwarts|Moordale Secondary|Sunnydale High
wednesday|Wednesday, Morticia and Gomez belong to which fictional family?|The Addams family|The Munsters|The Simpsons|The Flintstones
wednesday|What is Thing, Wednesday's unusual companion in Netflix's Wednesday?|A disembodied hand|A talking skull|A flying book|A pet raven
squid|Squid Game was originally produced in which country?|South Korea|Japan|Thailand|China
squid|What player number does Seong Gi-hun wear in Squid Game?|456|001|067|218
squid|What colour tracksuits do the contestants wear in the original Squid Game?|Green|Red|Yellow|Purple
squid|Which children's game is the first main contest in season one of Squid Game?|Red Light, Green Light|Musical Chairs|Hide-and-Seek|Hopscotch
bridgerton|In which city do the Bridgerton family mainly take part in the social season?|London|Paris|Vienna|Rome
bridgerton|Bridgerton's first season is set during which period of British history?|The Regency|The Tudor period|The Elizabethan era|The Second World War
bridgerton|Which pen name appears on the scandal sheets in Bridgerton?|Lady Whistledown|Lady Featherington|Lady Danbury|Lady Grantham
bridgerton|Whose novels were adapted into the television series Bridgerton?|Julia Quinn|Jane Austen|Georgette Heyer|Philippa Gregory
goodplace|At the start of The Good Place, Eleanor discovers she has arrived in what kind of setting?|An afterlife|A boarding school|A military base|A space colony
goodplace|Who plays Eleanor Shellstrop in The Good Place?|Kristen Bell|Tina Fey|Amy Poehler|Zooey Deschanel
goodplace|Who plays Michael in The Good Place?|Ted Danson|Kelsey Grammer|John Lithgow|Steve Martin
goodplace|In The Good Place, Chidi gives Eleanor lessons in which subject?|Ethics|Chemistry|Architecture|Music
heartstopper|Who created the graphic novels on which Heartstopper is based?|Alice Oseman|Suzanne Collins|Malorie Blackman|Holly Jackson
heartstopper|Who plays Nick Nelson in Heartstopper?|Kit Connor|Joe Locke|Asa Butterfield|Louis Partridge
heartstopper|Who plays Charlie Spring in Heartstopper?|Joe Locke|Kit Connor|Tom Holland|Freddie Highmore
heartstopper|Which school sport does Nick Nelson play in Heartstopper?|Rugby|Basketball|Cricket|Ice hockey
derry|Derry Girls is set in which part of the United Kingdom?|Northern Ireland|Wales|Scotland|England
derry|Derry Girls is mainly set during which decade?|The 1990s|The 1960s|The 1970s|The 2010s
derry|Who created and wrote Derry Girls?|Lisa McGee|Sharon Horgan|Phoebe Waller-Bridge|Michaela Coel
derry|The central young characters in Derry Girls are primarily what?|School friends|Hospital doctors|Police detectives|Law-firm partners
abbott|In which US city is Abbott Elementary set?|Philadelphia|Chicago|Boston|Seattle
abbott|What is the main occupation of the central staff in Abbott Elementary?|Teaching|Nursing|Policing|Journalism
abbott|Who plays Janine Teagues in Abbott Elementary?|Quinta Brunson|Issa Rae|Janelle James|Ayo Edebiri
abbott|Who is the school principal in Abbott Elementary?|Ava Coleman|Janine Teagues|Barbara Howard|Melissa Schemmenti
bear|In which US city is The Bear mainly set?|Chicago|New York City|Los Angeles|Miami
bear|What is Carmy's profession at the start of The Bear?|Chef|Architect|Lawyer|Journalist
bear|Who plays Carmy in The Bear?|Jeremy Allen White|Paul Mescal|Austin Butler|Aaron Taylor-Johnson
bear|Who plays Sydney Adamu in The Bear?|Ayo Edebiri|Quinta Brunson|Issa Rae|Janelle James
brooklyn|Brooklyn Nine-Nine is set in which city?|New York City|Chicago|Boston|San Francisco
brooklyn|The main characters in Brooklyn Nine-Nine work in which profession?|Police work|Medicine|Journalism|Firefighting
brooklyn|Who plays Jake Peralta in Brooklyn Nine-Nine?|Andy Samberg|Bill Hader|Jason Sudeikis|Adam Scott
brooklyn|What is the surname of the captain played by Andre Braugher in Brooklyn Nine-Nine?|Holt|Peralta|Boyle|Jeffords
murders|What is the name of the main apartment building in Only Murders in the Building?|The Arconia|The Dakota|The Plaza|The Savoy
murders|Who plays Mabel Mora in Only Murders in the Building?|Selena Gomez|Demi Lovato|Miley Cyrus|Ariana Grande
murders|What do the central trio create together in Only Murders in the Building?|A true-crime podcast|A restaurant review magazine|A travel vlog|A gardening television show
murders|In which city is the first season of Only Murders in the Building mainly set?|New York City|Boston|Chicago|San Francisco
lupin|What is the name of the main character played by Omar Sy in Lupin?|Assane Diop|Luther Stickell|Leroy Jethro Gibbs|Frank Martin
lupin|Who plays Assane Diop in Lupin?|Omar Sy|Idris Elba|Daniel Kaluuya|John Boyega
lupin|Netflix's Lupin is primarily set in which country?|France|Italy|Germany|Portugal
lupin|How is Assane Diop's criminal role best described in Lupin?|A gentleman thief|A drug kingpin|A contract killer|A counterfeiter of banknotes
taskmaster|Who is the Taskmaster in the original UK television series?|Greg Davies|Alex Horne|Richard Ayoade|David Mitchell
taskmaster|Who acts as the Taskmaster's assistant in the original UK series?|Alex Horne|Greg Davies|Lee Mack|Bob Mortimer
taskmaster|How many contestants usually compete in a regular full series of the UK Taskmaster?|Five|Three|Four|Six
taskmaster|The main trophy in the UK Taskmaster is a golden sculpture of which part of Greg Davies?|His head|His hand|His foot|His knee
traitors|Who hosts the original BBC version of The Traitors?|Claudia Winkleman|Davina McCall|Emma Willis|Alison Hammond
traitors|The castle used for the BBC version of The Traitors is in which country?|Scotland|Wales|England|Northern Ireland
traitors|Which group secretly chooses players to eliminate in The Traitors?|The Traitors|The Faithful|The audience|The contestants' families
traitors|How do contestants normally choose someone to banish at the Round Table in The Traitors?|By voting|By drawing lots|By racing|By answering a trivia question
crown|Which monarch's reign is the main focus of The Crown?|Elizabeth II|Victoria|Elizabeth I|Mary I
crown|The Crown mainly follows the royal family of which country?|The United Kingdom|Sweden|Spain|Denmark
crown|Who plays the young Elizabeth in the first season of The Crown?|Claire Foy|Olivia Colman|Imelda Staunton|Vanessa Kirby
crown|Who plays Prince Philip in the first season of The Crown?|Matt Smith|Tobias Menzies|Jonathan Pryce|Jared Harris
lastofus|The television series The Last of Us was adapted from what?|A video game|A stage musical|A radio comedy|A newspaper comic strip
lastofus|Who plays Joel in the first season of The Last of Us?|Pedro Pascal|Oscar Isaac|Diego Luna|Javier Bardem
lastofus|Who plays Ellie in The Last of Us?|Bella Ramsey|Maisie Williams|Kaitlyn Dever|Millie Bobby Brown
lastofus|Joel and Ellie travel across which country in the first season of The Last of Us?|The United States|Canada|Australia|Japan
moneyheist|What colour jumpsuits are worn by the main heist crew in the original Money Heist?|Red|Green|Yellow|Blue
moneyheist|The masks in the original Money Heist are modelled on which artist?|Salvador Dalí|Pablo Picasso|Vincent van Gogh|Andy Warhol
moneyheist|What title is used by the mastermind who organises the original Money Heist?|The Professor|The Captain|The Baron|The Judge
moneyheist|Tokyo, Berlin and Denver are used as character code names in Money Heist. What do these names have in common?|They are cities|They are rivers|They are planets|They are mountains
downton|What is the surname of the aristocratic family at the centre of Downton Abbey?|Crawley|Bridgerton|Shelby|Roy
downton|The fictional Downton Abbey estate is in which English county?|Yorkshire|Cornwall|Kent|Devon
downton|Alongside the aristocratic family, whose lives are a major focus of Downton Abbey?|Their household staff|A hospital's doctors|Rival police forces|Presidential advisers
downton|Who plays Violet, the Dowager Countess of Grantham, in Downton Abbey?|Maggie Smith|Judi Dench|Helen Mirren|Julie Andrews
mando|What is the personal name of the title character in The Mandalorian?|Din Djarin|Cassian Andor|Poe Dameron|Boba Fett
mando|What is Din Djarin's main occupation when The Mandalorian begins?|Bounty hunter|Senator|Moisture farmer|Starfighter mechanic
mando|Which young foundling does Din Djarin protect in The Mandalorian?|Grogu|Omega|Ezra|Jacen
mando|Which metal is used for Din Djarin's distinctive armour in The Mandalorian?|Beskar|Vibranium|Adamantium|Unobtainium'''
if __name__=='__main__':
 d=json.loads((H/'draft.json').read_text(encoding='utf8'));assert len(d)==20
 for line in rows.splitlines():
  key,prompt,*answers=line.split('|');assert len(answers)==4
  n=len(d)+1;d.append({'draftID':f'easy-14-{n:03d}','categoryID':'14','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'rationale':'UNAPPROVED: individual source/meaning/answer/grammar/category/overlap checks still required.','sourceURL':sources[key],'reviewStatus':'draft_awaiting_author_final_check'})
 assert len(d)==100
 (H/'draft.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('100 unapproved TV candidates; no final approvals or bank publication yet')
