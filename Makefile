.PHONY: lint check_dupes install

sources :=$(wildcard ./exercises/**.json)

exercises.json: $(sources)
	jq -s '.' $^ > $@
	jsonfmt
exercises.nd.json: $(sources) # output to new line delimited JSON
	jq -s '.[]' $^ > $@
exercises.csv: dist/exercises.json # output to csv format
	in2csv ./dist/exercises.json > $@
lint:
	check-jsonschema --schemafile ./schema.json $(sources)
check:
	# check for duplicate id's, if there's ID's listed here
	# we've got duplicate id's that need to be resolved
	jq -s ".[]" $(sources) | jq '.id' | sort | uniq -d
