import Foundation

enum QuestionReadingTime {
    static func seconds(for prompt:String)->Double {
        let words=prompt.split(whereSeparator: { $0.isWhitespace })
        let characters=words.joined(separator:" ").unicodeScalars.count
        return 3+ceil(max(0,Double(words.count-12)/3,Double(characters-72)/18))
    }
}
