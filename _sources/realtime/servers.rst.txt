Servers
=======

Supriya's :py:class:`~supriya.realtime.servers.Server` provides a handle to a
``scsynth`` process, allowing you to control the process's lifecycle, interact
with the entities it governs, and query its state.

Lifecycle
---------

Instantiate a server with::

    >>> server = supriya.Server()

Instantiated servers are initially *offline*::

    >>> server

To bring an offline server *online*, boot the server::

    >>> server.boot()

Quit a running server::

    >>> server.quit()

Booting without any additional options will use default settings for the
:term:`scsynth` server process, e.g. listening on the IP address ``127.0.0.1``
and port ``57110``, and will automatically attempt to detect the location of the
:term:`scsynth` binary via :py:func:`supriya.scsynth.find`.

You can override the IP address or port via keyword arguments::

    >>> server.boot(ip_address="0.0.0.0", port=56666)

.. book::
    :hide:

    >>> server.quit()

.. caution::

    Attempting to boot a server on a port where another server is already running
    will result in an error::

        >>> server_one = supriya.Server()
        >>> server_two = supriya.Server()

    .. book::
        :allow-exceptions:

        >>> server_one.boot()
        >>> server_two.boot()

    Use :py:func:`~supriya.osc.utils.find_free_port` to grab a random unused port to
    successfully boot::

        >>> server_two.boot(port=supriya.osc.find_free_port())

.. book::
    :hide:

    >>> server_one.quit()
    >>> server_two.quit()

You can also explicitly select the server binary via the ``scsynth_path`` keyword::

    >>> server.boot(scsynth_path="scsynth")

.. book::
    :hide:

    >>> server.quit()

The ``scsynth_path`` keyword allows you to boot with ``supernova`` if you have it available::

    >>> server.boot(scsynth_path="supernova")

.. book::
    :hide:

    >>> server.quit()

Boot options
````````````

:term:`scsynth` can be booted with a wide variety of command-line arguments,
which Supriya models via an :py:class:`~supriya.scsynth.Options` class::

    >>> supriya.Options()

Pass any of the named options found in :py:class:`~supriya.scsynth.Options` as
keyword arguments when booting::

    >>> server.boot(input_bus_channel_count=2, output_bus_channel_count=2)

.. book::
    :hide:

    >>> server.quit()

Multiple clients
````````````````

:term:`SuperCollider` support multiple users interacting with a single server
simultaneously. One user boots the server and governs the underlying server
process, and the remaining users simply connect to it.

Make sure that the server is booting with ``maximum_logins`` set to the max
number of users you expect to log into the server at once, because the default
login count is 1::

    >>> server_one = supriya.Server().boot(maximum_logins=2)

Connect to the existing server::

    >>> server_two = supriya.Server().connect(
    ...     ip_address=server_one.ip_address,
    ...     port=server_one.port,
    ... )

Each connected user has their own client ID and default group::

    >>> server_one.client_id
    >>> server_two.client_id
    >>> print(server_one.query())

Note that ``server_one`` is owned, while ``server_two`` isn't::

    >>> server_one.is_owner
    >>> server_two.is_owner

Supriya provides some very limited guard-rails to prevent server shutdown by
non-owners, e.g. a ``force`` boolean flag which non-owners can set to ``True``
if they really want to quit the server. Without ``force``, quitting a non-owned
server will error:

.. book::
    :allow-exceptions:

    >>> server_two.quit()

Finally, disconnect::

   >>> server_two.disconnect()

Disconnecting won't terminate the server. It continues to run from wherever
``server_one`` was originally booted.

.. book::
    :hide:

    >>> server_one.quit()

Inspection
----------

:py:class:`~supriya.realtime.servers.Server` provides a number of methods and
properties for inspecting its state.

::

    >>> server = supriya.Server().boot()

Inspect the "status" of audio processing::

    >>> server.status

.. hint::

    Server status is a great way of tracking :term:`scsynth`'s CPU usage.

