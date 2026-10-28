import SwiftUI

struct TournamentPrize:Decodable,Identifiable,Equatable {
    let id:String
    let topicID:String
    let kind:String
    let rank:Int
    let coins:Int
    let date:Double
    let score:Int
    var placing:String {rank == 1 ? "1st place" : (rank == 2 ? "2nd place" : "3rd place")}
    var colour:Color {Color(hex:rank == 1 ? "C8952C" : (rank == 2 ? "7C8DA3" : "B66F47"))}
}
struct CoinTrailStatus:Decodable {
    let wallet:TournamentWallet
    let topics:[String]
    let earnedToday:Int
    let dailyMaximum:Int
    let completedDays:Int
    let weeklyBonusEarned:Bool
    let resets:Double
}
struct PrizeInbox:Decodable {let pending:[TournamentPrize];let earned:[TournamentPrize];let selected:TournamentPrize?}

extension QuizStore {
    private var usesCoinFixtures:Bool {
        #if DEBUG
        return isUITesting && testResponse == nil
        #else
        return false
        #endif
    }
    static var testPrize:TournamentPrize {TournamentPrize(id:"test-prize",topicID:"22",kind:"daily",rank:1,coins:75,date:1_793_145_600,score:120)}
    func loadPrizes() async {
        guard profile != nil,!prizesLoading else{return}
        if usesCoinFixtures {
            earnedPrizes=[Self.testPrize]
            if ProcessInfo.processInfo.arguments.contains("--prize-popup"),!testPrizeAcknowledged {
                pendingPrizes=[Self.testPrize]
            }
            return
        }
        prizesLoading=true;defer{prizesLoading=false}
        do {let reply:PrizeInbox=try await request("prizes");pendingPrizes=reply.pending;earnedPrizes=reply.earned}
        catch { /* A connection error leaves unseen results pending on the server. */ }
    }
    func acknowledgePrize(_ prize:TournamentPrize,wear:Bool) async throws {
        if usesCoinFixtures {testPrizeAcknowledged=true;pendingPrizes.removeAll{$0.id==prize.id};if wear {ownCard?.displayBadge=prize};return}
        if wear {let _:OKReply=try await request("select-badge",body:["event":prize.id])}
        let _:OKReply=try await request("prize-seen",body:["event":prize.id])
        pendingPrizes.removeAll{$0.id==prize.id}
        if wear {ownCard=try await request("player")}
    }
    func selectBadge(_ prize:TournamentPrize?) async throws {
        if usesCoinFixtures {ownCard?.displayBadge=prize;return}
        let value:Any=prize.map{$0.id as Any} ?? NSNull()
        let _:OKReply=try await request("select-badge",body:["event":value])
        ownCard=try await request("player")
    }
    func coinTrail() async throws -> CoinTrailStatus {
        if usesCoinFixtures {return CoinTrailStatus(wallet:TournamentWallet(coins:110,tickets:0,dailyClaimed:true),topics:["22"],earnedToday:10,dailyMaximum:45,completedDays:2,weeklyBonusEarned:false,resets:1_793_232_000)}
        return try await request("coins")
    }
}

struct TournamentMedal:View {
    let prize:TournamentPrize
    var size:CGFloat=36
    var body:some View {
        ZStack {
            Circle().fill(prize.colour)
            Circle().stroke(.white,lineWidth:2)
            Text("\(prize.rank)").font(.system(size:size*0.5,weight:.black,design:.rounded)).foregroundStyle(.white)
        }.frame(width:size,height:size).accessibilityLabel("Tournament badge: \(prize.placing)")
    }
}

struct TournamentPrizePopup:View {
    @EnvironmentObject var store:QuizStore
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    let prize:TournamentPrize
    @State private var appeared=false
    @State private var busy=false
    @State private var error:String?
    private var topicName:String {store.topics.first{$0.id==prize.topicID}?.name ?? "Trivia"}
    var body:some View {
        ZStack {
            Color.black.opacity(0.55).ignoresSafeArea()
            VStack(spacing:20) {
                TournamentMedal(prize:prize,size:88).scaleEffect(appeared ? 1:0.6)
                Text("Congratulations!").font(.system(size:30,weight:.bold,design:.rounded))
                Text("You finished in \(prize.placing)").font(.title3.bold())
                Text("\(topicName) · \(prize.kind.capitalized) tournament").multilineTextAlignment(.center)
                Text(Date(timeIntervalSince1970:prize.date),style:.date).font(.caption).foregroundStyle(.secondary)
                Text("+\(prize.coins) coins").font(.system(size:36,weight:.black,design:.rounded)).foregroundStyle(prize.colour)
                Text("Your coins are in your balance. Your tournament badge is yours to keep.").font(.subheadline).multilineTextAlignment(.center).foregroundStyle(.secondary)
                Button("Wear this badge"){finish(wear:true)}.buttonStyle(PrimaryButton()).disabled(busy)
                Button("Continue"){finish(wear:false)}.disabled(busy)
                if busy {ProgressView()}
                if let error {Text(error).font(.caption).foregroundStyle(.red)}
            }.padding(28).background(Color.canvas,in:RoundedRectangle(cornerRadius:28)).padding(22)
                .accessibilityIdentifier("tournamentCongratulations")
                .animation(reduceMotion ? nil:.spring(response:0.5,dampingFraction:0.65),value:appeared)
                .onAppear{appeared=true}
        }
    }
    private func finish(wear:Bool) {
        busy=true;error=nil
        Task {do {try await store.acknowledgePrize(prize,wear:wear)}catch{self.error=error.localizedDescription};busy=false}
    }
}

