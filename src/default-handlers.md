## Default Handlers

Flix supports **default handlers** which means that an effect can declare a
handler that translate the effect into the `IO` effect. Then `main` or any
method marked `@Test` can use that effect without explicitly handling the
effect. 

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

As the example shows, a default handler is declared with `@DefaultHandler`
annotation. An effect can have at most one default handler and it must be in the
companion module of the effect. 

> **Note:** A default handler must translate an effect to the `IO` effect.

