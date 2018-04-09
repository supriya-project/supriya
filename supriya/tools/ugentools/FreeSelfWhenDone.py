from supriya.tools.ugentools.UGen import UGen


class FreeSelfWhenDone(UGen):
    """
    Frees the enclosing synth when `source` sets its `done` flag.

    ::

        >>> source = ugentools.Line.kr()
        >>> free_self_when_done = ugentools.FreeSelfWhenDone.kr(
        ...     source=source,
        ...     )
        >>> free_self_when_done
        FreeSelfWhenDone.kr()

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
        Constructs a control-rate ugen.

        ::

            >>> source = ugentools.Line.kr()
            >>> free_self_when_done = ugentools.FreeSelfWhenDone.kr(
            ...     source=source,
            ...     )
            >>> free_self_when_done
            FreeSelfWhenDone.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of FreeSelfWhenDone.

        ::

            >>> source = ugentools.Line.kr()
            >>> free_self_when_done = ugentools.FreeSelfWhenDone.kr(
            ...     source=source,
            ...     )
            >>> free_self_when_done.source
            Line.kr()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
