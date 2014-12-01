# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class BiPanB2(MultiOutUGen):
    r'''

    ::

        >>> bi_pan_b_2 = ugentools.BiPanB2.ar(
        ...     azimuth=azimuth,
        ...     gain=1,
        ...     in_a=in_a,
        ...     in_b=in_b,
        ...     )
        >>> bi_pan_b_2
        BiPanB2.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'in_a',
        'in_b',
        'azimuth',
        'gain',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        azimuth=None,
        gain=1,
        in_a=None,
        in_b=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            in_a=in_a,
            in_b=in_b,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        azimuth=None,
        gain=1,
        in_a=None,
        in_b=None,
        ):
        r'''Constructs an audio-rate BiPanB2.

        ::

            >>> bi_pan_b_2 = ugentools.BiPanB2.ar(
            ...     azimuth=azimuth,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2
            BiPanB2.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            in_a=in_a,
            in_b=in_b,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        azimuth=None,
        gain=1,
        in_a=None,
        in_b=None,
        ):
        r'''Constructs a control-rate BiPanB2.

        ::

            >>> bi_pan_b_2 = ugentools.BiPanB2.kr(
            ...     azimuth=azimuth,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2
            BiPanB2.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            in_a=in_a,
            in_b=in_b,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def azimuth(self):
        r'''Gets `azimuth` input of BiPanB2.

        ::

            >>> bi_pan_b_2 = ugentools.BiPanB2.ar(
            ...     azimuth=azimuth,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2.azimuth

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('azimuth')
        return self._inputs[index]

    @property
    def gain(self):
        r'''Gets `gain` input of BiPanB2.

        ::

            >>> bi_pan_b_2 = ugentools.BiPanB2.ar(
            ...     azimuth=azimuth,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2.gain
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def in_a(self):
        r'''Gets `in_a` input of BiPanB2.

        ::

            >>> bi_pan_b_2 = ugentools.BiPanB2.ar(
            ...     azimuth=azimuth,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2.in_a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('in_a')
        return self._inputs[index]

    @property
    def in_b(self):
        r'''Gets `in_b` input of BiPanB2.

        ::

            >>> bi_pan_b_2 = ugentools.BiPanB2.ar(
            ...     azimuth=azimuth,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2.in_b

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('in_b')
        return self._inputs[index]