# `bug!` and `unreachable!`

Flix supports two special "functions": `bug!` and
`unreachable!` that can be used to indicate when an
internal program invariant is broken and execute
should abort.
For example:

```flix
match o {
    case Some(x) => ...
    case None    => bug!("The value of `o` cannot be empty.")
}
```

As another example:

```flix
match k {
    case n if n == 0 => ...
    case n if n >= 0 => ...
    case n if n <= 0 => ...
    case n           =>  unreachable!()
}
```

Use of `bug!` and `unreachable!` should be avoided
whenever possible.
