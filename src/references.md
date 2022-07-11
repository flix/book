# References

Flix supports references in the ML-tradition.
The three key operations are `ref e`, `deref e`, and
`e := e`.
The `ref e` operation allocates a reference cell in
the heap and returns its location, the `deref`
operation dereferences a location and returns the
content of a reference cell, and finally the
assigment `:=` operation changes the value
of a reference cell. Informally, a reference cell can
be thought of as an "object" with a single field that
can be changed.

All operations on references are impure.
As such, all functions that use references must be
marked as `Impure` or be casted to `Pure`.

## Allocation

A reference cell is allocated as follows:

```flix
ref 42
```

which evaluates to a value of type `Ref[Int32]` which
is a reference (pointer) to a single memory cell that
holds the value `42`.

## Dereference

A reference cell is accessed (de-referenced) as
follows:

```flix
let l = ref 42;
deref l
```

which evaluates to `42` as expected.

## Assignment

A reference cell can have its value updated as
follows:

```flix
let l = ref 42;
l := 84;
deref l
```

which evaluates to `84` as expected.

## Example: A Simple Counter

The following program models a simple counter that
can be incremented:

```flix
enum Counter {
    case Counter(Ref[Int32])
}

def newCounter(): Counter & Impure = Counter(ref 0)

def getCount(c: Counter): Int32 & Impure =
    let Counter(l) = c;
    deref l

def increment(c: Counter): Unit & Impure =
    let Counter(l) = c;
    l := (deref l) + 1

def f(): Unit & Impure =
    let c = newCounter();
    increment(c);
    increment(c);
    increment(c);
    getCount(c) |> println
```

Note that the `newCounter`, `getCount`, `increment`
and `f` functions must all be marked as `Impure`.

## Aliasing and References to References

References naturally support aliasing since that is
exactly their purpose.
For example:

```flix
let l1 = ref 42;
let l2 = l1;
l2 := 84;
deref l1
```

Evaluates to `84` because the reference cell that
`l1` points to is modified through the alias `l2`.

References can point-to references as the following
example illustrates:

```flix
let l1 = ref 42;
let l2 = ref l1;
deref (deref l2)
```
Evaluates to `42` as expected.

#### Design Note

Flix does not support any notion of global mutable
state.
If you need to maintain a program-wide counter (or
other mutable state) then you have to allocate it in
the main function and explicitly thread it through
the program.

## Mutable Tuples and Records

Flix tuples and records are *immutable*.
However, tuples and records may contain mutable
references.

For example, here is a pair that contains two mutable
references:

```flix
let p = (ref 1, ref 2);
fst(p) := 123
```

The type of the pair is `(Ref[Int32], Ref[Int32])`.
The assignment does not change the pair itself (it is
immutable), but rather changes the value of the
reference cell in the first component of the pair.

Similarly, here is a record that contains two mutable
references:

```flix
let r = { fstName = ref "Lucky", lstName = ref "Luke"};
r.fstName := "Unlucky"
```

The type of the record is
`{"{ fstName :: Ref[String], lstName :: Ref[String] }"}`.
Again, the assignment does not change the record
itself, but rather changes the value of the reference
cell corresponding to the `fstName` field.
