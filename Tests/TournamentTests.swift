import XCTest
@testable import Quizfolk

@MainActor final class TournamentTests:XCTestCase {
 func testRunContinuesBeyondSevenAndStopsOnFirstWrongAnswer() async throws {
  let store=QuizStore();let fixture=TournamentFixture()
  store.testResponse={route,body in try await fixture.response(route,body)}
  let game=TournamentSession(event:QuizStore.testTournamentList().events[0],topic:store.topics.first{$0.id=="22"}!,store:store)
  defer{game.stop()}
  await game.begin()
  for n in 1...9 {
   await game.answer(0)
   XCTAssertEqual(game.score,n*20);XCTAssertEqual(game.streak,n)
   XCTAssertFalse(game.runEnded);XCTAssertTrue(game.revealed)
   await game.next()
  }
  await game.answer(1)
  XCTAssertEqual(game.score,180);XCTAssertEqual(game.streak,9)
  XCTAssertTrue(game.runEnded);XCTAssertEqual(game.correctIndex,0)
  XCTAssertFalse(game.showResult)
  await game.next();XCTAssertTrue(game.showResult)
 }
 func testTimeoutSubmissionIsNotCancelledByItsOwnTimer() async throws {
  let store=QuizStore();let fixture=TournamentFixture();fixture.remaining=0.05
  store.testResponse={route,body in try await fixture.response(route,body)}
  let game=TournamentSession(event:QuizStore.testTournamentList().events[0],topic:store.topics[0],store:store)
  defer{game.stop()};await game.begin()
  for _ in 0..<100 {
   if game.revealed || game.error != nil {break}
   try await Task.sleep(for:.milliseconds(20))
  }
  XCTAssertNil(game.error);XCTAssertTrue(game.runEnded);XCTAssertTrue(game.revealed)
  XCTAssertEqual(game.score,0);XCTAssertEqual(game.selected,-1)
  XCTAssertEqual(fixture.submissions,1)
 }
}

@MainActor private final class TournamentFixture {
 var remaining=10.0
 var submissions=0
 private var turn=0
 private var score=0
 private var streak=0
 private var state="playing"
 func response(_ route:String,_ body:[String:Any]?) async throws -> Data {
  // A real URLSession request also observes cancellation. This catches a timer
  // cancelling the very task that is submitting the timeout answer.
  try Task.checkCancellation()
  var r:[String:Any]=["id":"fixture-run","eventID":"test-event","score":score,"streak":streak,"turn":turn,"state":state]
  switch route {
  case "tournament-enter":break
  case "tournament-round":
   r["question"]=["id":"q-\(turn)","prompt":"Fixture question \(turn)?","answers":["Correct","Wrong","Other","Another"],"difficulty":"easy"]
   r["remaining"]=remaining;r["readingRemaining"]=0;r["phase"]="answer"
  case "tournament-answer":
   XCTAssertEqual(body?["turn"] as? Int,turn)
   submissions+=1;let correct=(body?["answer"] as? Int)==0
   turn+=1
   if correct {score+=20;streak+=1}else{state="finished"}
   r=["id":"fixture-run","eventID":"test-event","score":score,"streak":streak,"turn":turn,"state":state,"correctIndex":0,"points":correct ? 20:0,"correct":correct]
  default:throw APIError.message("Unexpected fixture route: \(route)")
  }
  return try JSONSerialization.data(withJSONObject:r)
 }
}
