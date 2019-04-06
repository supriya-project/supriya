Servers
=======

Server lifecycle
----------------

.. important:: 

   **TODO**: Handle clientID return via ``/done /notify 0 64`` for allocators

.. important:: 

   **TODO**: Implement ``connect()`` and ``disconnect()``

.. important::

   **TODO**: Use logging, not print, for debugging

.. important::

   **TODO**: Harden passing ``scsynth_path`` into ``boot()``

- boot
- quit
- reboot    
- connect
- disconnect
- kill

::

    >>> server = supriya.Server()
    >>> server.boot()
    >>> server.ip_address, server.port, server.is_running
    >>> supriya.Server.get_default_server() is server
    >>> server.reboot()
    >>> server.quit()
    >>> supriya.Server.kill()

Locating server executables
---------------------------

- scsynth default on OSX
- scsynth (in your path)
- scsynth via config
- scsynth via SCSYNTH_PATH

Server options
--------------

- i/o channel counts
- sample rate
- block size
- memory size
- object counts: buses, buffers, nodes, synthdefs

::

    >>> server.server_options
    >>> server.server_options.as_options_string()
    >>> server.reboot(memory_size=1024 * 32)
    >>> options = supriya.ServerOptions(
    ...     block_size=32,
    ...     input_bus_channel_count=2,
    ...     output_bus_channel_count=2,
    ... )
    >>> server.reboot(options)

::

    >>> server.reboot()
    >>> server.server_options.input_bus_channel_count

Inspecting
----------

- query_remote_nodes
- query_local_nodes
- str()
- status

::

    >>> server.boot()
    >>> supriya.Synth().allocate(server=server)
    >>> server.query_remote_nodes(include_controls=True)
    >>> print(server.query_remote_nodes(include_controls=True))
    >>> print(server.query_local_nodes(include_controls=True))
    >>> print(server)
    >>> server.status

Metering
--------

- meters

::

    >>> server.meters
    >>> supriya.graph(server)
    >>> server.meters.allocate()
    >>> supriya.graph(server)
    >>> import json, time; time.sleep(1)
    >>> print(json.dumps(server.meters.to_dict(), indent=4))
    >>> server.meters.free()
    >>> supriya.graph(server)

Recording
---------

- recorder

::

    >>> server.recorder

Debugging
---------

- debug_osc
- debug_request_names
- debug_udp
- debug_subprocess

::

    >>> server.debug_osc = True
    >>> server.reboot()

::

    >>> server.debug_request_names = True
    >>> server.reboot()

::

    >>> server.debug_udp = True
    >>> server.quit()

::

    >>> server.debug_osc = False
    >>> server.debug_subprocess = True
    >>> server.boot()
