import XCTest
@testable import Quizfolk

@MainActor final class ProgressRecoveryTests:XCTestCase {
    private let topic=Topic(id:"22",name:"Geography",symbol:"globe",color:"008080",emoji:"",questionCount:150)
    private func question(_ index:Int)->Question {Question(id:"progress-\(index)",categoryID:"22",difficulty:"easy",prompt:"Question \(index)?",answers:["Correct","Wrong one","Wrong two","Wrong three"],correctIndex:0)}
    private func record(_ id:String,count:Int=7,pending:Bool=false,kind:String="practice")->MatchRecord {
        MatchRecord(id:id,topicID:"22",date:Date(timeIntervalSince1970:1),score:140,opponentScore:0,opponent:"Bot",kind:kind,
            rounds:(0..<count).map{PlayedRound(question:question($0),selected:0,elapsed:1,points:20,opponentPoints:0)},pending:pending)
    }
    private func store(xp:Int=0)->QuizStore {
        let store=QuizStore();store.history=[]
        store.profile=OnlineProfile(id:"test-self",socialVersion:1,name:"Tester",avatar:nil,matches:0,wins:0,xp:xp,correct:0,answered:0)
        store.ownCard=QuizStore.testCard(following:false,own:true,topicXP:xp)
        return store
    }
    private func profileData(_ xp:Int)->Data {Data("""
        {"id":"test-self","name":"Tester","socialVersion":1,"matches":1,"wins":1,"xp":\(xp),"correct":7,"answered":7}
        """.utf8)}
    private func cardData(_ xp:Int)->Data {Data("""
        {"id":"test-self","name":"Tester","title":"Newcomer","interests":[],"sharedTopics":[],"following":false,"followers":0,"followingCount":0,"canChallenge":false,"stats":{"matches":1,"wins":1,"draws":0,"xp":\(xp),"correct":7,"answered":7,"perfect":1},"topics":[{"topicID":"22","xp":\(xp),"level":1,"matches":1,"wins":1}],"titles":[],"selectedTitle":"newcomer","discoverable":true,"challengesOpen":true}
        """.utf8)}
    private func waitUntil(_ condition:()->Bool) async throws {
        for _ in 0..<500 {if condition(){return};try await Task.sleep(for:.milliseconds(10))}
        XCTFail("Expected progress update did not arrive")
    }