Let's add a synth - explained :doc:`soon <nodes>` - to increase the
complexity of the status output::

    >>> synth = server.add_synth()

.. book::
    :hide:

    >>> server.sync()
    >>> supriya.commands.StatusRequest().communicate(server=server)

::

    >>> server.status

Note that ``synth_count``, ``synthdef_count`` and ``ugen_count`` have gone up
after adding the synth to our server.  We'll discuss these concepts in
following sections.

Querying the node tree with :py:meth:`~supriya.realtime.servers.Server.query`
will return a "query tree" representation, which you can print to generate
output similar to :term:`SuperCollider`'s ``s.queryAllNodes`` server method::

    >>> server.query()
    >>> print(_)

Access the server's :term:`root node` and :term:`default group`::

    >>> server.root_node
    >>> server.default_group

And access the input and output audio :term:`bus` groups, which represent
microphone inputs and speaker outputs::

    >>> server.audio_input_bus_group
    >>> server.audio_output_bus_group

.. book::
    :hide:

    >>> server.quit()

Interaction
-----------

.. book::
    :hide:

    >>> server.boot()

The server provides a variety of methods for interacting with it and modifying
its state.

You can send :term:`OSC` messages via the
:py:meth:`~supriya.realtime.servers.Server.query` method, either as lists, as
explicit :py:class:`~supriya.osc.messages.OscMessage` or
:py:class:`~supriya.osc.messages.OscBundle` objects, or as
:py:class:`~supriya.commands.bases.Requestable` objects::

    >>> server.send(["/g_new", 1000, 0, 1])

Many interactions with :term:`scsynth` don't take effect immediately. In fact,
none of them really do, because the server behaves asynchronously. For
operations with significant delay, e.g. sending multiple :term:`SynthDefs
<SynthDef>`, use :py:meth:`~supriya.realtime.servers.Server.sync` to block
until all previously initiated operations complete::

    >>> server.sync()

..  note:: See :doc:`../osc` for more information about OSC communication with
    the server, including OSC callbacks.

The server provides methods for allocating :term:`nodes <node>` (:term:`groups
<group>` and :term:`synths <synth>`), :term:`buffers <buffer>` and :term:`buses
<bus>`, all of which are discussed in the sections following this one::

    >>> server.add_group()
    >>> server.add_synth(amplitude=0.25, frequency=441.3)
    >>> server.add_buffer(channel_count=1, frame_count=512)
    >>> server.add_buffer_group(buffer_count=8, channel_count=2, frame_count=1024)
    >>> server.add_bus()
    >>> server.add_bus_group(bus_count=2, calculation_rate="audio")
    >>> print(server.query())

Resetting
`````````

Supriya supports *resetting* the state of the server, similar to
SuperCollider's ``CmdPeriod``::

    >>> server.reset()
    >>> print(server.query())

You can also just *reboot* the server, completely resetting all nodes, buses,
buffers and SynthDefs::

    >>> server.reboot()

.. book::
    :hide:

    >>> server.quit()

Lower level APIs
----------------

You can kill all running ``scsynth`` processes via :py:func:`supriya.scsynth.kill`::

    >>> supriya.scsynth.kill()

Get access to the server's underlying process management subsystem via
:py:attr:`~supriya.realtime.servers.Server.process_protocol`::

    >>> server.boot().process_protocol

Get access to the server's underlying OSC subsystem via
:py:attr:`~supriya.realtime.servers.Server.osc_protocol`::

    >>> server.osc_protocol

.. note::

    :py:class:`~supriya.realtime.servers.Server` manages its :term:`scsynth`
    subprocess and OSC communication via
    :py:class:`~supriya.realtime.protocols.SyncProcessProtocol` and
    :py:class:`~supriya.osc.protocols.ThreadedOscProtocol` objects while the
    :py:class:`~supriya.realtime.servers.AsyncServer` discussed later in
    :doc:`async` uses
    :py:class:`~supriya.realtime.protocols.AsyncProcessProtocol` and
    :py:class:`~supriya.osc.protocols.AsyncOscProtocol` objects.
