from supriya.ugens.UGen import UGen


class RecordBuf(UGen):
    """
    Records or overdubs into a buffer.

    ::

        >>> buffer_id = 23
        >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
        >>> record_buf = supriya.ugens.RecordBuf.ar(
        ...     buffer_id=buffer_id,
        ...     done_action=0,
        ...     loop=1,
        ...     offset=0,
        ...     preexisting_level=0,
        ...     record_level=1,
        ...     run=1,
        ...     source=source,
        ...     trigger=1,
        ...     )
        >>> record_buf
        RecordBuf.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'offset',
        'record_level',
        'preexisting_level',
        'run',
        'loop',
        'trigger',
        'done_action',
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
        done_action=0,
        source=None,
        loop=1,
        offset=0,
        preexisting_level=0,
        record_level=1,
        run=1,
        trigger=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            done_action=done_action,
            source=source,
            loop=loop,
            offset=offset,
            preexisting_level=preexisting_level,
            record_level=record_level,
            run=run,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        done_action=0,
        source=None,
        loop=1,
        offset=0,
        preexisting_level=0,
        record_level=1,
        run=1,
        trigger=1,
        ):
        """
        Constructs an audio-rate RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf
            RecordBuf.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            done_action=done_action,
            source=source,
            loop=loop,
            offset=offset,
            preexisting_level=preexisting_level,
            record_level=record_level,
            run=run,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        done_action=0,
        source=None,
        loop=1,
        offset=0,
        preexisting_level=0,
        record_level=1,
        run=1,
        trigger=1,
        ):
        """
        Constructs a control-rate RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.kr(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf
            RecordBuf.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            done_action=done_action,
            source=source,
            loop=loop,
            offset=offset,
            preexisting_level=preexisting_level,
            record_level=record_level,
            run=run,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf.buffer_id
            23.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def done_action(self):
        """
        Gets `done_action` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf.done_action
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def has_done_flag(self):
        """
        Is true if UGen has a done flag.

        Returns boolean.
        """
        return True

    @property
    def source(self):
        """
        Gets `source` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def loop(self):
        """
        Gets `loop` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf.loop
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def offset(self):
        """
        Gets `offset` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf.offset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('offset')
        return self._inputs[index]

    @property
    def preexisting_level(self):
        """
        Gets `preexisting_level` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf.preexisting_level
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('preexisting_level')
        return self._inputs[index]

    @property
    def record_level(self):
        """
        Gets `record_level` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf.record_level
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('record_level')
        return self._inputs[index]

    @property
    def run(self):
        """
        Gets `run` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf.run
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('run')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
            >>> record_buf = supriya.ugens.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     loop=1,
            ...     offset=0,
            ...     preexisting_level=0,
            ...     record_level=1,
            ...     run=1,
            ...     source=source,
            ...     trigger=1,
            ...     )
            >>> record_buf.trigger
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
