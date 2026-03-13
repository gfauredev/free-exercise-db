#!/usr/bin/env python3
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXERCISES_DIR = ROOT_DIR / "exercises"

def main():
    missing_images_count = 0
    empty_images_count = 0
    force_inconsistencies = 0
    
    for file_path in EXERCISES_DIR.glob("*.json"):
        with open(file_path, "r") as f:
            data = json.load(f)
        
        id = data.get("id")
        name = data.get("name", "").lower()
        force = data.get("force")
        images = data.get("images", [])

        # 1. Check for empty images
        if not images:
            print(f"Warning: {id} has an empty images array.")
            empty_images_count += 1

        # 2. Check for force consistency
        if "press" in name and force != "push":
            # Some stretches might have 'press' in name but be 'static'
            if force != "static":
                print(f"Potential force inconsistency: {id} ({name}) is '{force}' but has 'press' in name.")
                force_inconsistencies += 1
        
        if ("curl" in name or "row" in name or "pull" in name) and force != "pull":
             if force != "static" and "pullover" not in name: # Pullover can be push/pull depending on technique
                print(f"Potential force inconsistency: {id} ({name}) is '{force}' but has '{name}' in name (expected pull).")
                force_inconsistencies += 1

    print("\nSummary:")
    print(f"Empty images arrays: {empty_images_count}")
    print(f"Potential force inconsistencies: {force_inconsistencies}")

if __name__ == "__main__":
    main()
