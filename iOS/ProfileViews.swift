import SwiftUI
import PhotosUI

struct HistoryView:View {
    @EnvironmentObject var store:QuizStore
    var body:some View {
        NavigationStack {
            ScrollView {
                BrandHeader(title:"Good rivalries.",subtitle:"Every duel has a story.")
                if store.history.isEmpty {ContentUnavailableView("Your first rival is waiting",systemImage:"bolt.horizontal.circle",description:Text("Pick a topic in Discover and play your first duel."))}
                LazyVStack(spacing:12){ForEach(store.history){match in
                    NavigationLink{MatchDetailView(match:match)}label:{
                        HStack(spacing:13){Text(store.topics.first{$0.id==match.topicID}?.emoji ?? "🧠").font(.largeTitle);VStack(alignment:.leading,spacing:5){Text(store.topics.first{$0.id==match.topicID}?.name ?? "Trivia").font(.headline);Text("vs \(match.opponent)").font(.caption).foregroundStyle(.secondary);Text(match.kind=="human" ? "Recorded human run":(match.kind=="practice" ? "Offline practice":"Bot duel")).font(.system(size:10)).foregroundStyle(.secondary)};Spacer();VStack(alignment:.trailing,spacing:5){Text("\(match.score)–\(match.opponentScore)").font(.headline);Text(match.tied ? "DRAW":(match.won ? "WON":"LOST")).font(.system(size:10,weight:.heavy)).foregroundStyle(match.won ? .green:Color.coral);Text(match.date,style:.date).font(.system(size:9)).foregroundStyle(.secondary)}}.padding(16).background(.white,in:RoundedRectangle(cornerRadius:16)).foregroundStyle(Color.ink)
                    }.buttonStyle(.plain)
                }}.padding(.horizontal,22)
            }.background(Color.canvas).toolbar(.hidden,for:.navigationBar)
        }
    }
}
struct MatchDetailView:View {
    let match:MatchRecord
    var body:some View {
        List {
            Section("\(match.score) – \(match.opponentScore) vs \(match.opponent)") {
                ForEach(Array(match.rounds.enumerated()),id:\.element.id){i,r in VStack(alignment:.leading,spacing:8){Text("\(i+1). \(r.question.prompt)").font(.headline);Text("Correct: \(r.question.answers[r.question.correctIndex])");Text("Your answer: \(r.selected>=0 && r.selected<4 ? r.question.answers[r.selected]:"Timed out")").foregroundStyle(.secondary);Text("\(r.points) points · \(r.elapsed, specifier:"%.1f") seconds").font(.caption)}}
            }
            Section {Link("Question source · Open Trivia Database",destination:URL(string:"https://opentdb.com/")!);Link("Question source · OpenTriviaQA contributors",destination:URL(string:"https://github.com/uberspot/OpenTriviaQA")!);Link("Question licence · CC BY-SA 4.0",destination:URL(string:"https://creativecommons.org/licenses/by-sa/4.0/")!)}
        }.navigationTitle("Duel review")
    }
}
struct LeagueView:View {
    @EnvironmentObject var store:QuizStore
    var initialTopicID:String? = nil
    @State private var topicID="9"
    @State private var monthly=true
    var body:some View {
        NavigationStack {
            ScrollView {
                BrandHeader(title:"Make a name.",subtitle:"Your knowledge deserves a little glory.")
                VStack(spacing:18) {
                    Image(systemName:"trophy.fill").font(.system(size:56)).foregroundStyle(Color(hex:"DCA83D")).padding(.top,10)
                    Text("\(store.topics.first{$0.id==topicID}?.emoji ?? "🏆") \(store.topics.first{$0.id==topicID}?.name ?? "Topic") league").font(.system(size:24,weight:.bold,design:.rounded))
                    Picker("Period",selection:$monthly){Text("This month").tag(true);Text("All time").tag(false)}.pickerStyle(.segmented)
                    Picker("Topic",selection:$topicID){ForEach(store.topics){Text($0.name).tag($0.id)}}.tint(.ink).accessibilityIdentifier("leagueTopic")
                    if store.apiURL.isEmpty {ContentUnavailableView("Leagues need a connection",systemImage:"network",description:Text("Add your quiz server in You to join the real player leaderboards. Offline practice stays on this device."))}
                    else if store.board.isEmpty {Text("No completed duels yet. Play an online duel to set the pace.").foregroundStyle(.secondary).multilineTextAlignment(.center)}
                    ForEach(Array(store.board.enumerated()),id:\.element.id){index,row in HStack(spacing:14){Text("\(index+1)").font(.system(size:20,weight:.bold,design:.rounded)).foregroundStyle(index<3 ? Color(hex:"C28D2F"):Color.ink).frame(width:30);PlayerPortrait(name:row.name,avatar:row.avatar,size:34);VStack(alignment:.leading){Text(row.name).font(.headline);Text("\(row.matches) duels").font(.caption).foregroundStyle(.secondary)};Spacer();Text("\(row.xp) XP").font(.headline)}.padding(17).background(.white,in:RoundedRectangle(cornerRadius:14))}
                    if let error=store.onlineError {Text(error).font(.caption).foregroundStyle(.red)}
                    Text("Every topic has its own league. Monthly tables reset on the first day at 00:00 UTC. Topic XP = match score + 40 for finishing + 100 for a win or 50 for a draw. No paid multipliers. Offline practice does not enter the league.").font(.caption).foregroundStyle(.secondary).multilineTextAlignment(.center)
                    Button("Refresh league"){Task{await refresh()}}.buttonStyle(.bordered).disabled(store.apiURL.isEmpty)
                }.padding(.horizontal,22)
            }.background(Color.canvas).toolbar(.hidden,for:.navigationBar)
        }.task{if let selected=initialTopicID {topicID=selected};await refresh()}.onChange(of:topicID){_,_ in Task{await refresh()}}.onChange(of:monthly){_,_ in Task{await refresh()}}
    }
    private func refresh()async {if !store.apiURL.isEmpty {await store.loadBoard(topicID:topicID,monthly:monthly)}}
}
struct ProfileView:View {
    @EnvironmentObject var store:QuizStore
    @State private var saved=false
    @State private var deleteAccount=false
    @State private var draftName=""
    @State private var selectedPhoto:PhotosPickerItem?
    @State private var pendingPicture:Data?
    @State private var pictureError:String?
    @State private var showPicturePreview=false
    var correct:Int {store.history.flatMap{$0.rounds}.filter{$0.selected==$0.question.correctIndex}.count}
    var total:Int {store.history.flatMap{$0.rounds}.count}
    var wins:Int {store.history.filter{$0.won}.count}
    var body:some View {
        NavigationStack {
            ScrollView {
                BrandHeader(title:"A curious mind.",subtitle:"Look how far your knowledge takes you.")
                VStack(spacing:18) {
                    PlayerPortrait(name:store.name,avatar:store.avatar,size:100)
                    PhotosPicker(selection:$selectedPhoto,matching:.images,photoLibrary:.shared()){Label("Change profile picture",systemImage:"photo")}
                        .disabled(store.profileBusy).accessibilityIdentifier("changeProfilePicture")
                    if store.avatar != nil {Button("Remove profile picture",role:.destructive){Task{await store.changeAvatar(nil)}}.font(.caption).disabled(store.profileBusy)}
                    if let pictureError {Text(pictureError).font(.caption).foregroundStyle(.red)}
                    Text(store.name).font(.system(size:25,weight:.bold,design:.rounded))
                    Text("LEVEL \(1+store.xp/500) · \(store.xp.formatted()) LOCAL XP").font(.system(size:11,weight:.heavy)).tracking(1).foregroundStyle(.secondary)
                    HStack{metric("\(store.history.count)","Duels");metric("\(wins)","Wins");metric(total==0 ? "—":"\(Int(Double(correct)/Double(total)*100))%","Accuracy")}.padding(.vertical,18).background(.white,in:RoundedRectangle(cornerRadius:17))
                    VStack(alignment:.leading,spacing:14){Text("Your topic journey").font(.headline);ForEach(store.topics.filter{store.favourites.contains($0.id) || store.level($0)>1}){topic in HStack{Text(topic.emoji);Text(topic.name).font(.subheadline);Spacer();Text("Lv. \(store.level(topic))").font(.caption).bold().foregroundStyle(topic.tint)}}}.frame(maxWidth:.infinity,alignment:.leading)
                    settings
                    VStack(alignment:.leading,spacing:8){Text("Made for curious people").font(.headline);Text("Quizfolk is an independent app inspired by classic topic-based trivia. It is not affiliated with QuizUp. Questions are community-contributed and may contain errors. Use the review screen to check the correct answer.").font(.caption).foregroundStyle(.secondary);Link("Open Trivia Database · Question source",destination:URL(string:"https://opentdb.com/")!);Link("CC BY-SA 4.0 · Question data licence",destination:URL(string:"https://creativecommons.org/licenses/by-sa/4.0/")!)}.font(.caption).frame(maxWidth:.infinity,alignment:.leading)
                    Link("Privacy policy",destination:URL(string:"https://www.ways2earn.com/quizfolk-api/privacy.html")!).font(.caption)
                }.padding(.horizontal,22).padding(.bottom,25)
            }.background(Color.canvas).toolbar(.hidden,for:.navigationBar)
        }.onAppear{draftName=store.name}.onChange(of:store.name){old,value in if draftName==old {draftName=value}}
        .onChange(of:selectedPhoto){_,item in Task{do {guard let data=try await item?.loadTransferable(type:Data.self) else {return};pendingPicture=try ProfilePicture.make(data);pictureError=nil;showPicturePreview=true} catch {pictureError=error.localizedDescription};selectedPhoto=nil}}
        .sheet(isPresented:$showPicturePreview){NavigationStack{VStack(spacing:24){Text("Your player picture").font(.title2.bold());PlayerPortrait(name:store.name,avatar:pendingPicture?.base64EncodedString(),size:200);Text("This square crop will appear on your player card, in duels and in leagues. Photo location and other metadata are removed.").font(.subheadline).multilineTextAlignment(.center);Button("Use this picture"){showPicturePreview=false;Task{await store.changeAvatar(pendingPicture)}}.buttonStyle(PrimaryButton());Button("Cancel"){showPicturePreview=false}}.padding(28)}}
        .confirmationDialog("Delete your online player account and server match history? Your local practice history will remain on this device.",isPresented:$deleteAccount,titleVisibility:.visible){Button("Delete online account",role:.destructive){Task{await store.deleteAccount();saved=false}}}
    }
    private var settings:some View {
        VStack(alignment:.leading,spacing:12) {
            Text("Your player card").font(.headline)
            TextField("Display name",text:$draftName).textFieldStyle(.roundedBorder).textContentType(.nickname).autocorrectionDisabled().accessibilityIdentifier("playerName")
            Text("Player names are unique. Capitalisation and repeated spaces do not create a different name. Your current name is kept if a new one is taken.").font(.caption).foregroundStyle(.secondary)
            Text("Your name appears in online duels and leagues. Your player account stays on this iPhone; cross-device account recovery is not available yet.").font(.caption).foregroundStyle(.secondary)
            Button("Save player card"){store.saveSettings();Task{await store.changeName(to:draftName);saved=store.onlineError==nil;if saved {draftName=store.name}}}.buttonStyle(PrimaryButton()).disabled(store.profileBusy)
            DisclosureGroup("Advanced connection settings") {
                TextField("HTTPS service address",text:$store.apiURL).textFieldStyle(.roundedBorder).textInputAutocapitalization(.never).autocorrectionDisabled().keyboardType(.URL)
                Text("Only change this if you run your own quiz service. Changing the address creates a separate player account.").font(.caption).foregroundStyle(.secondary)
            }.font(.caption)
            if saved,let p=store.profile {Text("Connected · \(p.matches) online duels · \(p.xp) XP").font(.caption).foregroundStyle(.green)}
            if let error=store.onlineError {Text(error).font(.caption).foregroundStyle(.red)}
            if store.profile != nil {Button("Delete online account",role:.destructive){deleteAccount=true}.font(.caption)}
        }.padding(18).background(.white,in:RoundedRectangle(cornerRadius:17))
    }
    private func metric(_ value:String,_ label:String)->some View {VStack(spacing:5){Text(value).font(.system(size:25,weight:.bold,design:.rounded));Text(label).font(.caption).foregroundStyle(.secondary)}.frame(maxWidth:.infinity)}
}
