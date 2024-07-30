## Invoking Object Methods

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
        case _: IOException => println("Unable to write to file: ${f.getName()}")
    }
```


## Invoking Static Methods


<div style="color:gray">


We can invoke a _static_ method by writing the
`static` keyword after import:

```flix
import static java.lang.String.valueOf(Bool): String \ {};
valueOf(true)
```

</div>