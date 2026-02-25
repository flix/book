# Classes and Interfaces

Flix allows us to create objects that extend a Java class or implements a Java interface.

This feature is conceptually similar to Java's [Anonymous Classes](https://docs.oracle.com/javase/tutorial/java/javaOO/anonymousclasses.html): 
We can define an (unnamed class) which implements an interface or extends a class and create an object of that class. All in one expression. 

For example, we can create an object that implements the `java.lang.Runnable` interface:

```flix
import java.lang.Runnable

def newRunnable(): Runnable \ IO = new Runnable {
    def $run(_this: Runnable): Unit \ IO = 
        println("I am running!")
}
```

Every time we call `newRunnable` we get a *fresh* object that implements `java.lang.Runnable`.

> **Note:** The implicit `this` argument is always explicitly passed as the first argument in a new expression.

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

## Calling Super Methods

When overriding a method in an anonymous subclass, we can call the parent
class's implementation using `super.methodName(args)`.

For example, we can extend `Thread` and override `toString` to include the
parent's default representation:

```flix
import java.lang.Thread

def main(): Unit \ IO =
    let t = new Thread {
        def new(): Thread \ IO = super("my-thread")
        def run(_this: Thread): Unit \ IO =
            println("Hello from ${Thread.currentThread().getName()}")
        def toString(_this: Thread): String \ IO =
            "MyThread(" + super.toString() + ")"
    };
    println(t)
```

Here `super.toString()` calls the `toString` method defined by `Thread` (the
parent class), and we wrap the result in `"MyThread(...)"`.

> **Note:** Super method calls can only be used inside `new` expressions, i.e.
> when defining an anonymous subclass.
