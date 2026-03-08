# Http and Https

Flix provides `Http` and `Https` as library effects for sending HTTP requests.
Both effects have default handlers, so no explicit `runWithIO` call is needed in
`main`. The key modules are:

- `Net.Http` — the `Http` effect and convenience functions (`get`, `post`, `send`, etc.)
- `Net.Https` — the `Https` effect (enforces `https://` URLs)
- `Net.HttpRequest` — a fluent API for building requests
- `Net.HttpResponse` — accessors for inspecting responses
- `Net.Retry` — retry strategies for use with middleware

## Sending a GET Request

The simplest way to make an HTTP request is with `Http.get`. It returns a
`Result[IoError, HttpResponse]`, so we pattern match on `Ok` and `Err`:

```flix
use Net.Http
use Net.HttpResponse

def main(): Unit \ { Http, IO } =
    match Http.get("http://example.com/") {
        case Ok(resp) => println(HttpResponse.body(resp))
        case Err(err) => println(err)
    }
```

The `Http` effect supports both `http://` and `https://` URLs. The effect
appears in the type signature of `main` alongside `IO`.

## Inspecting the Response

The `HttpResponse` module provides accessors for status codes, headers, and body
content. The `expect` function returns `Err` for non-2xx status codes, which is
useful when you want to treat unsuccessful responses as errors:

```flix
use Net.Http
use Net.HttpResponse

def main(): Unit \ { Http, IO } =
    match Http.get("https://flix.dev/") {
        case Ok(resp) =>
            println("Status:         ${HttpResponse.status(resp)}");
            println("Is success?     ${HttpResponse.isSuccess(resp)}");
            println("Is client err?  ${HttpResponse.isClientError(resp)}");
            println("Is server err?  ${HttpResponse.isServerError(resp)}");
            println("Content-Type:   ${HttpResponse.contentType(resp)}");
            println("Content-Length: ${HttpResponse.contentLength(resp)}");
            println("Server header:  ${HttpResponse.headerValue("server", resp)}");
            match HttpResponse.expect(resp) {
                case Ok(r) =>
                    println("Body length: ${String.length(HttpResponse.body(r))}")
                case Err(e) =>
                    println("Unexpected status: ${e}")
            }
        case Err(err) =>
            println("Error: ${err}")
    }
```

## POST Requests and JSON

Use `HttpRequest.post` to create a POST request with a body. The request builder
supports `withContentType` and `withAccept` for setting common headers. Send the
built request with `Http.send`:

```flix
use Net.Http
use Net.HttpRequest
use Net.HttpResponse

def main(): Unit \ { Http, IO } =
    let body = "{\"name\": \"Asterix\", \"age\": 35}";
    let req = HttpRequest.post("https://flix.dev/api/users", body)
                |> HttpRequest.withContentType("application/json")
                |> HttpRequest.withAccept("application/json");
    match Http.send(req) {
        case Ok(resp) =>
            println("Status: ${HttpResponse.status(resp)}");
            println("Body: ${HttpResponse.body(resp)}")
        case Err(err) =>
            println("Error: ${err}")
    }
```

## Building Requests

The `HttpRequest` module provides a fluent API for building requests. You can add
query parameters, authentication tokens, custom headers, and timeouts using a
pipeline of `|>` calls:

```flix
use Net.Http
use Net.HttpRequest
use Net.HttpResponse
use Time.Duration.seconds

def main(): Unit \ { Http, IO } =
    let req =
        HttpRequest.get("https://flix.dev/api/search")
            |> HttpRequest.withQueryParam("q", "flix programming language")
            |> HttpRequest.withQueryParams(Map#{
                "page" => "1", "per_page" => "25", "sort" => "relevance"
            })
            |> HttpRequest.withBearerToken("ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ")
            |> HttpRequest.withHeader("User-Agent", "MyApp/1.0")
            |> HttpRequest.withTimeout(seconds(5));
    match Http.send(req) {
        case Ok(resp) =>
            println("Status: ${HttpResponse.status(resp)}");
            println("Body: ${String.takeLeft(80, HttpResponse.body(resp))}")
        case Err(err) =>
            println("Error: ${err}")
    }
```

Constructors are available for all HTTP methods: `HttpRequest.get`,
`HttpRequest.post`, `HttpRequest.put`, `HttpRequest.patch`, and
`HttpRequest.delete`.

## The Https Effect

The `Https` effect works like `Http` but enforces that all URLs use the
`https://` scheme. If you pass an `http://` URL, the request is rejected. Use
`Https` when you want the type system to guarantee that only secure connections
are made:

```flix
use Net.Https
use Net.HttpResponse

def main(): Unit \ { Https, IO } =
    match Https.get("https://example.com/") {
        case Ok(resp) => println(HttpResponse.body(resp))
        case Err(err) => println(err)
    }
```

