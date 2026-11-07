#if DEBUG
import Foundation

/// Fictional, local-only data used by the explicit App Store capture workflow.
/// This type and every entry point are compiled out of release builds.
@MainActor final class StoreScreenshotFixture {
    static var enabled:Bool {ProcessInfo.processInfo.arguments.contains("--store-screenshots")}
    static let names=["Maya", "Alex", "Leo", "Zara", "Finn", "Ruby"]
    static let stamp=1_793_923_200.0
    let questions:[Question]
    var turn=2
    init() {
        let bank:[Question]=(try? QuizStore.resource("questions")) ?? []
        let geography=bank.filter{$0.categoryID=="22" && $0.prompt.count<100 && $0.answers.allSatisfy{$0.count<35}}
        let favourite=geography.first{$0.id=="62e9086fe9de78aeeaab"} ?? geography[2]
        let other=geography.filter{$0.id != favourite.id}
        questions=Array(other.prefix(2))+[favourite]+Array(other.dropFirst(2).prefix(4))
    }
    static func decode<T:Decodable>(_ object:Any)->T {try! JSONDecoder().decode(T.self,from:JSONSerialization.data(withJSONObject:object))}
    static func card(own:Bool,following:Bool)->PlayerCard {
        let xp=own ? 4750:6350
        var object:[String:Any]=["id":own ? "test-self":"test-rival","name":own ? "Alex":"Maya","avatar":NSNull(),"title":"Newcomer"]
        object["interests"]=["22","11","12"];object["sharedTopics"]=["22","11"]
        object["following"]=following;object["followers"]=18;object["followingCount"]=12;object["canChallenge"] = !own
        object["stats"]=["matches":38,"wins":24,"draws":2,"xp":xp,"correct":205,"answered":266,"perfect":4]
        object["topics"]=[["topicID":"22","xp":xp,"level":TopicLevelling.progress(xp:xp).level,"matches":24,"wins":16],["topicID":"11","xp":2300,"level":2,"matches":14,"wins":8]]
        object["titles"]=[["id":"newcomer","name":"Newcomer"]];object["selectedTitle"]="newcomer"
        object["discoverable"]=true;object["challengesOpen"]=true
        object["headToHead"]=["games":9,"wins":5,"draws":1,"losses":3]
        object["badges"]=[["id":"first","name":"First duel","symbol":"bolt.fill","earned":true],["id":"podium","name":"Geography champion","symbol":"trophy.fill","earned":true,"topicID":"22","kind":"daily","rank":1]]
        object["displayBadge"]=prizeObject
        return decode(object)
    }
    static var prizeObject:[String:Any] {["id":"test-prize","topicID":"22","kind":"daily","rank":1,"coins":150,"date":stamp,"score":342]}
    static var prizes:[[String:Any]] {[prizeObject,["id":"test-weekly","topicID":"11","kind":"weekly","rank":2,"coins":250,"date":stamp-86400,"score":415],["id":"test-friends","topicID":"12","kind":"party","rank":3,"coins":20,"date":stamp-172800,"score":12]]}
    static var league:[BoardEntry] {zip(names,[6350,4750,4200,3650,3020,2800]).enumerated().map{i,p in BoardEntry(id:i==0 ? "test-rival":(i==1 ? "test-self":"capture-\(i)"),name:p.0,avatar:nil,xp:p.1,matches:38-i*3)}}
    static var wallet:[String:Any] {["coins":325,"tickets":0,"dailyClaimed":true]}
    static var events:[[String:Any]] {
        ["22","11","12","17"].enumerated().map{i,topic in ["id":i==0 ? "test-event":"capture-event-\(i)","topicID":topic,"kind":i==3 ? "weekly":"daily","starts":Date().timeIntervalSince1970-3600,"ends":Date().timeIntervalSince1970+21600,"coins":[25,50,75,100][i],"tickets":0,"closed":false,"best":i==0 ? 310:0,"streak":i==0 ? 18:0,"attempts":i==0 ? 2:0,"players":[28,21,34,56][i],"activeRun":NSNull(),"rank":i==0 ? 2 as Any:NSNull(),"reward":0,"featured":true] as [String:Any]}
    }
    static var tournamentList:TournamentList {decode(["events":events,"wallet":wallet])}
    static var tournamentBoard:TournamentBoard {
        let entries=names.enumerated().map{i,name in ["id":i==1 ? "test-self":"capture-\(i)","name":name,"avatar":NSNull(),"rank":i+1,"score":[342,310,298,280,265,240][i],"streak":[20,18,17,16,15,14][i],"reward":0] as [String:Any]}
        return decode(["event":events[0],"entries":entries,"own":[entries[1]],"wallet":wallet])
    }
    static var challenges:[ChallengeCard] {
        ["Maya","Leo","Zara"].enumerated().map{i,name in decode(["id":"capture-duel-\(i)","topicID":["22","11","12"][i],"opponentID":"test-rival","opponent":name,"avatar":NSNull(),"status":i==2 ? "complete":"accepted","incoming":i==0,"accepted":true,"ownFinished":i>0,"opponentFinished":i != 1,"score":i==2 ? 138:112,"opponentScore":i==2 ? 120 as Any:NSNull(),"created":stamp,"expires":stamp+864000,"matchID":"capture-match"]) }
    }
    var history:MatchRecord {MatchRecord(id:"history-fixture",topicID:"22",date:Date(timeIntervalSince1970:Self.stamp),score:138,opponentScore:112,opponent:"Maya",kind:"human",rounds:rounds(7),opponentID:"test-rival")}
    func rounds(_ count:Int)->[PlayedRound] {Array(questions.prefix(count)).enumerated().map{i,q in PlayedRound(question:q,selected:q.correctIndex,elapsed:2,points:i==6 ? 30:18,opponentPoints:i==1 ? 0:(i==6 ? 32:16))}}
    func response(_ route:String,body:[String:Any]?)->Data {
        let object:Any
        switch route {
        case "match-search": object=["searchID":"capture-search","state":"matched","elapsed":2,"match":["id":"capture-match","kind":"human","opponent":"Maya","opponentID":"test-rival","score":36,"opponentScore":16,"played":try! JSONSerialization.jsonObject(with:JSONEncoder().encode(rounds(2)))]]
        case "round","reveal":
            let q=questions[min(turn,6)]
            object=["round":turn,"question":["id":q.id,"prompt":q.prompt,"answers":q.answers,"difficulty":q.difficulty],"remaining":10.0,"readingRemaining":route=="round" ? 3.0:0.0,"phase":route=="round" ? "reading":"answering","power":["used":false,"hidden":[]]]
        case "answer":
            let q=questions[min(turn,6)],points=(body?["answer"] as? Int)==q.correctIndex ? 18:0
            object=["points":points,"correctIndex":q.correctIndex,"opponentPoints":16,"finished":turn==6,"score":36+points,"opponentScore":32,"pending":false];turn=min(6,turn+1)
        case "match-progress":object=["ownAnswered":turn,"opponentAnswered":7,"opponentResults":[true,false,true,true,false,true,true]]
        case "parties":object=["parties":[Self.party]]
        case "party-board":object=["party":Self.party,"selfID":"test-self","coins":325,"fixtures":[],"standings":Self.names.prefix(4).enumerated().map{i,name in ["id":i==1 ? "test-self":"capture-\(i)","name":name,"avatar":NSNull(),"topicID":["22","11","12","17"][i],"played":4,"wins":[3,2,2,1][i],"draws":0,"losses":[1,2,2,3][i],"points":[9,6,6,3][i],"quizPoints":[512,486,462,401][i],"rank":[1,2,2,4][i]] as [String:Any]}]
        case "prizes":object=["pending":[],"earned":Self.prizes,"selected":Self.prizeObject,"wallet":Self.wallet]
        case "daily-login":object=["wallet":Self.wallet,"awarded":0,"day":"2026-11-07","resets":Self.stamp+86400]
        default:object=["ok":true]
        }
        return try! JSONSerialization.data(withJSONObject:object)
    }
    static var party:[String:Any] {["id":"capture-party","name":"Friday quiz club","code":"QUIZ42","hostID":"test-self","status":"playing","cycles":1,"days":7,"powers":false,"ends":Date().timeIntervalSince1970+86400*3,"members":4,"entryCoins":0]}
}
#endif
