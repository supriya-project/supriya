from supriya.ugens.UGen import UGen


class Pause(UGen):
    """
    Pauses the node at `node_id` when triggered by `trigger`.

    ::

        >>> node_id = 1000
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> pause = supriya.ugens.Pause.kr(
        ...     node_id=node_id,
        ...     trigger=trigger,
        ...     )
        >>> pause
        Pause.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        trigger=None,
        node_id=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            trigger=trigger,
            node_id=node_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        trigger=None,
        node_id=None,
        ):
        """
        Constructs a control-rate ugen.

        ::

            >>> node_id = 1000
            >>> trigger = supriya.ugens.Impulse.kr(frequency=[1, 2])
            >>> pause = supriya.ugens.Pause.kr(
            ...     node_id=node_id,
            ...     trigger=trigger,
            ...     )
            >>> pause
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            trigger=trigger,
            node_id=node_id,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        """
        Gets `node_id` input of Pause.

        ::

            >>> node_id = 1000
            >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
            >>> pause = supriya.ugens.Pause.kr(
            ...     node_id=node_id,
            ...     trigger=trigger,
            ...     )
            >>> pause.node_id
            1000.0

        Returns input.
        """
        index = self._ordered_input_names.index('node_id')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of Pause.

        ::

            >>> node_id = 1000
            >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
            >>> pause = supriya.ugens.Pause.kr(
            ...     node_id=node_id,
            ...     trigger=trigger,
            ...     )
            >>> pause.trigger
            Impulse.kr()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
