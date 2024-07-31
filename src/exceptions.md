## Exceptions

> **Note:** Requires Flix 0.49.0

In Flix, we can catch Java exceptions using the `try-catch` construct. The
construct is similar to the one in Java, but the syntax is slightly different. 

For example: 

```flix
import java.io.BufferedReader
import java.io.File
import java.io.FileReader
import java.io.FileNotFoundException
import java.io.IOException

def main(): Unit \ IO = 
    let f = new File("foo.txt");
    try {
        let r = new BufferedReader(new FileReader(f));
        let l = r.readLine();
        println("The first line of the file is: ${l}");
        r.close()
    } catch {
        case _: FileNotFoundException => 
            println("The file does not exist!")
        case ex: IOException => 
            println("The file could not be read!");
            println("The error message was: ${ex.getMessage()}")
    }
```

Here the calls `new FileReader()`, `r.readLine()`, and `r.close()` can throw
`IOException`s. We use a `try-catch` block to catch these exceptions. We add a
special case for the `FileNotFoundException` exception. 

> **Note:** Flix programs should not use exceptions: it is considered bad style.
> Instead, programs should use the `Result[e, t]` type. The `try-catch`
> construct should only be used on the boundary between Flix and Java code. 

> **Note:** Flix does not (yet) support a `finally` block.

> **Note:** Flix does not (yet) support throwing Java exceptions. 

> **Note:** In Flix a function can contain at most one `try-catch` block.
