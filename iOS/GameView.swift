import SwiftUI

struct GameView:View {
    @ObservedObject var game:GameSession
    @EnvironmentObject var store:QuizStore
    @Environment(\.dismiss) var dismiss
    @Environment(\.scenePhase) var phase
    @State private var leave=false
    var body:some View {
        NavigationStack {
            Group {
                if game.finished {result}
                else {play}
            }.background(Color.canvas).foregroundStyle(Color.ink)
            .toolbar {ToolbarItem(placement:.topBarLeading){Button{leave=true}label:{Image(systemName:"xmark")}.accessibilityLabel("Leave match")};ToolbarItem(placement:.principal){Text(game.topic.name).font(.headline)}}
            .confirmationDialog("Leave this duel? An unfinished duel earns no XP.",isPresented:$leave,titleVisibility:.visible){Button("Leave duel",role:.destructive){game.stop();dismiss()}}
        }.task{await game.begin()}.onDisappear{game.stop()}
        .onChange(of:phase){_,new in if new == .active && !game.revealed && game.current != nil { /* ContinuousClock includes time away; the timer enforces expiry on resume. */ }}
    }
    private var play:some View {
        ScrollView {
            VStack(spacing:20) {
                HStack(alignment:.top) {
                    player(store.name,score:game.score,icon:"person.fill",color:game.topic.tint)
                    VStack(spacing:7){Text("VS").font(.system(size:14,weight:.black));Text(game.online && game.kind=="human" ? "RECORDED RUN":"BOT DUEL").font(.system(size:8,weight:.bold)).tracking(1)}.foregroundStyle(.secondary).padding(.top,18)
                    player(game.opponent,score:game.opponentScore,icon:game.kind=="human" ? "person.fill":"cpu.fill",color:.coral)
                }
                HStack(spacing:7){ForEach(0..<7){i in Capsule().fill(i<game.round ? game.topic.tint:(i==game.round ? Color.coral:Color.gray.opacity(0.15))).frame(height:5)}}
                HStack{Text(game.round==6 ? "FINAL ROUND · DOUBLE POINTS":"ROUND \(game.round+1) OF 7").font(.system(size:11,weight:.heavy)).tracking(1);Spacer();Label(String(format:"%.1fs",game.remaining),systemImage:"timer").font(.system(.subheadline,design:.monospaced)).foregroundStyle(game.remaining<3 ? Color.coral:Color.ink)}
                if let q=game.current {
                    Text(q.difficulty.uppercased()).font(.system(size:10,weight:.bold)).tracking(2).foregroundStyle(game.topic.tint)
                    Text(q.prompt).font(.system(size:25,weight:.bold,design:.rounded)).multilineTextAlignment(.center).frame(maxWidth:.infinity,minHeight:145)
                    VStack(spacing:10) {ForEach(q.answers.indices,id:\.self){i in answer(q,index:i)}}
                    if game.revealed {
                        Text(game.lastPoints>0 ? "+\(game.lastPoints) points · Nicely done!":(game.selected == -1 ? "Time’s up. You’ve got the next one.":"One to remember for next time.")).font(.headline).foregroundStyle(game.lastPoints>0 ? game.topic.tint:Color.coral).multilineTextAlignment(.center)
                        Button(game.round==6 ? "See results":"Next question"){Task{await game.next()}}.buttonStyle(PrimaryButton(color:game.topic.tint)).accessibilityIdentifier("advanceQuestion")
                    }
                } else if game.busy {ProgressView("Finding your duel…").padding(70)}
                if let error=game.error {Text(error).font(.subheadline).foregroundStyle(.red);Button("Try again"){Task{await game.retry()}}.buttonStyle(.bordered)}
                if game.busy && game.current != nil {ProgressView()}
                Text("\(game.current?.source ?? "Open trivia contributors") · CC BY-SA 4.0").font(.system(size:9)).foregroundStyle(.secondary)
            }.padding(22)
        }
    }
    private func player(_ name:String,score:Int,icon:String,color:Color)->some View {
        VStack(spacing:9){Image(systemName:icon).font(.title2).foregroundStyle(color).frame(width:56,height:56).background(color.opacity(0.12),in:Circle());Text(name).font(.system(size:12,weight:.semibold)).lineLimit(2).multilineTextAlignment(.center);Text("\(score)").font(.system(size:30,weight:.bold,design:.rounded))}.frame(maxWidth:.infinity)
    }
    private func answer(_ q:Question,index:Int)->some View {
        let correct=game.revealed && index==q.correctIndex
        let wrong=game.revealed && game.selected==index && !correct
        return Button{Task{await game.answer(index)}}label:{
            HStack(spacing:12){Text(String(UnicodeScalar(65+index)!)).font(.system(size:12,weight:.bold)).frame(width:28,height:28).background(Color.ink.opacity(0.06),in:Circle());Text(q.answers[index]).font(.system(size:16,weight:.semibold)).multilineTextAlignment(.leading);Spacer();if correct {Image(systemName:"checkmark.circle.fill").foregroundStyle(.green)} else if wrong {Image(systemName:"xmark.circle.fill").foregroundStyle(.red)}}.foregroundStyle(Color.ink).padding(16).frame(maxWidth:.infinity,minHeight:66).background(correct ? Color.green.opacity(0.12):(wrong ? Color.red.opacity(0.1):.white),in:RoundedRectangle(cornerRadius:14)).overlay{RoundedRectangle(cornerRadius:14).stroke(correct ? Color.green:(wrong ? Color.red:.clear),lineWidth:2)}
        }.buttonStyle(.plain).disabled(game.revealed || game.busy || game.error != nil).accessibilityIdentifier("answer-\(index)")
    }
    private var result:some View {
        ScrollView {
            VStack(spacing:19) {
                Image(systemName:game.score>game.opponentScore ? "trophy.fill":"sparkles").font(.system(size:65)).foregroundStyle(Color(hex:"D9A03B")).padding(.top,25)
                Text(game.score>game.opponentScore ? "That’s your win!":(game.score==game.opponentScore ? "Perfectly matched.":"A worthy rivalry.")).font(.system(size:30,weight:.bold,design:.rounded)).multilineTextAlignment(.center)
                Text("\(game.score) – \(game.opponentScore)").font(.system(size:44,weight:.heavy,design:.rounded)).foregroundStyle(game.topic.tint)
                Text("vs \(game.opponent) · \(game.kind=="human" ? "Recorded human run":"Bot")").font(.subheadline).foregroundStyle(.secondary)
                Text("+\(game.score) XP in \(game.topic.name)").font(.headline)
                HStack{Label("\(game.rounds.filter{$0.selected==$0.question.correctIndex}.count)/7 correct",systemImage:"checkmark.circle");Spacer();Text("Max 160")}.font(.caption)
                ForEach(Array(game.rounds.enumerated()),id:\.element.id){index,r in
                    VStack(alignment:.leading,spacing:7){HStack{Text("QUESTION \(index+1)").font(.system(size:9,weight:.heavy)).foregroundStyle(.secondary);Spacer();Text("+\(r.points)").bold().foregroundStyle(game.topic.tint)};Text(r.question.prompt).font(.subheadline).bold();Text("Answer: \(r.question.answers[r.question.correctIndex])").font(.caption).foregroundStyle(.secondary)}.padding(16).frame(maxWidth:.infinity,alignment:.leading).background(.white,in:RoundedRectangle(cornerRadius:14))
                }
                Button("Back to topics"){dismiss()}.buttonStyle(PrimaryButton(color:game.topic.tint))
            }.padding(22)
        }
    }
}
