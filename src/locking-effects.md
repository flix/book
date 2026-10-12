# Locking Effects

> **Note:** Effect locking is an experimental feature.

A dependency built in the `plain` or `paranoid` security context can only do what its
type and effect signatures say it does, as described in
[Trusting Dependencies](./trusting-dependencies.md). But signatures are not fixed. A
new version of a package may add an effect to a function we call. To catch such a
change, we would have to read every public signature of every dependency again after
every upgrade.

Effect locking does this for us. The `eff-lock` command records the type and effect
signature of every public function of every package the project has installed in an
`effects.lock` file, and the `eff-check` command tells us which of them have changed
since.

## Locking the Signatures

For a project that depends on:

```toml
[dependencies]
"github:flix/museum-giftshop" = { version = "2.0.2", mount = "giftshop" }
```

the `eff-lock` command type checks the project and reports:

```
Locked 3 signatures of 2 packages.
```

It writes an `effects.lock` file next to `flix.toml`:

```toml
[lock]
version = 1

[packages."github:flix/museum-clerk".defs]
"Clerk.welcomeVisitor" = "sha256:527d67f451945e784feca592a8e17b91f2a5152039171ce326efbdd200a01015"
"Clerk.work" = "sha256:527d67f451945e784feca592a8e17b91f2a5152039171ce326efbdd200a01015"

[packages."github:flix/museum-giftshop".defs]
"Giftshop.buyGift" = "sha256:527d67f451945e784feca592a8e17b91f2a5152039171ce326efbdd200a01015"
```

The lock file has a section for each package, and in it a line for each public
function the package declares, by its name inside the package, with a hash of the
function's type and effect signature. The signatures that a trait declares go in a
`sigs` table of their own.
The three functions here all have the signature `Unit -> Unit \ IO`, which is why
they all have the same hash.

The lock covers every package the project has installed, not only the ones the
manifest declares: `flix/museum-clerk` is locked because `flix/museum-giftshop`
depends on it. The library bundled with Flix is not locked, since the `flix` field of
the manifest already fixes the version of Flix that provides it, and neither is our
own code. If the project does not type check, nothing is locked.

> **Tip:** The `effects.lock` file should be committed to version control, like
> `packages.lock`.

## Checking the Signatures

The `eff-check` command type checks the project and compares the signature of every
locked function with the hash in the lock file. When nothing has changed, it reports:

```
Checked 3 signatures of 2 packages. Nothing has changed.
```

Suppose that the release of `flix/museum-giftshop` we locked declared `buyGift` as a
pure function, and that we upgrade to a release that declares it with the `IO`
effect. The `eff-check` command then reports:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@  WARNING! YOU MAY BE SUBJECT TO A SUPPLY CHAIN ATTACK!  @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            ~~ Signatures have changed! ~~

These declarations are not the ones that were locked. A dependency may now
be able to do things it could not do when you locked it.

  github:flix/museum-giftshop:
    Giftshop.buyGift
      def buyGift(): Unit \ IO

Do not build or run this project until you know why. Find out who published
the version you are building, and what changed in it.

Record the new signatures with flix eff-lock only once you are certain the
change is one the author made, and one you want.
```

A changed signature is not necessarily an attack. The author may have released the
change on purpose, and we may want it. But it should never pass unnoticed. Once we
know why a signature changed, and accept the change, we run `eff-lock` again to record
the new signatures.

> **Tip:** The `eff-check` command exits with status `1` when a signature has
> changed, and with `0` otherwise, so it can fail a CI build.

## Locking One Package at a Time

Both commands can name a package:

```
eff-lock flix/museum-giftshop
```

The command reports:

```
Locked 1 signature of 'github:flix/museum-giftshop'.
```

and replaces the section of `flix/museum-giftshop` in the lock file, leaving every
other section as it was. Likewise, `eff-check flix/museum-giftshop` checks that
package alone. This lets us accept the change in one package, and record it, while the
change in another is still under review.

## The Two Lock Files

A project has two lock files, and they guard against different things.

The `packages.lock` file records the digest of the files of each version the project
has resolved, so that a version, once seen, is always the same bytes. An upgrade
resolves new versions and records them: that is what an upgrade is for. The
`effects.lock` file records what the dependencies may do, and only `eff-lock` writes
it, so it survives an upgrade. The first catches a version whose files are no longer
the ones we downloaded. The second catches a version that does more than the one we
took on.

## Locks and Security Contexts

Effect locking rests on the guarantee of the security context. A signature says what
a function can do only when its package is built in the `plain` or `paranoid`
context. A package built in the `unrestricted` context is locked like any other, but
its signatures tell us nothing about what it may do, so an unchanged lock on it is no
assurance.

The lock is most informative when a library declares its own effects, as recommended
in [Writing a Library that Needs Effects](./trusting-dependencies.md#writing-a-library-that-needs-effects).
A function whose signature names the effects it uses, rather than `IO`, has a
signature that changes when what it does changes.
