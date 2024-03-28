# Glossary

***Algebraic Data Type.*** A data type defined using sum and product types, i.e.
using enumerated types and tuple types.

***Algebraic Effect.***  <a name="associated-effect"></a> A user-defined effect
which can be handled. The handler is supplied with the (delimited) continuation
of the effect. The continuation can be dropped, resume once, or resumed
multiple-times.

***Associated Type.***  <a name="associated-type"></a> A type that belongs to a
trait. Each trait instance specifies the specific associated type for that
instance. Hence different trait instances can have different associated types.

***Associated Effect.*** An effect that belongs to a trait. Each trait instance
specifies the specific associated effect for that instance. Hence different
trait instances can have different associated effects.

***Checked Cast.*** A safe cast that the compiler ensures is correct. Cannot
fail at runtime. 

***Effect.*** Flix supports three types of effects: built-in effects (e.g.
`IO` and `NonDet`), region-based effects, and user-defined effects.

***Effect Cast.*** A cast that changes the _effect_ of an expression.

***Effect Member.*** See [associated effect](#associated-effect).

***Effect Polymorphic.*** A function whose effect(s) depend on the effect(s) of
its function argument. See also [higher-order function](#higher-order-function).

***Effect Handler.*** An expression which handles a user-defined effect.

***Higher-Order Function.*** <a name="higher-order-function"></a> A function
that takes a function argument or returns a function.

***IO Effect.*** A built-in generic effect which represents any interaction with
the outside world. 

***Pure.*** A function (or expression) which has no effects.

***String Interpolation.*** A language feature that allows a string to contain
expressions. 

***Tail Call.*** A function call in tail-position and hence does not require
additional stack space. 

***Trait.*** An interface that specifies a collection of function signatures and
default functions. A trait can be implemented by several data types. Traits in
Flix are type classes. 

***Type Class.*** See Trait. 

***Type Cast.*** A cast that changes the _type_ of an expression.

***Type Inference.*** A language feature that allows the compiler to infer the
type of an expression without requiring annotations from the programmer. 

***Type Match.*** A language feature that allows a function to inspect (reflect)
on a type. 

***Type Member.*** See [associated type](#associated-type).

***Unchecked Cast.*** An unsafe cast which is not verified by the compiler. Can
fail at runtime. 

***Uninterpretable Effect.*** An effect that cannot (or should not) be handled, e.g. `IO`.
