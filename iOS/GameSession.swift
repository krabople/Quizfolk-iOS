import Foundation
import SwiftUI

struct PublicQuestion:Decodable {let id:String;let prompt:String;let answers:[String];let difficulty:String;let source:String?;let sourceURL:String?}
struct StartReply:Decodable {let id:String;let kind:String;let opponent:String}
struct RoundReply:Decodable {let round:Int;let question:PublicQuestion;let remaining:Double}
struct AnswerReply:Decodable {let points:Int;let correctIndex:Int;let opponentPoints:Int;let finished:Bool;let score:Int;let opponentScore:Int}
@MainActor final class GameSession:ObservableObject,Identifiable {
    let id=UUID()
    let topic:Topic
    let online:Bool
    @Published var packet:[Question]=[]
    @Published var current:Question?
    @Published var round=0
    @Published var selected:Int?
    @Published var remaining=10.0
    @Published var score=0
    @Published var opponentScore=0
    @Published var opponent="Pip · Bot"
    @Published var kind="bot"
    @Published var busy=false
    @Published var error:String?
    @Published var finished=false
    @Published var rounds:[PlayedRound]=[]
    @Published var lastPoints=0
    @Published var revealed=false
    private var matchID=""
    private var start:ContinuousClock.Instant?
    private var timer:Task<Void,Never>?
    private var pendingAnswer:Int?
    private var pendingElapsed=0.0
    private var store:QuizStore
    init(topic:Topic,store:QuizStore,online:Bool) {self.topic=topic;self.store=store;self.online=online}
    func begin() async {
        busy=true;error=nil
        do {
            if online {
                if store.profile==nil {await store.connect();if let message=store.onlineError {throw APIError.message(message)}}
                let r:StartReply=try await store.request("match",body:["topic":topic.id])
                matchID=r.id;opponent=r.opponent;kind=r.kind
                try await getOnlineRound()
            } else {
                packet=store.packet(topic)
                guard packet.count==7 else {throw APIError.message("This topic needs at least seven questions.")}
                current=packet[0];startTimer(seconds:10)
            }
        } catch {self.error=error.localizedDescription}
        busy=false
    }
    private func getOnlineRound() async throws {
        let reply:RoundReply=try await store.request("round",body:["match":matchID])
        round=reply.round
        current=Question(id:reply.question.id,categoryID:topic.id,difficulty:reply.question.difficulty,prompt:reply.question.prompt,answers:reply.question.answers,correctIndex:-1,source:reply.question.source,sourceURL:reply.question.sourceURL)
        startTimer(seconds:reply.remaining)
    }
    private func startTimer(seconds:Double) {
        timer?.cancel();remaining=max(0,seconds);start=ContinuousClock.now
        timer=Task { [weak self] in
            let allowance=max(0,seconds)
            while !Task.isCancelled {
                try? await Task.sleep(for:.milliseconds(50))
                guard !Task.isCancelled,let self,let start=self.start,!self.revealed else {return}
                let elapsed=Self.seconds(start.duration(to:.now))
                self.remaining=max(0,allowance-elapsed)
                if self.remaining<=0 {Task {await self.answer(-1)};return}
            }
        }
    }
    private static func seconds(_ d:Duration)->Double {Double(d.components.seconds)+Double(d.components.attoseconds)/1e18}
    func answer(_ index:Int) async {
        guard !revealed,!busy,let q=current else {return}
        timer?.cancel();busy=true;selected=index;pendingAnswer=index
        let elapsed=start.map{Self.seconds($0.duration(to:.now))} ?? 10
        pendingElapsed=elapsed
        await submit(q:q,index:index,elapsed:elapsed)
    }
    private func submit(q:Question,index:Int,elapsed:Double) async {
        error=nil
        do {
            let correct:Int;let points:Int;let other:Int
            if online {
                let r:AnswerReply=try await store.request("answer",body:["match":matchID,"round":round,"answer":index])
                correct=r.correctIndex;points=r.points;other=r.opponentPoints
            } else {
                correct=q.correctIndex;points=Scoring.points(correct:index==correct,elapsed:elapsed,round:round)
                let chance=q.difficulty=="easy" ? 0.83 : (q.difficulty=="hard" ? 0.45:0.65)
                other=Scoring.points(correct:Double.random(in:0...1)<chance,elapsed:Double.random(in:1.2...9.8),round:round)
            }
            let revealedQ=Question(id:q.id,categoryID:q.categoryID,difficulty:q.difficulty,prompt:q.prompt,answers:q.answers,correctIndex:correct,source:q.source,sourceURL:q.sourceURL)
            current=revealedQ;lastPoints=points;score+=points;opponentScore+=other
            rounds.append(PlayedRound(question:revealedQ,selected:index,elapsed:elapsed,points:points,opponentPoints:other))
            revealed=true;pendingAnswer=nil
            UIImpactFeedbackGenerator(style:.light).impactOccurred()
        } catch {self.error=error.localizedDescription}
        busy=false
    }
    func retry() async {
        if let index=pendingAnswer,let q=current {busy=true;await submit(q:q,index:index,elapsed:pendingElapsed)}
        else if matchID.isEmpty {await begin()}
        else {busy=true;do {try await getOnlineRound();error=nil} catch{self.error=error.localizedDescription};busy=false}
    }
    func next() async {
        guard revealed else {return}
        if round==6 {
            finished=true
            store.save(MatchRecord(id:online ? matchID:UUID().uuidString,topicID:topic.id,date:Date(),score:score,opponentScore:opponentScore,opponent:opponent,kind:online ? kind:"practice",rounds:rounds))
            if online {await store.connect()}
            return
        }
        selected=nil;revealed=false;round+=1
        if online {busy=true;do {try await getOnlineRound()} catch{self.error=error.localizedDescription};busy=false}
        else {current=packet[round];startTimer(seconds:10)}
    }
    func stop() {timer?.cancel()}
}
