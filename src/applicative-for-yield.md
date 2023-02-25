## Applicative For-Yield

> **Note:** This documentation is relevant for Flix version 0.35.0 or higher.

> **Note:** This documentation is a work in progress.

In addition to the monadic `forM` expression, Flix supports an applicative
`forA` expression that builds on the `Applicative` type class. The `forA`
construct makes it simple to write error-handling code which collects all errors
into a list. 

### Working with Validations

Here is an example of using the applicative `forA` syntax to validate user
input: 

```flix
enum Connection(String, String)

enum ValidationError {
    case InvalidUserName,
    case InvalidPassword
}

def validateUser(s: String): Validation[ValidationError, String] =
    if (12 <= String.length(s) and String.forAll(Char.isLetter, s))
        Validation.Success(s)
    else 
        Validation.Failure(Nec.singleton(InvalidUserName))

def validatePass(s: String): Validation[ValidationError, String] =
    if (12 <= String.length(s) and String.length(s) <= 20)
        Validation.Success(s)
    else 
        Validation.Failure(Nec.singleton(InvalidPassword))

def connect(u: String, p: String): Validation[ValidationError, Connection] = 
    forA (
        user <- validateUser(u);
        pass <- validatePass(p)
    ) yield Connection(user, pass) 
```
