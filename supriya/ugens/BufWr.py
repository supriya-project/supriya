from supriya.ugens.UGen import UGen


class BufWr(UGen):
    """
    A buffer-writing oscillator.

    ::

        >>> buffer_id = 23
        >>> phase = supriya.ugens.Phasor.ar(
        ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
        ...     start=0,
        ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
        ...     )
        >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
        >>> buf_wr = supriya.ugens.BufWr.ar(
        ...     buffer_id=buffer_id,
        ...     loop=1,
        ...     phase=phase,
        ...     source=source,
        ...     )
        >>> buf_wr
        BufWr.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'phase',
        'loop',
        'source',
        )

    _unexpanded_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        source=None,
        loop=1,
        phase=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            loop=loop,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        source=None,
        loop=1,
        phase=0,
        ):
        """
        Constructs an audio-rate BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = supriya.ugens.Phasor.ar(
            ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
            ...     )
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = supriya.ugens.BufWr.ar(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr
            BufWr.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            loop=loop,
            phase=phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        source=None,
        loop=1,
        phase=0,
        ):
        """
        Constructs a control-rate BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = supriya.ugens.Phasor.ar(
            ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
            ...     )
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = supriya.ugens.BufWr.kr(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr
            BufWr.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            loop=loop,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = supriya.ugens.Phasor.ar(
            ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
            ...     )
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = supriya.ugens.BufWr.ar(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr.buffer_id
            23.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def has_done_flag(self):
        """
        Is true if UGen has a done flag.

        Returns boolean.
        """
        return True

    @property
    def loop(self):
        """
        Gets `loop` input of BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = supriya.ugens.Phasor.ar(
            ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
            ...     )
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = supriya.ugens.BufWr.ar(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr.loop
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def phase(self):
        """
        Gets `phase` input of BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = supriya.ugens.Phasor.ar(
            ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
            ...     )
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = supriya.ugens.BufWr.ar(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr.phase
            Phasor.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = supriya.ugens.Phasor.ar(
            ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
            ...     )
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = supriya.ugens.BufWr.ar(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
