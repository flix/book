# Building a Flix Project

## Components of a Flix Project

A project is built from the following components:

* **Source Files:** A collection of `.flix` files containing Flix source code.
* **Resources:** Resources can be any type of file, but typically include:
  * HTML, CSS, etc.
  * Images
  * Data/configiguration (e.g. JSON, CSV, etc.)
* **Dependencies:** Libraries upon which this project depends. Flix supports two different types of dependency:
  * **Flix Libraries:** Flix library projects which themselves consist of source files, resources, and potentially further dependencies.
  * **JAR Files:** Java libraries packaged as JAR files.
* **Configuration:** Settings which modify the behaviour of the compiler.

The primary job of `FlixProject.toml` is, therefore, to specify how we should find the source code, resources, and dependencies that should be used to build our project.

## Build Flavours

A project can be built in multiple different flavours. By default these are:

* **Production:** A production build is used when building an application for release. Production builds:
  * Do not include either tests or benchmarks.
  * Disallow the use of [debugging](./debugging.md) functions and [holes](./holes.md).
* **Development:** The development build is similar to the production build, but differs from it in ways which make it easier to debug, for example:
  * [Debugging](./debugging.md) functions and [holes](./holes.md) are allowed.
  * A development build of a web application might allow insecure connections (i.e. over HTTP instead of HTTPS).
  * A development build may be configured to communicate with a different instance of a database or third-party service.
* **Testing:** Used when running tests.
* **Benchmark:** Used when running benchmarks.
* **Fpkg:** Used to build a Flix library for distribution.
  * Similarly to a production build, Flix packages may not include either [debugging](./debugging.md) functions and [holes](./holes.md).

A project defines a base set of source files, resources, dependencies, and configuration in its `[package]` section which applies across all different build flavours. These can then be added to or overridden within `[build.prod]`, `[build.dev]`, etc.

The following shows the default settings:

```ini
[package]
source-paths = ["src"]
resource-paths = ["resources"]

[build.dev]
source-paths = ["dev"]
config = { allow-holes = true, allow-debug = true }

[build.prod]
source-paths = ["prod"]
config = { allow-holes = false, allow-debug = false }

[build.test]
source-paths = ["test"]
config = { allow-holes = true, allow-debug = true }

[build.bench]
source-paths = ["bench"]
config = { allow-holes = true, allow-debug = true }

[build.fpkg]
source-paths = ["prod"]
config = { allow-holes = false, allow-debug = false }
```
