# Mutating functions

## Standard library functions for mutable collections

The following is the list of functions in the standard library
for Mutable collections. For immutable collections instead,
see [Standard functions](./standard-functions.md). Functions that
are the same for all the collections are excluded from the list below.

Exclusions:

Some functions are excluded from the list below:

- Functions that are the same for all the collections (e.g. `append`).
- Functions that applicable to only one collection (e.g. `makeSet`).

Legend:

* `Y`: Implemented.
* `P`: Planned to be implemented.
* `U`: Implementation to be changed to align with other collections.
* Empty space: Not applicable to the collection.


| Operation \ Type   | Array | MutList | MutDeque | MutQueue | MutSet | MutMap | MutDisjointSets |
|--------------------|:-----:|:-------:|:--------:|:--------:|:------:|:------:|:---------------:|
| @                  |   Y   |    P    |    P     |    P     |   P    |   P    |        P        |
| init               |   Y   |    P    |    P     |    P     |   P    |   P    |                 |
| enqueue            |       |         |          |    U     |        |        |                 |
| enqueueAll         |       |         |          |    U     |        |        |                 |
| map                |   Y   |    Y    |          |          |        |   Y    |                 |
| span               |   Y   |    P    |    P     |          |   P    |   P    |                 |
| tail               |   P   |    P    |          |          |        |        |                 |
| toChunks           |   P   |    P    |          |          |        |        |                 |
| transform          |   Y   |    Y    |          |          |   Y    |   Y    |                 |
| transformWithIndex |   Y   |    Y    |          |          |        |        |                 |
| transformWithKey   |       |         |          |          |        |   Y    |                 |
| toMutDeque         |   Y   |    Y    |          |    P     |   Y    |   Y    |        P        |
| toMutList          |   Y   |         |    P     |    P     |   P    |   P    |        P        |
| toMutQueue         |   P   |    P    |    P     |          |   P    |        |                 |
| unfold             |   P   |    P    |    P     |          |   P    |        |                 |
| unzip              |   Y   |    P    |    P     |          |   P    |        |                 |
| zip                |   Y   |    P    |    P     |          |   P    |        |                 |
| zipWith            |   Y   |    P    |    P     |          |   P    |        |                 |
| zipWithIndex       |   P   |    P    |    P     |          |   P    |        |                 |