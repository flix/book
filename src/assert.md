# Assert

Flix provides `Assert` as a library effect for runtime assertions. The `Assert`
effect has a default handler, so no explicit `runWithIO` call is needed in
`main`.

## Basic Assertions

The `Assert` module provides several assertion functions:

```flix
mod Assert {
    /// Asserts that `cond` is `true`.
    def assertTrue(cond: Bool): Unit \ Assert

    /// Asserts that `cond` is `false`.
    def assertFalse(cond: Bool): Unit \ Assert

    /// Asserts that `expected` equals `actual`.
    def assertEq(expected: a, actual: a): Unit \ Assert with Eq[a], ToString[a]

    /// Asserts that `unexpected` does not equal `actual`.
    def assertNeq(unexpected: a, actual: a): Unit \ Assert with Eq[a], ToString[a]

    /// Asserts that `o` is `Some`.
    def assertSome(o: Option[a]): Unit \ Assert

    /// Asserts that `o` is `None`.
    def assertNone(o: Option[a]): Unit \ Assert with ToString[a]

    /// Asserts that `r` is `Ok`.
    def assertOk(r: Result[e, a]): Unit \ Assert with ToString[e]

    /// Asserts that `r` is `Err`.
    def assertErr(r: Result[e, a]): Unit \ Assert with ToString[a]

    /// Asserts that `ma` is empty.
    def assertEmpty(ma: m[a]): Unit \ Assert with Foldable[m]

    /// Asserts that `ma` is non-empty.
    def assertNonEmpty(ma: m[a]): Unit \ Assert with Foldable[m]

    /// Unconditionally succeeds with the given message `msg`.
    def success(msg: String): Unit \ Assert

    /// Unconditionally fails with the given message `msg`.
    def fail(msg: String): Unit \ Assert
}
```

## Using `Assert` with the Default Handler

The default handler throws an `AssertionError` on failure, so no explicit
handler is needed:

```flix
use Assert.{assertTrue, assertFalse, assertEq, assertNeq}

def main(): Unit \ { Assert, IO } =
    assertTrue(1 + 1 == 2);
    assertFalse(1 > 2);
    assertEq(expected = 4, 2 + 2);
    assertNeq(unexpected = 0, 1 + 1);
    println("All assertions passed!")
```

## Printing Failures to Standard Out

The `runWithStdOut` handler prints assertion failures to standard out but allows
execution to continue:

```flix
use Assert.assertEq

def main(): Unit \ IO =
    run {
        assertEq(expected = 4, 2 + 2);
        assertEq(expected = 10, 3 + 3);
        println("Execution continued after failing assertion.")
    } with Assert.runWithStdOut
```

## Logging Failures with the Logger

The `runWithLogger` handler sends assertion failures to the `Logger` effect:

```flix
use Assert.assertEq

def main(): Unit \ IO =
    run {
        assertEq(expected = 42, 21 + 21);
        assertEq(expected = 10, 3 + 3);
        println("Execution continued after failing assertion.")
    } with Assert.runWithLogger
      with Logger.runWithIO
```
