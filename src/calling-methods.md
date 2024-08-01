## Invoking Object Methods

> **Note:** Requires Flix 0.49.0

In Flix, we can call methods on Java objects using syntax similar to Java.

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

## Callings Methods with VarArgs

TBD

## When Constructor or Method Resolution Fails

In some cases the Flix compiler is unable to determine what Java constructor or
method is called.

For example, in the program:

```flix
import java.lang.{String => JString}

def f(): String \ IO = 
    let o = ???;
    JString.valueOf(o)
```

The type of `o` is unknown, hence Flix cannot know if we want to call
`String.valueOf(boolean)`, `String.valueOf(char)`, `String.valueOf(double)`, or
one of the other overloaded versions. 

The solution is to put a type ascription on the relevant argument: 

```flix
import java.lang.{String => JString}

def f(): String \ IO = 
    let o = ???;
    JString.valueOf((o: Bool))
```

The type ascription specifies that `o` has type `Bool` which allows method
resolution to complete successfully. Note that the extra pair of parenthesis is
required. 

## Invoking Object Methods through Static Fields

We may want to write:

```flix
import java.lang.System

def main(): Unit \ IO = 
    System.out.println("Hello World!")
```

But due to a limitation of the Flix parser, the above has to be written as:

```flix
import java.lang.System

def main(): Unit \ IO = 
    (System.out).println("Hello World!")
```

## Invoking Java Methods Known to be Pure

Any Flix expression that creates a Java object, calls a Java method, or calls a
Java static method has the `IO` effect. This is to be expected: Java
constructors and methods may have arbitrary side-effects. 

If we know for certain that a Java constructor or method invocation has no
side-effects, we can use an `unsafe` block to tell Flix to treat that expression
as pure. 

For example:

```flix
import java.lang.Math

def pythagoras(x: Float64, y: Float64): Float64 = // Pure, no IO effect
    unsafe Math.sqrt((Math.pow(x, 2.0) + Math.pow(y, 2.0)))

def main(): Unit \ IO = 
    println(pythagoras(3.0, 4.0))
```

Here we know for certain that `Math.pow` and `Math.sqrt` are _pure_ functions,
hence we can put them inside an `unsafe` block. Thus we are able to type check
the Flix `pythagoras` function as pure, i.e. without the `IO` effect.

> **Warning:** Do not, under any circumstances, use `unsafe` on expressions that
> have side-effects. Doing so breaks the type and effect system which can lead
> to incorrect compiler optimizations which can change the meaning of your
> program in subtle or catastrophic ways! 

## Partial Application of Java Constructors and Methods

Flix supports partial application of Flix functions. However, Java constructors
and methods can never be partially applied. This limitation can be overcome
introducing an explicit lambda.

For example:

```flix
import java.lang.{String => JString}

def main(): Unit \ IO = 
    def replaceAll(s, src, dst) = s.replaceAll(src, dst);
    let f = replaceAll("Hello World");
    let s1 = f("World")("Galaxy");
    let s2 = f("World")("Universe");
    println(s1);
    println(s2)
```

Here we introduce a Flix function `replaceAll` which calls `String.replaceAll`.
Since `replaceAll` is a Flix function, we can partially apply it as shown in the
example. 
