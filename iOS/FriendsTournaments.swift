import SwiftUI

struct FriendsTournament:Decodable,Identifiable,Hashable {
 let id:String;let name:String;let code:String;let hostID:String;let status:String
 let cycles:Int;let days:Int;let powers:Bool;let ends:Double;let members:Int;let entryCoins:Int
}
struct FriendsInvitation:Decodable {let name:String;let entryCoins:Int;let status:String;let alreadyMember:Bool}
struct FriendsTournamentList:Decodable {let parties:[FriendsTournament]}
struct FriendsStanding:Decodable,Identifiable {
 let id:String;let name:String;let avatar:String?;let topicID:String
 let played:Int;let wins:Int;let draws:Int;let losses:Int;let points:Int;let quizPoints:Int;let rank:Int
}
struct FriendsFixture:Decodable,Identifiable {
 let id:String;let a:String;let b:String;let topicID:String;let homeID:String;let cycle:Int;let status:String;let ownFinished:Bool
}
struct FriendsBoard:Decodable {let party:FriendsTournament;let standings:[FriendsStanding];let fixtures:[FriendsFixture];let selfID:String;let coins:Int}

struct FriendsTournamentsView:View {
 @EnvironmentObject private var store:QuizStore
 @State private var rooms:[FriendsTournament]=[]
 @State private var error:String?
 @State private var composer=false
 var body:some View {
  ScrollView {
   VStack(alignment:.leading,spacing:20) {
    Text("Home topic. Away topic. Bragging rights.").font(.system(size:27,weight:.bold,design:.rounded))
    Text("A private round-robin for 2–8 friends. Each pair plays one duel in each person’s home topic per cycle. Play together at a party or catch up later.").foregroundStyle(.secondary)
    Button("Create or join a tournament"){composer=true}.buttonStyle(PrimaryButton(color:.ink))
    Text("Your friends tournaments").font(.title3.bold())
    ForEach(rooms){room in NavigationLink{FriendsTournamentView(room:room)}label:{VStack(alignment:.leading,spacing:8){Text(room.name).font(.headline);Text("\(room.members) players · \(room.status.capitalized)").font(.caption).foregroundStyle(.secondary)}.frame(maxWidth:.infinity,alignment:.leading).padding(18).background(.white,in:RoundedRectangle(cornerRadius:16))}.buttonStyle(.plain)}
    if rooms.isEmpty,error==nil {Text("Create a tournament and share its invitation code with your friends.").font(.subheadline).foregroundStyle(.secondary)}
    if let error {Text(error).font(.caption).foregroundStyle(.red);Button("Try again"){Task{await reload()}}}
   }.padding(22)
  }.background(Color.canvas).foregroundStyle(Color.ink).navigationTitle("Friends tournaments")
   .task{await reload()}.refreshable{await reload()}
   .sheet(isPresented:$composer,onDismiss:{Task{await reload()}}){FriendsTournamentComposer()}
 }
 private func reload()async {
  if store.profile==nil{await store.connect()}
  do{let r:FriendsTournamentList=try await store.request("parties");rooms=r.parties;error=nil}catch{self.error=error.localizedDescription}
 }
}

