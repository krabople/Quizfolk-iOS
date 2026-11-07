import SwiftUI

struct TournamentPrize:Decodable,Identifiable,Equatable {
    let id:String
    let topicID:String
    let kind:String
    let rank:Int
    let coins:Int
    let date:Double
    let score:Int
    var eventName:String?=nil
    var adjustmentCoins:Int?=nil
    var isPrizeIncrease:Bool {(adjustmentCoins ?? 0)>0 && (adjustmentCoins ?? 0)<coins}
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
    var loginClaimed:Bool?=nil
}
struct PrizeInbox:Decodable {let pending:[TournamentPrize];let earned:[TournamentPrize];let selected:TournamentPrize?;var wallet:TournamentWallet?=nil}
struct DailyLoginReward:Decodable {let wallet:TournamentWallet;let awarded:Int;let day:String;let resets:Double}

struct CoinSymbol:View {
    var size:CGFloat=22
    var body:some View {
        ZStack {
            Circle().fill(LinearGradient(colors:[Color(hex:"FFE29A"),Color(hex:"D99824")],startPoint:.topLeading,endPoint:.bottomTrailing))
            Circle().stroke(Color(hex:"A76B11"),lineWidth:max(1,size*0.06))
            Circle().stroke(Color(hex:"FFF0BC"),lineWidth:max(1,size*0.045)).padding(size*0.13)
            Text("Q").font(.system(size:size*0.5,weight:.black,design:.rounded)).foregroundStyle(Color(hex:"A66B17"))
        }.frame(width:size,height:size).accessibilityHidden(true)
    }
}
struct CoinAmount:View {
    let coins:Int;var size:CGFloat=22
    var body:some View {HStack(spacing:6){CoinSymbol(size:size);Text("\(coins) coins")}}
}

extension QuizStore {
    private var usesCoinFixtures:Bool {
        #if DEBUG
        return isUITesting && testResponse == nil && !StoreScreenshotFixture.enabled
        #else
        return false
        #endif
    }
    static var testPrize:TournamentPrize {TournamentPrize(id:"test-prize",topicID:"22",kind:"daily",rank:1,coins:150,date:1_793_145_600,score:120)}
    func loadPrizes() async {
        guard profile != nil,!prizesLoading else{return}
        if usesCoinFixtures {
            earnedPrizes=[Self.testPrize,TournamentPrize(id:"test-weekly",topicID:"17",kind:"weekly",rank:2,coins:250,date:1_793_145_600,score:110),TournamentPrize(id:"test-friends",topicID:"11",kind:"party",rank:3,coins:20,date:1_793_145_600,score:10)]
            if ProcessInfo.processInfo.arguments.contains("--prize-popup"),!testPrizeAcknowledged {
                pendingPrizes=[Self.testPrize]
            }
            return
        }
        prizesLoading=true;defer{prizesLoading=false}
        do {let reply:PrizeInbox=try await request("prizes");pendingPrizes=reply.pending;earnedPrizes=reply.earned;if let wallet=reply.wallet{coinBalance=wallet.coins}}
        catch { /* A connection error leaves unseen results pending on the server. */ }
    }
    func acknowledgePrize(_ prize:TournamentPrize,wear:Bool) async throws {
        if usesCoinFixtures {testPrizeAcknowledged=true;if wear{ownCard?.displayBadge=prize;badgeConfirmation=prize};pendingPrizes.removeAll{$0.id==prize.id};return}
        if wear {
            let reply:OKReply=try await request("select-badge",body:["event":prize.id,"acknowledge":true])
            if reply.acknowledged != true {let _:OKReply=try await request("prize-seen",body:["event":prize.id])}
            ownCard?.displayBadge=prize;badgeConfirmation=prize
        } else {let _:OKReply=try await request("prize-seen",body:["event":prize.id])}
        pendingPrizes.removeAll{$0.id==prize.id}
    }
    func selectBadge(_ prize:TournamentPrize?) async throws {
        if usesCoinFixtures {ownCard?.displayBadge=prize;return}
        let value:Any=prize.map{$0.id as Any} ?? NSNull()
        let _:OKReply=try await request("select-badge",body:["event":value])
        ownCard=try await request("player")
    }
    func coinTrail() async throws -> CoinTrailStatus {
        if usesCoinFixtures {coinBalance=110;return CoinTrailStatus(wallet:TournamentWallet(coins:110,tickets:0,dailyClaimed:true),topics:["22"],earnedToday:10,dailyMaximum:45,completedDays:2,weeklyBonusEarned:false,resets:1_793_232_000,loginClaimed:true)}
        let result:CoinTrailStatus=try await request("coins");coinBalance=result.wallet.coins;return result
    }
    func claimDailyLogin() async {
        guard profile != nil,!claimingDailyLogin,!usesCoinFixtures else{return}
        claimingDailyLogin=true;defer{claimingDailyLogin=false}
        do {let reward:DailyLoginReward=try await request("daily-login",body:[:]);dailyLoginReward=reward;coinBalance=reward.wallet.coins}
        catch { /* The server keeps this day's reward available for the next connection. */ }
    }
}

