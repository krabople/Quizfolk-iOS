"""Select named, original XCTest attachments without changing their pixels.

Usage: python prepare_captures.py DOWNLOADED_ARTIFACTS CAPTURE_ROOT RUN_ID
Download all Quizfolk-Store-* artifacts into DOWNLOADED_ARTIFACTS first.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import struct
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
parser.add_argument("destination", type=Path)
parser.add_argument("run")
parser.add_argument("--available", action="store_true")
parser.add_argument("--ipad-artifacts", type=Path)
parser.add_argument("--ipad-run")
parser.add_argument("--overlay", nargs=2, action="append", default=[], metavar=("ARTIFACTS", "RUN"),
                    help="Use named replacement captures from a later partial run")
args = parser.parse_args()
source, destination = args.source.resolve(), args.destination.resolve()
run = args.run
assert bool(args.ipad_artifacts) == bool(args.ipad_run), "Provide both iPad override arguments"
mapping = {
    "01-duel": "Gameplay", "02-topics": "Topics", "03-challenges": "Friends",
    "04-topic-progress": "Levels", "05-topic-league": "League",
    "06-tournament": "Tournament", "07-friends": "Party", "08-badges": "Badges",
    "09-rival-profile": "Profile", "10-result": "Result",
}
devices = {
    "iphone-medium": ("iphone-medium", (1206, 2622)),
    "iphone-large": ("iphone-large", (1320, 2868)),
    "ipad-13": ("ipad", (2064, 2752)),
}
report = {"run": run, "url": f"https://github.com/krabople/Quizfolk-iOS/actions/runs/{run}", "devices": []}
for artifact, (device, dimensions) in devices.items():
    device_run = args.ipad_run if artifact == "ipad-13" and args.ipad_run else run
    base = args.ipad_artifacts.resolve() if artifact == "ipad-13" and args.ipad_artifacts else source
    root = base / f"Quizfolk-Store-{artifact}"
    if not root.exists() and args.available:
        continue
    manifest_path = next(root.rglob("manifest.json"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    provenance_path = next(root.rglob("provenance.json"))
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    folder = destination / device
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copy2(manifest_path, folder / "attachment-manifest.json")
    shutil.copy2(provenance_path, folder / "provenance.json")
    candidates = [(manifest_path, manifest, provenance, device_run)]
    for overlay_directory, overlay_run in args.overlay:
        overlay_root = Path(overlay_directory).resolve() / f"Quizfolk-Store-{artifact}"
        if not overlay_root.exists():
            continue
        overlay_manifest_path = next(overlay_root.rglob("manifest.json"))
        overlay_manifest = json.loads(overlay_manifest_path.read_text(encoding="utf-8"))
        overlay_provenance_path = next(overlay_root.rglob("provenance.json"))
        overlay_provenance = json.loads(overlay_provenance_path.read_text(encoding="utf-8"))
        candidates.append((overlay_manifest_path, overlay_manifest, overlay_provenance, overlay_run))
        shutil.copy2(overlay_manifest_path, folder / f"attachment-manifest-{overlay_run}.json")
        shutil.copy2(overlay_provenance_path, folder / f"provenance-{overlay_run}.json")
    captures = []
    selected_sources = {}
    for label, name in mapping.items():
        for selected_manifest_path, selected_manifest, selected_provenance, selected_run in reversed(candidates):
            matches = [a for group in selected_manifest for a in group["attachments"]
                       if a.get("suggestedHumanReadableName", "").startswith(f"STORE-{label}_")
                       and not a.get("isAssociatedWithFailure", False)]
            if matches:
                break
        assert len(matches) == 1, (device, label, len(matches))
        attachment = matches[0]
        original = selected_manifest_path.parent / attachment["exportedFileName"]
        pixels = original.read_bytes()
        assert pixels[:8] == b"\x89PNG\r\n\x1a\n", original
        size = struct.unpack(">II", pixels[16:24])
        assert size == dimensions, (original, size, dimensions)
        target = folder / f"{name}.png"
        shutil.copy2(original, target)
        selected_sources[selected_run] = selected_provenance
        captures.append({"name": name, "originalAttachment": attachment["exportedFileName"],
                         "width": size[0], "height": size[1],
                         "run": selected_run, "sourceCommit": selected_provenance["source"],
                         "device": selected_provenance["device"]["name"],
                         "targetedDeviceFamily": selected_provenance.get("targetedDeviceFamily"),
                         "presentation": selected_provenance.get("ipadPresentation") if device == "ipad" else "Native iPhone",
                         "sha256": hashlib.sha256(pixels).hexdigest()})
    report["devices"].append({"key": device, "sources": selected_sources, "captures": captures})
    print(device, provenance["device"]["name"], len(captures), dimensions)
(destination / "capture-provenance.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
