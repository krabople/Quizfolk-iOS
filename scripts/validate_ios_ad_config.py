"""Fail release CI before signing if its AdMob configuration is missing or test-only."""
import os
import re

app_id = os.environ.get("QUIZFOLK_ADMOB_IOS_APP_ID", "")
unit_id = os.environ.get("QUIZFOLK_ADMOB_IOS_REWARDED_UNIT_ID", "")
if not re.fullmatch(r"ca-app-pub-[0-9]{16}~[0-9]{10}", app_id):
    raise SystemExit("Configure the production iOS AdMob app ID repository variable.")
if not re.fullmatch(r"ca-app-pub-[0-9]{16}/[0-9]{10}", unit_id):
    raise SystemExit("Configure the production iOS rewarded ad unit repository variable.")
if "3940256099942544" in app_id + unit_id:
    raise SystemExit("Google sample ad IDs are debug-only.")
if app_id.split("~")[0] != unit_id.split("/")[0]:
    raise SystemExit("The iOS app and rewarded unit must belong to the same publisher.")
print("Production iOS rewarded ad configuration verified.")
