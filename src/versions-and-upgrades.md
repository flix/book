# Versions and Upgrades

A version in a manifest is the *least* version we can build with, not the exact
version we get. Flix works out which version of every package to build, records
what it downloaded, and tells us when there is something newer.

## How Flix Resolves Dependencies

Flix resolves the dependencies of a project in four steps:

1. Flix reads `flix.toml` and downloads the manifest of every Flix package that can
   be reached through the dependencies, at every version they are required at.
2. Flix works out which single version of each package to build.
3. Flix downloads the package file of each selected package.
4. Flix inspects each package for its Maven dependencies and downloads these.

We can see these steps at work in a project that depends on `flix/museum`:

```toml
[dependencies]
"github:flix/museum" = { version = "4.0.0", mount = "museum", security = "unrestricted" }
```

The package reaches Java through one of its own dependencies, so it must be declared
`unrestricted`, as described in [Trusting Dependencies](./trusting-dependencies.md).
It has this dependency tree:

- `flix/museum` depends on:
    - `flix/museum-clerk` (v2.1.3)
    - `flix/museum-entrance` which depends on:
        - `flix/museum-clerk` (v2.1.2)
    - `flix/museum-giftshop` which depends on:
        - `flix/museum-clerk` (v2.1.2)
    - `flix/museum-restaurant` which depends on
        - `org.apache.commons:commons-lang3`

and so a single dependency gives us five packages:

```
Found 'flix.toml'. Checking dependencies...
Resolving Flix dependencies...
  Downloading `flix/museum.toml` (v4.0.0)... OK.
  Downloading `flix/museum-clerk.toml` (v2.1.3)... OK.
  Downloading `flix/museum-entrance.toml` (v2.0.2)... OK.
  Downloading `flix/museum-giftshop.toml` (v2.0.2)... OK.
  Downloading `flix/museum-restaurant.toml` (v2.0.2)... OK.
  Downloading `flix/museum-clerk.toml` (v2.1.2)... OK.
  Cached `flix/museum-clerk.toml` (v2.1.2).
  Raised `flix/museum-clerk` (v2.1.2 -> v2.1.3), required by `flix/museum` (v4.0.0).
Downloading Flix dependencies...
  Downloading `flix/museum-restaurant.fpkg` (v2.0.2)... OK.
  Downloading `flix/museum-entrance.fpkg` (v2.0.2)... OK.
  Downloading `flix/museum.fpkg` (v4.0.0)... OK.
  Downloading `flix/museum-giftshop.fpkg` (v2.0.2)... OK.
  Downloading `flix/museum-clerk.fpkg` (v2.1.3)... OK.
Resolving Maven dependencies...
  Adding `org.apache.commons:commons-lang3' (v3.12.0).
  Running Maven dependency resolver.
Downloading external jar dependencies...
Dependency resolution completed.
```

The manifest of `flix/museum-clerk` is downloaded at both of the versions it is
required at, but only one of them is built.

## How Flix Selects a Version

Flix builds a package at the greatest version that anything in the dependency graph
requires, which is the least version that satisfies every dependent.

In other words, when two parts of the dependency graph ask for different versions of
the same package, Flix takes the newer of them. This works because a version in a
manifest is a lower bound: a dependent that asks for an older version is happy to be
built against a newer one, as long as the major version is the same. We therefore
never get an older version of a package than we asked for, and we may well get a
newer one.

In the example above, `flix/museum` requires `flix/museum-clerk` at version
`2.1.3`, whereas `flix/museum-entrance` and `flix/museum-giftshop` require it at
`2.1.2`. Flix builds it at `2.1.3` and reports that it did so:

```
  Raised `flix/museum-clerk` (v2.1.2 -> v2.1.3), required by `flix/museum` (v4.0.0).
```

**A package is built at one version only.** If a project transitively depends on two
different major versions of the same package, then no single version satisfies every
dependent, and Flix reports an error. For example, if `flix/museum-giftshop` required
`flix/museum-clerk` at `1.1.0`, while the others require it at `2.1.2` and `2.1.3`:

```
Found incompatible versions of the same package in the dependency graph:
  The package 'github:flix/museum-clerk' is required at versions that do not share a major version:

    1.1.0 required by 'flix/museum-giftshop'
    2.1.2 required by 'flix/museum-entrance'
    2.1.3 required by 'flix/museum'

  A package is built at one version, which must satisfy every dependent: it must
  be at or above the version the dependent requires, and have the same major version.
  No version satisfies these, so one of the dependents must move across a major version.
