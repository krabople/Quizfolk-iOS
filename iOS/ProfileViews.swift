import SwiftUI

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
            Section {Link("Question source · Open Trivia Database",destination:URL(string:"https://opentdb.com/")!);Link("Question licence · CC BY-SA 4.0",destination:URL(string:"https://creativecommons.org/licenses/by-sa/4.0/")!)}
        }.navigationTitle("Duel review")
    }
}
struct LeagueView:View {
    @EnvironmentObject var store:QuizStore
    @State private var topicID=""
    @State private var weekly=true
    var body:some View {
        NavigationStack {
            ScrollView {
                BrandHeader(title:"Make a name.",subtitle:"Your knowledge deserves a little glory.")
                VStack(spacing:18) {
                    Image(systemName:"trophy.fill").font(.system(size:56)).foregroundStyle(Color(hex:"DCA83D")).padding(.top,10)
                    Text("The knowledge league").font(.system(size:24,weight:.bold,design:.rounded))
                    Picker("Period",selection:$weekly){Text("This week").tag(true);Text("All time").tag(false)}.pickerStyle(.segmented)
                    Picker("Topic",selection:$topicID){Text("All topics").tag("");ForEach(store.topics){Text($0.name).tag($0.id)}}.tint(.ink)
                    if store.apiURL.isEmpty {ContentUnavailableView("Leagues need a connection",systemImage:"network",description:Text("Add your quiz server in You to join the real player leaderboards. Offline practice stays on this device."))}
                    else if store.board.isEmpty {Text("No completed duels yet. Play an online duel to set the pace.").foregroundStyle(.secondary).multilineTextAlignment(.center)}
                    ForEach(Array(store.board.enumerated()),id:\.element.id){index,row in HStack(spacing:14){Text("\(index+1)").font(.system(size:20,weight:.bold,design:.rounded)).foregroundStyle(index<3 ? Color(hex:"C28D2F"):Color.ink).frame(width:30);VStack(alignment:.leading){Text(row.name).font(.headline);Text("\(row.matches) duels").font(.caption).foregroundStyle(.secondary)};Spacer();Text("\(row.xp) XP").font(.headline)}.padding(17).background(.white,in:RoundedRectangle(cornerRadius:14))}
                    if let error=store.onlineError {Text(error).font(.caption).foregroundStyle(.red)}
                    Text("Weekly leagues reset Monday at 00:00 UTC. Only completed online duels count. Bots never appear on the board.").font(.caption).foregroundStyle(.secondary).multilineTextAlignment(.center)
                    Button("Refresh league"){Task{await refresh()}}.buttonStyle(.bordered).disabled(store.apiURL.isEmpty)
                }.padding(.horizontal,22)
            }.background(Color.canvas).toolbar(.hidden,for:.navigationBar)
        }.task{await refresh()}.onChange(of:topicID){_,_ in Task{await refresh()}}.onChange(of:weekly){_,_ in Task{await refresh()}}
    }
    private func refresh()async {if !store.apiURL.isEmpty {await store.loadBoard(topicID:topicID,weekly:weekly)}}
}
struct ProfileView:View {
    @EnvironmentObject var store:QuizStore
    @State private var saved=false
    @State private var deleteAccount=false
    var correct:Int {store.history.flatMap{$0.rounds}.filter{$0.selected==$0.question.correctIndex}.count}
    var total:Int {store.history.flatMap{$0.rounds}.count}
    var wins:Int {store.history.filter{$0.won}.count}
    var body:some View {
        NavigationStack {
            ScrollView {
                BrandHeader(title:"A curious mind.",subtitle:"Look how far your knowledge takes you.")
                VStack(spacing:18) {
                    Image(systemName:"person.fill").font(.system(size:42)).foregroundStyle(Color.coral).frame(width:100,height:100).background(Color.coral.opacity(0.1),in:Circle())
                    Text(store.name).font(.system(size:25,weight:.bold,design:.rounded))
                    Text("LEVEL \(1+store.xp/500) · \(store.xp.formatted()) LOCAL XP").font(.system(size:11,weight:.heavy)).tracking(1).foregroundStyle(.secondary)
                    HStack{metric("\(store.history.count)","Duels");metric("\(wins)","Wins");metric(total==0 ? "—":"\(Int(Double(correct)/Double(total)*100))%","Accuracy")}.padding(.vertical,18).background(.white,in:RoundedRectangle(cornerRadius:17))
                    VStack(alignment:.leading,spacing:14){Text("Your topic journey").font(.headline);ForEach(store.topics.filter{store.favourites.contains($0.id) || store.level($0)>1}){topic in HStack{Text(topic.emoji);Text(topic.name).font(.subheadline);Spacer();Text("Lv. \(store.level(topic))").font(.caption).bold().foregroundStyle(topic.tint)}}}.frame(maxWidth:.infinity,alignment:.leading)
                    settings
                    VStack(alignment:.leading,spacing:8){Text("Made for curious people").font(.headline);Text("Quizfolk is an independent app inspired by classic topic-based trivia. It is not affiliated with QuizUp. Questions are community-contributed and may contain errors. Use the review screen to check the correct answer.").font(.caption).foregroundStyle(.secondary);Link("Open Trivia Database · Question source",destination:URL(string:"https://opentdb.com/")!);Link("CC BY-SA 4.0 · Question data licence",destination:URL(string:"https://creativecommons.org/licenses/by-sa/4.0/")!)}.font(.caption).frame(maxWidth:.infinity,alignment:.leading)
                }.padding(.horizontal,22).padding(.bottom,25)
            }.background(Color.canvas).toolbar(.hidden,for:.navigationBar)
        }.confirmationDialog("Delete your online player account and server match history? Your local practice history will remain on this device.",isPresented:$deleteAccount,titleVisibility:.visible){Button("Delete online account",role:.destructive){Task{await store.deleteAccount();saved=false}}}
    }
    private var settings:some View {
        VStack(alignment:.leading,spacing:12) {
            Text("Your player card").font(.headline)
            TextField("Display name",text:$store.name).textFieldStyle(.roundedBorder).textContentType(.nickname)
            Text("Quiz server").font(.headline).padding(.top,7)
            TextField("https://quiz.example.com/index.php",text:$store.apiURL).textFieldStyle(.roundedBorder).textInputAutocapitalization(.never).autocorrectionDisabled().keyboardType(.URL)
            Text("Offline practice works immediately. Online duels and leagues use your separately deployed server. Your account key is stored securely in Keychain on this device; account recovery is not yet available.").font(.caption).foregroundStyle(.secondary)
            Button("Save and connect"){store.saveSettings();Task{await store.connect();saved=store.onlineError==nil}}.buttonStyle(PrimaryButton())
            if saved,let p=store.profile {Text("Connected · \(p.matches) online duels · \(p.xp) XP").font(.caption).foregroundStyle(.green)}
            if let error=store.onlineError {Text(error).font(.caption).foregroundStyle(.red)}
            if store.profile != nil {Button("Delete online account",role:.destructive){deleteAccount=true}.font(.caption)}
        }.padding(18).background(.white,in:RoundedRectangle(cornerRadius:17))
    }
    private func metric(_ value:String,_ label:String)->some View {VStack(spacing:5){Text(value).font(.system(size:25,weight:.bold,design:.rounded));Text(label).font(.caption).foregroundStyle(.secondary)}.frame(maxWidth:.infinity)}
}
