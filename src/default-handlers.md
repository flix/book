## Default Handlers

Flix supports **default handlers**, meaning an effect can declare a handler that
translates the effect into the `IO` effect. This allows `main` and any method
annotated with `@Test` to use that effect without explicitly providing a
handler.

For example, we can write:

```flix
def main(): Unit \ {Clock, Env, Logger} = 
    let ts = Clock.currentTime(TimeUnit.Milliseconds);
    let os = Env.getOsName();
    Logger.info("UNIX Timestamp:   ${ts}");
    Logger.info("Operating System: ${os}")

```

which the Flix compiler automatically translates into:

```flix
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

Notably `Clock.runWithIO`, `Env.runWithIO`, and `Logger.runWithIO` are the
default handlers for their respective effects. 

For example, `Clock.runWithIO` is declared as:

```flix
@DefaultHandler
pub def runWithIO(f: Unit -> a \ ef): a \ (ef - Clock) + IO = ...
```

A default handler is declared using the `@DefaultHandler` annotation. Each
effect may have at most one default handler, and it must reside in the companion
module of that effect.

> **Note:** A default handler must have the signature: 
>
> ```flix
> runWithIO(f: Unit -> a \ ef): a \ (ef - E) + IO
> ```
> where `E` is the name of the effect.

