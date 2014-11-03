# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Free(UGen):
    r'''free the node at `node_id` when triggered by `trigger`.

    ::

        >>> node_id = 1000
        >>> trigger = ugentools.Impulse.kr(frequency=1.0)
        >>> free = ugentools.Free.kr(
        ...     node_id=node_id,
        ...     trigger=trigger,
        ...     )
        >>> free
        Free.kr()

    '''

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
        rate=None,
        trigger=None,
        node_id=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
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
        r'''Constructs a control-rate ugen.

        ::

            >>> node_id = 1000
            >>> trigger = ugentools.Impulse.kr(frequency=[1, 2])
            >>> free = ugentools.Free.kr(
            ...     node_id=node_id,
            ...     trigger=trigger,
            ...     )
            >>> free
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            trigger=trigger,
            node_id=node_id,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        r'''Gets `node_id` input of Free.

        ::

            >>> trigger = ugentools.Impulse.kr(frequency=1.0)
            >>> free = ugentools.Free.kr(
            ...     node_id=1000,
            ...     trigger=trigger,
            ...     )
            >>> free.node_id
            1000.0

        Returns input.
        '''
        index = self._ordered_input_names.index('node_id')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of Free.

        ::

            >>> trigger = ugentools.Impulse.kr(frequency=1.0)
            >>> free = ugentools.Free.kr(
            ...     node_id=1000,
            ...     trigger=trigger,
            ...     )
            >>> free.trigger
            OutputProxy(
                source=Impulse(
                    rate=<CalculationRate.CONTROL: 1>,
                    frequency=1.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]