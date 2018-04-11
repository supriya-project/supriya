from supriya.ugens.UGen import UGen


class Done(UGen):
    """
    Triggers when `source` sets its `done` flag.

    ::

        >>> source = supriya.ugens.Line.kr()
        >>> done = supriya.ugens.Done.kr(
        ...     source=source,
        ...     )
        >>> done
        Done.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        if not (hasattr(source, 'has_done_flag') and source.has_done_flag):
            raise ValueError(repr(source))
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        """
        Constructs a control-rate "done" trigger.

        ::

            >>> source = supriya.ugens.Line.kr(duration=[1, 2])
            >>> done = supriya.ugens.Done.kr(
            ...     source=source,
            ...     )
            >>> done
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of Done.

        ::

            >>> source = supriya.ugens.Line.kr()
            >>> done = supriya.ugens.Done.kr(
            ...     source=source,
            ...     )
            >>> done.source
            Line.kr()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
