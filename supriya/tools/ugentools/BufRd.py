# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class BufRd(MultiOutUGen):
    """
    A buffer-reading oscillator.

    ::

        >>> buffer_id = 23
        >>> phase = ugentools.Phasor.ar(
        ...     rate=ugentools.BufRateScale.kr(buffer_id),
        ...     start=0,
        ...     stop=ugentools.BufFrames.kr(buffer_id),
        ...     )
        >>> buf_rd = ugentools.BufRd.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     interpolation=2,
        ...     loop=1,
        ...     phase=phase,
        ...     )
        >>> buf_rd
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'phase',
        'loop',
        'interpolation',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        channel_count=None,
        interpolation=2,
        loop=1,
        phase=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            interpolation=interpolation,
            loop=loop,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        channel_count=None,
        interpolation=2,
        loop=1,
        phase=0,
        ):
        """
        Constructs an audio-rate BufRd.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=phase,
            ...     )
            >>> buf_rd
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            interpolation=interpolation,
            loop=loop,
            phase=phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        channel_count=None,
        interpolation=2,
        loop=1,
        phase=0,
        ):
        """
        Constructs a control-rate BufRd.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> buf_rd = ugentools.BufRd.kr(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=phase,
            ...     )
            >>> buf_rd
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            interpolation=interpolation,
            loop=loop,
            phase=phase,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of BufRd.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=phase,
            ...     )
            >>> buf_rd[0].source.buffer_id
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
    def interpolation(self):
        """
        Gets `interpolation` input of BufRd.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=phase,
            ...     )
            >>> buf_rd[0].source.interpolation
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('interpolation')
        return self._inputs[index]

    @property
    def loop(self):
        """
        Gets `loop` input of BufRd.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=phase,
            ...     )
            >>> buf_rd[0].source.loop
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def phase(self):
        """
        Gets `phase` input of BufRd.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=phase,
            ...     )
            >>> buf_rd[0].source.phase
            OutputProxy(
                source=Phasor(
                    calculation_rate=CalculationRate.AUDIO,
                    rate=OutputProxy(
                        source=BufRateScale(
                            buffer_id=23.0,
                            calculation_rate=CalculationRate.CONTROL
                            ),
                        output_index=0
                        ),
                    reset_pos=0.0,
                    start=0.0,
                    stop=OutputProxy(
                        source=BufFrames(
                            buffer_id=23.0,
                            calculation_rate=CalculationRate.CONTROL
                            ),
                        output_index=0
                        ),
                    trigger=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]
