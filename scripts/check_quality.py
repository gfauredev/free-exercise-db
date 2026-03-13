#!/usr/bin/env python3
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXERCISES_DIR = ROOT_DIR / "exercises"

def main():
    errors = 0
    total = 0
    for file_path in EXERCISES_DIR.glob("*.json"):
        total += 1
        with open(file_path, "r") as f:
            data = json.load(f)
        
        id = data.get("id")
        primary = set(data.get("primaryMuscles", []))
        secondary = set(data.get("secondaryMuscles", []))
        
        if not primary:
            print(f"Error: {id} has no primary muscles.")
            errors += 1
            
        overlap = primary.intersection(secondary)
        if overlap:
            print(f"Error: {id} has muscles in both primary and secondary: {overlap}")
            errors += 1
            
        if not data.get("instructions"):
            print(f"Error: {id} has no instructions.")
            errors += 1
            
        if not data.get("name"):
            print(f"Error: {id} has no name.")
            errors += 1

    print(f"\nChecked {total} exercises, found {errors} errors.")

if __name__ == "__main__":
    main()
