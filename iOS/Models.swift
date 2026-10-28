import Foundation
import SwiftUI

struct Topic: Codable, Identifiable, Hashable {
    let id: String
    let name: String
    let symbol: String
    let color: String
    let emoji: String
    let questionCount: Int
    var tint: Color { Color(hex: color) }
}
struct Question: Codable, Identifiable {
    let id: String
    let categoryID: String
    let difficulty: String
    let prompt: String
    let answers: [String]
    let correctIndex: Int
    var source: String? = nil
    var sourceURL: String? = nil
    func shuffled() -> Question {
        let indices = Array(answers.indices).shuffled()
        return Question(id:id, categoryID:categoryID, difficulty:difficulty, prompt:prompt,
                        answers:indices.map { answers[$0] }, correctIndex:indices.firstIndex(of:correctIndex)!,source:source,sourceURL:sourceURL)
    }
}
struct PlayedRound: Codable, Identifiable {
    var id: String { question.id }
    let question: Question
    let selected: Int
    let elapsed: Double
    let points: Int
    let opponentPoints: Int
}
struct MatchRecord: Codable, Identifiable {
    let id: String
    let topicID: String
    let date: Date
    let score: Int
    let opponentScore: Int
    let opponent: String
    let kind: String
    let rounds: [PlayedRound]
    var duelID:String? = nil
    var pending:Bool? = nil
    var opponentID:String? = nil
    var won: Bool { pending != true && score > opponentScore }
    var tied: Bool { pending != true && score == opponentScore }
    var xp: Int { pending == true ? 0:Scoring.experience(score:score,opponentScore:opponentScore) }
}
enum Scoring {
    static func experience(score:Int,opponentScore:Int)->Int {score+40+(score>opponentScore ? 100:(score==opponentScore ? 50:0))}
    static func points(correct: Bool, elapsed: Double, round: Int) -> Int {
        guard correct, elapsed >= 0, elapsed < 10, elapsed.isFinite else { return 0 }
        return (20 - Int(floor(elapsed))) * (round == 6 ? 2 : 1)
    }
}
extension Color {
    init(hex: String) {
        let n = UInt64(hex, radix:16) ?? 0
        self.init(red:Double((n >> 16) & 255)/255,green:Double((n >> 8) & 255)/255,blue:Double(n & 255)/255)
    }
    static let ink = Color(hex:"243449")
    static let canvas = Color(hex:"F7F6F2")
    static let coral = Color(hex:"E96959")
}
