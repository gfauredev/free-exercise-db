#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXERCISES_DIR = ROOT_DIR / "exercises"
TRANSLATIONS_DIR = ROOT_DIR / "translations"
I18N_FILE = ROOT_DIR / "i18n.json"
SCHEMA_FILE = ROOT_DIR / "schema.json"


def get_all_exercises():
    exercises = []
    for file in sorted(EXERCISES_DIR.glob("*.json")):
        with open(file, "r") as f:
            exercises.append(json.load(f))
    return exercises


def merge_translations(exercises, lang):
    lang_dir = TRANSLATIONS_DIR / lang
    if not lang_dir.exists():
        return []

    translated_exercises = []
    for ex in exercises:
        # 1. Check if the exercise has a full translation file (name AND instructions)
        trans_file = lang_dir / f"{ex['id']}.json"
        if not trans_file.exists():
            continue

        with open(trans_file, "r") as f:
            trans_data = json.load(f)

        if "name" not in trans_data or "instructions" not in trans_data:
            continue

        # 2. Return ONLY the requested fields
        translated_exercises.append({
            "id": ex["id"],
            "name": trans_data["name"],
            "instructions": trans_data["instructions"],
        })

    return translated_exercises


def check_duplicates():
    exercises = get_all_exercises()
    ids = [ex["id"] for ex in exercises]
    dupes = set([x for x in ids if ids.count(x) > 1])
    if dupes:
        print(f"Error: Duplicate IDs found: {', '.join(dupes)}")
        return False
    return True


def rename_exercise(old_id, new_id):
    old_file = EXERCISES_DIR / f"{old_id}.json"
    new_file = EXERCISES_DIR / f"{new_id}.json"

    if not old_file.exists():
        print(f"Error: Exercise {old_id} not found.")
        return False
    if new_file.exists():
        print(f"Error: Exercise {new_id} already exists.")
        return False

    # 1. Update the exercise file
    with open(old_file, "r") as f:
        data = json.load(f)
    data["id"] = new_id
    with open(new_file, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    old_file.unlink()

    # 2. Move images if they exist
    old_img_dir = EXERCISES_DIR / old_id
    new_img_dir = EXERCISES_DIR / new_id
    if old_img_dir.is_dir():
        old_img_dir.rename(new_img_dir)
        print(f"Moved images directory.")

    # 3. Rename translations
    for lang_dir in TRANSLATIONS_DIR.iterdir():
        if not lang_dir.is_dir():
            continue
        old_trans = lang_dir / f"{old_id}.json"
        new_trans = lang_dir / f"{new_id}.json"
        if old_trans.exists():
            with open(old_trans, "r") as f:
                trans_data = json.load(f)
            if "id" in trans_data:
                trans_data["id"] = new_id
            with open(new_trans, "w") as f:
                json.dump(trans_data, f, indent=2, ensure_ascii=False)
            old_trans.unlink()
            print(f"Renamed translation in {lang_dir.name}")

    print(f"Successfully renamed {old_id} to {new_id}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Manage Free Exercise DB")
    subparsers = parser.add_subparsers(dest="command")

    # Build command
    build_p = subparsers.add_parser("build", help="Combine all exercises into one JSON")
    build_p.add_argument("--lang", help="Target language (e.g. fr)")
    build_p.add_argument("--format", choices=["json", "ndjson"], default="json")
    build_p.add_argument("--output", help="Output file path")

    # Check command
    subparsers.add_parser("check", help="Check for duplicate IDs")

    # Rename command
    rename_p = subparsers.add_parser("rename", help="Rename an exercise")
    rename_p.add_argument("old_id")
    rename_p.add_argument("new_id")

    args = parser.parse_args()

    if args.command == "build":
        exercises = get_all_exercises()
        if args.lang:
            exercises = merge_translations(exercises, args.lang)

        if args.format == "json":
            out = json.dumps(exercises, indent=2, ensure_ascii=False)
        else:
            out = "\n".join([json.dumps(ex, ensure_ascii=False) for ex in exercises])

        if args.output:
            with open(args.output, "w") as f:
                f.write(out)
        else:
            print(out)

    elif args.command == "check":
        if not check_duplicates():
            sys.exit(1)
        print("No duplicate IDs found.")

    elif args.command == "rename":
        if not rename_exercise(args.old_id, args.new_id):
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
