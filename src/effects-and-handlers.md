## Effects and Handlers

> **Note:** User-defined effects and handlers requires Flix 0.53.0

Flix supports user-defined control effects and handlers in the style of
[Eff](https://www.eff-lang.org/) and [Koka](https://koka-lang.github.io/). 

Flix effect handlers use dynamic scope, shallow handlers, and support multiple
resumptions.

We gradually introduce effects and handlers, but we recommend the reader also
take a look at: 

- [An Introduction to Algebraic Effects and Handlers](https://www.eff-lang.org/handlers-tutorial.pdf) &mdash; Matija Pretnar

We begin an effect most programmers are familiar with: *exceptions*.

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
        def divByZero(_k) = println("Oops: Division by Zero!")
    }
```

Here we declare the effect `DivByZero` and use it inside the `divide` function.
In `main` we perform two divisions. The first succeeds and prints `1`. The
second fails and the error message is printed. The continuation `_k` is unused
(and in fact cannot be used because it requires an argument of type `Void`). The
`main` function has the `IO` effect since we use `println` in the handler, but
it does _not_ have the `DivByZero` effect since that has been handled.

> **Note:** `Void` is an empty (uninhabited) type built-in to Flix. The `Void`
> type, in combination with an effect operation, can be used everywhere a normal
> type is required. But notably a function, e.g. a continuation, which requires
> an argument of type `Void` cannot be called. 

Recall that Flix supports [effect polymorphism](./effect-polymorphism.md), hence
the following works without issue:

```flix
def main(): Unit \ IO = 
    let l = List#{3, 2, 1, 0};
    try {
        List.map(x -> divide(42, x), l) |> println
    } with DivByZero {
        def divByZero(_k) = println("Oops: Division by Zero!")
    }
```

Here we map over the list `List#{3, 2, 1, 0}`. The last call to `divide` will
raise a `DivByZero` exception, hence the program prints `Oops: Division by
Zero!` and nothing else. Importantly, the `DivByZero` effect is precisely
tracked through the effect polymorphic call to `List.map`. 

<div style="color:gray">

### Resumable Effects

We can also implement resumable effects. For example:

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
        try greeting() with Ask {
            def ask(k) = k("Bond, James Bond")
        }
    } with Say {
        def say(s, k) = { println(s); k() }
    }
```

Here we declare two effects: `Ask` and `Say`. We use both effects in `greeting`.
In `main` we call `greeting` and handle each effect. We handle the `Ask` effect
by always resuming the continuation with the string `"Bond, James Bond"`. We
handle the `Say` effect by printing to the terminal, and then resuming the
continuation.

In this case, the order of handlers does not matter, but in the general case the
order may matter. 

</div>

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