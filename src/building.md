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

* **Production:** A production build is used when building a release. Production builds:
  * Do not include either tests or benchmarks.
  * Disallow the use of [debugging](./debugging.md) functions and [holes](./holes.md).
* **Development:** The development build is similar to the production build, but differs from it in ways which make it easier to debug, for example:
  * Tests and benchmarks are included in the build.
  * [Debugging](./debugging.md) functions and [holes](./holes.md) are allowed.
  * A development build of a web application might allow insecure connections (i.e. over HTTP instead of HTTPS).
  * A development build may be configured to communicate with a different instance of a database or third-party service.

A project defines a base set of source files, resources, dependencies, and configuration in its `[package]` section which applies across all different build flavours. These can then be added to or overridden within `[build.prod]`, `[build.dev]`, etc.

The following shows the default settings:

```ini
[package]
source-paths = ["src"]
resource-paths = ["resources"]

[build.prod]
source-paths = ["prod"]
config = { allow-holes = false, allow-debug = false }

[build.dev]
source-paths = ["dev", "test", "bench"]
config = { allow-holes = true, allow-debug = true }
```

So both production and development builds include all source files within the `src` directory, and resources within the `resources` directory. Production builds add the `prod` directory (so the complete set of source paths is `["src", "prod"]`) and disable both holes and debugging functions. Development builds add the `dev`, `test`, and `bench` directories (so the complete set of source paths is `["src", "dev", "test", "bench"]`) and enable both holes and debugging functions.

## Building

The flix command allows the build flavour to be specified through the `--build` or `-B` command line arguments, so the following builds the development version of a project and starts the REPL:

```
% flix --build dev repl
     __   _   _
    / _| | | (_)            Welcome to Flix v0.33.0
   | |_  | |  _  __  __
   |  _| | | | | \ \/ /     Enter an expression to have it evaluated.
   | |   | | | |  >  <      Type ':help' for more information.
   |_|   |_| |_| /_/\_\     Type ':quit' or press 'ctrl + d' to exit.
      
flix>                                                                           
```

Which can be shortened to just `flix` as the default flavour is `dev` and the default command is `repl`.

A production JAR would be built with:

```
% flix --build prod jar
```

Which can be shortened to just `flix jar` as the `jar` command uses the `prod` flavour by default.
