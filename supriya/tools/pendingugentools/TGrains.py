# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class TGrains(MultiOutUGen):
    r'''

    ::

        >>> tgrains = ugentools.TGrains.ar(
        ...     amp=0.1,
        ...     buffer_id=0,
        ...     center_pos=0,
        ...     channel_count=channel_count,
        ...     duration=0.1,
        ...     interpolate=4,
        ...     pan=0,
        ...     rate=1,
        ...     trigger=0,
        ...     )
        >>> tgrains
        TGrains.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'trigger',
        'buffer_id',
        'rate',
        'center_pos',
        'duration',
        'pan',
        'amp',
        'interpolate',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        amp=0.1,
        buffer_id=0,
        center_pos=0,
        channel_count=None,
        duration=0.1,
        interpolate=4,
        pan=0,
        rate=1,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            amp=amp,
            buffer_id=buffer_id,
            center_pos=center_pos,
            channel_count=channel_count,
            duration=duration,
            interpolate=interpolate,
            pan=pan,
            rate=rate,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        amp=0.1,
        buffer_id=0,
        center_pos=0,
        channel_count=channel_count,
        duration=0.1,
        interpolate=4,
        pan=0,
        rate=1,
        trigger=0,
        ):
        r'''Constructs an audio-rate TGrains.

        ::

            >>> tgrains = ugentools.TGrains.ar(
            ...     amp=0.1,
            ...     buffer_id=0,
            ...     center_pos=0,
            ...     channel_count=channel_count,
            ...     duration=0.1,
            ...     interpolate=4,
            ...     pan=0,
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> tgrains
            TGrains.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            amp=amp,
            buffer_id=buffer_id,
            center_pos=center_pos,
            channel_count=channel_count,
            duration=duration,
            interpolate=interpolate,
            pan=pan,
            rate=rate,
            trigger=trigger,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def amp(self):
        r'''Gets `amp` input of TGrains.

        ::

            >>> tgrains = ugentools.TGrains.ar(
            ...     amp=0.1,
            ...     buffer_id=0,
            ...     center_pos=0,
            ...     channel_count=channel_count,
            ...     duration=0.1,
            ...     interpolate=4,
            ...     pan=0,
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> tgrains.amp
            0.1

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('amp')
        return self._inputs[index]

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of TGrains.

        ::

            >>> tgrains = ugentools.TGrains.ar(
            ...     amp=0.1,
            ...     buffer_id=0,
            ...     center_pos=0,
            ...     channel_count=channel_count,
            ...     duration=0.1,
            ...     interpolate=4,
            ...     pan=0,
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> tgrains.buffer_id
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def center_pos(self):
        r'''Gets `center_pos` input of TGrains.

        ::

            >>> tgrains = ugentools.TGrains.ar(
            ...     amp=0.1,
            ...     buffer_id=0,
            ...     center_pos=0,
            ...     channel_count=channel_count,
            ...     duration=0.1,
            ...     interpolate=4,
            ...     pan=0,
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> tgrains.center_pos
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('center_pos')
        return self._inputs[index]

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of TGrains.

        ::

            >>> tgrains = ugentools.TGrains.ar(
            ...     amp=0.1,
            ...     buffer_id=0,
            ...     center_pos=0,
            ...     channel_count=channel_count,
            ...     duration=0.1,
            ...     interpolate=4,
            ...     pan=0,
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> tgrains.channel_count

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def duration(self):
        r'''Gets `duration` input of TGrains.

        ::

            >>> tgrains = ugentools.TGrains.ar(
            ...     amp=0.1,
            ...     buffer_id=0,
            ...     center_pos=0,
            ...     channel_count=channel_count,
            ...     duration=0.1,
            ...     interpolate=4,
            ...     pan=0,
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> tgrains.duration
            0.1

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def interpolate(self):
        r'''Gets `interpolate` input of TGrains.

        ::

            >>> tgrains = ugentools.TGrains.ar(
            ...     amp=0.1,
            ...     buffer_id=0,
            ...     center_pos=0,
            ...     channel_count=channel_count,
            ...     duration=0.1,
            ...     interpolate=4,
            ...     pan=0,
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> tgrains.interpolate
            4.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('interpolate')
        return self._inputs[index]

    @property
    def pan(self):
        r'''Gets `pan` input of TGrains.

        ::

            >>> tgrains = ugentools.TGrains.ar(
            ...     amp=0.1,
            ...     buffer_id=0,
            ...     center_pos=0,
            ...     channel_count=channel_count,
            ...     duration=0.1,
            ...     interpolate=4,
            ...     pan=0,
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> tgrains.pan
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pan')
        return self._inputs[index]

    @property
    def rate(self):
        r'''Gets `rate` input of TGrains.

        ::

            >>> tgrains = ugentools.TGrains.ar(
            ...     amp=0.1,
            ...     buffer_id=0,
            ...     center_pos=0,
            ...     channel_count=channel_count,
            ...     duration=0.1,
            ...     interpolate=4,
            ...     pan=0,
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> tgrains.rate
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of TGrains.

        ::

            >>> tgrains = ugentools.TGrains.ar(
            ...     amp=0.1,
            ...     buffer_id=0,
            ...     center_pos=0,
            ...     channel_count=channel_count,
            ...     duration=0.1,
            ...     interpolate=4,
            ...     pan=0,
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> tgrains.trigger
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]