struct FriendsTournamentComposer:View {
 @EnvironmentObject private var store:QuizStore
 @Environment(\.dismiss) private var dismiss
 @State private var joining=false
 @State private var name="Game night"
 @State private var code=""
 @State private var topic="22"
 @State private var cycles=1
 @State private var days=7
 @State private var powers=false
 @State private var prizes=true
 @State private var invitation:FriendsInvitation?
 @State private var busy=false
 @State private var error:String?
 @State private var requestID=UUID().uuidString
 var body:some View {
  NavigationStack {
   Form {
    Section {Picker("Action",selection:$joining){Text("Create").tag(false);Text("Join").tag(true)}.pickerStyle(.segmented)}
    Section(joining ? "Invitation":"Your tournament") {
     if joining {TextField("Invitation code",text:$code).textInputAutocapitalization(.characters).autocorrectionDisabled()}
     else {
      TextField("Tournament name",text:$name)
      Stepper("\(cycles) cycle\(cycles==1 ? "":"s") · \(cycles*2) duels per pair",value:$cycles,in:1...3)
      Picker("Time to finish",selection:$days){ForEach([1,3,7,14],id:\.self){n in Text("\(n) day\(n==1 ? "":"s")").tag(n)}}
      Toggle("Coin entry and podium prizes",isOn:$prizes)
      Text(prizes ? "10 coins per person · coin and badge prizes":"Free entry · no coins, badges or tournament prizes").font(.caption).foregroundStyle(.secondary)
      Toggle("Allow power-ups",isOn:$powers)
     }
     Picker("My home topic",selection:$topic){ForEach(store.topics){t in Text(t.emoji+" "+t.name).tag(t.id)}}
    }
    if joining,let invitation {Section("Invitation details"){Text(invitation.name).font(.headline);Text(invitation.alreadyMember ? "You already joined · no further charge":(invitation.entryCoins==0 ? "Free entry · no prizes":"Entry: \(invitation.entryCoins) coins · coin and badge prizes"));if invitation.status != "lobby" && !invitation.alreadyMember {Text("Entries have closed").foregroundStyle(.secondary)}}}
    Section {
     Text("The host chooses free entry without prizes, or a 10-coin entry with podium prizes. Any entry fee is charged when you create or join. The host starts once everyone has joined and picked a topic. Topics and settings then lock.")
     Text("Win = 3 league points; draw = 1. Equal league points share a place. Both players get the same seven questions and their own clocks. Unfinished duels earn no league points.")
     Text("For a paid tournament, the entry pool awards coins and profile badges to the top three places. Two players share 60% / 40%; three or more share 50% / 30% / 20%. Tied places share those prizes.")
     Text("Only members can see the board. An unstarted lobby expires after 24 hours and refunds every entry. The host can also cancel before starting.")
    }.font(.caption).foregroundStyle(.secondary)
    if let error {Section{Text(error).foregroundStyle(.red)}}
    Section{Button(busy ? "Checking…":actionTitle){Task{await submit()}}.disabled(busy || (joining && code.isEmpty) || (!joining && name.trimmingCharacters(in:.whitespaces).count<2) || (joining && invitation != nil && invitation?.alreadyMember==false && invitation?.status != "lobby"))}
   }.navigationTitle("Play with friends").toolbar{ToolbarItem(placement:.topBarTrailing){Button("Done"){dismiss()}}}
  }.onChange(of:code){_,_ in invitation=nil}
 }
 private var actionTitle:String {
  if joining {guard let invitation else{return "Check invitation"};return invitation.alreadyMember ? "Open tournament":(invitation.entryCoins==0 ? "Join free":"Join · \(invitation.entryCoins) coins")}
  return prizes ? "Create · 10 coins":"Create free · no prizes"
 }
 private func submit()async {
  busy=true;defer{busy=false};error=nil
  if store.profile==nil{await store.connect()}
  do {
   if joining,invitation==nil {invitation=try await store.request("party-preview",body:["code":code]);return}
   let _:FriendsTournament=try await store.request(joining ? "party-join":"party-create",body:joining ? ["code":code,"topic":topic,"expectedEntryCoins":invitation?.entryCoins ?? 0]:["name":name,"entryCoins":prizes ? 10:0,"topic":topic,"cycles":cycles,"days":days,"powers":powers,"requestID":requestID])
   dismiss()
  }catch{self.error=error.localizedDescription}
 }
}

