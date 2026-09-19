# Package Management

Every non-trivial Flix project should have a `flix.toml` manifest. The manifest
contains information about the project and its dependencies.

A minimal manifest is of the form:

```toml
[package]
name    = "hello-library"
version = "0.1.0"
flix    = "0.76.2"
```

The `init` command creates such a manifest.

The `flix` field is the oldest version of Flix that can build the package. Flix
checks the field of every package in the dependency graph and refuses to build a
package that requires a newer version of Flix than the one that is running:

```
The package 'github:flix/museum' 2.1.0 requires Flix version 0.76.2, but the current version is 0.76.1.
Please upgrade to Flix 0.76.2 or newer.
```

A package that is published on GitHub must also declare its repository:

```toml
[package]
name       = "museum"
version    = "2.1.0"
flix       = "0.76.2"
repository = "github:flix/museum"
```

> **Note:** Flix requires version numbers to follow SemVer.

## Adding Flix Dependencies

We can add dependencies on other Flix packages to the manifest:

```toml
[dependencies]
"github:flix/museum"              = { version = "2.1.0", mount = "museum" }
"github:magnus-madsen/helloworld" = { version = "1.3.0", mount = "helloworld" }
```

A dependency declares two things: the `version` we require, and the `mount`, the
name we reach the package under. A dependency may also declare a `security`
context, as described in the [Security](#security) section below.

## Using a Dependency

A Flix package does not become part of our own namespace. Its modules live in a
namespace of their own, and we reach them through the package's *mount*, which we
write before `::` in a `use`:

```flix
use museum::Museum

def main(): Unit \ IO =
    Museum.visitMuseum()
```

The `::` separates the package from the module path inside it. What follows it is
an ordinary module path, separated by `.`, so every kind of `use` works. For a
package mounted as `game`:

```flix
use game::Board                          // a top-level module of the package
use game::Game.Rules                     // a nested module
use game::Game.Rules.players             // a function
use game::{Board, Game}                  // several modules
use game::Game.Rules.{players => count}  // with a rename
```

A few rules govern mounts:

- The mount is chosen by whoever depends on the package, in their own manifest.
  It cannot be renamed in a `use`.
- A mount is a letter, upper- or lowercase, followed by letters, digits, and
  underscores. It cannot contain a hyphen, so a repository whose name has one
  needs a mount that does not: `github:flix/museum-clerk` is mounted as `clerk`,
  and `github:jls/tic-tac-toe` as `ticTacToe`. A mount cannot be a Flix keyword.
- Two dependencies cannot share a mount.
- A mount is a name of its own and not a module: it occupies no module namespace.
  A mount named `List` does not shadow the standard library's `List`, and a mount
  may share its name with one of our own modules.
- `::` may appear only in a `use`, and at most once. We cannot write
  `museum::Museum.visitMuseum()` in an expression, nor `game::Board` in a type.
  We must bring the name into scope with a `use` first. Modules are always
  separated by `.`, so we write `use game::Game.Rules`, never
  `use game::Game::Rules`.

Only the `pub` declarations of a package can be reached. A module that is not
declared `pub` is private to the package that declares it, and a `use` of it is
an error:

```
>> Module 'github:flix/museum-clerk.Clerk' is not accessible from the module ''.
```

## Adding Maven Dependencies

We can also add dependencies on Maven packages to the manifest:

```toml
[mvn-dependencies]
"org.junit.jupiter:junit-jupiter-api" = "5.9.2"
```

## Adding JAR Dependencies

We can depend on a JAR-file that is downloaded from a URL. The key is the file
name the JAR is saved under, which must end in `.jar`:

```toml
[jar-dependencies]
"commons-lang3.jar" = "url:https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar"
```

## Understanding Dependency Resolution

Flix dependency resolution works as follows:

1. Flix reads `flix.toml` and downloads the manifest of every Flix package that
   can be reached through the dependencies, at every version they are required
   at.
2. Flix selects the version that each package is built at.
3. Flix downloads the package file of each selected package.
4. Flix inspects each package for its Maven dependencies and downloads these.

We illustrate with an example. Assume we have a Flix package with:

```toml
[dependencies]
"github:flix/museum" = { version = "2.1.0", mount = "museum" }
```

Running Flix produces:

```
Found 'flix.toml'. Checking dependencies...
Resolving Flix dependencies...
  Downloading `flix/museum.toml` (v2.1.0)... OK.
  Downloading `flix/museum-clerk.toml` (v2.1.0)... OK.
  Downloading `flix/museum-entrance.toml` (v2.0.0)... OK.
  Downloading `flix/museum-giftshop.toml` (v2.0.0)... OK.
  Downloading `flix/museum-restaurant.toml` (v2.0.0)... OK.
  Downloading `flix/museum-clerk.toml` (v2.0.0)... OK.
  Cached `flix/museum-clerk.toml` (v2.0.0).
  Raised `flix/museum-clerk` (v2.0.0 -> v2.1.0), required by `flix/museum` (v2.1.0).
Downloading Flix dependencies...
  Downloading `flix/museum.fpkg` (v2.1.0)... OK.
  Downloading `flix/museum-clerk.fpkg` (v2.1.0)... OK.
  Downloading `flix/museum-entrance.fpkg` (v2.0.0)... OK.
  Downloading `flix/museum-giftshop.fpkg` (v2.0.0)... OK.
  Downloading `flix/museum-restaurant.fpkg` (v2.0.0)... OK.
Resolving Maven dependencies...
  Running Maven dependency resolver.
Downloading external jar dependencies...
Dependency resolution completed.
```

This happens because `flix/museum` has the following dependency tree:

- `flix/museum` depends on:
    - `flix/museum-clerk` (v2.1.0)
    - `flix/museum-entrance` which depends on:
        - `flix/museum-clerk` (v2.0.0)
    - `flix/museum-giftshop` which depends on:
        - `flix/museum-clerk` (v2.0.0)
    - `flix/museum-restaurant` which depends on
        - `org.apache.commons:commons-lang3`

Note that the manifest of `flix/museum-clerk` is downloaded at both of the
versions it is required at, but only one of them is built. Which one is the
subject of the next section.

## Understanding Version Selection

A version in a manifest is the *least* version we can build with, not the exact
version we get. Flix builds a package at the greatest version that anything in
the dependency graph requires, which is the least version that satisfies every
dependent.

In the example above, `flix/museum` requires `flix/museum-clerk` at version
`2.1.0`, whereas `flix/museum-entrance` and `flix/museum-giftshop` require it at
`2.0.0`. Flix builds it at `2.1.0` and reports that it did so:

```
  Raised `flix/museum-clerk` (v2.0.0 -> v2.1.0), required by `flix/museum` (v2.1.0).
```

A package is built at one version only. If it is required at versions that do not
share a major version then there is nothing to select, and Flix reports an error.
For example, if one dependent required `flix/museum-clerk` at `1.1.0` while
another required it at `2.1.0`:

```
Found incompatible versions of the same package in the dependency graph:
  The package 'github:flix/museum-clerk' is required at versions that do not share a major version:

    1.1.0 required by 'museum-giftshop'
    2.1.0 required by 'museum'

  A package is built at one version, which must satisfy every dependent: it must
  be at or above the version the dependent requires, and have the same major version.
  No version satisfies these, so one of the dependents must move across a major version.
```

## The Lock File

When Flix resolves the dependencies of a project, it writes a `packages.lock`
file next to `flix.toml`:

```toml
[lock]
version = 1

[packages."github:flix/museum-clerk"."1.1.0"]
toml    = "sha256:2e1d0e275ffa437dedeae98f23d8af8edb548d62a34976bbd4f2e0b9f7b14216"
fpkg    = "sha256:acc4a95bc139741e511e554431b784fbb57a4b8836143ed592079e316c6b0b15"
```

The lock file records the digest of every file that the resolution read: the
`flix.toml` of every package at every version that the dependency graph requires,
and the package file of every package that is built. On a later build, Flix
verifies each file against the lock file as it is installed, and refuses to
compile a dependency that is no longer the same.

> **Tip:** The `packages.lock` file should be committed to version control.

## Security
To reduce the risk of supply-chain attacks, every dependency has a **security
context** — even if you don't set one explicitly. Security contexts control
which language features a dependency may use. Broader security contexts enable
more features but also increase the risk of supply-chain attacks.

The security contexts are defined as follows:

| Security Context | Java Interop | Unchecked Casts | The `IO` Effect |
|------------------|--------------|-----------------|-----------------|
| `paranoid`       | Forbidden    | Forbidden       | Forbidden       |
| `plain` (default)| Forbidden    | Forbidden       | Allowed         |
| `unrestricted`   | Allowed      | Allowed         | Allowed         |

You can set the security context of each dependency in the manifest like so:
```toml
[dependencies]
"github:flix/museum"              = { version = "2.1.0", mount = "museum", security = "plain" }
"github:magnus-madsen/helloworld" = { version = "1.3.0", mount = "helloworld", security = "unrestricted" }
```

Security contexts are transitive: a dependency's security context also applies
to its transitive dependencies, unless a dependency explicitly declares a lesser
security context. If multiple dependencies require the same library, the library
inherits the most restrictive security context requested.

The recommended approach is to **not** specify a security context, thus
defaulting to `plain`. It provides the best balance between flexibility and
safety. You should avoid `unrestricted` when possible, as it permits
(transitive) dependencies to do *anything*. Even building or compiling code that
includes `unrestricted` dependencies can by itself expose you to a supply-chain
attack.

If you are the author of a Flix library that requires effects, the best
practice is to introduce your own custom effects instead of using the `IO`
effect directly, and to split the library into two packages:

| Package                  | Description                           | Security Context |
|--------------------------|---------------------------------------|------------------|
| `webserver-lib`          | Core functionality using effects      | `plain`          |
| `webserver-lib-handlers` | Handlers that perform Java interop/IO | `unrestricted`   |

This approach provides several benefits:
- Most functionality remains in the trusted `plain` security context.
- Unsafe code is isolated in `webserver-lib-handlers` for easier review.
- Users can implement their own handlers if they don't trust the provided ones.
