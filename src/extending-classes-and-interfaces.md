## Extending Classes and Interfaces

Flix allows you to create objects that extend a class or interface.
For example, we can create a new object that implements the
`java.io.Closeable` interface as follows:

```flix
import java.io.Closeable

def newClosable(): Closeable \ IO = new Closeable {
    def close(_this: Closeable): Unit = ()
}
```

We can also extend classes. For example, we can create a
`java.lang.Object` where we override the `toString` method:

```flix
import java.lang.Object

def newObject(): Object \ IO = new Object {
    def toString(_this: Object): String = "Hello World!"
}
```
