# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class DecodeB2(MultiOutUGen):
    r'''

    ::

        >>> decode_b_2 = ugentools.DecodeB2.(
        ...     channel_count=None,
        ...     orientation=0.5,
        ...     w=None,
        ...     x=None,
        ...     y=None,
        ...     )
        >>> decode_b_2

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'w',
        'x',
        'y',
        'orientation',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=None,
        orientation=0.5,
        w=None,
        x=None,
        y=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            orientation=orientation,
            w=w,
            x=x,
            y=y,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=None,
        orientation=0.5,
        w=None,
        x=None,
        y=None,
        ):
        r'''Constructs an audio-rate DecodeB2.

        ::

            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=None,
            ...     orientation=0.5,
            ...     w=None,
            ...     x=None,
            ...     y=None,
            ...     )
            >>> decode_b_2

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            orientation=orientation,
            w=w,
            x=x,
            y=y,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        channel_count=None,
        orientation=0.5,
        w=None,
        x=None,
        y=None,
        ):
        r'''Constructs a control-rate DecodeB2.

        ::

            >>> decode_b_2 = ugentools.DecodeB2.kr(
            ...     channel_count=None,
            ...     orientation=0.5,
            ...     w=None,
            ...     x=None,
            ...     y=None,
            ...     )
            >>> decode_b_2

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            orientation=orientation,
            w=w,
            x=x,
            y=y,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of DecodeB2.

        ::

            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=None,
            ...     orientation=0.5,
            ...     w=None,
            ...     x=None,
            ...     y=None,
            ...     )
            >>> decode_b_2.channel_count

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def orientation(self):
        r'''Gets `orientation` input of DecodeB2.

        ::

            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=None,
            ...     orientation=0.5,
            ...     w=None,
            ...     x=None,
            ...     y=None,
            ...     )
            >>> decode_b_2.orientation

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('orientation')
        return self._inputs[index]

    @property
    def w(self):
        r'''Gets `w` input of DecodeB2.

        ::

            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=None,
            ...     orientation=0.5,
            ...     w=None,
            ...     x=None,
            ...     y=None,
            ...     )
            >>> decode_b_2.w

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('w')
        return self._inputs[index]

    @property
    def x(self):
        r'''Gets `x` input of DecodeB2.

        ::

            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=None,
            ...     orientation=0.5,
            ...     w=None,
            ...     x=None,
            ...     y=None,
            ...     )
            >>> decode_b_2.x

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('x')
        return self._inputs[index]

    @property
    def y(self):
        r'''Gets `y` input of DecodeB2.

        ::

            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=None,
            ...     orientation=0.5,
            ...     w=None,
            ...     x=None,
            ...     y=None,
            ...     )
            >>> decode_b_2.y

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('y')
        return self._inputs[index]