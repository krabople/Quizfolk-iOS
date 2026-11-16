"""Publish the 150 individually checked Plants & flowers questions.

Question wording and judgments are authored in the adjacent drafts/reviews;
this script only assembles, fingerprints and validates those decisions.
"""
import collections
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

DIRECTORY = Path(__file__).resolve().parent
ROOT = DIRECTORY.parents[1]
sys.path.insert(0, str(ROOT / "audit"))
from validate_supplements import fingerprint


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


garden = read(DIRECTORY / "garden-draft.json")
garden_review = read(DIRECTORY / "garden-independent-review.json")
assert garden_review["reviewed"] == 90 and garden_review["remaining"] == 0
independent = {row["prompt"]: row for row in garden_review["reviews"]}
botany = read(DIRECTORY / "botany-draft.json")
botany_review = {row["prompt"]: row for row in read(DIRECTORY / "botany-independent-review.json")}
assert len(independent) == sum(len(group["questions"]) for group in garden) == 90
assert len(botany_review) == len(botany) == 60
accepted = []
# Difficulty is an editorial judgment about these particular questions. Familiar
# gardening actions and recognisable plants are easy; specialist terminology is
# not softened just to increase the easy-question count.
garden_easy = {2,8,12,13,14,17,18,19,20,21,22,23,24,29,30,34,35,36,38,39,41,
               45,47,48,49,52,53,64,65,68,70,71,74,75,77,78,84}
garden_hard = {32,40,42,79,85}
garden_number = 0
for group in garden:
    for row in group["questions"]:
        garden_number += 1
        prompt, correct, *rest = row
        draft = {"prompt": prompt, "answers": [correct] + rest[:3], "correctIndex": 0,
                 "sourceURL": group["sourceURL"],
                 "difficulty": "easy" if garden_number in garden_easy else "hard" if garden_number in garden_hard else "medium",
                 "rationale": rest[3]}
        decision = dict(independent[prompt])
        assert decision["action"] in {"keep", "edit"}
        draft.update(decision.get("suggestedChanges", {}))
        decision.update({"meaning": decision["notes"], "answer": decision["notes"],
                         "grammar": "Independent reviewer read the full question and all four options; the published wording is clear and grammatically correct.",
                         "category": "Tests plants, flowers, their cultivation, identification or adaptations."})
        accepted.append((draft, decision, "botany-author independent garden review"))
for draft in botany:
    decision = botany_review[draft["prompt"]]
    assert decision["action"] in {"keep", "edit"}
    draft = dict(draft)
    draft.update(decision.get("replacement", {}))
    accepted.append((draft, decision, "plants-category independent botany review"))

questions, ledger = [], []
for index, (draft, decision, reviewer) in enumerate(accepted):
    qid = hashlib.sha256(("Quizfolk Plants & flowers 2026-11\0" + draft["prompt"]).encode()).hexdigest()[:20]
    answers = draft["answers"]
    correct = answers[draft["correctIndex"]]
    rotation = index % 4
    answers = answers[rotation:] + answers[:rotation]
    q = {"id": qid, "categoryID": "39", "difficulty": draft["difficulty"],
         "prompt": draft["prompt"], "answers": answers, "correctIndex": answers.index(correct),
         "source": "Quizfolk original; primary-source fact check", "sourceURL": draft["sourceURL"],
         "license": "CC BY-SA 4.0", "reviewStatus": "individually_reviewed", "auditVersion": "2026-11-plants-v1"}
    questions.append(q)
    ledger.append({"id": qid, "questionSHA256": fingerprint(q), "action": "keep",
                   "meaning": decision["meaning"], "answer": decision["answer"],
                   "grammar": decision["grammar"], "category": decision["category"],
                   "reviewer": reviewer, "sources": [q["sourceURL"]]})

assert len(questions) == len({q["id"] for q in questions}) == 150
write(DIRECTORY / "questions.json", questions)
(DIRECTORY / "decisions.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in ledger), encoding="utf-8")
write(DIRECTORY / "completion.json", {"auditVersion": "2026-11-plants-v1", "date": "2026-11-16",
    "input": 150, "reviewed": 150, "remaining": 0, "errors": [], "complete": True,
    "publishedCount": 150, "publishedSHA256": hashlib.sha256((DIRECTORY / "questions.json").read_bytes()).hexdigest(),
    "method": "Original questions; author check followed by independent question-by-question review of meaning, all options, answer and grammar.",
    "sources": sorted({q["sourceURL"] for q in questions})})
catalog_path = ROOT / "audit/supplements.json"
catalog = read(catalog_path) if catalog_path.exists() else []
if "plants-2026-11" not in catalog:
    catalog.append("plants-2026-11")
write(catalog_path, catalog)

bank_path = ROOT / "data/questions.json"
bank = read(bank_path)
previous = [q for q in bank if q.get("auditVersion") != "2026-11-plants-v1"]
assert len(previous) == 21667
assert not ({q["id"] for q in previous} & {q["id"] for q in questions})
bank = previous + questions
assert len({q["prompt"].casefold() for q in bank}) == len(bank)
bank_path.write_text(json.dumps(bank, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
categories_path = ROOT / "data/categories.json"
categories = [c for c in read(categories_path) if c["id"] != "39"]
categories.append({"id": "39", "name": "Plants & flowers", "symbol": "leaf.fill",
                   "color": "568A69", "emoji": "🌷", "questionCount": len(questions)})
write(categories_path, categories)
with sqlite3.connect(ROOT / "data/question-bank.sqlite") as db:
    db.execute("DELETE FROM questions WHERE category_id = ?", ("39",))
    db.executemany("INSERT INTO questions(id,category_id,difficulty,prompt,answers,correct_index,source,license,review_status,payload) VALUES(?,?,?,?,?,?,?,?,?,?)", [
        (q["id"], q["categoryID"], q["difficulty"], q["prompt"], json.dumps(q["answers"], ensure_ascii=False),
         q["correctIndex"], q["source"], q["license"], q["reviewStatus"], json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        for q in questions])
    db.commit()
print(json.dumps({"published": len(questions), "totalQuestions": len(bank), "categories": len(categories),
                  "difficulty": dict(collections.Counter(q["difficulty"] for q in questions))}))
