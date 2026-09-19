# Trusting Dependencies

To reduce the risk of supply-chain attacks, Flix builds every package dependency in a
*security context* that limits which language features it may use.

The security contexts are:

| Security Context  | Java Interop | Unchecked Casts | The `IO` Effect |
|-------------------|--------------|-----------------|-----------------|
| `paranoid`        | Forbidden    | Forbidden       | Forbidden       |
| `plain` (default) | Forbidden    | Forbidden       | Allowed         |
| `unrestricted`    | Allowed      | Allowed         | Allowed         |

A dependency built in the `plain` context can compute and it can use effects, but it
cannot reach outside Flix: no `import` of a Java class, no calls to Java constructors,
methods, or fields, no `unsafe`, and no unchecked casts. A dependency built in the
`paranoid` context cannot even use the `IO` effect.

This is what makes `plain` and `paranoid` safe to depend on: a package that cannot
reach Java, and cannot cast its way around the type system, can only do what its types
and effects say it does. We read the signature of a function we call, and the effect
system tells us what calling it can bring about — a `paranoid` package that returns a
pure value cannot touch the file system, open a socket, or read the clock, however it
is written inside. In the `unrestricted` context we have no such guarantee, and the
signatures tell us nothing about what the code may do.

## Setting the Security Context

We can set the security context of each dependency in the manifest:

```toml
[dependencies]
"github:flix/museum"              = { version = "2.1.0", mount = "museum", security = "plain" }
"github:magnus-madsen/helloworld" = { version = "1.3.0", mount = "helloworld", security = "unrestricted" }
```

A dependency that declares no security context is built in the `plain` context.

> **Note:** Security contexts apply to dependencies. Our own code is always
> unrestricted, whatever we declare for the packages we depend on.

## How Contexts Spread Through the Graph

Security contexts are transitive: the security context of a dependency also applies
to its own dependencies, unless one of them explicitly declares a lesser security
context. If several dependencies require the same package, the package inherits the
most restrictive security context requested.

A dependency can therefore not escape its context by depending on something else. A
package built in the `plain` or `paranoid` context may not even have Maven- or
JAR-dependencies of its own, since Java libraries require the `unrestricted`
context, and Flix reports an error if it finds one.

## Choosing a Context

The recommended approach is to **not** specify a security context, and thus default
to `plain`. It provides the best balance between flexibility and safety.

> **Warning:** Avoid `unrestricted` when possible, as it permits a dependency — and
> everything it depends on — to do *anything*. Even building or compiling code that
> includes `unrestricted` dependencies can by itself expose us to a supply-chain
> attack.

## Writing a Library that Needs Effects

If we are the author of a Flix library that requires effects, the best practice is
to introduce our own custom effects instead of using the `IO` effect directly, and
to split the library into two packages:

| Package                  | Description                           | Security Context |
|--------------------------|---------------------------------------|------------------|
| `webserver-lib`          | Core functionality using effects      | `plain`          |
| `webserver-lib-handlers` | Handlers that perform Java interop/IO | `unrestricted`   |

This approach has several benefits:

- Most functionality remains in the trusted `plain` security context.
- Unsafe code is isolated in `webserver-lib-handlers` for easier review.
- Users can implement their own handlers if they do not trust the provided ones.

See [Effects and Handlers](./effects-and-handlers.md) for how to define an effect
and its handlers.
