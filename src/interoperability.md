# Interoperability with Java

Flix programs compile to Java bytecode,
run on the Java Virtual Machine (JVM), and 
can interoperate with Java code.

In particular, Flix has support for most Java features, including:

- [Calling Constructors](./calling-constructors.md)
- [Calling Methods](./calling-methods.md)
- [Reading and Writing Fields](./reading-and-writing-fields.md)
- [Classes and Interfaces](./extending-classes-and-interfaces.md)

> **Design Note:** The Flix type system does not support sub-typing.
> Consequently, a type is not compatible with its super-type.
> For example, `java.lang.String` is incompatible
> with `java.lang.Object`. 
> Fortunately, this limitation can be overcome by using [upcasts](./upcast.md).
