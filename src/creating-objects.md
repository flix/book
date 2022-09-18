## Calling Constructors

We can use imports to retrieve the constructor of a
Java class and then call its associated function to
construct a new Java object.
For example:

```flix
import new java.io.File(String): ##java.io.File \ IO as newFile;
newFile("HelloWorld.txt")
```

Here we import the constructor of the `java.io.File`
class and give it the local name `newFile`.
The `newFile` function takes a string argument and
returns a fresh Java `File` object.
Constructing a fresh object is impure, hence `main`
is marked as `Impure` with annotation `\ IO`.

The type of the File object is written as
`##java.io.File` where the two hashes `##` designate
that it is a Java type.
Notice that this is how the return type is specified.

The `java.io.File` class has another constructor that
takes two arguments: one for parent pathname and one
for the child pathname.
We can use this constructor as follows:

```flix
import new java.io.File(String, String): ##java.io.File \ IO as newFile;
newFile("foo", "HelloWorld.txt")
```

The import describes the signature of the
constructor.
We can use this to import any constructor (or
method), even if the constructor (or method) is
overloaded, as in the above example.
The return type is always part of the constructor (or
method) signature.
