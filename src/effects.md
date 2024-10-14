# Effect System

> **Note:** The following text applies to Flix 0.54.0 or later.

Flix features a state-of-the-art type and effect system fully integrated into
the language. The Flix effect system is powerful and extensive, supporting
effect polymorphism, sub-effecting, effect exclusion, purity reflection, and
associated effects.

We will explore these new and exciting features over the coming pages.

What are the benefits of an effect system? There are many:

<div style="color:gray">

- (**Purity**) A type and effect system helps separate pure and impure
    expressions. In Flix, a pure expression is guaranteed to be referentially
    transparent. In particular, a pure function always returns the same value
    when given the same argument(s) and cannot have any (observable)
    side-effects. A pure function can still use mutable state and mutation if
    the mutable memory can be confined to the lifetime of the function.

- (**Reasoning**) A type and effect system helps programmers reason about the
    behavior of their programs by requiring each function to specify not only
    its argument types and return type, but also its actions. 

- (**Modularity and Documentation**) A type and effect system helps enforce
    modularity by being upfront about the behavior of functions. Moreover,
    effects serve as compiler-checked documentation on the actions that a
    function can take. Effects also capture whether evaluation is eager or lazy. 

- (**Effects and Handlers**) A type and effect system is the foundation that
    enables user-defined control effects and handlers. Effects and handlers
    allow programmers to implement their own control structures, such as
    exceptions, async, and cooperative multitasking. 

- (**Security**) A type and effect system offers guarantees about the behavior
    of functions -- which can be used to ensure that untrusted code does not
    cause unwanted side-effects. For example, if a function is pure, we know
    that it cannot access the filesystem. 

- (**Compiler Optimizations**) The Flix compiler uses effect information for
    more aggressive dead code elimination and inlining. 

- (**Purity Reflection**) A type and effect system with support for [purity
    reflection](./purity-reflection.md) enables higher-order functions to
    inspect the purity of their function argument. This feature can be used to
    implement automatic parallelization, among other features. 

The Flix type and effect is quiet sophisticated and requires some knowledge to
use effectively. In the next sections, we will gradually introduce the system
and discuss how to use it. 

To start with, it is important to know that in Flix there are three types of
effects:

- [Foundational effects](./foundational-effects.md)
- [Algebraic effects and Handlers](./effects-and-handlers.md)
- [Heap effects](./mutable-data.md) (as discussed in the section on mutable)

For the integration between traits and effects, see [Associated
Effects](./associated-effects.md).
