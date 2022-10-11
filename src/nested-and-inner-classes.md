## Nested and Inner Classes

[Java supports two different types of nested class](https://docs.oracle.com/javase/tutorial/java/javaOO/nested.html): static nested classes and inner classes:

```java
class OuterClass {
    ...
    class InnerClass {
        ...
    }
    static class StaticNestedClass {
        ...
    }
}
```

Although these appear superficially similar, they provide very different functionality.

Flix supports static nested classes, but does not yet support inner classes. To reference a static nested class, use a `$` instead of `.` in the class name, for example `java.util.Locale$Builder`.