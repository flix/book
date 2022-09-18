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

In this chapter we cover:

- [Calling Constructors](./calling-constructors.md)
- [Calling Methods](./calling-methods.md)
- [Reading and Writing Fields](./reading-and-writing-fields.md)
- [Extending Classes and Interfaces](./extending-classes-and-interfaces.md)

> **Design Note:** The Flix type system does not support sub-typing.
> Consequently, a sub-type is type incompatible with a
> super-type.
> For example, `##java.lang.String` is not compatible
> with `##java.lang.Object`.
> This limitation can be overcome by inserting explicit
> type casts.
> For example, `e as ##java.lang.Object` can be used to
> cast the type of `e` to `Object`.
