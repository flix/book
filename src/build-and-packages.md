# Build and Package Management

The Flix compiler ships with a built-in build system and package manager. The
Flix build system makes it easy to create, compile, run, and test a Flix
project. The Flix package manager makes it possible to create packages, publish
them on GitHub, and depend on them. The package manager also supports
Maven-style dependencies. 

The Flix build system supports the following commands:

- `init`: Creates a new project in the current directory.
- `check`: Checks the current project to check for errors.
- `build`: Builds (i.e. compiles) the current project.
- `build-jar`: Builds a jar-file from the current project. 
- `build-pkg`: Builds a fpkg-file from the current project. 
- `run`: Runs main for the current project.  
- `test`: Runs tests for the current project.

A Flix package is Flix project that contains a `flix.toml` manifest which
specifies the name of the package, its version, and its dependencies. As stated,
Flix packages can depend on other Flix packages and on Maven dependencies. 

Flix packages are published as releases on GitHub.

