## Packages

> **Note:** This section is a work in progress.

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

TBD


### Creating a GitHub Release 

1. Update `flix.toml` with the new version of the package.
2. Run `build-pkg`.
3. Create a new release on GitHub with the `.fpkg` and `.toml` files.

See the [Museum Project](https://github.com/flix/museum) for an example.

