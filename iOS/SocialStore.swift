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
 func rematch(topic:Topic,opponentID:String?,online:Bool,requestID:String) async throws -> GameSession {
  if let opponentID {
   let start=try await createChallenge(player:opponentID,topic:topic.id,requestID:requestID)
   return GameSession(topic:topic,store:self,online:true,match:start)
  }
  if online {
   let start:StartReply=try await request("match",body:["topic":topic.id,"botOnly":true])
   return GameSession(topic:topic,store:self,online:true,match:start)
  }
  return GameSession(topic:topic,store:self,online:false)
 }
 func openChallenge(_ id:String) async throws -> StartReply {try await request("duel-open",body:["duel":id])}
 func declineChallenge(_ id:String) async throws {let _:OKReply=try await request("duel-decline",body:["duel":id]);await refreshSocial()}
 func refreshSocial() async {
  #if DEBUG
  if StoreScreenshotFixture.enabled {challenges=StoreScreenshotFixture.challenges;activity=[];return}
  #endif
  #if DEBUG
  if isUITesting && testResponse==nil {challenges=[];activity=[];return}
  #else
  guard !isUITesting else {challenges=[];activity=[];return}
  #endif
  if profile==nil {await connect()}
  guard profile != nil else {return}
  do {
   async let inbox:ChallengesReply=request("duels")
   async let feed:ActivityReply=request("activity")
   let (d,f)=try await(inbox,feed);challenges=d.duels;activity=f.events;socialError=nil
   for card in challenges where card.complete {await resolveHistory(card)}
   if progressRefreshNeeded {try await refreshPlayerProgress()}
  } catch {socialError=error.localizedDescription}
 }
 func resolveHistory(_ card:ChallengeCard) async {
  guard let old=history.first(where:{$0.duelID==card.id && $0.pending==true}) else {return}
  do {
   let r=try await openChallenge(card.id)
   guard r.pending != true,r.played?.count==7 else {return}
   save(MatchRecord(id:old.id,topicID:old.topicID,date:old.date,score:r.score ?? old.score,opponentScore:r.opponentScore ?? old.opponentScore,opponent:r.opponent,kind:old.kind,rounds:r.played ?? old.rounds,duelID:card.id,pending:false,opponentID:r.opponentID,opponentAvatar:r.opponentAvatar))
   progressRefreshNeeded=true
  } catch {socialError=error.localizedDescription}
 }
 static func testCard(following:Bool,own:Bool=false,topicXP:Int=700)->PlayerCard {
  #if DEBUG
  if StoreScreenshotFixture.enabled {return StoreScreenshotFixture.card(own:own,following:following)}
  #endif
  let raw="""
  {"id":"\(own ? "test-self":"test-rival")","name":"\(own ? "UI Player":"Sample Rival")","avatar":null,"title":"Newcomer","interests":["22","17"],"sharedTopics":["22"],"following":\(following),"followers":\(following ? 1:0),"followingCount":0,"canChallenge":\(!own),"stats":{"matches":4,"wins":2,"draws":1,"xp":\(topicXP),"correct":20,"answered":28,"perfect":0},"topics":[{"topicID":"22","xp":\(topicXP),"level":\(TopicLevelling.progress(xp:topicXP).level),"matches":4,"wins":2}],"titles":[{"id":"newcomer","name":"Newcomer"}],"selectedTitle":"newcomer","discoverable":true,"challengesOpen":true,"headToHead":{"games":3,"wins":1,"draws":1,"losses":1},"badges":[{"id":"first","name":"First duel","symbol":"bolt.fill","earned":true,"group":"Duels","description":"Complete your first online duel.","progress":4,"target":1,"progressLabel":"1 / 1"},{"id":"duels:10000","name":"10,000 duels","symbol":"bolt.fill","earned":false,"group":"Duels","description":"Complete 10,000 online duels. Only completed online duels count.","progress":4,"target":10000,"progressLabel":"4 / 10,000"},{"id":"perfect","name":"Seven of seven","symbol":"checkmark.seal.fill","earned":false,"group":"Perfect games","description":"Answer all seven questions correctly in one completed online duel.","progress":0,"target":1,"progressLabel":"0 / 1"},{"id":"tournament-best:22","name":"Geography · Best #1","symbol":"trophy.fill","earned":true,"group":"Best tournament finishes","description":"Your highest public tournament placing in Geography. Only the best placing is shown here.","progress":1,"target":1,"progressLabel":"Best finish: 1st","topicID":"22","kind":"daily","rank":1}]}
  """
  return try! JSONDecoder().decode(PlayerCard.self,from:Data(raw.utf8))
 }
}
