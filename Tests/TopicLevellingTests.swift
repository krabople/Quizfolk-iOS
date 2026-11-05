import XCTest
import SwiftUI
@testable import Quizfolk

final class TopicLevellingTests:XCTestCase {
    func testProgressiveBoundariesAndFourPerfectWins() {
        let starts=[0,1500,3500,6000,9000,12500,16500,21000,26000,31500]
        for (index,xp) in starts.enumerated() {
            let p=TopicLevelling.progress(xp:xp)
            XCTAssertEqual(p.level,index+1);XCTAssertEqual(p.xpIntoLevel,0)
            XCTAssertEqual(p.xpForNextLevel,1500+index*500)
            if xp>0 {let before=TopicLevelling.progress(xp:xp-1);XCTAssertEqual(before.level,index);XCTAssertEqual(before.remainingXP,1)}
        }
        XCTAssertEqual(TopicLevelling.progress(xp:4*Scoring.experience(score:160,opponentScore:100)),TopicLevelState(level:1,xpIntoLevel:1200,xpForNextLevel:1500))
        XCTAssertEqual(TopicLevelling.progress(xp:-100).level,1)
        XCTAssertGreaterThan(TopicLevelling.progress(xp:Int.max).remainingXP,0)
    }
    func testAnnouncementsRequireAnUpwardBoundaryCrossing() {
        XCTAssertNil(TopicLevelling.levelUp(beforeXP:700,afterXP:1000))
        XCTAssertNil(TopicLevelling.levelUp(beforeXP:1600,afterXP:1600))
        XCTAssertNil(TopicLevelling.levelUp(beforeXP:1600,afterXP:1000))
        let up=TopicLevelling.levelUp(beforeXP:1499,afterXP:1700)!
        XCTAssertEqual(up.previousLevel,1);XCTAssertEqual(up.progress.level,2);XCTAssertEqual(up.progress.remainingXP,1800)
    }
    @MainActor func testCompletedMatchCelebratesOnceButPendingPracticeAndHistoryDoNot() async {
        let store=QuizStore();await store.connect();let topic=store.topics.first{$0.id=="22"}!
        store.ownCard=QuizStore.testCard(following:false,own:true,topicXP:1400)
        let game=GameSession(topic:topic,store:store,online:true);defer{game.stop()}
        game.finished=true;game.score=160;game.opponentScore=100
        game.rounds=store.packet(topic).map{PlayedRound(question:$0,selected:0,elapsed:0,points:20,opponentPoints:0)}
        game.awaitingOpponent=true;store.ownCard=QuizStore.testCard(following:false,own:true,topicXP:1700)
        game.updateLevelUp();XCTAssertNil(game.levelUp)
        game.awaitingOpponent=false;game.updateLevelUp();XCTAssertEqual(game.levelUp?.progress.level,2)
        let original=game.levelUp
        store.ownCard=QuizStore.testCard(following:false,own:true,topicXP:3600)
        game.updateLevelUp();XCTAssertEqual(game.levelUp,original)
        let record=MatchRecord(id:"done",topicID:topic.id,date:Date(),score:160,opponentScore:100,opponent:"Bot",kind:"bot",rounds:game.rounds)
        let replay=GameSession(topic:topic,store:store,record:record);defer{replay.stop()}
        store.ownCard=QuizStore.testCard(following:false,own:true,topicXP:3900)
        replay.updateLevelUp();XCTAssertNil(replay.levelUp)
        let practice=GameSession(topic:topic,store:store,online:false);defer{practice.stop()}
        practice.finished=true;practice.updateLevelUp();XCTAssertNil(practice.levelUp)
    }
    @MainActor func testLevelUpCardSnapshot() {
        let topic=QuizStore().topics.first{$0.id=="22"}!
        let view=TopicLevelCelebration(topic:topic,advancement:TopicLevelling.levelUp(beforeXP:1400,afterXP:1700)!).padding(20).background(Color(hex:"173E59")).preferredColorScheme(.dark)
        let image=ImageRenderer(content:view.frame(width:390)).uiImage!
        let attachment=XCTAttachment(image:image);attachment.name="TopicLevelUp";attachment.lifetime = .keepAlways;add(attachment)
        XCTAssertGreaterThan(image.size.height,250)
    }
}
