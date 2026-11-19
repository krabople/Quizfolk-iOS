import XCTest
@testable import Quizfolk

final class AchievementTests:XCTestCase {
 private func decode(_ values:[String:Any])throws->PlayerBadge {try JSONDecoder().decode(PlayerBadge.self,from:JSONSerialization.data(withJSONObject:values))}
 func testLegacyLockedPerfectStillExplainsSevenCorrectAnswers()throws {
  let badge=try decode(["id":"perfect","name":"Seven of seven","symbol":"checkmark.seal.fill","earned":false])
  XCTAssertTrue(badge.requirementText.contains("all seven questions correctly"));XCTAssertNil(badge.progressFraction)
 }
 func testNewLockedAndEarnedRequirementsDecodeWithoutLosingProgress()throws {
  var value:[String:Any]=["id":"duels:1000","name":"1,000 duels","symbol":"bolt.fill","earned":false,"description":"Complete 1,000 online duels.","group":"Duels","progress":999,"target":1000,"progressLabel":"999 / 1,000"]
  let locked=try decode(value);XCTAssertEqual(locked.requirementText,"Complete 1,000 online duels.");XCTAssertEqual(locked.groupName,"Duels");XCTAssertEqual(locked.progressFraction!,0.999,accuracy:0.0001)
  value["earned"]=true;value["progress"]=1200
  let earned=try decode(value);XCTAssertEqual(earned.progressFraction,1);XCTAssertEqual(earned.requirementText,locked.requirementText)
 }
 func testBestTopicTrophyRetainsEmblemMetadataAndMeaning()throws {
  let badge=try decode(["id":"tournament-best:18","name":"Computers · Best #1","symbol":"trophy.fill","earned":true,"topicID":"18","kind":"weekly","rank":1,"description":"Highest public tournament placing in Computers.","progress":1,"target":1,"progressLabel":"Best finish: 1st","group":"Best tournament finishes"])
  XCTAssertEqual(badge.topicID,"18");XCTAssertEqual(badge.rank,1);XCTAssertEqual(badge.kind,"weekly");XCTAssertTrue(badge.requirementText.contains("Highest"));XCTAssertEqual(badge.progressFraction,1)
 }
}
