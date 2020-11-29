Non-realtime usage
==================

::

    >>> session = supriya.Session()

::

    >>> with session.at(0):
    ...     synth = session.add_synth(duration=3)
    ...

::

    >>> with session.at(1):
    ...     group = session.add_group()
    ...

::

    >>> with session.at(2):
    ...     synth["frequency"] = 666.6
    ...

::

    >>> with session.at(1.5):
    ...     group.move_node(synth, "ADD_TO_HEAD")
    ...

