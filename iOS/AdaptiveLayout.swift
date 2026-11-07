import SwiftUI

/// The window stays native and fills the display; only long-form content has a readable width.
/// Uses the proposed window width, so Split View and Stage Manager resize naturally.
struct QuizPageScroll<Content:View>:View {
    var maxWidth:CGFloat=1040
    var spacing:CGFloat=8
    @ViewBuilder var content:()->Content
    var body:some View {
        ScrollView {
            VStack(spacing:spacing,content:content)
                .frame(maxWidth:maxWidth)
                .frame(maxWidth:.infinity)
        }
    }
}

enum QuizLayout {
    static func topicColumns(regular:Bool)->[GridItem] {
        regular ? [GridItem(.adaptive(minimum:200),spacing:12)] :
            [GridItem(.flexible(),spacing:12),GridItem(.flexible(),spacing:12)]
    }
}

/// Keeps modal actions reachable in landscape and small iPad windows.
struct QuizPopupCard<Content:View>:View {
    @ViewBuilder var content:()->Content
    var body:some View {
        GeometryReader { geometry in
            ScrollView {
                VStack(spacing:20,content:content)
                    .padding(28)
                    .frame(maxWidth:540)
                    .background(Color.canvas,in:RoundedRectangle(cornerRadius:28))
                    .padding(22)
                    .frame(maxWidth:.infinity)
                    .frame(minHeight:geometry.size.height)
            }
        }
    }
}
