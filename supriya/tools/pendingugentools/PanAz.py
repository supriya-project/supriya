# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PanAz(MultiOutUGen):
    r'''

    ::

        >>> pan_az = ugentools.PanAz.(
        ...     channel_count=None,
        ...     level=1,
        ...     orientation=0.5,
        ...     pos=0,
        ...     source=None,
        ...     width=2,
        ...     )
        >>> pan_az

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'source',
        'pos',
        'level',
        'width',
        'orientation',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=None,
        level=1,
        orientation=0.5,
        pos=0,
        source=None,
        width=2,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            level=level,
            orientation=orientation,
            pos=pos,
            source=source,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=None,
        level=1,
        orientation=0.5,
        pos=0,
        source=None,
        width=2,
        ):
        r'''Constructs an audio-rate PanAz.

        ::

            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=None,
            ...     level=1,
            ...     orientation=0.5,
            ...     pos=0,
            ...     source=None,
            ...     width=2,
            ...     )
            >>> pan_az

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            level=level,
            orientation=orientation,
            pos=pos,
            source=source,
            width=width,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        channel_count=None,
        level=1,
        orientation=0.5,
        pos=0,
        source=None,
        width=2,
        ):
        r'''Constructs a control-rate PanAz.

        ::

            >>> pan_az = ugentools.PanAz.kr(
            ...     channel_count=None,
            ...     level=1,
            ...     orientation=0.5,
            ...     pos=0,
            ...     source=None,
            ...     width=2,
            ...     )
            >>> pan_az

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            level=level,
            orientation=orientation,
            pos=pos,
            source=source,
            width=width,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of PanAz.

        ::

            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=None,
            ...     level=1,
            ...     orientation=0.5,
            ...     pos=0,
            ...     source=None,
            ...     width=2,
            ...     )
            >>> pan_az.channel_count

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of PanAz.

        ::

            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=None,
            ...     level=1,
            ...     orientation=0.5,
            ...     pos=0,
            ...     source=None,
            ...     width=2,
            ...     )
            >>> pan_az.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def pos(self):
        r'''Gets `pos` input of PanAz.

        ::

            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=None,
            ...     level=1,
            ...     orientation=0.5,
            ...     pos=0,
            ...     source=None,
            ...     width=2,
            ...     )
            >>> pan_az.pos

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pos')
        return self._inputs[index]

    @property
    def level(self):
        r'''Gets `level` input of PanAz.

        ::

            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=None,
            ...     level=1,
            ...     orientation=0.5,
            ...     pos=0,
            ...     source=None,
            ...     width=2,
            ...     )
            >>> pan_az.level

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def width(self):
        r'''Gets `width` input of PanAz.

        ::

            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=None,
            ...     level=1,
            ...     orientation=0.5,
            ...     pos=0,
            ...     source=None,
            ...     width=2,
            ...     )
            >>> pan_az.width

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('width')
        return self._inputs[index]

    @property
    def orientation(self):
        r'''Gets `orientation` input of PanAz.

        ::

            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=None,
            ...     level=1,
            ...     orientation=0.5,
            ...     pos=0,
            ...     source=None,
            ...     width=2,
            ...     )
            >>> pan_az.orientation

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('orientation')
        return self._inputs[index]