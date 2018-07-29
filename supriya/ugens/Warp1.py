from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class Warp1(MultiOutUGen):
    """

    ::

        >>> warp_1 = supriya.ugens.Warp1.ar(
        ...     buffer_id=0,
        ...     channel_count=1,
        ...     envelope_buffer_id=-1,
        ...     frequency_scaling=1,
        ...     interpolation=1,
        ...     overlaps=8,
        ...     pointer=0,
        ...     window_rand_ratio=0,
        ...     window_size=0.2,
        ...     )
        >>> warp_1
        Warp1.ar()[0]

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'pointer',
        'frequency_scaling',
        'window_size',
        'envelope_buffer_id',
        'overlaps',
        'window_rand_ratio',
        'interpolation',
        )

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=0,
        channel_count=1,
        envelope_buffer_id=-1,
        frequency_scaling=1,
        interpolation=1,
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
            envelope_buffer_id=envelope_buffer_id,
            frequency_scaling=frequency_scaling,
            interpolation=interpolation,
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
        envelope_buffer_id=-1,
        frequency_scaling=1,
        interpolation=1,
        overlaps=8,
        pointer=0,
        window_rand_ratio=0,
        window_size=0.2,
        ):
        """
        Constructs an audio-rate Warp1.

        ::

            >>> warp_1 = supriya.ugens.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envelope_buffer_id=-1,
            ...     frequency_scaling=1,
            ...     interpolation=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1
            Warp1.ar()[0]

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            envelope_buffer_id=envelope_buffer_id,
            frequency_scaling=frequency_scaling,
            interpolation=interpolation,
            overlaps=overlaps,
            pointer=pointer,
            window_rand_ratio=window_rand_ratio,
            window_size=window_size,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of Warp1.

        ::

            >>> warp_1 = supriya.ugens.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envelope_buffer_id=-1,
            ...     frequency_scaling=1,
            ...     interpolation=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.source.buffer_id
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def envelope_buffer_id(self):
        """
        Gets `envelope_buffer_id` input of Warp1.

        ::

            >>> warp_1 = supriya.ugens.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envelope_buffer_id=-1,
            ...     frequency_scaling=1,
            ...     interpolation=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.source.envelope_buffer_id
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('envelope_buffer_id')
        return self._inputs[index]

    @property
    def frequency_scaling(self):
        """
        Gets `frequency_scaling` input of Warp1.

        ::

            >>> warp_1 = supriya.ugens.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envelope_buffer_id=-1,
            ...     frequency_scaling=1,
            ...     interpolation=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.source.frequency_scaling
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency_scaling')
        return self._inputs[index]

    @property
    def interpolation(self):
        """
        Gets `interpolation` input of Warp1.

        ::

            >>> warp_1 = supriya.ugens.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envelope_buffer_id=-1,
            ...     frequency_scaling=1,
            ...     interpolation=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.source.interpolation
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('interpolation')
        return self._inputs[index]

    @property
    def overlaps(self):
        """
        Gets `overlaps` input of Warp1.

        ::

            >>> warp_1 = supriya.ugens.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envelope_buffer_id=-1,
            ...     frequency_scaling=1,
            ...     interpolation=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.source.overlaps
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

            >>> warp_1 = supriya.ugens.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envelope_buffer_id=-1,
            ...     frequency_scaling=1,
            ...     interpolation=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.source.pointer
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

            >>> warp_1 = supriya.ugens.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envelope_buffer_id=-1,
            ...     frequency_scaling=1,
            ...     interpolation=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.source.window_rand_ratio
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

            >>> warp_1 = supriya.ugens.Warp1.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     envelope_buffer_id=-1,
            ...     frequency_scaling=1,
            ...     interpolation=1,
            ...     overlaps=8,
            ...     pointer=0,
            ...     window_rand_ratio=0,
            ...     window_size=0.2,
            ...     )
            >>> warp_1.source.window_size
            0.2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('window_size')
        return self._inputs[index]