struct BadgeAppliedPopup:View {
    @EnvironmentObject private var store:QuizStore
    let prize:TournamentPrize
    var body:some View {
        ZStack {
            Color.black.opacity(0.55).ignoresSafeArea()
            QuizPopupCard {
                Image(systemName:"checkmark.circle.fill").font(.system(size:40)).foregroundStyle(.green)
                PlayerPortrait(name:store.name,avatar:store.avatar,size:120,badge:prize)
                Text("Badge added!").font(.system(size:29,weight:.bold,design:.rounded))
                Text("Your tournament badge is now displayed beside your profile picture.").multilineTextAlignment(.center)
                Button("Done"){store.badgeConfirmation=nil}.buttonStyle(PrimaryButton()).accessibilityIdentifier("badgeConfirmationDone")
            }
        }
    }
}

struct TournamentMedal:View {
    let prize:TournamentPrize
    var size:CGFloat=36
    var body:some View {TournamentBadgeEmblem(topicID:prize.topicID,kind:prize.kind,rank:prize.rank,size:size)}
}
struct TournamentBadgeEmblem:View {
    @EnvironmentObject private var store:QuizStore
    let topicID:String;let kind:String;let rank:Int
    var size:CGFloat=36
    private var topic:Topic? {store.topics.first{$0.id==topicID}}
    private var metal:Color {Color(hex:rank==1 ? "C8952C":(rank==2 ? "7C8DA3":"B66F47"))}
    var body:some View {
        ZStack {
            Image(systemName:kind=="weekly" ? "shield.fill":(kind=="party" ? "hexagon.fill":"seal.fill"))
                .resizable().scaledToFit().foregroundStyle(metal)
            Circle().fill(topic?.tint ?? .ink).frame(width:size*0.72,height:size*0.72)
            Image(systemName:kind=="party" ? "person.3.fill":(topic?.symbol ?? "trophy.fill")).font(.system(size:size*0.34,weight:.bold)).foregroundStyle(.white).offset(y:-size*0.05)
            HStack(spacing:1){Image(systemName:"trophy.fill");Text("\(rank)").fontWeight(.black)}
                .font(.system(size:max(6,size*0.18),weight:.bold)).foregroundStyle(.white)
                .padding(.horizontal,size*0.09).padding(.vertical,size*0.035).background(metal,in:Capsule()).offset(y:size*0.32)
        }.frame(width:size,height:size).accessibilityElement(children:.ignore)
            .accessibilityLabel("\(topic?.name ?? "Mixed topics"), \(kind=="party" ? "friends":kind) tournament, place \(rank) badge")
            .accessibilityIdentifier("badge-\(topicID)-\(kind)-\(rank)")
    }
}

