import SwiftUI

struct TopicLevelProgress:View {
 let topic:Topic;let xp:Int
 private var level:Int {1+xp/300}
 var body:some View {
  VStack(alignment:.leading,spacing:7){HStack{Text("Level \(level) in \(topic.name)").font(.subheadline.bold());Spacer();Text("\(xp) XP").font(.caption)};ProgressView(value:Double(xp%300),total:300).tint(topic.tint);Text("\(300-xp%300) XP to level \(level+1)").font(.caption).foregroundStyle(.secondary)}.accessibilityElement(children:.combine)
 }
}
struct PlayerRow:View {
 let card:PlayerCard
 var body:some View {
  HStack(spacing:12){PlayerPortrait(name:card.name,avatar:card.avatar,size:48);VStack(alignment:.leading,spacing:4){Text(card.name).font(.headline);Text(card.title).font(.caption).foregroundStyle(Color.coral);Text(card.sharedTopics.isEmpty ? "\(card.stats.matches) completed duels":"\(card.sharedTopics.count) shared interests · \(card.stats.matches) duels").font(.caption).foregroundStyle(.secondary)};Spacer();Image(systemName:"chevron.right").font(.caption).foregroundStyle(.secondary)}.foregroundStyle(Color.ink).padding(15).background(.white,in:RoundedRectangle(cornerRadius:16))
 }
}
struct PeopleView:View {
 @EnvironmentObject var store:QuizStore
 @State private var query=""
 @State private var mode="discover"
 @State private var loading=false
 @State private var blockedSheet=false
 var body:some View {
  NavigationStack {
   ScrollView {
    BrandHeader(title:"Your kind of people.",subtitle:"Meet minds that share your interests.")
    VStack(spacing:16) {
     Picker("People section",selection:$mode){Text("Discover").tag("discover");Text("Following").tag("following");Text("Followers").tag("followers");Text("Activity").tag("activity")}.pickerStyle(.segmented)
     if mode != "activity" {TextField("Find a player by name",text:$query).textFieldStyle(.roundedBorder).autocorrectionDisabled().textInputAutocapitalization(.never).accessibilityIdentifier("playerSearch")}
     if loading {ProgressView("Finding people…")}
     if mode=="activity" {activityContent}
     else {
      if store.people.isEmpty && !loading {ContentUnavailableView("No players found",systemImage:"person.2",description:Text("Search for a friend’s player name. Following someone makes it easy to challenge them again."))}
      ForEach(store.people){card in NavigationLink{PublicPlayerView(playerID:card.id)}label:{PlayerRow(card:card)}.buttonStyle(.plain).accessibilityIdentifier("player-\(card.id)")}
     }
     if let error=store.socialError {Text(error).font(.caption).foregroundStyle(.red)}
     Button("Blocked players"){blockedSheet=true}.font(.caption).padding(.top,8)
    }.padding(.horizontal,20).padding(.bottom,24)
   }.background(Color.canvas).toolbar(.hidden,for:.navigationBar).refreshable{await reload()}
  }.task(id:query+"|"+mode){do {try await Task.sleep(for:.milliseconds(350));await reload()}catch{}}
   .sheet(isPresented:$blockedSheet,onDismiss:{Task{await reload()}}){BlockedPlayersView()}
 }
 @ViewBuilder private var activityContent:some View {
  if store.activity.isEmpty {ContentUnavailableView("A little friendly competition",systemImage:"sparkles",description:Text("Follow players to see their completed duels here. Pull down to refresh."))}
  ForEach(store.activity){event in NavigationLink{PublicPlayerView(playerID:event.playerID)}label:{HStack(spacing:12){PlayerPortrait(name:event.name,avatar:event.avatar,size:42);VStack(alignment:.leading,spacing:5){Text(event.name).font(.headline);Text("\(event.draw ? "Drew":(event.won ? "Won":"Played")) in \(store.topics.first{$0.id==event.topicID}?.name ?? "Trivia") · \(event.score) points").font(.caption);Text(Date(timeIntervalSince1970:event.date),style:.relative).font(.caption2).foregroundStyle(.secondary)};Spacer()}.foregroundStyle(Color.ink).padding(15).background(.white,in:RoundedRectangle(cornerRadius:16))}.buttonStyle(.plain)}
 }
 private func reload() async {loading=true;defer{loading=false};if mode=="activity" {await store.refreshSocial()}else{await store.loadPeople(query:query,mode:mode)}}
}
struct BlockedPlayersView:View {
 @EnvironmentObject var store:QuizStore
 @Environment(\.dismiss) var dismiss
 @State private var error:String?
 var body:some View {
  NavigationStack{List{ForEach(store.people){p in HStack{Text(p.name);Spacer();Button("Unblock"){Task{do{try await store.blockPlayer(p.id,enabled:false);await store.loadPeople(mode:"blocked")}catch{self.error=error.localizedDescription}}}};if let error {Text(error).foregroundStyle(.red)}}.navigationTitle("Blocked players").toolbar{ToolbarItem(placement:.topBarTrailing){Button("Done"){dismiss()}}}}.task{await store.loadPeople(mode:"blocked")}
 }
}
struct PublicPlayerView:View {
 @EnvironmentObject var store:QuizStore
 let playerID:String
 @State private var card:PlayerCard?
 @State private var error:String?
 @State private var challenge=false
 @State private var confirmBlock=false
 var body:some View {
  ScrollView {
   if let card {
    VStack(spacing:19) {
     PlayerPortrait(name:card.name,avatar:card.avatar,size:100).padding(.top,20)
     Text(card.name).font(.system(size:29,weight:.bold,design:.rounded)).multilineTextAlignment(.center)
     Text(card.title).font(.headline).foregroundStyle(Color.coral)
     HStack{stat("\(card.stats.matches)","Duels");stat("\(card.stats.wins)","Wins");stat(card.stats.answered==0 ? "—":"\(card.stats.correct*100/card.stats.answered)%","Accuracy")}.padding(18).background(.white,in:RoundedRectangle(cornerRadius:18))
     Text("\(card.followers) followers · \(card.followingCount) following").font(.caption).foregroundStyle(.secondary)
     if playerID != store.profile?.id {
      if let h=card.headToHead {HeadToHeadView(name:card.name,tally:h)}
      HStack{Button(card.following ? "Following":"Follow"){Task{await toggleFollow(card)}}.buttonStyle(PrimaryButton(color:card.following ? .gray:.coral)).accessibilityIdentifier("followPlayer");Button("Challenge"){challenge=true}.buttonStyle(PrimaryButton(color:Color(hex:"348C98"))).disabled(!card.canChallenge).accessibilityIdentifier("challengePlayer")}
      if !card.canChallenge {Text("This player has paused new challenges.").font(.caption).foregroundStyle(.secondary)}
     } else {SocialPreferencesView(card:card,onSave:{await reload()})}
     interestSection(card)
     VStack(alignment:.leading,spacing:14){Text("Topic levels").font(.title3.bold());if card.topics.isEmpty {Text("Complete an online duel to start your first topic level.").font(.subheadline).foregroundStyle(.secondary)};ForEach(card.topics){p in if let topic=store.topics.first(where:{$0.id==p.topicID}){NavigationLink{TopicView(topic:topic)}label:{TopicLevelProgress(topic:topic,xp:p.xp).foregroundStyle(Color.ink)}.buttonStyle(.plain)}}}.padding(18).background(.white,in:RoundedRectangle(cornerRadius:18))
     if let badges=card.badges {badgeSection(badges)}
     if playerID != store.profile?.id {Button("Block player",role:.destructive){confirmBlock=true}.font(.caption)}
     if let error {Text(error).font(.caption).foregroundStyle(.red)}
    }.padding(22)
   } else if let error {ContentUnavailableView("Player unavailable",systemImage:"person.crop.circle.badge.exclamationmark",description:Text(error))}
   else {ProgressView("Loading player card…").padding(60)}
  }.background(Color.canvas).foregroundStyle(Color.ink).navigationTitle("Player card").navigationBarTitleDisplayMode(.inline).toolbar(.visible,for:.navigationBar)
   .task{await reload()}.refreshable{await reload()}
   .sheet(isPresented:$challenge){if let card {ChallengeComposer(playerID:card.id,name:card.name)}}
   .confirmationDialog("Block this player? Following links will be removed and unfinished challenges between you will be cancelled.",isPresented:$confirmBlock,titleVisibility:.visible){Button("Block player",role:.destructive){Task{do{try await store.blockPlayer(playerID,enabled:true);await reload()}catch{self.error=error.localizedDescription}}}}
 }
 private func stat(_ value:String,_ label:String)->some View {VStack{Text(value).font(.system(size:25,weight:.bold,design:.rounded));Text(label).font(.caption).foregroundStyle(.secondary)}.frame(maxWidth:.infinity)}
 private func interestSection(_ c:PlayerCard)->some View {
  VStack(alignment:.leading,spacing:10){Text("Shared interests & favourite topics").font(.title3.bold());if c.interests.isEmpty {Text("No topics followed yet.").font(.caption).foregroundStyle(.secondary)};ForEach(store.topics.filter{c.interests.contains($0.id)}){topic in NavigationLink{TopicView(topic:topic)}label:{HStack{Text(topic.emoji);Text(topic.name);Spacer();if c.sharedTopics.contains(topic.id){Text("Shared").font(.caption).foregroundStyle(topic.tint)};Image(systemName:"chevron.right").font(.caption)}.font(.subheadline).foregroundStyle(Color.ink)}}.padding(18).frame(maxWidth:.infinity,alignment:.leading).background(.white,in:RoundedRectangle(cornerRadius:18))
 }
 private func badgeSection(_ badges:[PlayerBadge])->some View {
  VStack(alignment:.leading,spacing:15){Text("Achievements").font(.title3.bold());ForEach(badges){b in HStack(spacing:13){Image(systemName:b.symbol).foregroundStyle(b.earned ? Color(hex:"D49A31"):.gray).frame(width:28);Text(b.name).font(.subheadline);Spacer();Text(b.earned ? "Earned":"Locked").font(.caption).foregroundStyle(.secondary)}}}.padding(18).background(.white,in:RoundedRectangle(cornerRadius:18))
 }
 private func reload()async {do{card=try await store.playerCard(playerID);error=nil;if playerID==store.profile?.id{store.ownCard=card}}catch{card=nil;self.error=error.localizedDescription}}
 private func toggleFollow(_ c:PlayerCard)async {do{try await store.followPlayer(c.id,enabled:!c.following);await reload()}catch{self.error=error.localizedDescription}}
}
struct HeadToHeadView:View {
 let name:String;let tally:HeadToHead
 var body:some View {
  VStack(spacing:12){Text("YOUR HEAD-TO-HEAD").font(.system(size:11,weight:.black)).tracking(1);HStack{record("You",tally.wins);Text("–").font(.title.bold());record(name,tally.losses)};Text("\(tally.draws) draws · \(tally.games) completed meetings").font(.caption).foregroundStyle(.secondary)}.padding(18).frame(maxWidth:.infinity).background(Color.coral.opacity(0.1),in:RoundedRectangle(cornerRadius:18)).accessibilityElement(children:.combine).accessibilityIdentifier("headToHead")
 }
 private func record(_ name:String,_ wins:Int)->some View {VStack{Text("\(wins)").font(.system(size:35,weight:.heavy,design:.rounded));Text(name).font(.caption).lineLimit(1)}.frame(maxWidth:.infinity)}
}
struct SocialPreferencesView:View {
 @EnvironmentObject var store:QuizStore
 let card:PlayerCard;var onSave:()async->Void
 @State private var title="newcomer"
 @State private var discoverable=true
 @State private var open=true
 @State private var busy=false
 @State private var message:String?
 var body:some View {
  VStack(alignment:.leading,spacing:14){Text("Your public player card").font(.headline);Text("Your name, picture, followed topics and completed online results appear on your player card. Each topic has its own level.").font(.caption).foregroundStyle(.secondary);Picker("Display title",selection:$title){ForEach(card.titles){Text($0.name).tag($0.id)}};Text("Topic titles unlock at levels 10, 20, 30, 40 and 50. Select any title you have earned.").font(.caption).foregroundStyle(.secondary);Toggle("Show me in player discovery",isOn:$discoverable);Toggle("Allow direct challenges",isOn:$open);Button("Save public card"){Task{busy=true;defer{busy=false};do{try await store.saveSocial(title:title,discoverable:discoverable,challengesOpen:open);message="Saved";await onSave()}catch{message=error.localizedDescription}}}.buttonStyle(PrimaryButton()).disabled(busy);if let message {Text(message).font(.caption)}}.padding(18).background(.white,in:RoundedRectangle(cornerRadius:18)).onAppear{title=card.selectedTitle;discoverable=card.discoverable;open=card.challengesOpen}
 }
}
struct ChallengeComposer:View {
 @EnvironmentObject var store:QuizStore
 @Environment(\.dismiss) var dismiss
 let playerID:String;let name:String
 var initialTopic:String?=nil
 @State private var topicID="9"
 @State private var busy=false
 @State private var error:String?
 @State private var session:GameSession?
 @State private var requestID=UUID().uuidString
 var body:some View {
  NavigationStack {
   VStack(alignment:.leading,spacing:22){Text("You vs \(name)").font(.system(size:29,weight:.bold,design:.rounded));Text("Play your seven questions now. They can accept and answer later. The same questions and answer order are used for both of you.").font(.body);Picker("Topic",selection:$topicID){ForEach(store.topics){Text($0.emoji+" "+$0.name).tag($0.id)}}.pickerStyle(.menu).accessibilityIdentifier("challengeTopic");Text("The result and your head-to-head record update when both runs are finished. Invitations expire after 14 days.").font(.subheadline).foregroundStyle(.secondary);Spacer();if let error {Text(error).foregroundStyle(.red).font(.caption)};Button(busy ? "Sending…":"Send challenge & play"){Task{await send()}}.buttonStyle(PrimaryButton()).disabled(busy).accessibilityIdentifier("sendChallenge")}.padding(24).background(Color.canvas).navigationTitle("Challenge").navigationBarTitleDisplayMode(.inline).toolbar{ToolbarItem(placement:.topBarTrailing){Button("Cancel"){dismiss()}.disabled(busy)}}
  }.onAppear{topicID=initialTopic ?? store.favourites.sorted().first ?? "9"}.onChange(of:topicID){_,_ in requestID=UUID().uuidString}
   .fullScreenCover(item:$session,onDismiss:{dismiss();Task{await store.refreshSocial()}}){GameView(game:$0).environmentObject(store)}
 }
 private func send()async {guard let topic=store.topics.first(where:{$0.id==topicID}) else{return};busy=true;defer{busy=false};do{let r=try await store.createChallenge(player:playerID,topic:topicID,requestID:requestID);session=GameSession(topic:topic,store:store,online:true,match:r)}catch{self.error=error.localizedDescription}}
}
struct DuelsView:View {
 @EnvironmentObject var store:QuizStore
 @State private var history=false
 @State private var session:GameSession?
 @State private var error:String?
 var body:some View {
  NavigationStack {
   VStack(spacing:0) {
    Picker("Duel section",selection:$history){Text("Challenges").tag(false);Text("Device history").tag(true)}.pickerStyle(.segmented).padding(.horizontal,20).padding(.top,12).accessibilityIdentifier("duelSection")
    if history {HistoryView()}
    else {ScrollView{BrandHeader(title:"A friendly rivalry.",subtitle:"Take your turn. They can catch up later.");VStack(spacing:15){if store.challenges.isEmpty {ContentUnavailableView("Your next rival is waiting",systemImage:"person.2.wave.2",description:Text("Find someone in People, follow them, then send a challenge. You can finish your questions before they accept."))};ForEach(store.challenges){card in challengeRow(card)};if let message=error ?? store.socialError{Text(message).font(.caption).foregroundStyle(.red)};Button("Refresh challenges"){Task{await store.refreshSocial();await store.connect()}}.buttonStyle(.bordered)}.padding(.horizontal,20).padding(.bottom,24)}.refreshable{await store.refreshSocial();await store.connect()}}
   }.background(Color.canvas).toolbar(.hidden,for:.navigationBar)
  }.task{await store.refreshSocial()}.fullScreenCover(item:$session,onDismiss:{Task{await store.refreshSocial();await store.connect()}}){GameView(game:$0).environmentObject(store)}
 }
 private func challengeRow(_ c:ChallengeCard)->some View {
  VStack(alignment:.leading,spacing:13){HStack(spacing:12){PlayerPortrait(name:c.opponent,avatar:c.avatar,size:45);VStack(alignment:.leading,spacing:4){Text(c.opponent).font(.headline);Text(store.topics.first{$0.id==c.topicID}?.name ?? "Trivia").font(.caption).foregroundStyle(.secondary)};Spacer();Text(c.statusText).font(.caption.bold()).multilineTextAlignment(.trailing).foregroundStyle(c.complete ? Color(hex:"348C98"):Color.coral)}
   if c.complete {Text("\(c.score) – \(c.opponentScore ?? 0)").font(.title2.bold())}
   if c.ownFinished && c.available {Text("Your answers are saved. The final result appears when \(c.opponent) finishes.").font(.caption).foregroundStyle(.secondary)}
   HStack{if c.needsTurn || c.complete {Button(c.complete ? "View result":(c.incoming && !c.accepted ? "Accept & play":"Play your turn")){Task{await open(c)}}.buttonStyle(.borderedProminent).tint(.coral)};if c.incoming && !c.accepted && c.available {Button("Decline",role:.destructive){Task{do{try await store.declineChallenge(c.id)}catch{self.error=error.localizedDescription}}}};Spacer();if let id=c.opponentID {NavigationLink("Player card"){PublicPlayerView(playerID:id)}.font(.caption)}}
  }.padding(17).background(.white,in:RoundedRectangle(cornerRadius:18)).foregroundStyle(Color.ink)
 }
 private func open(_ c:ChallengeCard)async {do{let r=try await store.openChallenge(c.id);guard let topic=store.topics.first(where:{$0.id==c.topicID})else{return};session=GameSession(topic:topic,store:store,online:true,match:r)}catch{self.error=error.localizedDescription}}
}
