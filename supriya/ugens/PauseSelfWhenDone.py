from supriya.ugens.UGen import UGen


class PauseSelfWhenDone(UGen):
    """
    Pauses the enclosing synth when `source` sets its `done` flag.

    ::

        >>> source = supriya.ugens.Line.kr()
        >>> pause_self_when_done = supriya.ugens.PauseSelfWhenDone.kr(
        ...     source=source,
        ...     )
        >>> pause_self_when_done
        PauseSelfWhenDone.kr()

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

            >>> source = supriya.ugens.Line.kr()
            >>> pause_self_when_done = supriya.ugens.PauseSelfWhenDone.kr(
            ...     source=source,
            ...     )
            >>> pause_self_when_done
            PauseSelfWhenDone.kr()

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
        Gets `source` input of PauseSelfWhenDone.

        ::

            >>> source = supriya.ugens.Line.kr()
            >>> pause_self_when_done = supriya.ugens.PauseSelfWhenDone.kr(
            ...     source=source,
            ...     )
            >>> pause_self_when_done.source
            Line.kr()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
