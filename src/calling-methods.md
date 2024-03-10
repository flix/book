## Invoking Object Methods

We can use the import mechanism to invoke methods on objects.

For example:

```flix
import java_new java.io.File(String): ##java.io.File \ IO as newFile;
import java.io.File.exists(): Bool \ IO as fileExists;
let f = newFile("HelloWorld.txt");
fileExists(f)
```

Here we import the `java.io.File.exists` method under the name `fileExists`.

If the Java method name is a legal Flix name and we want to reuse it,
we can also import the method without an `as` clause. For example:

```flix
import java_new java.io.File(String): ##java.io.File \ IO as newFile;
import java.io.File.exists(): Bool \ IO;
let f = newFile("HelloWorld.txt");
exists(f)
```

Here we import the method under the name `exists`.

When a Java method is imported, we must annotate it with its effect.
Most commonly, a Java method has a side-effect (such as deleting a file),
and hence must be annotated with the `IO` effect.

In rare cases where a method is pure, we can import it as such by
writing the empty effect set: `{}`. For example:

```flix
import java.lang.String.startsWith(String): Bool \ {};
startsWith("Hello World", "Hello")
```

And as another example:

```flix
import java.lang.String.charAt(Int32): Char \ {};
charAt("Hello World", 2)
```

Type signatures should use Flix type names and not
Java type names for primitive types.
For example, if a Java method takes a `Double` its
signature should use the Flix type `Float64`.
Similarly, if a Java method takes a `Boolean` its
signature should use the Flix type `Bool`.
This goes for return types, too.

## Invoking Static Methods

We can invoke a _static_ method by writing the
`static` keyword after import:

```flix
import static java.lang.String.valueOf(Bool): String \ {};
valueOf(true)
```

