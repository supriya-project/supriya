# Hello, world! via different kinds of contexts

Let's play a C-major chord with different kinds of contexts, and compare what
needs to change between them, and what can stay the same.

Note how playing the notes and stopping them are agnostic about what kind of
context is used, while booting/quitting the context (if realtime) and passing
time are different across each kind of context.

```
➜ python ./hello_world_contexts.py --help
usage: hello_world_contexts.py [-h] (--realtime-threaded | --realtime-async | --nonrealtime)

Play a C-major chord via different kinds of contexts

options:
  -h, --help           show this help message and exit
  --realtime-threaded  use a realtime threaded Server
  --realtime-async     use a realtime asyncio-enabled AsyncServer
  --nonrealtime        use a non-realtime Score
```

Play the chord using the standard threaded `Server` in realtime:

```
python ./hello_world_contexts.py --realtime-threaded
```

Play the chord using the asyncio-enabled `AsyncServer` in realtime:

```
python ./hello_world_contexts.py --realtime-async
```

Play the chord via a non-realtime `Score` and open the resulting soundfile:

```
python ./hello_world_contexts.py --nonrealtime
```
