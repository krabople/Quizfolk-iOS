"""100 beginner-focused game candidates; NONE approved by authoring/retrieval."""
import json,pathlib
H=pathlib.Path(__file__).parent
sources={
'among':'https://www.innersloth.com/games/among-us/',
'fall':'https://www.fallguys.com/en-US',
'fortnite':'https://www.fortnite.com/',
'minecraft':'https://www.minecraft.net/en-us/about-minecraft',
'roblox':'https://corp.roblox.com/parents/',
'stardew':'https://www.stardewvalley.net/about/',
'animal':'https://animalcrossing.nintendo.com/new-horizons/',
'overcooked':'https://www.team17.com/games/overcooked-2/',
'goose':'https://goose.game/',
'powerwash':'https://store.steampowered.com/app/1290000/PowerWash_Simulator/',
'stray':'https://store.steampowered.com/app/1332010/Stray/',
'ittakes':'https://www.ea.com/games/it-takes-two',
'hollow':'https://www.hollowknight.com/',
'cuphead':'https://www.cupheadgame.com/',
'portal':'https://store.steampowered.com/app/620/Portal_2/',
'beat':'https://www.beatsaber.com/',
'splatoon':'https://www.nintendo.com/us/store/products/splatoon-3-switch/',
'kart':'https://www.nintendo.com/us/store/products/mario-kart-8-deluxe-switch/',
'zelda':'https://www.zelda.com/tears-of-the-kingdom/',
'pokemon':'https://scarletviolet.pokemon.com/en-us/',
}
terms='''non-player-character|What does NPC stand for in a video-game world?|Non-player character|New playable character|Network player code|Next power challenge
dlc|In video games, DLC stands for what?|Downloadable content|Digital level counter|Direct local connection|Dual language control
health|What does an HP bar usually represent in a game?|Health or hit points|Internet connection speed|Distance across the map|Frames displayed per second
experience-point|What does XP usually stand for when a character progresses through levels?|Experience points|Extra powers|Exclusive player|Extreme performance
fps|When a game-performance display reports FPS, what is it measuring?|Frames per second|Files per save|Fights per session|Friends per server
role-playing-game|As a video-game genre, RPG stands for what?|Role-playing game|Racing performance guide|Random player group|Realistic puzzle generator
mmorpg|What is the MMO part of MMORPG short for?|Massively multiplayer online|Manual movement only|Multiple maps offline|Maximum mission order
co-op|In co-op play, players generally do what?|Work together towards a shared goal|Always compete to eliminate one another|Take turns being the only person allowed to play|Each play an unrelated single-player game
cross-play|What does cross-play allow in a multiplayer game?|People on different supported platforms to play together|A player to skip every level|Every game to work without an internet connection|A game to repair a damaged controller
checkpoint|What is the main purpose of a checkpoint in many video games?|Providing a recent point to restart from after failure|Changing the game's language|Increasing the screen's physical size|Installing a new graphics card
respawn|What does it mean for a character to respawn?|Reappear in the game world after being defeated|Permanently delete the player's account|Change the screen resolution|Finish downloading an update
tutorial|What is the main purpose of a game's tutorial?|Teaching the basic controls and mechanics|Listing only the production staff|Replacing the entire story with advertisements|Displaying the publisher's accounts
open-world|What is a common feature of an open-world game?|A large environment that players can explore relatively freely|A requirement that every location be visited in one fixed order|A complete absence of computer-controlled characters|A rule that no progress can ever be saved
save|What is a save-game file mainly used to preserve?|The player's progress or game state|Only the artwork on the game's box|The physical condition of the controller|The console's purchase receipt
autosave|Which feature records game progress without the player manually choosing Save?|Autosave|Photo mode|Fast travel|Split-screen
mod|When customising a PC game, what does a mod usually mean?|A modification that changes or adds to the game|A monthly internet subscription|A hardware warranty|A permanent ban from a server
cosmetic|An item described as purely cosmetic is intended to change what?|Appearance|Attack damage|Maximum health|The number of levels available
emote|What does an avatar's emote usually do?|Perform an expressive gesture or animation|Permanently increase attack power|Download a new map|Change the game's difficulty setting
quest|What does a quest log usually help a player track?|Tasks and objectives|The console's electricity bill|The monitor's colour calibration|The number of screws in a controller
split-screen|What does split-screen multiplayer usually let people do?|Play using separate views on the same display|Play only on separate consoles in separate countries|View the credits instead of the game|Automatically complete every multiplayer challenge'''
games='''among|In Among Us, which role is secretly trying to eliminate the crew?|The Impostor|The Crewmate|The Scientist|The Guardian Angel
among|What do Crewmates complete around the map in Among Us?|Tasks|Race laps|Restaurant orders|Football fixtures
among|After discussing suspicions in Among Us, how can the group eject a suspected Impostor?|By voting|By buying a ticket|By rolling dice|By winning a footrace
among|The Skeld map in Among Us is set mainly aboard what?|A spaceship|A cruise liner|A steam train|A submarine
fall|What kind of challenges are central to Fall Guys?|Colourful obstacle courses|Realistic flight missions|Historical war campaigns|Deep-sea diving expeditions
fall|Fall Guys contestants are often compared to which sweets because of their shape?|Jelly beans|Candy canes|Chocolate coins|Lollipops
fall|In a standard Fall Guys race round, what are players trying to reach?|The finish line|A hospital ward|A radio station|A courtroom
fall|What happens to players who fail to qualify in an elimination round of Fall Guys?|They are eliminated from that show|They automatically win the final|They become the game's host|They choose the next world champion
fortnite|In Fortnite Battle Royale, what is the usual aim for a player or team?|Be the last one remaining|Deliver the most newspaper subscriptions|Run a hospital|Complete a music album
fortnite|What happens to the safe area as the Storm advances in a standard Fortnite Battle Royale match?|It becomes smaller|It permanently covers the whole island|It moves to another planet|It becomes a menu screen
fortnite|What is Fortnite's virtual currency called?|V-Bucks|Robux|Minecoins|Bells
fortnite|In Fortnite's building modes, what is a pickaxe mainly used to harvest?|Building materials|Only musical notes|Only trophies|Only racing fuel
minecraft|Which Minecraft tool is particularly suited to chopping wood?|An axe|A shovel|A hoe|A fishing rod
minecraft|Which Minecraft block is used to smelt ore using fuel?|A furnace|A chest|A bookshelf|A loom
minecraft|Which item can a player use to sleep and set a respawn point in Minecraft's Overworld?|A bed|A chest|A crafting table|A cauldron
minecraft|Which of these Minecraft animals can normally be sheared for wool?|A sheep|A pig|A cow|A chicken
roblox|What is Roblox's virtual currency called?|Robux|V-Bucks|Bells|Minecoins
roblox|What is Roblox Studio mainly used for?|Creating Roblox games and experiences|Recording household electricity use|Repairing a computer screen|Printing school reports
roblox|On Roblox, what is a player's avatar?|Their in-game representation|Their internet service provider|Their computer's serial number|Their monthly electricity bill
roblox|Much of the playable content on Roblox is created by whom?|Its community of creators|Only television newsreaders|Only airline pilots|Only professional football referees
stardew|At the start of Stardew Valley, the player inherits a farm from which relative?|Their grandfather|Their aunt|Their cousin|Their sister
stardew|What is the name of the main nearby town in Stardew Valley?|Pelican Town|Pallet Town|Pewter City|Raccoon City
stardew|What generally needs to happen to planted crops each day so they can grow in Stardew Valley?|They need watering|They need painting|They need wrapping in paper|They need moving to a new field
stardew|What can the player catch with a fishing rod in Stardew Valley?|Fish|Butterflies only|Birds only|Rabbits only
animal|Where does the player begin building a community in Animal Crossing: New Horizons?|On a deserted island|On a space station|Inside a medieval castle|On a submarine
animal|Which company runs the airport in Animal Crossing: New Horizons?|Dodo Airlines|Nook Railways|K.K. Airways|Able Sisters Aviation
animal|What are Nook Miles used as in Animal Crossing: New Horizons?|A reward currency earned for activities|A measurement of a real aircraft's fuel|The island's clock settings|The player's real bank balance
animal|What lets players make tools and furniture from recipes in Animal Crossing: New Horizons?|DIY crafting|A racing tournament|A music audition|A football transfer
overcooked|What is the main job of players acting as chefs in Overcooked 2?|Prepare and serve dishes|Build spacecraft|Manage a football squad|Run a detective agency
overcooked|Overcooked 2 is best known for which style of multiplayer?|Cooperative cooking|Competitive kart racing|Military team shooting|Turn-based card battles
overcooked|How many people can normally play together in Overcooked 2?|Up to four|Up to two|Up to six|Up to eight
overcooked|Which action can help chefs pass ingredients across a gap in Overcooked 2?|Throwing ingredients|Rewinding the entire level|Turning into a bird|Making the kitchen invisible
goose|The main setting of Untitled Goose Game is what kind of place?|A village|A space station|An underwater city|A military bunker
goose|Which of these activities is typical of the goose's mischief in Untitled Goose Game?|Stealing and moving people's possessions|Piloting a fighter jet|Managing a football club|Mining diamonds underground
goose|Untitled Goose Game combines puzzles with which broad style of play?|Stealth and mischief|Realistic motor racing|Military flight simulation|Competitive card collecting
goose|How many geese can players control together in Untitled Goose Game's local co-op mode?|Two|Three|Four|Six
powerwash|Which fictional town is a main setting of PowerWash Simulator?|Muckingham|Raccoon City|Silent Hill|Pallet Town
powerwash|In PowerWash Simulator, what removes dirt from surfaces?|Pressurised water|Laser beams|Explosives|A magnetic field
powerwash|What do different nozzles mainly change in PowerWash Simulator?|The shape and spread of the water jet|The game's story language|The player's character name|The number of save slots
powerwash|In PowerWash Simulator's co-op mode, players can work together to do what?|Clean locations|Race motorbikes|Build a space station|Manage a football league
stray|What kind of animal does the player control in Stray?|A cat|A dog|A fox|A rabbit
stray|Which small drone befriends the cat in Stray?|B-12|R2-D2|WALL-E|Clank
stray|Many of the inhabitants of the city in Stray are what?|Robots|Dinosaurs|Giants|Mermaids
stray|What is the cat ultimately trying to escape from in Stray?|A forgotten city|A racing championship|A shopping-centre car park|A school sports day
ittakes|How many players is It Takes Two designed to be played by?|Two|One|Three|Four
ittakes|What are the names of the main playable couple in It Takes Two?|Cody and May|Joel and Ellie|Mario and Peach|Nathan and Elena
ittakes|What are Cody and May transformed into in It Takes Two?|Dolls|Dragons|Race cars|Spaceships
ittakes|What must the two players repeatedly do to overcome challenges in It Takes Two?|Cooperate|Avoid all communication|Always work on unrelated levels|Take turns uninstalling the game
hollow|What is the name of the fallen kingdom explored in Hollow Knight?|Hallownest|Hyrule|Azeroth|Tamriel
hollow|The player character's main weapon in Hollow Knight is called what?|A Nail|A lightsaber|A rocket launcher|A trident
hollow|Many inhabitants of Hollow Knight's world resemble which creatures?|Insects and other bugs|Large sea mammals|Farm cattle|Birds of prey
hollow|Hollow Knight is primarily presented from which viewpoint?|Side-on in 2D|Through a realistic cockpit|From a fixed television news desk|As a spreadsheet of stock prices
cuphead|Cuphead's visual style was strongly inspired by cartoons from which decade?|The 1930s|The 1960s|The 1980s|The 2000s
cuphead|Who is Cuphead's playable partner in the original game's two-player mode?|Mugman|Luigi|Tails|Diddy Kong
cuphead|A major part of Cuphead involves fighting what?|Boss enemies|Court cases|Football fixtures|Stock-market crashes
cuphead|To whom do Cuphead and Mugman owe a debt in the game's main story?|The Devil|Bowser|Dr. Eggman|King Dedede
portal|Which company runs the testing facilities in Portal 2?|Aperture Science|Black Mesa|Umbrella Corporation|Abstergo Industries
portal|What does the portal gun mainly create in Portal 2?|Two connected portals|An army of friendly soldiers|A supply of food|A permanent weather forecast
portal|Who is the main human player character in Portal 2's single-player story?|Chell|Alyx Vance|Samus Aran|Lara Croft
portal|What are the names of the two playable robots in Portal 2's co-op campaign?|Atlas and P-body|Ratchet and Clank|C-3PO and R2-D2|Wallace and Gromit
beat|In Beat Saber, players mainly slice blocks in time with what?|Music|A weather forecast|A television news bulletin|A football commentary
beat|What does a direction arrow on a standard Beat Saber block tell the player?|Which direction to cut it|Which country made the music|How to change the headset's battery|Which menu language to select
beat|In a standard two-colour Beat Saber level, what should players normally match to a block's colour?|The corresponding saber|Their avatar's shoe size|Their real postcode|The headset's purchase date
beat|Beat Saber is designed primarily for which type of gaming hardware?|Virtual-reality headsets|Steering-wheel controllers|Fishing-rod controllers|Flight-simulator throttles
splatoon|In a standard Turf War in Splatoon 3, teams mainly compete to cover ground with what?|Their own colour of ink|Sand|Snow|Grass seeds
splatoon|In Splatoon 3, changing into swim form helps players move through what?|Their own team's ink|Only clean water|Only enemy ink|Only bare concrete
splatoon|The main playable characters in Splatoon 3 include Inklings and which other group?|Octolings|Goombas|Koopas|Gorons
splatoon|What kind of game is Splatoon 3 primarily?|A colourful team shooter|A realistic driving simulator|A farming simulator|A card-based solitaire game
kart|What does a banana item usually make another kart do on contact in Mario Kart 8 Deluxe?|Spin out|Become invincible|Steal an item|Shrink in size
kart|What is a key feature of a green shell in Mario Kart 8 Deluxe?|It travels without automatically homing in on a racer|It always seeks the racer in first place|It makes the user invisible|It revives every racer who has finished
kart|What does a red shell usually do when thrown forwards in Mario Kart 8 Deluxe?|Home in on a racer ahead|Automatically refill everyone's coins|Make all karts smaller|Open a new course
kart|Which racer does the blue Spiny Shell mainly target in Mario Kart 8 Deluxe?|The racer in first place|The racer in last place|Only the racer carrying the most coins|Only a racer using a motorbike
zelda|What does Ultrahand let Link do in Tears of the Kingdom?|Move and attach objects to build things|Turn every enemy into a friend|Automatically finish every shrine|Change the game's spoken language
zelda|What does Fuse let Link do in Tears of the Kingdom?|Combine materials with weapons or shields|Permanently remove all enemies|Reset every completed quest|Change the console's screen resolution
zelda|What does Ascend let Link do in Tears of the Kingdom?|Pass upwards through a suitable ceiling|Travel only down waterfalls|Summon every horse in Hyrule|Replace all armour with a single button press
zelda|What does Recall do to a selected moving object in Tears of the Kingdom?|Reverses its movement through time|Changes it into a cooking pot|Permanently doubles its weight|Makes it stop existing
pokemon|Which region is the main setting of Pokémon Scarlet and Violet?|Paldea|Kanto|Johto|Sinnoh
pokemon|What is Sprigatito's type as a first partner in Pokémon Scarlet and Violet?|Grass|Fire|Water|Electric
pokemon|The first-partner Pokémon Quaxly resembles which bird?|A duck|An owl|A penguin|An eagle
pokemon|Which legendary Pokémon is the main ride companion in Pokémon Scarlet?|Koraidon|Miraidon|Rayquaza|Lugia'''
if __name__=='__main__':
 out=[]
 for line in (terms+'\n'+games).splitlines():
  key,prompt,*answers=line.split('|');assert len(answers)==4
  n=len(out)+1
  out.append({'draftID':f'easy-15-{n:03d}','categoryID':'15','difficulty':'easy','prompt':prompt,'answers':answers,'correctIndex':0,'rationale':'UNAPPROVED: every fact, option, grammar, category, source and overlap must be individually checked. Several initial distractors require improvement.','sourceURL':sources.get(key,'https://dictionary.cambridge.org/dictionary/english/'+key),'reviewStatus':'draft_awaiting_author_final_check'})
 assert len(out)==100,len(out)
 (H/'draft.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('100 UNAPPROVED Video Games candidates; no source retrieval or automatic approval claimed')
