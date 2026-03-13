.PHONY: lint check_dupes install

sources :=$(wildcard ./exercises/**.json)

exercises.json: $(sources)
	jq -s '.' $^ > $@
	jsonfmt --write
exercises.nd.json: $(sources) # output to new line delimited JSON
	jq -s '.[]' $^ > $@
exercises.csv: exercises.json # output to csv format
	in2csv ./exercises.json > $@
lint:
	check-jsonschema --schemafile ./schema.json $(sources)
check:
	# check for duplicate id's, if there's ID's listed here
	# we've got duplicate id's that need to be resolved
	jq -s ".[]" $(sources) | jq '.id' | sort | uniq -d
