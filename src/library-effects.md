# Library Effects

Flix provides several built-in library effects for common I/O operations. These
effects all have default handlers, so no explicit `runWithIO` is needed in
`main`.

| Effect                                              | Description                                                                                    |
|------------------------------------------------------|------------------------------------------------------------------------------------------------|
| [`Assert`](./assert.md)                              | Runtime assertions (`assertTrue`, `assertEq`, etc.) with configurable handlers.                |
| [`Logger`](./logger.md)                              | Structured logging at five severity levels with filtering and collection.                      |
| [`Math.Random`](./random.md)                         | Generating pseudorandom numbers, with optional seeded determinism.                             |
| [`Fs.FileSystem`](./filesystem.md) <br> [`Fs.FileRead`](./filesystem.md) <br> [`Fs.FileWrite`](./filesystem.md) <br> [`Fs.FileStat`](./filesystem.md) | File I/O, metadata, directories, and middleware (chroot, atomic writes, in-memory FS, etc.).   |
| [`Net.Http`](./http-and-https.md) <br> [`Net.Https`](./http-and-https.md) | Sending HTTP requests with a fluent API, middleware (retries, rate limiting, circuit breakers). |
| [`Sys.Console`](./console.md)                        | Terminal I/O: reading input, printing to stdout/stderr, prompts, and menus.                    |
| [`Sys.Env`](./env.md)                                | Accessing environment variables, system properties, and platform information.                  |
| [`Sys.Exit`](./exit.md)                              | Terminating the program with a specific exit code.                                             |
| [`Sys.Process`](./process.md)                        | Spawning and managing OS processes.                                                            |
| [`Time.Clock`](./clock.md)                           | Querying the current wall-clock time in various units.                                         |
| [`Time.Sleep`](./sleep.md)                           | Pausing the current thread with composable middleware (jitter, caps, logging).                  |
