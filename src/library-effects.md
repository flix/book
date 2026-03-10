# Library Effects

Flix provides several built-in library effects for common I/O operations. These
effects all have default handlers, so no explicit `runWithIO` is needed in
`main`.

| Effect                          | Module                    | Description                                                                                      |
|---------------------------------|---------------------------|--------------------------------------------------------------------------------------------------|
| [Assert](./assert.md)           | `Assert`                  | Runtime assertions (`assertTrue`, `assertEq`, etc.) with configurable handlers.                  |
| [Console](./console.md)         | `Sys.Console`             | Terminal I/O: reading input, printing to stdout/stderr, prompts, and menus.                      |
| [Http / Https](./http-https.md) | `Net.Http`, `Net.Https`   | Sending HTTP requests with a fluent API, middleware (retries, rate limiting, circuit breakers).   |
| [Process](./process.md)         | `Sys.Process`             | Spawning and managing OS processes.                                                              |
