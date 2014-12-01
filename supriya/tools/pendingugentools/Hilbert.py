# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Hilbert(MultiOutUGen):
    r'''

    ::

        >>> hilbert = ugentools.Hilbert.ar(
        ...     source=source,
        ...     )
        >>> hilbert
        Hilbert.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=source,
        ):
        r'''Constructs an audio-rate Hilbert.

        ::

            >>> hilbert = ugentools.Hilbert.ar(
            ...     source=source,
            ...     )
            >>> hilbert
            Hilbert.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of Hilbert.

        ::

            >>> hilbert = ugentools.Hilbert.ar(
            ...     source=source,
            ...     )
            >>> hilbert.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]