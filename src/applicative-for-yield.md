# Applicative For-Yield

In addition to the monadic `forM` expression, Flix supports an applicative
`forA` expression that builds on the `Applicative` trait. The `forA`
construct makes it simple to write error-handling code which uses the
`Validation[e, t]` data type. 

## Working with Validations

We can use the `forA` expression to validate user input while collecting all
errors.

```flix
enum Connection(String, String)

enum InvalidInput {
    case InvalidUserName,
    case InvalidPassword
}

def validateUser(s: String): Validation[InvalidInput, String] =
    if (8 <= String.length(s) and String.forAll(Char.isLetter, s))
        Validation.Success(s)
    else 
        Validation.Failure(Nec.singleton(InvalidInput.InvalidUserName))

def validatePass(s: String): Validation[InvalidInput, String] =
    if (12 <= String.length(s) and String.length(s) <= 20)
        Validation.Success(s)
    else 
        Validation.Failure(Nec.singleton(InvalidInput.InvalidPassword))

def connect(u: String, p: String): Validation[InvalidInput, Connection] = 
    forA (
        user <- validateUser(u);
        pass <- validatePass(p)
    ) yield Connection.Connection(user, pass)
```

The expression:

```flix
connect("Lucky Luke", "Ratata")
```

evaluates to:

```flix
Failure(Nec#{InvalidUserName, InvalidPassword})
```

which contains _both_ input validation errors. On the other hand, the expression:

```flix
connect("luckyluke", "password12356789")
```

evaluates to:

```flix
Success(Connection(luckyluke, password12356789))
```

## Applicatives are Independent Computations

We can write a monadic `forM` expression where the result of one monadic
operation is used as the input to another monadic operation. For example:

```flix
forM(x <- Some(123);  y <- Some(x)) 
    yield (x, y)
```

Here the value of `y` depends on `x`. That is, the computation of `x` and `y`
are not independent. 

If we try to same with the applicative `forA` expression:

```flix
forA(x <- Some(123); y <- Some(x))
    yield (x, y)
```

then the Flix compiler emits a compiler error:

```flix
❌ -- Resolution Error --------------

>> Undefined name 'x'.

10 |         y <- Some(x)
                       ^
                       name not found
```

because the computations of `x` and `y` are _independent_ and hence the value of
`x` is _not_ in scope when we define the value of `y`.

## Desugaring

The `forA` expression is syntactic sugar for uses of `Functor.map` and
`Applicative.ap`.

For example, the expression:

```flix
let o1 = Some(21);
let o2 = Some(42);
forA(x <- o1; y <- o2) 
    yield x + y;
```

is de-sugared to:

```flix
Applicative.ap(Functor.map(x -> y -> x + y, o1), o2)
```
