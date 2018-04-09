from supriya.tools.ugentools.UGen import UGen


class DelTapRd(UGen):
    """
    A delay tap reader unit generator.

    ::

        >>> buffer_id = 0
        >>> source = ugentools.SoundIn.ar(0)
        >>> tapin = ugentools.DelTapWr.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )

    ::

        >>> tapin
        DelTapWr.ar()

    ::

        >>> tapout = ugentools.DelTapRd.ar(
        ...     buffer_id=buffer_id,
        ...     phase=tapin,
        ...     delay_time=0.1,
        ...     interpolation=True,
        ...     )

    ::

        >>> tapout
        DelTapRd.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'phase',
        'delay_time',
        'interpolation',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        phase=None,
        delay_time=None,
        interpolation=None,
        ):
        buffer_id = int(buffer_id)
        interpolation = int(bool(interpolation))
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            phase=phase,
            delay_time=delay_time,
            interpolation=interpolation,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        phase=None,
        delay_time=None,
        interpolation=True,
        ):
        """
        Constructs an audio-rate delay tap reader.

        ::

            >>> buffer_id = 0
            >>> source = ugentools.SoundIn.ar(0)
            >>> phase = ugentools.DelTapWr.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> del_tap_rd = ugentools.DelTapRd.ar(
            ...     buffer_id=buffer_id,
            ...     phase=phase,
            ...     delay_time=0.1,
            ...     interpolation=True,
            ...     )
            >>> del_tap_rd
            DelTapRd.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            phase=phase,
            delay_time=delay_time,
            interpolation=interpolation,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        phase=None,
        delay_time=None,
        interpolation=True,
        ):
        """
        Constructs a control-rate delay tap reader.

        ::

            >>> source = ugentools.In.kr(0)
            >>> phase = ugentools.DelTapWr.kr(
            ...     buffer_id=23,
            ...     source=source,
            ...     )
            >>> del_tap_rd = ugentools.DelTapRd.kr(
            ...     buffer_id=23,
            ...     phase=phase,
            ...     delay_time=0.1,
            ...     interpolation=True,
            ...     )
            >>> del_tap_rd
            DelTapRd.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            phase=phase,
            delay_time=delay_time,
            interpolation=interpolation,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of DelTapRd.

        ::

            >>> phase = ugentools.DelTapWr.ar(
            ...     buffer_id=23,
            ...     source=ugentools.In.ar(bus=0),
            ...     )
            >>> del_tap_rd = ugentools.DelTapRd.ar(
            ...     buffer_id=23,
            ...     delay_time=0.1,
            ...     phase=phase,
            ...     )
            >>> del_tap_rd.buffer_id
            23.0

        Returns input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def delay_time(self):
        """
        Gets `delay_time` input of DelTapRd.

        ::

            >>> delay_time = 0.2
            >>> phase = ugentools.DelTapWr.ar(
            ...     buffer_id=23,
            ...     source=ugentools.In.ar(bus=0),
            ...     )
            >>> del_tap_rd = ugentools.DelTapRd.ar(
            ...     buffer_id=23,
            ...     delay_time=delay_time,
            ...     phase=phase,
            ...     )
            >>> del_tap_rd.delay_time
            0.2

        Returns input.
        """
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]

    @property
    def interpolation(self):
        """
        Gets `interpolation` input of DelTapRd.

        ::

            >>> interpolation = 1
            >>> phase = ugentools.DelTapWr.ar(
            ...     buffer_id=23,
            ...     source=ugentools.In.ar(bus=0),
            ...     )
            >>> del_tap_rd = ugentools.DelTapRd.ar(
            ...     buffer_id=23,
            ...     delay_time=0.1,
            ...     interpolation=interpolation,
            ...     phase=phase,
            ...     )
            >>> del_tap_rd.interpolation
            1.0

        Returns input.
        """
        index = self._ordered_input_names.index('interpolation')
        return self._inputs[index]

    @property
    def phase(self):
        """
        Gets `phase` input of DelTapRd.

        ::

            >>> phase = ugentools.DelTapWr.ar(
            ...     buffer_id=23,
            ...     source=ugentools.In.ar(bus=0),
            ...     )
            >>> del_tap_rd = ugentools.DelTapRd.ar(
            ...     buffer_id=23,
            ...     delay_time=0.1,
            ...     phase=phase,
            ...     )
            >>> del_tap_rd.phase
            DelTapWr.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]
