# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class GrainIn(MultiOutUGen):
    r'''

    ::

        >>> grain_in = ugentools.GrainIn.ar(
        ...     channel_count=1,
        ...     duration=1,
        ...     envbufnum=-1,
        ...     max_grains=512,
        ...     pan=0,
        ...     source=source,
        ...     trigger=0,
        ...     )
        >>> grain_in
        GrainIn.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'trigger',
        'duration',
        'source',
        'pan',
        'envbufnum',
        'max_grains',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=1,
        duration=1,
        envbufnum=-1,
        max_grains=512,
        pan=0,
        source=None,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            max_grains=max_grains,
            pan=pan,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=1,
        duration=1,
        envbufnum=-1,
        max_grains=512,
        pan=0,
        source=source,
        trigger=0,
        ):
        r'''Constructs an audio-rate GrainIn.

        ::

            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     max_grains=512,
            ...     pan=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in
            GrainIn.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            max_grains=max_grains,
            pan=pan,
            source=source,
            trigger=trigger,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of GrainIn.

        ::

            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     max_grains=512,
            ...     pan=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.channel_count
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def duration(self):
        r'''Gets `duration` input of GrainIn.

        ::

            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     max_grains=512,
            ...     pan=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.duration
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def envbufnum(self):
        r'''Gets `envbufnum` input of GrainIn.

        ::

            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     max_grains=512,
            ...     pan=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.envbufnum
            -1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('envbufnum')
        return self._inputs[index]

    @property
    def max_grains(self):
        r'''Gets `max_grains` input of GrainIn.

        ::

            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     max_grains=512,
            ...     pan=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.max_grains
            512.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('max_grains')
        return self._inputs[index]

    @property
    def pan(self):
        r'''Gets `pan` input of GrainIn.

        ::

            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     max_grains=512,
            ...     pan=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.pan
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pan')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of GrainIn.

        ::

            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     max_grains=512,
            ...     pan=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of GrainIn.

        ::

            >>> grain_in = ugentools.GrainIn.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     max_grains=512,
            ...     pan=0,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> grain_in.trigger
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]