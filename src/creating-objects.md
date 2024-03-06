## Creating Objects

We can import the constructor of a Java class as a
Flix function and use it to construct new objects.

For example:

```flix
import java_new java.io.File(String): ##java.io.File \ IO as newFile;
newFile("HelloWorld.txt")
```

Here we import the constructor of the `java.io.File`
class and give it the local name `newFile`.
The `newFile` function takes a string argument and
returns a fresh Java `File` object.
Constructing a fresh object is impure, hence `main`
is marked as having the `IO` effect.

When we import a constructor, we must specify the
types of its formal parameters. This is required because
Java supports constructor overloading (i.e. a class may
have multiple constructors only distinguished by their
formal parameters.)

For example, the `java.io.File` class has another
constructor that takes two arguments: one for the parent
pathname and one for the child pathname.
We can use this constructor as follows:

```flix
import java_new java.io.File(String, String): ##java.io.File \ IO as newFile;
newFile("foo", "HelloWorld.txt")
```

Here the import describes that the constructor expects two
`String` arguments.

> **Note:** `import` statements must occur at the expression-level,
> i.e. they must occur inside a function. Unlike `use` declarations,
> they cannot occur at top of a module.
