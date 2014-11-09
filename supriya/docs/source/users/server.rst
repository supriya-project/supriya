Interacting with the Server
===========================

(Documentation coming soon)

Instantiate the server
----------------------

::

    >>> server = Server()
    >>> server
    <Server: offline>

::

    >>> Server() is server
    True

::

    >>> Server.get_default_server()
    <Server: offline>

::

    >>> server.is_running
    False

Boot the server
---------------

::

    >>> server.boot()
    <Server: udp://127.0.0.1:57751, 8i8o>

::

    >>> server.is_running
    True

Query the server
----------------

::

    >>> print(server)
    NODE TREE 0 group
        1 group

::

    >>> print(server.query_remote_nodes())
    NODE TREE 0 group
        1 group

::

    >>> Synth(synthdefs.default).allocate()
    <Synth: 1000>

::

    >>> print(server.query_remote_nodes(include_controls=True))
    NODE TREE 0 group
        1 group
            1000 default
                out: 0.0, amplitude: 0.10000000149, frequency: 440.0, gate: 1.0, pan: 0.5

::

    >>> server.server_status  # doctest: +SKIP
    StatusResponse(
        actual_sample_rate=44099.737053336095
        average_cpu_usage=0.06510373950004578,
        group_count=2,
        peak_cpu_usage=0.13062040507793427,
        synth_count=0,
        synthdef_count=5,
        target_sample_rate=44100.0,
        ugen_count=0,
        )

Quit the server
---------------

::

    >>> server.quit()
    <Server: offline>

::

    >>> server.is_running
    False

Configure the server
--------------------

::

    >>> server.server_options
    ServerOptions(
        audio_bus_channel_count=128,
        block_size=64,
        buffer_count=1024,
        control_bus_channel_count=4096,
        initial_node_id=1000,
        input_bus_channel_count=8,
        input_stream_mask=False,
        load_synthdefs=True,
        maximum_node_count=1024,
        maximum_synthdef_count=1024,
        memory_locking=False,
        memory_size=8192,
        output_bus_channel_count=8,
        output_stream_mask=False,
        protocol='udp',
        random_number_generator_count=64,
        remote_control_volume=False,
        verbosity=0,
        wire_buffer_count=64,
        zero_configuration=False
        )

Server options can only be changed when booting the server.

::

    >>> server_options = servertools.ServerOptions(
    ...     audio_bus_channel_count=256,
    ...     )
    >>> server.boot(server_options=server_options)
    <Server: udp://127.0.0.1:57751, 8i8o>

Debug the server
----------------

::

    >>> server.debug_osc = True

::

    >>> Group().allocate()
    SEND OscBundle(
        contents=(
            OscMessage(21, 1000, 0, 1),
            OscMessage(52, 2),
            )
        )
    RECV OscMessage('/n_go', 1000, 1, -1, -1, 1, -1, -1)
    RECV OscMessage('/synced', 2)
    <Group: 1000>

::

    >>> server.debug_udp = True

::

    >>> Synth(synthdefs.test).allocate()
    SEND OscMessage(5, bytearray(b'SCgf\x00\x00\x00\x02\x00\x01\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02?\x80\x00\x00C\xdc\x00\x00\x00\x00\x00\x02\tamplitude\x00\x00\x00\x00\tfrequency\x00\x00\x00\x01\x00\x00\x00\x05\x0cAudioControl\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x02\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01\x06SinOsc\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00'))
        size 240
           0   00 00 00 05  2c 62 00 00  00 00 00 e1  53 43 67 66   |....,b......SCgf|
          16   00 00 00 02  00 01 04 74  65 73 74 00  00 00 01 00   |.......test.....|
          32   00 00 00 00  00 00 02 3f  80 00 00 43  dc 00 00 00   |.......?...C....|
          48   00 00 02 09  61 6d 70 6c  69 74 75 64  65 00 00 00   |....amplitude...|
          64   00 09 66 72  65 71 75 65  6e 63 79 00  00 00 01 00   |..frequency.....|
          80   00 00 05 0c  41 75 64 69  6f 43 6f 6e  74 72 6f 6c   |....AudioControl|
          96   02 00 00 00  00 00 00 00  01 00 00 02  07 43 6f 6e   |.............Con|
         112   74 72 6f 6c  01 00 00 00  00 00 00 00  01 00 01 01   |trol............|
         128   06 53 69 6e  4f 73 63 02  00 00 00 02  00 00 00 01   |.SinOsc.........|
         144   00 00 00 00  00 01 00 00  00 00 ff ff  ff ff 00 00   |................|
         160   00 00 02 0c  42 69 6e 61  72 79 4f 70  55 47 65 6e   |....BinaryOpUGen|
         176   02 00 00 00  02 00 00 00  01 00 02 00  00 00 02 00   |................|
         192   00 00 00 00  00 00 00 00  00 00 00 02  03 4f 75 74   |.............Out|
         208   02 00 00 00  02 00 00 00  00 00 00 ff  ff ff ff 00   |................|
         224   00 00 00 00  00 00 03 00  00 00 00 00  00 00 00 00   |................|
    RECV OscMessage('/done', '/d_recv')
        size 20
           0   2f 64 6f 6e  65 00 00 00  2c 73 00 00  2f 64 5f 72   |/done...,s../d_r|
          16   65 63 76 00                                          |ecv.|
    SEND OscMessage(9, 'test', 1001, 0, 1)
        size 32
           0   00 00 00 09  2c 73 69 69  69 00 00 00  74 65 73 74   |....,siii...test|
          16   00 00 00 00  00 00 03 e9  00 00 00 00  00 00 00 01   |................|
    RECV OscMessage('/n_go', 1001, 1, -1, 1000, 0)
        size 36
           0   2f 6e 5f 67  6f 00 00 00  2c 69 69 69  69 69 00 00   |/n_go...,iiiii..|
          16   00 00 03 e9  00 00 00 01  ff ff ff ff  00 00 03 e8   |................|
          32   00 00 00 00                                          |....|
    <Synth: 1001>

::

    >>> server.debug_osc = False

Working with multiple servers
-----------------------------

::

    >>> other_server = Server(port=57752)
    >>> other_server.boot()
    <Server: udp://127.0.0.1:57752, 8i8o>

::

    >>> another_server = Server(port=57753)
    >>> another_server.boot()
    <Server: udp://127.0.0.1:57753, 8i8o>