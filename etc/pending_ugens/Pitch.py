from supriya.ugens.MultiOutUGen import MultiOutUGen


class Pitch(MultiOutUGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pitch = supriya.ugens.Pitch.ar(
        ...     amp_threshold=0.01,
        ...     clar=0,
        ...     down_sample=1,
        ...     exec_frequency=100,
        ...     init_frequency=440,
        ...     max_bins_per_octave=16,
        ...     max_frequency=4000,
        ...     median=1,
        ...     min_frequency=60,
        ...     peak_threshold=0.5,
        ...     source=source,
        ...     )
        >>> pitch
        Pitch.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'init_frequency',
        'min_frequency',
        'max_frequency',
        'exec_frequency',
        'max_bins_per_octave',
        'median',
        'amp_threshold',
        'peak_threshold',
        'down_sample',
        'clar',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        amp_threshold=0.01,
        clar=0,
        down_sample=1,
        exec_frequency=100,
        init_frequency=440,
        max_bins_per_octave=16,
        max_frequency=4000,
        median=1,
        min_frequency=60,
        peak_threshold=0.5,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            amp_threshold=amp_threshold,
            clar=clar,
            down_sample=down_sample,
            exec_frequency=exec_frequency,
            init_frequency=init_frequency,
            max_bins_per_octave=max_bins_per_octave,
            max_frequency=max_frequency,
            median=median,
            min_frequency=min_frequency,
            peak_threshold=peak_threshold,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        amp_threshold=0.01,
        clar=0,
        down_sample=1,
        exec_frequency=100,
        init_frequency=440,
        max_bins_per_octave=16,
        max_frequency=4000,
        median=1,
        min_frequency=60,
        peak_threshold=0.5,
        source=None,
        ):
        """
        Constructs a control-rate Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.kr(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch
            Pitch.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            amp_threshold=amp_threshold,
            clar=clar,
            down_sample=down_sample,
            exec_frequency=exec_frequency,
            init_frequency=init_frequency,
            max_bins_per_octave=max_bins_per_octave,
            max_frequency=max_frequency,
            median=median,
            min_frequency=min_frequency,
            peak_threshold=peak_threshold,
            source=source,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def amp_threshold(self):
        """
        Gets `amp_threshold` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.amp_threshold
            0.01

        Returns ugen input.
        """
        index = self._ordered_input_names.index('amp_threshold')
        return self._inputs[index]

    @property
    def clar(self):
        """
        Gets `clar` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.clar
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('clar')
        return self._inputs[index]

    @property
    def down_sample(self):
        """
        Gets `down_sample` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.down_sample
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('down_sample')
        return self._inputs[index]

    @property
    def exec_frequency(self):
        """
        Gets `exec_frequency` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.exec_frequency
            100.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('exec_frequency')
        return self._inputs[index]

    @property
    def init_frequency(self):
        """
        Gets `init_frequency` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.init_frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('init_frequency')
        return self._inputs[index]

    @property
    def max_bins_per_octave(self):
        """
        Gets `max_bins_per_octave` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.max_bins_per_octave
            16.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('max_bins_per_octave')
        return self._inputs[index]

    @property
    def max_frequency(self):
        """
        Gets `max_frequency` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.max_frequency
            4000.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('max_frequency')
        return self._inputs[index]

    @property
    def median(self):
        """
        Gets `median` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.median
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('median')
        return self._inputs[index]

    @property
    def min_frequency(self):
        """
        Gets `min_frequency` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.min_frequency
            60.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('min_frequency')
        return self._inputs[index]

    @property
    def peak_threshold(self):
        """
        Gets `peak_threshold` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.peak_threshold
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('peak_threshold')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Pitch.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pitch = supriya.ugens.Pitch.ar(
            ...     amp_threshold=0.01,
            ...     clar=0,
            ...     down_sample=1,
            ...     exec_frequency=100,
            ...     init_frequency=440,
            ...     max_bins_per_octave=16,
            ...     max_frequency=4000,
            ...     median=1,
            ...     min_frequency=60,
            ...     peak_threshold=0.5,
            ...     source=source,
            ...     )
            >>> pitch.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
