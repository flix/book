# Arrays

While Flix recommends the use of immutable data
structures (such as immutable lists, sets, and maps),
mutable arrays may be useful for performance critical
code.

We recommend that arrays are used sparingly and that
when possible their use is hidden as an
implementation detail.
For example, the Flix Datalog engine uses arrays
internally but exposes a functional (immutable)
interface.

Flix uses monomorphization and consequently primitive
arrays are not boxed.
For example, the representation of an `Array[Int32]`
is compact and efficient.

All operations on arrays are impure.
As such, all functions that use arrays must be marked
as `Impure` or be casted to `Pure`.
However, accessing the length of an array is pure 
since the size of an array cannot change after it has
been created.

Arrays should only be used for low-level code.
The `MutList` data structure, available in the
standard library, provides a mutable
dynamically-expanding data structure similar to
`java.util.ArrayList`. Its implementation is backed
by an array that is dynamically resized and it
provides amortized O(1) push operations.

## Array Literals

An array literal is of the form `[e1, e2, ... en]`.
For example, the expression:

```flix
[1, 2, 3, 4]
```

evaluates to an array with the four elements:
`1, 2, 3, 4`.

In some cases it is useful to allocate a large array
filled with the same value.
The expression:

```flix
["Hello World"; 100]
```

evaluates to an array of length 100 where every entry
contains the string `"Hello World"`.

#### Design Note

Flix does not allow the allocation of an array
without assigning a "default value" to each entry in
the array.

## Reading and Writing from Arrays

Arrays can be accessed and updated using standard
syntax.
For example:

```flix
let a = [0; 10];
a[0] = 21;
a[1] = 42;
a[0] + a[1]
```

evaluates to `63`, as expected.

## Array Slicing

Arrays can be sliced.
Slicing an array (shallowly) copies a subrange of the
array.
For example:

```flix
let a = [1, 2, 3, 4, 5];
a[2..4]
```

evaluates to the array `[3, 4]`.

The start or end index may be omitted.
For example:

```flix
let a = [1, 2, 3, 4, 5];
let a1 = a[2..]; // evaluates to [3, 4, 5]
let a2 = a[..4]  // evaluates to [1, 2, 3, 4]
```

If both the start and end index are omitted the
entire array is copied.
For example:

```flix
let a = [1, 2, 3, 4, 5];
a[..]
```

evaluates to the (copied) array `[1, 2, 3, 4, 5]`.

#### Design Note

Slicing an array using the same start and end index
returns the empty array.
For example, `[0, 1, 2, 3][2..2]` evaluates to `[]`.

#### Warning

Slicing with negative indices is undefined and
results in runtime errors.

## Array Length

The length of an array is accessed as follows:

```flix
let a = [1, 2, 3, 4, 5];
a.length
```
which evaluates to `5`.
