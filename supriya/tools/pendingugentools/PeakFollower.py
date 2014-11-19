# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PeakFollower(UGen):
    r'''

    ::

        >>> peak_follower = ugentools.PeakFollower.(
        ...     decay=0.999,
        ...     source=None,
        ...     )
        >>> peak_follower

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'decay',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        decay=0.999,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            decay=decay,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decay=0.999,
        source=None,
        ):
        r'''Constructs an audio-rate PeakFollower.

        ::

            >>> peak_follower = ugentools.PeakFollower.ar(
            ...     decay=0.999,
            ...     source=None,
            ...     )
            >>> peak_follower

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decay=decay,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        decay=0.999,
        source=None,
        ):
        r'''Constructs a control-rate PeakFollower.

        ::

            >>> peak_follower = ugentools.PeakFollower.kr(
            ...     decay=0.999,
            ...     source=None,
            ...     )
            >>> peak_follower

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decay=decay,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of PeakFollower.

        ::

            >>> peak_follower = ugentools.PeakFollower.ar(
            ...     decay=0.999,
            ...     source=None,
            ...     )
            >>> peak_follower.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def decay(self):
        r'''Gets `decay` input of PeakFollower.

        ::

            >>> peak_follower = ugentools.PeakFollower.ar(
            ...     decay=0.999,
            ...     source=None,
            ...     )
            >>> peak_follower.decay

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('decay')
        return self._inputs[index]