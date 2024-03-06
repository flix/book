## Exceptions

In Flix, all error handling should be done using the `Result[e, t]` type.
However, for interoperability with Java, Flix also has a classic `try-catch`
mechanism.

For example, we can write:

```flix
///
/// Returns `true` if the given file `f` exists.
///
pub def exists(f: String): Result[String, Bool] \ IO =
    try {
        import java_new java.io.File(String): ##java.io.File \ IO as newFile;
        import java.io.File.exists(): Bool \ IO;
        Ok(exists(newFile(f)))
    } catch {
        case ex: ##java.io.IOException =>
            import java.lang.Throwable.getMessage(): String \ IO;
            Err(getMessage(ex))
    }
```

Here we import the `File` constructor as `newFile` and the `File.exists` method
as `exists`. We then call the methods and catch the `IOException`.

> **Note:** Flix programs should not rely on the exception mechanism. Instead,
> we should guard all call to Java code that might throw exceptions close to
> their call site and turn these exceptions into `Result`s.

### Structured Concurrency and Exceptions

Flix supports [structured concurrency](./concurrency.md). This means that (1)
threads cannot outlive the lifetime of their region and (2) that exceptions
thrown in sub-threads are propagated to the thread of the region.

For example, given the program:

```flix
def main(): Unit \ IO =
    region rc {
        spawn f() @ rc;
        spawn g() @ rc
    };
    println("Done")
```

where `f` and `g` are some functions. If `f` or `g` were to throw an unhandled
exception then that exception would be _caught_ and _rethrown_ inside the `main`
thread. This means that we cannot successfully leave the scope of `rc` _unless_
`f` and `g` terminated _and_ did not throw any unhandled exceptions.
