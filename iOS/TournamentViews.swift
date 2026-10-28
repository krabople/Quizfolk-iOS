import SwiftUI

struct TournamentsView:View {
 @EnvironmentObject var store:QuizStore
 @State private var list:TournamentList?
 @State private var error:String?
 @State private var section="daily"
 var body:some View {
  NavigationStack {
   ScrollView {
    BrandHeader(title:"Keep your streak alive.",subtitle:"One wrong answer. One final score.")
    VStack(spacing:18) {
     if let list {
      walletView(list.wallet)
      Text("Build the biggest score before your first wrong answer or timeout. Faster correct answers earn more points. Your best run counts.").font(.subheadline).foregroundStyle(.secondary)
      Picker("Tournament section",selection:$section) {
       Text("Daily").tag("daily");Text("Weekly").tag("weekly");Text("My entries").tag("results")
      }.pickerStyle(.segmented)
      let visible=list.events.filter{section=="results" ? $0.attempts>0:$0.kind==section && !$0.closed && $0.isFeatured}
      if section=="daily" {Text("Three topics each day · 25, 50 and 75 coins to enter").font(.caption).foregroundStyle(.secondary)}
      if section=="results" {Text("Resume your runs and see results from every tournament you entered.").font(.caption).foregroundStyle(.secondary)}
      if visible.isEmpty {ContentUnavailableView(section=="results" ? "Your next trophy awaits":"New tournaments soon",systemImage:"trophy",description:Text("Daily topics rotate at midnight UTC. Weekly tournaments close on Monday at midnight UTC."))}
      ForEach(visible) {event in
       if let topic=store.topics.first(where:{$0.id==event.topicID}) {
        NavigationLink {TournamentDetailView(event:event,topic:topic)} label: {TournamentTile(event:event,topic:topic)}.buttonStyle(.plain).accessibilityIdentifier("tournament-\(event.id)")
       }
      }
     } else if error==nil {ProgressView("Loading tournaments…").padding(40)}
     if let error {Text(error).font(.caption).foregroundStyle(.red);Button("Try again"){Task{await reload()}}}
    }.padding(.horizontal,20).padding(.bottom,24)
   }.background(Color.canvas).toolbar(.hidden,for:.navigationBar).refreshable{await reload()}
  }.task{await reload()}
 }
 private func walletView(_ w:TournamentWallet)->some View {
  VStack(spacing:12) {
   HStack {Label("\(w.coins) coins",systemImage:"circle.fill").font(.title2.bold());Spacer();NavigationLink("Earn coins"){CoinTrailView()}.font(.headline)}.foregroundStyle(Color.ink)
   Text("Complete your Daily Trail to earn coins, then put them towards a tournament entry.").font(.caption).foregroundStyle(.secondary)
  }.padding(17).background(.white,in:RoundedRectangle(cornerRadius:17))
 }
 private func reload()async {do{list=try await store.tournamentList();error=nil}catch{self.error=error.localizedDescription}}
}

struct TournamentTile:View {
 let event:TournamentEvent;let topic:Topic
 var body:some View {
  HStack(spacing:14) {
   Text(topic.emoji).font(.system(size:34)).frame(width:64,height:64).background(topic.tint.opacity(0.13),in:RoundedRectangle(cornerRadius:16))
   VStack(alignment:.leading,spacing:6) {
    Text(topic.name).font(.headline)
    Text(event.closed ? "Finished · Best \(event.best) points":event.entryLabel+" · \(event.players) player\(event.players==1 ? "":"s")").font(.caption).foregroundStyle(.secondary)
    if event.closed {if let rank=event.rank {Text("Final place #\(rank) · \(event.reward) prize coins").font(.caption.bold()).foregroundStyle(topic.tint)}}
    else {HStack(spacing:4){Text("Ends in");Text(Date(timeIntervalSince1970:event.ends),style:.relative)}.font(.caption.bold()).foregroundStyle(topic.tint)}
   }
   Spacer(minLength:0);Image(systemName:"chevron.right").font(.caption).foregroundStyle(.secondary)
  }.padding(15).background(.white,in:RoundedRectangle(cornerRadius:19)).foregroundStyle(Color.ink)
 }
}

