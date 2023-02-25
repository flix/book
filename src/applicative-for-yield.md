## Applicative For-Yield

> **Note:** This documentation is relevant for Flix version 0.35.0 or higher.

> **Note:** This documentation is a work in progress.

In addition to the monadic `forM` expression, Flix supports an applicative
`forA` expression that builds on the `Applicative` type class. The `forA`
construct makes it simple to write error-handling code which uses the
`Validated[e, t]` data type. 

### Working with Validations

For example, we can use the `forA` expression to validate user input while
aggregating all errors into a `List[e]` (technically a `Chain[e]`).

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
        Validation.Failure(Nec.singleton(InvalidUserName))

def validatePass(s: String): Validation[InvalidInput, String] =
    if (12 <= String.length(s) and String.length(s) <= 20)
        Validation.Success(s)
    else 
        Validation.Failure(Nec.singleton(InvalidPassword))

def connect(u: String, p: String): Validation[InvalidInput, Connection] = 
    forA (
        user <- validateUser(u);
        pass <- validatePass(p)
    ) yield Connection(user, pass) 

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
