# Test Framework

> This section is under construction.

Flix comes with a built-in test framework:

```flix
def add(x: Int32, y: Int32): Int32 = x + y

@Test
def testAdd01(): Bool = Assert.eq(1, add(0, 1))

@Test
def testAdd02(): Bool = Assert.eq(4, add(1, 2))

@Test @Skip
def testAdd03(): Bool = Assert.eq(8, add(2, 3))
```

Running this gives:

```
Running 3 tests...

   PASS  testAdd01 301,5us
   FAIL  testAdd02 499,4us
   SKIP  testAdd03

--------------------------------------------------------------------------------

   FAIL  testAdd02
    Assertion Error:
      Expected: 4
      Actual:   3

--------------------------------------------------------------------------------

Passed: 1, Failed: 1. Skipped: 1. Elapsed: 3,0ms.
```
