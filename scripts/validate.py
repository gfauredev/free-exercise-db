#!/usr/bin/env python3
import json
import jsonschema
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
EXERCISES_DIR = ROOT_DIR / "exercises"
TRANSLATIONS_DIR = ROOT_DIR / "translations"
I18N_FILE = ROOT_DIR / "i18n.json"
SCHEMA_FILE = ROOT_DIR / "schema.json"

def validate_schema(schema, data, file_path):
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Schema violation in {file_path}: {e.message}")
        return False

def main():
    errors = 0
    warnings = 0

    if not SCHEMA_FILE.exists():
        print(f"Error: {SCHEMA_FILE} not found.")
        sys.exit(1)

    with open(SCHEMA_FILE, "r") as f:
        schema = json.load(f)

    # 1. Check exercises
    all_exercise_files = list(EXERCISES_DIR.glob("*.json"))
    all_exercise_ids = set()
    
    for file_path in all_exercise_files:
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error: {file_path} is not valid JSON: {e}")
                errors += 1
                continue

        # Check schema
        if not validate_schema(schema, data, file_path):
            errors += 1

        # Check id matches filename
        expected_id = file_path.stem
        if data.get("id") != expected_id:
            print(f"Error: {file_path}: 'id' ({data.get('id')}) does not match filename.")
            errors += 1
        
        all_exercise_ids.add(expected_id)

        # Check images exist
        img_paths = data.get("images", [])
        for img_rel_path in img_paths:
            img_abs_path = EXERCISES_DIR / img_rel_path
            if not img_abs_path.exists():
                print(f"Error: {file_path}: Image {img_rel_path} does not exist.")
                errors += 1

    # 2. Check for extra directories in exercises
    for item in EXERCISES_DIR.iterdir():
        if item.is_dir():
            json_file = EXERCISES_DIR / f"{item.name}.json"
            if not json_file.exists():
                print(f"Warning: Directory {item} exists but no corresponding .json file found.")
                warnings += 1

    # 3. Check translations
    if TRANSLATIONS_DIR.exists():
        for lang_dir in TRANSLATIONS_DIR.iterdir():
            if not lang_dir.is_dir():
                continue
            
            for trans_file in lang_dir.glob("*.json"):
                with open(trans_file, "r") as f:
                    try:
                        trans_data = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Error: {trans_file} is not valid JSON.")
                        errors += 1
                        continue
                
                trans_id = trans_file.stem
                if trans_id not in all_exercise_ids:
                    print(f"Error: Translation {trans_file} for unknown exercise ID: {trans_id}")
                    errors += 1
                
                if trans_data.get("id") != trans_id:
                    print(f"Error: Translation {trans_file}: 'id' ({trans_data.get('id')}) does not match filename.")
                    errors += 1

    # 4. Check i18n.json consistency
    if I18N_FILE.exists():
        with open(I18N_FILE, "r") as f:
            i18n_data = json.load(f)
        
        # Check all exercises have at least some metadata in i18n? 
        # i18n.json seems to contain category/muscle names translations, not per-exercise.
        pass

    print(f"\nValidation complete: {errors} errors, {warnings} warnings.")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