struct TournamentDetailView:View {
 @EnvironmentObject var store:QuizStore
 let event:TournamentEvent;let topic:Topic
 @State private var board:TournamentBoard?
 @State private var error:String?
 @State private var entryNotice:EntryNotice?
 @State private var entryBusy=false
 @State private var entryRequestID=UUID().uuidString
 @State private var session:TournamentSession?
 private var current:TournamentEvent {board?.event ?? event}
 var body:some View {
  ScrollView {
   VStack(spacing:18) {
    Text(topic.emoji).font(.system(size:62)).padding(.top,15)
    Text(topic.name).font(.system(size:30,weight:.bold,design:.rounded)).multilineTextAlignment(.center)
    Text(current.kind.capitalized+" survival tournament").font(.headline).foregroundStyle(topic.tint)
    if !current.closed {HStack{Text("Closes");Text(Date(timeIntervalSince1970:current.ends),style:.date);Text(Date(timeIntervalSince1970:current.ends),style:.time)}.font(.caption)}
    HStack {summary("\(current.best)","Your best points");summary("\(current.players)","Players");summary("\(current.attempts)","Your attempts")}.padding(18).background(.white,in:RoundedRectangle(cornerRadius:18))
    if !current.closed {
     if let wallet=board?.wallet {Text("Your balance: \(wallet.coins) coins").font(.caption).foregroundStyle(.secondary)}
     if current.isFeatured || current.activeRun != nil {
      Button(entryBusy ? "Checking entry…":(current.activeRun==nil ? "Enter · \(current.entryLabel)":"Resume your run · already entered")) {
       Task{await prepareEntry()}
      }.buttonStyle(PrimaryButton(color:topic.tint)).disabled(entryBusy).accessibilityIdentifier("enterTournament")
     } else {
      Text("New entries are closed for this earlier tournament. Your score is kept until the tournament ends.").font(.subheadline).multilineTextAlignment(.center)
     }
    }
    rules
    if let pool=current.prizePool {Label("\(pool) coins in the prize pool",systemImage:"trophy").font(.headline).foregroundStyle(topic.tint)}
    VStack(alignment:.leading,spacing:15) {
     HStack {Text(current.closed ? "Final standings":"Tournament standings").font(.title3.bold());Spacer();Button{Task{await reload()}}label:{Image(systemName:"arrow.clockwise")}.accessibilityLabel("Refresh tournament standings")}
     Text("Best score counts · equal scores share a place").font(.caption).foregroundStyle(.secondary)
     if let board {
      if board.entries.isEmpty {Text("Be the first player to set a score.").font(.subheadline).foregroundStyle(.secondary)}
      ForEach(board.entries) {entry in
       NavigationLink {PublicPlayerView(playerID:entry.id)} label: {
        HStack(spacing:11) {
         Text("#\(entry.rank)").font(.headline).frame(width:38)
         PlayerPortrait(name:entry.name,avatar:entry.avatar,size:36)
         VStack(alignment:.leading,spacing:3){Text(entry.name).font(.subheadline.bold());Text("\(entry.streak) correct in that run").font(.caption2).foregroundStyle(.secondary)}
         Spacer();Text("\(entry.score)").font(.title3.bold()).foregroundStyle(topic.tint)
        }.foregroundStyle(Color.ink)
       }.buttonStyle(.plain)
      }
      if let own=board.own.first,!board.entries.contains(where:{$0.id==own.id}) {Text("Your place: #\(own.rank) · \(own.score) points").font(.headline)}
     } else {ProgressView()}
    }.padding(18).background(.white,in:RoundedRectangle(cornerRadius:18))
    if let error {Text(error).font(.caption).foregroundStyle(.red)}
   }.padding(22)
  }.background(Color.canvas).foregroundStyle(Color.ink).navigationTitle("Tournament").navigationBarTitleDisplayMode(.inline).toolbar(.visible,for:.navigationBar)
   .task{await reload()}.refreshable{await reload()}
   .alert(item:$entryNotice) {notice in
    if notice.confirmation {
     return Alert(title:Text(notice.title),message:Text(notice.message),primaryButton:.default(Text("Enter · \(current.entryLabel)")){Task{await start()}},secondaryButton:.cancel())
    }
    return Alert(title:Text(notice.title),message:Text(notice.message),dismissButton:.default(Text("OK")))
   }
   .fullScreenCover(item:$session,onDismiss:{Task{await reload()}}){TournamentPlayView(game:$0).environmentObject(store)}
 }
 private var rules:some View {
  VStack(alignment:.leading,spacing:11) {
   Text("How this tournament works").font(.headline)
   Text("Keep answering in \(topic.name) until your first wrong answer or timeout. Read each question for 2 seconds, then choose from four answers within 10 seconds. Correct answers earn 11–20 points for speed; every question has the same value. Your score is the total points in that run.")
   Text("Try again for the displayed entry cost. Only your best run counts; attempts do not add together. Every question in a run is different. If you clear the entire topic bank, that completes your run.")
   Text("The leaderboard closes at the stated time. Earned points are kept if you end a run early or the event closes. The top three places receive coins and a profile badge.")
   Text("Entry coins form the prize pool. With three or more players, first place receives 50%, second 30% and third 20%. With two players, the split is 60% and 40%; a sole entrant receives the whole pool. Tied players share the prizes for the places they occupy, rounded down to whole coins.")
   Text("You compete against other players’ scores on your own schedule. Tournament points are separate from duel XP and topic levels.")
  }.font(.caption).foregroundStyle(.secondary).padding(18).background(.white,in:RoundedRectangle(cornerRadius:18)).accessibilityIdentifier("tournamentRules")
 }
 private func summary(_ value:String,_ label:String)->some View {VStack(spacing:5){Text(value).font(.system(size:24,weight:.heavy,design:.rounded));Text(label).font(.caption2).foregroundStyle(.secondary)}.frame(maxWidth:.infinity)}
 private struct EntryNotice:Identifiable {
  let id=UUID();let title:String;let message:String;var confirmation=false
 }
 private func prepareEntry()async {
  guard !entryBusy else{return}
  entryBusy=true;defer{entryBusy=false}
  do {
   let fresh=try await store.tournamentBoard(event.id)
   board=fresh;error=nil
   guard !fresh.event.closed else {
    entryNotice=EntryNotice(title:"Tournament finished",message:"Entries have closed. Choose one of today’s tournaments.");return
   }
   if let problem=fresh.wallet.entryProblem(for:fresh.event) {
    entryNotice=EntryNotice(title:problem.title,message:problem.message);return
   }
   if fresh.event.activeRun != nil {
    await start()
   } else {
    entryNotice=EntryNotice(title:"Enter for \(fresh.event.entryLabel)?",message:"This entry costs \(fresh.event.entryLabel). Each new attempt has the same cost. Resuming this run is free, and only your best score counts.",confirmation:true)
   }
  } catch {
   entryNotice=EntryNotice(title:"Couldn’t check your entry",message:error.localizedDescription)
  }
 }
 private func start()async {
  entryBusy=true;defer{entryBusy=false}
  do {
   // Admission happens here, before opening the game. The server checks the
   // latest balance atomically and reuses this key if a network request retries.
   let admitted:TournamentRunReply=try await store.request("tournament-enter",body:["event":event.id,"requestID":entryRequestID])
   session=TournamentSession(event:current,topic:topic,store:store,admittedRun:admitted)
   entryRequestID=UUID().uuidString
  } catch {
   entryNotice=EntryNotice(title:"Couldn’t enter tournament",message:error.localizedDescription)
   await reload()
  }
 }
 private func reload()async {do{board=try await store.tournamentBoard(event.id);error=nil}catch{self.error=error.localizedDescription}}
}

