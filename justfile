default: # List all commands
	@just --list
lint: # Lint all exercises against the schema
	check-jsonschema --schemafile schema.json exercises/*.json
check: # Check for duplicate IDs
	./scripts/db_manager.py check
format: # Format all JSON files
	jsonfmt --write exercises/*.json translations/**/*.json
build: # Build the combined exercises.json (English)
	./scripts/db_manager.py build --output exercises.json
build-ndjson: # Build the combined exercises.nd.json (NDJSON)
	./scripts/db_manager.py build --format ndjson --output exercises.nd.json
build-fr: # Build exercises.json’s names and instructions French translations
	./scripts/db_manager.py build --lang fr --output exercises.fr.json
export-csv: build # Export to CSV (requires exercises.json to be built)
	in2csv exercises.json > exercises.csv
reid old_id new_id: # Change an exercise ID (usage: just rename old_id new_id)
	./scripts/db_manager.py rename {{old_id}} {{new_id}}
clean: # Clean up build artifacts
	rm --recursive --verbose exercises.json exercises*.json exercises.csv dist/
dist: build build-fr # Package artifacts
	mkdir --verbose dist/
	mv --verbose exercises*.json dist/
	cp --verbose i18n.json dist/