    func testOldPracticeRecordsRecoverAfterReopenAndNeverDuplicateServerXp() async throws {
        let previous=UserDefaults.standard.data(forKey:"history");defer{UserDefaults.standard.set(previous,forKey:"history")}
        let store=store(),completed=record("old")
        let data=try JSONEncoder().encode([completed,completed,record("partial",count:6),record("pending",pending:true),record("online",kind:"bot")])
        store.history=try JSONDecoder().decode([MatchRecord].self,from:data)
        XCTAssertEqual(store.practiceXP(topic),280);XCTAssertEqual(store.onlineTopicXP(topic),0);XCTAssertEqual(store.topicXP(topic),280)
        store.persistHistory()
        let reopened=QuizStore();reopened.profile=store.profile;reopened.ownCard=store.ownCard
        reopened.testResponse={route,_ in
            if route=="profile" {return self.profileData(700)}
            XCTAssertEqual(route,"player");return self.cardData(700)
        }
        try await reopened.refreshPlayerProgress();try await reopened.refreshPlayerProgress()
        XCTAssertEqual(reopened.practiceXP(topic),280);XCTAssertEqual(reopened.onlineTopicXP(topic),700);XCTAssertEqual(reopened.topicXP(topic),980)
        XCTAssertEqual(reopened.ownCard?.topics.first?.xp,700,"Public totals must not include local practice")
    }
    func testPracticeFinalAnswerAddsXpAndCelebratesOnlyTheNewResult() async {
        let previous=UserDefaults.standard.data(forKey:"history");defer{UserDefaults.standard.set(previous,forKey:"history")}
        let store=store();store.history=(0..<5).map{record("old-\($0)")}
        let game=GameSession(topic:topic,store:store,online:false);defer{game.stop()}
        game.prepared=true;game.showIntro=false;game.round=6;game.rounds=Array(record("fixture").rounds.prefix(6));game.score=120;game.current=question(6)
        await game.answer(0);await game.next()
        XCTAssertEqual(store.practiceXP(topic),1700);XCTAssertEqual(store.onlineTopicXP(topic),0);XCTAssertEqual(game.levelUp?.progress.level,2)
        await game.next();XCTAssertEqual(store.topicXP(topic),1700)
        let replay=GameSession(topic:topic,store:store,record:store.history[0]);defer{replay.stop()}
        replay.updateLevelUp();XCTAssertNil(replay.levelUp)
    }
    func testSeventhOnlineAnswerRefreshSurvivesClosingBeforeResults() async throws {
        let previous=UserDefaults.standard.data(forKey:"history");defer{UserDefaults.standard.set(previous,forKey:"history")}
        let store=store();var routes:[String]=[];var release:CheckedContinuation<Void,Never>?
        defer{release?.resume()}
        store.testResponse={route,_ in
            routes.append(route)
            switch route {
            case "round":return Data(#"{"round":6,"question":{"id":"last","prompt":"Which?","answers":["A","B","C","D"],"difficulty":"easy"},"remaining":10,"phase":"answer"}"#.utf8)
            case "answer":return Data(#"{"points":40,"correctIndex":0,"opponentPoints":0,"finished":true,"score":160,"opponentScore":0,"pending":false}"#.utf8)
            case "profile":return self.profileData(300)
            case "player":await withCheckedContinuation{release=$0};return self.cardData(300)
            case "match-progress":return Data(#"{"ownAnswered":6,"opponentAnswered":6}"#.utf8)
            case "duels":return Data(#"{"duels":[]}"#.utf8)
            case "activity":return Data(#"{"events":[]}"#.utf8)
            default:throw APIError.message("Unexpected request: \(route)")
            }
        }
        let start=StartReply(id:"final-online",kind:"bot",opponent:"Bot",opponentAvatar:nil,played:Array(record("fixture").rounds.prefix(6)),score:120,opponentScore:0)
        let game=GameSession(topic:topic,store:store,online:true,match:start);defer{game.stop()}
        await game.begin();await game.startPlaying();await game.answer(0)
        try await waitUntil{release != nil}
        XCTAssertFalse(game.finished);XCTAssertEqual(store.topicXP(topic),0)
        game.stop();release?.resume();release=nil
        try await waitUntil{store.onlineTopicXP(self.topic)==300}
        XCTAssertEqual(store.profile?.xp,300);XCTAssertEqual(store.history.count,1)
        XCTAssertFalse(routes.contains("register"));XCTAssertFalse(routes.contains("social-settings"))
    }
    func testFailedRefreshKeepsLastConfirmedTotals() async throws {
        let store=store(xp:700);store.history=[record("practice")]
        store.testResponse={route,_ in
            if route=="profile" {return self.profileData(1000)}
            throw APIError.message("Temporarily unavailable")
        }
        do {try await store.refreshPlayerProgress();XCTFail("Expected failure")}catch{}
        XCTAssertEqual(store.profile?.xp,700);XCTAssertEqual(store.topicXP(topic),980)
    }
    func testSettledChallengeReplacesPendingHistoryAndRefreshesOnce() async throws {
        let previous=UserDefaults.standard.data(forKey:"history");defer{UserDefaults.standard.set(previous,forKey:"history")}
        let store=store();var reads=0
        var pending=record("pending",pending:true,kind:"challenge");pending.duelID="duel";store.history=[pending]
        let played=try JSONSerialization.jsonObject(with:JSONEncoder().encode(pending.rounds))
        store.testResponse={route,_ in
            switch route {
            case "duel-open":return try JSONSerialization.data(withJSONObject:["id":"pending","kind":"challenge","opponent":"Rival","duelID":"duel","score":140,"opponentScore":0,"pending":false,"played":played])
            case "profile":return self.profileData(280)
            case "player":reads+=1;return self.cardData(280)
            case "duels":return Data(#"{"duels":[]}"#.utf8)
            case "activity":return Data(#"{"events":[]}"#.utf8)
            default:throw APIError.message("Unexpected request: \(route)")
            }
        }
        let card=ChallengeCard(id:"duel",topicID:"22",opponentID:"rival",opponent:"Rival",avatar:nil,status:"complete",incoming:false,accepted:true,ownFinished:true,opponentFinished:true,score:140,opponentScore:0,created:0,expires:1,matchID:"pending")
        await store.resolveHistory(card);await store.refreshSocial();await store.refreshSocial()
        XCTAssertEqual(reads,1);XCTAssertEqual(store.history.count,1);XCTAssertEqual(store.history.first?.pending,false);XCTAssertEqual(store.onlineTopicXP(topic),280)
    }
}
