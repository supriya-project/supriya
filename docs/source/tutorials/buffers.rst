:status: under-construction

Buffers
=======

..  self-criticism::

    These docs are still under construction. It's true!

:term:`Buffers <buffer>` are fixed-size arrays of sample data. Like sound
files, they have one or more :term:`channels <channel>`, and one or more
:term:`frames <frame>`. They can be read from disk (or written back to it),
created empty and populated later, or synthesized by the server - typically to
create window functions or waveforms for wavetable synthesis. They're also used
when streaming audio to or from soundfiles too large to load into memory at
once.

Like buses, :term:`scsynth` boots with a fixed number of buffers available.
Unlike buses, these buffers can be reconfigured with different channel counts
and durations on allocation. The :py:class:`~supriya.contexts.entities.Buffer`
class provides a :term:`proxy` to the buffer datastructure residing in a
running :term:`scsynth` process, and the
:py:class:`~supriya.contexts.entities.BufferGroup` class models a contiguous
block of buffers.

Lifecycle
---------

Buffers can only be added to running servers, so let’s create one and boot it:

    >>> server = supriya.Server().boot()

..  note::

    :py:class:`Scores <supriya.contexts.nonrealtime.Score>` are neither online
    nor offline, so you can add buffers to them whenever you like.

Creation
````````

Buffers can be allocated empty or immediately filled with all or part of a
soundfile read from disk.

Let's allocate an empty buffer with
:py:meth:`~supriya.contexts.realtime.Server.add_buffer` and print its
:term:`repr` to the terminal::

    >>> buffer_ = server.add_buffer(channel_count=1, frame_count=512)
    >>> buffer_

..  note::

    You must specify the number of channels and frames when allocating a buffer.

    These properties cannot be changed during the lifetime of the buffer.

The :term:`repr` shows the buffer's type (``Buffer``), its :term:`ID <ID,
buffer>` (``0``) and indicates it has been allocated (``+``).

Now, allocate a contiguous group of four empty buffers with
:py:meth:`~supriya.contexts.realtime.Server.add_buffer_group` and print its
:term:`repr` to the terminal::

    >>> buffer_group = server.add_buffer_group(
    ...     count=4, channel_count=1, frame_count=512
    ... )
    >>> buffer_group

The :term:`repr` shows the buffer group's type (``BufferGroup``), the :term:`ID
<ID, buffer>` of the first buffer in the group (``1``) and indicates it has
been allocated (``+``).

..  note::

    Why use a :py:class:`~supriya.contexts.entities.BufferGroup`?

    While you could allocate multiple single buffers, allocating a group of
    buffers in a single operation guarantees that the IDs of the buffers are
    contiguous. Some :term:`UGens <UGen>` that operator on buffers, like the
    wavetable oscillator :py:class:`~supriya.ugens.osc.VOsc`, expect that the
    buffers they operate over are contiguously allocated.

    The buffer group's :py:meth:`~supriya.contexts.entities.BufferGroup.free`
    method also guarantees that those IDs are released back to the allocator
    pool simultaneously.

Creation from files
```````````````````

Let's locate a soundfile::

    >>> file_path = supriya.samples_path / "birds-01.wav"

Allocate a buffer from a soundfile by passing a value to ``file_path`` when
using :py:meth:`~supriya.contexts.realtime.Server.add_buffer`::

    >>> buffer_ = server.add_buffer(file_path=file_path)

Let's plot it, and play it::

    >>> supriya.plot(buffer_)
    >>> supriya.play(buffer_)

Note that ``channel_count`` and ``frame_count`` were omitted; we're taking the
full set of channels and frames from the source file when reading its contents
into the buffer.

We can allocate a buffer from a partial soundfile by passing a combination of
``channel_count``, ``frame_count`` and ``starting_frame`` parameters. Let's
allocate a buffer from the middle of that soundfile, plot it and play it::

    >>> buffer_ = server.add_buffer(
    ...     file_path=file_path, frame_count=8192, starting_frame=33091 // 2
    ... )
    >>> supriya.plot(buffer_)
    >>> supriya.play(buffer_)

Let's grab another soundfile, this time an octophonic one::

    >>> file_path = supriya.samples_path / "sine_440hz_44100sr_16bit_octo.wav"

Allocating a buffer from this soundfile shows it contains eight channels::

    >>> server.add_buffer(file_path=file_path)

We can allocate a buffer from a subset of those channels by passing the number
of channels to grab via the ``channel_count`` parameter::

    >>> server.add_buffer(channel_indices=[0, 1], file_path=file_path)

..  todo:: Implement ``server.add_buffer_group(file_paths=[..., ..., ...])``

Deletion
````````

Free a buffer with::

    >>> buffer_.free()

