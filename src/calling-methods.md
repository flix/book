## Invoking Object Methods

We can use the import mechanism to invoke methods on
objects.
For example:

```flix
import new java.io.File(String): ##java.io.File \ IO as newFile;
import java.io.File.exists(): Bool \ IO;
let f = newFile("HelloWorld.txt");
exists(f)
```

In this case the method is imported without an `as`
clause, hence its local name is simply the Java local
name: `exists`.
Note that Java methods (and fields) with names that
are illegal as Flix names must be imported with the
`as` clause using a legal Flix name.
For example, a non-idiomatic Java method may start
with an uppercase letter, whereas a Flix function
must start with a lowercase letter.

All Java operations are marked as impure since Java
is an impure language.
If you call a function which you know to be pure, you
can cast it from impure to pure, as the following
example shows:

```flix
def startsWith(prefix: {prefix = String}, s: String): Bool =
    import java.lang.String.startsWith(String): Bool \ {};
    startsWith(s, prefix.prefix)
```

We can pass arguments to methods as the following
example shows:

```flix
def charAt(i: Int32, s: String): Char =
    import java.lang.String.charAt(Int32): Char \ {};
    charAt(s, i)
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
import static java.lang.String.valueOf(Bool): String \ IO;
valueOf(true)
```

