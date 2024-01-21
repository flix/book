# Effects and Handlers

> **Warning:** Effects and handlers are an experimental feature. Do not use them
> in production.

> **Warning:** Do not use effects and handlers inside spawn expressions.

> **Warning:** Do not use effects and handlers inside new object expressions.

> **Warning:** Typing of user-defined effects, in the presence of effect
> polymorpism, is incomplete. In other words, programs may pass the type
> checker, but crash at runtime (or perhaps crash the compiler during code
> generation). 

## Getting Started with Effects and Handlers

### Exceptions

We can use effects and handlers to implement exceptions. For example:

```flix
eff Throw {
    pub def throw(): Void
}

def divide(x: Int32, y: Int32): Int32 \ Throw = 
    if (y == 0) {
        do Throw.throw()
    } else {
        x / y
    }

def main(): Unit \ IO = 
    try {
        println(divide(3, 2));
        println(divide(3, 0))
    } with Throw {
        def throw(_k) = println("Oops: Division by Zero!")
    }
```

Here we declare the effect `Throw` and use it inside `Divide`. In `main` we
perform two divisions. The first succeeds and prints `1`. The second fails, and
the error message is printed. The continuation `_k` is unused (and in fact
cannot be used because it requires an argument of type `Void`). 

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
In `main` we call `greeting` and register a handler for each effect. We handle
the `Ask` effect by always resuming the continuation with `Bond, James Bond`.
We handle the `Say` effect by printing to the terminal, and then resuming the
continuation.

> **Note:** Only monomorphic effects are supported at this time.

## Milestones

We are currently implementing effects and handlers as a collection of work packages.

Here is the current status:

**WP1: (completed):** Add support for declaration of monomorphic effects.

**WP2: (completed):** Add support `do` and `try-with` with simplified effect type rules.

**WP3: (completed):** Add support for suspensions and resumptions.

**WP4: (completed):** Add special type rule for `do` and for `Void` to support
the exception use case.

**WP5: (in progress):** Add tests for effects and handlers.

**WP6: (in progress):** Add some common effects to standard library. Proposed effects
include: (i) randomness, (ii) logging, and (iii) time.

**WP7: (in progress):** Add support for associated effects. Update standard
library to use associated effects where appropriate. 

**WP8: (in progress):** Re-order compiler pipeline in the backend to make it
more robust in the presence of erasure. 

**WP9: (planned):** Enforce that all effects are handled within a spawn expression.

**WP10: (planned):** Enforce that all effects are handled within a new object expression.

**WP11: (planned):** Upgrade the effect system to work in the Boolean algebra of
sets, instead of the algebra of Boolean formulas. 

**WP12: (planned)** Compilation to efficient JVM bytecode. Proposed optimizations
include: (i) split Purity into three: Pure, Impure, ControlImpure, and use the
information to generate more compact call sites, (ii) only restore live
variables at resumption points, (iii) merge Boolean and Int8-Int32 into Int64,
and merge Float32 into Float64 in the Value class. 

**WP13: (planned)** Allow effects to declared as exceptions (i.e. non-resumable)
and use exceptions in the implementation. Integrate with Java exceptions, if
possible. 

**WP14: (planned)** Add support for polymorphic user-defined effects, e.g.
`Throw[a]`. This extension requires new research. 

## Effect System Limitations

The Flix effect system currently has some limitations. We are working on improving
these.

### Mixing User-Defined Effects and IO

The Flix effect system does not yet enforce that all effects are handled, if
user-defined effects are mixed with the built-on `IO` effect. For example: 

```flix
eff Ask {
    pub def ask(): String
}

def main(): Unit \ IO = 
    do Ask.ask();
    println("Hello World!")
```

The recommendation is to avoid mixing user-defined effects and `IO`.

### Spawn

The Flix effect system does not yet enforce that all effects are handled in spawn.

For example, the program below will compile, but crash at runtime:

```flix
eff Ask {
    pub def ask(): String
}

def main(): Unit \ IO = 
    region rc {
        spawn do Ask.ask() @ rc
    }
```

### New Object Expressions

The Flix effect system does not yet enforce that all effects are handled in new object expressions.

For example, the program below will compile, but crash at runtime:

```flix
import java.lang.Runnable

eff Ask {
    pub def ask(): String
}

def newRunnable(): Runnable \ IO = new Runnable {
    def run(_this: Runnable): Unit \ IO = 
        do Ask.ask(); ()
}

def main(): Unit \ IO = 
    import java.lang.Runnable.run(): Unit \ IO;
    let r = newRunnable();
    run(r)

```
