# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class FreeSelf(UGen):
    r'''Free the enclosing synth when triggered by `trigger`.

    ::

        >>> trigger = ugentools.Impulse.kr(frequency=1.0)
        >>> free_self = ugentools.FreeSelf.kr(
        ...     trigger=trigger,
        ...     )
        >>> free_self
        FreeSelf.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        trigger=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        trigger=None,
        ):
        r'''Constructs a control-rate ugen.

        ::

            >>> trigger = ugentools.Impulse.kr(frequency=[1, 2])
            >>> free_self = ugentools.FreeSelf.kr(
            ...     trigger=trigger,
            ...     )
            >>> free_self
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def trigger(self):
        r'''Gets `trigger` input of FreeSelf.

        ::

            >>> trigger = ugentools.Impulse.kr(frequency=1.0)
            >>> free_self = ugentools.FreeSelf.kr(
            ...     trigger=trigger,
            ...     )
            >>> free_self.trigger
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