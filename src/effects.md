# Effect System

> **Note:** The following text applies to Flix 0.54.0 or later.

Flix features a state-of-the-art type and effect system fully integrated into
the language. The Flix effect system is powerful and extensive, supporting
effect polymorphism, sub-effecting, effect exclusion, purity reflection, and
associated effects.

We will explore these new and exciting features over the coming pages.

What are the benefits of an effect system? There are many:

- **(Purity)** A type and effect system separates pure and impure functions. In
  Flix, a pure function cannot have any side-effects and must return the same
  value when given the same arguments. Nevertheless, a pure function can still
  be implemented in an imperative style using mutable data structures as long as
  those data structures leave scope when the function ends.

- **(Reasoning)** A type and effect system helps programmers understand how
  their programs work by requiring every function to specify its argument and
  return types, as well as the side-effects of the function.

- **(Modularity)**  A type and effect system enforces modularity by forcing
  programmers to consider what side effects are allowed where in the program.
  Moreover, effects &mdash; like types &mdash; serve as compiler checked
  documentation.

- **(Effects and Handlers)** A type and effect system is the foundation for
  algebraic effects and handlers. These allow programmers to implement their own
  control structures, such as exceptions, async/await, and cooperative
  multitasking.

- **(Security)** A type and effect system offers iron-clad guarantees about the
  behavior of functions, allowing programmers to increase their trust in unknown
  code. For example, if a function is pure, it cannot have any side-effects: it
  cannot access the file system, the network, etc. A specific benefit is that
  programs become more resistant to supply chain attacks.

- **(Purity Reflection)** The Flix Standard Library (and other library authors
  in extension) can use [purity reflection](./purity-reflection.md) to inspect
  the purity of function arguments passed to higher-order functions. We can
  exploit this information to implement automatic parallelization while
  preserving the original semantics of the program. For example, in Flix, the
  `Set.count` function uses parallel evaluation if (a) the set is sufficiently
  large and (b) the passed predicate function is pure. 

- **(Optimizations)** The Flix compiler exploits purity information for
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
