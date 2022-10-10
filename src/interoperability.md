# Interoperability with Java

Flix is [Java Virtual Machine](https://en.wikipedia.org/wiki/Java_virtual_machine) (JVM)-based programming language,
hence:

- Flix programs compile to efficient JVM bytecode.
- Flix programs run on any Java Virtual Machine[^1].
- Flix programs can call Java code.

Flix supports most Java features necessary for interoperability:

- [Creating objects from existing classes](./creating-objects.md)
- [Calling methods on classes and objects](./calling-methods.md)
- [Reading and writing fields on objects](./reading-and-writing-fields.md)
- [Anonymous extension of classes and interfaces](./extending-classes-and-interfaces.md)
- [Nested and inner classes](./nested-and-inner-classes.md)

Thus Flix programs can reuse Java Class Library and have access to the Java ecosystem.

Flix and Java share the same base types, in particular:

| Flix Type | Java Type |
|-----------|-----------|
| Bool      | boolean   |
| Char      | char      |
| Float32   | float     |
| Float64   | double    |
| Int8      | byte      |
| Int16     | short     |
| Int32     | int       |
| Int64     | long      |
| String    | String    |

In Flix primitive types are always unboxed.
Hence, to call a Java method that expects a `java.lang.Integer`,
if you have a Flix `Int32`, it must be boxed by calling `java.lang.Integer.valueOf`.

> **Design Note:** Unlike other programming languages that target the JVM,
> Flix does not aim to embed the Java type system within Flix.
> Instead, Flix sacrifices some convenience to stay true to its design goals.
> In particular, the Flix type system does not support sub-typing.
> Consequently, unlike in Java, a sub-type cannot be used where its super-type is expected.
> For example, `java.lang.String` is incompatible with `java.lang.Object`.
> Fortunately, this limitation can be overcome by using [upcasts](./upcast.md).

[^1]: Flix currently targets Java 11. Once Project Loom is released, we will target that version.
