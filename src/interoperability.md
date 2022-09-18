# Interoperability with Java

Flix is [Java Virtual Machine](https://en.wikipedia.org/wiki/Java_virtual_machine) (JVM)-based programming language,
hence:

- Flix programs compile to efficient JVM bytecode.
- Flix programs run on any Java Virtual Machine[^1] .
- Flix programs can call into Java code.

Flix supports most Java features necessary for interoperability:

- [Creating objects from existing classes](./creating-objects.md)
- [Calling methods on classes and objects](./calling-methods.md)
- [Reading and writing fields on objects](./reading-and-writing-fields.md)
- [Anonymous extension of classes and interfaces](./extending-classes-and-interfaces.md)

Thus Flix programs have access to the entire Java Class Library and to the Java ecosystem.

> **Design Note:** Unlike other programming languages that target the JVM,
> Flix does not aim to embed the Java type system within Flix.
> Instead, Flix sacrifices some convenience to stay true to its design goals.
> In particular, the Flix type system does not support sub-typing.
> Consequently, unlike in Java, a sub-type cannot be used where its super-type is expected.
> For example, `java.lang.String` is incompatible with `java.lang.Object`.
> Fortunately, this limitation can be overcome by using [upcasts](./upcast.md).

[^1]: Flix currently targets Java 11.
