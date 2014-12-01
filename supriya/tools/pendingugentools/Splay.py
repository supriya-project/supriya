# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Splay(UGen):
    r'''

    ::

        >>> splay = ugentools.Splay.ar(
        ...     center=0,
        ...     in_array=in_array,
        ...     level=1,
        ...     level_comp=True,
        ...     spread=1,
        ...     )
        >>> splay
        Splay.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'in_array',
        'spread',
        'level',
        'center',
        'level_comp',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        center=0,
        in_array=None,
        level=1,
        level_comp=True,
        spread=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            center=center,
            in_array=in_array,
            level=level,
            level_comp=level_comp,
            spread=spread,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        center=0,
        in_array=None,
        level=1,
        level_comp=True,
        spread=1,
        ):
        r'''Constructs an audio-rate Splay.

        ::

            >>> splay = ugentools.Splay.ar(
            ...     center=0,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay
            Splay.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            center=center,
            in_array=in_array,
            level=level,
            level_comp=level_comp,
            spread=spread,
            )
        return ugen

    # def arFill(): ...

    @classmethod
    def kr(
        cls,
        center=0,
        in_array=None,
        level=1,
        level_comp=True,
        spread=1,
        ):
        r'''Constructs a control-rate Splay.

        ::

            >>> splay = ugentools.Splay.kr(
            ...     center=0,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay
            Splay.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            center=center,
            in_array=in_array,
            level=level,
            level_comp=level_comp,
            spread=spread,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def center(self):
        r'''Gets `center` input of Splay.

        ::

            >>> splay = ugentools.Splay.ar(
            ...     center=0,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay.center
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('center')
        return self._inputs[index]

    @property
    def in_array(self):
        r'''Gets `in_array` input of Splay.

        ::

            >>> splay = ugentools.Splay.ar(
            ...     center=0,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay.in_array

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('in_array')
        return self._inputs[index]

    @property
    def level(self):
        r'''Gets `level` input of Splay.

        ::

            >>> splay = ugentools.Splay.ar(
            ...     center=0,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay.level
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def level_comp(self):
        r'''Gets `level_comp` input of Splay.

        ::

            >>> splay = ugentools.Splay.ar(
            ...     center=0,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay.level_comp
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('level_comp')
        return self._inputs[index]

    @property
    def spread(self):
        r'''Gets `spread` input of Splay.

        ::

            >>> splay = ugentools.Splay.ar(
            ...     center=0,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay.spread
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('spread')
        return self._inputs[index]