# Hello, world!

Let's play a C-major chord:

```
➜ python3 ./hello_world.py --help
usage: hello world! [-h] (--realtime-threaded | --realtime-async | --nonrealtime)

options:
  -h, --help           show this help message and exit
  --realtime-threaded
  --realtime-async
  --nonrealtime
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
