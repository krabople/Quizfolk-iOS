import XCTest
@testable import Quizfolk

@MainActor final class PowerAvailabilityTests:XCTestCase {
    func testPerTypeContractAndConservativeLegacyFallback() throws {
        let state=try JSONDecoder().decode(PowerState.self,from:Data(#"{"used":true,"type":"fifty","hidden":[1,2],"usedTypes":["double","fifty"],"activeTypes":["double","fifty"]}"#.utf8))
        XCTAssertTrue(state.hasUsed(.double));XCTAssertTrue(state.hasUsed(.fifty));XCTAssertFalse(state.hasUsed(.right));XCTAssertTrue(state.active(.double))
        let next=state.nextQuestion();XCTAssertTrue(next.hasUsed(.double));XCTAssertFalse(next.active(.double));XCTAssertTrue(next.hidden.isEmpty)
        let legacy=try JSONDecoder().decode(PowerState.self,from:Data(#"{"used":true,"hidden":[]}"#.utf8))
        XCTAssertTrue(QuizPower.allCases.allSatisfy{legacy.hasUsed($0)})
    }
    func testPracticeDoubleChoiceSurvivesFiftyAndAllThreeBecomeUnavailableNextQuestion() async {
        let store=QuizStore(),topic=store.topics[0]
        let game=GameSession(topic:topic,store:store,online:false);defer{game.stop()}
        game.current=Question(id:"power",categoryID:topic.id,difficulty:"easy",prompt:"Which?",answers:["Correct","Wrong one","Wrong two","Wrong three"],correctIndex:0)
        await game.usePower(.double);await game.usePower(.fifty)
        let wrong=(1...3).first{!game.power.hidden.contains($0)}!
        await game.answer(wrong)
        XCTAssertFalse(game.revealed);XCTAssertEqual(game.power.firstWrong,wrong)
        await game.usePower(.right)
        XCTAssertTrue(game.revealed);XCTAssertEqual(game.rounds.count,1);XCTAssertGreaterThan(game.lastPoints,0)
        let next=game.power.nextQuestion()
        XCTAssertTrue(QuizPower.allCases.allSatisfy{next.hasUsed($0)});XCTAssertNil(next.firstWrong);XCTAssertTrue(next.hidden.isEmpty)
    }
    func testTournamentCanUseEachTypeOnceAndRightAnswerSubmitsAutomatically() async throws {
        let store=QuizStore();var used:[String]=[],hidden:[Int]=[],firstWrong:Int?=nil,turn=0,coins=150,calls=0
        func run()->[String:Any] { ["id":"run","eventID":"event","score":turn*20,"streak":turn,"turn":turn,"state":"playing"] }
        func power()->[String:Any] { ["used":!used.isEmpty,"usedTypes":used,"activeTypes":turn==0 ? used:[],"type":used.last ?? "","hidden":hidden] }
        store.testResponse={route,body in
            calls+=1
            var response:[String:Any]
            switch route {
            case "tournament-enter":response=run()
            case "tournament-round":response=run();response["question"]=["id":"q-\(turn)","prompt":"Which?","answers":["A","B","C","D"],"difficulty":"easy"];response["remaining"]=10;response["phase"]="answer";response["power"]=power()
            case "tournament-power":
                let choice=QuizPower(rawValue:body!["type"] as! String)!
                XCTAssertFalse(used.contains(choice.rawValue));used.append(choice.rawValue);coins-=choice.price
                if choice == .fifty {hidden=[1,2]}
                response=["power":power(),"remaining":9,"coins":coins]
                if choice == .right {turn=1;var answer=run();answer["selectedIndex"]=0;answer["correctIndex"]=0;answer["points"]=20;answer["correct"]=true;response["tournamentAnswer"]=answer;hidden=[]}
            case "tournament-answer":
                XCTAssertNil(firstWrong);firstWrong=body?["answer"] as? Int;hidden.append(firstWrong!)
                response=run();response["retry"]=true;response["remaining"]=9;response["power"]=power()
            default:throw APIError.message("Unexpected request: \(route)")
            }
            return try JSONSerialization.data(withJSONObject:response)
        }
        let game=TournamentSession(event:QuizStore.testTournamentList().events[0],topic:store.topics[0],store:store);defer{game.stop()}
        await game.begin();await game.usePower(.double);await game.usePower(.fifty);await game.answer(3)
        XCTAssertFalse(game.revealed);XCTAssertEqual(game.power.firstWrong,3);XCTAssertFalse(game.runEnded)
        await game.usePower(.right);XCTAssertTrue(game.revealed);XCTAssertEqual(game.score,20);XCTAssertEqual(store.coinBalance,110)
        await game.next();let previous=calls
        for choice in QuizPower.allCases {await game.usePower(choice)}
        XCTAssertEqual(calls,previous);XCTAssertEqual(coins,110);XCTAssertNil(game.powerError)
    }
}
