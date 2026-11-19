import Foundation

struct PlayerStats:Decodable {let matches:Int;let wins:Int;let draws:Int;let xp:Int;let correct:Int;let answered:Int;let perfect:Int}
struct TopicProgress:Decodable,Identifiable {var id:String{topicID};let topicID:String;let xp:Int;let level:Int;let matches:Int;let wins:Int}
struct EarnedTitle:Decodable,Identifiable {let id:String;let name:String}
struct PlayerBadge:Decodable,Identifiable {
 let id:String;let name:String;let symbol:String;let earned:Bool
 var topicID:String?=nil;var kind:String?=nil;var rank:Int?=nil
 var description:String?=nil;var progress:Int?=nil;var target:Int?=nil;var progressLabel:String?=nil;var group:String?=nil
 var requirementText:String {
  if let description,!description.isEmpty{return description}
  switch id {
  case "first":return "Complete your first online duel."
  case "winner":return "Win your first completed online duel."
  case "perfect":return "Answer all seven questions correctly in one completed online duel."
  case "ten":return "Complete ten online duels."
  case "explorer":return "Complete online duels in five different topics."
  default:return topicID == nil ? "Complete this milestone through online play.":"Earn a podium finish in a tournament in this topic."
  }
 }
 var groupName:String {group ?? (topicID == nil ? "Milestones":"Best tournament finishes")}
 var progressFraction:Double? {
  guard let progress,let target,target>0 else{return nil}
  return min(1,max(0,Double(progress)/Double(target)))
 }
}
struct HeadToHead:Decodable {let games:Int;let wins:Int;let draws:Int;let losses:Int}
struct PlayerCard:Decodable,Identifiable {
 let id:String;let name:String;let avatar:String?;let title:String;let interests:[String];let sharedTopics:[String]
 let following:Bool;let followers:Int;let followingCount:Int;let canChallenge:Bool
 let stats:PlayerStats;let topics:[TopicProgress];let titles:[EarnedTitle];let selectedTitle:String
 let discoverable:Bool;let challengesOpen:Bool;let headToHead:HeadToHead?;let badges:[PlayerBadge]?
 var displayBadge:TournamentPrize?=nil
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
