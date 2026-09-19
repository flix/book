# Using Dependencies

A Flix project can depend on three kinds of things: Flix packages published on
GitHub, Java libraries published on Maven, and JAR-files downloaded from a URL. We
declare all three in the manifest, and Flix downloads them for us.

Ideally a Flix project depends on Flix packages only. A Flix package is compiled from
source, is built in a security context that limits what it may do, and is written in
the language we are writing. A Maven library, and even more so a JAR-file from a URL,
is a last resort: we should look for a Flix package first, and reach for Java only
when there is none.

## Adding a Flix Package

We can add a dependency on a Flix package in the `[dependencies]` section of the
manifest:

```toml
[dependencies]
"github:flix/museum" = { version = "2.1.0", mount = "museum" }
```

The key is the GitHub repository the package is published from. A dependency
declares two things: the `version` we require, and the `mount`, the name we reach
the package under. A dependency may also declare a `security` context, as
described in [Trusting Dependencies](./trusting-dependencies.md).

The next time we run a command, Flix downloads the package and everything it
depends on:

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

We asked for one package and got five: a Flix package brings its own dependencies
with it. Which versions Flix picks, and why the manifest of `flix/museum-clerk` is
downloaded twice, is the subject of
[Versions and Upgrades](./versions-and-upgrades.md).

## Using a Mounted Package

A Flix package does not become part of our own namespace. Its modules live in a
namespace of their own, and we reach them through the package's *mount*, which we
write before `::` in a `use`:

```flix
use museum::Museum

def main(): Unit \ IO =
    Museum.visitMuseum()
```

We choose the mount ourselves, in our own manifest, so two projects may reach the
same package under different names.

> **Note:** A mount must be a simple name: a letter followed by letters, digits,
> and underscores. A repository whose name contains a hyphen therefore needs a
> different one, which is why `github:flix/museum-clerk` is mounted as `clerk`.

> **Note:** The `::` can be written in a `use` only. We cannot write
> `museum::Museum.visitMuseum()` in an expression, nor `museum::Museum` in a type.

> **Note:** Only the `pub` declarations of a package can be reached. A module that
> a package does not declare `pub` is private to it.

## Adding a Maven Dependency

We can add a dependency on a Java library published on Maven in the
`[mvn-dependencies]` section:

```toml
[mvn-dependencies]
"org.apache.commons:commons-lang3" = "3.12.0"
```

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
        └── museum
            └── 2.1.0
                ├── museum-2.1.0.fpkg
                └── museum-2.1.0.toml
```

The `lib` directory is managed by Flix and should not be committed. It is not
scanned: Flix loads the dependencies that `flix.toml` declares, and nothing else,
so a package or JAR-file we place in `lib` by hand is ignored.