Note that freeing the buffer returns a
:py:class:`~supriya.contexts.core.Completion` context manager, allowing you to
chain additional commands after the free operation completes.

Free a buffer group with::

    >>> buffer_group.free()

Disk IO
```````

Buffers can be read into or written back to disk *after* they've been
allocated, via their :py:meth:`~supriya.contexts.entities.Buffer.read` and
:py:meth:`~supriya.contexts.entities.Buffer.write` methods.

Reading a file into a buffer takes nearly the same arguments as allocating a
buffer from a file, including frame start and count, channel indices, completion messages, etc.::

    >>> buffer_ = server.add_buffer(frame_count=1024)
    >>> _ = buffer_.read(file_path, frame_count=512, starting_frame=256, channel_indices=[1])
    >>> _ = server.sync()
    >>> supriya.plot(buffer_)

Writing a buffer to a file also accepts frame start and count, and a completion
message, but always writes out all channels in the buffer. You can also select
what file format and sample format you'd like in the resulting audio file:

::

    >>> import pathlib, tempfile
    >>> with tempfile.TemporaryDirectory() as tmpdirname:
    ...     path = pathlib.Path(tmpdirname) / "audio.aiff"
    ...     _ = buffer_.write(
    ...         path,
    ...         frame_count=768,
    ...         header_format="aiff",
    ...         sample_format="int16",
    ...         starting_frame=128,
    ...     )
    ...     # wait for writing to complete before deleting the tempdir
    ...     _ = server.sync()
    ...

SuperCollider supports a relatively small set of header and sample formats::

    >>> for x in supriya.HeaderFormat:
    ...     print(repr(x))
    ...

::

    >>> for x in supriya.SampleFormat:
    ...     print(repr(x))
    ...

Both reading into buffers and writing out of buffers also support a `leave_open`
boolean keyword, allowing more audio to be read into or out of the buffer
during its lifetime. We'll demonstrate this when discussing :ref:`disk IO UGens
<Disk IO UGens>` further on.

Inspection
----------

Like nodes and buses, buffers and buffer groups know a few things about
themselves and can query the server for additional information.

Let's reset the server for a clean slate::

    >>> _ = server.reset()

... and then allocate a fresh buffer and buffer group::

    >>> buffer_ = server.add_buffer(channel_count=2, frame_count=512)
    >>> buffer_group = server.add_buffer_group(channel_count=1, count=4, frame_count=1024)

Identity and context
````````````````````

Like :doc:`nodes <nodes>` and :doc:`buses <buses>`, every buffer has an ``id_``
and a reference to its context::

    >>> buffer_.id_, buffer_.context

Buffer groups also have an ID and context reference, using the first child
buffer in the group::

    >>> buffer_group.id_, buffer_group.context

Buffer group members
````````````````````

Buffer groups know how many buffers they contain, and can hand them back to you as
:py:class:`~supriya.contexts.entities.Buffer` instances::

    >>> len(buffer_group)
    >>> buffer_group.buffers

Buffer groups can be indexed, sliced and iterated over, just like a sequence::

    >>> buffer_group[0]
    >>> buffer_group[1:3]
    >>> for child in buffer_group:
    ...     child.id_
    ...

Note that the ``id_`` of each buffer is one greater than the last. That's what we
mean by a *contiguous* block.

Querying
````````

- Buffer.query()

::

    >>> buffer_ = server.add_buffer(channel_count=2, frame_count=512)
    >>> buffer_.query()

Getting
```````

- Buffer.get()
- Buffer.get_range()

::

    >>> buffer_.get(0, 2, 4)

::

    >>> buffer_.get_range(0, 4)

Interaction
-----------

::

    >>> buffer_ = server.add_buffer(channel_count=1, frame_count=128)
    >>> server.sync()

Setting
```````

- Buffer.set()
- Buffer.set_range()

::

    >>> buffer_.set(64, 0.5)
    >>> supriya.plot(buffer_)

::

    >>> buffer_.set_range(96, [1.0, -1.0, 1.0, -1.0])
    >>> supriya.plot(buffer_)

Filling
```````
- Buffer.fill()

::

    >>> buffer_.fill(32, 16, -0.5)
    >>> supriya.plot(buffer_)

Generating
``````````

- Buffer.generate()

::

    >>> buffer_.generate(
    ...     command_name="cheby",
    ...     amplitudes=[1.0, 0.5, 0.25],
    ... )
    >>> supriya.plot(buffer_)

::

    >>> buffer_.generate(
    ...     command_name="sine1",
    ...     amplitudes=[1.0, 0.5, 0.25],
    ... )
    >>> supriya.plot(buffer_)

::

    >>> buffer_.generate(
    ...     command_name="sine2",
    ...     amplitudes=[1.0, 0.5, 0.25],
    ...     frequencies=[1, 3, 5],
    ... )
    >>> supriya.plot(buffer_)


