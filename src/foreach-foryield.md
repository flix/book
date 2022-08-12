# For-Each and For-Yield

> **Note:** This feature is experimental and not yet intended for use.

In Flix, as in other functional programming languages, most iteration is expressed either through recursion or with combinators (e.g. `map` or `foldLef`).

That said, Flix has syntactic sugar for two common types of loops: _for each_ and _for yield_. 

## For Each

## For Yield

The for-yield expression:

```flix
let l1 = 1 :: 2 :: 3 :: Nil;
let l2 = 1 :: 2 :: 3 :: Nil;
for (x <- l1; y <- l2) 
    yield (x, y)
```

evaluates to the list:

```
(1, 1) :: (1, 2) :: (1, 3) :: (2, 1) :: (2, 2) :: (2, 3) :: (3, 1) :: (3, 2) :: (3, 3) :: Nil
```

The for-yield expression:

```flix
let l1 = 1 :: 2 :: 3 :: Nil;
let l2 = 1 :: 2 :: 3 :: Nil;
for (x <- l1; y <- l2; if x < y) 
    yield (x, y)
```

evaluates to the list:

```
(1, 2) :: (1, 3) :: (2, 3) :: Nil
```

We can use for-yield on any data type which implements the `Monad` type class. For example, we can iterate through non-empty lists:

```flix
let l1 = Nel(1, 2 :: 3 :: Nil);
let l2 = Nel(1, 2 :: 3 :: Nil);
for (x <- l1; y <- l2) 
    yield (x, y)
```

which evaluates to the non-empty list:

```
Nel((1, 1), (1, 2) :: (1, 3) :: (2, 1) :: (2, 2) :: (2, 3) :: (3, 1) :: (3, 2) :: (3, 3) :: Nil)
```

> **Note:** We cannot use an `if`-guard with a non-empty list because such an `if`-guard requires an instance of the `MonadZero` type class which is not implemented by non-empty list. Intuitively, we cannot use a filter in combination with a data structures that cannot be empty.
