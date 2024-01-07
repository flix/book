## Package Management

Every non-trivial Flix project should have a `flix.toml` manifest. The manifest
contains information about the project and its dependencies. 

A minimal manifest is of the form:

```toml
[package]
name        = "hello-library"
description = "A simple library"
version     = "0.1.0"
flix        = "0.35.0"
license     = "Apache-2.0"
authors     = ["John Doe <john@example.com>"]
```

> **Note:** The `flix` field is not yet used, but it will be used in the future. 

### Adding Flix Dependencies

We can add dependencies on other Flix packages to the manifest:

```toml
[dependencies]
"github:flix/museum"              = "1.4.0"
"github:magnus-madsen/helloworld" = "1.3.0"
```

> **Note:** Flix requires version numbers to follow SemVer.

### Adding Maven Dependencies

We can also add dependencies on Maven packages to the manifest:

```toml
[mvn-dependencies]
"org.junit.jupiter:junit-jupiter-api" = "5.9.2"
```

### Understanding Dependency Resolution

Flix dependency resolution works as follows:

1. Flix reads `flix.toml` and computes the transitive set of Flix package
   dependencies. 
2. Flix downloads all of these Flix packages.
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

This happens because `flix/museum` has the following dependency tree:

- `flix/museum` depends on:
    - `flix/museum-entrance` which depends on:
        - `flix/museum-clerk`
    - `flix/museum-giftshop` which depends on:
        - `flix/museum-clerk`
    - `flix/museum-restaurant` which depends on
        - `org.apache.commons:commons-lang3`
