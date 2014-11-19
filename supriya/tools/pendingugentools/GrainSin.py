# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class GrainSin(MultiOutUGen):
    r'''

    ::

        >>> grain_sin = ugentools.GrainSin.(
        ...     channel_count=1,
        ...     duration=1,
        ...     envbufnum=-1,
        ...     frequency=440,
        ...     max_grains=512,
        ...     pan=0,
        ...     trigger=0,
        ...     )
        >>> grain_sin

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'trigger',
        'duration',
        'frequency',
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
        frequency=440,
        max_grains=512,
        pan=0,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            frequency=frequency,
            max_grains=max_grains,
            pan=pan,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=1,
        duration=1,
        envbufnum=-1,
        frequency=440,
        max_grains=512,
        pan=0,
        trigger=0,
        ):
        r'''Constructs an audio-rate GrainSin.

        ::

            >>> grain_sin = ugentools.GrainSin.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     frequency=440,
            ...     max_grains=512,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_sin

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            frequency=frequency,
            max_grains=max_grains,
            pan=pan,
            trigger=trigger,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of GrainSin.

        ::

            >>> grain_sin = ugentools.GrainSin.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     frequency=440,
            ...     max_grains=512,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_sin.channel_count

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of GrainSin.

        ::

            >>> grain_sin = ugentools.GrainSin.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     frequency=440,
            ...     max_grains=512,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_sin.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def duration(self):
        r'''Gets `duration` input of GrainSin.

        ::

            >>> grain_sin = ugentools.GrainSin.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     frequency=440,
            ...     max_grains=512,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_sin.duration

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of GrainSin.

        ::

            >>> grain_sin = ugentools.GrainSin.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     frequency=440,
            ...     max_grains=512,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_sin.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def pan(self):
        r'''Gets `pan` input of GrainSin.

        ::

            >>> grain_sin = ugentools.GrainSin.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     frequency=440,
            ...     max_grains=512,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_sin.pan

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pan')
        return self._inputs[index]

    @property
    def envbufnum(self):
        r'''Gets `envbufnum` input of GrainSin.

        ::

            >>> grain_sin = ugentools.GrainSin.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     frequency=440,
            ...     max_grains=512,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_sin.envbufnum

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('envbufnum')
        return self._inputs[index]

    @property
    def max_grains(self):
        r'''Gets `max_grains` input of GrainSin.

        ::

            >>> grain_sin = ugentools.GrainSin.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     frequency=440,
            ...     max_grains=512,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_sin.max_grains

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('max_grains')
        return self._inputs[index]