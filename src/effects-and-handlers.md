# Effects and Handlers

> **Warning:** Effects and handlers are an experimental feature. Do not use in
> production.

> **Warning:** Do not use effects and handlers inside new object expressions.

## Getting Started with Effects and Handlers

## Milestones

We are implementing effects and handlers in a collection of work packages.

Here is the current status:

**WP1: (completed):** Add support for declaration of monomorphic effects.

**WP2: (completed):** Add support `do` and `try-with` with simplified effect type rules.

**WP3: (completed):** Add support for suspensions and resumptions.

**WP4: (in progress):** Add tests for effects and handlers.

**WP5: (in progress):** Add common effects to standard library. Proposed effects
include: (i) randomness, (ii) logging, (iii) current time, (iv) file operations,
(v) sockets (vi) http client, and more.

**WP5: (planned):** Add tests for effects and handlers.


**WP6: (planned)** Compilation to efficient JVM bytecode. Proposed optimizations
include: (i) split Purity into three: Pure, Impure, ControlImpure, and use the
information to generate more compact call sites, (ii) only restore live
variables at resumption points, (iii) merge Boolean and Int8-Int32 into Int64,
and merge Float32 into Float64 in the Value class. 

**WP7: (planned)** Allow effects to declared as exceptions (i.e. non-resumable)
and use exceptions in the implementation. Integrate with Java exceptions, if
possible. 

