import XCTest
@testable import Quizfolk

@MainActor final class QuestionImageTests:XCTestCase {
    func testEveryPictureDecodesAndSurvivesShuffling() throws {
        let bank:[Question]=try QuizStore.resource("questions")
        let pictures=bank.filter{$0.imagePng != nil}
        XCTAssertEqual(pictures.count,412)
        for q in pictures {
            XCTAssertNotNil(QuestionImageData.image(q.imagePng,sha:q.imageSHA256),q.id)
            let shuffled=q.shuffled()
            XCTAssertEqual(shuffled.imageSHA256,q.imageSHA256)
            XCTAssertEqual(shuffled.imagePng,q.imagePng)
            XCTAssertEqual(shuffled.answers[shuffled.correctIndex],q.answers[q.correctIndex])
        }
        XCTAssertEqual(Set(bank.filter{$0.categoryID=="41"}.map(\.promptKey)).count,197)
        XCTAssertEqual(Set(bank.filter{$0.categoryID=="43"}.map(\.promptKey)).count,197)
    }
    func testRejectsBadOrOversizedImageData() throws {
        let bank:[Question]=try QuizStore.resource("questions");let q=try XCTUnwrap(bank.first{$0.imagePng != nil})
        XCTAssertNil(QuestionImageData.decode(q.imagePng,sha:String(repeating:"0",count:64)))
        XCTAssertNil(QuestionImageData.decode(String(repeating:"A",count:100_000),sha:q.imageSHA256))
        XCTAssertNil(QuestionImageData.decode("not a PNG",sha:q.imageSHA256))
    }
}
