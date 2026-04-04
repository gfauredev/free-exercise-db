#!/usr/bin/env python3
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
I18N_FILE = ROOT_DIR / "i18n.json"
SCHEMA_FILE = ROOT_DIR / "schema.json"
EXERCISES_DIR = ROOT_DIR / "exercises"
TRANSLATIONS_DIR = ROOT_DIR / "translations"


def check_enum_translations():
    with open(SCHEMA_FILE, "r") as f:
        schema = json.load(f)

    with open(I18N_FILE, "r") as f:
        i18n = json.load(f)

    enums = {
        "movement": schema["properties"]["movement"]["enum"],
        "level": schema["properties"]["level"]["enum"],
        "mechanic": schema["properties"]["mechanic"]["enum"],
        "equipment": schema["properties"]["equipment"]["enum"],
        "category": schema["properties"]["category"]["enum"],
        "muscles": schema["properties"]["primaryMuscles"]["items"][0]["enum"]
    }

    errors = 0
    for lang, translations in i18n.items():
        print(f"Checking language: {lang}")
        for key, values in enums.items():
            if key not in translations:
                print(f"  Error: {key} missing in {lang}")
                errors += 1
                continue

            for val in values:
                if val not in translations[key]:
                    print(f"  Error: {key}.{val} missing translation in {lang}")
                    errors += 1
    return errors


def check_exercise_translations():
    exercise_ids = sorted(p.stem for p in EXERCISES_DIR.glob("*.json"))

    total_errors = 0
    for lang_dir in sorted(TRANSLATIONS_DIR.iterdir()):
        if not lang_dir.is_dir():
            continue
        lang = lang_dir.name
        translated_ids = {p.stem for p in lang_dir.glob("*.json")}
        missing = [eid for eid in exercise_ids if eid not in translated_ids]
        if missing:
            print(f"\nMissing exercise translations for language '{lang}' ({len(missing)} missing):")
            for eid in missing:
                print(f"  {eid}")
            total_errors += len(missing)
        else:
            print(f"\nAll {len(exercise_ids)} exercises translated for language '{lang}'.")
    return total_errors


def main():
    enum_errors = check_enum_translations()
    exercise_errors = check_exercise_translations()

    total = enum_errors + exercise_errors
    if total == 0:
        print("\nAll i18n checks passed.")
    else:
        print(f"\n{total} issue(s) found.")


if __name__ == "__main__":
    main()
