import Foundation
import CryptoKit

struct MobileQuestionBank: Decodable, Sendable {
    let format:Int
    let categories:[Topic]
    let questions:[Question]

    static func decode(_ data:Data) throws -> MobileQuestionBank {
        guard data.count<=50_000_000 else {throw CocoaError(.coderReadCorrupt)}
        let bank=try JSONDecoder().decode(Self.self,from:data)
        let ids=Set(bank.categories.map(\.id))
        guard (bank.format==1 || bank.format==2),!ids.isEmpty,ids.count==bank.categories.count,!ids.contains("mixed"),
              Set(bank.questions.map(\.id)).count==bank.questions.count else {throw CocoaError(.coderReadCorrupt)}
        var counts:[String:Int]=[:]
        for q in bank.questions {
            if q.imagePng != nil,QuestionImageData.decode(q.imagePng,sha:q.imageSHA256)==nil {throw CocoaError(.coderReadCorrupt)}
            guard !q.id.isEmpty,!q.prompt.trimmingCharacters(in:.whitespacesAndNewlines).isEmpty,
                  ids.contains(q.categoryID),q.answers.count==4,Set(q.answers).count==4,
                  q.answers.allSatisfy({!$0.trimmingCharacters(in:.whitespacesAndNewlines).isEmpty}),
                  (0..<4).contains(q.correctIndex) else {throw CocoaError(.coderReadCorrupt)}
            counts[q.categoryID,default:0]+=1
        }
        guard bank.categories.allSatisfy({!$0.name.isEmpty && $0.questionCount>=7 && counts[$0.id]==$0.questionCount}) else {throw CocoaError(.coderReadCorrupt)}
        return bank
    }
}

enum QuestionBankUpdates {
    struct Manifest:Decodable {let format:Int;let revision:String;let file:String;let bytes:Int;let questionCount:Int;let topicCount:Int}
    static func sha(_ data:Data)->String {SHA256.hash(data:data).map{String(format:"%02x",$0)}.joined()}
    static func directory(_ endpoint:String)throws->URL {
        guard let api=URL(string:endpoint),api.scheme=="https",api.host != nil else {throw CocoaError(.fileReadUnsupportedScheme)}
        return api.deletingLastPathComponent().appendingPathComponent("bank-v2",isDirectory:true)
    }
    static func cacheURL(_ endpoint:String)throws->URL {
        let root=try FileManager.default.url(for:.applicationSupportDirectory,in:.userDomainMask,appropriateFor:nil,create:true).appendingPathComponent("QuestionBanks",isDirectory:true)
        try FileManager.default.createDirectory(at:root,withIntermediateDirectories:true)
        return root.appendingPathComponent(sha(Data((endpoint+"|images-v2").utf8))+".json")
    }
    static func cached(_ endpoint:String)->MobileQuestionBank? {
        guard let url=try? cacheURL(endpoint),let data=try? Data(contentsOf:url) else {return nil}
        return try? MobileQuestionBank.decode(data)
    }
    static func fetch(_ endpoint:String)async throws->MobileQuestionBank? {
        let base=try directory(endpoint)
        var request=URLRequest(url:base.appendingPathComponent("manifest.json"),cachePolicy:.reloadIgnoringLocalCacheData,timeoutInterval:15)
        request.setValue("application/json",forHTTPHeaderField:"Accept")
        // These are public, data-only assets. Never attach a player token.
        let (metadata,response)=try await URLSession.shared.data(for:request)
        guard let http=response as? HTTPURLResponse,http.statusCode==200,http.url?.scheme=="https",http.url?.host==base.host,metadata.count<=65_536 else {throw CocoaError(.coderReadCorrupt)}
        let manifest=try JSONDecoder().decode(Manifest.self,from:metadata)
        guard (manifest.format==1 || manifest.format==2),manifest.revision.range(of:"^[a-f0-9]{64}$",options:.regularExpression) != nil,
              manifest.file=="bank-"+manifest.revision+".json",(1...50_000_000).contains(manifest.bytes) else {throw CocoaError(.coderReadCorrupt)}
        let cache=try cacheURL(endpoint)
        if let saved=try? Data(contentsOf:cache),sha(saved)==manifest.revision,(try? MobileQuestionBank.decode(saved)) != nil {return nil}
        request.url=base.appendingPathComponent(manifest.file)
        let (data,download)=try await URLSession.shared.data(for:request)
        guard let received=download as? HTTPURLResponse,received.statusCode==200,received.url?.scheme=="https",received.url?.host==base.host,
              data.count==manifest.bytes,sha(data)==manifest.revision else {throw CocoaError(.coderReadCorrupt)}
        let bank=try await Task.detached(priority:.utility){try MobileQuestionBank.decode(data)}.value
        guard bank.questions.count==manifest.questionCount,bank.categories.count==manifest.topicCount else {throw CocoaError(.coderReadCorrupt)}
        try data.write(to:cache,options:.atomic)
        var excluded=cache;var values=URLResourceValues();values.isExcludedFromBackup=true;try? excluded.setResourceValues(values)
        return bank
    }
}

extension QuizStore {
    func refreshQuestionBankIfNeeded() async {
        guard !isUITesting,!refreshingBank,Date().timeIntervalSince(lastBankCheck ?? .distantPast)>=900 else {return}
        refreshingBank=true;lastBankCheck=Date();defer{refreshingBank=false}
        let service=apiURL
        do {
            if let bank=try await QuestionBankUpdates.fetch(service),apiURL==service {
                questions=bank.questions;topics=bank.categories+[.mixed(count:bank.questions.count)];loadError=nil
            }
        } catch { /* An unavailable or invalid update leaves the last valid bank in use. */ }
    }
}