```

One of the dependents then has to move across a major version, which is something
only its author can do.

## The Version of Flix

Every package declares, in its `flix` field, the oldest version of Flix that can
build it. Flix checks the field of every package in the dependency graph, and
refuses to build a package that requires a newer version of Flix than the one we
are running:

```
The package 'github:flix/museum' 4.0.0 requires Flix version 0.76.2, but the current version is 0.76.1.
Please upgrade to Flix 0.76.2 or newer.
```

## The Lock File

When Flix resolves the dependencies of a project, it writes a `packages.lock` file
next to `flix.toml`. For the example above, it begins:

```toml
[lock]
version = 1

[packages."github:flix/museum"."4.0.0"]
toml    = "sha256:5be4c6f17203a0c62294612f2877f52c181e2029153d88c8c65789f64bdf1c5f"
fpkg    = "sha256:c6d22cf0cdb1a45208b175636830f8364308db9f3f7259a2e4960dfb536d1e3c"

[packages."github:flix/museum-clerk"."2.1.2"]
toml    = "sha256:8dc56b5b992d348ce09ace7b4faad00eb81b8803a02ffa2f18051bda93d800de"

[packages."github:flix/museum-clerk"."2.1.3"]
toml    = "sha256:6f34418fffc6c8d5614f32c1f904dbed385bc00e9ac7692e9cbe277fed54f66d"
fpkg    = "sha256:f7817d79093be36bcf9bf1ed66fa920d1e6eab6b1ac3759c1cc6581568b6ff8b"
```

The lock file records the digest of every file that the resolution read: the
`flix.toml` of every package at every version that the dependency graph requires,
and the package file of every package that is built. Here, the manifest of
`flix/museum-clerk` is recorded at both versions, but its package file only at
`2.1.3`, the version that is built. On a later build, Flix verifies each file against
the lock file as it is installed, and refuses to compile a dependency that is no
longer the same.

> **Tip:** The `packages.lock` file should be committed to version control.

> **Note:** The lock file records Flix packages only. Maven libraries and JAR-files
> downloaded from a URL are not covered by it.

## Finding Outdated Packages

We can check whether any of our Flix packages have newer releases with the
`outdated` command. For a project that depends on:

```toml
[dependencies]
"github:flix/museum"          = { version = "3.0.1", mount = "museum", security = "unrestricted" }
"github:flix/museum-giftshop" = { version = "2.0.1", mount = "giftshop" }
```

the `outdated` command reports:

```
package                 declared    built    major    minor    patch
flix/museum             3.0.1       3.0.1    4.0.0             3.0.2
flix/museum-giftshop    2.0.1       2.0.2
```

The package `flix/museum` has two updates available: we can upgrade from `3.0.1` to
`3.0.2` without changing major version, or to `4.0.0` across one.

The table has two version columns:

- `declared` is the version written in `flix.toml`.
- `built` is the version the package is actually built at, which can be greater: a
  declared version is the least version we can build with, and another dependent
  may require a greater one.

A package is compared by the version it is built at. Here, `flix/museum` requires
`flix/museum-giftshop` at `2.0.2`, its newest release, so there is nothing newer to
move to. It is listed all the same, because we declare an older version than the one
it is built at: we can declare `2.0.2` instead. When nothing is listed, Flix reports:

```
All dependencies are up to date
```

> **Tip:** The `outdated` command exits with status `1` when it lists a dependency,
> and with `0` otherwise, so it can fail a CI build.

> **Note:** Only Flix packages are listed. Maven dependencies are not checked.

## Upgrading a Package

We can upgrade a package by changing the `version` of its entry in `flix.toml`, or
with the `upgrade` command:

```
upgrade flix/museum
```

The `upgrade` command declares the newest release that has the same major version as
the one we declare, and tells us if there is a newer major version:

```
Upgraded 'flix/museum' v3.0.1 -> v3.0.2.

A newer major release is available, ask for it by name:
  flix upgrade flix/museum@4.0.0
```

A new major version may break our code, so `upgrade` only moves to one when we name
it:

```
upgrade flix/museum@4.0.0
```

A version that we name is taken as it is, so we can also name an older release to
move back to it. The `upgrade` command changes only the version: the mount and the
security context stay as we declared them.

We can name several packages, or none at all. With none, `upgrade` upgrades every
Flix package that the manifest declares, each within its major version, and reports
only the ones it changed. For the project in
[Finding Outdated Packages](#finding-outdated-packages), it reports:

```
Upgraded 'flix/museum' v3.0.1 -> v3.0.2.
Upgraded 'flix/museum-giftshop' v2.0.1 -> v2.0.2.

A newer major release is available, ask for it by name:
  flix upgrade flix/museum@4.0.0
```

The packages that one command upgrades are changed together or not at all. When two
packages must move to a new major version at the same time, because the new major
version of one requires the new major version of the other, we change both in one
edit of `flix.toml`, or name both in one `upgrade` command.
