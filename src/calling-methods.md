## Invoking Object Methods

> **Note:** Requires Flix 0.49.0

In Flix, we can call methods on objects using syntax similar to Java.

For example:

```flix
import java.io.File

def main(): Unit \ IO = 
    let f = new File("foo.txt");
    println(f.getName())
```

Here we import the `java.io.File` class, instantiate a `File` object, and then
call the `getName` method on that object. 

Like with constructors, Flix resolves the method based on the number of
arguments and their types.

Here is another example:

```flix
import java.io.File

def main(): Unit \ IO = 
    let f = new File("foo.txt");
    if (f.exists())
        println("The file ${f.getName()} exists!")
    else
        println("The file ${f.getName()} does not exist!")
```

And here is a larger example:

```flix
import java.io.File
import java.io.FileWriter

def main(): Unit \ IO = 
    let f = new File("foo.txt");
    let w = new FileWriter(f);
    w.append("Hello World\n");
    w.close()
```

In the above example, we may want to catch the `IOException` that can be raised:

```flix
import java.io.File
import java.io.FileWriter
import java.io.IOException

def main(): Unit \ IO = 
    let f = new File("foo.txt");
    try {
        let w = new FileWriter(f);
        w.append("Hello World\n");
        w.close()
    } catch {
        case ex: IOException => 
            println("Unable to write to file: ${f.getName()}");
            println("The error message was: ${ex.getMessage()}")
    }
```

## Invoking Static Methods

In Flix, we can call static methods (i.e. class methods) using syntax similar to Java:

For example:

```flix
import java.lang.Math

def main(): Unit \ IO = 
    let n = Math.sin(3.14);
    println(n)

```

Like with constructors and methods, Flix resolves the static method based on the
number of arguments and their types.

Here is another example:

```flix
import java.lang.Math

def main(): Unit \ IO = 
    println(Math.abs(-123i32));
    println(Math.abs(-123i64));
    println(Math.abs(-123.456f32));
    println(Math.abs(-123.456f64))
```

## Invoking Java Methods Known to be Pure

Any Flix expression that creates a Java object, calls an object method, or calls
a static method gets the `IO` effect. This is to be expected: Java code may have
side-effects on the environment. 

In rare cases, if we know for certain that a Java method has no side-effects, we
can use an `unsafe` block to inform Flix to treat that expression as pure. 

For example:

```flix
import java.lang.Math

def pythagoras(x: Float64, y: Float64): Float64 = 
    unsafe Math.sqrt((Math.pow(x, 2.0) + Math.pow(y, 2.0)))

def main(): Unit \ IO = 
    println(pythagoras(3.0, 4.0))
```

Here we know for certain that `Math.pow` and `Math.sqrt` are _pure_ functions,
hence we can put them inside an `unsafe` block. Thus we are able to type the
Flix `pythagoras` function as pure, i.e. without the `IO` effect.

> **Warning:** Do _not_, under any circumstances, use `unsafe` on expressions
> that have side-effects. Doing so breaks the type and effect system which can
> lead to incorrect compiler optimizations which can change the meaning of your
> program in subtle or catastrophic ways! 
