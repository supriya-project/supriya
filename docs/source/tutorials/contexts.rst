Contexts
========

Supriya's :py:class:`context <supriya.contexts.core.Context>` interface exposes
a set of common functions for interacting with :term:`scsynth`-compatible
execution contexts in both *realtime* and *non-realtime*.

::

    >>> server = supriya.Server().boot()  # realtime
    >>> score = supriya.Score()  # non-realtime

See the :doc:`servers <servers>` and :doc:`scores <scores>` pages for in-depth
documentation on how each type of context works.

Types of contexts
-----------------

There are really two broad categories of contexts: write-only non-realtime
contexts, and read/write realtime contexts.

..  inheritance-diagram:: supriya.contexts
    :lineage: supriya.contexts.core.Context

Write-only contexts
```````````````````

The SuperCollider server's non-realtime mode doesn't support queries, only mutations.
E.g. you *cannot* ask for the server's status, for information about a node, for the
structure of the node tree, for the contents of a buffer. You can only modify
the state of the server. Therefore non-realtime contexts - scores - are
*write-only*.

Mutations in Supriya's context implementations are synchronous in the Pythonic sense of
sync-vs-async: the messages just fire off.

Read/write contexts
```````````````````

The SuperCollider server's realtime mode supports queries *and* mutations. You
*can* ask for the for the server's status, for information about a node, for
the structure of the node tree, for the contents of a buffer, and the server
will reply with a message encoding that information.

Queries in Supriya's context implementations may be synchronous or asynchronous
(in the Pythonic sense of async/await syntax), and which specific syntax
depends on the specific type of server used and what concurrency paradigm it
supports. :py:class:`"Async" servers <supriya.contexts.realtime.AsyncServer>`
support async/await syntax for queries, while :py:class:`"sync" servers
<supriya.contexts.realtime.Server>` will block the current thread until their
query replies arrive.

Moments
-------

Contexts can bundle requests together via
:py:class:`~supriya.contexts.core.Moment` context managers.

For non-realtime contexts, all requests must happen inside a moment, while for
realtime contexts issuing requests outside of a moment - or inside a moment
with no timestamp - simply means "do this as soon as possible". Use
:py:meth:`~supriya.contexts.core.Context.at` to create a new moment.

-   Scores count time from zero:

    ::
        
        >>> with score.at(0):
        ...     score_group = score.add_group()
        ... 

-   Servers use real timestamps:

    ::

        >>> import time
        >>> with server.at(time.time() + 0.1):  # 0.1 seconds from now
        ...     server_group = server.add_group()
        ...

-   Servers can use moments without timestamps:

    ::

        >>> with server.at():  # do it ASAP
        ...     server.add_group()
        ...

-   Servers can also omit moments entirely:

    ::

        >>> server.add_group()

Completions
-----------

Some commands to :term:`SuperCollider` are "async" and may take multiple
control blocks to complete, e.g. reading a file from disk into a buffer. These
commands often accept a final "completion message": an OSC message or bundle to
be executed once the original command completes. A common use-case is to load a
:term:`SynthDef` and then allocate a synth using that definition in the
completion message.

Like moments, Supriya exposes completions via
:py:class:`~supriya.contexts.core.Completion` context managers. Some context
methods return a completion, and all requests issued inside that completion's
context with be bundled together into the original request's ``on_completion``
argument.

::

    >>> with score.at(0):
    ...     with score.add_synthdefs(supriya.default):
    ...         score.add_synth(supriya.default, target_node=score_group)
    ...

::

    >>> with server.at():
    ...     with server.add_synthdefs(supriya.default):
    ...         server.add_synth(supriya.default, target_node=server_group)
    ...

Because realtime contexts can issue requests outside of a moment context, all
command methods that return completions also accept an ``on_completion``
argument: a callable taking the context as its only argument. This callable
will be executed and any issued requests will be bundled as a completion
message.

::

    >>> server.add_synthdefs(
    ...     supriya.default,
    ...     on_completion=lambda context: context.add_synth(supriya.default),
    ... )

If issuing commands inside a moment, the completion must be used before the
moment closes, because the request to which the completion message will be
added will have been sent once the moment closed.

..  book::
    :allow-exceptions:

    >>> with server.at():
    ...     completion = server.add_buffer(channel_count=1, frame_count=512)
    ...
    >>> with completion:
    ...     ...
    ...
