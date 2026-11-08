import XCTest
import GoogleMobileAds
@testable import Quizfolk

final class RewardedAdFailureTests:XCTestCase {
    func testConnectionAndTimeoutFailuresAreNotPresentedAsNoFill() {
        let network=AdLoadFailure(NSError(domain:GADErrorDomain,code:RequestError.Code.networkError.rawValue))
        let timeout=AdLoadFailure(NSError(domain:GADErrorDomain,code:RequestError.Code.timeout.rawValue))
        let noFill=AdLoadFailure(NSError(domain:GADErrorDomain,code:RequestError.Code.noFill.rawValue))
        XCTAssertEqual(network.kind,.network);XCTAssertEqual(timeout.kind,.timeout);XCTAssertEqual(noFill.kind,.noFill)
        XCTAssertNotEqual(network.errorDescription,noFill.errorDescription)
        XCTAssertNotEqual(timeout.errorDescription,noFill.errorDescription)
        XCTAssertEqual(AdLoadFailure(URLError(.notConnectedToInternet)).kind,.network)
        XCTAssertEqual(AdLoadFailure(URLError(.timedOut)).kind,.timeout)
    }
    func testSameNumericCodeFromAnotherDomainDoesNotInventNoFill() {
        let failure=AdLoadFailure(NSError(domain:"another.provider",code:RequestError.Code.noFill.rawValue))
        XCTAssertEqual(failure.kind,.unknown)
        XCTAssertEqual(AdLoadFailure(NSError(domain:GADErrorDomain,code:999)).kind,.unknown)
        XCTAssertEqual(AdLoadFailure(NSError(domain:GADErrorDomain,code:RequestError.Code.invalidRequest.rawValue)).kind,.request)
        XCTAssertEqual(AdLoadFailure(NSError(domain:GADErrorDomain,code:RequestError.Code.serverError.rawValue)).kind,.server)
    }
    func testCopyDetailsPreservesSDKFieldsWithoutDumpingOtherUserInfo() {
        let error=NSError(domain:GADErrorDomain,code:RequestError.Code.invalidRequest.rawValue,userInfo:[
            NSLocalizedDescriptionKey:"Invalid ad request",
            NSLocalizedFailureReasonErrorKey:"Account not approved yet",
            "authorization":"do-not-copy-this-token",
            NSUnderlyingErrorKey:NSError(domain:"private",code:5,userInfo:[NSLocalizedDescriptionKey:"do-not-copy-this-account"])
        ])
        let failure=AdLoadFailure(error,responseIdentifier:"google-response-example")
        XCTAssertEqual(failure.domain,error.domain);XCTAssertEqual(failure.code,error.code)
        XCTAssertEqual(failure.sdkMessage,error.localizedDescription)
        XCTAssertEqual(failure.sdkFailureReason,"Account not approved yet")
        XCTAssertEqual(failure.responseIdentifier,"google-response-example")
        XCTAssertTrue(failure.diagnosticText.contains("SDK message: Invalid ad request"))
        XCTAssertTrue(failure.diagnosticText.contains("SDK reason: Account not approved yet"))
        XCTAssertTrue(failure.diagnosticText.contains("Response ID: google-response-example"))
        XCTAssertFalse(failure.diagnosticText.contains("do-not-copy"))
    }
}
