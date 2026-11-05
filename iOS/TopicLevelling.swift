import Foundation

struct TopicLevelState:Equatable {
    let level:Int
    let xpIntoLevel:Int
    let xpForNextLevel:Int
    var remainingXP:Int {xpForNextLevel-xpIntoLevel}
}
struct TopicLevelUp:Equatable {
    let previousLevel:Int
    let progress:TopicLevelState
}
enum TopicLevelling {
    // Level L starts at 250 * (L-1) * (L+4) total topic XP.
    static func progress(xp:Int)->TopicLevelState {
        let xp=max(0,xp)
        var lower=0,upper=xp/1500+1
        while lower<upper {
            let middle=lower+(upper-lower+1)/2
            if middle <= (xp/250)/(middle+5) {lower=middle} else {upper=middle-1}
        }
        return TopicLevelState(level:lower+1,xpIntoLevel:xp-250*lower*(lower+5),xpForNextLevel:1500+500*lower)
    }
    static func levelUp(beforeXP:Int,afterXP:Int)->TopicLevelUp? {
        let before=progress(xp:beforeXP),after=progress(xp:afterXP)
        return after.level>before.level ? TopicLevelUp(previousLevel:before.level,progress:after):nil
    }
}
