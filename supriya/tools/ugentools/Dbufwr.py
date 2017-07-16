from supriya.tools.ugentools.DUGen import DUGen


class Dbufwr(DUGen):
    """
    A buffer-writing demand-rate UGen.

    ::

        >>> dbufwr = ugentools.Dbufwr(
        ...     buffer_id=0,
        ...     source=0,
        ...     loop=1,
        ...     phase=0,
        ...     )
        >>> dbufwr
        Dbufwr()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'buffer_id',
        'phase',
        'loop',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=0,
        source=0,
        loop=1,
        phase=0,
        ):
        DUGen.__init__(
            self,
            buffer_id=buffer_id,
            source=source,
            loop=loop,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=0,
        source=0,
        loop=1,
        phase=0,
        ):
        """
        Constructs a Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr.new(
            ...     buffer_id=0,
            ...     source=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr
            Dbufwr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            source=source,
            loop=loop,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr(
            ...     buffer_id=0,
            ...     source=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr.buffer_id
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def has_done_flag(self):
        """
        Is true if UGen has a done flag.

        Returns boolean.
        """
        return True

    @property
    def loop(self):
        """
        Gets `loop` input of Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr(
            ...     buffer_id=0,
            ...     source=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr.loop
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def phase(self):
        """
        Gets `phase` input of Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr(
            ...     buffer_id=0,
            ...     source=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr.phase
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr(
            ...     buffer_id=0,
            ...     source=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr.source
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
