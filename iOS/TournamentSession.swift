import SwiftUI

@MainActor final class TournamentSession:ObservableObject,Identifiable {
 let id=UUID()
 let event:TournamentEvent
 let topic:Topic
 private let store:QuizStore
 private let requestID=UUID().uuidString
 private var runID:String?
 private var turn=0
 private var timer:Task<Void,Never>?
 private var readingTask:Task<Void,Never>?
 private var closed=false
 private var pendingAnswer:Int?
 @Published var question:PublicQuestion?
 @Published var score=0
 @Published var streak=0
 @Published var remaining=10.0
 @Published var reading=false
 @Published var revealed=false
 @Published var selected:Int?
 @Published var correctIndex:Int?
 @Published var lastPoints=0
 @Published var runEnded=false
 @Published var showResult=false
 @Published var busy=false
 @Published var error:String?
 var hasStarted:Bool {runID != nil}
 init(event:TournamentEvent,topic:Topic,store:QuizStore) {
  self.event=event;self.topic=topic;self.store=store;runID=event.activeRun
 }
 func begin() async {
  guard !closed,!busy else{return}
  busy=true;defer{busy=false};error=nil
  do {
   if runID==nil {
    let r:TournamentRunReply=try await store.request("tournament-enter",body:["event":event.id,"requestID":requestID])
    runID=r.id;apply(r)
   }
   try await loadRound()
  } catch {self.error=error.localizedDescription}
 }
 private func apply(_ r:TournamentRunReply) {
  score=r.score;streak=r.streak;turn=r.turn;runEnded=r.state != "playing"
 }
 private func loadRound() async throws {
  guard let runID else{return}
  let r:TournamentRunReply=try await store.request("tournament-round",body:["run":runID])
  apply(r)
  if runEnded {showResult=true;return}
  selected=nil;correctIndex=nil;revealed=false;showQuestion(r)
 }
 private func showQuestion(_ r:TournamentRunReply) {
  question=r.question;remaining=r.remaining ?? 10;reading=r.phase=="reading"
  if reading {
   timer?.cancel();readingTask?.cancel()
   readingTask=Task {[weak self] in
    guard let self,let runID=self.runID else{return}
    do {
     try await Task.sleep(for:.seconds(max(0,r.readingRemaining ?? 2)))
     guard !self.closed,!Task.isCancelled else{return}
     let next:TournamentRunReply=try await self.store.request("tournament-reveal",body:["run":runID])
     guard !self.closed,!Task.isCancelled else{return}
     self.apply(next)
     if self.runEnded {self.showResult=true}else{self.showQuestion(next)}
    } catch {if !Task.isCancelled{self.error=error.localizedDescription}}
   }
  } else {startTimer(remaining)}
 }
 private func startTimer(_ seconds:Double) {
  timer?.cancel();let start=ContinuousClock.now
  timer=Task {[weak self] in
   while !Task.isCancelled {
    do {try await Task.sleep(for:.milliseconds(50))}catch{return}
    guard let self,!self.closed,!self.revealed else{return}
    let d=start.duration(to:.now);let elapsed=Double(d.components.seconds)+Double(d.components.attoseconds)/1e18
    self.remaining=max(0,seconds-elapsed)
    if self.remaining<=0 {Task{await self.answer(-1)};return}
   }
  }
 }
 func answer(_ index:Int) async {
  guard !busy,!reading,!revealed,!runEnded,runID != nil else{return}
  timer?.cancel();selected=index;pendingAnswer=index
  await submitAnswer()
 }
 private func submitAnswer() async {
  guard let runID,let pendingAnswer else{return}
  busy=true;defer{busy=false};error=nil
  do {
   let r:TournamentRunReply=try await store.request("tournament-answer",body:["run":runID,"turn":turn,"answer":pendingAnswer])
   apply(r);correctIndex=r.correctIndex;lastPoints=r.points ?? 0;revealed=true;reading=false;self.pendingAnswer=nil
   if r.correctIndex==nil && runEnded {showResult=true}
  } catch {self.error=error.localizedDescription}
 }
 func next() async {
  if runEnded {showResult=true;return}
  busy=true;defer{busy=false};error=nil
  do{try await loadRound()}catch{self.error=error.localizedDescription}
 }
 func retry() async {
  if pendingAnswer != nil {await submitAnswer()}else{await begin()}
 }
 func end() async -> Bool {
  guard let runID else{return true}
  timer?.cancel();readingTask?.cancel();busy=true;defer{busy=false}
  do {
   let r:TournamentRunReply=try await store.request("tournament-end",body:["run":runID])
   apply(r);showResult=true;error=nil;return true
  } catch {self.error=error.localizedDescription;return false}
 }
 func resume() async {
  guard !closed,!revealed,!showResult,!busy,runID != nil else{return}
  readingTask?.cancel();timer?.cancel();await next()
 }
 func stop(){closed=true;timer?.cancel();readingTask?.cancel()}
}