struct CoinTrailView:View {
    @EnvironmentObject var store:QuizStore
    @State private var status:CoinTrailStatus?
    @State private var error:String?
    @State private var loading=false
    var body:some View {
        ScrollView {
            VStack(alignment:.leading,spacing:22) {
                Text("A little curiosity pays off.").font(.system(size:29,weight:.bold,design:.rounded))
                Text("Complete an online duel with at least 4 correct answers in each of 3 different topics today.").font(.body)
                if let status {
                    HStack {
                        Label("\(status.wallet.coins) coins",systemImage:"circle.fill").font(.headline).foregroundStyle(Color(hex:"B27B23"))
                        Spacer()
                        Text("\(status.earnedToday) / 45 earned today").font(.caption)
                    }
                    ForEach(0..<3,id:\.self){i in trailStep(i,status:status)}
                    Text("10 coins per topic + 15 for finishing all three").font(.subheadline.bold())
                    VStack(alignment:.leading,spacing:9) {
                        Text("Your weekly trail").font(.headline)
                        ProgressView(value:Double(min(status.completedDays,5)),total:5).tint(.coral)
                        Text(status.weeklyBonusEarned ? "50-coin weekly bonus earned":"\(min(status.completedDays,5)) of 5 daily trails · earn 50 bonus coins").font(.subheadline)
                    }.padding(18).background(.white,in:RoundedRectangle(cornerRadius:16))
                    Text("Daily limit: 45 coins. Weekly bonus: once per week. Days reset at 00:00 UTC; weeks reset on Monday. Repeating a topic, offline practice and tournament attempts do not earn trail coins. You can complete all five days at your own pace within the week.").font(.caption).foregroundStyle(.secondary)
                    if status.topics.count<3 {
                        Text("Choose your next topic").font(.title3.bold())
                        ForEach(store.topics.filter{!status.topics.contains($0.id)}){topic in
                            NavigationLink {TopicView(topic:topic)} label: {
                                HStack{Text(topic.emoji);Text(topic.name);Spacer();Image(systemName:"chevron.right").font(.caption)}.foregroundStyle(Color.ink).padding(14).background(.white,in:RoundedRectangle(cornerRadius:12))
                            }
                        }
                    }
                } else if loading {ProgressView("Loading your trail…")}
                if let error {Text(error).foregroundStyle(.red);Button("Try again"){Task{await reload()}}}
                Text("Spend your coins on daily and weekly tournament entries. Each event shows its entry cost and podium prizes before you join.").font(.subheadline).foregroundStyle(.secondary)
            }.padding(22)
        }.background(Color.canvas).navigationTitle("Daily Trail").navigationBarTitleDisplayMode(.inline)
            .toolbar(.visible,for:.navigationBar).task{await reload()}.refreshable{await reload()}
    }
    private func trailStep(_ index:Int,status:CoinTrailStatus)->some View {
        let topic=index<status.topics.count ? store.topics.first{$0.id==status.topics[index]}:nil
        return HStack(spacing:14) {
            Image(systemName:topic==nil ? "circle":"checkmark.circle.fill").font(.title2).foregroundStyle(topic==nil ? .gray:.green)
            VStack(alignment:.leading,spacing:4){Text(topic?.name ?? "Topic \(index+1)").font(.headline);Text(topic==nil ? "4 correct answers in one completed duel":"10 coins earned").font(.caption).foregroundStyle(.secondary)}
            Spacer()
        }.padding(18).background(.white,in:RoundedRectangle(cornerRadius:16))
    }
    private func reload() async {
        loading=true;error=nil;defer{loading=false}
        if store.profile==nil {await store.connect()}
        do {status=try await store.coinTrail()}catch{self.error=error.localizedDescription}
    }
}

struct TournamentBadgePicker:View {
    @EnvironmentObject var store:QuizStore
    @State private var error:String?
    @State private var busy=false
    var body:some View {
        List {
            Section("Beside your profile picture") {
                Button("No tournament badge"){choose(nil)}.disabled(busy)
                ForEach(store.earnedPrizes){prize in
                    Button {choose(prize)} label: {
                        HStack(spacing:14){TournamentMedal(prize:prize);VStack(alignment:.leading,spacing:4){Text("\(store.topics.first{$0.id==prize.topicID}?.name ?? "Trivia") · \(prize.placing)");Text(Date(timeIntervalSince1970:prize.date),style:.date).font(.caption).foregroundStyle(.secondary)};Spacer();if store.ownCard?.displayBadge?.id==prize.id {Image(systemName:"checkmark")}}
                    }.disabled(busy)
                }
                if store.earnedPrizes.isEmpty {Text("Finish in the top three of a tournament to earn your first badge.").foregroundStyle(.secondary)}
            }
            if let error {Text(error).foregroundStyle(.red)}
        }.navigationTitle("Tournament badges").task{await store.loadPrizes()}
    }
    private func choose(_ prize:TournamentPrize?) {busy=true;Task{do {try await store.selectBadge(prize);error=nil}catch{self.error=error.localizedDescription};busy=false}}
}
