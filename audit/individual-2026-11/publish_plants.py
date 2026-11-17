"""Assemble the two completed Plants reviews; no editorial decisions are generated here."""
import collections
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "audit"))
from validate_supplements import fingerprint, reviewed_batch

BATCHES = {
    "plants-easy": "2026-11-plants-easy-v1",
    "plants-challenge": "2026-11-plants-challenge-v1",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


all_questions = []
for name, version in BATCHES.items():
    directory = HERE / name
    drafts = read(directory / "draft.json")
    review = read(directory / "independent-review.json")
    assert review["status"] == "complete" and review["remaining"] == 0
    assert review["reviewed"] == len(drafts) == len(review["decisions"]) == 100
    decisions = {row["draftID"]: row for row in review["decisions"]}
    assert len(decisions) == 100
    questions, ledger = [], []
    for index, draft in enumerate(drafts):
        decision = decisions[draft["draftID"]]
        assert decision["decision"] in {"keep", "edited"}
        assert decision["prompt"] == draft["prompt"]
        # Match the reviewer's JSON.stringify fingerprint, preserving field order.
        draft_hash = hashlib.sha256(json.dumps(draft, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
        assert draft_hash == decision["reviewedSHA256"], draft["draftID"]
        assert draft["categoryID"] == "39" and len(set(draft["answers"])) == 4
        assert draft["difficulty"] in {"easy", "medium", "hard"}
        assert draft["sourceURL"].startswith("https://") and draft["rationale"]
        correct = draft["answers"][draft["correctIndex"]]
        rotation = index % 4
        answers = draft["answers"][rotation:] + draft["answers"][:rotation]
        qid = hashlib.sha256(("Quizfolk " + version + "\0" + draft["prompt"]).encode()).hexdigest()[:20]
        question = {"id": qid, "categoryID": "39", "difficulty": draft["difficulty"],
                    "prompt": draft["prompt"], "answers": answers, "correctIndex": answers.index(correct),
                    "source": "Quizfolk original; primary-source fact check", "sourceURL": draft["sourceURL"],
                    "license": "CC BY-SA 4.0", "reviewStatus": "individually_reviewed", "auditVersion": version}
        questions.append(question)
        ledger.append({"id": qid, "questionSHA256": fingerprint(question), "action": "keep",
                       "meaning": decision["meaning"], "answer": decision["answer"],
                       "grammar": decision["grammar"],
                       "category": decision.get("category", "Plant identification, science or gardening; relevant to Plants & flowers."),
                       "reviewer": decision["reviewer"], "sources": [draft["sourceURL"]],
                       "authorRationale": draft["rationale"], "independentDraftID": draft["draftID"]})
    write(directory / "questions.json", questions)
    (directory / "decisions.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in ledger), encoding="utf-8", newline="\n")
    write(directory / "completion.json", {
        "auditVersion": version, "date": "2026-11-17", "input": 100, "reviewed": 100,
        "remaining": 0, "errors": [], "complete": True, "publishedCount": 100,
        "publishedSHA256": hashlib.sha256((directory / "questions.json").read_bytes()).hexdigest(),
        "method": "Original individually authored questions followed by an independent question-by-question review of meaning, every option, correct answer, grammar, relevance and existing-bank overlap. Only final fingerprint-matched drafts are assembled.",
        "sources": sorted({q["sourceURL"] for q in questions}),
        "difficulty": dict(collections.Counter(q["difficulty"] for q in questions)),
    })
    assert reviewed_batch(directory) == questions
    all_questions.extend(questions)

bank_path = ROOT / "data/questions.json"
bank = [q for q in read(bank_path) if q.get("auditVersion") not in BATCHES.values()]
assert len(bank) == 21817, "Base bank changed; coordinate before publishing"
assert not ({q["id"] for q in bank} & {q["id"] for q in all_questions})
bank += all_questions
assert len(bank) == len({q["id"] for q in bank}) == len({q["prompt"].casefold() for q in bank}) == 22017
assert sum(q["categoryID"] == "39" for q in bank) == 350
bank_path.write_text(json.dumps(bank, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")

categories_path = ROOT / "data/categories.json"
categories = read(categories_path)
for category in categories:
    if category["id"] == "39":
        category["questionCount"] = 350
write(categories_path, categories)

catalog_path = ROOT / "audit/supplements.json"
catalog = read(catalog_path)
for name in BATCHES:
    entry = "individual-2026-11/" + name
    if entry not in catalog:
        catalog.append(entry)
write(catalog_path, catalog)

with sqlite3.connect(ROOT / "data/question-bank.sqlite") as db:
    db.executemany("DELETE FROM questions WHERE id = ?", [(q["id"],) for q in all_questions])
    db.executemany("INSERT INTO questions(id,category_id,difficulty,prompt,answers,correct_index,source,license,review_status,payload) VALUES(?,?,?,?,?,?,?,?,?,?)", [
        (q["id"], q["categoryID"], q["difficulty"], q["prompt"], json.dumps(q["answers"], ensure_ascii=False),
         q["correctIndex"], q["source"], q["license"], q["reviewStatus"], json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        for q in all_questions])
    db.commit()
print(json.dumps({"added": 200, "totalQuestions": len(bank), "plants": 350,
                  "difficultyAdded": dict(collections.Counter(q["difficulty"] for q in all_questions)),
                  "bankSHA256": hashlib.sha256(bank_path.read_bytes()).hexdigest()}))
