# Type Match

Flix supports a type match construct that enables compile-time pattern matching
on the type of a polymorphic value. 

For example, we can write a function that inspects the type of its argument:

```flix
def inspect(x: a): String = typematch x {
    case _: Int32   => "x is an Int32"
    case _: String  => "x is a String"
    case _: _       => "x is neither an Int32 nor a String"
}

def main(): Unit \ IO = 
    println(inspect(12345));
    println(inspect("abc"));
    println(inspect(false))
```

Here the `inspect` function pattern matches on the type of the formal parameter
`x` using the `typematch` construct. For example, if the type of `x` is an
`Int32` then the function returns the string `"x is an Int32"` and so forth.

The `typematch` construct is eliminated at compile-time, hence there is no
runtime cost.

As the example shows, the `typematch` construct always requires a default case.
This is because Flix has infinitely many types, and a `typematch` cannot cover
all of them.

A type match can also inspect more complex types, as the following example
shows:

```flix
def inspect(x: a): String = typematch x {
    case _: List[Int32]   => "x is a list of integers"
    case _: List[String]  => "x is a list of strings"
    case _: _             => "x is something else"
}

def main(): Unit \ IO = 
    println(inspect(1 :: 2 :: 3 :: Nil));
    println(inspect("abc" :: "def" :: Nil));
    println(inspect(false))
```

We can also bind values with type match, as the following example shows:

```flix
def inspect(x: a): String = typematch x {
    case i: Int32   => "${i * i}"
    case s: String  => String.toUpperCase(s)
    case _: _ 		=> "-"
}

def main(): Unit \ IO = 
    println(inspect(12345));
    println(inspect("abc"));
    println(inspect(false))
```

> **Warning:** While type match is a powerful meta-programming construct, it
> should be used sparingly and with great care.

A typical legitimate use case for type match is when we want to work around
limitations imposed by the JVM. For example, the Flix Standard Library uses type
match to implement the `Array.copyOfRange` function as shown below:

```flix
def copyOfRange(_: Region[r2], b: Int32, e: Int32, a: Array[a, r1]): ... =
typematch a {
    case arr: Array[Int16, r1] =>
        import static java.util.Arrays.copyOfRange(Array[Int16, r1], Int32, Int32): ...
    ...
    case arr: Array[Int32, r1] =>
        import static java.util.Arrays.copyOfRange(Array[Int32, r1], Int32, Int32): ...
    ...
    // ... additional cases ...
}
```

Here type match allows us to call the right overloaded version of
`java.util.Arrays.copyOfRange`. Thus Flix programmers can use our version of
`copyOfRange` (i.e., `Array.copyOfRange`) while underneath the hood, we always
call the most efficient Java version. 
