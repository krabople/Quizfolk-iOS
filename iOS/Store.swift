import Foundation
import SwiftUI
import Security

@MainActor final class QuizStore: ObservableObject {
    @Published var topics: [Topic] = []
    @Published var questions: [Question] = []
    @Published var favourites: Set<String> = []
    @Published var history: [MatchRecord] = []
    @Published var name = "Quiz explorer"
    @Published var apiURL = ""
    @Published var loadError: String?
    @Published var onlineError: String?
    @Published var profile: OnlineProfile?
    @Published var board: [BoardEntry] = []
    private var token: String?
    init() {
        do {
            topics = try Self.resource("categories")
            questions = try Self.resource("questions")
        } catch { loadError = "The question bank could not be loaded: \(error.localizedDescription)" }
        favourites = Set(UserDefaults.standard.stringArray(forKey:"favourites") ?? [])
        name = UserDefaults.standard.string(forKey:"name") ?? "Quiz explorer"
        apiURL = UserDefaults.standard.string(forKey:"apiURL") ?? ""
        if let data = UserDefaults.standard.data(forKey:"history"), let saved = try? JSONDecoder().decode([MatchRecord].self,from:data) { history=saved }
        token = Keychain.read()
    }
    static func resource<T:Decodable>(_ name:String) throws -> T {
        guard let url=Bundle.main.url(forResource:name,withExtension:"json") else { throw CocoaError(.fileNoSuchFile) }
        return try JSONDecoder().decode(T.self,from:Data(contentsOf:url))
    }
    func toggle(_ topic:Topic) {
        if favourites.contains(topic.id) { favourites.remove(topic.id) } else { favourites.insert(topic.id) }
        UserDefaults.standard.set(Array(favourites),forKey:"favourites")
    }
    func saveSettings() {
        name=String(name.trimmingCharacters(in:.whitespacesAndNewlines).prefix(24))
        if name.isEmpty { name="Quiz explorer" }
        UserDefaults.standard.set(name,forKey:"name")
        UserDefaults.standard.set(apiURL,forKey:"apiURL")
    }
    func packet(_ topic:Topic) -> [Question] {
        let seen=Set(history.filter{$0.topicID==topic.id}.flatMap{$0.rounds.map{$0.question.id}})
        let bank=questions.filter{$0.categoryID==topic.id}
        let fresh=bank.filter{!seen.contains($0.id)}.shuffled()
        let extra=bank.filter{seen.contains($0.id)}.shuffled()
        return Array((fresh+extra).prefix(7)).map{$0.shuffled()}
    }
    func save(_ match:MatchRecord) {
        guard !history.contains(where:{$0.id==match.id}) else {return}
        history.insert(match,at:0)
        if let data=try? JSONEncoder().encode(history) { UserDefaults.standard.set(data,forKey:"history") }
    }
    var xp:Int { history.reduce(0){$0+$1.score} }
    func level(_ topic:Topic)->Int { 1+history.filter{$0.topicID==topic.id}.reduce(0){$0+$1.score}/300 }
    func request<T:Decodable>(_ route:String,body:[String:Any]?=nil,query:[URLQueryItem]=[]) async throws -> T {
        guard var parts=URLComponents(string:apiURL),parts.scheme=="https",parts.host != nil else {throw APIError.message("Enter the deployed HTTPS API URL in your profile first.")}
        parts.queryItems=(parts.queryItems ?? [])+[URLQueryItem(name:"r",value:route)]+query
        guard let url=parts.url else {throw APIError.message("Invalid API URL")}
        var req=URLRequest(url:url);req.timeoutInterval=20
        if let token {req.setValue("Bearer \(token)",forHTTPHeaderField:"Authorization")}
        if let body {req.httpMethod="POST";req.setValue("application/json",forHTTPHeaderField:"Content-Type");req.httpBody=try JSONSerialization.data(withJSONObject:body)}
        let (data,response)=try await URLSession.shared.data(for:req)
        guard let http=response as? HTTPURLResponse,(200..<300).contains(http.statusCode) else {
            let failure=try? JSONDecoder().decode(Failure.self,from:data)
            throw APIError.message(failure?.error ?? "Server request failed. Please try again.")
        }
        return try JSONDecoder().decode(T.self,from:data)
    }
    func connect() async {
        saveSettings();onlineError=nil
        do {
            if token==nil {
                let auth:AuthReply=try await request("register",body:["name":name])
                guard Keychain.save(auth.token) else {throw APIError.message("Could not securely save your account key.")}
                token=auth.token
            }
            profile=try await request("profile")
        } catch {onlineError=error.localizedDescription}
    }
    func loadBoard(topicID:String?=nil,weekly:Bool=true) async {
        onlineError=nil
        do { let response:BoardReply=try await request("leaderboard",query:[URLQueryItem(name:"topic",value:topicID ?? ""),URLQueryItem(name:"period",value:weekly ? "week":"all")])
            board=response.entries
        } catch {onlineError=error.localizedDescription}
    }
}
enum APIError: LocalizedError {
    case message(String)
    var errorDescription:String? {if case .message(let s)=self{return s};return nil}
}
struct Failure:Decodable {let error:String}
struct AuthReply:Decodable {let token:String}
struct OnlineProfile:Decodable {let name:String;let matches:Int;let wins:Int;let xp:Int;let correct:Int;let answered:Int}
struct BoardEntry:Decodable,Identifiable {let id:String;let name:String;let xp:Int;let matches:Int}
struct BoardReply:Decodable {let entries:[BoardEntry]}
enum Keychain {
    static let service="com.quizfolk.player"
    static func read()->String? {
        let q:[String:Any]=[kSecClass as String:kSecClassGenericPassword,kSecAttrService as String:service,kSecAttrAccount as String:"token",kSecReturnData as String:true,kSecMatchLimit as String:kSecMatchLimitOne]
        var item:CFTypeRef?
        guard SecItemCopyMatching(q as CFDictionary,&item)==errSecSuccess,let data=item as? Data else {return nil}
        return String(data:data,encoding:.utf8)
    }
    static func save(_ token:String)->Bool {
        let q:[String:Any]=[kSecClass as String:kSecClassGenericPassword,kSecAttrService as String:service,kSecAttrAccount as String:"token"]
        let attrs:[String:Any]=[kSecValueData as String:Data(token.utf8),kSecAttrAccessible as String:kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly]
        let status=SecItemUpdate(q as CFDictionary,attrs as CFDictionary)
        if status==errSecItemNotFound {return SecItemAdd(q.merging(attrs){_,new in new} as CFDictionary,nil)==errSecSuccess}
        return status==errSecSuccess
    }
}
