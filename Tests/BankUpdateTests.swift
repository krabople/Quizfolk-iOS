import XCTest
@testable import Quizfolk

final class BankUpdateTests:XCTestCase {
    private func fixture()->[String:Any] {
        ["format":1,"categories":[["id":"99","name":"A new topic","symbol":"leaf","color":"008080","emoji":"🌿","questionCount":7]],
         "questions":(0..<7).map{["id":"new-\($0)","categoryID":"99","difficulty":"easy","prompt":"New question \($0)?","answers":["A","B","C","D"],"correctIndex":0] as [String:Any]}]
    }
    private func decode(_ value:[String:Any])throws->MobileQuestionBank {try MobileQuestionBank.decode(JSONSerialization.data(withJSONObject:value))}
    func testNewTopicAndQuestionsCanArriveAsData()throws {
        let bank=try decode(fixture())
        XCTAssertEqual(bank.categories.first?.id,"99");XCTAssertEqual(bank.questions.count,7)
    }
    func testRejectsWrongCountsUnknownTopicsAndDuplicateIDs() {
        var value=fixture();var topics=value["categories"] as! [[String:Any]]
        topics[0]["questionCount"]=8;value["categories"]=topics;XCTAssertThrowsError(try decode(value))
        value=fixture();var questions=value["questions"] as! [[String:Any]]
        questions[0]["categoryID"]="missing";value["questions"]=questions;XCTAssertThrowsError(try decode(value))
        value=fixture();questions=value["questions"] as! [[String:Any]]
        questions[1]["id"]=questions[0]["id"];value["questions"]=questions;XCTAssertThrowsError(try decode(value))
    }
    func testRejectsInvalidCorrectAnswerAndDuplicateChoices() {
        var value=fixture();var questions=value["questions"] as! [[String:Any]]
        questions[0]["correctIndex"]=4;value["questions"]=questions;XCTAssertThrowsError(try decode(value))
        value=fixture();questions=value["questions"] as! [[String:Any]]
        questions[0]["answers"]=["A","A","C","D"];value["questions"]=questions;XCTAssertThrowsError(try decode(value))
    }
    func testSnapshotHashChangesWhenQuestionChanges()throws {
        let data=try JSONSerialization.data(withJSONObject:fixture(),options:.sortedKeys)
        var changed=data;changed.append(32)
        XCTAssertNotEqual(QuestionBankUpdates.sha(data),QuestionBankUpdates.sha(changed))
        XCTAssertEqual(QuestionBankUpdates.sha(Data("abc".utf8)),"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    }
}
