from supriya.ugens.DUGen import DUGen


class Dreset(DUGen):
    """
    Resets demand-rate UGens.

    ::

        >>> source = supriya.ugens.Dseries(start=0, step=2)
        >>> dreset = supriya.ugens.Dreset(
        ...     reset=0,
        ...     source=source,
        ...     )
        >>> dreset
        Dreset()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'reset',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        reset=0,
        source=None,
        ):
        DUGen.__init__(
            self,
            reset=reset,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        reset=0,
        source=None,
        ):
        """
        Constructs a Dreset.

        ::

            >>> source = supriya.ugens.Dseries(start=0, step=2)
            >>> dreset = supriya.ugens.Dreset.new(
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> dreset
            Dreset()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            reset=reset,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def reset(self):
        """
        Gets `reset` input of Dreset.

        ::

            >>> source = supriya.ugens.Dseries(start=0, step=2)
            >>> dreset = supriya.ugens.Dreset(
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> dreset.reset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Dreset.

        ::

            >>> source = supriya.ugens.Dseries(start=0, step=2)
            >>> dreset = supriya.ugens.Dreset(
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> dreset.source
            Dseries()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