Note that `Http` already supports `https://` URLs — `Https` is for when you want
the *effect signature* to make the security guarantee explicit.

## Middleware

Middleware are effect handlers that intercept `Http` (or `Https`) requests. They
are applied using `run { ... } with Http.<middleware>` and compose by stacking
multiple `with` clauses.

### Base URL

`withBaseUrl` prefixes relative paths with a base URL. Absolute URLs (containing
`://`) bypass the base and are sent as-is:

```flix
use Net.Http
use Net.HttpResponse

def main(): Unit \ { Http, IO } =
    run {
        match Http.get("/api/users") {
            case Ok(resp) => println("/api/users -> ${HttpResponse.status(resp)}")
            case Err(err) => println("/api/users -> ${err}")
        };
        match Http.get("/api/posts") {
            case Ok(resp) => println("/api/posts -> ${HttpResponse.status(resp)}")
            case Err(err) => println("/api/posts -> ${err}")
        };
        // Absolute URLs bypass the base.
        match Http.get("https://flix.dev/other") {
            case Ok(resp) => println("absolute   -> ${HttpResponse.status(resp)}")
            case Err(err) => println("absolute   -> ${err}")
        }
    } with Http.withBaseUrl("https://flix.dev")
```

### Default Headers

`withDefaultHeaders` injects headers into every request. Headers already present
on a request are not overridden:

```flix
use Net.Http
use Net.HttpResponse

def main(): Unit \ { Http, IO } =
    let defaults = Map#{
        "Accept"        => List#{"application/json"},
        "Authorization" => List#{"Bearer ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789"}
    };
    run {
        match Http.get("https://flix.dev/api/users") {
            case Ok(resp) => println("Status: ${HttpResponse.status(resp)}")
            case Err(err) => println("Error: ${err}")
        }
    } with Http.withDefaultHeaders(defaults)
```

### Logging

`withLogging` logs each request and response via the `Logger` effect. Note that
`Logger` appears in the type signature of `main`:

```flix
use Net.Http
use Net.HttpResponse

def main(): Unit \ { Http, Logger, IO } =
    run {
        match Http.get("https://flix.dev/") {
            case Ok(resp) => println("Status: ${HttpResponse.status(resp)}")
            case Err(err) => println("Error: ${err}")
        };
        match Http.get("https://notfound.flix.dev/") {
            case Ok(resp) => println("Status: ${HttpResponse.status(resp)}")
            case Err(err) => println("Error: ${err}")
        }
    } with Http.withLogging
```

### Retries

`withRetry` adds automatic retries using strategies from the `Net.Retry` module.
Each strategy is a function that decides whether to retry based on the attempt
number and the outcome (transport error or HTTP error):

```flix
use Net.Http
use Net.Retry
use Net.HttpResponse
use Time.Duration.milliseconds

def main(): Unit \ { Http, IO } =
    // Linear: retry up to 3 times with 100ms delay.
    run {
        println("--- Linear retry ---");
        match Http.get("https://notfound.flix.dev/") {
            case Ok(resp) => println("Status: ${HttpResponse.status(resp)}")
            case Err(err) => println("Error: ${err}")
        }
    } with Http.withRetry(Retry.linear(maxRetries = 3, delay = milliseconds(100)));

    // Exponential: retry up to 3 times with 100ms base delay.
    run {
        println("--- Exponential retry ---");
        match Http.get("https://notfound.flix.dev/") {
            case Ok(resp) => println("Status: ${HttpResponse.status(resp)}")
            case Err(err) => println("Error: ${err}")
        }
    } with Http.withRetry(Retry.exponential(maxRetries = 3, baseDelay = milliseconds(100)));

    // Transport-only: only retry on connection failures, not HTTP errors.
    run {
        println("--- Transport-only retry ---");
        match Http.get("https://notfound.flix.dev/") {
            case Ok(resp) => println("Status: ${HttpResponse.status(resp)}")
            case Err(err) => println("Error: ${err}")
        }
    } with Http.withRetry(Retry.retryTransportOnly(maxRetries = 2, delay = milliseconds(100)))
```

The available strategies are:

- `Retry.linear` — fixed delay between retries
- `Retry.exponential` — doubling delay between retries
- `Retry.retryAfter` — honours the `Retry-After` response header on 429/503 responses
- `Retry.retryTransportOnly` — retries only on connection failures, not HTTP errors

Strategies can be wrapped with `Retry.withJitter` to add random jitter to
delays, and `Retry.withDeadline` to enforce a total time budget across all
retries.

### Circuit Breaker

