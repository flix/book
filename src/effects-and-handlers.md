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

We can use effects and handlers to implement exceptions.

For example:

```flix
eff Throw {
    pub def throw(): Void
}

def divide(x: Int32, y: Int32): Int32 \ Throw = 
    if (y == 0) {
        do Throw.throw(); unreachable!()
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

Here we declare the effect `Throw` and use it inside `Divide`. Because of a
limitation of the Flix type system, we have to follow the call to `throw` with a
call to `unreachable!`. In `main` we perform two divisions. The first succeeds
and prints `1`. The second fails, and the error message is printed. The
continuation `_k` is unused (and in fact cannot be used because it requires an
argument of type `Void`). 



> **Note:** Only monomorphic effects are supported at this time.

## Milestones

We are currently implementing effects and handlers as a collection of work packages.

Here is the current status:

**WP1: (completed):** Add support for declaration of monomorphic effects.

**WP2: (completed):** Add support `do` and `try-with` with simplified effect type rules.

**WP3: (completed):** Add support for suspensions and resumptions.

**WP4: (in progress):** Add tests for effects and handlers.

**WP5: (in progress):** Add common effects to standard library. Proposed effects
include: (i) randomness, (ii) logging, (iii) current time, (iv) file operations,
(v) sockets (vi) http client, and more.

**WP6: (in progress):** Add support for associated effects. Update standard
library to use associated effects where appropriate. 

**WP7: (planned):** Enforce that all effects are handled within a spawn expression.

**WP8: (planned):** Enforce that all effects are handled within a new object expression.

**WP9: (planned):** Re-order compiler pipeline in the backend to make it more
robust in the presence of erasure. 

**WP10: (planned)** Compilation to efficient JVM bytecode. Proposed optimizations
include: (i) split Purity into three: Pure, Impure, ControlImpure, and use the
information to generate more compact call sites, (ii) only restore live
variables at resumption points, (iii) merge Boolean and Int8-Int32 into Int64,
and merge Float32 into Float64 in the Value class. 

**WP11: (planned)** Allow effects to declared as exceptions (i.e. non-resumable)
and use exceptions in the implementation. Integrate with Java exceptions, if
possible. 

**WP12: (planned)** Add support for polymorphic user-defined effects, e.g.
`Throw[a]`. This extension requires new research. 
