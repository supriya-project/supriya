# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class SyncSaw(PureUGen):
    r"""
    A sawtooth wave that is hard synched to a fundamental pitch.

    ::

        >>> sync_saw = ugentools.SyncSaw.ar(
        ...     saw_frequency=440,
        ...     sync_frequency=440,
        ...     )
        >>> sync_saw
        SyncSaw.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'sync_frequency',
        'saw_frequency',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        saw_frequency=440,
        sync_frequency=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            saw_frequency=saw_frequency,
            sync_frequency=sync_frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        saw_frequency=440,
        sync_frequency=440,
        ):
        r"""
        Constructs an audio-rate SyncSaw.

        ::

            >>> sync_saw = ugentools.SyncSaw.ar(
            ...     saw_frequency=440,
            ...     sync_frequency=440,
            ...     )
            >>> sync_saw
            SyncSaw.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            saw_frequency=saw_frequency,
            sync_frequency=sync_frequency,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        saw_frequency=440,
        sync_frequency=440,
        ):
        r"""
        Constructs a control-rate SyncSaw.

        ::

            >>> sync_saw = ugentools.SyncSaw.kr(
            ...     saw_frequency=440,
            ...     sync_frequency=440,
            ...     )
            >>> sync_saw
            SyncSaw.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            saw_frequency=saw_frequency,
            sync_frequency=sync_frequency,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def saw_frequency(self):
        r"""
        Gets `saw_frequency` input of SyncSaw.

        ::

            >>> sync_saw = ugentools.SyncSaw.ar(
            ...     saw_frequency=440,
            ...     sync_frequency=440,
            ...     )
            >>> sync_saw.saw_frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('saw_frequency')
        return self._inputs[index]

    @property
    def sync_frequency(self):
        r"""
        Gets `sync_frequency` input of SyncSaw.

        ::

            >>> sync_saw = ugentools.SyncSaw.ar(
            ...     saw_frequency=440,
            ...     sync_frequency=440,
            ...     )
            >>> sync_saw.sync_frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('sync_frequency')
        return self._inputs[index]
