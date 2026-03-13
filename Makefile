.PHONY: lint check_dupes install rename-exercise

sources :=$(wildcard ./exercises/**.json)
translations_fr :=$(wildcard ./translations/fr/*.json)

exercises.json: $(sources)
	jq -s '.' $^ > $@
	jsonfmt --write
exercises.nd.json: $(sources) # output to new line delimited JSON
	jq -s '.[]' $^ > $@
exercises.csv: exercises.json # output to csv format
	in2csv ./exercises.json > $@
exercises.fr.json: exercises.json $(translations_fr) # merge French translations into exercises
	jq -s '(.[1:] | map({(.id): .}) | add // {}) as $$tr | \
	  .[0] | map(if $$tr[.id] then . + {i18n: {fr: ($$tr[.id] | {name, instructions})}} else . end)' \
	  exercises.json $(translations_fr) > $@
lint:
	check-jsonschema --schemafile ./schema.json $(sources)
check:
	# check for duplicate id's, if there's ID's listed here
	# we've got duplicate id's that need to be resolved
	jq -s ".[]" $(sources) | jq '.id' | sort | uniq -d
rename-exercise: # usage: make rename-exercise OLD=<old_id> NEW=<new_id>
	@test -n "$(OLD)" || { echo "Usage: make rename-exercise OLD=<old_id> NEW=<new_id>"; exit 1; }
	@test -n "$(NEW)" || { echo "Usage: make rename-exercise OLD=<old_id> NEW=<new_id>"; exit 1; }
	@test -f exercises/$(OLD).json || { echo "Error: exercises/$(OLD).json not found"; exit 1; }
	@test ! -f exercises/$(NEW).json || { echo "Error: exercises/$(NEW).json already exists"; exit 1; }
	jq '.id = "$(NEW)"' exercises/$(OLD).json > exercises/$(NEW).json
	rm exercises/$(OLD).json
	@[ ! -d exercises/$(OLD) ] || mv exercises/$(OLD) exercises/$(NEW)
	@for lang_dir in translations/*/; do \
	  [ -f "$${lang_dir}$(OLD).json" ] && mv "$${lang_dir}$(OLD).json" "$${lang_dir}$(NEW).json" || true; \
	done
	@echo "Renamed exercise $(OLD) -> $(NEW)"
