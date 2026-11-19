import SwiftUI

struct AchievementList:View {
 let badges:[PlayerBadge]
 @State private var filter="All"
 @State private var selected:PlayerBadge?
 private var visible:[PlayerBadge] {badges.filter{filter=="All" || (filter=="Unlocked" ? $0.earned:!$0.earned)}}
 private var groups:[String] {var seen=Set<String>();return visible.compactMap{seen.insert($0.groupName).inserted ? $0.groupName:nil}}
 var body:some View {
  VStack(alignment:.leading,spacing:15) {
   Text("Achievements").font(.title3.bold())
   Text("\(badges.filter(\.earned).count) of \(badges.count) unlocked").font(.subheadline).foregroundStyle(.secondary)
   Text("Milestones to work towards, and your best public tournament finish in each topic. Tap any achievement to see its requirement and progress.").font(.caption).foregroundStyle(.secondary)
   Picker("Show achievements",selection:$filter){ForEach(["All","Unlocked","Locked"],id:\.self){Text($0).tag($0)}}.pickerStyle(.segmented).accessibilityIdentifier("achievementFilter")
   if visible.isEmpty {Text(filter=="Locked" ? "Every available achievement has been unlocked.":"No achievements in this section yet.").font(.subheadline).foregroundStyle(.secondary)}
   ForEach(groups,id:\.self){group in
    Text(group).font(.headline).padding(.top,7)
    ForEach(visible.filter{$0.groupName==group}){badge in
     Button{selected=badge}label:{AchievementRow(badge:badge)}.buttonStyle(.plain)
      .accessibilityIdentifier("achievement-\(badge.id)").accessibilityHint("View requirement and progress")
    }
   }
  }.padding(18).background(.white,in:RoundedRectangle(cornerRadius:18))
   .sheet(item:$selected){AchievementDetail(badge:$0)}
 }
}
struct AchievementEmblem:View {
 let badge:PlayerBadge
 var body:some View {
  if let topic=badge.topicID,let rank=badge.rank {TournamentBadgeEmblem(topicID:topic,kind:badge.kind ?? "daily",rank:rank,size:44)}
  else {Image(systemName:badge.symbol).font(.system(size:21,weight:.semibold)).foregroundStyle(badge.earned ? Color.coral:.gray).frame(width:44,height:44).background((badge.earned ? Color.coral:Color.gray).opacity(0.12),in:RoundedRectangle(cornerRadius:12))}
 }
}
struct AchievementRow:View {
 let badge:PlayerBadge
 var body:some View {
  HStack(spacing:13) {
   AchievementEmblem(badge:badge)
   VStack(alignment:.leading,spacing:5) {
    Text(badge.name).font(.subheadline.bold())
    Text(badge.requirementText).font(.caption).foregroundStyle(.secondary).lineLimit(2)
    if let progress=badge.progressLabel {Text(progress).font(.caption.monospacedDigit()).foregroundStyle(.secondary)}
    if let fraction=badge.progressFraction {ProgressView(value:fraction).tint(badge.earned ? .green:.coral)}
   }
   Spacer(minLength:0)
   VStack(spacing:7){Text(badge.earned ? "Unlocked":"Locked").font(.caption2);Image(systemName:"info.circle")}.foregroundStyle(.secondary)
  }.foregroundStyle(Color.ink).padding(.vertical,7).contentShape(Rectangle())
 }
}
struct AchievementDetail:View {
 let badge:PlayerBadge
 @Environment(\.dismiss) private var dismiss
 var body:some View {
  NavigationStack {
   ScrollView {
    VStack(alignment:.leading,spacing:22) {
     HStack(spacing:16){AchievementEmblem(badge:badge);VStack(alignment:.leading,spacing:5){Text(badge.name).font(.title2.bold());Text(badge.earned ? "Unlocked":"Not unlocked yet").font(.subheadline).foregroundStyle(badge.earned ? Color.green:Color.secondary).accessibilityIdentifier("achievementStatus")}}
     Text("How to unlock").font(.headline)
     Text(badge.requirementText).accessibilityIdentifier("achievementRequirement")
     if let progress=badge.progressLabel {
      Text("Progress").font(.headline)
      Text(progress).monospacedDigit().accessibilityIdentifier("achievementProgress")
      if let fraction=badge.progressFraction {ProgressView(value:fraction).tint(.coral)}
     }
    }.padding(24).frame(maxWidth:650,alignment:.leading).frame(maxWidth:.infinity)
   }.background(Color.canvas).navigationTitle("Achievement").navigationBarTitleDisplayMode(.inline)
    .toolbar{ToolbarItem(placement:.topBarTrailing){Button("Done"){dismiss()}}}
  }
 }
}
