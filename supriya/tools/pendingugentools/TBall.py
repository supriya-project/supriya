# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class TBall(UGen):
    r'''

    ::

        >>> tball = ugentools.TBall.ar(
        ...     damping=0,
        ...     friction=0.01,
        ...     g=10,
        ...     source=source,
        ...     )
        >>> tball
        TBall.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'g',
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
        g=10,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            friction=friction,
            g=g,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damping=0,
        friction=0.01,
        g=10,
        source=None,
        ):
        r'''Constructs an audio-rate TBall.

        ::

            >>> tball = ugentools.TBall.ar(
            ...     damping=0,
            ...     friction=0.01,
            ...     g=10,
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
            g=g,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        damping=0,
        friction=0.01,
        g=10,
        source=None,
        ):
        r'''Constructs a control-rate TBall.

        ::

            >>> tball = ugentools.TBall.kr(
            ...     damping=0,
            ...     friction=0.01,
            ...     g=10,
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
            g=g,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def damping(self):
        r'''Gets `damping` input of TBall.

        ::

            >>> tball = ugentools.TBall.ar(
            ...     damping=0,
            ...     friction=0.01,
            ...     g=10,
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

            >>> tball = ugentools.TBall.ar(
            ...     damping=0,
            ...     friction=0.01,
            ...     g=10,
            ...     source=source,
            ...     )
            >>> tball.friction
            0.01

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('friction')
        return self._inputs[index]

    @property
    def g(self):
        r'''Gets `g` input of TBall.

        ::

            >>> tball = ugentools.TBall.ar(
            ...     damping=0,
            ...     friction=0.01,
            ...     g=10,
            ...     source=source,
            ...     )
            >>> tball.g
            10.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('g')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of TBall.

        ::

            >>> tball = ugentools.TBall.ar(
            ...     damping=0,
            ...     friction=0.01,
            ...     g=10,
            ...     source=source,
            ...     )
            >>> tball.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]