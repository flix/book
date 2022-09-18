# Interoperability

Flix supports interoperability with Java. 

This includes support for:

- [Calling Constructors](./calling-constructors.md)
- [Calling Methods](./calling-methods.md)
- [Reading and Writing Fields](./reading-and-writing-fields.md)
- [Classes and Interfaces](./extending-classes-and-interfaces.md)

> **Design Note:** The Flix type system does not support sub-typing.
> Consequently, a sub-type is type incompatible with a
> super-type.
> For example, `java.lang.String` is not compatible
> with `java.lang.Object`.
> This limitation can be overcome by inserting [upcasts](./upcast.md).
