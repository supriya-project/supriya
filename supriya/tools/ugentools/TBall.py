# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class TBall(UGen):
    r'''A bouncing object physical model.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> tball = ugentools.TBall.ar(
        ...     damping=0,
        ...     friction=0.01,
        ...     gravity=10,
        ...     source=source,
        ...     )
        >>> tball
        TBall.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Physical Modelling UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'gravity',
        'damping',
        'friction',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        damping=0,
        friction=0.01,
        gravity=10,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            friction=friction,
            gravity=gravity,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damping=0,
        friction=0.01,
        gravity=10,
        source=None,
        ):
        r'''Constructs an audio-rate TBall.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> tball = ugentools.TBall.ar(
            ...     damping=0,
            ...     friction=0.01,
            ...     gravity=10,
            ...     source=source,
            ...     )
            >>> tball
            TBall.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            friction=friction,
            gravity=gravity,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        damping=0,
        friction=0.01,
        gravity=10,
        source=None,
        ):
        r'''Constructs a control-rate TBall.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> tball = ugentools.TBall.kr(
            ...     damping=0,
            ...     friction=0.01,
            ...     gravity=10,
            ...     source=source,
            ...     )
            >>> tball
            TBall.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            friction=friction,
            gravity=gravity,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def damping(self):
        r'''Gets `damping` input of TBall.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> tball = ugentools.TBall.ar(
            ...     damping=0,
            ...     friction=0.01,
            ...     gravity=10,
            ...     source=source,
            ...     )
            >>> tball.damping
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('damping')
        return self._inputs[index]

    @property
    def friction(self):
        r'''Gets `friction` input of TBall.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> tball = ugentools.TBall.ar(
            ...     damping=0,
            ...     friction=0.01,
            ...     gravity=10,
            ...     source=source,
            ...     )
            >>> tball.friction
            0.01

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('friction')
        return self._inputs[index]

    @property
    def gravity(self):
        r'''Gets `gravity` input of TBall.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> tball = ugentools.TBall.ar(
            ...     damping=0,
            ...     friction=0.01,
            ...     gravity=10,
            ...     source=source,
            ...     )
            >>> tball.gravity
            10.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('gravity')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of TBall.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> tball = ugentools.TBall.ar(
            ...     damping=0,
            ...     friction=0.01,
            ...     gravity=10,
            ...     source=source,
            ...     )
            >>> tball.source
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