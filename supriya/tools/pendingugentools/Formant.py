# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Formant(PureUGen):
    r'''

    ::

        >>> formant = ugentools.Formant.(
        ...     bwfrequency=880,
        ...     formfrequency=1760,
        ...     fundfrequency=440,
        ...     )
        >>> formant

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'fundfrequency',
        'formfrequency',
        'bwfrequency',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bwfrequency=880,
        formfrequency=1760,
        fundfrequency=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bwfrequency=bwfrequency,
            formfrequency=formfrequency,
            fundfrequency=fundfrequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bwfrequency=880,
        formfrequency=1760,
        fundfrequency=440,
        ):
        r'''Constructs an audio-rate Formant.

        ::

            >>> formant = ugentools.Formant.ar(
            ...     bwfrequency=880,
            ...     formfrequency=1760,
            ...     fundfrequency=440,
            ...     )
            >>> formant

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bwfrequency=bwfrequency,
            formfrequency=formfrequency,
            fundfrequency=fundfrequency,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def fundfrequency(self):
        r'''Gets `fundfrequency` input of Formant.

        ::

            >>> formant = ugentools.Formant.ar(
            ...     bwfrequency=880,
            ...     formfrequency=1760,
            ...     fundfrequency=440,
            ...     )
            >>> formant.fundfrequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('fundfrequency')
        return self._inputs[index]

    @property
    def formfrequency(self):
        r'''Gets `formfrequency` input of Formant.

        ::

            >>> formant = ugentools.Formant.ar(
            ...     bwfrequency=880,
            ...     formfrequency=1760,
            ...     fundfrequency=440,
            ...     )
            >>> formant.formfrequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('formfrequency')
        return self._inputs[index]

    @property
    def bwfrequency(self):
        r'''Gets `bwfrequency` input of Formant.

        ::

            >>> formant = ugentools.Formant.ar(
            ...     bwfrequency=880,
            ...     formfrequency=1760,
            ...     fundfrequency=440,
            ...     )
            >>> formant.bwfrequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bwfrequency')
        return self._inputs[index]