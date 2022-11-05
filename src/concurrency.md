# Concurrency with Channels and Processes

Flix supports CSP-style concurrency with channels and
processes inspired by Go and Rust.

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
def main(): Int32 \ IO =
    let (s, r) = Channel.unbuffered();
    spawn Channel.send(42, s);
    Channel.recv(r)
```

Here the `main` function creates an unbuffered
channel which returns `Sender` `s` and a `Receiver` `r` channels,
spawns the `send` function, and waits
for a message from the channel.

As the example shows, a channel consists of two end points:
the _Sender_ and the _Receiver_. As one would expect, 
messages can only be send using the `Sender`, and only 
received using the `Receiver`.

## Selecting on Channels

We can use the `select` expression to receive a
message from a collection of channels.
For example:

```flix
def meow(s: Sender[String]): Unit \ IO = Channel.send("Meow!", s)

def woof(s: Sender[String]): Unit \ IO = Channel.send("Woof!", s)

def main(): Unit \ IO =
    let (s1, r1) = Channel.buffered(1);
    let (s2, r2) = Channel.buffered(1);
    spawn meow(s1);
    spawn woof(s2);
    select {
        case m <- recv(r1) => m
        case m <- recv(r2) => m
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
def main(): String \ IO =
    let (_, r1) = Channel.buffered(1);
    let (_, r2) = Channel.buffered(1);
    select {
        case _ <- recv(r1) => "one"
        case _ <- recv(r2) => "two"
        case _             => "default"
    }
```

Here a message is never sent to `r1` nor `r2`.
The `select` expression tries all cases, and if no
channel is ready, it immediately selects the default
case.
Hence using a default case prevents the `select`
expression from blocking forever.

### Selecting with Timeouts

As an alternative to a default case, we can use
_tickers_ and _timers_ to wait for pre-defined
periods of time inside a `select` expression.

For example, here is a program that has a slow
function that takes a minute to send a message on
a channel, but the `select` expression relies on
`Channel.timeout` to only wait `5` seconds before
giving up:

```flix
def slow(s: Sender[String]): Unit \ IO =
    Thread.sleep(Time/Duration.fromSeconds(60));
    Channel.send("I am very slow", s)

def main(): Unit \ IO =
    let (s, r) = Channel.buffered(1);
    spawn slow(s);
    let timeout = Channel.timeout(Time/Duration.fromSeconds(5));
    select {
        case m <- recv(r)        => m
        case _ <- recv(timeout)  => "timeout"
    } |> println
```

This program prints the string `"timeout"` after five
seconds.
