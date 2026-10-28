import Foundation

struct PlayerStats:Decodable {let matches:Int;let wins:Int;let draws:Int;let xp:Int;let correct:Int;let answered:Int;let perfect:Int}
struct TopicProgress:Decodable,Identifiable {var id:String{topicID};let topicID:String;let xp:Int;let level:Int;let matches:Int;let wins:Int}
struct EarnedTitle:Decodable,Identifiable {let id:String;let name:String}
struct PlayerBadge:Decodable,Identifiable {let id:String;let name:String;let symbol:String;let earned:Bool}
struct HeadToHead:Decodable {let games:Int;let wins:Int;let draws:Int;let losses:Int}
struct PlayerCard:Decodable,Identifiable {
 let id:String;let name:String;let avatar:String?;let title:String;let interests:[String];let sharedTopics:[String]
 let following:Bool;let followers:Int;let followingCount:Int;let canChallenge:Bool
 let stats:PlayerStats;let topics:[TopicProgress];let titles:[EarnedTitle];let selectedTitle:String
 let discoverable:Bool;let challengesOpen:Bool;let headToHead:HeadToHead?;let badges:[PlayerBadge]?
}
struct PeopleReply:Decodable {let players:[PlayerCard]}
struct ChallengeCard:Decodable,Identifiable {
 let id:String;let topicID:String;let opponentID:String?;let opponent:String;let avatar:String?
 let status:String;let incoming:Bool;let accepted:Bool;let ownFinished:Bool;let opponentFinished:Bool
 let score:Int;let opponentScore:Int?;let created:Double;let expires:Double;let matchID:String?
 var complete:Bool {status=="complete"}
 var available:Bool {status=="invited" || status=="accepted"}
 var needsTurn:Bool {available && !ownFinished}
 var statusText:String {
  if complete {return score==(opponentScore ?? 0) ? "Draw":(score>(opponentScore ?? 0) ? "You won":"You lost")}
  if !available {return status.capitalized}
  if ownFinished {return accepted ? "Waiting for their answers":"Played · invitation pending"}
  return incoming && !accepted ? "Invitation · your turn":"Your turn"
 }
}
struct ChallengesReply:Decodable {let duels:[ChallengeCard]}
struct FriendActivity:Decodable,Identifiable {let id:String;let playerID:String;let name:String;let avatar:String?;let topicID:String;let score:Int;let won:Bool;let draw:Bool;let date:Double}
struct ActivityReply:Decodable {let events:[FriendActivity]}
struct SearchReply:Decodable {let searchID:String;let state:String;let elapsed:Double;let match:StartReply?}
