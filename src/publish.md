## Publishing a Package on GitHub

Flix packages can be published on GitHub.

### Automatically Publishing a Package

> **Note:** This feature requires Flix 0.44.0+

Flix can automatically package and publish artifacts to GitHub.

Follows these steps to create and publish a package from scratch. Let us assume
your GitHub username is `obelix` and you want to create and publish the
repository `obelix/magicpotion`. 

1. Create the GitHub repository (e.g. `obelix/magicpotion`)
2. Run `init` in the project folder (either from VSCode or from the command line).
3. Update `name` and `version` in `flix.toml` (e.g. `name = "magicpotion"` and
   `version = "1.2.3"`)
4. Add a `repository = "github:user/repo"` property. (e.g. `repository =
   "github:obelix/magicpotion"`).
4. Goto [GitHub](https://github.com/) and navigate to `Settings > Developer
   settings > Personal access tokens`. Create a new token and ensure it has read
   and write access to contents. Let us assume the token is
   `github_pat_11AAROSUI0...XYZ`.
5. Run `check` and `test` to ensure that everything looks alright.
6. Run `release --github-key github_pat_11AAROSUI0...XYZ`. You should see:

```shell
Found `flix.toml'. Checking dependencies...
Resolving Flix dependencies...
Downloading Flix dependencies...
Resolving Maven dependencies...
  Running Maven dependency resolver.
Downloading external jar dependencies...
Dependency resolution completed.
Release github:obelix/magicpotion v1.2.3? [y/N]: y
Building project...
Publishing new release...

 Successfully released v1.2.3
 https://github.com/obelix/magicpotion/releases/tag/v1.2.3
```

> **Tip:** See the [Museum Project](https://github.com/flix/museum) for an
> example of a package that has been published on GitHub.

> **Warning:** The Github repository must not be empty. You cannot publish
> releases for empty GitHub repositories. 

### Manually Publishing a Package

A package can also be manually published by following these steps:

1. Check that you have a `flix.toml` manifest (if not create one with `init`).
2. Check that the version field in `flix.toml` is correct.
3. Run `check` and `test` to ensure that everything looks alright.
4. Run `build-pkg`. Check that the `artifact` directory is populated.
5. Go to the repository on GitHub:
    1. Click "Releases".
    2. Click "Draft new release".
    3. Enter a tag of the form `v1.2.3` (i.e. use SemVer).
    4. Upload the `package.fpkg` and `flix.toml` from the `artifact` directory.
