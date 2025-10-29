## Package Management

Every non-trivial Flix project should have a `flix.toml` manifest. The manifest
contains information about the project and its dependencies.

A minimal manifest is of the form:

```toml
[package]
name        = "hello-library"
description = "A simple library"
version     = "0.1.0"
flix        = "0.35.0"
license     = "Apache-2.0"
authors     = ["John Doe <john@example.com>"]
```

> **Note:** The `flix` field is not yet used, but it will be used in the future.

### Adding Flix Dependencies

We can add dependencies on other Flix packages to the manifest:

```toml
[dependencies]
"github:flix/museum"              = "1.4.0"
"github:magnus-madsen/helloworld" = "1.3.0"
```

> **Note:** Flix requires version numbers to follow SemVer.

### Adding Maven Dependencies

We can also add dependencies on Maven packages to the manifest:

```toml
[mvn-dependencies]
"org.junit.jupiter:junit-jupiter-api" = "5.9.2"
```

### Understanding Dependency Resolution

Flix dependency resolution works as follows:

1. Flix reads `flix.toml` and computes the transitive set of Flix package
   dependencies.
2. Flix downloads all of these Flix packages.
3. Flix inspects each package for its Maven dependencies and downloads these.

We illustrate with an example. Assume we have a Flix package with:

```toml
[dependencies]
"github:flix/museum"              = "1.4.0"
```

Running Flix produces:

```
Found `flix.toml'. Checking dependencies...
Resolving Flix dependencies...
  Downloading `flix/museum.toml` (v1.4.0)... OK.
  Downloading `flix/museum-entrance.toml` (v1.2.0)... OK.
  Downloading `flix/museum-giftshop.toml` (v1.1.0)... OK.
  Downloading `flix/museum-restaurant.toml` (v1.1.0)... OK.
  Downloading `flix/museum-clerk.toml` (v1.1.0)... OK.
  Cached `flix/museum-clerk.toml` (v1.1.0).
Downloading Flix dependencies...
  Downloading `flix/museum.fpkg` (v1.4.0)... OK.
  Downloading `flix/museum-entrance.fpkg` (v1.2.0)... OK.
  Downloading `flix/museum-giftshop.fpkg` (v1.1.0)... OK.
  Downloading `flix/museum-restaurant.fpkg` (v1.1.0)... OK.
  Downloading `flix/museum-clerk.fpkg` (v1.1.0)... OK.
  Cached `flix/museum-clerk.fpkg` (v1.1.0).
Resolving Maven dependencies...
  Adding `org.apache.commons:commons-lang3' (3.12.0).
  Running Maven dependency resolver.
Dependency resolution completed.
```

This happens because `flix/museum` has the following dependency tree:

- `flix/museum` depends on:
    - `flix/museum-entrance` which depends on:
        - `flix/museum-clerk`
    - `flix/museum-giftshop` which depends on:
        - `flix/museum-clerk`
    - `flix/museum-restaurant` which depends on
        - `org.apache.commons:commons-lang3`

### Security
To reduce supply-chain attacks, every dependency has a *trust*
level--even if you don't set one explicitly.
Trust levels control which language features a dependency may use.
Higher trust levels enable more features but also increase
the risk of supply-chain attacks.

The trust levels are as follows (from lowest to highest):
- `pure`: forbids Java interop, the `IO` effect, and unchecked casts.
- `plain` (default): permits the `IO` effect but forbids Java interop
  and unchecked casts.
- `unrestricted`: allows Java interop, the IO effect, and unchecked casts.

You can set the trust level of each dependency in the manifest like so:
```toml
[dependencies]
"github:flix/museum"              = { "version" = "1.4.0", "trust" = "plain" }
"github:magnus-madsen/helloworld" = { "version" = "1.3.0", "trust" = "unrestricted" }
```

Trust levels are transitive: a dependency's trust level also applies
to its transitive dependencies, unless a dependency explicitly declares
a lower trust level.
If multiple dependencies require the same library,
the library inherits the lowest trust level requested.

The recommended approach is to **not** specify a trust level, thus
defaulting to `plain`.
It provides the best balance between flexibility and safety.
You should avoid unrestricted when possible, as it permits
(transitive) dependencies to do *anything*.
Even building or compiling code that includes unrestricted dependencies
can by itself expose you to a supply-chain attack.
However, the package manager never downloads a package
that declares Java dependencies in its manifest if it has
trust level `plain` or lower.

If you author a Flix library that uses Java, split it into two
packages: a core library that implements pure logic and custom
effects, and a separate handler package that performs Java interop.
This makes the core library easier to test and review.
Keep effects small and document the expected handler behavior so
users can implement their own handlers if they do no wish to
use handler library.
