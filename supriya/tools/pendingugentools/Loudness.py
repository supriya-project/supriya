# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Loudness(UGen):
    r'''

    ::

        >>> loudness = ugentools.Loudness.(
        ...     chain=None,
        ...     smask=0.25,
        ...     tmask=1,
        ...     )
        >>> loudness

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'chain',
        'smask',
        'tmask',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        chain=None,
        smask=0.25,
        tmask=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chain=chain,
            smask=smask,
            tmask=tmask,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        chain=None,
        smask=0.25,
        tmask=1,
        ):
        r'''Constructs a control-rate Loudness.

        ::

            >>> loudness = ugentools.Loudness.kr(
            ...     chain=None,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chain=chain,
            smask=smask,
            tmask=tmask,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def chain(self):
        r'''Gets `chain` input of Loudness.

        ::

            >>> loudness = ugentools.Loudness.ar(
            ...     chain=None,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('chain')
        return self._inputs[index]

    @property
    def smask(self):
        r'''Gets `smask` input of Loudness.

        ::

            >>> loudness = ugentools.Loudness.ar(
            ...     chain=None,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.smask

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('smask')
        return self._inputs[index]

    @property
    def tmask(self):
        r'''Gets `tmask` input of Loudness.

        ::

            >>> loudness = ugentools.Loudness.ar(
            ...     chain=None,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.tmask

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('tmask')
        return self._inputs[index]