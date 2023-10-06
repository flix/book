## Records

Flix supports row polymorphic extensible records.

Flix records are immutable (but may contain mutable reference cells).

### Record Literals

A record literal is written with curly braces:

```flix
{ x = 1, y = 2 }
```

which has the record type
`{ x = Int32, y = Int32 }`.

The order of labels in a record does not matter. Hence the above record is
equivalent to:

```flix
{ y = 2, x = 1 }
```

which has type `{ y = Int32, x = Int32 }`. This type is equivalent to `{ x =
Int32, y = Int32 }`. In other words, the order of labels within a record type
does not matter.

### Label Access

We can access the label of a record using a dot:

```flix
let p = { x = 1, y = 2 };
p.x + p.y
```

The type system ensures that we cannot access a label that does not exist.

Records are immutable. Once constructed, the values of the record labels cannot
be changed.

### Label Update

While records are immutable, we can construct a new
record with an updated label value:

```flix
let p1 = { x = 1, y = 2 };
let p2 = { x = 3 | p1 };
p1.x + p2.x
```

The expression `{ x = 3 | p1 }` updates the record `p1` with a new value of its
`x` label. Note that updating a label requires that the label exists on the
record. A record cannot be *updated* with a new label, but it can be *extended*
with a new label, as we shall see later.

### Record Extension

We can add a new label to an existing record as follows:

```flix
let p1 = { x = 1, y = 2 };
let p2 = { +z = 3 | p1 };
p1.x + p1.y + p2.z
```

Here the expression `{ +z = 3 | p1 }` extends the record `p1` with a new label
`z` such that the result has three labels: `x`, `y`, and `z` all of which are of
`Int32` type.

### Record Restriction

Similarly to record extension, we can also remove a label from a record:

```flix
let p1 = { x = 1, y = 2 };
let p2 = { -y | p1 };
```

Here the record `p2` has the same labels as `p1` except that the `y` label has
been removed.

### Row Polymorphism: Open and Closed Records

A function may specify that it requires a record with two labels:

```flix
def f(r: {x = Int32, y = Int32}): Int32 = r.x + r.y
```

We can call this function with the records `{ x = 1, y = 2 }` and `{ y = 2, x =
1 }`, but we *cannot* call it with the record `{ x = 1, y = 2, z = 3 }` since
the signature of `f` demands a record with *exactly* two labels: `x` and `y`. We
say that the record `r` is *closed*.

We can lift this restriction by using row polymorphism:

```flix
def g(r: {x = Int32, y = Int32 | s}): Int32 = r.x + r.y
```

We can call this function with *any* record as long as it has `x` and `y` labels
which are of type `Int32`. We say that the record type of `r` is *open*.

### Named Parameters with Records

When a function has multiple parameters that share the same type, it is easy to
get confused about the right argument order. For example, what does
`String.contains("Hello","Hello World")` return? What does
`String.contains("Hello World", "Hello")` return?

A common solution to this problem is to use *named parameters*. Flix supports a
form of named parameters building on records. For example, we can write a
function translate to translate from one language to another as follows:

```flix
def translate(from: {from = Language}, to: {to = Language}, text: String): String = ???
```

We can call this function as follows:

```flix
translate({from = English}, {to = French}, "Where is the library?")
```

Since such verbosity gets tedious, we can also use the syntactic sugar:

```flix
translate(from = English, to = French, "Where is the library?")
```

which is equivalent to the above.

## Pattern matching
