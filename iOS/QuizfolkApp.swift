import SwiftUI

@main struct QuizfolkApp: App {
    @StateObject private var store=QuizStore()
    var body:some Scene {WindowGroup {RootView().environmentObject(store).preferredColorScheme(.light)}}
}
struct RootView:View {
    @EnvironmentObject var store:QuizStore
    @Environment(\.scenePhase) private var scenePhase
    @State private var tab=0
    @State private var interests=false
    @AppStorage("didChooseInterests") private var didChoose=false
    var body:some View {
        TabView(selection:$tab) {
            DiscoverView().tabItem{Label("Discover",systemImage:"square.grid.2x2.fill")}.tag(0)
            DuelsView().tabItem{Label("Duels",systemImage:"bolt.horizontal.fill")}.tag(1)
            TournamentsView().tabItem{Label("Tournaments",systemImage:"trophy.fill")}.tag(2)
            PeopleView().tabItem{Label("People",systemImage:"person.2.fill")}.tag(4)
            ProfileView().tabItem{Label("You",systemImage:"person.crop.circle.fill")}.tag(3)
        }.tint(.coral)
        .onAppear{if !didChoose {interests=true}}
        .accessibilityHidden(!interests && !store.pendingPrizes.isEmpty)
        .overlay{if !interests,let prize=store.pendingPrizes.first {TournamentPrizePopup(prize:prize).id(prize.id)}}
        .task {await store.connect();await store.refreshSocial();await store.loadPrizes()}
        .onChange(of:scenePhase){_,phase in if phase == .active {Task{await store.refreshSocial();await store.loadPrizes()}}}
        .sheet(isPresented:$interests,onDismiss:{didChoose=true}){InterestsView()}
        .alert("Question bank unavailable",isPresented:Binding(get:{store.loadError != nil},set:{_ in store.loadError=nil})){Button("OK",role:.cancel){}}message:{Text(store.loadError ?? "")}
    }
}
struct BrandHeader:View {
    var title:String
    var subtitle:String
    var body:some View {
        HStack(alignment:.center) {
            VStack(alignment:.leading,spacing:7) {
                Text("quizfolk").font(.system(size:21,weight:.black,design:.rounded)).tracking(-1).foregroundStyle(Color.coral)
                Text(title).font(.system(size:32,weight:.bold,design:.rounded)).foregroundStyle(Color.ink)
                Text(subtitle).font(.subheadline).foregroundStyle(.secondary)
            }
            Spacer()
            Image("BrandMark").resizable().scaledToFit().frame(width:54,height:54).clipShape(RoundedRectangle(cornerRadius:14)).accessibilityLabel("Quizfolk logo")
        }.padding(.horizontal,22).padding(.top,16).padding(.bottom,14)
    }
}
struct DiscoverView:View {
    @EnvironmentObject var store:QuizStore
    @State private var search=""
    @State private var onlyFavourites=false
    @State private var interests=false
    private var visible:[Topic] {store.topics.filter{(!onlyFavourites || store.favourites.contains($0.id)) && (search.isEmpty || $0.name.localizedCaseInsensitiveContains(search))}}
    var body:some View {
        NavigationStack {
            ScrollView {
                BrandHeader(title:"Find your people.",subtitle:"A little knowledge. A great rivalry.")
                HStack(spacing:12) {
                    Image(systemName:"magnifyingglass").foregroundStyle(.secondary)
                    TextField("Find your favourite subject",text:$search).accessibilityLabel("Search categories")
                }.padding(15).background(.white,in:RoundedRectangle(cornerRadius:14)).padding(.horizontal,22)
                hero.padding(.horizontal,22).padding(.top,8)
                HStack {
                    Text("Your next obsession").font(.system(size:21,weight:.bold,design:.rounded))
                    Spacer()
                    Button{interests=true}label:{Image(systemName:"slider.horizontal.3").padding(10)}.accessibilityLabel("Choose interests")
                }.foregroundStyle(Color.ink).padding(.horizontal,22).padding(.top,15)
                HStack(spacing:8) {
                    filter("All topics",selected:!onlyFavourites){onlyFavourites=false}
                    filter("My interests",selected:onlyFavourites){onlyFavourites=true}
                    Spacer()
                    Text("\(visible.count) topics").font(.caption).foregroundStyle(.secondary)
                }.padding(.horizontal,22)
                Text("Open a topic to play, see your level or view its league.").font(.caption).foregroundStyle(.secondary).padding(.horizontal,22)
                LazyVGrid(columns:[GridItem(.flexible(),spacing:12),GridItem(.flexible(),spacing:12)],spacing:12) {
                    ForEach(visible){topic in NavigationLink{TopicView(topic:topic)}label:{TopicTile(topic:topic,level:store.level(topic),favourite:store.favourites.contains(topic.id))}.buttonStyle(.plain).accessibilityIdentifier("topic-\(topic.id)")}
                }.padding(.horizontal,22).padding(.vertical,12)
                if visible.isEmpty {ContentUnavailableView("No topics found",systemImage:"magnifyingglass",description:Text("Try another search or choose some interests."))}
                Text("\(store.questions.count.formatted()) questions. So many ways to shine.").font(.caption).foregroundStyle(.secondary).padding(.bottom,20)
            }.background(Color.canvas).toolbar(.hidden,for:.navigationBar)
        }.sheet(isPresented:$interests){InterestsView()}
    }
    private var hero:some View {
        HStack(spacing:8) {
            VStack(alignment:.leading,spacing:10) {
                Text("THE CLASSIC DUEL").font(.system(size:10,weight:.heavy)).tracking(2).opacity(0.85)
                Text("Big on rivalry.\nEasy on your time.").font(.system(size:24,weight:.bold,design:.rounded))
                Text("7 questions · 10 seconds · 1 winner").font(.system(size:12,weight:.medium))
            }
            Spacer(minLength:0)
            Image(systemName:"bolt.fill").font(.system(size:56,weight:.black)).rotationEffect(.degrees(12)).foregroundStyle(Color(hex:"FFD79F"))
        }.foregroundStyle(.white).padding(22).frame(maxWidth:.infinity,alignment:.leading).background(Color.coral,in:RoundedRectangle(cornerRadius:20))
    }
    private func filter(_ title:String,selected:Bool,action:@escaping()->Void)->some View {
        Button(action:action){Text(title).font(.system(size:12,weight:.semibold)).padding(.horizontal,14).padding(.vertical,10).background(selected ? Color.ink:.white,in:Capsule()).foregroundStyle(selected ? .white:Color.ink)}
    }
}
struct TopicTile:View {
    let topic:Topic
    let level:Int
    var favourite=false
    var body:some View {
        VStack(alignment:.leading,spacing:12) {
            HStack {
                Text(topic.emoji).font(.system(size:34)).frame(width:66,height:66).background(.white.opacity(0.19),in:Circle())
                Spacer(minLength:0)
                if favourite {Image(systemName:"heart.fill").font(.caption).foregroundStyle(.white.opacity(0.85))}
            }
            VStack(alignment:.leading,spacing:5) {
                Text(topic.name).font(.system(size:17,weight:.bold,design:.rounded)).lineLimit(2).minimumScaleFactor(0.85).frame(height:42,alignment:.topLeading)
                Text("Lv. \(level) · Play & league").font(.system(size:10,weight:.medium)).opacity(0.9)
            }
            Capsule().fill(.white.opacity(0.22)).frame(height:3).overlay(alignment:.leading){Capsule().fill(.white.opacity(0.8)).frame(width:CGFloat(min(110,level*9)),height:3)}
        }.foregroundStyle(.white).padding(17).frame(maxWidth:.infinity).frame(height:190,alignment:.topLeading).background(topic.tint,in:RoundedRectangle(cornerRadius:18))
        .accessibilityElement(children:.combine)
    }
}
struct InterestsView:View {
    @EnvironmentObject var store:QuizStore
    @Environment(\.dismiss) var dismiss
    var body:some View {
        NavigationStack {
            ScrollView {
                Text("What makes you tick?").font(.system(size:29,weight:.bold,design:.rounded)).frame(maxWidth:.infinity,alignment:.leading).padding(.top,20)
                Text("Pick the topics you love. You can change these any time.").foregroundStyle(.secondary).frame(maxWidth:.infinity,alignment:.leading).padding(.bottom,14)
                LazyVGrid(columns:[GridItem(.flexible()),GridItem(.flexible())],spacing:10) {
                    ForEach(store.topics){topic in
                        Button{store.toggle(topic)}label:{
                            HStack{Text(topic.emoji);Text(topic.name).font(.system(size:13,weight:.semibold));Spacer(minLength:0);Image(systemName:store.favourites.contains(topic.id) ? "checkmark.circle.fill":"circle")}.foregroundStyle(store.favourites.contains(topic.id) ? .white:Color.ink).padding(14).frame(maxWidth:.infinity,minHeight:68).background(store.favourites.contains(topic.id) ? topic.tint:.white,in:RoundedRectangle(cornerRadius:13))
                        }.buttonStyle(.plain).accessibilityAddTraits(store.favourites.contains(topic.id) ? .isSelected:[])
                    }
                }
            }.padding(.horizontal,22).background(Color.canvas)
            .safeAreaInset(edge:.bottom){Button("Let’s play\(store.favourites.isEmpty ? "":" · \(store.favourites.count) interests")"){dismiss()}.buttonStyle(PrimaryButton()).padding().background(Color.canvas)}
            .toolbar{ToolbarItem(placement:.topBarTrailing){Button("Done"){dismiss()}}}
        }
    }
}
struct TopicView:View {
    @EnvironmentObject var store:QuizStore
    let topic:Topic
    @State private var session:GameSession?
    @State private var rankings=false
    var body:some View {
        ScrollView {
            VStack(spacing:18) {
                Text(topic.emoji).font(.system(size:64)).frame(width:112,height:112).background(topic.tint.opacity(0.15),in:Circle()).padding(.top,12)
                Text(topic.name).font(.system(size:31,weight:.bold,design:.rounded)).multilineTextAlignment(.center)
                Text("\(topic.questionCount) questions").font(.subheadline).foregroundStyle(.secondary)
                Picker("Topic page",selection:$rankings){Text("Play & progress").tag(false);Text("League").tag(true)}.pickerStyle(.segmented).accessibilityIdentifier("topicSection")
                if rankings {TopicLeaguePanel(topic:topic)}
                else {
                    TopicLevelProgress(topic:topic,xp:store.topicXP(topic))
                    Button{store.toggle(topic)}label:{Label(store.favourites.contains(topic.id) ? "Following topic":"Follow topic",systemImage:store.favourites.contains(topic.id) ? "heart.fill":"heart")}.tint(topic.tint)
                    HStack(spacing:0){stat("7","questions");stat("2s","to read");stat("10s","to answer")}.padding(.vertical,18).background(.white,in:RoundedRectangle(cornerRadius:18))
                    Text("We search for a human first. You can meet another searcher or face a recorded human run. A labelled bot is offered after six seconds when nobody is available. Play your own questions on your own schedule.").font(.subheadline).foregroundStyle(.secondary)
                    Button("Find a duel"){session=GameSession(topic:topic,store:store,online:true)}.buttonStyle(PrimaryButton(color:topic.tint))
                    Button("Practise against a bot"){session=GameSession(topic:topic,store:store,online:false)}.font(.headline).padding(12).tint(topic.tint)
                    Text("Correct: 11–20 points for speed. Final question counts double. Wrong answers and timeouts score zero. Maximum 160.").font(.caption).foregroundStyle(.secondary).multilineTextAlignment(.center)
                }
            }.padding(22)
        }.background(Color.canvas).foregroundStyle(Color.ink).navigationTitle(topic.name).navigationBarTitleDisplayMode(.inline).toolbar(.visible,for:.navigationBar)
        .fullScreenCover(item:$session){game in GameView(game:game).environmentObject(store)}
    }
    private func stat(_ value:String,_ label:String)->some View {VStack(spacing:5){Text(value).font(.system(size:25,weight:.bold,design:.rounded));Text(label).font(.caption).foregroundStyle(.secondary)}.frame(maxWidth:.infinity)}
}
struct PrimaryButton:ButtonStyle {
    var color:Color = .coral
    func makeBody(configuration:Configuration)->some View {configuration.label.font(.system(size:17,weight:.bold,design:.rounded)).foregroundStyle(.white).frame(maxWidth:.infinity).padding(.vertical,18).background(color.opacity(configuration.isPressed ? 0.75:1),in:RoundedRectangle(cornerRadius:15)).scaleEffect(configuration.isPressed ? 0.98:1)}
}
