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

<div style="color:black">

- (**Security**) A type and effect system offers iron-clad guarantees about the
  behavior of functions, allowing programmers to increase their trust in unknown
  code. For example, if a function is pure, it cannot have any side-effects: it
  cannot access the file system, the network, etc. A specific benefit is that
  programs become more resistant to supply chain attacks.

- (**Purity Reflection**) The Flix Standard Library (and other library authors
  in extension) can use [purity reflection](./purity-reflection.md) to inspect
  the purity of function arguments passed to higher-order functions. We can
  exploit this information to implement automatic parallelization while
  preserving the original semantics of the program. For example, in Flix, the
  `Set.count` function uses parallel evaluation if (a) the set is sufficiently
  large and (b) the passed predicate function is pure. 

- (**Optimizations**) The Flix compiler exploits purity information for
  aggressive dead code elimination and inlining.


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
