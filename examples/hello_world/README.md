# Hello, world!

Let's play a C-major chord:

```
➜ python examples/hello_world/hello_world.py --help
usage: hello world! [-h] (--realtime-threaded | --realtime-async | --nonrealtime)

Play a C-major chord

options:
  -h, --help           show this help message and exit
  --realtime-threaded  use a realtime threaded Server
  --realtime-async     use a realtime asyncio-enabled AsyncServer
  --nonrealtime        use a non-realtime Score
```

Play the chord using the standard threaded `Server` in realtime:

```
python ./hello_world.py --realtime-threaded
```

Play the chord using the asyncio-enabled `AsyncServer` in realtime:

```
python ./hello_world.py --realtime-async
```

Play the chord via a non-realtime `Score` and open the resulting soundfile:

```
python ./hello_world.py --nonrealtime
```
