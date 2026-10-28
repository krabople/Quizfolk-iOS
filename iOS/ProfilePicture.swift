import SwiftUI
import UIKit
import ImageIO

struct PlayerPortrait:View {
    let name:String
    var avatar:String? = nil
    var bot=false
    var size:CGFloat=68
    var badge:TournamentPrize?=nil
    var body:some View {
        Group {
            if let avatar,let data=Data(base64Encoded:avatar),let image=UIImage(data:data) {Image(uiImage:image).resizable().scaledToFill()}
            else {ZStack{Circle().fill(Color.coral);Image(systemName:bot ? "cpu.fill":"person.fill").font(.system(size:size*0.42,weight:.bold)).foregroundStyle(.white)}}
        }.frame(width:size,height:size).clipShape(Circle()).overlay(Circle().stroke(.white.opacity(0.8),lineWidth:3))
            .overlay(alignment:.bottomTrailing){if let badge {TournamentMedal(prize:badge,size:max(22,size*0.32)).offset(x:3,y:3)}}
            .accessibilityLabel("\(name) profile picture\(badge.map{", tournament \($0.placing) badge"} ?? "")")
    }
}
enum ProfilePicture {
    static func make(_ data:Data)throws->Data {
        guard data.count<=30_000_000,
              let source=CGImageSourceCreateWithData(data as CFData,nil),
              let thumbnail=CGImageSourceCreateThumbnailAtIndex(source,0,[kCGImageSourceCreateThumbnailFromImageAlways:true,kCGImageSourceCreateThumbnailWithTransform:true,kCGImageSourceThumbnailMaxPixelSize:512] as CFDictionary)
        else {throw APIError.message("This photo could not be opened. Try another picture.")}
        let image=UIImage(cgImage:thumbnail)
        let format=UIGraphicsImageRendererFormat();format.scale=1;format.opaque=true
        let output=UIGraphicsImageRenderer(size:CGSize(width:128,height:128),format:format).image{context in
            UIColor.white.setFill();context.fill(CGRect(x:0,y:0,width:128,height:128))
            let scale=max(128/image.size.width,128/image.size.height)
            let w=image.size.width*scale,h=image.size.height*scale
            image.draw(in:CGRect(x:(128-w)/2,y:(128-h)/2,width:w,height:h))
        }
        guard let jpeg=output.jpegData(compressionQuality:0.75),jpeg.count<=16384 else {throw APIError.message("This picture is too detailed. Try another photo.")}
        return jpeg
    }
}
