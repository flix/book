# Primitive Effects

> **Note:** This page is slightly updated and pending a rewrite.

Flix comes with a collection of pre-defined primitive effects. Unlike algebraic
and heap effects, primitive effects cannot be handled and never go out of scope.
A primitive effect represents a side-effect that happens on the machine. It
cannot be undone or reinterpreted.

The most important primitive effect is the `IO` effect.

## The `IO` Effect

The `IO` effect represents any action that interacts with the world outside the
program. Such actions include printing to the console, creating, reading, and
writing files, accessing the network, and more. The `IO` represents actions that
_change_ the outside world (e.g., modifying a file) but also actions that merely
_access_ the outside world (e.g., retrieving the current time). Unlike a pure
function, a function with the `IO` effect may change behavior every time it is
called, even if its arguments are the same. For example, reading the same file
twice is not guaranteed to return the same result since the file may have
changed between the two accesses.

The `IO` effect, and all other primitive effects, are _viral_. If a function has
a primitive effect, all its callers will also have that primitive effect. That
is to say, once you have tainted yourself with impurity, you remain tainted. 

## The Other Primitive Effects

- **NonDet**: The `NonDet` effect represents an almost pure computation. For
  example, a function that flips a coin is virtually pure; it has no
  side-effects. Yet, it may return different results, even when given the same
  arguments.
