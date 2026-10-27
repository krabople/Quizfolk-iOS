import SwiftUI

struct GameView:View {
 @ObservedObject var game:GameSession
 @EnvironmentObject var store:QuizStore
 @Environment(\.dismiss) var dismiss
 @Environment(\.accessibilityReduceMotion) var reduceMotion
 @State private var leave=false
 @State private var entered=false
 var body:some View {
  NavigationStack {
   Group {if game.finished {result} else if game.showIntro {intro} else {play}}
    .foregroundStyle(.white).background(LinearGradient(colors:[Color(hex:"102640"),game.topic.tint,Color(hex:"123452")],startPoint:.topLeading,endPoint:.bottomTrailing).ignoresSafeArea())
    .toolbarBackground(Color(hex:"102640"),for:.navigationBar).toolbarBackground(.visible,for:.navigationBar).toolbarColorScheme(.dark,for:.navigationBar)
    .toolbar {ToolbarItem(placement:.topBarLeading){Button{leave=true}label:{Image(systemName:"xmark")}.accessibilityLabel("Leave match")};ToolbarItem(placement:.principal){Text(game.topic.name).font(.headline)}}
    .confirmationDialog("Leave this duel? An unfinished duel earns no XP.",isPresented:$leave,titleVisibility:.visible){Button("Leave duel",role:.destructive){game.stop();dismiss()}}
  }.task{await game.begin()}.onDisappear{game.stop()}
 }
 private var intro:some View {
  VStack(spacing:26) {
   Image("BrandMark").resizable().frame(width:70,height:70).clipShape(RoundedRectangle(cornerRadius:18)).padding(.top,24)
   Text("A NEW RIVALRY").font(.system(size:12,weight:.black)).tracking(3)
   HStack(alignment:.top,spacing:12) {
    contestant(store.name,avatar:store.avatar,bot:false).offset(x:entered ? 0:-170)
    Text("VS").font(.system(size:25,weight:.black,design:.rounded)).foregroundStyle(Color(hex:"FFD494")).padding(.top,26)
    contestant(game.opponent,avatar:game.opponentAvatar,bot:game.kind != "human").offset(x:entered ? 0:170)
   }.accessibilityElement(children:.combine).accessibilityLabel("\(store.name) versus \(game.opponent)").accessibilityIdentifier("matchupTitle")
   Text(game.topic.emoji+" "+game.topic.name).font(.title3.bold())
   Text(game.online && game.kind=="human" ? "A recorded human run.\nSame seven questions. Your own pace.":"Seven questions. A friendly bot.\nSpeed and knowledge decide the winner.").font(.subheadline).multilineTextAlignment(.center).opacity(0.8)
   Spacer(minLength:0)
   if game.prepared {Text("\(game.introCount)").font(.system(size:58,weight:.heavy,design:.rounded)).contentTransition(.numericText());Button("Start duel"){Task{await game.startPlaying()}}.buttonStyle(PrimaryButton(color:.coral)).disabled(game.busy)}
   else if game.busy {ProgressView("Preparing your duel…").tint(.white)}
   if let error=game.error {Text(error).font(.caption);Button("Try again"){Task{await game.retry()}}.buttonStyle(.bordered)}
  }.padding(24).onAppear{withAnimation(reduceMotion ? nil:.spring(response:0.65,dampingFraction:0.7)){entered=true}}.task(id:game.prepared){if game.prepared {await game.countdownAndStart()}}
 }
 private func contestant(_ name:String,avatar:String?,bot:Bool)->some View {
  VStack(spacing:12){PlayerPortrait(name:name,avatar:avatar,bot:bot,size:88);Text(name).font(.headline).multilineTextAlignment(.center).lineLimit(2).minimumScaleFactor(0.7)}.frame(maxWidth:.infinity)
 }
 private var play:some View {
  GeometryReader {geometry in
   VStack(spacing:9) {
    HStack {player(store.name,avatar:store.avatar,score:game.score,bot:false);Text("VS").font(.system(size:12,weight:.black)).opacity(0.6);player(game.opponent,avatar:game.opponentAvatar,score:game.opponentScore,bot:game.kind != "human")}.frame(height:48)
    HStack(spacing:6){ForEach(0..<7){i in roundMarker(i)}}
    HStack {VStack(alignment:.leading,spacing:5){Text(game.round==6 ? "FINAL ROUND":"ROUND \(game.round+1) OF 7").font(.system(size:12,weight:.black)).tracking(1);Text(game.round==6 ? "DOUBLE POINTS":"FASTER = MORE POINTS").font(.system(size:9,weight:.bold)).foregroundStyle(Color(hex:"FFD494"))};Spacer();timer}.frame(height:78)
    if let q=game.current {
     Text(q.prompt).font(.system(size:25,weight:.bold,design:.rounded)).multilineTextAlignment(.center).lineLimit(7).minimumScaleFactor(0.65).frame(maxWidth:.infinity,maxHeight:.infinity).layoutPriority(1)
     VStack(spacing:9){ForEach(q.answers.indices,id:\.self){i in answer(q,index:i)}}.frame(height:geometry.size.height*(game.revealed ? 0.43:0.50))
     if game.revealed {
      Text(game.lastPoints>0 ? "+\(game.lastPoints) points · Correct!":(game.selected == -1 ? "Time’s up! The answer is highlighted.":"The correct answer is highlighted.")).font(.system(size:13,weight:.semibold)).lineLimit(1).minimumScaleFactor(0.8)
      Button(game.round==6 ? "See results":"Next question"){Task{await game.next()}}.buttonStyle(PrimaryButton(color:.coral)).accessibilityIdentifier("advanceQuestion")
     }
    } else {Spacer();ProgressView("Loading question…").tint(.white);Spacer()}
    if let error=game.error {Text(error).font(.caption);Button("Try again"){Task{await game.retry()}}.buttonStyle(.bordered)}
    Text("\(game.current?.source ?? "Open trivia contributors") · CC BY-SA 4.0").font(.system(size:8)).opacity(0.65).lineLimit(1)
   }.padding(.horizontal,18).padding(.vertical,10)
  }
 }
 private var timer:some View {
  ZStack {
   Circle().stroke(.white.opacity(0.18),lineWidth:6)
   Circle().trim(from:0,to:max(0,min(1,game.remaining/10))).stroke(game.remaining<=3 ? Color.coral:Color(hex:"FFD494"),style:StrokeStyle(lineWidth:6,lineCap:.round)).rotationEffect(.degrees(-90))
   VStack(spacing:-2){Text(String(format:"%.1f",game.remaining)).font(.system(size:29,weight:.black,design:.rounded)).monospacedDigit();Text("SECONDS").font(.system(size:8,weight:.heavy)).tracking(1)}
  }.frame(width:74,height:74).accessibilityElement(children:.ignore).accessibilityLabel("\(String(format:"%.1f",game.remaining)) seconds remaining").accessibilityIdentifier("roundTimer")
 }
 private func roundMarker(_ i:Int)->some View {
  let complete=i<game.rounds.count
  let right=complete && game.rounds[i].selected==game.rounds[i].question.correctIndex
  let state=complete ? (right ? "correct":"incorrect"):(i==game.round ? "current":"upcoming")
  return ZStack {Capsule().fill(complete ? (right ? Color.green:Color.coral):(i==game.round ? Color(hex:"FFD494"):.white.opacity(0.17)));if complete {Image(systemName:right ? "checkmark":"xmark").font(.system(size:8,weight:.black)).foregroundStyle(.white)}}.frame(height:13).accessibilityLabel("Round \(i+1): \(state)").accessibilityIdentifier("roundMarker-\(i)")
 }
 private func player(_ name:String,avatar:String?,score:Int,bot:Bool)->some View {
  HStack(spacing:8){PlayerPortrait(name:name,avatar:avatar,bot:bot,size:34);VStack(alignment:.leading,spacing:0){Text(name).font(.system(size:10,weight:.semibold)).lineLimit(1).minimumScaleFactor(0.6);Text("\(score)").font(.system(size:25,weight:.bold,design:.rounded))}}.frame(maxWidth:.infinity,alignment:.leading)
 }
 private func answer(_ q:Question,index:Int)->some View {
  let correct=game.revealed && index==q.correctIndex
  let wrong=game.revealed && game.selected==index && !correct
  return Button{Task{await game.answer(index)}}label:{
   HStack(spacing:12){Text(String(UnicodeScalar(65+index)!)).font(.system(size:14,weight:.black)).frame(width:31,height:31).background(Color.ink.opacity(0.08),in:Circle());Text(q.answers[index]).font(.system(size:18,weight:.semibold)).multilineTextAlignment(.leading).lineLimit(4).minimumScaleFactor(0.65).frame(maxWidth:.infinity,alignment:.leading);if correct {Image(systemName:"checkmark.circle.fill").foregroundStyle(.green)} else if wrong {Image(systemName:"xmark.circle.fill").foregroundStyle(.red)}}.foregroundStyle(Color.ink).padding(.horizontal,13).padding(.vertical,8).frame(maxWidth:.infinity,maxHeight:.infinity).background(correct ? Color(hex:"CCF3D7"):(wrong ? Color(hex:"FFDED7"):.white),in:RoundedRectangle(cornerRadius:17)).overlay{RoundedRectangle(cornerRadius:17).stroke(correct ? Color.green:(wrong ? Color.coral:.clear),lineWidth:3)}
  }.buttonStyle(.plain).disabled(game.revealed || game.busy || game.error != nil).accessibilityIdentifier("answer-\(index)")
 }
 private var result:some View {
  let won=game.score>game.opponentScore
  let tied=game.score==game.opponentScore
  let bonus=won ? 100:(tied ? 50:0)
  return ScrollView {
   VStack(spacing:18) {
    Image(systemName:tied ? "equal.circle.fill":"trophy.fill").font(.system(size:68)).foregroundStyle(Color(hex:"FFD494")).symbolEffect(.bounce,value:game.finished).padding(.top,20)
    Text(tied ? "IT’S A DRAW":(won ? "YOU WIN!":"\(game.opponent.uppercased()) WINS!")).font(.system(size:31,weight:.black,design:.rounded)).multilineTextAlignment(.center).accessibilityIdentifier("winnerAnnouncement")
    HStack(alignment:.top,spacing:14){podium(store.name,avatar:store.avatar,score:game.score,winner:won,bot:false);Text("–").font(.system(size:36,weight:.bold)).padding(.top,60);podium(game.opponent,avatar:game.opponentAvatar,score:game.opponentScore,winner:!won && !tied,bot:game.kind != "human")}
    VStack(spacing:8){Text("+\(Scoring.experience(score:game.score,opponentScore:game.opponentScore)) TOPIC XP").font(.system(size:25,weight:.black,design:.rounded));Text("\(game.score) score + 40 finish + \(bonus) \(tied ? "draw":"win") bonus").font(.caption);Text(game.online ? "Added to your \(game.topic.name) league":"Offline practice · local XP only").font(.caption).opacity(0.7)}.padding(16).frame(maxWidth:.infinity).background(.white.opacity(0.1),in:RoundedRectangle(cornerRadius:18))
    Button("Back to topics"){dismiss()}.buttonStyle(PrimaryButton(color:.coral))
    Text("\(game.rounds.filter{$0.selected==$0.question.correctIndex}.count) OF 7 CORRECT · DUEL REVIEW").font(.system(size:11,weight:.heavy)).tracking(1).padding(.top,10)
    ForEach(Array(game.rounds.enumerated()),id:\.element.id){index,r in
     VStack(alignment:.leading,spacing:8){HStack{Image(systemName:r.selected==r.question.correctIndex ? "checkmark.circle.fill":"xmark.circle.fill").foregroundStyle(r.selected==r.question.correctIndex ? Color.green:Color.coral);Text("QUESTION \(index+1)").font(.system(size:10,weight:.heavy));Spacer();Text("+\(r.points)").bold()};Text(r.question.prompt).font(.subheadline.bold());Text("Answer: \(r.question.answers[r.question.correctIndex])").font(.caption)}.padding(16).frame(maxWidth:.infinity,alignment:.leading).foregroundStyle(Color.ink).background(.white,in:RoundedRectangle(cornerRadius:16))
    }
   }.padding(22)
  }.overlay(alignment:.top){if !reduceMotion {VictoryConfetti().allowsHitTesting(false)}}
 }
 private func podium(_ name:String,avatar:String?,score:Int,winner:Bool,bot:Bool)->some View {
  VStack(spacing:7){Image(systemName:"crown.fill").foregroundStyle(Color(hex:"FFD494")).opacity(winner ? 1:0).frame(height:15);PlayerPortrait(name:name,avatar:avatar,bot:bot,size:66);Text(name).font(.caption.bold()).lineLimit(2).multilineTextAlignment(.center);Text("\(score)").font(.system(size:39,weight:.black,design:.rounded))}.frame(maxWidth:.infinity)
 }
}
struct VictoryConfetti:View {
 @State private var fall=false
 var body:some View {
  GeometryReader {g in ForEach(0..<28){i in RoundedRectangle(cornerRadius:2).fill([Color.coral,Color(hex:"FFD494"),Color.white,Color.green][i%4]).frame(width:7,height:12).rotationEffect(.degrees(fall ? Double(i*47):0)).position(x:g.size.width*CGFloat((i*37)%100)/100,y:fall ? g.size.height+40:-40-CGFloat(i%6)*20).opacity(fall ? 0:1).animation(.easeIn(duration:2.2).delay(Double(i%7)*0.07),value:fall)}}.frame(height:500).onAppear{fall=true}.accessibilityHidden(true)
 }
}
