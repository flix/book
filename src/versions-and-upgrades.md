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

The example in [Using Dependencies](./using-dependencies.md) downloads five
packages from a single dependency, because `flix/museum` has this dependency tree:

- `flix/museum` depends on:
    - `flix/museum-clerk` (v2.1.0)
    - `flix/museum-entrance` which depends on:
        - `flix/museum-clerk` (v2.0.0)
    - `flix/museum-giftshop` which depends on:
        - `flix/museum-clerk` (v2.0.0)
    - `flix/museum-restaurant` which depends on
        - `org.apache.commons:commons-lang3`

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
`2.1.0`, whereas `flix/museum-entrance` and `flix/museum-giftshop` require it at
`2.0.0`. Flix builds it at `2.1.0` and reports that it did so:

```
  Raised `flix/museum-clerk` (v2.0.0 -> v2.1.0), required by `flix/museum` (v2.1.0).
```

**A package is built at one version only.** If a project transitively depends on two
different major versions of the same package, then no single version satisfies every
dependent, and Flix reports an error. For example, if one dependent required
`flix/museum-clerk` at `1.1.0` while another required it at `2.1.0`:

```
Found incompatible versions of the same package in the dependency graph:
  The package 'github:flix/museum-clerk' is required at versions that do not share a major version:

    1.1.0 required by 'flix/museum-giftshop'
    2.1.0 required by 'flix/museum'

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
The package 'github:flix/museum' 2.1.0 requires Flix version 0.76.2, but the current version is 0.76.1.
Please upgrade to Flix 0.76.2 or newer.
```

## The Lock File

When Flix resolves the dependencies of a project, it writes a `packages.lock` file
next to `flix.toml`:

```toml
[lock]
version = 1

[packages."github:flix/museum-clerk"."1.0.0"]
toml    = "sha256:af31faa57878e01363946f2b82df193bd5cc939ce0c5235c6e125ab727bbe35d"
fpkg    = "sha256:ed9210a2088e9a31d4406d4e1306737c68fb3080f7d5a1c11e7316b780bb5704"

[packages."github:flix/museum-giftshop"."1.0.0"]
toml    = "sha256:d1e5db83f30efa1ef8b16911a6d7289d87cba33bb8ec4f70d4c4f0af763482e8"
fpkg    = "sha256:49349a6c68d3b4c0636e0dd0215e4d3099edc6ab06565960fd525575e5790bf2"
```

The lock file records the digest of every file that the resolution read: the
`flix.toml` of every package at every version that the dependency graph requires,
and the package file of every package that is built. On a later build, Flix verifies
each file against the lock file as it is installed, and refuses to compile a
dependency that is no longer the same.

> **Tip:** The `packages.lock` file should be committed to version control.

> **Note:** The lock file records Flix packages only. Maven libraries and JAR-files
> downloaded from a URL are not covered by it.

## Finding Outdated Packages

We can check whether any of our Flix packages have newer releases with the
`outdated` command. For a project that depends on:

```toml
[dependencies]
"github:flix/museum-giftshop" = { version = "1.0.0", mount = "giftshop" }
```

the `outdated` command reports:

```
package                 declared    built    major    minor    patch
flix/museum-giftshop    1.0.0       1.0.0    2.0.0    1.1.0
```

The package `flix/museum-giftshop` has two updates available: we can upgrade from
`1.0.0` to `1.1.0` without changing major version, or to `2.0.0` across one.

The table has two version columns:

- `declared` is the version written in `flix.toml`.
- `built` is the version the package is actually built at, which can be greater: a
  declared version is the least version we can build with, and another dependent
  may require a greater one.

A package is compared by the version it is built at. A dependency that is built at
its newest release is therefore up to date, and is not listed, even if the version
we declare is older. When nothing is outdated, Flix reports:

```
All dependencies are up to date
```

To upgrade a package, we change the version in `flix.toml` ourselves. Flix does not
edit the manifest for us.

> **Note:** Only Flix packages are listed. Maven dependencies are not checked.
