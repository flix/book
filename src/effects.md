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

- (**Purity Reflection**) A type and effect system with support for [purity
    reflection](./purity-reflection.md) enables higher-order functions to
    inspect the purity of their function argument. This feature can be used to
    implement automatic parallelization, among other features. 

- (**Compiler Optimizations**) The Flix compiler uses effect information for
    more aggressive dead code elimination and inlining. 

<div style="color:black">

The Flix type and effect system is quite sophisticated and requires some
background knowledge to use effectively. In the next couple of sections, we
gradually introduce the features of the type and effect system and give several
examples of its use. 

To start, it is important to understand that Flix has three types of effects: 

- [foundational effects](./foundational-effects.md)
- [algebraic effects](./effects-and-handlers.md)
- [heap effects](./mutable-data.md)

We describe how traits and effects interact in the section on [Associated
Effects](./associated-effects.md).
