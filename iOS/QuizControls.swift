import SwiftUI

struct PowerState:Decodable {
 var used:Bool=false
 var type:String?=nil
 var hidden:[Int]=[]
 var highlight:Int?=nil
 func nextQuestion()->PowerState {PowerState(used:used)}
}
struct PowerReply:Decodable {let power:PowerState;let remaining:Double;let coins:Int;var duelAnswer:AnswerReply?=nil;var tournamentAnswer:TournamentRunReply?=nil}
struct MatchProgress:Decodable {let ownAnswered:Int;let opponentAnswered:Int;var opponentResults:[Bool?]?=nil}

struct QuestionTimeBar:View {
 let remaining:Double;let reading:Bool
 static func fraction(_ seconds:Double)->Double {seconds.isFinite ? max(0,min(1,seconds/10)):0}
 var body:some View {
  GeometryReader {g in
   ZStack(alignment:.leading) {
    Capsule().fill(.white.opacity(0.18))
    Capsule().fill(reading ? Color.white.opacity(0.4):(remaining<=3 ? Color.coral:(remaining<=5 ? Color(hex:"FFD494"):Color(hex:"64D9B0"))))
     .frame(width:g.size.width*CGFloat(reading ? 1:Self.fraction(remaining)))
   }
  }.frame(height:9)
   .accessibilityElement(children:.ignore).accessibilityLabel(reading ? "Reading time; answer clock has not started":"Answer time remaining")
   .accessibilityValue(reading ? "3-second preview":String(format:"%.1f seconds",remaining)).accessibilityIdentifier("answerTimeBar")
 }
}
enum QuizPower:String,CaseIterable {
 case fifty,double,right
 var title:String {switch self{case .fifty:return "Fifty Fifty";case .double:return "Double Choice";case .right:return "Right Answer"}}
 var symbol:String {switch self{case .fifty:return "50.circle";case .double:return "arrow.triangle.branch";case .right:return "checkmark.circle"}}
 var price:Int {switch self{case .fifty:return 5;case .double:return 10;case .right:return 25}}
 var detail:String {switch self{case .fifty:return "Removes two wrong options.";case .double:return "One extra choice after a wrong pick; the clock keeps running.";case .right:return "Selects and submits the correct answer for you."}}
}
struct PowerTray:View {
 let power:PowerState;let enabled:Bool;var practice=false;var allowed=true
 let action:(QuizPower)->Void
 var body:some View {
  VStack(spacing:5) {
   if allowed {
    HStack(spacing:7) {ForEach(QuizPower.allCases,id:\.rawValue){p in
     Button{action(p)}label:{VStack(spacing:3){Label(p.title,systemImage:p.symbol).font(.system(size:10,weight:.bold));HStack(spacing:3){if !practice{CoinSymbol(size:11)};Text(practice ? "Practice":"\(p.price) coins").font(.system(size:10,weight:.medium))}}.frame(maxWidth:.infinity).padding(.vertical,9).background(.white.opacity(0.13),in:RoundedRectangle(cornerRadius:9))}.disabled(!enabled || power.used).opacity(power.used ? 0.45:1).accessibilityLabel("\(p.title), \(practice ? "practice":String(p.price)+" coins"). \(p.detail)").accessibilityIdentifier("power-\(p.rawValue)")
    }}
    Text(power.used ? "Power-up used · one per run":"One power-up per run · clock keeps running").font(.system(size:9)).opacity(0.8)
   } else {Text("Host has switched power-ups off").font(.caption2).opacity(0.8)}
  }
 }
}
struct QuizAnswerTile:View {
 let text:String;let right:Bool;let wrong:Bool;let hidden:Bool;let highlighted:Bool
 let action:()->Void
 var body:some View {
  Button(action:action){
   VStack(spacing:6){Text(hidden && !wrong ? "":text).font(.system(size:19,weight:.semibold)).multilineTextAlignment(.center).lineLimit(6).minimumScaleFactor(0.6).frame(maxWidth:.infinity,maxHeight:.infinity);if right || highlighted{Image(systemName:"checkmark.circle.fill")}else if wrong{Image(systemName:"xmark.circle.fill")}}
    .foregroundStyle(right || wrong ? .white:Color.ink).padding(12).frame(maxWidth:.infinity,maxHeight:.infinity)
    .background(right ? Color(hex:"259D66"):(wrong ? Color.coral:.white.opacity(hidden ? 0.12:1)),in:RoundedRectangle(cornerRadius:7))
    .overlay{RoundedRectangle(cornerRadius:7).stroke(highlighted ? Color(hex:"FFD494"):.clear,lineWidth:4)}
  }.buttonStyle(AnswerButtonStyle()).disabled(hidden).accessibilityHidden(hidden && !wrong)
 }
}
struct DuelProgressView:View {
 let ownName:String;let opponent:String;let rounds:[PlayedRound];let opponentAnswered:Int;let recorded:Bool
 var opponentResults:[Bool?]=[]
 enum Outcome:String {case correct,incorrect,answered,upcoming}
 static func opponentOutcome(index:Int,answered:Int,results:[Bool?])->Outcome {
  if index<results.count,let right=results[index] {return right ? .correct:.incorrect}
  return index<answered ? .answered:.upcoming
 }
 var body:some View {
  VStack(spacing:5) {
   lane(ownName,count:rounds.count,own:true)
   lane(opponent+(recorded ? " · recorded":""),count:opponentAnswered,own:false)
  }.accessibilityIdentifier("duelProgress")
 }
 private func lane(_ name:String,count:Int,own:Bool)->some View {
  HStack(spacing:6){Text(name).font(.system(size:9,weight:.bold)).lineLimit(1).frame(width:95,alignment:.leading);ForEach(0..<7){i in
   let state=own ? (i<rounds.count ? (rounds[i].points>0 ? Outcome.correct:.incorrect):.upcoming):Self.opponentOutcome(index:i,answered:count,results:opponentResults)
   ZStack {
    Capsule().fill(state == .correct ? Color.green:(state == .incorrect ? Color.coral:.white.opacity(state == .answered ? 0.35:0.15)))
    if state == .correct || state == .incorrect {Image(systemName:state == .correct ? "checkmark":"xmark").font(.system(size:6,weight:.black))}
   }.frame(height:10)
    .accessibilityElement(children:.ignore).accessibilityLabel("Round \(i+1): \(state == .answered ? "answered; result pending":state.rawValue)")
    .accessibilityIdentifier("\(own ? "roundMarker":"opponentRoundMarker")-\(i)")
  };Text("\(min(7,count))/7").font(.system(size:9,weight:.bold)).monospacedDigit()}.accessibilityElement(children:.contain).accessibilityLabel("\(name), \(count) of seven questions answered. Saved progress.")
 }
}
