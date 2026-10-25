#!/usr/bin/env python3
"""
Scans the photos/ and gallery/ folders and writes photos.json.

You normally never run this by hand: the GitHub Actions deploy runs it on every push.
For local preview:  python3 scan.py && python3 -m http.server 8000
"""
import json, os, re, subprocess, sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
FOLDERS = {"photos": "photos", "gallery": "gallery"}   # folder name -> key in photos.json
SHOWN = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".svg", ".bmp"}
NOT_BROWSER_SAFE = {".heic", ".heif", ".tif", ".tiff"}

CAMERA_NAME = re.compile(
    r"(?i)(img|_mg|dsc[nf]?|pxl|mvimg|photo|image|screenshot)?[-_ ]*[\d\-_ ]+(edited|copy|\(\d+\))?"
)


def nice_title(stem: str) -> str:
    """'sunset-at-the_lake' -> 'sunset at the lake'. Camera/UUID names -> '' (no caption)."""
    if CAMERA_NAME.fullmatch(stem) or (len(stem) >= 12 and re.fullmatch(r"[0-9a-fA-F\-_]+", stem)):
        return ""
    title = re.sub(r"[-_]+", " ", stem)
    title = re.sub(r"[<>\"'&]", "", title)
    return re.sub(r"\s+", " ", title).strip()


def added_time(path: Path) -> float:
    """When the file was added (git commit time), falling back to file modified time."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return float(out)
    except Exception:
        pass
    return path.stat().st_mtime


def warn(msg: str):
    print(("::warning::" if os.environ.get("GITHUB_ACTIONS") else "WARNING: ") + msg, file=sys.stderr)


def main():
    result = {}
    for folder, key in FOLDERS.items():
        base = ROOT / folder
        items = []
        if base.is_dir():
            for p in base.rglob("*"):
                if not p.is_file() or any(part.startswith(".") for part in p.relative_to(base).parts):
                    continue
                ext = p.suffix.lower()
                if ext in NOT_BROWSER_SAFE:
                    warn(f"{p.relative_to(ROOT)} skipped: {ext} files don't display in most browsers. Export it as JPG.")
                    continue
                if ext not in SHOWN:
                    continue
                items.append((added_time(p), p))
        items.sort(key=lambda t: (-t[0], t[1].name.lower()))   # newest first
        result[key] = [
            {
                "title": nice_title(p.stem),
                "desc": "",
                "imageUrl": quote(p.relative_to(ROOT).as_posix()),
            }
            for _, p in items
        ]
        print(f"{folder}/: {len(items)} image(s)")

    (ROOT / "photos.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
