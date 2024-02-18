## Outdated

We can use the `outdated` command to check if any Flix packages have updates
available. 

For example, if we have the following dependency in `flix.toml`:

```toml
[dependencies]
"github:flix/museum"              = "1.3.0"
```

then we can run `outdated` command, which produces:

```shell
Found `flix.toml`. Checking dependencies...
Resolving Flix dependencies...
  Cached `flix/museum.toml` (v1.3.0).
  Cached `flix/museum-entrance.toml` (v1.2.0).  
  Cached `flix/museum-giftshop.toml` (v1.1.0).  
  Cached `flix/museum-restaurant.toml` (v1.1.0).
  Cached `flix/museum-clerk.toml` (v1.1.0).     
  Cached `flix/museum-clerk.toml` (v1.1.0).     
Downloading Flix dependencies...
  Cached `flix/museum.fpkg` (v1.3.0).
  Cached `flix/museum-entrance.fpkg` (v1.2.0).  
  Cached `flix/museum-giftshop.fpkg` (v1.1.0).  
  Cached `flix/museum-restaurant.fpkg` (v1.1.0).
  Cached `flix/museum-clerk.fpkg` (v1.1.0).     
  Cached `flix/museum-clerk.fpkg` (v1.1.0).     
Resolving Maven dependencies...
  Adding `org.apache.commons:commons-lang3' (v3.12.0).
  Running Maven dependency resolver.
Downloading external jar dependencies...
Dependency resolution completed.

package        current    major    minor    patch
flix/museum    1.3.0               1.4.0         
```

At the bottom, we can see that we are using `flix/museum` at version `1.3.0`,
but version `1.4.0` is available. 