::

    >>> buffer_.generate(
    ...     command_name="sine3",
    ...     amplitudes=[1.0, 0.5, 0.25],
    ...     frequencies=[1, 3, 5],
    ...     phases=[0.0, 0.333, -0.666],
    ... )
    >>> supriya.plot(buffer_)

Copying
```````

- Buffer.copy()

::

    >>> other_buffer = server.add_buffer(channel_count=1, frame_count=128)
    >>> buffer_.copy(
    ...     target_buffer=other_buffer,
    ...     starting_frame=32,
    ...     target_starting_frame=0,
    ...     frame_count=64
    ... )
    >>> supriya.plot(other_buffer)

Normalizing
```````````
We can *normalize* a buffer, scaling its samples such that their maximum
absolute value matches our desired maximum, typically `1.0`:

::

    >>> buffer_.normalize()
    >>> supriya.plot(buffer_)

Zeroing
```````

We can *zero* a buffer, setting all of its samples to `0.0`:

::

    >>> buffer_.zero()
    >>> supriya.plot(buffer_)

Note that zeroing a buffer returns a
:py:class:`~supriya.contexts.core.Completion` context manager, allowing you to
chain additional commands after the zero operation completes.

Integration
-----------

Supriya's :py:class:`~supriya.contexts.entities.Buffer` and
:py:class:`~supriya.contexts.entities.BufferGroup` classes provide affordances for
interacting with other parts of the system.

Referencing
```````````

Buffers and buffer groups fulfil ``SupportsInt``, so you can pass them anywhere an
integer ID is expected::

    >>> int(buffer_)
    >>> int(buffer_group)

Info UGens
``````````

- BufChannels
- BufDur
- BufFrames
- BufRateScale
- BufSampleRate
- BufSamples

IO UGens
````````

- BufRd
- BufWr
- PlayBuf
- RecordBuf

.. _Disk IO UGens:

Disk IO UGens
`````````````

- DiskIn
- DiskOut
- VDiskIn
- ``leaving_open``
- Buffer.close()

Wavetable synthesis
```````````````````

SuperCollider provides a number of :term:`wavetable <wavetable synthesis>`
oscillators, including :py:class:`~supriya.ugens.osc.Osc`,
:py:class:`~supriya.ugens.osc.COsc`, :py:class:`~supriya.ugens.osc.VOsc`, and
:py:class:`~supriya.ugens.osc.VOsc3`

All of these :term:`UGens <UGen>` accept a ``buffer_id`` argument, pointing to
a buffer filled with some waveform to use as their source material.  The
interpolation algorithm used by these oscillators has one important
requirement: the waveforms *must* be in SuperCollider's "wavetable format".

We can ensure the buffer contents are in wavetable format when using any of
the ``.fill_...()`` methods by setting ``as_wavetable=True``.

Grab a fresh buffer::

    >>> buffer_ = server.add_buffer(channel_count=1, frame_count=128)

... and compare the following calls against the non-wavetable versions
demonstrated earlier::

    >>> buffer_.generate(
    ...     command_name="cheby",
    ...     amplitudes=[1.0, 0.5, 0.25],
    ...     as_wavetable=True,
    ... )
    >>> supriya.plot(buffer_)

    >>> buffer_.generate(
    ...     command_name="sine1",
    ...     amplitudes=[1.0, 0.5, 0.25],
    ...     as_wavetable=True,
    ... )
    >>> supriya.plot(buffer_)

    >>> buffer_.generate(
    ...     command_name="sine2",
    ...     amplitudes=[1.0, 0.5, 0.25],
    ...     frequencies=[1, 3, 5],
    ...     as_wavetable=True,
    ... )
    >>> supriya.plot(buffer_)

    >>> buffer_.generate(
    ...     command_name="sine3",
    ...     amplitudes=[1.0, 0.5, 0.25],
    ...     frequencies=[1, 3, 5],
    ...     phases=[0.0, 0.333, -0.666],
    ...     as_wavetable=True,
    ... )
    >>> supriya.plot(buffer_)

While ``/b_gen`` may be able to create waveforms in the expected wavetable
format, there's no functionality built into :term:`scsynth` to load arbitrary
soundfiles and convert them into wavetable format in the process, or to copy an
existing buffer's contents into another buffer and convert.

..  todo:: Implement wavetable utilities for loading arbitrary audio.

Configuration
-------------

The maximum number of buffers available in a context is controlled by its
:py:class:`options <supriya.scsynth.Options>`.

- Set the maximum number of buffers with the ``buffer_count`` keyword.

This can be set on an :py:class:`~supriya.scsynth.Options` instance passed the
context when initialized or booting, or just as keyword arguments.
