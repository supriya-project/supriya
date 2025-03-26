Realtime Servers
================

Supriya's :py:class:`~supriya.contexts.realtime.Server` provides a handle to a
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

You can also explicitly select the server binary via the ``executable`` keyword::

    >>> server.boot(executable="scsynth")

.. book::
    :hide:

    >>> server.quit()

The ``executable`` keyword allows you to boot with ``supernova`` if you have it available::

    >>> server.boot(executable="supernova")

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
    ...     ip_address=server_one.options.ip_address,
    ...     port=server_one.options.port,
    ... )

Each connected user has their own client ID and default group::

    >>> server_one.client_id
    >>> server_two.client_id
    >>> print(server_one.query_tree())

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

Lifecycle events
````````````````

Supriya allows hooking into server lifecycle events via lifecycle callbacks.
Use lifecycle callbacks to execute code before booting, once booting, before
quitting, after quitting, or even on server panic:

    >>> for event in supriya.ServerLifecycleEvent:
    ...     print(repr(event))
    ..

..  note:: This is spiritually equivalent to :term:`sclang`'s ``Server.doWhenBooted``.

..  tip:: Use lifecycle callbacks to load SynthDefs on server boot. Make sure
    to sync the server inside the callback procedure so your code blocks until
    the loading completes.

Define a callback and register it against one or more events:

    >>> def print_event(event):
    ...     print(repr(event))
    ...
    >>> callback = server.register_lifecycle_callback(
    ...     event=list(supriya.ServerLifecycleEvent),
    ...     procedure=print_event,
    ... )

Boot the server and watch the events print:

    >>> server.boot()

Quit the server and watch the events print:

    >>> server.quit()

Unregister the callback:

    >>> server.unregister_lifecycle_callback(callback)

Inspection
----------

:py:class:`~supriya.contexts.realtime.Server` provides a number of methods and
properties for inspecting its state.

Let's boot the server again::

    >>> server = supriya.Server().boot()

Querying status
```````````````

Inspect the "status" of audio processing::

    >>> server.status

.. hint::

    Server status is a great way of tracking :term:`scsynth`'s CPU usage.

Let's add a SynthDef and a synth - explained :doc:`soon <nodes>` - to increase the
complexity of the status output::

    >>> with server.at():
    ...     with server.add_synthdefs(supriya.default):
    ...         synth = server.add_synth(supriya.default)
    ...

.. book::
    :hide:

    >>> server.sync()
    >>> supriya.contexts.requests.QueryStatus().communicate(server=server)

::

    >>> server.status

Note that ``synth_count``, ``synthdef_count`` and ``ugen_count`` have gone up
after adding the synth to our server.  We'll discuss these concepts in
following sections.

Querying nodes
``````````````

Querying the node tree with :py:meth:`~supriya.contexts.realtime.Server.query`
will return a "query tree" representation, which you can print to generate
output similar to :term:`SuperCollider`'s ``s.queryAllNodes`` server method::

    >>> server.query_tree()
    >>> print(_)

Querying default entities
`````````````````````````

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
    >>> server.add_synthdefs(supriya.default)
    >>> server.sync()

The server provides a variety of methods for interacting with it and modifying
its state.

Sending OSC
```````````

You can send :term:`OSC` messages via the
:py:meth:`~supriya.contexts.realtime.Server.send` method, either as
explicit :py:class:`~supriya.osc.OscMessage` or
:py:class:`~supriya.osc.OscBundle` objects, or as
:py:class:`~supriya.contexts.requests.Requestable` objects::

    >>> from supriya.osc import OscMessage
    >>> server.send(OscMessage("/g_new", 1000, 0, 1))

Syncing
```````

Many interactions with :term:`scsynth` don't take effect immediately. In fact,
none of them really do, because the server behaves asynchronously. For
operations with significant delay, e.g. sending multiple :term:`SynthDefs
<SynthDef>` or reading/writing buffers from/to disk, use
:py:meth:`~supriya.contexts.realtime.Server.sync` to block until all previously
initiated operations complete::

    >>> server.sync()

..  note:: See :doc:`../osc` for more information about OSC communication with
    the server, including OSC callbacks.

Mutating
````````

The server provides methods for allocating :term:`nodes <node>` (:term:`groups
<group>` and :term:`synths <synth>`), :term:`buffers <buffer>` and :term:`buses
<bus>`, all of which are discussed in the sections following this one::

    >>> server.add_group()
    >>> server.add_synth(supriya.default, amplitude=0.25, frequency=441.3)
    >>> server.add_buffer(channel_count=1, frame_count=512)
    >>> server.add_buffer_group(count=8, channel_count=2, frame_count=1024)
    >>> server.add_bus()
    >>> server.add_bus_group(count=2, calculation_rate="audio")
    >>> print(server.query_tree())

Resetting
`````````

Supriya supports *resetting* the state of the server, similar to
SuperCollider's ``CmdPeriod``::

    >>> server.reset()
    >>> print(server.query_tree())

You can also just *reboot* the server, completely resetting all nodes, buses,
buffers and SynthDefs::

    >>> server.reboot()

.. book::
    :hide:

    >>> server.quit()

Async servers
-------------

Supriya supports asyncio event loops via
:py:class:`~supriya.contexts.realtime.AsyncServer`, which provides async
variants of many :py:class:`~supriya.contexts.realtime.Server`'s methods. All
lifecycle methods (booting, quitting) are async, and all getter and query
methods are async as well.

::

    >>> import asyncio

::

    >>> async def main():
    ...     # Instantiate an async server
    ...     print(async_server := supriya.AsyncServer())
    ...     # Boot it on an arbitrary open port
    ...     print(await async_server.boot(port=supriya.osc.find_free_port()))
    ...     # Send an OSC message to the async server (doesn't require await!)
    ...     async_server.send(["/g_new", 1000, 0, 1])
    ...     # Query the async server's node tree
    ...     print(await async_server.query_tree())
    ...     # Quit the async server
    ...     print(await async_server.quit())
    ...

::

    >>> asyncio.run(main())

Use :py:class:`~supriya.contexts.realtime.AsyncServer` with
:py:class:`~supriya.clocks.asynchronous.AsyncClock` to integrate with
eventloop-driven libraries like `aiohttp`_, `python-prompt-toolkit`_ and
`pymonome`_.

Lower level APIs
----------------

You can kill all running ``scsynth`` processes via :py:func:`supriya.scsynth.kill`::

    >>> supriya.scsynth.kill()

Get access to the server's underlying process management subsystem via
:py:attr:`~supriya.contexts.realtime.Server.process_protocol`::

    >>> server.process_protocol

Get access to the server's underlying OSC subsystem via
:py:attr:`~supriya.contexts.realtime.Server.osc_protocol`::

    >>> server.osc_protocol

.. note::

    :py:class:`~supriya.contexts.realtime.Server` manages its :term:`scsynth`
    subprocess and OSC communication via
    :py:class:`~supriya.scsynth.SyncProcessProtocol` and
    :py:class:`~supriya.osc.ThreadedOscProtocol` objects while the
    :py:class:`~supriya.contexts.realtime.AsyncServer` discussed later uses
    :py:class:`~supriya.scsynth.AsyncProcessProtocol` and
    :py:class:`~supriya.osc.AsyncOscProtocol` objects.

.. _aiohttp: https://docs.aiohttp.org/
.. _python-prompt-toolkit: https://python-prompt-toolkit.readthedocs.io/
.. _pymonome: https://github.com/artfwo/pymonome
