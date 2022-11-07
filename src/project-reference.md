# Project Reference

## Package Settings

The following is a list of settings that can be set at a package level.

### name

The name of the project.

**Required** for both application and library projects.

Used to create the name of the Jar of Fpkg file, so must be of a form that's compatible with major filesystems.

### version

The version number of the project.

**Required** for library projects.

Must follow [semantic versioning](https://semver.org) conventions. Note: this may be enforced by a future version of the compiler.

### flix

The version of Flix to be used when compiling.

**Required** for both library and application projects.

### license or license-file

The license (or licenses) that apply this this package.

**Required** for library projects.

Either license (as an [SPDX 2.1 license expression](https://spdx.dev/spdx-specification-21-web-version/#h.jxpfx0ykyb60)) or a `license-file` referencing a license text file.

### description

A textual description of the package.

**Required** for library projects.

### homepage

The URL for the project.

**Required** for library projects.

### source-paths

**Default:** `["src"]`

A list of directories to be used to search for `.flix` files.

### resource-paths

**Default:** `["resources"]`

A list of directories containing resources (files which will be included in the Jar or Fpkg).

> 🤔 Note: There are probably other things we could add to this list (e.g. source code repository URL, authors, ...) but I think that this is a good enough starting point.

### config

**Default:** `{ allow-holes = false, allow-debug = false }`

Configures compiler settings. Typically specified within build flavours (see below).

## Build Flavor-specfic Settings

Settings specific to a particular build flavour can be set by creating a `[build.<flavour>]` section. Settings within a build flavour override package settings, apart for array-valued settings (e.g. `src-paths` and `resource-paths`) where they add to the equivalent package setting.

The default build flavours are `prod` and `dev` with the following defaults:

```ini
[build.prod]
source-paths = ["prod"]
config = { allow-holes = false, allow-debug = false }

[build.dev]
source-paths = ["dev", "test", "bench"]
config = { allow-holes = true, allow-debug = true }
```
