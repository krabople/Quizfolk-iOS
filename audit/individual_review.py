"""Track an editorial review. This tool never makes editorial decisions.

Prepare freezes the expanded input. Status checks coverage. Apply refuses to
publish a partial review and regenerates both playable copies from decisions.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "audit" / "individual-2026-10"
INPUT = REVIEW / "input.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint(question):
    return hashlib.sha256(canonical(question).encode("utf-8")).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_question(q):
    assert re.fullmatch(r"[a-f0-9]{20}", q["id"]), q["id"]
    assert isinstance(q["prompt"], str) and q["prompt"].strip()
    assert len(q["answers"]) == 4 and all(isinstance(a, str) and a.strip() for a in q["answers"])
    assert len({a.casefold().strip() for a in q["answers"]}) == 4, q["id"]
    assert type(q["correctIndex"]) is int and 0 <= q["correctIndex"] < 4
    assert q["categoryID"] in {str(n) for n in range(9, 39)}


def prepare():
    if INPUT.exists():
        raise SystemExit("Frozen input already exists; do not silently replace a review in progress.")
    bank = read(ROOT / "data" / "questions.json")
    original_count = len(bank)
    candidate_files = sorted((ROOT / "data" / "candidates").glob("*-expansion.json"))
    if not candidate_files:
        raise SystemExit("Add new question candidates before starting the full editorial review.")
    for path in candidate_files:
        bank.extend(read(path))
    for q in bank:
        validate_question(q)
    assert len({q["id"] for q in bank}) == len(bank), "Duplicate IDs in expanded input"
    REVIEW.mkdir(parents=True, exist_ok=True)
    write(INPUT, bank)
    write(REVIEW / "manifest.json", {
        "originalCount": original_count, "addedCandidates": len(bank) - original_count,
        "inputCount": len(bank), "inputSHA256": fingerprint(bank),
        "candidateFiles": [str(p.relative_to(ROOT)).replace("\\", "/") for p in candidate_files],
        "method": "Individual editorial judgments with per-question rationale. Automated code only checks coverage, schema and consistency.",
    })
    print(f"Frozen {len(bank)} questions, including {len(bank)-original_count} new candidates.")


def decisions(bank):
    by_id = {q["id"]: q for q in bank}
    reviewed = {}
    errors = []
    # Author review files are evidence, not independent acceptance decisions.
    for path in sorted((REVIEW / "decisions").glob("*.jsonl")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            d = json.loads(line)
            qid = d.get("id")
            where = f"{path.name}:{line_no} ({qid})"
            if qid not in by_id:
                errors.append(f"Unknown ID {where}")
                continue
            if qid in reviewed:
                errors.append(f"Duplicate decision {where}")
                continue
            if d.get("inputSHA256") != fingerprint(by_id[qid]):
                errors.append(f"Missing or stale input fingerprint {where}")
            if d.get("action") not in {"keep", "edit", "reject"}:
                errors.append(f"Invalid action {where}")
            for field in ("meaning", "answer", "grammar", "category", "reviewer"):
                if not isinstance(d.get(field), str) or not d[field].strip():
                    errors.append(f"Missing {field} rationale {where}")
            if not isinstance(d.get("sources"), list):
                errors.append(f"Missing sources list (empty for self-contained proof) {where}")
            if d.get("action") == "edit":
                replacement = d.get("replacement")
                if not isinstance(replacement, dict) or replacement.get("id") != qid:
                    errors.append(f"Missing full replacement {where}")
                else:
                    validate_question(replacement)
            reviewed[qid] = d
    return reviewed, errors


def status(apply=False):
    bank = read(INPUT)
    reviewed, errors = decisions(bank)
    missing = [q for q in bank if q["id"] not in reviewed]
    result = {"input": len(bank), "reviewed": len(reviewed), "remaining": len(missing),
              "decisions": dict(collections.Counter(d["action"] for d in reviewed.values())),
              "remainingByCategory": dict(sorted(collections.Counter(q["categoryID"] for q in missing).items())),
              "errors": errors, "complete": not missing and not errors}
    write(REVIEW / "progress.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not apply:
        return
    if not result["complete"]:
        raise SystemExit("Refusing publication: every input question needs an individual decision with valid evidence.")
    active, rejected = [], []
    for q in bank:
        d = reviewed[q["id"]]
        if d["action"] == "reject":
            rejected.append({"question": q, "decision": d})
            continue
        final = dict(d.get("replacement", q))
        final["reviewStatus"] = "individually_reviewed"
        final["auditVersion"] = "2026-10-individual-v1"
        validate_question(final)
        active.append(final)
    counts = collections.Counter(q["categoryID"] for q in active)
    categories = read(ROOT / "data" / "categories.json")
    for category in categories:
        category["questionCount"] = counts[category["id"]]
        if category["questionCount"] < 150:
            raise SystemExit(f"Insufficient reviewed questions in {category['name']}")
    payload = json.dumps(active, ensure_ascii=False, separators=(",", ":"))
    (ROOT / "data" / "questions.json").write_text(payload, encoding="utf-8")
    write(ROOT / "data" / "categories.json", categories)
    with sqlite3.connect(ROOT / "data" / "question-bank.sqlite") as db:
        db.execute("DELETE FROM questions")
        db.executemany("INSERT INTO questions(id,category_id,difficulty,prompt,answers,correct_index,source,license,review_status,payload) VALUES(?,?,?,?,?,?,?,?,?,?)", [
            (q["id"], q["categoryID"], q["difficulty"], q["prompt"], json.dumps(q["answers"], ensure_ascii=False),
             q["correctIndex"], q["source"], q["license"], q["reviewStatus"], canonical(q)) for q in active
        ])
        db.commit()
        db.execute("VACUUM")
    write(REVIEW / "rejected.json", rejected)
    result.update({"publishedCount": len(active), "publishedSHA256": hashlib.sha256(payload.encode()).hexdigest()})
    write(REVIEW / "completion.json", result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "status", "apply"))
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    else:
        status(apply=args.command == "apply")
