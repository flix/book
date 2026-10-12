# Annotations

An annotation is a marker written before a declaration, such as `@Test` before
a function. Annotations ask the compiler to check or treat the declaration in a
specific way.

For example, the `@Tailrec` annotation asks the compiler to verify that every
recursive call in a function is a tail call. The `sum` function below passes
the check, because the recursive call is the last thing it does:

```flix
@Tailrec
def sum(l: List[Int32], acc: Int32): Int32 = match l {
    case Nil     => acc
    case x :: xs => sum(xs, acc + x)
}
```

As another example, the `@Test` annotation marks a function as a test. The test
framework runs every such function and reports whether it passed:

```flix
@Test
def testSum01(): Unit \ Assert =
    Assert.assertEq(expected = 6, sum(1 :: 2 :: 3 :: Nil, 0))
```

Flix has the following annotations:

| Annotation          | Meaning                                                                                                                |
|---------------------|------------------------------------------------------------------------------------------------------------------------|
| `@Test`             | Runs the function as a test. See [Test Framework](./test-framework.md).                                                |
| `@Skip`             | Skips a `@Test` function. The test is reported as skipped, not run.                                                    |
| `@DefaultHandler`   | Marks the default handler of an effect. See [Default Handlers](./default-handlers.md).                                 |
| `@Tailrec`          | Verifies that every self-recursive call is a tail call. See [Tail Recursion](./tail-recursion.md).                     |
| `@Terminates`       | Verifies that the function is structurally recursive. See [Termination Checking](./termination-checking.md).           |
| `@Inline`           | Makes the compiler always inline the function.                                                                         |
| `@DontInline`       | Makes the compiler never inline the function.                                                                          |
| `@Deprecated`       | Documents that the declaration is deprecated.                                                                          |
| `@Experimental`     | Documents that the declaration may change or be removed without warning.                                               |
| `@Lazy`             | Documents that the function uses lazy evaluation.                                                                      |
| `@LazyWhenPure`     | Documents that the function uses lazy evaluation when given a pure function. See [Purity Reflection](./purity-reflection.md). |
| `@Parallel`         | Documents that the function uses parallel evaluation.                                                                  |
| `@ParallelWhenPure` | Documents that the function uses parallel evaluation when given a pure function. See [Purity Reflection](./purity-reflection.md). |

The last six annotations are documentation. They are shown in the API docs and
as hints in the editor, but they do not change how the compiler translates the
function.

> **Note:** Flix has no `@Override` annotation. An instance that overrides a
> default implementation from its trait marks the function with the `redef`
> keyword instead.
