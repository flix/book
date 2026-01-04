# Test Framework

Flix comes with a built-in test framework.

A test is a Flix function marked with the `@Test` annotation. 

A test function must have return type `Unit` and the `Assert` effect.

The `Assert` module provides assertion functions for testing. Here are the most commonly used:

| Function | Purpose |
|----------|---------|
| `Assert.assertEq(expected = value, actual)` | Assert equality between values |
| `Assert.assertNeq(unexpected = value, actual)` | Assert inequality between values |
| `Assert.assertTrue(cond)` | Assert condition is true |
| `Assert.assertFalse(cond)` | Assert condition is false |
| `Assert.assertSome(opt)` | Assert Option is Some |
| `Assert.assertNone(opt)` | Assert Option is None |
| `Assert.assertOk(res)` | Assert Result is Ok |
| `Assert.assertErr(res)` | Assert Result is Err |
| `Assert.assertEmpty(coll)` | Assert collection is empty |
| `Assert.assertMemberOf(x, coll)` | Assert element is in collection |
| `Assert.fail(msg)` | Unconditionally fail with message |
| `Assert.success(msg)` | Unconditionally succeed with message |

The `assertEq` and `assertNeq` require the use of a labelled argument `expected` / `unexpected`.

Here is an example:

```flix
use Assert.{assertEq, assertTrue, assertFalse, assertOk, assertErr}

def add(x: Int32, y: Int32): Int32 = x + y

def isEven(x: Int32): Bool = Int32.modulo(x, 2) == 0

def safeDivide(x: Int32, y: Int32): Result[String, Int32] =
    if (y == 0) Err("Division by zero") else Ok(x / y)

@Test
def testAdd01(): Unit \ Assert =
    assertEq(expected = 5, add(2, 3))

@Test
def testIsEven01(): Unit \ Assert =
    assertTrue(isEven(4))

@Test
def testIsEven02(): Unit \ Assert =
    assertFalse(isEven(3))

@Test
def testSafeDivide01(): Unit \ Assert =
    assertOk(safeDivide(10, 2))

@Test
def testSafeDivide02(): Unit \ Assert =
    assertErr(safeDivide(10, 0))
```

Running the tests (e.g. with `flix test`) yields:

```
Running 5 tests...

   PASS  testAdd01 1,4ms
   PASS  testIsEven01 312,5us
   PASS  testIsEven02 229,8us
   PASS  testSafeDivide01 366,0us
   PASS  testSafeDivide02 299,7us

Passed: 5, Failed: 0. Skipped: 0. Elapsed: 3,8ms.
```

## Assertions with Custom Messages

Most assertions have `WithMsg` variants for custom error messages.

```flix
use Assert.{assertEqWithMsg, assertTrueWithMsg, assertFalseWithMsg}

@Test
def testAdd01(): Unit \ Assert =
    assertEqWithMsg(expected = 5, add(2, 3), "addition should work")

@Test
def testIsEven01(): Unit \ Assert =
    assertTrueWithMsg(isEven(4), "4 should be even")

@Test
def testIsEven02(): Unit \ Assert =
    assertFalseWithMsg(isEven(3), "3 should be odd")
```
