import Foundation

struct TournamentWallet:Decodable {
 let coins:Int;let tickets:Int;let dailyClaimed:Bool
 func entryProblem(for event:TournamentEvent)->(title:String,message:String)? {
  // Resuming an admitted run never costs another entry fee.
  guard event.activeRun==nil else{return nil}
  if coins<event.coins {
   return ("Not enough coins","This tournament costs \(event.coins) coins. Your balance is \(coins) coins. Open Earn coins to complete your Daily Trail.")
  }
  return nil
 }
}
struct TournamentEvent:Decodable,Identifiable {
 let id:String;let topicID:String;let kind:String;let starts:Double;let ends:Double
 let coins:Int;let tickets:Int;let closed:Bool;let best:Int;let streak:Int;let attempts:Int;let players:Int
 let activeRun:String?;let rank:Int?;let reward:Int
 var featured:Bool?=nil
 var prizePool:Int?=nil
 var isFeatured:Bool {featured ?? true}
 var entryLabel:String {"\(coins) coins"}
}
struct TournamentList:Decodable {let events:[TournamentEvent];let wallet:TournamentWallet}
struct TournamentEntry:Decodable,Identifiable {let id:String;let name:String;let avatar:String?;let rank:Int;let score:Int;let streak:Int;let reward:Int}
struct TournamentBoard:Decodable {let event:TournamentEvent;let entries:[TournamentEntry];let own:[TournamentEntry];let wallet:TournamentWallet}
struct TournamentRunReply:Decodable {
 let id:String;let eventID:String;let score:Int;let streak:Int;let turn:Int;let state:String
 let question:PublicQuestion?;let remaining:Double?;let readingRemaining:Double?;let phase:String?
 let correctIndex:Int?;let points:Int?;let correct:Bool?
 var questionChanged:Bool?=nil
}

extension QuizStore {
 func tournamentList() async throws -> TournamentList {
  if isUITesting {return Self.testTournamentList()}
  if profile==nil {await connect()}
  return try await request("tournaments")
 }
 func tournamentBoard(_ id:String) async throws -> TournamentBoard {
  if isUITesting {
   return TournamentBoard(event:Self.testTournamentList().events[0],entries:[],own:[],wallet:Self.testTournamentList().wallet)
  }
  return try await request("tournament-board",query:[URLQueryItem(name:"event",value:id)])
 }
 static func testTournamentList()->TournamentList {
  let emptyWallet=ProcessInfo.processInfo.arguments.contains("--ui-testing-empty-wallet")
  return TournamentList(events:[TournamentEvent(id:"test-event",topicID:"22",kind:"daily",starts:Date().timeIntervalSince1970-100,ends:Date().timeIntervalSince1970+3600,coins:25,tickets:0,closed:false,best:0,streak:0,attempts:0,players:0,activeRun:nil,rank:nil,reward:0)],wallet:TournamentWallet(coins:emptyWallet ? 0:100,tickets:0,dailyClaimed:false))
 }
}
