# Finding Outdated Packages

We can use the `outdated` command to check if any Flix packages have updates
available.

For example, if we have the following dependency in `flix.toml`:

```toml
[dependencies]
"github:flix/museum-giftshop" = { version = "1.0.0", mount = "giftshop" }
```

then we can run the `outdated` command which will produce:

```shell
Found 'flix.toml'. Checking dependencies...
Resolving Flix dependencies...
  Cached `flix/museum-giftshop.toml` (v1.0.0).
  Cached `flix/museum-clerk.toml` (v1.0.0).
Downloading Flix dependencies...
  Cached `flix/museum-clerk.fpkg` (v1.0.0).
  Cached `flix/museum-giftshop.fpkg` (v1.0.0).
Resolving Maven dependencies...
  Running Maven dependency resolver.
Downloading external jar dependencies...
Dependency resolution completed.

package                 declared    built    major    minor    patch
flix/museum-giftshop    1.0.0       1.0.0    2.0.0    1.1.0
```

The `outdated` command tells us that `flix/museum-giftshop` has two updates
available: we can upgrade from `1.0.0` to `1.1.0` without changing major version,
or to `2.0.0` across one.

The table has two version columns:

- `declared` is the version written in `flix.toml`.
- `built` is the version the package is actually built at, which can be greater:
  a declared version is the *least* version we can build with, and another
  dependent may require a greater one. See
  [Package Management](./packages.md#understanding-version-selection).

A package is compared by the version it is built at. A dependency that is built
at its newest release is therefore up to date, and is not listed, even if the
version we declare is older.

Only Flix packages are listed. Maven dependencies are not checked.

If we want to upgrade a package, we must manually modify `flix.toml`.
