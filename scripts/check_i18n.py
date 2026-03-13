#!/usr/bin/env python3
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
I18N_FILE = ROOT_DIR / "i18n.json"
SCHEMA_FILE = ROOT_DIR / "schema.json"

def main():
    with open(SCHEMA_FILE, "r") as f:
        schema = json.load(f)
    
    with open(I18N_FILE, "r") as f:
        i18n = json.load(f)

    enums = {
        "force": schema["properties"]["force"]["enum"],
        "level": schema["properties"]["level"]["enum"],
        "mechanic": schema["properties"]["mechanic"]["enum"],
        "equipment": schema["properties"]["equipment"]["enum"],
        "category": schema["properties"]["category"]["enum"],
        "muscles": schema["properties"]["primaryMuscles"]["items"][0]["enum"]
    }

    for lang, translations in i18n.items():
        print(f"Checking language: {lang}")
        for key, values in enums.items():
            if key not in translations:
                print(f"  Error: {key} missing in {lang}")
                continue
            
            for val in values:
                if val not in translations[key]:
                    print(f"  Error: {key}.{val} missing translation in {lang}")

if __name__ == "__main__":
    main()
