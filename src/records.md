# Records

Flix supports row polymorphic extensible records.

Flix records are immutable (but may contain mutable
reference cells).

## Record Literals

A record literal is written with curly braces:

```flix
{ x = 1, y = 2 }
```

which has the record type
`{ x :: Int32, y :: Int32 }`.

The order of fields in a record does not matter,
hence the above record is equivalent to the
record:

```flix
{ y = 2, x = 1 }
```

which has the record type
`{ y :: Int32, x :: Int32 }`.
This type is equivalent to the record type
`{ x :: Int32, y :: Int32 }`.
That is, the order of fields within a record type do
not matter.

## Field Access

We can access the field of a record using a dot:

```flix
let p = { x = 1, y = 2 };
p.x + p.y
```

The Flix type system ensures that we cannot access a
field that does not exist.

Records are immutable. A record, once constructed,
cannot have the values of any of its fields changed.
