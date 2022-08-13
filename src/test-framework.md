# Test Framework

Flix comes with a simple built-in test framework. 

A test is a Flix function marked with the `@Test` annotation. That's it. 

A test function can return any value. If it returns a Bool then `true` is interpreted as success and `false` as failure. Any non-Boolean value is interpreted as success. 

The `Assert.eq` function can be used to test for equality between two values that implement the `Eq` and `ToString` type classes. The advantage of `Assert.eq` (over `==`) is that it will print the two values if they are unequal. The `Assert.eq` function should not be used outside of unit tests.

Here is an example:

```flix
def add(x: Int32, y: Int32): Int32 = x + y

@Test
def testAdd01(): Bool = 0 == add(0, 0)

@Test
def testAdd02(): Bool = Assert.eq(1, add(0, 1))

@Test
def testAdd03(): Bool = Assert.eq(2, add(1, 1))

@Test
def testAdd04(): Bool = Assert.eq(4, add(1, 2))

@Test @Skip
def testAdd05(): Bool = Assert.eq(8, add(2, 3))
```

Running the tests (e.g. with the command `test`) yields:

```
Running 5 tests...

   PASS  testAdd01 237,3us
   PASS  testAdd02 21,1us
   PASS  testAdd03 10,3us
   FAIL  testAdd04 (Assertion Error)
   SKIP  testAdd05 (SKIPPED)

--------------------------------------------------------------------------------

   FAIL  testAdd04
    Assertion Error
      Expected: 4
      Actual:   3

    dev.flix.runtime.HoleError: Hole '?Assert.assertEq' at Assert.flix:32:13    
        at Assert.Def%eq%174731.invoke(Unknown Source)
        at Cont%Bool.unwind(Cont%Bool)
        at Ns.m_testAdd04(Unknown Source)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at ca.uwaterloo.flix.language.phase.jvm.JvmBackend$.$anonfun$link$1(JvmBackend.scala:286)
        at ca.uwaterloo.flix.language.phase.jvm.JvmBackend$.$anonfun$getCompiledDefs$2(JvmBackend.scala:259)
        at ca.uwaterloo.flix.tools.Tester$TestRunner.runTest(Tester.scala:182)
        at ca.uwaterloo.flix.tools.Tester$TestRunner.$anonfun$run$7(Tester.scala:153)
        at ca.uwaterloo.flix.tools.Tester$TestRunner.$anonfun$run$7$adapted(Tester.scala:152)
        at scala.collection.immutable.Vector.foreach(Vector.scala:1856)
        at ca.uwaterloo.flix.tools.Tester$TestRunner.run(Tester.scala:152)

--------------------------------------------------------------------------------

Passed: 3, Failed: 1. Skipped: 1. Elapsed: 3,0ms.
```
