# Default task: List all commands
default:
	@just --list

# Lint all exercises against the schema
lint:
	check-jsonschema --schemafile schema.json exercises/*.json

# Check for duplicate IDs
check:
	./scripts/db_manager.py check

# Format all JSON files
format:
	jsonfmt --write exercises/*.json translations/**/*.json

# Build the combined exercises.json (English)
build:
	./scripts/db_manager.py build --output exercises.json

# Build the combined exercises.nd.json (NDJSON)
build-ndjson:
	./scripts/db_manager.py build --format ndjson --output exercises.nd.json

# Build the French translations for exercises.json’s names and instructions
build-fr:
	./scripts/db_manager.py build --lang fr --output exercises.fr.json

# Export to CSV (requires exercises.json to be built)
export-csv: build
	in2csv exercises.json > exercises.csv

# Change an exercise ID (usage: just rename old_id new_id)
reid old_id new_id:
	./scripts/db_manager.py rename {{old_id}} {{new_id}}

# Clean up build artifacts
clean:
	rm -f exercises.json exercises.nd.json exercises.fr.json exercises.csv
