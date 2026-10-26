import XCTest
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
    @MainActor func testBundleBank() throws {
        let q:[Question]=try QuizStore.resource("questions")
        let topics:[Topic]=try QuizStore.resource("categories")
        XCTAssertGreaterThanOrEqual(q.count,4000)
        XCTAssertEqual(topics.count,24)
        XCTAssertEqual(Set(q.map{$0.id}).count,q.count)
        for topic in topics {XCTAssertEqual(q.filter{$0.categoryID==topic.id}.count,topic.questionCount)}
        for item in q {let s=item.shuffled();XCTAssertEqual(Set(s.answers).count,4);XCTAssertEqual(s.answers[s.correctIndex],item.answers[item.correctIndex])}
    }
}
