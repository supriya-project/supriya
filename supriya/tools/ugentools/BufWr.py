# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class BufWr(UGen):
    r'''A buffer-writing oscillator.

    ::

        >>> buffer_id = 23
        >>> phase = ugentools.Phasor.ar(
        ...     rate=ugentools.BufRateScale.kr(buffer_id),
        ...     start=0,
        ...     stop=ugentools.BufFrames.kr(buffer_id),
        ...     )
        >>> source = ugentools.SoundIn.ar(bus=(0, 1))
        >>> buf_wr = ugentools.BufWr.ar(
        ...     buffer_id=buffer_id,
        ...     loop=1,
        ...     phase=phase,
        ...     source=source,
        ...     )
        >>> buf_wr
        BufWr.ar()

    '''

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
        r'''Constructs an audio-rate BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = ugentools.BufWr.ar(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr
            BufWr.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
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
        r'''Constructs a control-rate BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = ugentools.BufWr.kr(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr
            BufWr.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
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
        r'''Gets `buffer_id` input of BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = ugentools.BufWr.ar(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr.buffer_id
            23.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def has_done_flag(self):
        r'''Is true if UGen has a done flag.

        Returns boolean.
        '''
        return True

    @property
    def loop(self):
        r'''Gets `loop` input of BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = ugentools.BufWr.ar(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr.loop
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = ugentools.BufWr.ar(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr.phase
            OutputProxy(
                source=Phasor(
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    rate=OutputProxy(
                        source=BufRateScale(
                            buffer_id=23.0,
                            calculation_rate=<CalculationRate.CONTROL: 1>
                            ),
                        output_index=0
                        ),
                    reset_pos=0.0,
                    start=0.0,
                    stop=OutputProxy(
                        source=BufFrames(
                            buffer_id=23.0,
                            calculation_rate=<CalculationRate.CONTROL: 1>
                            ),
                        output_index=0
                        ),
                    trigger=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of BufWr.

        ::

            >>> buffer_id = 23
            >>> phase = ugentools.Phasor.ar(
            ...     rate=ugentools.BufRateScale.kr(buffer_id),
            ...     start=0,
            ...     stop=ugentools.BufFrames.kr(buffer_id),
            ...     )
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> buf_wr = ugentools.BufWr.ar(
            ...     buffer_id=buffer_id,
            ...     loop=1,
            ...     phase=phase,
            ...     source=source,
            ...     )
            >>> buf_wr.source
            OutputProxy(
                source=In(
                    bus=OutputProxy(
                        source=NumOutputBuses(
                            calculation_rate=<CalculationRate.SCALAR: 0>
                            ),
                        output_index=0
                        ),
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    channel_count=2
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]