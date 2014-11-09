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

    >>> # server.debug_osc = True

::

    >>> Group().allocate(server=server)
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

    >>> # server.debug_udp = True

::

    >>> Synth(synthdefs.default).allocate()
    <Synth: 1001>

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