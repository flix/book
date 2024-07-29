## Creating Objects

In Flix, we can create objects using syntax similar to Java.

For example:

```flix
import java.io.File

def main(): Unit \ IO = 
    let f = new File("foo.txt");
    println("Hello World!")
```

Here we import the `java.io.File` class and instantiate a `File` object by
calling one of its constructor using the `new` keyword. 

The `File` class has multiple constructors, so we can also write:

```flix
import java.io.File

def main(): Unit \ IO = 
    let f1 = new File("foo.txt");
    let f2 = new File("bar", "foo.txt");
    println("Hello World!")
```

Flix resolves the constructor based on the number of arguments and their types.

As a final example, we can write:

```flix
import java.io.File
import java.net.URI

def main(): Unit \ IO = 
    let f1 = new File("foo.txt");
    let f2 = new File("bar", "foo.txt");
    let f3 = new File(new URI("file://foo.txt"));
    println("Hello World!")
```

We can use a _renaming import_ to resolve a clash between a Java name and a Flix
module: 

```flix
import java.lang.{String => JString}

def main(): Unit \ IO = 
    let s = new JString("Hello World");
    println("Hello World!")
```

Here `JString` refers to the Java class `java.lang.String` whereas `String`
refers to the Flix module. Note that internally Flix and Java strings are the
same. 

> **Note:** In Flix, Java classes must be `import`ed before they can be used.
> Specifically, we _cannot_ write `new java.io.File(...)`.
