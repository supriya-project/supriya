# Hello, world! with debugging output

Let's play a C-major chord! But this time, let's also print out logs and
debugging information about the state of the server, the scsynth process, and
the OSC messages sent by our client.

We'll perform four kinds of debugging:

- Turn on logging for the `scsynth` subprocess so we can see what it says when it boots up.
- Print the "status" of the server at various points so we can see CPU usage, actual sample rates, node counts, etc.
- Print the "node tree": the structure of the groups and synths in the server.
- Capture and print OSC messages sent by Supriya to `scsynth`.

```
$ python ./hello_world_debugged.py
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] booting ...
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] command: /Applications/SuperCollider.app/Contents/Resources/scsynth -R 0 -l 1 -u 57110
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received: Number of Devices: 6
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received:    0 : "BlackHole 16ch"
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received:    1 : "MacBook Pro Microphone"
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received:    2 : "MacBook Pro Speakers"
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received:    3 : "Joséphine's iPhone Microphon"
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received:    4 : "ZoomAudioD"
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received:    5 : "BlackHoleMoon"
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received: "MacBook Pro Microphone" Input Device
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received:    Streams: 1
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received:       0  channels 1
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received: "MacBook Pro Speakers" Output Device
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received:    Streams: 1
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received:       0  channels 2
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received: SC_AudioDriver: sample rate = 44100.000000, driver's block size = 512
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] received: SuperCollider 3 server ready.
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] ... booted!

BEFORE PLAYING:

Server status: StatusInfo(actual_sample_rate=44100.00000477962, average_cpu_usage=0.08445477485656738, group_count=2, peak_cpu_usage=0.6118271946907043, synth_count=0, synthdef_count=32, target_sample_rate=44100.0, ugen_count=0)
NODE TREE 0 group
    1 group

PLAYING:

Server status: StatusInfo(actual_sample_rate=44100.00000477962, average_cpu_usage=0.08445477485656738, group_count=2, peak_cpu_usage=0.6118271946907043, synth_count=0, synthdef_count=32, target_sample_rate=44100.0, ugen_count=0)
NODE TREE 0 group
    1 group
        1002 default
            amplitude: 0.1, frequency: 392.0, gate: 1.0, pan: 0.5, out: 0.0
        1001 default
            amplitude: 0.1, frequency: 329.630005, gate: 1.0, pan: 0.5, out: 0.0
        1000 default
            amplitude: 0.1, frequency: 261.630005, gate: 1.0, pan: 0.5, out: 0.0
Sent: OscMessage('/d_recv', b'SCgf\x00\x00\x00\x02\x00\x01\x07default\x00\x00\x00\x0c\x00\x00\x00\x00>\x99\x99\x9a<#\xd7\n?333@\x00\x00\x00\xbe\xcc\xcc\xcd>\xcc\xcc\xcdEz\x00\x00E\x9c@\x00E\x1c@\x00EH\x00\x00?\x80\x00\x00\x00\x00\x00\x05=\xcc\xcc\xcdC\xdc\x00\x00?\x80\x00\x00?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\tamplitude\x00\x00\x00\x00\tfrequency\x00\x00\x00\x01\x04gate\x00\x00\x00\x02\x03pan\x00\x00\x00\x03\x03out\x00\x00\x00\x04\x00\x00\x00\x14\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x01\x01\x01\x01\x06VarSaw\x02\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x05Linen\x01\x00\x00\x00\x05\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xff\xff\xff\xff\x00\x00\x00\x02\xff\xff\xff\xff\x00\x00\x00\x03\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x04\x01\x07Control\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x04\x00\x04Rand\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x05\xff\xff\xff\xff\x00\x00\x00\x00\x00\x0cBinaryOpUGen\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\x00\x01\x06VarSaw\x02\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x04Rand\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x06\x00\x0cBinaryOpUGen\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00\x01\x06VarSaw\x02\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x04Sum3\x02\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00\x00\n\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x04Rand\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x07\xff\xff\xff\xff\x00\x00\x00\x08\x00\x04Rand\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\t\xff\xff\xff\xff\x00\x00\x00\n\x00\x05XLine\x01\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x0b\xff\xff\xff\xff\x00\x00\x00\x00\x01\x03LPF\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x0b\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x04Pan2\x02\x00\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\xff\xff\xff\x00\x00\x00\x0b\x02\x02\tOffsetOut\x02\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00\x01\x00\x00', OscBundle(contents=[OscMessage('/s_new', 'default', 1000, 0, 1, 'frequency', 261.63), OscMessage('/s_new', 'default', 1001, 0, 1, 'frequency', 329.63), OscMessage('/s_new', 'default', 1002, 0, 1, 'frequency', 392.0)]))

BEFORE FREEING:

Server status: StatusInfo(actual_sample_rate=44100.05894027885, average_cpu_usage=0.561026930809021, group_count=2, peak_cpu_usage=0.6470469236373901, synth_count=3, synthdef_count=33, target_sample_rate=44100.0, ugen_count=60)
NODE TREE 0 group
    1 group
        1002 default
            amplitude: 0.1, frequency: 392.0, gate: 1.0, pan: 0.5, out: 0.0
        1001 default
            amplitude: 0.1, frequency: 329.630005, gate: 1.0, pan: 0.5, out: 0.0
        1000 default
            amplitude: 0.1, frequency: 261.630005, gate: 1.0, pan: 0.5, out: 0.0

FREEING:

Server status: StatusInfo(actual_sample_rate=44100.05894027885, average_cpu_usage=0.561026930809021, group_count=2, peak_cpu_usage=0.6470469236373901, synth_count=3, synthdef_count=33, target_sample_rate=44100.0, ugen_count=60)
NODE TREE 0 group
    1 group
        1002 default
            amplitude: 0.1, frequency: 392.0, gate: 0.0, pan: 0.5, out: 0.0
        1001 default
            amplitude: 0.1, frequency: 329.630005, gate: 0.0, pan: 0.5, out: 0.0
        1000 default
            amplitude: 0.1, frequency: 261.630005, gate: 0.0, pan: 0.5, out: 0.0
Sent: OscMessage('/n_set', 1000, 'gate', 0.0)
Sent: OscMessage('/n_set', 1001, 'gate', 0.0)
Sent: OscMessage('/n_set', 1002, 'gate', 0.0)

AFTER FREEING:

Server status: StatusInfo(actual_sample_rate=44100.11842268476, average_cpu_usage=0.6431891322135925, group_count=2, peak_cpu_usage=0.8913453817367554, synth_count=3, synthdef_count=33, target_sample_rate=44100.0, ugen_count=60)
NODE TREE 0 group
    1 group

INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] quitting ...
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] ... quit!
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] quitting ...
INFO:supriya.scsynth:[127.0.0.1:57110/0x102efc1a0] ... already quit!
```
