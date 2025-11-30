# Nested and Inner Classes

Java supports nested static and non-static inner classes:

For example:

```java
package Foo.Bar;

class OuterClass {
    ...
    class InnerClass {
        ...
    }
    static class StaticInnerClass {
        public static String hello() { return "Hi"; }
    }
}
```

In Flix, we can access the `StaticInnerClass` using the `import` statement:

```flix
import Foo.Bar.{OuterClass$StaticInnerClass => Inner}

def main(): Unit \ IO = 
    println(Inner.hello())
```

A typical example is to access the `Map.Entry` class:

```flix
import java.util.{Map$Entry => Entry}
```

> **Note:** Flix does not support accessing nested non-static inner classes.
