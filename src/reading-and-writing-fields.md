# Reading and Writing Fields

Flix supports reading object fields and static (class) fields with standard Java
syntax.

## Reading Object Fields

We can read an object field as follows:

```flix
import java.awt.Point

def area(p: Point): Int32 \ IO = p.x * p.y
```

## Reading Static Fields

We can read a static field as follows:

```flix
import java.lang.Math

def area(radius: Float64): Float64 = (unsafe Math.PI) * radius * radius
```

We import the `java.lang.Math` class and then we access the static `PI` field. 

We know that the `PI` field will never change, hence we cast away the effect with `unsafe`.
