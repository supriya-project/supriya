# -*- encoding: utf-8 -*-
import collections
from supriya.tools.ugentools.UGen import UGen


class XOut(UGen):
    r'''A cross-fading bus output unit generator.

    ::

        >>> source = ugentools.WhiteNoise.ar()
        >>> xout = ugentools.XOut.ar(
        ...     bus=0,
        ...     crossfade=0.5,
        ...     source=source,
        ...     )
        >>> xout
        XOut.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        'crossfade',
        'source',
        )

    _unexpanded_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        crossfade=0,
        source=None,
        ):
        if not isinstance(source, collections.Sequence):
            source = (source,)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            crossfade=crossfade,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=0,
        crossfade=0,
        source=None,
        ):
        r'''Constructs an audio-rate XOut.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> xout = ugentools.XOut.ar(
            ...     bus=0,
            ...     crossfade=0.5,
            ...     source=source,
            ...     )
            >>> xout
            XOut.ar()

        Returns ugen graph.
        '''
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        prototype = (
            servertools.Bus,
            servertools.BusGroup,
            servertools.BusProxy,
            )
        if isinstance(bus, prototype):
            bus = int(bus)
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            crossfade=crossfade,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bus=0,
        crossfade=0,
        source=None,
        ):
        r'''Constructs a control-rate XOut.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> xout = ugentools.XOut.kr(
            ...     bus=0,
            ...     crossfade=0.5,
            ...     source=source,
            ...     )
            >>> xout
            XOut.kr()

        Returns ugen graph.
        '''
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        prototype = (
            servertools.Bus,
            servertools.BusGroup,
            servertools.BusProxy,
            )
        if isinstance(bus, prototype):
            bus = int(bus)
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            crossfade=crossfade,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        r'''Gets `bus` input of XOut.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> xout = ugentools.XOut.ar(
            ...     bus=0,
            ...     crossfade=0.5,
            ...     source=source,
            ...     )
            >>> xout.bus
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def crossfade(self):
        r'''Gets `crossfade` input of XOut.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> xout = ugentools.XOut.ar(
            ...     bus=0,
            ...     crossfade=0.5,
            ...     source=source,
            ...     )
            >>> xout.crossfade
            0.5

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('crossfade')
        return self._inputs[index]

    @property
    def is_output_ugen(self):
        return True

    @property
    def source(self):
        r'''Gets `source` input of XOut.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> xout = ugentools.XOut.ar(
            ...     bus=0,
            ...     crossfade=0.5,
            ...     source=source,
            ...     )
            >>> xout.source
            (OutputProxy(
                source=WhiteNoise(
                    calculation_rate=CalculationRate.AUDIO
                    ),
                output_index=0
                ),)

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return tuple(self._inputs[index:])
