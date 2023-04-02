## Packages

### The `flix.toml` Manifest

Flix packages are identified by a manifest file called `flix.toml`.

A minimal manifest could be:

```toml
[package]
name        = "hello-library"                   # The name of the package.
description = "A simple library"                # The description of the package.
version     = "0.1.0"                           # The semantic version of the package.
flix        = "0.33.0"                          # The required version of the Flix compiler.
license     = "Apache-2.0"                      # The license applicable to this project (see also LICENSE.md).
authors     = ["John Doe <john@example.com>"]   # The authors of this project.
```

### Flix Dependencies

```toml
[dependencies]                                  # Dependencies on Flix packages.
"github:flix/museum"              = "1.1.0"
"github:magnus-madsen/helloworld" = "1.3.0"
```

### Maven Dependencies

```toml
[mvn-dependencies]                              # Dependencies on Maven packages.
"org.junit.jupiter:junit-jupiter-api" = "5.9.2"
```

### Understanding Dependency Resolution

Flix dependency resolution works as follows:

1. Flix reads `flix.toml` and compute the transitive set of Flix package dependencies. 
2. Flix downloads all these Flix packages.
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

The run shows the following dependency tree:

- the `flix/museum` package depends on:
    - the `flix/museum-entrance` package which depends on:
        - the `flix/museum-clerk` package which has no dependencies.
    - the `flix/museum-giftshop` package which depends on:
        - the `flix/museum-clerk` package which has no dependencies.
    - the `flix/museum-restaurant` package which depends on
        - the `org.apache.commons:commons-lang3` Maven package.

### Publishing a Package on GitHub

Creating and publish a package on GitHub is straightforward: 

1. Check that you have `flix.toml` manifest (if not create on with `init`).
2. Check that the version field in `flix.toml` is correct.
3. Run `check` and `test` to ensure that everything looks alright.
4. Run `build-pkg`. Check that the `artifact` directory is populated.
5. Go to the repository on GitHub:
    1. Click "Releases".
    2. Click "Draft new release".
    3. Enter a tag of the form `v1.2.3` (i.e. SemVer).
    4. Upload `package.fpkg` and `flix.toml` from the `artifact` directory.

> **Tip:** See the [Museum Project](https://github.com/flix/museum) for an
> example of a package that has been published on GitHub.
