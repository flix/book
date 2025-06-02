# Standard functions

## Standard library functions for collections

Flix offers a rich set of functions that operate over collections.
Many functions apply over all the collections (e.g. `filter`).
Other functions are not implemented for specific collections
because they are semantically meaningless or the data structure
cannot provide a performant implementation of the operation.
For example, `map` over `Set` or `MutSet` is not implemented
because duplicated output of the function get discarded, which
is not usually what the user expects.

The following is the list of functions in the standard library
for Immutable collections. For mutable collections instead,
see [Mutating functions](./mutating-functions.md).

Legend:

* `Y`: Implemented.
* `P`: Planned to be implemented.
* `U`: Implementation to be changed to align with other collections.
* `R`: To be removed.
* Empty space: Not applicable to the collection.


| Operation        | String | List | Chain | Vector | DelayList | Set | Map |
|------------------|:------:|:----:|:-----:|:------:|:---------:|:---:|:---:|
| dropRight        |   Y    |      |   Y   |   Y    |           |     |     |
| head             |   P    |  Y   |   Y   |   Y    |     Y     |     |     |
| last             |   P    |  Y   |   Y   |   Y    |     Y     |     |     |
| init             |   Y    |  U   |   Y   |   Y    |     Y     |     |     |
| map              |   Y    |  Y   |   Y   |   Y    |     Y     |  R  |     |
| tail             |   P    |  P   |       |   P    |     Y     |     |     |
| toChunks         |   Y    |  P   |       |   P    |     P     |     |     |
| toMutQueue       |        |  P   |       |        |           |     |     |
| unfold           |   Y    |  Y   |       |   P    |     P     |  Y  |  Y  |
| unfoldWithIter   |   Y    |  Y   |       |   P    |     P     |  Y  |  Y  |
| unfoldWithOkIter |        |  Y   |       |        |           |     |     |
| unzip            |   P    |  Y   |   Y   |   Y    |     P     |     |     |
| zipWithIndex     |   P    |  Y   |       |   P    |     Y     |     |     |


Exclusions: Functions that are excluded from the list above are:

- Functions that are the same for all the collections (e.g. `ap`).
- Functions that applicable to only one collection (e.g. `lines`).
- Specialized collections like DelayMap, RedBlackTree, Nel, Nec.
