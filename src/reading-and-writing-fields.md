## Reading and Writing Fields

Flix supports reading object fields and static (class) fields with standard Java
syntax.

### Reading Object Fields

TBD

### Reading Static Fields

We can read a static field as follows:

```flix
import java.lang.Math

def area(radius: Float64): Float64 = (unsafe Math.PI) * radius * radius
```

We import the `java.lang.Math` class and then we access the static `PI` field. 

We know that the `PI` field will never change, hence we cast away the effect with `unsafe`.

### Writing Object Fields

Flix supports writing to an object field with the non-standard syntax:

```flix
import java_set_field foo.bar.Baz.boolField: Unit \ IO as setField;
let o = ...;
setField(o, false)
```

Here the `import` *expression* creates a function named `setField` which we
call. 

> **Note**: We are currently working on a more tolerable syntax.

### Writing Static Fields

Flix supports writing to a static field with the non-standard syntax:

```flix
import static java_set_field foo.bar.Baz.StaticBoolField: Unit \ IO as setField;
let o = ...;
setField(o, false)
```
> **Note**: We are currently working on a more tolerable syntax.

Here the `import` *expression* creates a function named `setField` which we
call. 