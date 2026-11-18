import XCTest
@testable import Quizfolk

final class QuestionReadingTimeTests:XCTestCase {
    func testLongQuestionsReceiveMoreTimeWithoutPenalisingUnicode() {
        XCTAssertEqual(QuestionReadingTime.seconds(for:"Which planet is known as the Red Planet?"),3)
        XCTAssertEqual(QuestionReadingTime.seconds(for:String(repeating:"word ",count:12)),3)
        XCTAssertEqual(QuestionReadingTime.seconds(for:String(repeating:"word ",count:30)),9)
        XCTAssertEqual(QuestionReadingTime.seconds(for:String(repeating:"word ",count:60)),19)
        XCTAssertEqual(QuestionReadingTime.seconds(for:String(repeating:"🌿",count:90)),4)
        XCTAssertEqual(QuestionReadingTime.seconds(for:"  one\t two\nthree\u{00A0}four  "),3)
    }
}
