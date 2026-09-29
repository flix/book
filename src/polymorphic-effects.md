# Polymorphic Effects

> **Note:** Polymorphic effects are an experimental feature.

A _polymorphic effect_ is an effect that is parameterized by one or more types.

For example, we can declare an effect that emits values of type `t`:

```flix
eff Emit[t] {
    def emit(x: t): Unit
}
```

Here the `Emit` effect has the type parameter `t`, which is the type of the
argument of the `emit` operation. We can use `Emit` to emit integers, strings,
or values of any other type.

For example, we can write a function that emits a range of integers:

```flix
def range(b: Int32, e: Int32): Unit \ Emit[Int32] =
    if (b >= e)
        ()
    else {
        Emit.emit(b);
        range(b + 1, e)
    }
```

and a function that emits two strings:

```flix
def greetings(): Unit \ Emit[String] =
    Emit.emit("Hello");
    Emit.emit("World")
```

The `range` function has the effect `Emit[Int32]` whereas the `greetings`
function has the effect `Emit[String]`. We call the operation as `Emit.emit`
without a type argument. Flix infers the type argument from the value that we
emit.

> **Note:** Polymorphic effects should not be confused with [effect
> polymorphism](./effect-polymorphism.md). A polymorphic effect is an _effect_
> that is parameterized by a type, whereas an effect polymorphic function is a
> _function_ that is parameterized by an effect.

## Handling a Polymorphic Effect

We handle a polymorphic effect like any other effect:

```flix
def main(): Unit \ IO =
    run {
        range(1, 4)
    } with handler Emit {
        def emit(x, resume) = { println(x); resume() }
    }
```

which prints:

```
1
2
3
```

We write `with handler Emit` without a type argument. Flix infers that we handle
`Emit[Int32]` and hence that `x` has type `Int32`.

A handler can work for every type argument. For example, we can write a function
that collects the emitted values into a list:

```flix
def collect(f: Unit -> Unit \ ef): List[t] \ ef - Emit[t] =
    run {
        f();
        Nil
    } with handler Emit {
        def emit(x, resume) = x :: resume()
    }
```

Here `collect` handles the effect `Emit[t]`, for any type `t`, and returns a
`List[t]`. We can use it with both `range` and `greetings`:

```flix
def numbers(): List[Int32] = collect(() -> range(1, 4))

def words(): List[String] = collect(() -> greetings())

def main(): Unit \ IO =
    println(numbers());
    println(words())
```

which prints:

```
1 :: 2 :: 3 :: Nil
Hello :: World :: Nil
```

## Polymorphic Functions

A function can be polymorphic in the type argument of an effect:

```flix
def emitAll(l: List[t]): Unit \ Emit[t] =
    foreach (x <- l)
        Emit.emit(x)
```

Here `emitAll` emits every element of a list. If we call `emitAll` with a
`List[Int32]` then the call has the effect `Emit[Int32]`, and if we call it with
a `List[String]` then the call has the effect `Emit[String]`.

## Multiple Type Parameters

An effect can have several type parameters:

```flix
eff Ask[q, a] {
    def ask(question: q): a
}

def age(): Int32 \ Ask[String, Int32] =
    Ask.ask("How old are you?")
```

Here the `Ask` effect is parameterized by the type of the question `q` and by
the type of the answer `a`.

The type parameters belong to the effect: an operation cannot declare type
parameters of its own. Moreover, every type parameter of an effect must be used
by at least one of its operations.

## One Instantiation per Function

Different functions can use a polymorphic effect with different type arguments,
as `range` and `greetings` do. But _within_ a function, a polymorphic effect
must be used with the same type arguments everywhere.

For example, if we write:

```flix
def f(): Unit \ Emit[Int32] + Emit[String] =
    Emit.emit(42);
    Emit.emit("Hello")
```

The Flix compiler emits the error message:

```
-- Type Error [E6795] -------------------------------------------- src/Main.flix

>> Mismatched type arguments for effect 'Emit': 'Int32' and 'String'.

5 | def f(): Unit \ Emit[Int32] + Emit[String] =
                                  ^^^^^^^^^^^^
                                  mismatched effect type argument.

The effect 'Emit' is used with different types for its 1st type parameter 't'.

Effect One: Emit[Int32]
Effect Two: Emit[String]
```

The restriction applies to the whole function: to its signature, to its body
(including lambda expressions and local definitions), and to the effects that
are _handled_ inside the function.

For example, the following `main` function is rejected, even though it handles
both effects:

```flix
def main(): Unit \ IO =
    println(collect(() -> range(1, 4)));
    println(collect(() -> greetings()))
```

The problem is that `main` uses both `Emit[Int32]` and `Emit[String]`. The
solution is to move each use into its own function, as we did with `numbers` and
`words` above.

The restriction also means that we cannot write a function that handles an
effect by using the same effect with a different type argument:

```flix
def render(f: Unit -> Unit \ Emit[Int32]): Unit \ Emit[String] = ...
```

Here `render` is rejected because its signature uses both `Emit[Int32]` and
`Emit[String]`.

The restriction only concerns multiple uses of the _same_ effect. A function can
freely use different polymorphic effects, e.g. `Emit[Int32]` and
`Ask[String, Int32]`.

## Default Handlers

A polymorphic effect can have a default handler. We describe the details in the
section on [Default Handlers](./default-handlers.md).
