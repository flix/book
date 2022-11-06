# Installing Flix

Prerequisites: [Java](#java)

## Brew (macOS and Linux)

The recommended way to install Flix on both macOS and Linux is via the [flix/tools]() tap for [Homebrew](https://brew.sh) ([other ways to install](#other-ways-to-install-flix)):

```
brew install flix/tools/flix
```

> 🤔 Note: I'm suggesting that we follow [Clojure's lead](https://github.com/clojure/homebrew-tools) and create our own Homebrew Tap so that we can have complete control.

## Windows

> 🤔 Note: Decide on what the right approach for Windows is. Probably [winget](https://learn.microsoft.com/en-us/windows/package-manager/), but we could also create an installer package or use [Scoop](https://scoop.sh)?

## Testing your setup

You can check to see what version of Flix you have installed with the command `flix --version` which should output:

```
% flix --version
The Flix Programming Language v0.32.0
```

## Other ways to install Flix

> ⚠️ TODO: Instructions for how to download and install manually.

## Java

> ⚠️ TODO: Details of which versions of Java Flix supports
