# Publishing a Package

Flix packages are published on GitHub. A release holds two files: the package file
that `build-pkg` builds, and the manifest that describes it. Whoever depends on the
package downloads both.

## Preparing the Manifest

A package that is published on GitHub must declare the repository it is published
from:

```toml
[package]
name       = "museum"
version    = "2.1.0"
flix       = "0.76.2"
repository = "github:flix/museum"
```

Before we release, we check three things:

1. That the `version` field is the version we mean to release.
2. That the `repository` field names the repository we release to.
3. That `check` and `test` both pass.

## Releasing with the release Command

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

Flix builds the package, creates a release tagged `v1.2.3`, and uploads the package
file and the manifest to it.

> **Tip:** Flix looks for the GitHub token in three places, in order: the
> `--github-token` option, a `.GITHUB_TOKEN` file in the project directory, and the
> `GITHUB_TOKEN` environment variable.

> **Tip:** The `--yes` option answers the confirmation prompt for us, which is what
> we want when we release from a script or from CI.

> **Warning:** Be sure to keep the token safe. The generated `.gitignore` excludes
> `.GITHUB_TOKEN` so that we do not commit it by accident.

> **Note:** We cannot publish a release for an empty GitHub repository.

## Publishing Manually

We can also publish a release by hand:

1. Run `check` and `test` to ensure that everything looks correct.
2. Run `build-pkg` and check that the `artifact` directory is populated.
3. Go to the repository on GitHub:
    1. Click "Releases".
    2. Click "Draft new release".
    3. Enter a tag of the form `v1.2.3`, i.e. use SemVer.
    4. Upload the package file and the `flix.toml` from the `artifact` directory.

> **Warning:** We must upload _both_ the package file (`museum.fpkg`) and the
> manifest file (`flix.toml`). A release that holds only one of them cannot be
> resolved.

> **Tip:** See the [Museum Project](https://github.com/flix/museum) for an example of
> a package that has been published on GitHub.

## What a Package Promises

Two fields of the manifest are promises to whoever depends on the package:

- The `version` field must match the tag the package is released under. A release of
  `v1.2.3` whose manifest declares another version is rejected when it is resolved,
  and only its author can fix it.
- The `flix` field must be the oldest version of Flix that can build the package.
  Flix refuses to build a package that requires a newer version than the one that is
  running, so raising this field in a new release excludes everyone who has not
  upgraded.

A published package is compiled from source by whoever depends on it, so only its
`pub` declarations can be reached. Every module our dependents are meant to use must
be declared `pub`.

> **Note:** Version numbers must follow [SemVer](https://semver.org/), and a package
> is built at one version only. A breaking change therefore belongs in a new major
> version, as described in [Versions and Upgrades](./versions-and-upgrades.md).
