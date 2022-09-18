## Classes and Interfaces

Flix allows us to create objects that extend a class or implements an interface.

This feature is conceptually similar to Java [Anonymous Classes](https://docs.oracle.com/javase/tutorial/java/javaOO/anonymousclasses.html). 
That is, we can define an unnamed class that implements an interface or extends a class, and then construct an object of that class. All in one go. 

For example, we can create an object that implements the `java.lang.Runnable` interface:

```flix
import java.lang.Runnable

def newRunnable(): Runnable \ IO = new Runnable {
    def run(_this: Runnable): Unit \ IO = 
        println("I am running!")
}
```

Every time we call `newRunnable` we get a *new* object that implements `java.lang.Runnable`.

As another example, we can create an object that implements the `java.io.Closeable` interface:

```flix
import java.io.Closeable

def newClosable(): Closeable \ IO = new Closeable {
    def close(_this: Closeable): Unit \ IO = 
        println("I am closing!")
}
```

We can also extend classes. For example, we can create a
`java.lang.Object` where we override the `hashCode` and `toString` methods:

```flix
def newObject(): Object \ IO = new Object {
    def hashCode(_this: Object): Int32 = 42
    def toString(_this: Object): String = "Hello World!"
}
```

As these examples show, the implicit `this` argument because the first argument to each Flix function inside a new expression.

> **Note:** As these examples demonstrate, the new expression always has the `IO` effect (since it allocates a new object). Java methods, on the other hand, only need the `IO` effect if they themselves have side-effects. 
