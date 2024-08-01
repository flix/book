## Boxing and Unboxing

> **Note:** Requires Flix 0.49.0

Unlike Java, Flix never performs implicit boxing or unboxing of values. 

We believe auto boxing is a design flaw and do not plan to support it. Hence,
primitive values must be manually boxed and unboxed. 

### Boxing

The following example shows how to box a primitive integer:

```flix
def f(x: Int32): String \ IO = 
    let i = Box.box(x); // Integer
    i.toString()
```

Here the call to `Box.box(x)` returns an `Integer` object. Since `i` is an
object, we can call `toString` on it. Boxing is a pure operation, but calling
`toString` has the `IO` effect. 

### Unboxing

The following example shows how to unbox two Java `Integer` objects:

```flix
import java.lang.Integer

def sum(x: Integer, y: Integer): Int32 = 
    Box.unbox(x) + Box.unbox(y)
```

Here the call to `Box.unbox` returns an `Int32` primitive value. 

Unboxing is a pure operation.
