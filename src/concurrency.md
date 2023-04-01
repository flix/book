# Structured Concurrency

Flix supports CSP-style concurrency with channels and
processes inspired by Go and Rust.

## Spawning Processes

We can spawn a process with the `spawn` keyword:

```flix
def main(): Unit \ IO = region rc {
    spawn println("Hello from thread") @ rc;
    println("Hello from main")
}
```

Spawned processes are always associated with a region; the region 
will not exit until all the processes associated with it have completed:

```flix
def slowPrint(delay: Int32, message: String): Unit \ IO =
    Thread.sleep(Time/Duration.fromSeconds(delay));
    println(message)

def main(): Unit \ IO = 
    region r1 {
        region r2 {
            spawn slowPrint(2, "Hello from r1") @ r1;
            spawn slowPrint(1, "Hello from r2") @ r2
        };
        println("r2 is now complete")
    };
    println("r1 is now complete")
```

This means that Flix supports _structured concurrency_; spawned 
processes have clearly defined entry and exit points.

## Communicating with Channels

To communicate between processes we use channels.
A _channel_ allows two or more processes to exchange
data by sending immutable messages to each other.

A channel comes in one of two variants: _buffered_ or
_unbuffered_. Channels are always associated with a region.

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
def main(): Int32 \ IO = region rc {
    let (tx, rx) = Channel.unbuffered(rc);
    spawn Channel.send(42, tx) @ rc;
    Channel.recv(rx)
}
```

Here the `main` function creates an unbuffered
channel which returns `Sender` `tx` and a `Receiver` `rx` channels,
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
def meow(tx: Sender[String, r]): Unit \ { Write(r) } = 
    Channel.send("Meow!", tx)

def woof(tx: Sender[String, r]): Unit \ { Read(r), Write(r) } = 
    Channel.send("Woof!", tx)

def main(): Unit \ IO = region rc {
    let (tx1, rx1) = Channel.buffered(rc, 1);
    let (tx2, rx2) = Channel.buffered(rc, 1);
    spawn meow(tx1) @ rc;
    spawn woof(tx2) @ rc;
    select {
        case m <- recv(rx1) => m
        case m <- recv(rx2) => m
    } |> println
}
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
def main(): String = region rc {
    let (_, rx1) = Channel.buffered(rc, 1);
    let (_, rx2) = Channel.buffered(rc, 1);
    select {
        case _ <- recv(rx1) => "one"
        case _ <- recv(rx2) => "two"
        case _             => "default"
    }
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
def slow(tx: Sender[String, r]): Unit \ { Write(r), IO} =
    Thread.sleep(Time/Duration.fromSeconds(60));
    Channel.send("I am very slow", tx)

def main(): Unit \ IO = region rc {
    let (tx, rx) = Channel.buffered(rc, 1);
    spawn slow(tx) @ rc;
    let timeout = Channel.timeout(rc, Time/Duration.fromSeconds(5));
    select {
        case m <- recv(rx)       => m
        case _ <- recv(timeout)  => "timeout"
    } |> println
}
```

This program prints the string `"timeout"` after five
seconds.
