# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class DelTapWr(UGen):
    r"""
    A delay tap writer unit generator.

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
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        calculation_rate=None,
        source=None,
        ):
        buffer_id = int(buffer_id)
        UGen.__init__(
            self,
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        source=None,
        ):
        r"""
        Constructs an audio-rate delay tap write.

        ::

            >>> buffer_id = 0
            >>> source = ugentools.In.ar(0)
            >>> del_tap_wr = ugentools.DelTapWr.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> del_tap_wr
            DelTapWr.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        source = cls._as_audio_rate_input(source)
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        source=None,
        ):
        r"""
        Constructs an audio-rate delay tap write.

        ::

            >>> buffer_id = 0
            >>> source = ugentools.In.kr(0)
            >>> del_tap_wr = ugentools.DelTapWr.kr(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> del_tap_wr
            DelTapWr.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        source = cls._as_audio_rate_input(source)
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r"""
        Gets `buffer_id` input of DelTapWr.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.In.ar(bus=0)
            >>> del_tap_wr = ugentools.DelTapWr.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> del_tap_wr.buffer_id
            23.0

        Returns input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def source(self):
        r"""
        Gets `source` input of DelTapWr.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.In.ar(bus=0)
            >>> del_tap_wr = ugentools.DelTapWr.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> del_tap_wr.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
