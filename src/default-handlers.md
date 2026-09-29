# Default Handlers

Flix supports **default handlers** which means that an effect can declare a
handler that translates the effect into the `IO` effect. This allows `main` (and
any method annotated with `@Test`) to use that effect without explicitly
providing a handler in a `run-with` block.

For example, we can write:

```flix
use Sys.Env
use Time.Clock

def main(): Unit \ {Clock, Env, Logger} =
    let ts = Clock.currentTime(TimeUnit.Milliseconds);
    let os = Env.getOsName();
    Logger.info("UNIX Timestamp:   ${ts}");
    Logger.info("Operating System: ${os}")

```

which the Flix compiler translates to:

```flix
use Sys.Env
use Time.Clock

def main(): Unit \ IO =
    run {
        let ts = Clock.currentTime(TimeUnit.Milliseconds);
        let os = Env.getOsName();
        Logger.info("UNIX Timestamp:   ${ts}");
        Logger.info("Operating System: ${os}")
    } with Clock.runWithIO
      with Env.runWithIO
      with Logger.runWithIO
```

That is, the Flix compiler automatically inserts calls to `Clock.runWithIO`,
`Env.runWithIO`, and `Logger.runWithIO` which are the default handlers for their
respective effects.

For example, `Clock.runWithIO` is declared as:

```flix
use Time.Clock

@DefaultHandler
pub def runWithIO(f: Unit -> a \ ef): a \ (ef - Clock) + IO = ...
```

A default handler is declared using the `@DefaultHandler` annotation. Each
effect may have at most one default handler, and it must reside in the companion
module of that effect.

A default handler must have a signature of the form: 

```flix
def runWithIO(f: Unit -> a \ ef): a \ (ef - E) + IO
```
where `E` is the name of the effect.

We can use effects with default handlers in tests. For example:

```flix
@Test
def myTest01(): Unit \ {Assert, Logger} = 
    Logger.info("Running test!");
    Assert.assertEq(expected = 42, 42)
```

## Polymorphic Effects

A [polymorphic effect](./polymorphic-effects.md) can also have a default
handler. For example:

```flix
mod Emit {
    pub eff Emit[t] {
        def emit(x: t): Unit
    }

    @DefaultHandler
    pub def runWithIO(f: Unit -> a \ ef): a \ (ef - Emit[t]) + IO =
        run {
            f()
        } with handler Emit {
            def emit(_, resume) = resume()
        }
}

def main(): Unit \ {Emit[Int32], IO} =
    Emit.emit(42);
    println("Done")
```

Here the default handler of `Emit` discards the emitted values.

The default handler of a polymorphic effect `E[t]` must have a signature of the
form:

```flix
def runWithIO(f: Unit -> a \ ef): a \ (ef - E[t]) + IO
```

where `t` is a type variable. The signature cannot have trait constraints, e.g.
we cannot add `with ToString[t]`, because a default handler must work for every
type `t`. This is why the default handler above cannot print the emitted values.
