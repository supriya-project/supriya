Async
=====

Outline:

- what is async server
- instantiation
- basic usage
- differences with non-async server

Supriya supports asyncio event loops via a stripped-down
:py:class:`~supriya.realtime.servers.AsyncServer`, which provides async
variants of a subset of :py:class:`~supriya.realtime.servers.Server`'s methods.

Perform some work asyncronously::

    >>> import asyncio

    >>> async def main():
    ...     # Instantiate an async server
    ...     print(async_server := supriya.AsyncServer())
    ...     # Boot it on an arbitrary open port
    ...     print(await async_server.boot(port=supriya.osc.find_free_port()))
    ...     # Send an OSC message to the async server (doesn't require await!)
    ...     async_server.send(["/g_new", 1000, 0, 1])
    ...     # Query the async server's node tree
    ...     print(await async_server.query())
    ...     # Quit the async server
    ...     print(await async_server.quit())
    ...

    >>> asyncio.run(main())

Use :py:class:`~supriya.realtime.server.AsyncServer` with the
:py:class:`~supriya.clocks.asynchronous.AsyncClock` and
:py:class:`~supriya.providers.Provider` classes to integrate with
eventloop-driven libraries like `aiohttp`_, `python-prompt-toolkit`_ and
`pymonome`_.

.. _aiohttp: https://docs.aiohttp.org/
.. _python-prompt-toolkit: https://python-prompt-toolkit.readthedocs.io/
.. _pymonome: https://github.com/artfwo/pymonome
