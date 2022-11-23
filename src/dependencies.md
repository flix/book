# Dependencies

Flix supports two different types of dependency: Flix libraries (Fpkgs) and Jar files. Flix libraries are typically downloaded from GitHub and Jars from Maven (other repositories will be supported in the future).

# Specifying Dependencies

Dependencies shared by all build flavours are specified within the `[package.dependencies]` section of `flix.toml`. Dependencies specific to a particular build flavour are specified in `[build.<flavour>.dependencies]`, for example:

```ini
[package]
name = "example-flix-project"
version = "1.2.3"
flix = "0.31.0"

[package.dependencies]
mvn."org.postgresql:postgresql" = "42.3.3"
mvn."org.eclipse.jetty:jetty-server" = "11.0.11"
fpkg."com.github.paulbutcher/my-flix-library" = "0.3.1"

[build.dev.dependencies]
fpkg."com.github.example/debugging-helper" = "2.3.4"
```

This defines an application which depends upon two different Maven dependencies: `org.postgresql:postgresql` and `org.eclipse.jetty:jetty-server`, plus a single Fpgk: `com.github.paulbutcher/my-flix-library`. The development build also depends upon an additional Fpkg: `com.github.example/debugging-helper`.

> 🤔 Note: In [#4380](https://github.com/flix/flix/issues/4380) I proposed that we had "group-id/artifact".mvn, but I think I've convinced myself that the other way around works slightly better. Ultimately it doesn't really make much difference and we can pick whichever way round we think is best.

> 🤔 Note: I'm suggesting that we specify dependencies with the most natural separator for the type of dependency, so `:` for Maven and `/` for fpkg. We could alternatively use a common separator for both (probably `/`).

# Maven Dependencies

Maven dependencies are specified as a [_maven coordinate_](https://maven.apache.org/pom.html#Maven_Coordinates) of the form `groupId:artifactId`. In the simple case this maps onto a simple version number, but in the event that you need to deal with subdependency conflicts or reduce the size of the build, you can exclude subdependencies as follows:

```ini
[package.dependencies]
mvn."org.eclipse.jetty:jetty-server" = { version = "11.0.11", exclusions = ["org.slf4j:slf4j-api"] }
```

Maven dependencies are downloaded to your `~/.m2` directory and referenced directly on the classpath (i.e. if two different projects reference the same dependency, it is only downloaded once).

> 🤔 Note: Ultimately we'll have to handle all kinds of interesting edge cases like:
> 
> * Allowing different maven repositories over and above maven central
> * Support for authenticated repos
> * Maven proxies
> * Ability to configure the local repository
> * ...
> 
> But I suggest that we keep things simple to start with.

# Fpgk Dependencies

Flix library dependencies reference a GitHub release specified in the form `com.github.<org>/project`. The version number references a specific [release](https://docs.github.com/en/repositories/releasing-projects-on-github).

An Fpkg release comprises two files:

* An `.fpkg` file containing the compressed source code for the library.
* The library's `flix.toml` file which is used to determine metadata for the library.

Flix requires that a library specifies at least the following minimum set of metadata:

* Name
* Description
* Version
* License
* Homepage

Fpkg dependencies are downloaded to your `~/.fpkg` directory and referenced directly (i.e. if two different projects reference the same dependency, it is only downloaded once).

> 🤔 Note: I suspect that we might have to get users to authenticate with GitHub in the same manner as the [GitHub CLI](https://cli.github.com) because otherwise they're likely to be rate limited when accessing the GitHub API.

## Building Fpkg Dependencies

Imagine that we have a Flix library project with the following structure:

```svgbob
 |
 +- src
 |   |
 |   +- Example.flix
 |   '- Utils.flix
 |
 +- test
 |   |
 |   '- TestExample.flix
 |
 +- resources
 |   |
 |   '- ProductionData.json
 |
 +- dev
 |   |
 |   '- DebuggingData.json
 |
 +- flix.toml
 +- LICENSE.txt
 '- README.md
```

Here are the contents of its `flix.toml`:

```ini
[package]
name = "example-flix-library"
version = "2.3.4"
flix = "0.31.0"
license = "MIT OR Apache-2.0"
description = """
An example of a Flix library, distributed as an fpkg
"""
homepage = "https://github.com/org-name/example-flix-library"

[package.dependencies]
mvn."com.example:some-lib" = "1.2.3"
fpkg."com.example/another-flix-library" = "2.3.4"

[build.dev.dependencies]
fpkg."com.github.example/debugging-helper" = "3.4.5"
```

An Fpkg can be built from this with the following command:

```
% flix fpkg
```

Because the `fpkg` command uses the `prod` build flavour by default, the resulting package will contain the contents of the `src` and `resources` directories, but not the `test` or `dev` directories:

```svgbob
 |
 +- src
 |   |
 |   +- Example.flix
 |   '- Utils.flix
 |
 +- resources
 |   |
 |   '- ProductionData.json
 |
 +- flix.toml
 +- LICENSE.txt
 '- README.md
```

The Fpkg can be uploaded to a GitHub release with:

```
% flix release
```

> 🤔 Note: We'll definitely need to user to authenticate with GitHub for this!

# Semantic Versioning

Flix is opinionated on versioning and enforces [semantic versioning](https://semver.org) for Fpkg dependencies. In other words Flix assumes that version 1.3.4 of a library is backwardly compatible with (say) version 1.2.3 but that 2.1.2 is not.

A future version of the compiler will automatically detect and forbid changes to a library's public API which break semantic versioning. So it will not allow any changes to the public API for patch releases (e.g. from 1.2.3 to 1.2.4), and will not allow changes that are not backwardly compatible for minor releases (e.g. from 1.2.3 to 1.3.0).

# Dependency Resolution

Unlike (for example) [npm](https://docs.npmjs.com/cli) or [Cargo](https://doc.rust-lang.org/stable/cargo/index.html) version numbers in `flix.html` are specified exactly: you get precisely the version of the library referenced. There are no [version ranges, tildes, carets, or wildcards](https://doc.rust-lang.org/stable/cargo/reference/specifying-dependencies.html).

In the event that two dependencies both depend on the same sub-dependency, the most recent version specified will be used, as long as the versions they use are compatible according to semantic versioning.

For example, imagine that this is the `[package.dependencies]` section of our `flix.toml`:

```ini
[package.dependencies]
fpgk."com.example/frobnicate" = "1.2.3"
fpkg."com.example/munge" = "2.0.1"
```

Let's imagine that both Frobnicate and Munge depend upon a third library "Loggify". Perhaps Frobnicate depends upon version `1.0.1` and Munge depends upon version `1.2.3`. In this case, Flix will download and used version `1.2.3` because it's the most recent version and is backwards compatible with `1.0.1`.

But imagine that we upgrade to release `2.0.0` of Frobnicate which now depends upon Loggify `2.1.0`. Now Flix will raise an error because `2.1.0` is not backwardly compatible with the version of Loggify being used by Munge.

If you find yourself in this situation, you will either have to wait for your dependencies to be upgraded or, if testing demonstrates that the most recent version of the library works for your situation, you can override Flix's default behaviour by excluding the sub-dependency:

```ini
[package.dependencies]
fpgk."com.example/frobnicate" = { version = "2.0.0", exclusions = ["com.example/loggify"] }
fpkg."com.example/munge" = "2.0.1"
```

# Utilities

You can visualise a project's dependency tree with:

```
% flix dependencies
com.example/frobnicate: 2.0.0
  - com.example/loggify: 2.1.0 (excluded)
com.example/munge: 2.0.1
  - com.example/loggify: 1.2.3
```

You can see whether newer versions of dependencies are available with:

```
% flix outdated
com.example.frobnicate:
  Version in use: 1.2.3
  More recent patch version available: 1.2.4
  More recent minor version available: 1.3.0
```

And you can automatically update `flix.toml` with `flix upgrade`:

```
% flix upgrade --help
Usage: flix upgrade [--patch|--minor|--major]
Automatically upgrades dependencies to the most recent patch, minor, or major versions.
```
