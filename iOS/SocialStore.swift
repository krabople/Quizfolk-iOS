import Foundation

extension QuizStore {
 func loadPeople(query:String="",mode:String="discover") async {
  let requestID=UUID();peopleRequest=requestID;socialError=nil
  if isUITesting {people=mode=="following" && !testFollowing ? []:[Self.testCard(following:testFollowing)];return}
  if profile==nil {await connect()}
  do {let r:PeopleReply=try await request("people",query:[URLQueryItem(name:"q",value:query),URLQueryItem(name:"mode",value:mode)]);if peopleRequest==requestID{people=r.players}}
  catch {if peopleRequest==requestID{socialError=error.localizedDescription}}
 }
 func playerCard(_ id:String?=nil) async throws -> PlayerCard {
  if isUITesting {return Self.testCard(following:testFollowing,own:id==nil || id==profile?.id)}
  if profile==nil {await connect()}
  return try await request("player",query:id.map{[URLQueryItem(name:"id",value:$0)]} ?? [])
 }
 func followPlayer(_ id:String,enabled:Bool) async throws {
  if isUITesting {testFollowing=enabled;return}
  let _:OKReply=try await request("follow",body:["player":id,"enabled":enabled])
 }
 func blockPlayer(_ id:String,enabled:Bool) async throws {let _:OKReply=try await request("block",body:["player":id,"enabled":enabled]);await refreshSocial()}
 func saveSocial(interests:[String]?=nil,title:String?=nil,discoverable:Bool?=nil,challengesOpen:Bool?=nil) async throws {
  var body:[String:Any]=[:]
  if let interests {body["interests"]=interests};if let title {body["titleID"]=title};if let discoverable {body["discoverable"]=discoverable};if let challengesOpen {body["challengesOpen"]=challengesOpen}
  let _:OKReply=try await request("social-settings",body:body)
 }
 func createChallenge(player:String,topic:String,requestID:String) async throws -> StartReply {try await request("challenge",body:["player":player,"topic":topic,"requestID":requestID])}
 func openChallenge(_ id:String) async throws -> StartReply {try await request("duel-open",body:["duel":id])}
 func declineChallenge(_ id:String) async throws {let _:OKReply=try await request("duel-decline",body:["duel":id]);await refreshSocial()}
 func refreshSocial() async {
  guard !isUITesting else {challenges=[];activity=[];return}
  if profile==nil {await connect()}
  guard profile != nil else {return}
  do {
   async let inbox:ChallengesReply=request("duels")
   async let feed:ActivityReply=request("activity")
   let (d,f)=try await(inbox,feed);challenges=d.duels;activity=f.events;socialError=nil
   let newlyCompleted=challenges.contains{c in c.complete && history.contains{$0.duelID==c.id && $0.pending==true}}
   for card in challenges where card.complete {await resolveHistory(card)}
   if newlyCompleted{await connect()}
  } catch {socialError=error.localizedDescription}
 }
 func resolveHistory(_ card:ChallengeCard) async {
  guard let index=history.firstIndex(where:{$0.duelID==card.id && $0.pending==true}) else {return}
  do {
   let r=try await openChallenge(card.id);let old=history[index]
   history[index]=MatchRecord(id:old.id,topicID:old.topicID,date:old.date,score:r.score ?? old.score,opponentScore:r.opponentScore ?? old.opponentScore,opponent:r.opponent,kind:old.kind,rounds:r.played ?? old.rounds,duelID:card.id,pending:false,opponentID:r.opponentID)
   persistHistory()
  } catch {socialError=error.localizedDescription}
 }
 static func testCard(following:Bool,own:Bool=false)->PlayerCard {
  let raw="""
  {"id":"\(own ? "test-self":"test-rival")","name":"\(own ? "UI Player":"Sample Rival")","avatar":null,"title":"Newcomer","interests":["22","17"],"sharedTopics":["22"],"following":\(following),"followers":\(following ? 1:0),"followingCount":0,"canChallenge":\(!own),"stats":{"matches":4,"wins":2,"draws":1,"xp":700,"correct":20,"answered":28,"perfect":1},"topics":[{"topicID":"22","xp":700,"level":3,"matches":4,"wins":2}],"titles":[{"id":"newcomer","name":"Newcomer"}],"selectedTitle":"newcomer","discoverable":true,"challengesOpen":true,"headToHead":{"games":3,"wins":1,"draws":1,"losses":1},"badges":[{"id":"first","name":"First duel","symbol":"bolt.fill","earned":true}]}
  """
  return try! JSONDecoder().decode(PlayerCard.self,from:Data(raw.utf8))
 }
}
