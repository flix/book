# Tail Recursion

In Flix, and functional programming in general, iteration is expressed through
[recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)).

Flix has support full [tail call](https://en.wikipedia.org/wiki/Tail_call)
elimination which means that tail calls never increases the stack height. 

For example, if we want to determine if a list contains an element, we can write
a recursive function:

```flix
def memberOf(x: a, l: List[a]): Bool with Eq[a] = 
    match l {
        case Nil     => false
        case y :: ys => if (x == y) true else memberOf(x, ys)
    }
```

The `memberOf` function pattern matches on the list `l`. If it is empty then it
returns `false`. Otherwise, we have an element `y` and the rest of the list
`ys`. If `x == y` then we have found the element and we return `true`. Otherwise
we _recurse_ on the rest of the list `ys`. 

The recursive call to `memberOf` is in _tail position_, i.e. it is the last
thing to happen in the `memberOf` function. This has two important benefits: (a)
the Flix compiler is able to write `memberOf` to use an ordinary loop (which is
more efficient than a function call) and more importantly (b) a call to
`memberOf` _cannot_ overflow the stack, because the call stack never increases
in height.
