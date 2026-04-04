#!/usr/bin/env python3
import json
from re import search
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXERCISES_DIR = ROOT_DIR / "exercises"


def main():
    missing_images_count = "TODO Measure missing images and images directories"
    empty_images_count = 0
    force_inconsistencies = 0

    for file_path in EXERCISES_DIR.glob("*.json"):
        with open(file_path, "r") as f:
            data = json.load(f)

        id = data.get("id")
        name = data.get("name", "").lower()
        movement = data.get("movement")
        images = data.get("images", [])

        # 1. Check for empty images
        if not images:
            print(f"Warning: {id} has an empty images array")
            empty_images_count += 1

        # 2. Check for movement consistency
        if search("\bpress\b|\bthrow\b", name) and movement not in ("push", "isometric"):
            print(
                f"Potential movement inconsistency: {id} ({name}) is '{movement}' but has '{name}' in name (expected push)"
            )
            force_inconsistencies += 1
        if (search("\bcurl\b|\brow\b|\bpull\b", name)) and movement not in (
            "pull",
            "isometric",
        ):
            print(
                f"Potential movement inconsistency: {id} ({name}) is '{movement}' but has '{name}' in name (expected pull)"
            )
            force_inconsistencies += 1

    print("\nSummary:")
    print(f"Empty images arrays: {empty_images_count}")
    print(f"Referenced but missing images: {missing_images_count}")
    print(f"Potential force inconsistencies: {force_inconsistencies}")


if __name__ == "__main__":
    main()
