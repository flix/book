## Classes and Interfaces

Flix allows us to create objects that extend a class or implements an interface.

This feature is conceptually similar to Java [Anonymous Classes](https://docs.oracle.com/javase/tutorial/java/javaOO/anonymousclasses.html). 
That is, we can define an (unnamed class) which implements an interface or extends a class, and then construct an object of that class. All in one go. 

For example, we can create an object that implements the `java.lang.Runnable` interface:

```flix
import java.lang.Runnable

def newRunnable(): Runnable \ IO = new Runnable {
    def run(_this: Runnable): Unit \ IO = 
        println("I am running!")
}
```

Every time we call `newRunnable` we get a *fresh* object that implements `java.lang.Runnable`.

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

The implicit `this` argument is always passed as the first argument in a new expression.

The Flix compiler ensures that a new expression implemenets all abstract methods of a class or interface.

A new expression always has the `IO` effect. 
