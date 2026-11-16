"""Validate separately audited additions without rewriting the October review."""
import hashlib
import json
import re


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def reviewed_supplements(root):
    catalog = root / "audit/supplements.json"
    if not catalog.exists():
        return []
    published = []
    directories = json.loads(catalog.read_text(encoding="utf-8"))
    assert len(directories) == len(set(directories))
    audit_root = (root / "audit").resolve()
    for entry in directories:
        directory = (audit_root / entry).resolve()
        assert directory.is_relative_to(audit_root)
        published.extend(reviewed_batch(directory))
    assert len(published) == len({q["id"] for q in published})
    return published


def reviewed_batch(directory):
    report = json.loads((directory / "completion.json").read_text(encoding="utf-8"))
    raw = (directory / "questions.json").read_bytes().replace(b"\r\n", b"\n")
    questions = json.loads(raw)
    review = [json.loads(line) for line in (directory / "decisions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert report["complete"] and report["remaining"] == 0 and not report["errors"]
    assert report["publishedCount"] == report["reviewed"] == len(questions) == len(review)
    assert report["publishedSHA256"] == hashlib.sha256(raw).hexdigest()
    assert questions and report["auditVersion"]
    decisions = {item["id"]: item for item in review}
    assert len(decisions) == len(review) == len({q["id"] for q in questions})
    for question in questions:
        assert re.fullmatch(r"[a-f0-9]{20}", question["id"])
        assert question["reviewStatus"] == "individually_reviewed"
        assert question["auditVersion"] == report["auditVersion"]
        decision = decisions[question["id"]]
        assert decision["questionSHA256"] == fingerprint(question)
        assert decision["action"] == "keep"
        for field in ("meaning", "answer", "grammar", "category", "reviewer"):
            assert isinstance(decision[field], str) and decision[field].strip()
        assert question["sourceURL"] in decision["sources"]
    return questions
