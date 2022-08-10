Fake Docs
=========

::

    >>> import platform
    >>> if platform.system() != "Windows":
    ...     say_hello = supriya.Say("Hello world!", voice="Daniel")
    ...     supriya.play(say_hello)
    ...

::

    >>> session_one = supriya.Session(
    ...     name="inner-session",
    ... )
    >>> with session_one.at(0):
    ...     synth = session_one.add_synth(duration=10)
    ...

::

    >>> with supriya.synthdefs.SynthDefBuilder(out_bus=0, buffer_id=0) as builder:
    ...     source = supriya.ugens.DiskIn.ar(
    ...        buffer_id=builder["buffer_id"], channel_count=8
    ...     )
    ...     supriya.ugens.Out.ar(bus=builder["out_bus"], source=source)
    ...
    >>> diskin_synthdef = builder.build()

::

    >>> session_two = supriya.Session(name="middle-session")
    >>> with session_two.at(0):
    ...     buffer_one = session_two.cue_soundfile(session_one, duration=10)
    ...     buffer_two = session_two.cue_soundfile(session_one, duration=10)
    ...     session_two.add_synth(
    ...         synthdef=diskin_synthdef, buffer_id=buffer_one, duration=10
    ...     )
    ...     session_two.add_synth(
    ...         synthdef=diskin_synthdef, buffer_id=buffer_two, duration=10
    ...     )

::

    >>> session_three = supriya.Session(name="outer-session")
    >>> with session_three.at(0):
    ...     buffer_one = session_three.cue_soundfile(session_one, duration=10)
    ...     buffer_two = session_three.cue_soundfile(session_two, duration=10)
    ...     session_three.add_synth(
    ...         synthdef=diskin_synthdef, buffer_id=buffer_one, duration=10
    ...     )
    ...     session_three.add_synth(
    ...         synthdef=diskin_synthdef, buffer_id=buffer_two, duration=10
    ...     )

::

    >>> supriya.play(session_three)
