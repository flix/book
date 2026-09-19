# Publishing a Package

Flix packages are published on GitHub. A release holds two files, which are the two
files that `build-pkg` leaves in the `artifact` directory: `package.fpkg`, the package
itself, and `flix.toml`, the manifest that describes it. Whoever depends on the package
downloads both.

## Preparing the Manifest

A package that is published on GitHub must declare the repository it is published
from:

```toml
[package]
version    = "2.1.0"
flix       = "0.76.2"
repository = "github:flix/museum"
```

Flix builds and uploads the package for us, but it cannot tell whether the manifest
says what we meant. We — as the developer — must check three things before we release:

1. That the `version` field is the version we mean to release, and that we have not
   released it before. A version is published once and cannot be changed afterwards.
2. That the `repository` field names the repository we release to. It is the name our
   dependents write to depend on the package.
3. That `check` and `test` both pass. The `release` command builds the package, which
   means the project has to compile, but it does not run the tests for us.

## Publishing with the `release` Command

Flix can package and publish a release for us with the `release` command. The
command needs a GitHub token that has read and write access to `Contents` for the
repository, which we create under `Settings > Developer settings > Personal access
tokens` on GitHub.

We can then run `release --github-token <TOKEN>`:

```
Found 'flix.toml'. Checking dependencies...
Resolving Flix dependencies...
Downloading Flix dependencies...
Resolving Maven dependencies...
  Running Maven dependency resolver.
Downloading external jar dependencies...
Dependency resolution completed.
Release github:user/repo v1.2.3? [y/N]: y
Building project...
Publishing a new release...

Successfully released v1.2.3
https://github.com/user/repo/releases/tag/v1.2.3
```

Flix builds the package, creates a release tagged `v1.2.3`, and uploads the two files
of the release to it: `package.fpkg` and `flix.toml`.

> **Tip:** Flix looks for the GitHub token in three places, in order: the
> `--github-token` option, a `.GITHUB_TOKEN` file in the project directory, and the
> `GITHUB_TOKEN` environment variable.

> **Tip:** The `--yes` option answers the confirmation prompt for us, which is what
> we want when we release from a script or from CI.

> **Warning:** Be sure to keep the token safe. The generated `.gitignore` excludes
> `.GITHUB_TOKEN` so that we do not commit it by accident.

> **Note:** We cannot publish a release for an empty GitHub repository.

> **Tip:** See the [Museum Project](https://github.com/flix/museum) for an example of
> a package that has been published on GitHub.

## Versioning a Package

Two version numbers in the manifest follow [SemVer](https://semver.org/), and they say
different things.

The `version` field is the version of the package itself. Which part we increment tells
our dependents what kind of change to expect:

- A **patch** release, `1.2.3` to `1.2.4`, fixes something and leaves the API alone.
- A **minor** release, `1.2.3` to `1.3.0`, adds to the API without breaking what was
  already there.
- A **major** release, `1.2.3` to `2.0.0`, changes or removes something that dependents
  may rely on.

Here the distinction is not only a convention: it is what dependency resolution runs on.
Flix builds a package at one version, which must be at or above what every dependent
requires and have the same major version. A patch or a minor release is therefore
something our dependents can take without thinking, whereas a major release is a step
each of them has to make deliberately, as described in
[Versions and Upgrades](./versions-and-upgrades.md). That is also what the three columns
of `outdated` separate.

The `flix` field is the oldest version of the Flix compiler that can build the package.
Flix compares it against the compiler that is running, and refuses to build a package
that wants a newer one, so raising this field shuts out every dependent that has not
upgraded yet. We raise it when the package needs something a newer compiler provides,
and preferably in a minor or a major release rather than in a patch.

> **Note:** Flix itself is at major version `0`, so its own minor releases may change
> the language. The `flix` field is a lower bound only: Flix assumes that a newer
> compiler can build a package that asks for an older one.

## What a Package Promises

Two fields of the manifest are promises to whoever depends on the package:

- The `version` field must match the tag the package is released under. A release of
  `v1.2.3` whose manifest declares another version is rejected when it is resolved,
  and only its author can fix it.
- The `flix` field must be the oldest version of Flix that can build the package. A
  package that declares a newer version than it needs excludes dependents for no
  reason; one that declares an older version than it needs does not compile for them.

A published package is compiled from source by whoever depends on it, so only its
`pub` declarations can be reached. Every module our dependents are meant to use must
be declared `pub`.
