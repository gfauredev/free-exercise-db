---
lang: en
---

[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

# Free Exercise DB 💪

<!--toc:start-->

- [What do they look like?](#what-do-they-look-like)
- [How do I use them?](#how-do-i-use-them)
- [Build tasks](#build-tasks)
  - [Linting & Check](#linting-check)
  - [Combining into a single JSON file](#combining-into-a-single-json-file)
  - [Importing into PostgreSQL](#importing-into-postgresql)
- [TODO](#todo)

<!--toc:end-->

My fork of the `JSON` (800+) Exercise Dataset by [yuhonas] that I use in my
training app [LogOut].

### What do they look like?

All exercises are stored as seperate `JSON` documents and conform to the
following [JSON Schema](./schema.json). Here’s an example :

```json
{
  "id": "alternate_incline_dumbbell_curl",
  "name": "Alternate Incline Dumbbell Curl",
  "force": "pull",
  "level": "beginner",
  "mechanic": "isolation",
  "equipment": "dumbbell",
  "primaryMuscles": [
    "biceps"
  ],
  "secondaryMuscles": [
    "forearms"
  ],
  "instructions": [
    "Sit down on an incline bench with a dumbbell in each hand being held at arms length. Tip: Keep the elbows close to the torso.This will be your starting position."
  ],
  "category": "strength",
  "images": [
    "alternate_incline_dumbbell_curl/0.jpg",
    "alternate_incline_dumbbell_curl/1.jpg"
  ]
}
```

See [Alternate Incline Dumbbell Curl JSON file].

To further explore the data, you can use [datasette].

### How do I use them?

Main combined DB `exercises.json`, translated `name` and `instructions` DBs
`exercises.<language>.json` and translated enums DB `i18n.json` are available
through [GitHub Releases](releases).

For images, you can leverage GitHub's hostinge prefixing image path's contained
in `JSON` with
`https://raw.githubusercontent.com/gfauredev/free-exercise-db/main/exercises/`,
eg. [air_bike/0.jpg].

### Build tasks

There are a number of helpful [justfile](./justfile) tasks that you can use.

#### Linting & Check

To lint all the `JSON` files against the [schema.json](./schema.json) use

```sh
just lint
```

To check for non-unique IDs, use

```sh
just check
```

#### Combining into a single JSON file

If you make changes to any of the exercises or add new ones, recombine all
single `JSON` files into a single `JSON` containing an array of objects, using
the `build` just task

```sh
just build
```

#### Importing into PostgreSQL

To combine all `JSON` files into [Newline Delimeted JSON](http://ndjson.org)
suitable for import into PostgreSQL use the following just task

```sh
just build-ndjson
```

See also
[Importing JSON into PostgreSQL using COPY](https://konbert.com/blog/import-json-into-postgres-using-copy)

[Alternate Incline Dumbbell Curl JSON file]: ./exercises/alternate_incline_dumbbell_curl.json
[air_bike/0.jpg]: https://raw.githubusercontent.com/gfauredev/free-exercise-db/main/exercises/air_bike/0.jpg
[cypress]: https://www.cypress.io
[eslint]: https://eslint.org
[exercises.json]: https://raw.githubusercontent.com/gfauredev/free-exercise-db/main/exercises.json
[logout]: https://github.com/gfauredev/LogOut
[vitest]: https://vitest.dev
[vue.js]: https://vuejs.org
[yuhonas]: https://github.com/yuhonas/free-exercise-db
[yuhonas.github.io/free-exercise-db]: https://yuhonas.github.io/free-exercise-db
[lite.datasette.io]: https://lite.datasette.io/?json=https://github.com/gfauredev/free-exercise-db/blob/main/exercises.json#/data/exercises?_facet_array=primaryMuscles&_facet=force&_facet=level&_facet=equipment
[datasette]: https://lite.datasette.io/?json=https://github.com/gfauredev/free-exercise-db/blob/main/exercises.json#/data/exercises?_facet_array=primaryMuscles&_facet=force&_facet=level&_facet=equipment
