[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

<!--toc:start-->

- [Free Exercise DB 💪](#free-exercise-db-💪)
  - [What do they look like?](#what-do-they-look-like)
  - [How do I use them?](#how-do-i-use-them)
    - [Alternatively](#alternatively)
  - [Build tasks](#build-tasks)
    - [Linting](#linting)
    - [Combining into a single JSON file](#combining-into-a-single-json-file)
    - [Importing into PostgreSQL](#importing-into-postgresql)
  - [Browsable frontend](#browsable-frontend)
    - [Setup](#setup)
    - [Compile and Hot-Reload for Development](#compile-and-hot-reload-for-development)
    - [Compile and Minify for Production](#compile-and-minify-for-production)
    - [Run Unit Tests with Vitest](#run-unit-tests-with-vitest)
    - [Run End-to-End Tests with Cypress](#run-end-to-end-tests-with-cypress)
    - [Lint with ESLint](#lint-with-eslint)
  - [TODO](#todo)
    - [Incomplete fields](#incomplete-fields)
    - [Images](#images)

<!--toc:end-->

# Free Exercise DB 💪

My fork of the `JSON` (800+) Exercise Dataset by [yuhonas] that I use in my
training app [LogOut].

### What do they look like?

All exercises are stored as seperate `JSON` documents and conform to the
following [JSON Schema](./schema.json) eg.

```json
{
  "id": "Alternate_Incline_Dumbbell_Curl",
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
    "Alternate_Incline_Dumbbell_Curl/0.jpg",
    "Alternate_Incline_Dumbbell_Curl/1.jpg"
  ]
}
```

See
[Alternate_Incline_Dumbbell_Curl.json](./exercises/Alternate_Incline_Dumbbell_Curl.json)

To further explore the data, you can use [datasette].

### How do I use them?

You can check the repo out and use the `JSON` files and images locally

#### Alternatively

You can leverage github's hosting and access the single or combined
[exercises.json] and prefix any of image path's contained in the `JSON` with
`https://raw.githubusercontent.com/gfauredev/free-exercise-db/main/exercises/`
to get a hosted version of the image, eg.
[Air_Bike/0.jpg](https://raw.githubusercontent.com/gfauredev/free-exercise-db/main/exercises/Air_Bike/0.jpg).

### Build tasks

There are a number of helpful [Makefile](./Makefile) tasks that you can utilize

#### Linting

To lint all the `JSON` files against the [schema.json](./schema.json) use

```
make lint
```

#### Combining into a single JSON file

If you make changes to any of the exercises or add new ones, to recombine all
single `JSON` files into a single `JSON` containing an array of objects using
the following make task

```sh
make dist/exercises.json
```

#### Importing into PostgreSQL

To combine all `JSON` files into [Newline Delimeted JSON](http://ndjson.org)
suitable for import into PostgreSQL use the following make task

```sh
make dist/exercises.nd.json
```

See also
[Importing JSON into PostgreSQL using COPY](https://konbert.com/blog/import-json-into-postgres-using-copy)

### Browsable frontend

There is a simple searchable/browsable frontend to the data written in [Vue.js]
available at [yuhonas.github.io/free-exercise-db] all related code is in the
[site](./site) directory

#### Setup

```sh
npm install
```

#### Compile and Hot-Reload for Development

```sh
npm run dev
```

#### Compile and Minify for Production

```sh
npm run build
```

#### Run Unit Tests with [Vitest]

```sh
npm run test:unit
```

#### Run End-to-End Tests with [Cypress]

```sh
npm run test:e2e:dev
```

This runs the end-to-end tests against the Vite development server. It is much
faster than the production build.

But it's still recommended to test the production build with `test:e2e` before
deploying (e.g. in CI environments):

```sh
npm run build
npm run test:e2e
```

#### Lint with [ESLint]

```sh
npm run lint
```

### TODO

#### Incomplete fields

The following fields are incomplete in _some_ `JSON` files and in such have had
to allow `null` in [schema.json](./schema.json)

- force
- mechanic
- equipment

#### Images

There are also a small number of duplicate images eg.

```sh
jdupes --summarize --recurse .

Scanning: 2620 files, 874 items (in 1 specified)
25 duplicate files (in 22 sets), occupying 809 KB
```

[Cypress]: https://www.cypress.io
[Eslint]: https://eslint.org
[exercises.json]: https://raw.githubusercontent.com/gfauredev/free-exercise-db/main/dist/exercises.json
[LogOut]: https://github.com/gfauredev/LogOut
[logout]: https://github.com/gfauredev/LogOut
[Vitest]: https://vitest.dev
[Vue.js]: https://vuejs.org
[yuhonas]: https://github.com/yuhonas/free-exercise-db
[yuhonas.github.io/free-exercise-db]: https://yuhonas.github.io/free-exercise-db
[lite.datasette.io]: https://lite.datasette.io/?json=https://github.com/gfauredev/free-exercise-db/blob/main/dist/exercises.json#/data/exercises?_facet_array=primaryMuscles&_facet=force&_facet=level&_facet=equipment
[datasette]: https://lite.datasette.io/?json=https://github.com/gfauredev/free-exercise-db/blob/main/dist/exercises.json#/data/exercises?_facet_array=primaryMuscles&_facet=force&_facet=level&_facet=equipment
