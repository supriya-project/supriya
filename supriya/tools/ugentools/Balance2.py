# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Balance2(MultiOutUGen):
    r'''A stereo signal balancer.

    ::

        >>> left = ugentools.WhiteNoise.ar()
        >>> right = ugentools.SinOsc.ar()
        >>> balance_2 = ugentools.Balance2.ar(
        ...     left=left,
        ...     level=1,
        ...     position=0,
        ...     right=right,
        ...     )
        >>> balance_2
        Balance2.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'left',
        'right',
        'position',
        'level',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        left=None,
        level=1,
        position=0,
        right=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=2,
            left=left,
            level=level,
            position=position,
            right=right,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        left=None,
        level=1,
        position=0,
        right=None,
        ):
        r'''Constructs an audio-rate Balance2.

        ::

            >>> left = ugentools.WhiteNoise.ar()
            >>> right = ugentools.SinOsc.ar()
            >>> balance_2 = ugentools.Balance2.ar(
            ...     left=left,
            ...     level=1,
            ...     position=0,
            ...     right=right,
            ...     )
            >>> balance_2
            Balance2.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            left=left,
            level=level,
            position=position,
            right=right,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        left=None,
        level=1,
        position=0,
        right=None,
        ):
        r'''Constructs a control-rate Balance2.

        ::

            >>> left = ugentools.WhiteNoise.kr()
            >>> right = ugentools.SinOsc.kr()
            >>> balance_2 = ugentools.Balance2.kr(
            ...     left=left,
            ...     level=1,
            ...     position=0,
            ...     right=right,
            ...     )
            >>> balance_2
            Balance2.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            left=left,
            level=level,
            position=position,
            right=right,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def left(self):
        r'''Gets `left` input of Balance2.

        ::

            >>> left = ugentools.WhiteNoise.ar()
            >>> right = ugentools.SinOsc.ar()
            >>> balance_2 = ugentools.Balance2.ar(
            ...     left=left,
            ...     level=1,
            ...     position=0,
            ...     right=right,
            ...     )
            >>> balance_2.left
            WhiteNoise.ar()

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('left')
        return self._inputs[index]

    @property
    def level(self):
        r'''Gets `level` input of Balance2.

        ::

            >>> left = ugentools.WhiteNoise.ar()
            >>> right = ugentools.SinOsc.ar()
            >>> balance_2 = ugentools.Balance2.ar(
            ...     left=left,
            ...     level=1,
            ...     position=0,
            ...     right=right,
            ...     )
            >>> balance_2.level
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def position(self):
        r'''Gets `position` input of Balance2.

        ::

            >>> left = ugentools.WhiteNoise.ar()
            >>> right = ugentools.SinOsc.ar()
            >>> balance_2 = ugentools.Balance2.ar(
            ...     left=left,
            ...     level=1,
            ...     position=0.5,
            ...     right=right,
            ...     )
            >>> balance_2.position
            0.5

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('position')
        return self._inputs[index]

    @property
    def right(self):
        r'''Gets `right` input of Balance2.

        ::

            >>> left = ugentools.WhiteNoise.ar()
            >>> right = ugentools.SinOsc.ar()
            >>> balance_2 = ugentools.Balance2.ar(
            ...     left=left,
            ...     level=1,
            ...     position=0,
            ...     right=right,
            ...     )
            >>> balance_2.right
            SinOsc.ar()

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('right')
        return self._inputs[index]