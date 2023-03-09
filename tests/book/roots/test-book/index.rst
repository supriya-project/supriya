Fake Docs
=========

::

    >>> import platform
    >>> from supriya.soundfiles import Say
    >>> if platform.system() != "Windows":
    ...     say_hello = Say("Hello world!", voice="Daniel")
    ...     supriya.play(say_hello)
    ...

::

    >>> score = supriya.Score()
    >>> with score.at(0):
    ...     with score.add_synthdefs(supriya.default):
    ...         synth = score.add_synth(supriya.default)
    ...
    >>> with score.at(10):
    ...     score.do_nothing()
    ...
    >>> supriya.play(score)

::

    >>> server = supriya.Server().boot()
    >>> with server.at():
    ...     buffer_ = server.add_buffer(channel_count=1, frame_count=512)
    ...     with buffer_:
    ...         buffer_.generate("sine1", amplitudes=[1.0])
    ...
    >>> server.sync()
    >>> supriya.play(buffer_)
    >>> supriya.plot(buffer_)
