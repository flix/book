# Monadic For-Yield

Flix supports a monadic _forM-yield_ construct similar to Scala's
for-comprehensions and Haskell's do notation. The _forM_ construct is syntactic
sugar for uses of `point` and `flatMap` (which are provided by the `Monad`
trait). The _forM_ construct also supports a _guard_-expression that uses
`empty` (which is provided by the `MonadZero` trait).

For example, the monadic `forM` expression:

```flix
let l1 = 1 :: 2 :: Nil;
let l2 = 1 :: 2 :: Nil;
forM (x <- l1; y <- l2)
    yield (x, y)
```

evaluates to the list:

```flix
(1, 1) :: (1, 2) :: (2, 1) :: (2, 2) :: Nil
```

## Using Guard Expressions

We can use _guard expressions_ in `forM` expressions. For example, the program:

```flix
let l1 = 1 :: 2 :: Nil;
let l2 = 1 :: 2 :: Nil;
forM (x <- l1; y <- l2; if x < y)
    yield (x, y)
```

evaluates to the list:

```flix
(1, 2) :: Nil
```

## Working with Options and Results

We can also use `forM` to work with the `Option` data type. For example:

```flix
def divide(x: Int32, y: Int32): Option[Int32] = 
    if (y == 0) None else Some(x / y)

def f(): Option[Int32] = 
    forM (
        x <- divide(5, 2);
        y <- divide(x, 8);
        z <- divide(9, y)
    ) yield x + y + z
```

Here the function `f` returns `None` since `x = 5 / 2 = 2` and `2 / 8 = 0` hence
the last division fails. 

Similarly, we can use `forM` to work with the `Result[e, t]` data type. For
example:

```flix
def main(): Result[String, Unit] \ IO = 
    println("Please enter your first name, last name, and age:");
    forM (
        fstName <- Console.readLine();
        lstName <- Console.readLine();
        ageLine <- Console.readLine();
        ageNum  <- Int32.parse(10, ageLine)
    ) yield {
        println("Hello ${lstName}, ${fstName}.");
        println("You are ${ageNum} years old!")
    }
```

Here `main` prompts the user to enter their first name, last name, and age. Each
call to `Console.readLine` returns a `Result[String, String]` value which is
either an error or the input string. Thus the local variables `fstName`,
`lstName`, and `ageLine` are `String`s. We parse `ageLine` into an `Int32` using
`Int32.parse`, which returns a `Result[String, Int32]` value. If every operation
is successful then we print a greeting and return `Ok(())` (i.e., `Ok` of
`Unit`). Otherwise, we return an `Err(msg)` value.

## Working with Other Monads

We can use `forM` with other types of `Monad`s, including `Chain` and `Nel`s
(non-empty lists). For example, we can write:

```flix
let l1 = Nel(1, 2 :: Nil);
let l2 = Nel(1, 2 :: Nil);
forM (x <- l1; y <- l2)
    yield (x, y)
```

which evaluates to the non-empty list:

```flix
Nel((1, 1), (1, 2) :: (2, 1) :: (2, 2) :: Nil)
```

> **Note:** We cannot use an `if`-guard with non-empty lists because such an
> `if`-guard requires an instance of the `MonadZero` trait which is not
> implemented by non-empty list (since such a list cannot be empty). 

## Desugaring

The `forM` expression is syntactic sugar for uses of `Monad.flatMap`,
`Applicative.point`, and `MonadZero.empty`. 

For example, the expression:

```flix
let l1 = 1 :: 2 :: Nil;
let l2 = 1 :: 2 :: Nil;
forM (x <- l1; y <- l2; if x < y)
    yield (x, y)
```

is de-sugared to:

```flix
Monad.flatMap(x -> 
    Monad.flatMap(y -> 
        if (x < y)
            Applicative.point((x, y))
        else 
            MonadZero.empty(), 
    l2), 
l1);
```
