# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Warp1(MultiOutUGen):
    """

    ::

        >>> warp_1 = ugentools.Warp1.ar(
        ...     buffer_id=0,
        ...     channel_count=1,
        ...     envbufnum=-1,
        ...     frequency_scaling=1,
        ...     interpolate=1,
        ...     overlaps=8,
        ...     pointer=0,
        ...     window_rand_ratio=0,
        ...     window_size=0.2,
        ...     )
        >>> warp_1
        Warp1.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'buffer_id',
        'pointer',
        'frequency_scaling',
        'window_size',
        'envbufnum',
        'overlaps',
        'window_rand_ratio',
        'interpolate',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=0,
        channel_count=1,
        envbufnum=-1,
        frequency_scaling=1,
        interpolate=1,
        overlaps=8,
        pointer=0,
        window_rand_ratio=0,
        window_size=0.2,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            envbufnum=envbufnum,
            frequency_scaling=frequency_scaling,
            interpolate=interpolate,
            overlaps=overlaps,
            pointer=pointer,
            window_rand_ratio=window_rand_ratio,
            window_size=window_size,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=0,
        channel_count=1,
        envbufnum=-1,
        frequency_scaling=1,
        interpolate=1,
        overlaps=8,
        pointer=0,
        window_rand_ratio=0,
        window_size=0.2,
        ):
        """
        Constructs an audio-rate Warp1.

        ::

            >>> warp_1 = ugentools.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envbufnum=-1,
            ...     frequency_scaling=1,
            ...     interpolate=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1
            Warp1.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            envbufnum=envbufnum,
            frequency_scaling=frequency_scaling,
            interpolate=interpolate,
            overlaps=overlaps,
            pointer=pointer,
            window_rand_ratio=window_rand_ratio,
            window_size=window_size,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of Warp1.

        ::

            >>> warp_1 = ugentools.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envbufnum=-1,
            ...     frequency_scaling=1,
            ...     interpolate=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.buffer_id
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def channel_count(self):
        """
        Gets `channel_count` input of Warp1.

        ::

            >>> warp_1 = ugentools.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envbufnum=-1,
            ...     frequency_scaling=1,
            ...     interpolate=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.channel_count
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def envbufnum(self):
        """
        Gets `envbufnum` input of Warp1.

        ::

            >>> warp_1 = ugentools.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envbufnum=-1,
            ...     frequency_scaling=1,
            ...     interpolate=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.envbufnum
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('envbufnum')
        return self._inputs[index]

    @property
    def frequency_scaling(self):
        """
        Gets `frequency_scaling` input of Warp1.

        ::

            >>> warp_1 = ugentools.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envbufnum=-1,
            ...     frequency_scaling=1,
            ...     interpolate=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.frequency_scaling
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency_scaling')
        return self._inputs[index]

    @property
    def interpolate(self):
        """
        Gets `interpolate` input of Warp1.

        ::

            >>> warp_1 = ugentools.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envbufnum=-1,
            ...     frequency_scaling=1,
            ...     interpolate=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.interpolate
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('interpolate')
        return self._inputs[index]

    @property
    def overlaps(self):
        """
        Gets `overlaps` input of Warp1.

        ::

            >>> warp_1 = ugentools.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envbufnum=-1,
            ...     frequency_scaling=1,
            ...     interpolate=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.overlaps
            8.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('overlaps')
        return self._inputs[index]

    @property
    def pointer(self):
        """
        Gets `pointer` input of Warp1.

        ::

            >>> warp_1 = ugentools.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envbufnum=-1,
            ...     frequency_scaling=1,
            ...     interpolate=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.pointer
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pointer')
        return self._inputs[index]

    @property
    def window_rand_ratio(self):
        """
        Gets `window_rand_ratio` input of Warp1.

        ::

            >>> warp_1 = ugentools.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envbufnum=-1,
            ...     frequency_scaling=1,
            ...     interpolate=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.window_rand_ratio
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('window_rand_ratio')
        return self._inputs[index]

    @property
    def window_size(self):
        """
        Gets `window_size` input of Warp1.

        ::

            >>> warp_1 = ugentools.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envbufnum=-1,
            ...     frequency_scaling=1,
            ...     interpolate=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.window_size
            0.2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('window_size')
        return self._inputs[index]