struct FriendsTournamentView:View {
 @EnvironmentObject private var store:QuizStore
 let room:FriendsTournament
 @State private var board:FriendsBoard?
 @State private var error:String?
 @State private var busy=false
 @State private var topic="22"
 @State private var game:GameSession?
 @State private var cancel=false
 var current:FriendsTournament {board?.party ?? room}
 var body:some View {
  ScrollView {
   VStack(alignment:.leading,spacing:20) {
    Text(current.name).font(.system(size:29,weight:.bold,design:.rounded))
    Text("Private · \(current.members) players · \(current.status.capitalized)").font(.subheadline).foregroundStyle(.secondary)
    if current.status=="lobby" {
     HStack{Text(current.code).font(.system(.title3,design:.monospaced).bold()).textSelection(.enabled);Spacer();ShareLink(item:"Join my Quizfolk friends tournament: \(current.name). Invitation code: \(current.code)"){Label("Invite",systemImage:"square.and.arrow.up")}}
     Text(current.entryCoins==0 ? "Share the code and wait for your friends. Entry is free, with no tournament prizes. Your lobby closes in 24 hours if it isn’t started.":"Share the code and wait for your friends. Joining costs \(current.entryCoins) coins. Your lobby closes in 24 hours if it isn’t started.").font(.caption).foregroundStyle(.secondary)
     Picker("My home topic",selection:$topic){ForEach(store.topics){t in Text(t.emoji+" "+t.name).tag(t.id)}}
     Button("Save home topic"){Task{await changeTopic()}}.disabled(busy)
     if board?.selfID==current.hostID {
      Button("Start tournament · lock players and topics"){Task{await command("party-start")}}.buttonStyle(PrimaryButton()).disabled(busy || current.members<2)
      Button(current.entryCoins==0 ? "Cancel tournament":"Cancel and refund all entries",role:.destructive){cancel=true}.disabled(busy)
     } else {Text("The host will start when everyone is ready.").font(.subheadline)}
    } else if current.status=="playing" {
     HStack{Text("Finish by");Text(Date(timeIntervalSince1970:current.ends),style:.date);Text(Date(timeIntervalSince1970:current.ends),style:.time)}.font(.caption)
    }
    standings
    if let board,current.status != "lobby" {
     Text("Your matches").font(.title3.bold())
     ForEach(board.fixtures.filter{$0.a==board.selfID || $0.b==board.selfID}){f in fixture(f,board:board)}
    }
    VStack(alignment:.leading,spacing:8){Text("How this tournament works").font(.headline);Text("Each pair plays \(current.cycles*2) duels: both home topics in every cycle. Win 3 points, draw 1. Ties share a place. The board updates after both players finish. Unfinished matches score zero at the deadline.");Text(current.powers ? "One coin-funded power-up per duel is allowed.":"Power-ups are switched off for everyone.");Text(current.entryCoins==0 ? "Free tournament · no coin prizes or profile badges. Results appear when all duels finish or the deadline arrives.":"The entry pool pays the top three places and awards profile badges. Results appear when all duels finish or the deadline arrives.")}.font(.caption).foregroundStyle(.secondary)
    if let error {Text(error).font(.caption).foregroundStyle(.red)}
    Button("Refresh"){Task{await reload()}}.disabled(busy)
   }.padding(22)
  }.background(Color.canvas).foregroundStyle(Color.ink).navigationTitle("Friends tournament").navigationBarTitleDisplayMode(.inline)
   .task{await reload()}.refreshable{await reload()}
   .fullScreenCover(item:$game,onDismiss:{Task{await reload();await store.loadPrizes()}}){g in GameView(game:g).environmentObject(store)}
   .confirmationDialog(current.entryCoins==0 ? "Cancel this free tournament?":"Cancel this lobby and refund everyone’s entry coins?",isPresented:$cancel,titleVisibility:.visible){Button("Cancel tournament",role:.destructive){Task{await command("party-cancel")}}}
 }
 private var standings:some View {
  VStack(alignment:.leading,spacing:12) {
   Text(current.status=="complete" ? "Final standings":"Tournament standings").font(.title3.bold())
   Text("Wins 3 · draws 1 · equal points share a place").font(.caption).foregroundStyle(.secondary)
   if let board {ForEach(board.standings){r in
    HStack(spacing:10){Text("#\(r.rank)").font(.headline);PlayerPortrait(name:r.name,avatar:r.avatar,size:34);VStack(alignment:.leading,spacing:3){Text(r.name).font(.subheadline.bold());Text("\(r.played) played · \(r.wins)W \(r.draws)D \(r.losses)L").font(.caption2).foregroundStyle(.secondary);Text("Home: \(topicName(r.topicID))").font(.caption2).foregroundStyle(.secondary)};Spacer();Text("\(r.points)").font(.title2.bold())}
   }} else {ProgressView()}
  }.padding(17).background(.white,in:RoundedRectangle(cornerRadius:17))
 }
 private func fixture(_ f:FriendsFixture,board:FriendsBoard)->some View {
  let other=f.a==board.selfID ? f.b:f.a
  let name=board.standings.first{$0.id==other}?.name ?? "Former player"
  return VStack(alignment:.leading,spacing:7){Text("vs \(name)").font(.headline);Text("\(topicName(f.topicID)) · Cycle \(f.cycle) · \(f.homeID==board.selfID ? "Your home topic":"Their home topic")").font(.caption).foregroundStyle(.secondary)
   if current.status=="playing" || f.status=="complete" {Button(f.status=="complete" ? "View result":(f.ownFinished ? "Run saved · check result":"Play duel")){Task{await play(f)}}.disabled(busy)}else{Text("Unfinished · no league points").font(.caption)}
  }.frame(maxWidth:.infinity,alignment:.leading).padding(16).background(.white,in:RoundedRectangle(cornerRadius:15))
 }
 private func topicName(_ id:String)->String {store.topics.first{$0.id==id}?.name ?? "Topic"}
 private func reload()async {
  do{let r:FriendsBoard=try await store.request("party-board",query:[URLQueryItem(name:"id",value:room.id)]);board=r;topic=r.standings.first{$0.id==r.selfID}?.topicID ?? topic;error=nil}catch{self.error=error.localizedDescription}
 }
 private func command(_ route:String)async {
  busy=true;defer{busy=false}
  do{let _:OKReply=try await store.request(route,body:["party":room.id]);await reload()}catch{self.error=error.localizedDescription}
 }
 private func changeTopic()async {
  busy=true;defer{busy=false}
  do{let _:OKReply=try await store.request("party-topic",body:["party":room.id,"topic":topic]);await reload()}catch{self.error=error.localizedDescription}
 }
 private func play(_ fixture:FriendsFixture)async {
  guard let topic=store.topics.first(where:{$0.id==fixture.topicID})else{return}
  busy=true;defer{busy=false}
  do{let match:StartReply=try await store.request("party-play",body:["party":room.id,"fixture":fixture.id]);game=GameSession(topic:topic,store:store,online:true,match:match)}catch{self.error=error.localizedDescription}
 }
}
