## Publishing a Package on GitHub

Flix packages are published on GitHub.

### Automatically Publishing a Package

> **Note:** This feature requires Flix 0.44.0+

Flix can automatically package and publish artifacts on GitHub by following these steps:

1. Check that you have a `flix.toml` manifest (if not create one with `init`).
2. Check that the version field in `flix.toml` is correct.
3. Check that the repository field in `flix.toml` is correct. (e.g. `repository
   = "github:user/repo"`)
4. Check that you have a GitHub token which has read and write access to
   `Contents` for the relevant repository.
    - If not go to GitHub and navigate to `Settings > Developer settings >
   Personal access tokens` and create a new token.
5. Run `check` and `test` to ensure that everything looks alright.
6. Run `release --github-token <TOKEN>`. You should see:

```shell
Found `flix.toml'. Checking dependencies...
Resolving Flix dependencies...
Downloading Flix dependencies...
Resolving Maven dependencies...
  Running Maven dependency resolver.
Downloading external jar dependencies...
Dependency resolution completed.
Release github:user/repo v1.2.3? [y/N]: y
Building project...
Publishing new release...

 Successfully released v1.2.3
 https://github.com/user/repo/releases/tag/v1.2.3
```

> **Tip:** See the [Museum Project](https://github.com/flix/museum) for an
> example of a package that has been published on GitHub.

> **Tip:** Flix will read the GitHub token from the environment variable
> `GITHUB_TOKEN`, if available. 

> **Tip:** Flix will also read the GitHub token from the file `.GITHUB_TOKEN`,
> if available. 

> **Note:** You cannot publish artifacts for empty GitHub repositories.

> **Warning:** Be sure to keep your token safe!

### Manually Publishing a Package

A package can also be manually published by following these steps:

1. Check that you have a `flix.toml` manifest (if not create one with `init`).
2. Check that the version field in `flix.toml` is correct.
3. Run `check` and `test` to ensure that everything looks correct.
4. Run `build-pkg`. Check that the `artifact` directory is populated.
5. Go to the repository on GitHub:
    1. Click "Releases".
    2. Click "Draft new release".
    3. Enter a tag of the form `v1.2.3` (i.e. use SemVer).
    4. Upload the `package.fpkg` and `flix.toml` from the `artifact` directory.

> **Warning:** You must upload _both_ the package file  (`foo.fpkg`) and the
> manifest file (`flix.toml`).
