# Using Dependencies

A Flix project can depend on three kinds of things: Flix packages published on
GitHub, Java libraries published on Maven, and JAR-files downloaded from a URL. We
declare all three in the manifest, and Flix downloads them for us.

Ideally a Flix project depends on Flix packages only. A Flix package is compiled from
source, is built in a security context that limits what it may do, and is written in
the language we are writing. A Maven library, and even more so a JAR-file from a URL,
is a last resort: we should look for a Flix package first, and reach for Java only
when there is none.

## Two Ways to Declare a Dependency

The dependencies of a project are the ones its manifest declares. We can change them
in two ways, and both are equally valid: we edit `flix.toml` ourselves, or we run a
command that edits it for us.

| Task               | By editing `flix.toml`             | By running               |
|--------------------|------------------------------------|--------------------------|
| Add a Flix package | add its entry to `[dependencies]`  | `install <owner>/<repo>` |
| Change its version | change the `version` of its entry  | `upgrade <owner>/<repo>` |
| Remove it          | delete its entry                   | `remove <owner>/<repo>`  |

Each command can name several packages at once, as in
`install flix/museum-giftshop flix/museum-entrance`, and changes either all of them
or none.

Both ways give the same manifest, and we can mix them as we like. The sections below
show them side by side, and [How the Two Ways Differ](#how-the-two-ways-differ) sums
up what sets them apart.

## Adding a Flix Package

A dependency on a Flix package is an entry in the `[dependencies]` section of the
manifest:

```toml
[dependencies]
"github:flix/museum-giftshop" = { version = "2.0.2", mount = "giftshop" }
```

The key is the GitHub repository the package is published from. A dependency
declares two things: the `version` we require, and the `mount`, the name we reach
the package under. A dependency may also declare a `security` context, as
described in [Trusting Dependencies](./trusting-dependencies.md).

We can write this entry ourselves, or have Flix write it for us with the `install`
command:

```
install flix/museum-giftshop
```

The `install` command makes the choices that we otherwise make ourselves. It
declares the newest release of the package, unless we name a version, as in
`install flix/museum-giftshop@2.0.2`. It mounts the package under the name of its
repository if that name is a valid mount, and asks us for one otherwise:

```
github:flix/museum-giftshop is reached through a mount, as in 'use MuseumGiftshop::greet'.
Mount [MuseumGiftshop]: giftshop
```

We type the mount we want, or press Enter to take the one in brackets. With the
`--yes` option, `install` takes the one in brackets without asking. Once the
dependencies are resolved, `install` reports what it declared:

```
Added 'flix/museum-giftshop' v2.0.2, mounted at 'giftshop'.
```

Either way, Flix downloads the package and everything it depends on: `install` does
so right away, and for an entry we wrote ourselves, Flix does so the next time we run
a command, such as `check`:

```
Found 'flix.toml'. Checking dependencies...
Resolving Flix dependencies...
  Downloading `flix/museum-giftshop.toml` (v2.0.2)... OK.
  Downloading `flix/museum-clerk.toml` (v2.1.2)... OK.
Downloading Flix dependencies...
  Downloading `flix/museum-giftshop.fpkg` (v2.0.2)... OK.
  Downloading `flix/museum-clerk.fpkg` (v2.1.2)... OK.
Resolving Maven dependencies...
  Running Maven dependency resolver.
Downloading external jar dependencies...
Dependency resolution completed.
```

We asked for one package and got two: a Flix package brings its own dependencies
with it, and `flix/museum-giftshop` depends on `flix/museum-clerk`. Which version of
each package Flix picks is the subject of
[Versions and Upgrades](./versions-and-upgrades.md).

## Using a Mounted Package

A Flix package does not become part of our own namespace. Its modules live in a
namespace of their own, and we reach them through the package's *mount*, which we
write before `::` in a `use`:

```flix
use giftshop::Giftshop

def main(): Unit \ IO =
    Giftshop.buyGift()
```

The mount is declared in our own manifest, not by the package, so two projects may
reach the same package under different names.

> **Note:** A mount must be a simple name: a letter followed by letters, digits,
> and underscores. A repository whose name contains a hyphen therefore needs a
> different one, which is why `github:flix/museum-giftshop` is mounted as
> `giftshop`, and why `install` asks for its mount.

> **Note:** The `::` can be written in a `use` only. We cannot write
> `giftshop::Giftshop.buyGift()` in an expression, nor `giftshop::Giftshop` in a
> type.

> **Note:** Only the `pub` declarations of a package can be reached. A module that
> a package does not declare `pub` is private to it.

## Removing a Flix Package

We can remove a Flix package by deleting its entry from `[dependencies]`, or with
the `remove` command:

```
remove flix/museum-giftshop
```

which reports:

```
Removed 'flix/museum-giftshop' v2.0.2, which was mounted at 'giftshop'.
```

Either way, we can only remove a package that our manifest declares. A package that
is reached through another dependency, like `flix/museum-clerk` here, is declared by
that dependency, and goes away with it.

The files that Flix downloaded for a removed package stay in the `lib` directory,
where they are ignored, as described in [The lib Directory](#the-lib-directory).

## How the Two Ways Differ

Both ways declare the same dependency. They differ in who makes the choices, and in
when the change takes effect:

|                     | Editing `flix.toml`                          | Running a command                                      |
|---------------------|----------------------------------------------|--------------------------------------------------------|
| Version             | we choose it                                 | the newest release, or the one we name                 |
| Mount               | we choose it                                 | the name of the repository, or the one we answer with  |
| Security context    | we choose it                                 | none, which means `plain`                              |
| Takes effect        | the next time we run a command, e.g. `check` | right away                                             |
| If resolution fails | the error is reported, and our edit stays    | the error is reported, and `flix.toml` is put back     |
| Covers              | Flix packages, Maven, and JAR-dependencies   | Flix packages only                                     |

The version, mount, and security rows describe `install`. The `upgrade` command
changes only the version, and stays within the major version unless we name another,
as described in [Versions and Upgrades](./versions-and-upgrades.md#upgrading-a-package).

A package that must be trusted with a security context other than `plain`, such as
`flix/museum` in [Versions and Upgrades](./versions-and-upgrades.md), is therefore
declared by editing the manifest.

## Adding a Maven Dependency

We can add a dependency on a Java library published on Maven in the
`[mvn-dependencies]` section:

```toml
[mvn-dependencies]
"org.apache.commons:commons-lang3" = "3.12.0"
```

> **Note:** There is no command for Maven- or JAR-dependencies. We declare them by
> editing `flix.toml`.

Flix hands the section to a Maven dependency resolver, which downloads the library
together with the libraries it depends on:

```
Resolving Maven dependencies...
  Adding `org.apache.commons:commons-lang3' (v3.12.0).
  Running Maven dependency resolver.
```

We then use the library as we use any other Java library, as described in
[Interoperability with Java](./interoperability.md):

```flix
import org.apache.commons.lang3.StringUtils

def main(): Unit \ IO =
    println(StringUtils.reverse("Hello World!"))
```

## Adding a JAR-file from a URL

We can depend on a JAR-file that is downloaded from a URL in the
`[jar-dependencies]` section. The key is the file name the JAR-file is saved under,
which must end in `.jar`:

```toml
[jar-dependencies]
"commons-lang3.jar" = "url:https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar"
```

Flix downloads it while it resolves the dependencies:

```
Downloading external jar dependencies...
  Downloading `commons-lang3.jar` from `https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar`... OK.
```

> **Warning:** A JAR-dependency is whatever the URL serves, from wherever it points.
> We should avoid external JAR-dependencies: a Flix package is better, and a Maven
> library is better than a URL.

## The lib Directory

Flix places what it downloads in the `lib` directory: Flix packages under
`lib/github`, Maven libraries in `lib/cache`, and JAR-files downloaded from a URL
in `lib/external`. Every Flix package is kept under its repository and version:

```
lib
└── github
    └── flix
        ├── museum-clerk
        │   └── 2.1.2
        │       ├── museum-clerk-2.1.2.fpkg
        │       └── museum-clerk-2.1.2.toml
        └── museum-giftshop
            └── 2.0.2
                ├── museum-giftshop-2.0.2.fpkg
                └── museum-giftshop-2.0.2.toml
```

The `lib` directory is managed by Flix and should not be committed. It is not
scanned: Flix loads the dependencies that `flix.toml` declares, and nothing else,
so a package or JAR-file we place in `lib` by hand is ignored, and so is what a
removed package leaves behind.
