#!/usr/bin/env python3
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXERCISES_DIR = ROOT_DIR / "exercises"

EQUIPMENT_KEYWORDS = {
    "medicine ball": ["medicine ball"],
    "dumbbell": ["dumbbell"],
    "bands": ["band"],
    "kettlebells": ["kettlebell"],
    "foam roll": ["foam roll", "smr"],
    "cable": ["cable", "low pulley", "high pulley"],
    "machine": ["machine", "leverage", "smith"],
    "barbell": ["barbell", "axle", "straight bar"],
    "exercise ball": ["exercise ball", "stability ball", "physioball"],
    "e-z curl bar": ["ez bar", "e-z bar"],
}

def main():
    total = 0
    missing = 0
    for file_path in EXERCISES_DIR.glob("*.json"):
        with open(file_path, "r") as f:
            data = json.load(f)
        
        name = data.get("name", "").lower()
        equipment = data.get("equipment")
        
        if not equipment:
            for eq, keywords in EQUIPMENT_KEYWORDS.items():
                for kw in keywords:
                    if kw in name:
                        print(f"Potential missing equipment '{eq}' for: {data.get('id')} ({data.get('name')})")
                        missing += 1
                        break
        total += 1
    
    print(f"\nChecked {total} exercises, found {missing} potential missing equipment fields.")

if __name__ == "__main__":
    main()
