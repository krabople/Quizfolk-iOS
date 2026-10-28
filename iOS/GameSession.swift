import Foundation
import SwiftUI

struct PublicQuestion:Decodable {let id:String;let prompt:String;let answers:[String];let difficulty:String;let source:String?;let sourceURL:String?}
struct StartReply:Decodable {let id:String;let kind:String;let opponent:String;let opponentAvatar:String?;var opponentID:String?=nil;var duelID:String?=nil;var played:[PlayedRound]?=nil;var score:Int?=nil;var opponentScore:Int?=nil;var pending:Bool?=nil}
struct RoundReply:Decodable {let round:Int;let question:PublicQuestion;let remaining:Double;let readingRemaining:Double?;let phase:String?}
struct AnswerReply:Decodable {let points:Int;let correctIndex:Int;let opponentPoints:Int;let finished:Bool;let score:Int;let opponentScore:Int;let pending:Bool?}
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
    @Published var opponentAvatar:String?
    @Published var opponentID:String?
    @Published var duelID:String?
    @Published var awaitingOpponent=false
    @Published var reading=false
    @Published var searching=false
    @Published var searchMessage="Looking for players in this topic…"
    private let searchRequestID=UUID().uuidString
    private let localHistoryID=UUID().uuidString
    private var readingTask:Task<Void,Never>?
    private var searchID:String?
    private var suppliedMatch:StartReply?
    var isHuman:Bool {online && kind != "bot"}
    var canCloseWithoutWarning:Bool {finished || rounds.count==7 || (showIntro && current==nil)}
    @Published var busy=false
    @Published var error:String?
    @Published var finished=false
    @Published var showIntro=true
    @Published var prepared=false
    @Published var introCount=3
    @Published var introCounting=false
    @Published var rounds:[PlayedRound]=[]
    @Published var lastPoints=0
    @Published var revealed=false
    private var matchID=""
    private var start:ContinuousClock.Instant?
    private var timer:Task<Void,Never>?
    private var closed=false
    private var pendingAnswer:Int?
    private var pendingElapsed=0.0
    private var store:QuizStore
    init(topic:Topic,store:QuizStore,online:Bool,match:StartReply?=nil) {self.topic=topic;self.store=store;self.online=online;self.suppliedMatch=match;self.searching=online && match==nil}
    func begin() async {
        busy=true;error=nil;defer{busy=false;searching=false}
        do {
            if online {
                if store.profile==nil {await store.connect();if let message=store.onlineError {throw APIError.message(message)}}
                if let suppliedMatch {apply(suppliedMatch)}
                else {
                    searching=true;defer{searching=false}
                    for attempt in 0..<7 {
                        guard !closed,!Task.isCancelled else {return}
                        let reply:SearchReply=try await store.request("match-search",body:["topic":topic.id,"requestID":searchRequestID])
                        searchID=reply.searchID
                        if let match=reply.match {apply(match);break}
                        searchMessage=attempt<2 ? "Looking for players in \(topic.name)…":"Still checking for a human opponent…"
                        try await Task.sleep(for:.seconds(2))
                    }
                    guard !matchID.isEmpty else {throw APIError.message("The search took too long. Please try again.")}
                }
            } else {
                packet=store.packet(topic)
                guard packet.count==7 else {throw APIError.message("This topic needs at least seven questions.")}
            }
            prepared=true
        } catch {self.error=error.localizedDescription}
        busy=false
    }
    private func apply(_ r:StartReply) {
        matchID=r.id;opponent=r.opponent;opponentAvatar=r.opponentAvatar;kind=r.kind;opponentID=r.opponentID;duelID=r.duelID
        rounds=r.played ?? [];score=r.score ?? 0;opponentScore=r.opponentScore ?? 0;awaitingOpponent=r.pending ?? false
        if rounds.count==7 {round=6;current=rounds.last?.question;revealed=true;finished=true;saveResult()}
        else {round=rounds.count}
    }
    private func saveResult() {
        store.save(MatchRecord(id:online ? matchID:localHistoryID,topicID:topic.id,date:Date(),score:score,opponentScore:opponentScore,opponent:opponent,kind:online ? kind:"practice",rounds:rounds,duelID:duelID,pending:duelID == nil ? false:awaitingOpponent,opponentID:opponentID))
    }
    func refreshResult() async {
        guard let duelID else {return};busy=true;defer{busy=false}
        do {let r=try await store.openChallenge(duelID);apply(r);await store.refreshSocial();await store.connect();error=nil} catch {self.error=error.localizedDescription}
    }
    func countdownAndStart() async {
        guard prepared,showIntro,!introCounting,!busy else {return}
        introCounting=true;defer{introCounting=false}
        for n in (1...3).reversed() {
            guard !Task.isCancelled,!closed,showIntro else {return};introCount=n
            do {try await Task.sleep(for:.seconds(1))} catch {return}
        }
        if !Task.isCancelled {await startPlaying()}
    }
    func startPlaying() async {
        guard !closed,showIntro,prepared,!busy else {return}
        busy=true;error=nil
        do {
            if online {try await getOnlineRound()}
            else {beginOfflineReading(packet[0])}
            showIntro=false
        } catch {self.error=error.localizedDescription}
        busy=false
    }
    private func getOnlineRound() async throws {
        let reply:RoundReply=try await store.request("round",body:["match":matchID]);applyQuestion(reply)
    }
    private func applyQuestion(_ reply:RoundReply) {
        round=reply.round
        current=Question(id:reply.question.id,categoryID:topic.id,difficulty:reply.question.difficulty,prompt:reply.question.prompt,answers:reply.question.answers,correctIndex:-1,source:reply.question.source,sourceURL:reply.question.sourceURL)
        if reply.phase=="reading" {
            timer?.cancel();reading=true;remaining=10;readingTask?.cancel()
            readingTask=Task{[weak self] in
                guard let self else{return}
                do {
                    try await Task.sleep(for:.seconds(max(0,reply.readingRemaining ?? 2)))
                    guard !self.closed,!Task.isCancelled else{return}
                    let shown:RoundReply=try await self.store.request("reveal",body:["match":self.matchID])
                    guard !self.closed,!Task.isCancelled else{return};self.applyQuestion(shown)
                } catch {if !Task.isCancelled {self.error=error.localizedDescription}}
            }
        } else {reading=false;startTimer(seconds:reply.remaining)}
    }
    private func beginOfflineReading(_ q:Question) {
        timer?.cancel();readingTask?.cancel();current=q;reading=true;remaining=10
        readingTask=Task{[weak self] in
            do{try await Task.sleep(for:.seconds(2))}catch{return}
            guard let self,!self.closed,!Task.isCancelled else{return};self.reading=false;self.startTimer(seconds:10)
        }
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
        guard !reading,!revealed,!busy,let q=current else {return}
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
                correct=r.correctIndex;points=r.points;other=r.opponentPoints;opponentScore=r.opponentScore-other;awaitingOpponent=r.pending ?? false
            } else {
                correct=q.correctIndex;points=Scoring.points(correct:index==correct,elapsed:elapsed,round:round)
                let chance=q.difficulty=="easy" ? 0.83 : (q.difficulty=="hard" ? 0.45:0.65)
                other=Scoring.points(correct:Double.random(in:0...1)<chance,elapsed:Double.random(in:1.2...9.8),round:round)
            }
            let revealedQ=Question(id:q.id,categoryID:q.categoryID,difficulty:q.difficulty,prompt:q.prompt,answers:q.answers,correctIndex:correct,source:q.source,sourceURL:q.sourceURL)
            current=revealedQ;lastPoints=points;score+=points;opponentScore+=other
            rounds.append(PlayedRound(question:revealedQ,selected:index,elapsed:elapsed,points:points,opponentPoints:other))
            revealed=true;pendingAnswer=nil
            if rounds.count==7 {saveResult()}
            UIImpactFeedbackGenerator(style:.light).impactOccurred()
        } catch {self.error=error.localizedDescription}
        busy=false
    }
    func retry() async {
        if showIntro {if prepared {await startPlaying()} else {await begin()};return}
        if let index=pendingAnswer,let q=current {busy=true;await submit(q:q,index:index,elapsed:pendingElapsed)}
        else if matchID.isEmpty {await begin()}
        else {busy=true;do {try await getOnlineRound();error=nil} catch{self.error=error.localizedDescription};busy=false}
    }
    func next() async {
        guard revealed else {return}
        if round==6 {
            finished=true
            saveResult()
            if online {await store.connect();await store.refreshSocial()}
            return
        }
        selected=nil;revealed=false;round+=1
        if online {busy=true;do {try await getOnlineRound()} catch{self.error=error.localizedDescription};busy=false}
        else {beginOfflineReading(packet[round])}
    }
    func stop() {closed=true;timer?.cancel();readingTask?.cancel();if let searchID {Task{let _:OKReply?=try? await store.request("cancel-search",body:["searchID":searchID])}}}
}