struct TournamentPrizePopup:View {
    @EnvironmentObject var store:QuizStore
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    let prize:TournamentPrize
    @State private var appeared=false
    @State private var busy=false
    @State private var error:String?
    private var topicName:String {prize.eventName ?? store.topics.first{$0.id==prize.topicID}?.name ?? "Trivia"}
    var body:some View {
        ZStack {
            Color.black.opacity(0.55).ignoresSafeArea()
            QuizPopupCard {
                TournamentMedal(prize:prize,size:88).scaleEffect(appeared ? 1:0.6)
                Text("Congratulations!").font(.system(size:30,weight:.bold,design:.rounded))
                Text("You finished in \(prize.placing)").font(.title3.bold())
                Text("\(topicName) · \(prize.kind=="party" ? "Friends":prize.kind.capitalized) tournament").multilineTextAlignment(.center)
                Text(Date(timeIntervalSince1970:prize.date),style:.date).font(.caption).foregroundStyle(.secondary)
                Text("\(prize.isPrizeIncrease ? "Prize increased to":"Prize:") \(prize.coins) coins").font(.system(size:30,weight:.black,design:.rounded)).foregroundStyle(prize.colour)
                if prize.isPrizeIncrease {Text("An extra \(prize.adjustmentCoins ?? 0) coins have been credited automatically.").font(.subheadline.bold()).multilineTextAlignment(.center)}
                Text("Awarded automatically to your wallet. Your tournament badge is yours to keep.").font(.subheadline).multilineTextAlignment(.center).foregroundStyle(.secondary)
                Button("Wear this badge"){finish(wear:true)}.buttonStyle(PrimaryButton()).disabled(busy)
                Button("Continue"){finish(wear:false)}.disabled(busy)
                if busy {ProgressView()}
                if let error {Text(error).font(.caption).foregroundStyle(.red)}
            }
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
        QuizPageScroll(maxWidth:860) {
            VStack(alignment:.leading,spacing:22) {
                Text("A little curiosity pays off.").font(.system(size:29,weight:.bold,design:.rounded))
                Text("Complete an online duel with at least 4 correct answers in each of 3 different topics today.").font(.body)
                if let status {
                    HStack {
                        CoinAmount(coins:store.coinBalance ?? status.wallet.coins).font(.headline).foregroundStyle(Color(hex:"B27B23"))
                        Spacer()
                        Text("\(status.earnedToday) / 45 earned today").font(.caption)
                    }
                    HStack(spacing:12){CoinSymbol(size:30);VStack(alignment:.leading,spacing:4){Text("50 coins for opening Quizfolk each day").font(.headline);Text(status.loginClaimed==true ? "Today's login reward is claimed":"Credited automatically when you open the app").font(.caption).foregroundStyle(.secondary)}}.padding(16).frame(maxWidth:.infinity,alignment:.leading).background(.white,in:RoundedRectangle(cornerRadius:16))
                    RewardedAdCard()
                    Text("DAILY TRAIL · EXTRA COINS").font(.caption.bold()).foregroundStyle(.secondary)
                    ForEach(0..<3,id:\.self){i in trailStep(i,status:status)}
                    Text("10 coins per topic + 15 for finishing all three").font(.subheadline.bold())
                    VStack(alignment:.leading,spacing:9) {
                        Text("Your weekly trail").font(.headline)
                        ProgressView(value:Double(min(status.completedDays,5)),total:5).tint(.coral)
                        Text(status.weeklyBonusEarned ? "50-coin weekly bonus earned":"\(min(status.completedDays,5)) of 5 daily trails · earn 50 bonus coins").font(.subheadline)
                    }.padding(18).background(.white,in:RoundedRectangle(cornerRadius:16))
                    Text("Login reward: 50 coins once per day. Trail limit: 45 extra coins per day. Weekly trail bonus: once per week. Days reset at 00:00 UTC; weeks reset on Monday. Repeating a topic, offline practice and tournament attempts do not earn trail coins. You can complete all five trail days at your own pace within the week.").font(.caption).foregroundStyle(.secondary)
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
        do {status=try await store.coinTrail();await RewardedAdCoordinator.shared.refresh()}catch{self.error=error.localizedDescription}
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
                        HStack(spacing:14){TournamentMedal(prize:prize,size:46);VStack(alignment:.leading,spacing:4){Text("\(store.topics.first{$0.id==prize.topicID}?.name ?? "Trivia") · \(prize.placing)");Text("\(prize.kind=="party" ? "Friends":prize.kind.capitalized) tournament").font(.caption.bold());Text(Date(timeIntervalSince1970:prize.date),style:.date).font(.caption).foregroundStyle(.secondary)};Spacer();if store.ownCard?.displayBadge?.id==prize.id {Image(systemName:"checkmark")}}
                    }.disabled(busy).accessibilityIdentifier("earnedBadge-\(prize.id)")
                }
                if store.earnedPrizes.isEmpty {Text("Finish in the top three of a tournament to earn your first badge.").foregroundStyle(.secondary)}
            }
            if let error {Text(error).foregroundStyle(.red)}
        }.navigationTitle("Tournament badges").task{await store.loadPrizes()}
    }
    private func choose(_ prize:TournamentPrize?) {busy=true;Task{do {try await store.selectBadge(prize);error=nil}catch{self.error=error.localizedDescription};busy=false}}
}
