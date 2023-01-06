# Declaring Modules

As we have already seen, modules can be declared using the `mod` keyword:

```flix
mod Museum {
    // ... members ...
}
```

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
}
```

We can call these methods as follows:

```flix
def main(): Unit \ IO = 
    Museum.Entrance.buyTicket();
    Museum.Restaurant.buyMeal();
    Museum.Giftshop.buyGift()
```

Or alternatively as follows:

```flix
use Museum.Entrance.buyTicket;
use Museum.Restaurant.buyMeal;
use Museum.Giftshop.buyGift;
def main(): Unit \ IO = 
    buyTicket();
    buyMeal();
    buyGift()
```

## Accessibility

A module member `m` declared in module `A` is accessible from another module `B`
if:

- the member `m` is declared as public (`pub`).
- the module `B` is a sub-module of `A`.

For example, the following is allowed:

```flix
mod A {
    mod B {
       pub def g(): Unit \ IO = A.f() // OK
    }

    def f(): Unit \ IO = println("A.f() was called.")
}
```

Here `f` is private to the module A. However, since `B` is a sub-module of `A`
can access `f` from inside `B`. On the other hand, the following is _not_
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