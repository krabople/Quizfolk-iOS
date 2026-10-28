import XCTest
import UIKit
@testable import Quizfolk
final class ScoringTests:XCTestCase {
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
        XCTAssertFalse(game.reading);XCTAssertGreaterThan(game.remaining,9)
        await game.answer(game.current!.correctIndex)
        XCTAssertEqual(game.lastPoints,20)
    }
    @MainActor func testPendingChallengeHasNoPrematureWinOrXP() {
        let q=Question(id:"sample",categoryID:"22",difficulty:"easy",prompt:"Sample?",answers:["A","B","C","D"],correctIndex:0)
        let r=PlayedRound(question:q,selected:0,elapsed:1,points:19,opponentPoints:0)
        let m=MatchRecord(id:"waiting",topicID:"22",date:Date(),score:100,opponentScore:0,opponent:"Rival",kind:"challenge",rounds:[r],duelID:"duel",pending:true,opponentID:"rival")
        XCTAssertEqual(m.xp,0);XCTAssertFalse(m.won);XCTAssertFalse(m.tied)
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
}
