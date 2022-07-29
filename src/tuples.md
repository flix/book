# Tuples

A tuple is a product of values.

A tuple is written with parentheses.
For example, here is a 2-tuple (a pair) of an
`Int32` and a `Bool`:

```flix
(123, true)
```

The type of the tuple is `(Int32, Bool)`.

We can destructure a tuple using pattern matching.
For example:

```flix
let t = ("Lucky", "Luke", 42, true); // 4-tuple
let (fstName, lstName, age, male) = t;
lstName
```

evaluates to the string `"Luke"`.

The Flix prelude defines the `fst` and `snd`
functions:

```flix
let t = (1, 2);
let x = fst(t); // x = 1
let y = snd(t)  // y = 2
```

which are useful when working with 2-tuples (i.e.
pairs).
For example:

```flix
let l = (1, 1) :: (2, 2) :: Nil; // has type List[(Int32, Int32)]
List.map(fst, l)                 // has type List[Int32]
```

which evaluates to a list that contains all the
first components of the list `l`.
