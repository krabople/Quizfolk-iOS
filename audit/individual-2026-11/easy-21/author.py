"""100 original accessible Sport candidates. Authoring does not approve them."""
import json,pathlib
H=pathlib.Path(__file__).parent
refs={
'archery':'https://www.worldarchery.sport/',
'fencing':'https://fie.org/',
'curling':'https://worldcurling.org/about/curling/',
'squash':'https://www.worldsquash.org/',
'badminton':'https://bwfbadminton.com/',
'netball':'https://netball.sport/',
'handball':'https://www.olympics.com/ioc/news/handball-game-rules-regulations-how-to-play',
'tabletennis':'https://www.ittf.com/',
'climbing':'https://www.thebmc.co.uk/',
'rowing':'https://worldrowing.com/',
'canoe':'https://www.canoeicf.com/',
'orienteering':'https://orienteering.sport/',
'discgolf':'https://www.pdga.com/',
'ultimate':'https://wfdf.sport/',
'hockey':'https://www.fih.hockey/',
'rugby':'https://passport.world.rugby/',
'volleyball':'https://www.fivb.com/',
'cricket':'https://www.lords.org/mcc/the-laws-of-cricket',
'tennis':'https://www.itftennis.com/',
'golf':'https://www.randa.org/',
}
text='''archery|In archery, what is a quiver used to hold?|Arrows|Bowstrings only|Target faces|Scorecards only
archery|What is the main purpose of fletching on an arrow?|Helping stabilise its flight|Making the bow easier to carry|Measuring the target distance|Protecting the archer's fingers
archery|Which item protects an archer's forearm from the bowstring?|An armguard|A finger tab|A quiver|A sight
archery|On a standard five-colour target-archery face, which colour is in the centre?|Gold|Blue|Black|White
archery|Which part of an archery bow does the archer draw back before releasing an arrow?|The string|The sight|The riser grip|The arrow rest
fencing|Which set names the three weapons used in Olympic fencing?|Foil, épée and sabre|Foil, javelin and lance|Épée, discus and sabre|Sabre, rapier and shot
fencing|What is the strip on which fencers compete called?|A piste|A crease|A rink|A fairway
fencing|Which protective item covers a fencer's face and head?|A fencing mask|A chest plastron|A glove|A shin guard
fencing|Which fencing weapon allows scoring with the edge as well as the point?|Sabre|Foil|Épée|All three equally
fencing|In fencing, what does a salute mainly express before a bout?|Respect towards the opponent and officials|A request for extra time|A claim that the bout has already been won|A demand to change the score
curling|Curling players slide stones across which surface?|Ice|Sand|Grass|Clay
curling|In curling, what is the circular target area called?|The house|The crease|The key|The crease line
curling|What do curling players use to sweep the ice in front of a stone?|Brushes or brooms|Hockey sticks|Tennis rackets|Golf clubs
curling|In curling, an end is best described as what?|A round in which the teams deliver their stones|The handle attached to a stone|The winner of the entire tournament|A player's final training session
curling|Which curling player normally directs the team's tactics?|The skip|The coxswain|The wicketkeeper|The libero
squash|In squash, a legal return must reach which wall before bouncing on the floor?|The front wall|Only the back wall|Only the left wall|Only the right wall
squash|What is the squash ball mainly made from?|Rubber|Cork|Solid wood|Leather stuffed with feathers
squash|In squash, what does the referee's call of let usually mean?|Replay the rally|Award two points to the server|End the match immediately|Replace the racket
squash|Which marked area must a squash server have one foot in contact with when serving?|A service box|The centre circle|The goal area|The penalty spot
squash|In squash, what is the low panel at the bottom of the front wall called?|The tin|The net|The crossbar|The backboard
badminton|In standard badminton singles, how many players are on each side of the net?|One|Two|Three|Four
badminton|In standard badminton doubles, how many players make up one pair?|Two|One|Three|Four
badminton|What separates the two sides of a badminton court?|A net|A solid wall|A water channel|A row of hurdles
badminton|Which piece of equipment is used to strike the shuttle in badminton?|A racket|A paddle with no strings|A club|A curved stick
badminton|In badminton, a shuttle that lands on a boundary line of the relevant court is judged how?|In|Out|Automatically a let|Automatically a service fault
netball|How many players from each team are normally on court in standard seven-a-side netball?|Seven|Five|Six|Nine
netball|Which netball positions are allowed to shoot for goal?|Goal Shooter and Goal Attack|Centre and Wing Attack|Goal Defence and Goal Keeper|Wing Defence and Centre
netball|What does a netball goal ring normally lack compared with a basketball hoop?|A backboard|A supporting post|A circular ring|A net
netball|In standard netball, how long may a player normally hold the ball before passing or shooting?|Three seconds|One second|Five seconds|Ten seconds
netball|After landing with the ball in netball, which movement is normally allowed while keeping the landing foot grounded?|Pivoting|Running several steps|Jumping forward repeatedly with the ball|Dribbling down the court
handball|How many players per team are normally on court in indoor handball, including the goalkeeper?|Seven|Five|Eight|Eleven
handball|In indoor handball, how many steps may a player normally take while holding the ball without dribbling?|Three|One|Five|Seven
handball|In indoor handball, how long may a player normally hold the ball without playing it?|Three seconds|One second|Eight seconds|Ten seconds
handball|What are indoor handball teams mainly trying to do to score?|Throw the ball into the opposing goal|Kick the ball over a crossbar|Strike the ball into a hole|Carry the ball across an end line
handball|In indoor handball, which player is normally permitted to stand inside their own goal area to defend?|The goalkeeper|Any defender|Only the team captain|Only a substitute
tabletennis|How many points normally win a standard table-tennis game, provided the player leads by two?|Eleven|Seven|Fifteen|Twenty-one
tabletennis|What must happen to a legal table-tennis singles serve before it reaches the receiver's side?|It must bounce on the server's half of the table|It must bounce on the floor|It must hit the receiver's racket first|It must touch a side wall
tabletennis|In table-tennis doubles, how do the two partners normally take shots during a rally?|They must alternate shots|Either partner may take every shot|Only the server may strike the ball|They must strike the ball together
tabletennis|What divides the two halves of a table-tennis table?|A net|A glass wall|A raised wooden board|A row of pegs
tabletennis|What is the main function of a table-tennis bat or racket?|Striking the ball over the net|Marking the service line|Measuring the table height|Keeping the score electronically
climbing|Which climbing discipline uses short routes above landing mats, normally without ropes?|Bouldering|Lead climbing|Abseiling|Ice climbing
climbing|In roped climbing, what does a belayer mainly manage?|The safety rope|The route's paint colour|The climber's scorecard|The timing of other climbers
climbing|What is a carabiner used for in climbing?|Connecting parts of the safety system|Measuring the cliff's height|Drying the climber's hands|Marking a route's difficulty
climbing|Why do climbers commonly use chalk on their hands?|To absorb moisture and improve grip|To make the rock softer|To mark each climb as completed|To increase the rope's elasticity
climbing|In lead climbing, what does the climber do with the rope as they ascend?|Clip it into protection points along the route|Leave it coiled at the foot of the wall|Use it only to measure the route|Tie it around each handhold
rowing|In sculling, how many oars does each rower normally use?|Two|One|Three|Four
rowing|In sweep rowing, how many oars does each rower normally use?|One|Two|Three|Four
rowing|In a coxed rowing boat, what is one main task of the coxswain?|Steering and coordinating the crew|Taking every rowing stroke|Judging all the other boats|Swimming behind the boat
rowing|In conventional racing rowing, which way do rowers face relative to the boat's direction of travel?|Backwards|Forwards|Always towards the bank|Always towards the finish officials
rowing|Which machine lets a rower train on land by simulating rowing strokes?|A rowing ergometer|A treadmill|A stationary bicycle|A ski lift
canoe|What kind of paddle is normally used in racing kayak events?|A double-bladed paddle|A single-bladed paddle|An oar fixed to the boat|A pole pushed against the riverbed
canoe|What kind of paddle is normally used in racing canoe events?|A single-bladed paddle|A double-bladed paddle|An oar fixed to the boat|A pair of hand paddles
canoe|In canoe slalom, competitors navigate a course marked by what?|Hanging gates|Floating basketball hoops|A row of diving boards|Moving goalposts
canoe|What is the main purpose of a helmet in white-water canoeing or kayaking?|Protecting the head|Measuring paddling speed|Providing the main source of buoyancy|Steering the boat
canoe|What is a buoyancy aid mainly designed to help a paddler do?|Stay afloat|Paddle faster in every current|Breathe underwater|Stop all river movement
orienteering|Which two navigation aids are traditionally central to orienteering?|A map and compass|A stopwatch and whistle only|A telescope and tripod|A ruler and calculator only
orienteering|In a standard orienteering course, what must competitors find in the required order?|Control points|Refreshment stalls only|Other competitors' homes|The tallest trees in the forest
orienteering|Why does an orienteer punch or electronically register at a control?|To record that they visited it|To change the map's scale|To stop every competitor's clock|To move the control to a new place
orienteering|On an orienteering map, what do contour lines mainly show?|The shape and height of the ground|The direction of the wind|The age of each tree|The number of competitors
orienteering|What does a map legend or key explain for an orienteer?|The meanings of map symbols|The finishing time of every competitor|The weather for the next month|The distance already run by every runner
discgolf|What is the target in most disc-golf holes?|A basket with hanging chains|A hole dug into the turf|A goal with a crossbar|A hoop mounted on a backboard
discgolf|In ordinary stroke-play disc golf, which total is better?|Fewer throws|More throws|More time spent on the course|More discs carried in a bag
discgolf|Where does play on a disc-golf hole begin?|The teeing area|Inside the target basket|The car park|Any neighbouring fairway
discgolf|In disc golf, what is a putt generally trying to do?|Get the disc into the nearby basket|Throw the disc back to the tee|Hit another player's disc|Send the disc beyond the next hole
discgolf|What do players throw in disc golf?|Flying discs|Golf balls|Beanbags|Shuttlecocks
ultimate|What object is passed between teammates in ultimate?|A flying disc|A rugby ball|A shuttlecock|A puck
ultimate|How does a team normally score a goal in ultimate?|Catch a pass in the attacking end zone|Kick the disc over a crossbar|Bounce the disc into a basket|Carry the disc around the whole field
ultimate|Once an ultimate player has established a pivot after catching the disc, what may they do?|Pivot and pass|Run downfield while carrying the disc|Bounce the disc while running|Hand the disc to an opponent to keep possession
ultimate|What normally happens after an incomplete pass in ultimate?|Possession changes to the other team|The passing team automatically scores|The match ends|The same team gets unlimited replacement throws
ultimate|Ultimate's Spirit of the Game places particular emphasis on what?|Fair play and players' responsibility for following the rules|Winning by any means|Avoiding all discussion of fouls|Leaving every decision to spectators
hockey|In standard outdoor field hockey, what is used to strike the ball?|A hockey stick|A racket|A club with a full circular face|A paddle fixed to a boat
hockey|Which side of an ordinary field-hockey stick is used to play the ball?|The flat side|Only the rounded side|Either side equally|Only the top of the handle
hockey|For a normal field-hockey goal to count, where must an attacker play the ball before it enters the goal?|Inside the shooting circle|Only from beyond the halfway line|Only from the corner flag|Only from outside the pitch
hockey|In field hockey, what is the D another name for?|The shooting circle|The centre spot|The substitution bench|The back of the goal
hockey|What is a goalkeeper mainly trying to prevent in field hockey?|The ball entering their goal|All passes across the halfway line|The opposition making substitutions|The referee stopping play
rugby|In rugby union, how many points is a try worth?|Five|Three|Two|One
rugby|In rugby union, how many points is a successful conversion worth?|Two|One|Three|Five
rugby|In rugby union, in which direction may a player normally throw a pass to a teammate?|Backwards or sideways|Forwards only|In any direction without restriction|Only vertically upwards
rugby|In standard fifteen-a-side rugby union, how many players per team start on the field?|Fifteen|Eleven|Thirteen|Seven
rugby|In rugby union, what is a lineout used for?|Restarting play after the ball goes into touch|Awarding a try without grounding the ball|Starting a penalty shoot-out|Deciding who wins a tied tournament
volleyball|In standard indoor volleyball, how many players from each team are on court?|Six|Four|Five|Seven
volleyball|In indoor volleyball, what is the main aim of an attacking spike?|Send the ball forcefully into the opponents' court|Throw the ball directly into a basket|Hold the ball until time expires|Kick the ball over the arena roof
volleyball|In indoor volleyball, what action starts a rally?|A serve|A face-off|A scrum|A centre bounce
volleyball|In indoor volleyball, what is a block mainly intended to stop?|An opponent's attack crossing the net|The referee seeing the court|Teammates changing positions|The match clock reaching zero
volleyball|Excluding a blocking contact, how many team hits are normally allowed to return the ball in indoor volleyball?|Three|Two|Four|Five
cricket|In cricket, how many legal deliveries normally make up an over?|Six|Four|Eight|Ten
cricket|In cricket, what is a duck?|A batter's dismissal without scoring a run|A ball hit for six|A match with no wickets|A delivery that bounces twice
cricket|In cricket, what is the wicketkeeper positioned behind?|The batter's wicket|The bowler's run-up|The boundary rope|The sightscreen only
cricket|In cricket, what does a batter normally use to protect their lower legs?|Batting pads|A fielding cap|A helmet visor|A wristband
cricket|In cricket, what is a boundary four?|A hit that reaches the boundary after touching the ground|A hit that clears the boundary without bouncing|Four wickets taken in an innings|Four consecutive maiden overs
tennis|In tennis scoring, what does love mean?|Zero|One|Fifteen|Forty
tennis|In an ordinary advantage-scoring tennis game, what score is called deuce?|Forty-all|Thirty-all|Fifteen-all|Game point with no reply
tennis|In tennis, what is a volley?|A shot hit before the ball bounces|A serve that hits the net and lands out|A shot played after two bounces|A score of six games each
tennis|In a standard tennis serve, which service box must the ball land in?|The diagonally opposite service box|Either service box chosen freely|The server's own service box|Only the area behind the receiver's baseline
tennis|In tennis, what is an ace?|A legal serve the receiver does not touch|A rally lasting more than twenty shots|A point awarded for a double fault|A shot that hits both net posts
golf|In golf, what does a birdie mean on a hole?|One stroke under par|One stroke over par|Two strokes over par|Exactly par
golf|In golf, what does a bogey mean on a hole?|One stroke over par|One stroke under par|Two strokes under par|Exactly par
golf|Which golf club is mainly designed for rolling the ball on the putting green?|A putter|A driver|A sand wedge|A three-wood
golf|In ordinary stroke-play golf, which total score wins?|The lowest number of strokes|The highest number of strokes|The most balls used|The greatest total distance walked
golf|What warning should a golfer shout if a struck ball may endanger someone?|Fore!|Love!|Let!|Howzat!'''
if __name__=='__main__':
 out=[]
 for line in text.splitlines():
  key,prompt,*answers=line.split('|');assert len(answers)==4
  out.append({'draftID':f'easy-21-{len(out)+1:03d}','categoryID':'21','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'rationale':'UNAPPROVED: individual meaning, sole correct offered option, grammar, sport/version scope, source relevance and duplicate review required. Reference homepages are provisional, not verified evidence.','sourceURL':refs[key],'reviewStatus':'draft_awaiting_author_final_check'})
 assert len(out)==100,len(out)
 (H/'draft.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print('100 UNAPPROVED Sport candidates; no bank changes.')
