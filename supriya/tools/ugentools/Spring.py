# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class Spring(UGen):
    r'''A resonating spring physical model.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> spring = ugentools.Spring.ar(
        ...     damping=0,
        ...     source=source,
        ...     spring=1,
        ...     )
        >>> spring
        Spring.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Physical Modelling UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'spring',
        'damping',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        damping=0,
        source=None,
        spring=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            source=source,
            spring=spring,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damping=0,
        source=None,
        spring=1,
        ):
        r'''Constructs an audio-rate Spring.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> spring = ugentools.Spring.ar(
            ...     damping=0,
            ...     source=source,
            ...     spring=1,
            ...     )
            >>> spring
            Spring.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            source=source,
            spring=spring,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        damping=0,
        source=None,
        spring=1,
        ):
        r'''Constructs a control-rate Spring.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> spring = ugentools.Spring.kr(
            ...     damping=0,
            ...     source=source,
            ...     spring=1,
            ...     )
            >>> spring
            Spring.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            source=source,
            spring=spring,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def damping(self):
        r'''Gets `damping` input of Spring.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> spring = ugentools.Spring.ar(
            ...     damping=0,
            ...     source=source,
            ...     spring=1,
            ...     )
            >>> spring.damping
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('damping')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Spring.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> spring = ugentools.Spring.ar(
            ...     damping=0,
            ...     source=source,
            ...     spring=1,
            ...     )
            >>> spring.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def spring(self):
        r'''Gets `spring` input of Spring.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> spring = ugentools.Spring.ar(
            ...     damping=0,
            ...     source=source,
            ...     spring=1,
            ...     )
            >>> spring.spring
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('spring')
        return self._inputs[index]