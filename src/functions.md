# Functions and Higher-Order Functions

Functions and higher-order functions are the key
building block of a functional programming language.

In Flix, top-level functions are defined with the
`def` keyword.
For example:

```flix
def add(x: Int32, y: Int32): Int32 = x + y + 1
```

A definition consists of the function name followed
by an argument list, the return type, and the
function body. Although Flix supports type
inference, top-level function definitions must
declare the type of their arguments and their return
type.

In Flix, all function arguments and local variables
must be used. If a function argument is not used
it must be prefixed with an underscore to explicitly
mark it as unused.
