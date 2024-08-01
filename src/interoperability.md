# Interoperability with Java

Flix is a [Java Virtual Machine](https://en.wikipedia.org/wiki/Java_virtual_machine) (JVM)-based programming language,
hence:

- Flix programs compile to efficient JVM bytecode.
- Flix programs run on any Java Virtual Machine[^1].
- Flix programs can call Java code.

Flix supports most Java features necessary for interoperability:

- [Creating objects from classes](./creating-objects.md)
- [Calling methods on classes and objects](./calling-methods.md)
- [Reading and writing fields on classes and objects](./reading-and-writing-fields.md)
- [Anonymous extension of classes and interfaces](./extending-classes-and-interfaces.md)
- [Accessing inner classes](./nested-and-inner-classes.md)
- [Catching and throwing exceptions](./exceptions.md)
- [Boxing and unboxing of primitive values](./boxing-and-unboxing.md)

Thus Flix programs can reuse the Java Class Library. In addition, the Flix
package manager has Maven support. 

Flix and Java share the same base types, but they have different names, as shown
in the table:

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

[^1]: Flix requires at least Java 21.
