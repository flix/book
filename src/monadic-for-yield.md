# Monadic For-Yield

Flix supports a _for-yield_ construct similar to Scala's for-comprehensions and
Haskell's do notation. The _for-yield_ construct is syntactic sugar for uses of
`point` and `flatMap` (which are provided by the `Monad` type class). The
_for-yield_ construct also supports a _guard_-expression that uses `empty`
(which is provided by the `MonadZero` type class).

For example, the `for-yield` expression

```flix
let l1 = 1 :: 2 :: Nil;
let l2 = 1 :: 2 :: Nil;
for (x <- l1; y <- l2)
    yield (x, y)
```

evaluates to the list:

```flix
(1, 1) :: (1, 2) :: (2, 1) :: (2, 2) :: Nil
```

Whereas the `for-yield` expression with a guard

```flix
let l1 = 1 :: 2 :: Nil;
let l2 = 1 :: 2 :: Nil;
for (x <- l1; y <- l2; if x < y)
    yield (x, y)
```

evaluates to the list:

```flix
(1, 2) :: Nil
```

We can use `for-yield` on any data type which implements the `Monad` type class.

So, for example, we can use `for-yield` to work with `Option`s. Here

```flix
let o1 = Some(123);
let o2 = Some(456);
for (x <- o1; y <- o2) 
    yield x + y;
```

evaluates to:

```flix
Some(579)
```

We can also use `for-yield` to iterate through non-empty lists (`Nel`s)

```flix
let l1 = Nel(1, 2 :: Nil);
let l2 = Nel(1, 2 :: Nil);
for (x <- l1; y <- l2)
    yield (x, y)
```

which evaluates to the non-empty list:

```flix
Nel((1, 1), (1, 2) :: (2, 1) :: (2, 2) :: Nil)
```

> **Note:** We cannot use an `if`-guard with a non-empty list because such an
> `if`-guard requires an instance of the `MonadZero` type class which is not
> implemented by non-empty list. Intuitively, we cannot use a filter in
> combination with a data structures that cannot be empty.