`withCircuitBreaker` protects against cascading failures. After
`failureThreshold` consecutive failures (transport errors or 5xx responses), the
circuit opens and immediately rejects requests for the `cooldown` duration. A
successful request resets the failure counter. Note that the `Clock` effect
appears in the type signature:

```flix
use Net.Http
use Net.HttpResponse
use Time.Duration.seconds

def main(): Unit \ { Clock, Http, IO } =
    run {
        let urls = List#{"/a", "/b", "/c", "/d", "/e", "/f", "/g", "/h"};
        foreach (url <- urls) {
            match Http.get(url) {
                case Ok(resp) => println("${url} -> ${HttpResponse.status(resp)}")
                case Err(err) => println("${url} -> ${err}")
            }
        }
    } with Http.withCircuitBreaker(failureThreshold = 3, cooldown = seconds(5))
      with Http.withBaseUrl("https://notfound.flix.dev")
```

### Rate Limiting

Flix provides three rate-limiting strategies:

- `withMinInterval` — enforces a fixed minimum delay between consecutive requests
- `withTokenBucket` — allows a burst of requests up front, then a steady rate
- `withSlidingWindow` — allows at most N requests in any rolling time window

All three require the `Clock` effect:

```flix
use Net.Http
use Net.HttpResponse
use Time.Duration.{milliseconds, seconds}

def main(): Unit \ { Clock, Http, IO } =
    // Min interval: at least 100ms between consecutive requests.
    run {
        println("--- Min interval ---");
        let urls = List#{"/a", "/b", "/c", "/d"};
        foreach (url <- urls) {
            match Http.get(url) {
                case Ok(resp) => println("${url} -> ${HttpResponse.status(resp)}")
                case Err(err) => println("${url} -> ${err}")
            }
        }
    } with Http.withMinInterval(interval = milliseconds(100))
      with Http.withBaseUrl("https://flix.dev");

    // Token bucket: burst of 2, then 1 request per 100ms.
    run {
        println("--- Token bucket ---");
        let urls = List#{"/a", "/b", "/c", "/d"};
        foreach (url <- urls) {
            match Http.get(url) {
                case Ok(resp) => println("${url} -> ${HttpResponse.status(resp)}")
                case Err(err) => println("${url} -> ${err}")
            }
        }
    } with Http.withTokenBucket(burstSize = 2, interval = milliseconds(100))
      with Http.withBaseUrl("https://flix.dev");

    // Sliding window: at most 2 requests per 1000ms window.
    run {
        println("--- Sliding window ---");
        let urls = List#{"/a", "/b", "/c", "/d"};
        foreach (url <- urls) {
            match Http.get(url) {
                case Ok(resp) => println("${url} -> ${HttpResponse.status(resp)}")
                case Err(err) => println("${url} -> ${err}")
            }
        }
    } with Http.withSlidingWindow(maxRequests = 2, window = seconds(1))
      with Http.withBaseUrl("https://flix.dev")
```

## Composing Middleware

Middleware compose by stacking `with` clauses. Each `with` wraps the preceding
block, so the outermost handler runs first. Here is an example that stacks base
URL, default headers, retry, circuit breaker, rate limiting, and logging:

```flix
use Net.Http
use Net.Retry
use Net.HttpResponse
use Time.Duration.{milliseconds, seconds}

def main(): Unit \ { Clock, Http, Logger, IO } =
    let defaultHeaders = Map#{
        "Accept"        => List#{"application/json"},
        "Authorization" => List#{"Bearer tok123"}
    };
    run {
        let urls = List#{"/api/users", "/api/posts"};
        foreach (url <- urls) {
            match Http.get(url) {
                case Ok(resp) => println("${url} -> ${HttpResponse.status(resp)}")
                case Err(err) => println("${url} -> ${err}")
            }
        };
        match Http.get("https://notfound.flix.dev/") {
            case Ok(resp) => println("notfound -> ${HttpResponse.status(resp)}")
            case Err(err) => println("notfound -> ${err}")
        }
    } with Http.withBaseUrl("https://flix.dev")
      with Http.withDefaultHeaders(defaultHeaders)
      with Http.withRetry(Retry.linear(maxRetries = 2, delay = milliseconds(100)))
      with Http.withCircuitBreaker(failureThreshold = 3, cooldown = seconds(5))
      with Http.withSlidingWindow(maxRequests = 2, window = seconds(1))
      with Http.withLogging
```

The `Http`, `Logger`, and `Clock` effects all have default handlers, so they are
handled automatically when they appear in the type signature of `main`.

The order of `with` clauses matters. The outermost handler (listed last) wraps
all inner handlers. In the example above, `withLogging` is outermost, so it
sees *every* HTTP request — including retries and circuit-breaker probes. If we
moved `withLogging` before `withRetry`, it would only see the original requests,
not the retries. When composing middleware, think about which layer should
observe which requests.
