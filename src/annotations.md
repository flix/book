# Annotations

An annotation is a marker written before a declaration, such as `@Test` before
a function. Annotations ask the compiler to check or treat the declaration in a
specific way. For example, `@Test` marks a function as a test, and `@Tailrec`
asks the compiler to verify that a function is tail recursive:

```flix
@Test
def testSum01(): Unit \ Assert =
    Assert.assertEq(expected = 6, sum(1 :: 2 :: 3 :: Nil, 0))

@Tailrec
def sum(l: List[Int32], acc: Int32): Int32 = match l {
    case Nil     => acc
    case x :: xs => sum(xs, acc + x)
}
```

The set of annotations is fixed by the language. You cannot define your own,
annotations take no arguments, and a program cannot inspect them at runtime.
Where other languages use annotations for language features, Flix uses keywords
instead: for example, an instance that overrides a default implementation from
its trait marks the function with `redef`, not `@Override`. Annotation names
are capitalized. Several annotations may be placed on the same declaration, but
each may appear only once.

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

Annotations go on top-level declarations and on declarations inside modules,
traits, and instances. A local function declared inside another function accepts
only `@Tailrec` and `@Terminates`.
