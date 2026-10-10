# Declaring Modules

As we have already seen, modules can be declared using the `mod` keyword:

```flix
mod Museum {
    // ... members ...
}
```

## Nested Modules

We can nest modules inside other modules:

```flix
mod Museum {
    mod Entrance {
        pub def buyTicket(): Unit \ IO =
            println("Museum.Entrance.buyTicket() was called.")
    }

    mod Restaurant {
        pub def buyMeal(): Unit \ IO =
            println("Museum.Restaurant.buyMeal() was called.")
    }

    mod Giftshop {
        pub def buyGift(): Unit \ IO =
            println("Museum.Giftshop.buyGift() was called.")
    }

    pub def visit(): Unit \ IO =
        Entrance.buyTicket();
        Restaurant.buyMeal();
        Giftshop.buyGift()
}
```

Here the `Entrance`, `Restaurant`, and `Giftshop` modules are nested inside the
`Museum` module, and the `visit` function calls a function from each of them.

We can call `visit` from outside of the `Museum` module:

```flix
def main(): Unit \ IO =
    Museum.visit()
```

A module is _private_ to the module it is declared in, unless we declare it as
public. Hence the three nested modules can be used from inside `Museum`, as
`visit` does, but not from outside of it. If we try:

```flix
def main(): Unit \ IO =
    Museum.Entrance.buyTicket()
```

then Flix reports:

```
-- Resolution Error [E2544] -------------------------------------- src/Main.flix

>> Module 'Museum.Entrance' is not accessible from the module ''.

2 |     Museum.Entrance.buyTicket()
        ^^^^^^^^^^^^^^^^^^^^^^^^^
        inaccessible module

Tip: Mark the module as 'pub'.
```

## Public Modules

We make a module accessible from everywhere by declaring it as public with `pub
mod`. A public module is declared at the top level of a file of its own, under
its full name, and the path of the file must match the name of the module:

| Module                    | File                       |
|---------------------------|----------------------------|
| `pub mod Museum`          | `src/Museum.flix`          |
| `pub mod Museum.Entrance` | `src/Museum/Entrance.flix` |

For example, we can make the entrance of the museum public. In the file
`src/Museum.flix`, we write:

```flix
pub mod Museum {
    pub def visit(): Unit \ IO =
        Entrance.buyTicket()
}
```

and in the file `src/Museum/Entrance.flix`, we write:

```flix
pub mod Museum.Entrance {
    pub def buyTicket(): Unit \ IO =
        println("Museum.Entrance.buyTicket() was called.")
}
```

Here `Museum.Entrance` is the module `Entrance` inside the module `Museum`, as
if we had nested it, but now it is public. We can call `buyTicket` from
everywhere:

```flix
def main(): Unit \ IO =
    Museum.Entrance.buyTicket()
```

Or alternatively:

```flix
use Museum.Entrance.buyTicket;

def main(): Unit \ IO =
    buyTicket()
```

A public module cannot be nested inside the body of another module. If we write
`pub mod Entrance` inside the body of `Museum`, then Flix reports:

```
-- Name Error [E5544] ------------------------------------------ src/Museum.flix

>> Nested public module: 'Museum.Entrance'.

2 |     pub mod Entrance {
                ^^^^^^^^
                nested public module

Explanation: A public module must be declared at the top level of its
own file, not inside another module. For example:

  // File Museum/Entrance.flix
  pub mod Museum.Entrance { ... }
```

> **Note:** The parent of a module must be declared. We cannot declare the
> module `Museum.Entrance` without declaring the module `Museum`.

> **Note:** A private module may be declared in any file, and may also be
> declared under its full name: `mod Museum.Vault { ... }` declares a module
> that is private to `Museum`.

## Accessibility

Modules and their members are private by default. We make them public with the
`pub` modifier.

A module or member `m` declared in a module `A` is accessible from a module `B`
if:

- `m` is declared as public (`pub`), or
- `B` is the module `A` itself, or is nested inside `A`.

For example, the following is allowed:

```flix
mod A {
    mod B {
       pub def g(): Unit \ IO = A.f() // OK
    }

    def f(): Unit \ IO = println("A.f() was called.")
}
```

Here `f` is private to the module `A`. However, since `B` is nested inside `A`,
we can access `f` from inside `B`. On the other hand, the following is _not_
allowed:

```flix
mod A {
    mod B {
       def g(): Unit \ IO = println("A.B.g() was called.")
    }

    pub def f(): Unit \ IO = A.B.g() // NOT OK
}
```

because `g` is private to `B`.

The same rule applies to the modules themselves. For example, the following is
allowed:

```flix
mod A {
    mod B {
        pub def g(): Unit \ IO = println("A.B.g() was called.")
    }

    mod C {
        pub def h(): Unit \ IO = A.B.g() // OK
    }
}
```

Here `B` is private to the module `A`. However, since `C` is nested inside `A`,
we can access `B` from inside `C`.

When we write a qualified name, such as `A.B.g`, every module along the way
must be accessible, and so must the member itself.

> **Note:** A module that is not nested inside another module, such as `A`, is
> accessible from every module of our project, whether or not it is public.

## A Module is Declared Once

A module has exactly one declaration. We cannot declare a module and later
_reopen_ it to add more members, whether in the same file or in another file.

For example, if we write:

```flix
mod Museum {
    pub def open(): Unit \ IO = println("The museum is open.")
}

mod Museum {
    pub def close(): Unit \ IO = println("The museum is closed.")
}
```

then Flix reports:

```
-- Name Error [E5410] -------------------------------------------- src/Main.flix

>> Duplicate module: 'Museum'.

1 | mod Museum {
        ^^^^^^
        first declaration in src/Main.flix

5 | mod Museum {
        ^^^^^^
        duplicate declaration in src/Main.flix

Explanation: A module may have only one declaration site
in the program. Reopening a module — either across files or as multiple
sibling blocks — is not allowed. Combine the declarations into a single
module body.
```

Instead, we must declare both functions in the same module.

> **Note:** The modules of the Standard Library are also declared once. Hence we
> cannot declare a module with the name of one of them, e.g. `List`, `Math`, or
> `String`.

> **Note:** A top-level module cannot be named `Main`. The name is reserved for
> the entry point of the program.
