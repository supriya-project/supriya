# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.AbstractOut import AbstractOut


class XOut(AbstractOut):
    r'''

    ::

        >>> xout = ugentools.XOut.ar(
        ...     bus=bus,
        ...     crossfade=crossfade,
        ...     source=source,
        ...     )
        >>> xout
        XOut.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        'crossfade',
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=None,
        crossfade=None,
        source=None,
        ):
        AbstractOut.__init__(
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
        bus=None,
        crossfade=None,
        source=None,
        ):
        r'''Constructs an audio-rate XOut.

        ::

            >>> xout = ugentools.XOut.ar(
            ...     bus=bus,
            ...     crossfade=crossfade,
            ...     source=source,
            ...     )
            >>> xout
            XOut.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            crossfade=crossfade,
            source=source,
            )
        return ugen

    # def isOutputUGen(): ...

    @classmethod
    def kr(
        cls,
        bus=None,
        crossfade=None,
        source=None,
        ):
        r'''Constructs a control-rate XOut.

        ::

            >>> xout = ugentools.XOut.kr(
            ...     bus=bus,
            ...     crossfade=crossfade,
            ...     source=source,
            ...     )
            >>> xout
            XOut.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            crossfade=crossfade,
            source=source,
            )
        return ugen

    # def numFixedArgs(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        r'''Gets `bus` input of XOut.

        ::

            >>> xout = ugentools.XOut.ar(
            ...     bus=bus,
            ...     crossfade=crossfade,
            ...     source=source,
            ...     )
            >>> xout.bus

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def crossfade(self):
        r'''Gets `crossfade` input of XOut.

        ::

            >>> xout = ugentools.XOut.ar(
            ...     bus=bus,
            ...     crossfade=crossfade,
            ...     source=source,
            ...     )
            >>> xout.crossfade

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('crossfade')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of XOut.

        ::

            >>> xout = ugentools.XOut.ar(
            ...     bus=bus,
            ...     crossfade=crossfade,
            ...     source=source,
            ...     )
            >>> xout.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]