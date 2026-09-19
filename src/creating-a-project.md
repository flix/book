# Creating a Project

A Flix project is a directory that contains a `flix.toml` manifest, Flix source
code in `src`, and tests in `test`.

We can create such a project with the `init` command. The command creates the
default project structure:

```
.
├── .github
│   └── workflows
│       └── build-and-test.yaml
├── .gitignore
├── flix.toml
├── LICENSE.md
├── README.md
├── src
│   └── Main.flix
└── test
    └── TestMain.flix

4 directories, 7 files
```

The three files we work in are `flix.toml`, `src/Main.flix`, and
`test/TestMain.flix`. The rest is a starting point we are meant to edit: a
`README.md` and a `LICENSE.md` with placeholder text, a `.gitignore`, and a
GitHub Actions workflow.

> **Tip:** The `init` command only creates the files that are not already there.
> It is safe to run in a directory that already has files, and we can run it in an
> existing project to add what is missing.

## The Manifest

The manifest describes the project. The one that `init` writes is minimal:

```toml
[package]
version = "0.1.0"
flix    = "0.76.2"

# repository = "github:<owner>/hello-world"
```

The `version` is the version of the project. The `flix` field is the oldest version
of Flix that can build the project, which `init` sets to the version of Flix we are
running. The `repository` field, which `init` leaves commented out, is the GitHub
repository we publish the project from, as described in
[Publishing a Package](./publishing-a-package.md).

The manifest grows with the project: we add a `[dependencies]` section when we
depend on other packages, as described in
[Using Dependencies](./using-dependencies.md).

> **Note:** Flix requires version numbers to follow [SemVer](https://semver.org/).

> **Note:** A package is named by the repository it is published from, and by
> nothing else. A manifest may still carry a `name` field, but Flix ignores it.

## Where Flix Looks for Source Code

Flix scans for source files in the paths `*.flix`, `src/**/*.flix`, and
`test/**/*.flix`. We are free to organize the files inside `src` and `test` as we
like: Flix finds them at any depth.

The generated `src/Main.flix` holds the entry point of the program:

```flix
// The main entry point.
def main(): Unit \ IO =
    println("Hello World!")
```

and the generated `test/TestMain.flix` holds a single test:

```flix
@Test
def test01(): Unit \ Assert = Assert.assertEq(expected = 2, 1 + 1)
```

A project may also have a `resources` directory. Flix does not compile what is in
it, but bundles it into the JAR-files we build, as described in
[Building Artifacts](./building-artifacts.md).

## What to Commit

Flix generates three directories: `build` holds class files and generated
documentation, `artifact` holds the JAR- and package-files we build, and `lib`
holds the dependencies Flix has downloaded. These directories should typically
_not_ be checked into version control, and the generated `.gitignore` already
excludes them:

```
*.fpkg
*.jar
.GITHUB_TOKEN
artifact/
build/
lib/
crash_report_*.txt
```

Flix also writes a `packages.lock` file next to `flix.toml`. The lock file records
what every dependency was when it was downloaded, and it *should* be committed,
which is why `.gitignore` does not exclude it. See
[Versions and Upgrades](./versions-and-upgrades.md#the-lock-file).

> **Warning:** A `.GITHUB_TOKEN` file is one of the places Flix looks for a GitHub
> token. It is excluded because a committed token can be used by anyone who can read
> the repository, and would have to be revoked at once.

## Checking and Testing on Every Push

The generated `.github/workflows/build-and-test.yaml` is a GitHub Actions workflow
that checks and tests the project on every push and pull request. It reads the
version of Flix from the `flix` field of `flix.toml`, downloads that version of
Flix, and runs `check` followed by `test`.
