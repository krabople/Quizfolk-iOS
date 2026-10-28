import SwiftUI

struct TopicLeaguePanel:View {
 @EnvironmentObject var store:QuizStore
 let topic:Topic
 @State private var monthly=true
 @State private var following=false
 @State private var entries:[BoardEntry]=[]
 @State private var loading=false
 @State private var error:String?
 var body:some View {
  VStack(alignment:.leading,spacing:18) {
   Label("\(topic.name) league",systemImage:"trophy.fill").font(.system(size:23,weight:.bold,design:.rounded)).foregroundStyle(topic.tint)
   Picker("League period",selection:$monthly){Text("This month").tag(true);Text("All time").tag(false)}.pickerStyle(.segmented).accessibilityIdentifier("leaguePeriod")
   Picker("League players",selection:$following){Text("Everyone").tag(false);Text("Following + you").tag(true)}.pickerStyle(.segmented).accessibilityIdentifier("leaguePlayers")
   Text(monthly ? "Monthly topic XP · resets on the 1st at 00:00 UTC":"Lifetime XP earned in this topic").font(.caption).foregroundStyle(.secondary)
   if loading {ProgressView("Loading \(topic.name) rankings…")}
   if entries.isEmpty && !loading {Text(following ? "Follow players in People to build your friends’ league. Your completed online duels appear here too.":"No completed online duels in this topic yet. Play one to set the pace.").font(.subheadline).foregroundStyle(.secondary).padding(.vertical,12)}
   HStack{Text("RANK").frame(width:42,alignment:.leading);Text("PLAYER");Spacer();Text("TOPIC XP")}.font(.system(size:10,weight:.heavy)).foregroundStyle(.secondary)
   ForEach(Array(entries.enumerated()),id:\.element.id){i,row in
    NavigationLink{PublicPlayerView(playerID:row.id)}label:{HStack(spacing:12){Text("\(i+1)").font(.system(size:22,weight:.bold,design:.rounded)).frame(width:32).foregroundStyle(i<3 ? Color(hex:"C28D2F"):Color.ink);PlayerPortrait(name:row.name,avatar:row.avatar,size:38);VStack(alignment:.leading,spacing:4){Text(row.name).font(.headline).lineLimit(1);Text("\(row.matches) duels").font(.caption).foregroundStyle(.secondary)};Spacer();Text("\(row.xp)").font(.headline)}.padding(13).foregroundStyle(Color.ink).background(.white,in:RoundedRectangle(cornerRadius:15))}.buttonStyle(.plain)
   }
   if let error {Text(error).font(.caption).foregroundStyle(.red)}
   Button("Refresh \(topic.name) league"){Task{await load()}}.font(.subheadline.bold()).tint(topic.tint)
   Text("XP = your match score + 40 for finishing + 100 for a win or 50 for a draw. A challenge enters the table after both people finish. Practice stays out of online leagues.").font(.caption).foregroundStyle(.secondary)
  }.frame(maxWidth:.infinity,alignment:.leading).task(id:"\(topic.id)-\(monthly)-\(following)"){await load()}
 }
 private func load()async {
  loading=true;defer{loading=false};error=nil
  if store.isUITesting {entries=[BoardEntry(id:"test-rival",name:"Sample Rival",avatar:nil,xp:700,matches:4)];return}
  if store.profile==nil{await store.connect()}
  do{let r:BoardReply=try await store.request("leaderboard",query:[URLQueryItem(name:"topic",value:topic.id),URLQueryItem(name:"period",value:monthly ? "month":"all"),URLQueryItem(name:"scope",value:following ? "following":"all")]);guard !Task.isCancelled else{return};entries=r.entries}catch{if !Task.isCancelled{self.error=error.localizedDescription}}
 }
}
