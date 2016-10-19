# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class Tap(UGen):
    r"""

    ::

        >>> tap = ugentools.Tap.ar(
        ...     buffer_id=0,
        ...     channel_count=1,
        ...     delay_time=0.2,
        ...     )
        >>> tap
        Tap.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'channel_count',
        'delay_time',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=0,
        channel_count=1,
        delay_time=0.2,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            delay_time=delay_time,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=0,
        channel_count=1,
        delay_time=0.2,
        ):
        r"""
        Constructs an audio-rate Tap.

        ::

            >>> tap = ugentools.Tap.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     delay_time=0.2,
            ...     )
            >>> tap
            Tap.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            delay_time=delay_time,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r"""
        Gets `buffer_id` input of Tap.

        ::

            >>> tap = ugentools.Tap.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     delay_time=0.2,
            ...     )
            >>> tap.buffer_id
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def channel_count(self):
        r"""
        Gets `channel_count` input of Tap.

        ::

            >>> tap = ugentools.Tap.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     delay_time=0.2,
            ...     )
            >>> tap.channel_count
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def delay_time(self):
        r"""
        Gets `delay_time` input of Tap.

        ::

            >>> tap = ugentools.Tap.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     delay_time=0.2,
            ...     )
            >>> tap.delay_time
            0.2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]
