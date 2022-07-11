# Interoperability

Flix supports interoperability with Java libraries
through imports.
The `import` construct allows a Java constructor,
method, or field to be exposed as an impure Flix
function.

The `import` mechanism should not be confused with
the `use` mechanism.
The former enables interoperability with Java,
whereas the latter is part of the Flix
[namespace](./namespaces.md) mechanism.

## Creating Objects

We can use imports to retrieve the constructor of a
Java class and then call its associated function to
construct a new Java object.
For example:

```flix
import new java.io.File(String): ##java.io.File & Impure as newFile;
newFile("HelloWorld.txt")
```

Here we import the constructor of the `java.io.File`
class and give it the local name `newFile`.
The `newFile` function takes a string argument and
returns a fresh Java `File` object.
Constructing a fresh object is impure, hence `main`
is marked as `Impure`.

The type of the File object is written as
`##java.io.File` where the two hashes `##` designate
that it is a Java type.
Notice that this is how the return type is specified.

A common trick is to use a type alias to make it
easier to work with Java types.
For example:

```flix
type alias File = ##java.io.File

def openFile(s: String): File & Impure =
    import new java.io.File(String): File & Impure as newFile;
    newFile(s)
```

The type alias can then be used to specify the return
type of both `openFile` and
`new java.io.File(String)`.

The `java.io.File` class has another constructor that
takes two arguments: one for parent pathname and one
for the child pathname.
We can use this constructor as follows:

```flix
import new java.io.File(String, String): ##java.io.File & Impure as newFile;
newFile("foo", "HelloWorld.txt")
```

The import describes the signature of the
constructor.
We can use this to import any constructor (or
method), even if the constructor (or method) is
overloaded, as in the above example.
The return type is always part of the constructor (or
method) signature.

## Invoking Object Methods

We can use the import mechanism to invoke methods on
objects.
For example:

```flix
import new java.io.File(String): ##java.io.File & Impure as newFile;
import java.io.File.exists(): Bool & Impure;
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
def startsWith(prefix: {prefix :: String}, s: String): Bool =
    import java.lang.String.startsWith(String): Bool & Pure;
    startsWith(s, prefix.prefix)
```

We can pass arguments to methods as the following
example shows:

```flix
def charAt(i: Int32, s: String): Char =
    import java.lang.String.charAt(Int32): Char & Pure;
    charAt(s, i)
```

Type signatures should use Flix type names and not
Java type names for primitive types.
For example, if a Java method takes a `Double` its
signature should use the Flix type `Float64`.
Similarly, if a Java method takes a `Boolean` its
signature should use the Flix type `Bool`.
This goes for return types, too.

## Reading Object Fields

Reading a field of an object is straightforward:

```flix
import new flix.test.TestClass(): ##flix.test.TestClass & Impure as newObject;
import get flix.test.TestClass.boolField: Bool & Impure as getField;
let o = newObject();
getField(o)
```

Here we assume that `TestClass` is a Java class with
an instance field named `boolField` of type `Bool`.

## Writing Object Fields

Writing a field of an object is also straightforward:

```flix
import new flix.test.TestClass(): ##flix.test.TestClass & Impure as newObject;
import get flix.test.TestClass.boolField: Bool & Impure as getField;
import set flix.test.TestClass.boolField: Unit & Impure as setField;
let o = newObject();
setField(o, false);
getField(o)
```

## Invoking Static Methods

We can invoke a *static* method by writing the
`static` keyword after import:

```flix
import static java.lang.String.valueOf(Bool): String & Impure;
valueOf(true)
```

## Reading and Writing Static Fields

Reading or writing *static* fields is similar to
reading or writing object fields.
For example:

```flix
import static get java.lang.Integer.MIN_VALUE: Int32 & Impure as getMinValue;
getMinValue()
```

As above, the only difference is to write the
`static` keyword to indicate that the reference is to
a static field.

## Summary

The table below gives an overview of the syntax.

Note: the return types and effects must always be
specifed but are omitted for a simpler overview.

| Import           | Syntax                                      |
|:----------------:|:-------------------------------------------:|
| Constructor      | `import new Foo.Bar.Baz(...)`               |
| Object Method    | `import Foo.Bar.baz(...) [as name]`         |
| Static Method    | `import static Foo.Bar.baz(...) [as name]`  |
| Get Object Field | `import get Foo.Bar.baz as getValue`        |
| Set Object Field | `import set Foo.Bar.baz as setValue`        |
| Get Static Field | `import static get Foo.Bar.baz as getValue` |
| Set Static Field | `import static set Foo.Bar.baz as setValue` |

## Limitations

Flix does not currently support any of the following
features:

- Defining new classes (or interfaces).
- Defining new anonymous classes (e.g. to implement a
  Java interface).

If any of these features are needed, we recommend
that you write a small Java wrapper.

## Design Note

The import mechanism is only supported at the
expression level: it is not currently possible to
import Java constructors, methods, and fields at the
top-level.

## Design Note

The Flix type system does not support sub-typing.
Consequently, a sub-type is type incompatible with a
super-type.
For example, `##java.lang.String` is not compatible
with `##java.lang.Object`.
This limitation can be overcome by inserting explicit
type casts.
For example, `e as ##java.lang.Object` can be used to
cast the type of `e` to `Object`.

## Warning

The Flix compiler does not support any kind of
cross-compilation (e.g. compiling Java sources
together with Flix sources).
Furthermore, the format of the JVM bytecode generated
by the Flix compiler is not yet stable.
If you write a library in Flix and use it from Java,
you should be prepared for breakages with future
versions of the Flix compiler.
