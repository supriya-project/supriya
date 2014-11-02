# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PauseSelf(UGen):
    r'''Pause the enclosing synth when triggered by `trigger`.
    
    ::

        >>> trigger = ugentools.Impulse.kr(frequency=1.0)
        >>> pause_self = ugentools.PauseSelf.kr(
        ...     trigger=trigger,
        ...     )
        >>> pause_self
        PauseSelf.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    _ordered_input_names = (
        'trigger',
        )

    __slots__ = (
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
            >>> pause_self = ugentools.PauseSelf.kr(
            ...     trigger=trigger,
            ...     )
            >>> pause_self
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def trigger(self):
        r'''Gets `trigger` input of PauseSelf.

        ::

            >>> trigger = ugentools.Impulse.kr(frequency=1.0)
            >>> pause_self = ugentools.PauseSelf.kr(
            ...     trigger=trigger,
            ...     )
            >>> pause_self.trigger
            OutputProxy(
                source=Impulse(
                    rate=<Rate.CONTROL: 1>,
                    frequency=1.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]