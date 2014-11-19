# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class LinXFade2(UGen):
    r'''

    ::

        >>> lin_xfade_2 = ugentools.LinXFade2.(
        ...     in_a=None,
        ...     in_b=0,
        ...     level=1,
        ...     pan=0,
        ...     )
        >>> lin_xfade_2

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'in_a',
        'in_b',
        'pan',
        'level',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        in_a=None,
        in_b=0,
        level=1,
        pan=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            in_a=in_a,
            in_b=in_b,
            level=level,
            pan=pan,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        in_a=None,
        in_b=0,
        level=1,
        pan=0,
        ):
        r'''Constructs an audio-rate LinXFade2.

        ::

            >>> lin_xfade_2 = ugentools.LinXFade2.ar(
            ...     in_a=None,
            ...     in_b=0,
            ...     level=1,
            ...     pan=0,
            ...     )
            >>> lin_xfade_2

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            in_a=in_a,
            in_b=in_b,
            level=level,
            pan=pan,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        in_a=None,
        in_b=0,
        level=1,
        pan=0,
        ):
        r'''Constructs a control-rate LinXFade2.

        ::

            >>> lin_xfade_2 = ugentools.LinXFade2.kr(
            ...     in_a=None,
            ...     in_b=0,
            ...     level=1,
            ...     pan=0,
            ...     )
            >>> lin_xfade_2

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            in_a=in_a,
            in_b=in_b,
            level=level,
            pan=pan,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def in_a(self):
        r'''Gets `in_a` input of LinXFade2.

        ::

            >>> lin_xfade_2 = ugentools.LinXFade2.ar(
            ...     in_a=None,
            ...     in_b=0,
            ...     level=1,
            ...     pan=0,
            ...     )
            >>> lin_xfade_2.in_a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('in_a')
        return self._inputs[index]

    @property
    def in_b(self):
        r'''Gets `in_b` input of LinXFade2.

        ::

            >>> lin_xfade_2 = ugentools.LinXFade2.ar(
            ...     in_a=None,
            ...     in_b=0,
            ...     level=1,
            ...     pan=0,
            ...     )
            >>> lin_xfade_2.in_b

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('in_b')
        return self._inputs[index]

    @property
    def level(self):
        r'''Gets `level` input of LinXFade2.

        ::

            >>> lin_xfade_2 = ugentools.LinXFade2.ar(
            ...     in_a=None,
            ...     in_b=0,
            ...     level=1,
            ...     pan=0,
            ...     )
            >>> lin_xfade_2.level

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def pan(self):
        r'''Gets `pan` input of LinXFade2.

        ::

            >>> lin_xfade_2 = ugentools.LinXFade2.ar(
            ...     in_a=None,
            ...     in_b=0,
            ...     level=1,
            ...     pan=0,
            ...     )
            >>> lin_xfade_2.pan

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pan')
        return self._inputs[index]