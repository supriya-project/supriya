# Hello, world! with debugging output

Let's play a C-major chord! But this time, let's also print out logs and
debugging information about the state of the server, the scsynth process, and
the OSC messages sent by our client.

We'll perform four kinds of debugging:

- Turn on logging for the `scsynth` subprocess so we can see what it says when
  it boots up.
- Print the "status" of the server at various points so we can see CPU usage,
  actual sample rates, node counts, etc.
- Print the "node tree": the structure of the groups and synths in the server.
- Capture and print OSC messages sent by Supriya to `scsynth`.

Invoke with:

```
supriya$ python -m examples.hello_world_debugged
```

See the examples documentation for a complete explanation.
