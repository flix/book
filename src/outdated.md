## Finding Outdated Packages

We can use the `outdated` command to check if any Flix packages have updates
available. 

For example, if we have the following dependency in `flix.toml`:

```toml
[dependencies]
"github:flix/museum"            = "1.0.0"
"github:flix/museum-giftshop"   = "1.0.0"
```

then we can run `outdated` command which will produce:

```shell
Found `flix.toml`. Checking dependencies...
Resolving Flix dependencies...
  Cached `flix/museum.toml` (v1.0.0).
  Cached `flix/museum-giftshop.toml` (v1.0.0).  
  Cached `flix/museum-entrance.toml` (v1.0.0).  
  Cached `flix/museum-giftshop.toml` (v1.0.0).  
  Cached `flix/museum-restaurant.toml` (v1.0.0).
  Cached `flix/museum-clerk.toml` (v1.0.0).     
  Cached `flix/museum-clerk.toml` (v1.0.0).
Downloading Flix dependencies...
  Cached `flix/museum.fpkg` (v1.0.0).
  Cached `flix/museum-giftshop.fpkg` (v1.0.0).
  Cached `flix/museum-entrance.fpkg` (v1.0.0).
  Cached `flix/museum-giftshop.fpkg` (v1.0.0).
  Cached `flix/museum-restaurant.fpkg` (v1.0.0).
  Cached `flix/museum-clerk.fpkg` (v1.0.0).
  Cached `flix/museum-clerk.fpkg` (v1.0.0).
Resolving Maven dependencies...
  Running Maven dependency resolver.
Downloading external jar dependencies...
Dependency resolution completed.

package                 current    major    minor    patch
flix/museum             1.0.0               1.4.0         
flix/museum-giftshop    1.0.0               1.1.0         
```

The `outdated` command tells us that we are using two packages which have
updates available:

- `flix/museum` can be upgraded from `1.0.0` to `1.4.0`.
- `flix/museum-giftshop` can be upgraded from `1.0.0` to `1.1.0`.

If we want to upgrade a package, we must manually modify `flix.toml`.
