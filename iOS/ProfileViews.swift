import SwiftUI
import PhotosUI

struct HistoryView:View {
    @EnvironmentObject var store:QuizStore
    var body:some View {
        NavigationStack {
            QuizPageScroll(maxWidth:900) {
                BrandHeader(title:"Good rivalries.",subtitle:"Every duel has a story.")
                if store.history.isEmpty {ContentUnavailableView("Your first rival is waiting",systemImage:"bolt.horizontal.circle",description:Text("Pick a topic in Discover and play your first duel."))}
                LazyVStack(spacing:12){ForEach(store.history){match in
                    NavigationLink{MatchDetailView(match:match)}label:{
                        HStack(spacing:13){Text(store.topics.first{$0.id==match.topicID}?.emoji ?? "🧠").font(.largeTitle);VStack(alignment:.leading,spacing:5){Text(store.topics.first{$0.id==match.topicID}?.name ?? "Trivia").font(.headline);Text("vs \(match.opponent)").font(.caption).foregroundStyle(.secondary);Text(match.kind=="challenge" ? "Asynchronous challenge":(match.kind=="human" ? "Recorded human run":(match.kind=="practice" ? "Offline practice":"Bot duel"))).font(.system(size:10)).foregroundStyle(.secondary)};Spacer();VStack(alignment:.trailing,spacing:5){Text("\(match.score)–\(match.opponentScore)").font(.headline);Text(match.pending==true ? "WAITING":(match.tied ? "DRAW":(match.won ? "WON":"LOST"))).font(.system(size:10,weight:.heavy)).foregroundStyle(match.won ? .green:Color.coral);Text(match.date,style:.date).font(.system(size:9)).foregroundStyle(.secondary)}}.padding(16).background(.white,in:RoundedRectangle(cornerRadius:16)).foregroundStyle(Color.ink)
                    }.buttonStyle(.plain).accessibilityIdentifier("history-match-\(match.id)")
                }}.padding(.horizontal,22)
            }.background(Color.canvas).toolbar(.hidden,for:.navigationBar)
        }
    }
}
struct MatchDetailView:View {
    @EnvironmentObject private var store:QuizStore
    let match:MatchRecord
    @State private var session:GameSession?
    @State private var rematching=false
    @State private var rematchError:String?
    @State private var requestID=UUID().uuidString
    var body:some View {
        List {
            if match.rounds.count==7,let topic=store.topics.first(where:{$0.id==match.topicID}) {
                Button("View result"){session=GameSession(topic:topic,store:store,record:match)}.accessibilityIdentifier("historyResult")
            }
            if let id=match.opponentID {
                Section("Your opponent") {
                    NavigationLink {PublicPlayerView(playerID:id)}label:{HStack(spacing:14){PlayerPortrait(name:match.opponent,avatar:match.opponentAvatar,size:52);VStack(alignment:.leading,spacing:4){Text(match.opponent).font(.headline);Text("View profile & follow").font(.caption).foregroundStyle(.secondary)}}}.accessibilityIdentifier("historyOpponentProfile")
                }
            }
            if match.pending != true,(match.opponentID != nil || match.kind=="bot" || match.kind=="practice"),let topic=store.topics.first(where:{$0.id==match.topicID}) {
                Section {
                    Button(rematching ? "Preparing rematch…":"Rematch"){Task{rematching=true;defer{rematching=false};do{session=try await store.rematch(topic:topic,opponentID:match.opponentID,online:match.kind != "practice",requestID:requestID);rematchError=nil}catch{rematchError=error.localizedDescription}}}.disabled(rematching).accessibilityIdentifier("historyRematch")
                    if let rematchError {Text(rematchError).foregroundStyle(.red).font(.caption)}
                }
            }
            Section(match.pending==true ? "\(match.score) points · waiting for \(match.opponent)":"\(match.score) – \(match.opponentScore) vs \(match.opponent)") {
                ForEach(Array(match.rounds.enumerated()),id:\.element.id){i,r in VStack(alignment:.leading,spacing:8){Text("\(i+1). \(r.question.prompt)").font(.headline);Text("Correct: \(r.question.answers[r.question.correctIndex])");Text("Your answer: \(r.selected>=0 && r.selected<4 ? r.question.answers[r.selected]:"Timed out")").foregroundStyle(.secondary);Text("\(r.points) points · \(r.elapsed, specifier:"%.1f") seconds").font(.caption)}}
            }
        }.navigationTitle("Duel review")
            .fullScreenCover(item:$session,onDismiss:{requestID=UUID().uuidString}){GameView(game:$0).environmentObject(store)}
    }
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
    var correct:Int {store.history.flatMap{$0.rounds}.filter{$0.points>0}.count}
    var total:Int {store.history.flatMap{$0.rounds}.count}
    var wins:Int {store.history.filter{$0.won}.count}
    var body:some View {
        NavigationStack {
            QuizPageScroll(maxWidth:860) {
                BrandHeader(title:"A curious mind.",subtitle:"Look how far your knowledge takes you.")
                VStack(spacing:18) {
                    PlayerPortrait(name:store.name,avatar:store.avatar,size:100,badge:store.ownCard?.displayBadge)
                    PhotosPicker(selection:$selectedPhoto,matching:.images,photoLibrary:.shared()){Label("Change profile picture",systemImage:"photo")}
                        .disabled(store.profileBusy).accessibilityIdentifier("changeProfilePicture")
                    if store.avatar != nil {Button("Remove profile picture",role:.destructive){Task{await store.changeAvatar(nil)}}.font(.caption).disabled(store.profileBusy)}
                    if let pictureError {Text(pictureError).font(.caption).foregroundStyle(.red)}
                    Text(store.name).font(.system(size:25,weight:.bold,design:.rounded))
                    HStack(spacing:12){
                        NavigationLink{CoinTrailView()}label:{profileAction("Earn coins",symbol:"",coin:true)}.accessibilityLabel("Earn coins")
                        NavigationLink{TournamentBadgePicker()}label:{profileAction("Tournament badges",symbol:"trophy.fill")}.accessibilityLabel("Tournament badges")
                    }.buttonStyle(.plain)
                    Text("A DIFFERENT LEVEL IN EVERY TOPIC").font(.system(size:11,weight:.heavy)).tracking(1).foregroundStyle(.secondary)
                    if let id=store.profile?.id{NavigationLink{PublicPlayerView(playerID:id)}label:{HStack(spacing:12){Image(systemName:"person.text.rectangle.fill");Text("Your public card, titles & achievements").multilineTextAlignment(.leading);Spacer(minLength:0);Image(systemName:"chevron.right").font(.caption)}.font(.subheadline.bold()).padding(17).frame(maxWidth:.infinity,alignment:.leading).foregroundStyle(.white).background(Color.ink,in:RoundedRectangle(cornerRadius:16))}.buttonStyle(.plain)}
                    NavigationLink{NotificationSettingsView()}label:{Label("Notifications",systemImage:"bell.badge.fill").font(.headline).frame(maxWidth:.infinity).padding(17).background(.white,in:RoundedRectangle(cornerRadius:16))}.buttonStyle(.plain).accessibilityIdentifier("notificationSettings")
                    HStack{metric("\(store.history.count)","Duels");metric("\(wins)","Wins");metric(total==0 ? "—":"\(Int(Double(correct)/Double(total)*100))%","Accuracy")}.padding(.vertical,18).background(.white,in:RoundedRectangle(cornerRadius:17))
                    VStack(alignment:.leading,spacing:14){Text("Your topic journey").font(.headline);ForEach(store.topics.filter{store.favourites.contains($0.id) || store.topicXP($0)>0}){topic in VStack(alignment:.leading,spacing:8){Text(topic.emoji+" "+topic.name).font(.subheadline.bold());TopicLevelProgress(topic:topic,xp:store.topicXP(topic))}}}.frame(maxWidth:.infinity,alignment:.leading)
                    settings
                    VStack(alignment:.leading,spacing:8){Text("Made for curious people").font(.headline);Text("Quizfolk is an independent app inspired by classic topic-based trivia. It is not affiliated with QuizUp. Questions have been individually reviewed and edited for clarity, accuracy and topic relevance. Use the duel review to see each correct answer.").font(.caption).foregroundStyle(.secondary);Link("Credits & licences",destination:URL(string:"https://www.ways2earn.com/quizfolk-api/credits.html")!)}.font(.caption).frame(maxWidth:.infinity,alignment:.leading)
                    Link("Privacy policy",destination:URL(string:"https://www.ways2earn.com/quizfolk-api/privacy.html")!).font(.caption)
                }.padding(.horizontal,22).padding(.bottom,25)
            }.background(Color.canvas).toolbar(.hidden,for:.navigationBar)
        }.onAppear{draftName=store.name}.onChange(of:store.name){old,value in if draftName==old {draftName=value}}
        .onChange(of:selectedPhoto){_,item in Task{do {guard let data=try await item?.loadTransferable(type:Data.self) else {return};pendingPicture=try ProfilePicture.make(data);pictureError=nil;showPicturePreview=true} catch {pictureError=error.localizedDescription};selectedPhoto=nil}}
        .sheet(isPresented:$showPicturePreview){
            NavigationStack {
                GeometryReader { geometry in
                    QuizPageScroll(maxWidth:600) {
                        VStack(spacing:24) {
                            Text("Your player picture").font(.title2.bold())
                            PlayerPortrait(name:store.name,avatar:pendingPicture?.base64EncodedString(),size:200)
                            Text("This square crop will appear on your player card, in duels and in leagues. Photo location and other metadata are removed.").font(.subheadline).multilineTextAlignment(.center)
                            Button("Use this picture"){showPicturePreview=false;Task{await store.changeAvatar(pendingPicture)}}.buttonStyle(PrimaryButton())
                            Button("Cancel"){showPicturePreview=false}
                        }.padding(28).frame(minHeight:geometry.size.height)
                    }
                }
            }
        }
        .confirmationDialog("Delete your online player account and server match history? Your local practice history will remain on this device.",isPresented:$deleteAccount,titleVisibility:.visible){Button("Delete online account",role:.destructive){Task{await store.deleteAccount();saved=false}}}
    }
    private var settings:some View {
        VStack(alignment:.leading,spacing:12) {
            Text("Your player card").font(.headline)
            TextField("Display name",text:$draftName).textFieldStyle(.roundedBorder).textContentType(.nickname).autocorrectionDisabled().accessibilityIdentifier("playerName")
            Text("Player names are unique. Capitalisation and repeated spaces do not create a different name. Your current name is kept if a new one is taken.").font(.caption).foregroundStyle(.secondary)
            Text("Your name appears in online duels and leagues. Your player account stays on this device; cross-device account recovery is not available yet.").font(.caption).foregroundStyle(.secondary)
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
    private func profileAction(_ title:String,symbol:String,coin:Bool=false)->some View {
        VStack(spacing:9){if coin{CoinSymbol(size:27)}else{Image(systemName:symbol).font(.system(size:26)).foregroundStyle(Color.coral)};Text(title).font(.system(size:15,weight:.semibold)).multilineTextAlignment(.center).lineLimit(2)}
            .frame(maxWidth:.infinity).frame(height:90).background(.white,in:RoundedRectangle(cornerRadius:16)).overlay{RoundedRectangle(cornerRadius:16).stroke(Color.ink.opacity(0.12))}.foregroundStyle(Color.ink)
    }
    private func metric(_ value:String,_ label:String)->some View {VStack(spacing:5){Text(value).font(.system(size:25,weight:.bold,design:.rounded));Text(label).font(.caption).foregroundStyle(.secondary)}.frame(maxWidth:.infinity)}
}
