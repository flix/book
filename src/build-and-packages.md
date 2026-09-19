# Build and Package Management

Flix comes with a build system and package manager. The build system makes it
simple to compile a Flix program to a collection of Java classes and to build a
fat JAR. The package manager makes it possible to create Flix packages, publish
them on GitHub, and depend on them via a manifest file. The package manager also
makes it possible to depend on Java JAR-artifacts published on Maven. 

The Flix build system supports the following commands:

- `init`: creates a new Flix project in the current directory.
- `check`: checks the current project for compiler errors.
- `build`: builds (i.e. compiles) the current project.
- `build-classes`: builds the current project and writes the class files to the `build` directory.
- `build-jar`: builds a jar-file from the current project. 
- `build-fatjar`: builds a jar-file with all dependencies bundled.
- `build-pkg`: builds a fpkg-file from the current project. 
- `clean`: removes the `build` directory.
- `doc`: generates API documentation for the current project.
- `format`: formats the Flix source files of the current project.
- `outdated`: shows dependencies which have newer versions available.
- `release`: releases a new version of the current project to GitHub.
- `run`: runs main in current project.  
- `test`: runs all tests in the current project.

All commands can be executed from the command line, from the REPL, and from
VSCode.

All commands, except `build-pkg`, `clean`, and `release`, work without a manifest
file. To build, package, and publish a Flix project, a `flix.toml` manifest is
required. The `init` command will create an empty skeleton `flix.toml` manifest,
if not already present. 

## Project Structure

Flix scans for source files in the paths `*.flix`, `src/**/*.flix,`, and
`test/**/*.flix`.

Flix places the dependencies declared in `flix.toml` into the `lib` directory:
Flix packages in `lib`, Maven JAR-artifacts in `lib/cache`, and JAR-files
downloaded from a URL in `lib/external`. The directory is not scanned: Flix loads
the dependencies that `flix.toml` declares, and nothing else, so a package or
JAR-file placed in `lib` by hand is ignored.

The `lib` directory is managed by Flix and should not be committed.

A project with dependencies also has a `packages.lock` file next to its
`flix.toml`. It records what every dependency was when it was downloaded, and it
should be committed. See [Packages](./packages.md#the-lock-file).
