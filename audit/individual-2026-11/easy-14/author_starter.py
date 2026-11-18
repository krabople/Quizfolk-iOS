"""First20 TV candidates, NOT an approved or complete100-question batch."""
import json,pathlib
H=pathlib.Path(__file__).parent
rows='''miniseries|What is a television miniseries?|A series intended to tell its story in a limited number of episodes|A television programme with no sound|A channel showing only advertisements|A live broadcast with no script
cliffhanger|What is a cliffhanger at the end of a television episode?|An unresolved situation that creates suspense about what happens next|A list of the programme's production staff|A summary that resolves every storyline|A recording error that removes the sound
spin-off|What is a television spin-off?|A new programme developed from an existing programme or its characters|An episode shown again without changes|A broadcast accidentally played backwards|An advertisement placed after the credits
rerun|What is a rerun of a television programme?|A repeat showing of an episode already broadcast|The first public showing of a brand-new episode|A rehearsal that is never recorded|A trailer for a future series
syndication|In television, what does syndication allow?|A programme to be sold or licensed to multiple broadcasters|Only one household to watch a broadcast|All episodes to be deleted after one showing|A programme to be shown without any legal rights
sitcom|The word sitcom is short for what?|Situation comedy|Silent commentary|Simultaneous competition|Single-camera communication
soap-opera|Which description best fits a television soap opera?|An ongoing drama following the lives and relationships of recurring characters|A programme teaching only soap-making|A one-off live opera performance|A daily weather bulletin
docuseries|What is a docuseries?|A documentary presented as a series of episodes|A drama in which every character is a doctor|A collection of television advertisements|A series broadcast without pictures
telecast|What does it mean to telecast an event?|To broadcast it on television|To turn it into a printed book|To perform it without an audience|To record its sound for radio only
watershed|In UK television scheduling, what does the watershed concern?|When programmes unsuitable for children may be shown|When every television transmitter shuts down|When weather forecasts must be broadcast|When programmes must switch to black and white
prime-time|What does prime time generally refer to in television?|The period when the largest audiences are expected to watch|Only the first minute of any programme|The time needed to repair a television|Only programmes shown before sunrise
closed-captioning|What does closed captioning provide for television viewers?|Optional on-screen text representing speech and relevant sounds|A brighter picture with no text|A camera view from behind the television|A recording of the programme's production budget
showrunner|What is a television showrunner generally responsible for?|Overseeing a series' creative direction and production|Delivering televisions to shops|Measuring the running speed of actors|Choosing the batteries for remote controls
finale|What is a season finale?|The final episode of a television season|The first advertisement before a series begins|A daily rehearsal before filming|An episode that has never been completed
premiere|What is a television season premiere?|The first episode shown in a new season|The final commercial break of the year|A repeat of every previous season|A private costume fitting for the cast
talk-show|What is a talk show mainly built around?|Conversations and interviews led by a host|Silent demonstrations without speech|Only live sporting competition|An uninterrupted sequence of advertisements
game-show|What do contestants normally do on a television game show?|Compete in games or answer questions|Read the news as full-time presenters|Repair the broadcaster's transmitters|Choose the channel's annual accounts
infomercial|What is an infomercial?|A television advertisement presented like a longer programme|A news bulletin with no commercial content|An emergency announcement from the police|A programme's list of cast members
simulcast|What is a simulcast?|The same programme broadcast at the same time through different outlets|A programme broadcast without any cameras|A repeat shown exactly one year later|A programme watched only by its director
remote-control|What lets a viewer change television channels without touching the television itself?|A remote control|A camera tripod|A microphone stand|An aerial extension pole'''
if __name__=='__main__':
 out=[]
 for i,line in enumerate(rows.splitlines(),1):
  key,prompt,*answers=line.split('|')
  assert len(answers)==4
  out.append({'draftID':f'easy-14-{i:03d}','categoryID':'14','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'rationale':'UNAPPROVED: source, wording, all options, category and global concept overlap still require final individual review.','sourceURL':'https://dictionary.cambridge.org/dictionary/english/'+key,'reviewStatus':'draft_awaiting_author_final_check'})
 (H/'draft.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('20 unapproved TV candidates;80 more candidates still needed')
