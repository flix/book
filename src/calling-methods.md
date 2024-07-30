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

