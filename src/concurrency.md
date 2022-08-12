# Concurrency with Channels and Processes

Flix supports CSP-style concurrency with channels and
processes inspired by Go.

## Spawning Processes

We can spawn a process with the `spawn` keyword:

```flix
spawn (1 + 2)
```

This spawns a process that computes `1 + 2` and
throws the result away.
The `spawn` expression always returns `Unit`.
We can spawn any expression, but we typically spawn
functions to run in a new process:

```flix
def sum(x: Int32, y: Int32): Int32 = x + y

def main(): Unit \ IO = spawn sum(1, 2)
```

## Communicating with Channels

To communicate between processes we use channels.
A _channel_ allows two or more processes to exchange
data by sending immutable messages to each other.

A channel comes in one of two variants: _buffered_ or
_unbuffered_.

A buffered channel has a size, set at creation time,
and can hold that many messages.
If a process attempts to put a message into a
buffered channel that is full, then the process is
blocked until space becomes available.
If, on the other hand, a process attempts to get a
message from an empty channel, the process is blocked
until a message is put into the channel.

An unbuffered channel works like a buffered channel
of size zero; for a get and a put to happen both
processes must rendezvous (block) until the message
is passed from sender to receiver.

Here is an example of sending and receiving a message
over a channel:

```flix
def send(c: Channel[Int32]): Unit \ IO = c <- 42; ()

def main(): Unit \ IO =
    let c = chan Int32 0;
    spawn send(c);
    <- c;
    ()
```

Here the `main` function creates an unbuffered
channel `c`, spawns the `send` function, and waits
for a message from `c`.
The `send` function simply puts the value `42` into
the channel.

## Selecting on Channels

We can use the `select` expression to receive a
message from a collection of channels.
For example:

```flix
def meow(c: Channel[String]): Unit \ IO = c <- "Meow!"; ()

def woof(c: Channel[String]): Unit \ IO = c <- "Woof!"; ()

def main(): Unit \ IO =
    let c1 = chan String 1;
    let c2 = chan String 1;
    spawn meow(c1);
    spawn woof(c2);
    select {
        case m <- c1 => m
        case m <- c2 => m
    } |> println

```

Many important concurrency patterns such as
producer-consumer and load balancers can be expressed
using the `select` expression.

### Selecting with Default

In some cases, we do not want to block until a
message arrives, potentially waiting forever.
Instead, we want to take some alternative action if
no message is readily available.
We can achieve this with a _default case_ as shown
below:

```flix
def main(): Unit \ IO =
    let c1 = chan String 1;
    let c2 = chan String 1;
    select {
        case m <- c1 => "one"
        case m <- c2 => "two"
        case _       => "default"
    }
```

Here a message is never sent to `c1` nor `c2`.
The `select` expression tries all cases, and if no
channel is ready, it immediately selects the default
case.
Hence using a default case prevents the `select`
expression from blocking forever.

### Selecting with Tickers and Timers

As an alternative to a default case, we can use
_tickers_ and _timers_ to wait for pre-defined
periods of time inside a `select` expression.

For example, here is a program that has a slow
function that takes a minute to send a message on
a channel, but the `select` expression relies on
`Timer.seconds` to only wait `5` seconds before
giving up:

```flix
def slow(c: Channel[String]): Unit \ IO =
    import static java.lang.Thread.sleep(Int64): Unit \ IO;
    sleep(Time/Duration.oneMinute() / 1000000i64);
    c <- "I am very slow";
    ()

def main(): Unit \ IO =
    use Concurrent/Channel/Timer.seconds;
    let c = chan String 1;
    spawn slow(c);
    select {
        case m <- c              => m
        case _ <- seconds(5i64)  => "timeout"
    } |> println
```

This program prints the string `"timeout"` after five
seconds.

Flix also supports _tickers_ which are similar to
timers, but instead of sending a message one after a
pre-defined time they repeatedly send a message every
tick.

#### Planned Feature

Flix does not currently support _put_ operations in
`select` expressions.
This is something that we might support in the future.
