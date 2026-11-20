import SwiftUI
import UIKit
import CryptoKit

enum QuestionImageData {
    static func decode(_ encoded:String?,sha:String?)->Data? {
        guard let encoded,encoded.utf8.count<=90_000,let data=Data(base64Encoded:encoded),data.count<=65_536,data.count>=24,
              Array(data.prefix(8)) == [137,80,78,71,13,10,26,10],
              let sha,SHA256.hash(data:data).map({String(format:"%02x",$0)}).joined()==sha else{return nil}
        let bytes=Array(data.prefix(24))
        let width=bytes[16..<20].reduce(UInt32(0)){($0<<8)|UInt32($1)}
        let height=bytes[20..<24].reduce(UInt32(0)){($0<<8)|UInt32($1)}
        guard (1...512).contains(width),(1...512).contains(height) else{return nil}
        return data
    }
    private static let cache=NSCache<NSString,UIImage>()
    static func image(_ encoded:String?,sha:String?)->UIImage? {
        guard let sha else{return nil}
        if let cached=cache.object(forKey:sha as NSString){return cached}
        guard let data=decode(encoded,sha:sha),let image=UIImage(data:data) else{return nil}
        cache.setObject(image,forKey:sha as NSString);return image
    }
}

struct QuestionPicture:View {
    let png:String?;let sha:String?
    var body:some View {
        if let image=QuestionImageData.image(png,sha:sha) {
            Image(uiImage:image).resizable().interpolation(.high).scaledToFit().padding(10)
                .frame(maxWidth:.infinity,maxHeight:.infinity).background(.white,in:RoundedRectangle(cornerRadius:12))
                .overlay(RoundedRectangle(cornerRadius:12).stroke(Color.gray.opacity(0.25)))
                .accessibilityLabel("Question image").accessibilityIdentifier("questionImage")
        }
    }
}

struct QuizQuestionContent:View {
    let prompt:String;let png:String?;let sha:String?;var fontSize:CGFloat=25;var identifier="quizQuestion"
    var body:some View {
        if png != nil {
            VStack(spacing:10) {
                Text(prompt).font(.system(size:min(fontSize,22),weight:.bold,design:.rounded)).multilineTextAlignment(.center)
                    .lineLimit(4).minimumScaleFactor(0.7).accessibilityIdentifier(identifier)
                QuestionPicture(png:png,sha:sha)
            }.frame(maxWidth:.infinity,maxHeight:.infinity)
        } else {
            Text(prompt).font(.system(size:fontSize,weight:.bold,design:.rounded)).multilineTextAlignment(.center)
                .lineLimit(fontSize>30 ? 10:7).minimumScaleFactor(0.6).frame(maxWidth:.infinity,maxHeight:.infinity).accessibilityIdentifier(identifier)
        }
    }
}
