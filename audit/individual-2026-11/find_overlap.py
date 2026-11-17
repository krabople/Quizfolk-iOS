"""Surface possible repeated concepts for a human; this does not approve questions."""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
draft = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
bank = json.loads((root / "data/questions.json").read_text(encoding="utf-8"))
stop = set("a an the of to for in on at by with from what which who when where why how is are was were be been being do does did usually commonly normally as its it this that these those and or not would you your called known name term type part can has have most one following often than per".split())


def words(text):
    return set(re.findall(r"[a-z0-9]+", text.casefold())) - stop


indexed = [(q, words(q["prompt"])) for q in bank]
for number, q in enumerate(draft, 1):
    tokens = words(q["prompt"])
    hits = []
    for old, other in indexed:
        common = len(tokens & other)
        union = len(tokens | other)
        score = common / max(1, union)
        coverage = common / max(1, min(len(tokens), len(other)))
        if score >= .5 or (common >= 3 and coverage >= .8):
            hits.append((score, old))
    if hits:
        print(json.dumps({"number": number, "prompt": q["prompt"], "matches": [{"similarity": round(s, 2), "id": old["id"], "categoryID": old["categoryID"], "prompt": old["prompt"], "answer": old["answers"][old["correctIndex"]]} for s, old in sorted(hits, key=lambda hit: -hit[0])[:3]]}, ensure_ascii=False))