struct TournamentPlayView:View {
 @ObservedObject var game:TournamentSession
 @Environment(\.dismiss) private var dismiss
 @Environment(\.scenePhase) private var scenePhase
 @Environment(\.accessibilityReduceMotion) private var reduceMotion
 @State private var leave=false
 var body:some View {
  NavigationStack {
   Group {
    if game.showResult {result}
    else {play}
   }.foregroundStyle(.white).background(LinearGradient(colors:[Color(hex:"102640"),game.topic.tint,Color(hex:"123452")],startPoint:.topLeading,endPoint:.bottomTrailing).ignoresSafeArea())
    .navigationTitle(game.topic.name).navigationBarTitleDisplayMode(.inline).toolbarColorScheme(.dark,for:.navigationBar)
    .toolbar {ToolbarItem(placement:.topBarLeading){Button{if game.runEnded || !game.hasStarted{dismiss()}else{leave=true}}label:{Image(systemName:"xmark")}.disabled(game.busy).accessibilityLabel("Close tournament run")}}
    .confirmationDialog("End this run and keep your current score?",isPresented:$leave,titleVisibility:.visible) {
     Button("End run & save score",role:.destructive){Task{if await game.end(){dismiss()}}}
     Button("Keep playing",role:.cancel){}
    }
  }.preferredColorScheme(.dark).task{await game.begin()}.onDisappear{game.stop()}
   .onChange(of:scenePhase){_,phase in if phase == .active {Task{await game.resume()}}}
 }
 private var play:some View {
  GeometryReader {geo in
   VStack(spacing:16) {
    HStack {
     VStack(alignment:.leading,spacing:5){Text("SURVIVAL TOURNAMENT").font(.system(size:10,weight:.black)).tracking(1);Text("\(game.score) points").font(.system(size:30,weight:.heavy,design:.rounded));Text("\(game.streak) correct in a row").font(.caption)}
     Spacer();if game.question != nil {timer}
    }
    if let question=game.question {
     Text(question.prompt).font(.system(size:25,weight:.bold,design:.rounded)).multilineTextAlignment(.center).lineLimit(7).minimumScaleFactor(0.6).frame(maxWidth:.infinity,maxHeight:.infinity)
     if game.reading {Text("Read the question · answers appear in a moment").font(.subheadline.bold()).multilineTextAlignment(.center);Spacer(minLength:50)}
     else {
      VStack(spacing:10){ForEach(question.answers.indices,id:\.self){i in answer(question.answers[i],index:i)}}.frame(height:geo.size.height*(game.revealed ? 0.40:0.48))
     }
     if game.revealed {
      HStack {
       Text(game.lastPoints>0 ? "+\(game.lastPoints) points":(game.selected == -1 ? "Time’s up · run finished":"Wrong answer · run finished")).font(.subheadline.bold())
       Spacer()
       Button(game.runEnded ? "See score":"Next question"){Task{await game.next()}}.buttonStyle(.borderedProminent).tint(.coral).accessibilityIdentifier("advanceTournament")
      }
     }
     Text("\(question.source ?? "Open trivia contributors") · CC BY-SA 4.0").font(.system(size:8)).opacity(0.65).lineLimit(1)
    } else {
     Spacer()
     if game.error==nil {ProgressView("Preparing your run…").tint(.white)}
     else {Label("Your run couldn’t load",systemImage:"exclamationmark.circle").font(.headline)}
     Spacer()
    }
    if let error=game.error {Text(error).font(.caption);Button("Try again"){Task{await game.retry()}}.buttonStyle(.bordered)}
   }.padding(20)
  }
 }
 private var timer:some View {
  ZStack {
   Circle().stroke(.white.opacity(0.2),lineWidth:6)
   Circle().trim(from:0,to:game.remaining/10).stroke(Color(hex:"FFD494"),style:StrokeStyle(lineWidth:6,lineCap:.round)).rotationEffect(.degrees(-90))
   if game.reading {Image(systemName:"book.fill").font(.system(size:28))}
   else {Text(String(format:"%.1f",game.remaining)).font(.system(size:28,weight:.heavy,design:.rounded)).monospacedDigit()}
  }.frame(width:78,height:78).accessibilityLabel(game.reading ? "Read the question":"\(String(format:"%.1f",game.remaining)) seconds remaining")
 }
 private func answer(_ text:String,index:Int)->some View {
  let right=game.revealed && index==game.correctIndex
  let wrong=game.revealed && index==game.selected && !right
  return Button{Task{await game.answer(index)}}label:{
   HStack(spacing:12){Text(String(UnicodeScalar(65+index)!)).font(.headline);Text(text).font(.system(size:18,weight:.semibold)).lineLimit(4).minimumScaleFactor(0.65).multilineTextAlignment(.leading);Spacer();if right{Image(systemName:"checkmark.circle.fill").foregroundStyle(.green)}else if wrong{Image(systemName:"xmark.circle.fill").foregroundStyle(.red)}}.foregroundStyle(Color.ink).padding(15).frame(maxWidth:.infinity,maxHeight:.infinity,alignment:.leading).background(right ? Color(hex:"CCF3D7"):(wrong ? Color(hex:"FFDED7"):.white),in:RoundedRectangle(cornerRadius:17))
  }.buttonStyle(AnswerButtonStyle()).disabled(game.busy || game.revealed || game.reading || game.error != nil).accessibilityIdentifier("tournament-answer-\(index)")
 }
 private var result:some View {
  ScrollView {
   VStack(spacing:23) {
    Image(systemName:"flame.fill").font(.system(size:78)).foregroundStyle(Color(hex:"FFD494")).symbolEffect(.bounce,value:reduceMotion ? false:game.showResult).padding(.top,35)
    Text(game.score>game.event.best ? "NEW PERSONAL BEST":"RUN COMPLETE").font(.system(size:26,weight:.black,design:.rounded))
    Text("\(game.score)").font(.system(size:82,weight:.black,design:.rounded)).contentTransition(.numericText())
    Text("TOURNAMENT POINTS").font(.caption.bold()).tracking(2)
    Text("\(game.streak) correct before the run ended").font(.title3.bold())
    Text("Your best run counts against other players in this topic. Final places and prizes are awarded when the tournament closes.").multilineTextAlignment(.center).opacity(0.85)
    Button("Back to tournament"){dismiss()}.buttonStyle(PrimaryButton()).padding(.top,10)
   }.padding(28)
  }.accessibilityIdentifier("tournamentResult")
 }
}
