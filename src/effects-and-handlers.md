## Effects and Handlers

> **Note:** The following text applies to Flix 0.54.0 or later.

Flix supports algebraic effects and handlers in the style of
[Eff](https://www.eff-lang.org/) and [Koka](https://koka-lang.github.io/). 

Flix effect handlers use dynamic scope, shallow handlers, and support multiple
resumptions.

In this section, we introduce effects and handlers, but we also recommend the
reader take a look at: 

- [An Introduction to Algebraic Effects and Handlers](https://www.eff-lang.org/handlers-tutorial.pdf) &mdash; Matija Pretnar

We begin a type of effect most programmers are familiar with: *exceptions*.

### Non-Resumable Effects: Exceptions

We can use effects and handlers to implement exceptions. For example:

```flix
eff DivByZero {
    pub def divByZero(): Void
}

def divide(x: Int32, y: Int32): Int32 \ DivByZero = 
    if (y == 0) {
        do DivByZero.divByZero()
    } else {
        x / y
    }

def main(): Unit \ IO = 
    try {
        println(divide(3, 2));
        println(divide(3, 0))
    } with DivByZero {
        def divByZero(_resume) = println("Oops: Division by Zero!")
    }
```

Here we declare the effect `DivByZero` and use it inside the `divide` function.
Hence the `divide` function has the `DivByZero` effect. In `main` we perform two
divisions. The first succeeds and prints `1`. The second fails and prints an
error message. The continuation, `_resume`, is unused and cannot be used because
its argument type is `Void`. The `main` function has the `IO` effect since we
use `println` in the handler, but it does _not_ have the `DivByZero` effect
since that has been handled.

Exceptions are non-resumable because once an exception has been raised, we
cannot resume execution from where the exception was thrown. We can only handle
the exception and do something else. We know that `DivByZero` is an exception
because its effect operation has the `Void` return type. 

> **Note:** The `Void` type is an empty, i.e., uninhabited, type built into
> Flix. A function with the return type `Void` cannot return normally; it only
> returns abnormally (e.g., by throwing an exception). Similarly, a function
> that takes an argument of type `Void` cannot be called. 

Recall that Flix supports [effect polymorphism](./effect-polymorphism.md), hence
the following works without issue:

```flix
def main(): Unit \ IO = 
    let l = List#{1, 2, 0};
    try {
        List.map(x -> println(divide(42, x)), l)
    } with DivByZero {
        def divByZero(_) = println("Oops: Division by Zero!")
    }
```

This program will print:

```
42
21
Oops: Division by Zero!
```

Because the first two calls to `divide` succeed, whereas the last call will
raise a `DivByZero` exception. Notably, the Flix type and effect system can
track the exception effect through the effect polymorphic call to `List.map`.

### Resumable Effects

Flix also supports resumable effects. For example:

```flix
import java.time.LocalDateTime

eff HourOfDay {
    pub def getCurrentHour(): Int32
}

def greeting(): String \ {HourOfDay} = 
    let h = do HourOfDay.getCurrentHour();
    if (h <= 12) 
        "Good morning"
    else if (h <= 18)
        "Good afternoon"
    else 
        "Good evening"

def main(): Unit \ IO = 
    try {
        println(greeting())
    } with HourOfDay {
        def getCurrentHour(_, resume) = 
            let dt = LocalDateTime.now();
            resume(dt.getHour())
    }
```

Here we declare an effect `HourOfDay` with a single operation that returns the
current hour of the day. Next, we define the `greeting` function which uses the
`HourOfDay` effect to return a greeting appropriate for the current time.
Lastly, in `main`, we call `greeting` and print its result. We register a
handler for `HourOfDay` which uses Java interoperability to get the current
hour.

What is important is that when the effect `getHourOfDay` is called, Flix
captures the current continuation finds the closest handler (in `main`) which
**resumes** the computation from within `greeting` using the current hour of the
day, as obtained from Java. 

### Multiple Effects and Handlers

We can use and handle multiple effects:

```flix
eff Ask {
    pub def ask(): String
}

eff Say {
    pub def say(s: String): Unit
}

def greeting(): Unit \ {Ask, Say} = 
    let name = do Ask.ask();
    do Say.say("Hello Mr. ${name}")

def main(): Unit \ IO = 
    try {
        greeting()
    } with Ask {
        def ask(_, resume) = resume("Bond, James Bond")
    } with Say {
        def say(s, resume) = { println(s); resume() }
    }
```

Here we declare two effects: `Ask` and `Say`. The `Ask` effect is a consumer: it
needs a string from the environment. The `Say` effect is a producer: it passes a
string to the environment. We use both effects in `greeting`. In `main` we call
`greeting` and handle each effect. We handle the `Ask` effect by always resuming
the continuation with the string `"Bond, James Bond"`. We handle the `Say`
effect by printing to the terminal, and then resuming the continuation.

In this case, the order of handlers does not matter, but in the general case the
order may matter. 

### Multiple Resumptions

Flix supports multiple resumptions. We can use this to implement backtracking
search, co-operative multi tasking, and more. 

Here is a simple example:

```flix
eff Amb {
    pub def flip(): Bool
}

eff Exc {
    pub def raise(m: String): Void
}

def drunkFlip(): String \ {Amb, Exc} = {
    if (do Amb.flip()) {
        let heads = do Amb.flip();
        if (heads) "heads" else "tails"
    } else {
        do Exc.raise("too drunk to flip")
    }
}

def handleAmb(f: a -> b \ ef ): a -> List[b] \ ef - Amb =  
    x -> try {
        f(x) :: Nil
    } with Amb {
        def flip(_, resume) = resume(true) ::: resume(false)
    }

def handleExc(f: a -> b \ ef): a -> Option[b] \ ef - Exc = 
    x -> try {
        Some(f(x))
    } with Exc {
        def raise(_, _) = None
    }


def main(): Unit \ IO = {
    // Prints: Some(heads) :: Some(tails) :: None :: Nil
    handleAmb(handleExc((drunkFlip)))() |> println;

    // Prints: None
    handleExc(handleAmb((drunkFlip)))() |> println
}
```

We declare two effects `Amb` (short for ambiguous) and `Exc` (short for
exception). We then define the `drunkFlip` function. The idea is to model a
drunk man trying to flip a coin. **First** we flip a coin to determine if the
man is able to flip the or if he drops it. **Second**, if the first flip was
succesful, we flip the coin again to obtain its actually value. What's important
is that `drunkFlip` conceptually has three outcomes: "heads", "tails", or "too
drunk". 

We then define two handlers `handleAmb` and `handleExc`. Starting with the
latter, the `Exc` handler simply catches the exception and returns `None`. If no
exception is raised, it returns `Some(x)` of the computed value. The `Amb`
handler handles the `flip` effect by calling the continuation **twice** with
`true` and `false`, and collecting the result in a list. In other words, the `Amb` handler explores **both** outcomes of flipping a coin. 

In `main` we use the two handlers. Notably, the *nesting order of handlers
matters*! If we handle the `Exc` effect "first" then we obtain the list
`Some(heads) :: Some(tails) :: None :: Nil`. If, on the other hand, we handle
`Exc` "last" then the whole computation fails with `None`.

### Effect Handlers and Monads

Flix supports effect handlers and [monads](./monadic-for-yield.md) because we
want to support both styles of programming: 

- If you want to program with pure data using `Option`s, `Result`s, and
  `Validation`s using monadic syntax, you can do that. 
- If you prefer to program with effect handlers, you can do that. 

Flix gives you the power to define your own applicative functors and monads, and
to use syntactic sugar for them. But Flix also gives you the power to define
your own effects and handlers, and use that instead. The choice is yours.

That said, the Flix Standard Library is biased towards using `Option`s and
`Result`s over effects. On the other hand, Flix has no built in `IO` monad, and
instead uses effects for interoperability with Java. 

### Polymorphic Effects

The Flix type and effect system does not yet support polymorphic effects.[^1] 

For example, we *cannot* declare a polymorphic `Throw[a]` effect:

```flix
eff Throw[a] {
    pub def throw(x: a): Void
}
```

the Flix compiler reports:

```
❌ -- Syntax Error --

>> Unexpected effect type parameters.

1 | eff Throw[a] {
              ^
              unexpected effect type parameters
```

Unfortunately, if we need to throw values of different types, we have to declare
different effects. 

For example:

```flix
eff ThrowBool {
    pub def throw(x: Bool): Void
}

eff ThrowInt32 {
    pub def throw(x: Int32): Void
}
```

### Control Effects in New Object and Spawn Expressions

Flix does not permit unhandled control effects in new object expressions nor in
spawn expressions. 

For example, if we write:

```flix
eff Ask {
    pub def ask(): String
}

def main(): Unit \ IO = 
    region rc {
        spawn do Ask.ask() @ rc
    }
```

The Flix compiler emits the error message:

```
-- Safety Error -------------------------------------------------- 

>> Illegal spawn effect: 'Ask'. 

>> A spawn expression must be pure or have a base effect.

7 |         spawn do Ask.ask() @ rc
                  ^^^^^^^^^^^^
                  illegal effect.
```

[^1]: We are currently working on lifting this restrction, but it requires
    further research. 