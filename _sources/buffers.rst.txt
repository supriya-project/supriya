Buffers
=======

:term:`Buffers <buffer>` are arrays of sample data. Like sound files, they have
one or more :term:`channels <channel>`, and one or more :term:`frames <frame>`.
They can be read from disk (or written back to it), created empty and populated
later, or synthesized by the server - typically to create window functions or
waveforms for wavetable synthesis. They're also used when streaming audio to or
from soundfiles too large to load into memory at once.

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

.. note::

   :py:class:`Scores <supriya.contexts.nonrealtime.Score>` are neither online
   nor offline, so you can add buffers to them whenever you like.

Creation
````````

Buffers can be allocated empty or immediately filled with all or part of a
soundfile read from disk.

.. note::

    You must specify the number of channels and frames when allocating a buffer.

    These properties cannot be changed during the lifetime of the buffer.

Allocate an empty buffer with
:py:meth:`~supriya.contexts.realtime.Server.add_buffer` and print its
:term:`repr` to the terminal::

    >>> buffer_ = server.add_buffer(channel_count=1, frame_count=512)
    >>> buffer_

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

.. note::

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

    >>> file_path = supriya.assets_path / "audio/birds/birds-01.wav"

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

    >>> file_path = supriya.assets_path / "audio/sine_440hz_44100sr_16bit_octo.wav"

Allocating a buffer from this soundfile shows it contains eight channels::

    >>> server.add_buffer(file_path=file_path)

We can allocate a buffer from a subset of those channels by passing the number
of channels to grab via the ``channel_count`` parameter::

    >>> server.add_buffer(channel_indices=[0, 1], file_path=file_path)

.. todo:: Implement ``server.add_buffer_group(file_paths=[..., ..., ...])``

Deletion
````````

Free a buffer with::

    >>> buffer_.free()

Free a buffer group with::

    >>> buffer_group.free()

Disk IO
```````

- .read()
- .write()

Inspection
----------

- .buffer_id
- .__int__()

::

    >>> buffer_ = server.add_buffer(channel_count=2, frame_count=512)
    >>> buffer_.id_
    >>> int(buffer_)

Querying
````````

- .query()

::

    >>> buffer_ = server.add_buffer(channel_count=2, frame_count=512)
    >>> buffer_.query()

Getting
```````

- .get()
- .get_range()

::

    >>> buffer_.get(0, 2, 4)

Buffer UGens
````````````

- BufChannels
- BufDur
- BufFrames
- BufRateScale
- BufSampleRate
- BufSamples

Interaction
-----------

Setting
```````

- .set()
- .set_range()

Filling
```````

Given a single-channel buffer with 1024 samples::

    >>> buffer_ = server.add_buffer(channel_count=1, frame_count=128)

- .fill()
- .generate()

Copying
```````

- .copy()

Zeroing
```````

- .zero()

Normalizing
```````````

- .normalize()

Integration
-----------

Referencing
```````````

Buffer IO
`````````

- BufRd and BufWr
- PlayBuf and RecordBuf

Continuous Disk IO
``````````````````

- DiskIn and DiskOut
- VDiskIn
- ``leaving_open``
- .close()

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
    ...     phases=[0.0, 0.333, 0.666],
    ...     as_wavetable=True,
    ... )
    >>> supriya.plot(buffer_)

While ``/b_gen`` may be able to create waveforms in the expected wavetable
format, there's no functionality built into :term:`scsynth` to load arbitrary
soundfiles and convert them into wavetable format in the process, or to copy an
existing buffer's contents into another buffer and convert.

.. todo:: Implement wavetable utilities for loading arbitrary audio.

Configuration
-------------

The maximum number of buffers available in a context is controlled by its options.

- Options.buffer_count
