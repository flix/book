## Boxing and Unboxing

> **Note:** Requires Flix 0.49.0

Unlike Java, Flix never performs implicit boxing or unboxing of values. We
believe auto boxing is a design flaw and do not plan to support it. 

Consequently, you must explicitly box and unbox values as needed.

### Boxing

The following example shows how to manually box a Java `Integer`: 

```flix
import java.lang.Integer
import java.util.Objects

def hash(x: Int32): Int32 = unsafe {
        let boxed = Integer.valueOf(x);
        Objects.hashCode(boxed)
    }
```

We must use `unsafe` to cast away the `IO` effect from the call to
`Integer.valueOf()` and `Objects.hashCode()`.


### Unboxing

The following example shows how to manually unbox two Java `Integer`s:

```flix
import java.lang.Integer

def sum(x: Integer, y: Integer): Int32 = 
    unsafe x.intValue() + y.intValue()
```

We must use `unsafe` to cast away the `IO` effect from the call to `intValue()`.

