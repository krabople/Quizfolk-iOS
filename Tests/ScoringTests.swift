import XCTest
import UIKit
@testable import Quizfolk
final class ScoringTests:XCTestCase {
    @MainActor func testOpponentMarkersShowResultsAndKeepUnknownRoundsNeutral() {
        XCTAssertEqual(DuelProgressView.opponentOutcome(index:0,answered:2,results:[true,false]),.correct)
        XCTAssertEqual(DuelProgressView.opponentOutcome(index:1,answered:2,results:[true,false]),.incorrect)
        XCTAssertEqual(DuelProgressView.opponentOutcome(index:2,answered:7,results:[true,false]),.answered)
        XCTAssertEqual(DuelProgressView.opponentOutcome(index:2,answered:2,results:[]),.upcoming)
        XCTAssertEqual(QuestionTimeBar.fraction(10),1)
        XCTAssertEqual(QuestionTimeBar.fraction(3),0.3)
        XCTAssertEqual(QuestionTimeBar.fraction(-1),0)
        XCTAssertEqual(QuestionTimeBar.fraction(.nan),0)
    }
    func testSpeedAndFinalRound() {
        XCTAssertEqual(Scoring.points(correct:true,elapsed:0,round:0),20)
        XCTAssertEqual(Scoring.points(correct:true,elapsed:3.7,round:0),17)
        XCTAssertEqual(Scoring.points(correct:true,elapsed:9.99,round:0),11)
        XCTAssertEqual(Scoring.points(correct:true,elapsed:0,round:6),40)
        XCTAssertEqual(Scoring.points(correct:true,elapsed:10,round:0),0)
        XCTAssertEqual(Scoring.points(correct:false,elapsed:0,round:6),0)
        XCTAssertEqual(Scoring.points(correct:true,elapsed:-1,round:0),0)
        XCTAssertEqual(Scoring.points(correct:true,elapsed:.nan,round:0),0)
        XCTAssertEqual((0..<7).reduce(0){$0+Scoring.points(correct:true,elapsed:0,round:$1)},160)
    }
    @MainActor func testRightAnswerAppliesAtomicServerSubmissionWithoutAnotherTap() async throws {
        let store=QuizStore();await store.connect()
        let match=try JSONDecoder().decode(StartReply.self,from:Data(#"{"id":"auto-match","kind":"bot","opponent":"Bot","opponentAvatar":null}"#.utf8))
        store.testResponse={route,body in
            switch route {
            case "round": return Data(#"{"round":0,"question":{"id":"q","prompt":"Which option?","answers":["A","B","C","D"],"difficulty":"easy"},"remaining":10,"phase":"answer"}"#.utf8)
            case "power":
                XCTAssertEqual(body?["autoAnswer"] as? Bool,true)
                return Data(#"{"power":{"used":true,"type":"right","hidden":[],"highlight":2},"remaining":8,"coins":125,"duelAnswer":{"selectedIndex":2,"correctIndex":2,"points":18,"opponentPoints":0,"finished":false,"score":18,"opponentScore":0}}"#.utf8)
            case "match-progress":return Data(#"{"ownAnswered":1,"opponentAnswered":1}"#.utf8)
            default:XCTFail("Unexpected request: \(route)");throw APIError.message("Unexpected request")
            }
        }
        let game=GameSession(topic:store.topics[0],store:store,online:true,match:match);defer{game.stop()}
        await game.begin();await game.startPlaying();await game.usePower(.right)
        XCTAssertTrue(game.revealed);XCTAssertEqual(game.selected,2);XCTAssertEqual(game.rounds.count,1)
        XCTAssertEqual(game.lastPoints,18);XCTAssertEqual(store.coinBalance,125)
        await game.answer(0);XCTAssertEqual(game.rounds.count,1)
    }
    @MainActor func testRematchPreservesHumanTargetAndTopicAndKeepsBotsLabelled() async throws {
        let store=QuizStore(),topic=store.topics.first{$0.id=="22"}!
        var routes:[String]=[]
        store.testResponse={route,body in
            routes.append(route);XCTAssertEqual(body?["topic"] as? String,"22")
            if route=="challenge" {
                XCTAssertEqual(body?["player"] as? String,"rival");XCTAssertEqual(body?["requestID"] as? String,"retry-key")
                return Data(#"{"id":"new-human","kind":"challenge","opponent":"Rival","opponentID":"rival","opponentAvatar":null}"#.utf8)
            }
            XCTAssertEqual(route,"match");XCTAssertEqual(body?["botOnly"] as? Bool,true)
            return Data(#"{"id":"new-bot","kind":"bot","opponent":"Pip · Bot","opponentAvatar":null}"#.utf8)
        }
        let human=try await store.rematch(topic:topic,opponentID:"rival",online:true,requestID:"retry-key")
        await human.begin();XCTAssertEqual(human.opponentID,"rival");XCTAssertTrue(human.showIntro);human.stop()
        let bot=try await store.rematch(topic:topic,opponentID:nil,online:true,requestID:"bot-key")
        await bot.begin();XCTAssertEqual(bot.kind,"bot");XCTAssertNil(bot.opponentID);bot.stop()
        let practice=try await store.rematch(topic:topic,opponentID:nil,online:false,requestID:"practice-key")
        await practice.begin();XCTAssertFalse(practice.online);XCTAssertEqual(practice.packet.count,7);practice.stop()
        XCTAssertEqual(routes,["challenge","match"])
    }
    func testExperienceBonuses() {
        XCTAssertEqual(Scoring.experience(score:160,opponentScore:100),300)
        XCTAssertEqual(Scoring.experience(score:100,opponentScore:100),190)
        XCTAssertEqual(Scoring.experience(score:50,opponentScore:100),90)
    }
    @MainActor func testProfilePicture() throws {
        let renderer=UIGraphicsImageRenderer(size:CGSize(width:500,height:300))
        let input=renderer.image{ctx in UIColor.red.setFill();ctx.fill(CGRect(x:0,y:0,width:500,height:300))}.pngData()!
        let output=try ProfilePicture.make(input)
        let image=UIImage(data:output)!
        XCTAssertEqual(image.size,CGSize(width:128,height:128))
        XCTAssertLessThanOrEqual(output.count,16384)
        XCTAssertThrowsError(try ProfilePicture.make(Data("not an image".utf8)))
    }
    @MainActor func testLevelsAreIndependentByTopic() async {
        let store=QuizStore();await store.connect()
        let geo=store.topics.first{$0.id=="22"}!,science=store.topics.first{$0.id=="17"}!
        XCTAssertEqual(store.level(geo),3)
        XCTAssertEqual(store.level(science),1)
    }
    @MainActor func testReadingDoesNotUseAnswerTime() async throws {
        let store=QuizStore();let game=GameSession(topic:store.topics[0],store:store,online:false)
        defer{game.stop()}
        await game.begin();await game.startPlaying()
        XCTAssertTrue(game.reading);XCTAssertEqual(game.remaining,10)
        await game.answer(0);XCTAssertTrue(game.rounds.isEmpty)
        try await Task.sleep(for:.milliseconds(2200))
        XCTAssertTrue(game.reading,"The complete three-second reading period must be respected")
        try await Task.sleep(for:.milliseconds(1000))
        XCTAssertFalse(game.reading);XCTAssertGreaterThan(game.remaining,9)
        await game.answer(game.current!.correctIndex)
        XCTAssertEqual(game.lastPoints,20)
    }
    @MainActor func testMixedDeckBalancesCategoriesAndDoubleChoiceHasOneUse() async throws {
        let store=QuizStore(),mixed=Topic.mixed(count:store.questions.count)
        let packet=store.packet(mixed)
        XCTAssertEqual(packet.count,7)
        XCTAssertEqual(Set(packet.map{$0.categoryID}).count,7)
        XCTAssertEqual(Set(packet.map{$0.promptKey}).count,7)
        let game=GameSession(topic:mixed,store:store,online:false)
        defer{game.stop()};await game.begin();await game.startPlaying()
        await game.usePower(.right);XCTAssertFalse(game.power.used)
        // The reading task and this test share MainActor. Await the phase
        // change rather than assuming both tasks were scheduled together.
        let readingDeadline=ContinuousClock.now.advanced(by:.seconds(6))
        while game.reading && ContinuousClock.now<readingDeadline {
            try await Task.sleep(for:.milliseconds(50))
        }
        XCTAssertFalse(game.reading,"The reading phase must reveal the answers")
        await game.usePower(.double);XCTAssertTrue(game.power.used)
        let q=try XCTUnwrap(game.current),wrong=(q.correctIndex+1)%4
        await game.answer(wrong)
        XCTAssertFalse(game.revealed);XCTAssertTrue(game.rounds.isEmpty)
        XCTAssertEqual(game.power.hidden,[wrong])
        await game.usePower(.right);XCTAssertEqual(game.power.type,"double")
        await game.answer(q.correctIndex)
        XCTAssertEqual(game.rounds.count,1);XCTAssertGreaterThan(game.lastPoints,0)
        let consumed=game.power.nextQuestion()
        XCTAssertTrue(consumed.used);XCTAssertNil(consumed.type);XCTAssertTrue(consumed.hidden.isEmpty)
    }
    @MainActor func testPendingChallengeHasNoPrematureWinOrXP() {
        let q=Question(id:"sample",categoryID:"22",difficulty:"easy",prompt:"Sample?",answers:["A","B","C","D"],correctIndex:0)
        let r=PlayedRound(question:q,selected:0,elapsed:1,points:19,opponentPoints:0)
        let m=MatchRecord(id:"waiting",topicID:"22",date:Date(),score:100,opponentScore:0,opponent:"Rival",kind:"challenge",rounds:[r],duelID:"duel",pending:true,opponentID:"rival")
        XCTAssertEqual(m.xp,0);XCTAssertFalse(m.won);XCTAssertFalse(m.tied)
    }
    @MainActor func testReopeningSavedResultDoesNotStartOrSaveAnotherMatch() async {
        let store=QuizStore(),topic=store.topics[0]
        let rounds=store.packet(topic).map{PlayedRound(question:$0,selected:$0.correctIndex,elapsed:1,points:19,opponentPoints:10)}
        let record=MatchRecord(id:"saved-result",topicID:topic.id,date:Date(),score:133,opponentScore:70,opponent:"Rival",kind:"human",rounds:rounds,opponentID:"rival")
        store.history=[record]
        store.testResponse={route,_ in XCTFail("Reopening a saved result must not request a new match: \(route)");throw APIError.message("Unexpected request")}
        let game=GameSession(topic:topic,store:store,record:record);defer{game.stop()};await game.begin()
        XCTAssertTrue(game.finished);XCTAssertFalse(game.showIntro);XCTAssertEqual(game.opponentID,"rival")
        XCTAssertEqual(game.score,133);XCTAssertEqual(game.rounds.count,7);XCTAssertEqual(store.history.count,1)
    }
    @MainActor func testBundleBank() throws {
        let q:[Question]=try QuizStore.resource("questions")
        let topics:[Topic]=try QuizStore.resource("categories")
        XCTAssertGreaterThanOrEqual(q.count,20000)
        XCTAssertEqual(topics.count,30)
        XCTAssertEqual(Set(q.map{$0.id}).count,q.count)
        for topic in topics {XCTAssertEqual(q.filter{$0.categoryID==topic.id}.count,topic.questionCount)}
        for item in q {let s=item.shuffled();XCTAssertEqual(Set(s.answers).count,4);XCTAssertEqual(s.answers[s.correctIndex],item.answers[item.correctIndex])}
    }
    func question(_ id:String,_ prompt:String) -> Question {
        Question(id:id,categoryID:"17",difficulty:"easy",prompt:prompt,answers:["Right","Wrong one","Wrong two","Wrong three"],correctIndex:0)
    }
    func testPromptKeysNormalizeTypographyWithoutChangingMeaningfulNotation() {
        XCTAssertEqual(question("a","  What’s Éarth? ").promptKey,question("b","WHAT'S   ÉARTH!!!").promptKey)
        XCTAssertEqual(question("a","Straße?").promptKey,question("b","STRASSE").promptKey)
        XCTAssertNotEqual(question("a","What is 2 + 2?").promptKey,question("b","What is 2 × 2?").promptKey)
        for pair in [("2-3","23"),("1.2","12"),("2/3","23"),("6!","6"),("2^3","23"),("−2","2"),("3%","3"),("2 ≤ 3","2 < 3"),("now here","nowhere")] {
            XCTAssertNotEqual(question("a","Calculate \(pair.0)?").promptKey,question("b","Calculate \(pair.1)?").promptKey)
        }
    }
    @MainActor func testOfflinePacketsExcludeDuplicateContentAndPreserveFreshness() {
        let store=QuizStore(),topic=Topic(id:"17",name:"Science",symbol:"atom",color:"47A6A3",emoji:"",questionCount:9)
        let old=question("old","What’s Earth?")
        store.questions=[old,question("copy","WHAT'S EARTH!!!")]+(0..<7).map{question("fresh-\($0)","Fresh question \($0)?")}
        store.history=[MatchRecord(id:"seen",topicID:"17",date:Date(),score:20,opponentScore:0,opponent:"Bot",kind:"practice",rounds:[PlayedRound(question:old,selected:0,elapsed:0,points:20,opponentPoints:0)])]
        for _ in 0..<10 {
            let packet=store.packet(topic)
            XCTAssertEqual(packet.count,7);XCTAssertEqual(Set(packet.map{$0.promptKey}).count,7)
            XCTAssertTrue(packet.allSatisfy{$0.id.hasPrefix("fresh-")})
            XCTAssertTrue(packet.allSatisfy{$0.answers[$0.correctIndex]=="Right"})
        }
        store.history=[]
        store.questions=[old,question("copy","WHAT'S EARTH!!!")]+(0..<5).map{question("fresh-\($0)","Fresh question \($0)?")}
        XCTAssertEqual(store.packet(topic).count,6,"Exhaustion must not refill with duplicate prompts")
    }
    @MainActor func testOfflineInsufficientUniqueQuestionsShowsErrorAndPreparedDeckDoesNotChange() async {
        let store=QuizStore(),topic=Topic(id:"17",name:"Science",symbol:"atom",color:"47A6A3",emoji:"",questionCount:7)
        store.history=[]
        store.questions=(0..<7).map{question("copy-\($0)","Same question?")}
        let insufficient=GameSession(topic:topic,store:store,online:false)
        await insufficient.begin()
        XCTAssertFalse(insufficient.prepared);XCTAssertFalse(insufficient.busy)
        XCTAssertTrue(insufficient.error?.contains("seven different") == true)
        store.questions=(0..<9).map{question("unique-\($0)","Different question \($0)?")}
        let game=GameSession(topic:topic,store:store,online:false)
        defer{game.stop();insufficient.stop()}
        await game.begin();let ids=game.packet.map{$0.id},choices=game.packet.map{$0.answers}
        await game.begin()
        XCTAssertTrue(game.prepared);XCTAssertEqual(game.packet.map{$0.id},ids)
        XCTAssertEqual(game.packet.map{$0.answers},choices)
    }
}
