# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class GrainBuf(MultiOutUGen):
    r"""

    ::

        >>> grain_buf = ugentools.GrainBuf.ar(
        ...     channel_count=1,
        ...     duration=1,
        ...     envbufnum=-1,
        ...     interpolate=2,
        ...     max_grains=512,
        ...     pan=0,
        ...     pos=0,
        ...     rate=1,
        ...     sndbuf=sndbuf,
        ...     trigger=0,
        ...     )
        >>> grain_buf
        GrainBuf.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'trigger',
        'duration',
        'sndbuf',
        'rate',
        'pos',
        'interpolate',
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
        interpolate=2,
        max_grains=512,
        pan=0,
        pos=0,
        rate=1,
        sndbuf=None,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            interpolate=interpolate,
            max_grains=max_grains,
            pan=pan,
            pos=pos,
            rate=rate,
            sndbuf=sndbuf,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=1,
        duration=1,
        envbufnum=-1,
        interpolate=2,
        max_grains=512,
        pan=0,
        pos=0,
        rate=1,
        sndbuf=None,
        trigger=0,
        ):
        r"""
        Constructs an audio-rate GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf
            GrainBuf.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            interpolate=interpolate,
            max_grains=max_grains,
            pan=pan,
            pos=pos,
            rate=rate,
            sndbuf=sndbuf,
            trigger=trigger,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        r"""
        Gets `channel_count` input of GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf.channel_count
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def duration(self):
        r"""
        Gets `duration` input of GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf.duration
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def envbufnum(self):
        r"""
        Gets `envbufnum` input of GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf.envbufnum
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('envbufnum')
        return self._inputs[index]

    @property
    def interpolate(self):
        r"""
        Gets `interpolate` input of GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf.interpolate
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('interpolate')
        return self._inputs[index]

    @property
    def max_grains(self):
        r"""
        Gets `max_grains` input of GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf.max_grains
            512.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('max_grains')
        return self._inputs[index]

    @property
    def pan(self):
        r"""
        Gets `pan` input of GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf.pan
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pan')
        return self._inputs[index]

    @property
    def pos(self):
        r"""
        Gets `pos` input of GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf.pos
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pos')
        return self._inputs[index]

    @property
    def rate(self):
        r"""
        Gets `rate` input of GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf.rate
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def sndbuf(self):
        r"""
        Gets `sndbuf` input of GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf.sndbuf

        Returns ugen input.
        """
        index = self._ordered_input_names.index('sndbuf')
        return self._inputs[index]

    @property
    def trigger(self):
        r"""
        Gets `trigger` input of GrainBuf.

        ::

            >>> grain_buf = ugentools.GrainBuf.ar(
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     interpolate=2,
            ...     max_grains=512,
            ...     pan=0,
            ...     pos=0,
            ...     rate=1,
            ...     sndbuf=sndbuf,
            ...     trigger=0,
            ...     )
            >>> grain_buf.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
