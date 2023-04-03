# Build and Package Management

Flix comes with a build system and package manager. The build system makes it
simple to compile a Flix program to a collection of Java classes and to build a
fat JAR. The package manager makes it possible to create Flix packages, publish
them on GitHub, and depend on them via a manifest file. The package manager also
makes it possible to depend on Java JAR-artifacts published on Maven. 

The Flix build system supports the following commands:

- `init`: creates a new Flix project in the current directory.
- `check`: checks the current project for compiler errors.
- `build`: builds the current project (i.e. emits Java bytecode).
- `build-jar`: builds a jar-file from the current project. 
- `build-pkg`: builds a fpkg-file from the current project. 
- `run`: runs main in current project.  
- `test`: runs all tests in the current project.

All commands can be executed from the command line, from the REPL, and from
VSCode.

All commands, except `build-pkg` work without a manifest file. To build,
package, and publish a Flix project, a `flix.toml` manifest is required. The
`init` command will create an empty skeleton `flix.toml` manifest, if not
already present. 

## Project Structure

Flix scans for source files in the paths `*.flix`, `src/**.flix,`, and
`test/**.flix`.

Flix scans for Flix packages and JARs in the paths `lib/**.fpkg` and
`lib/**.jhar`.
