# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Loudness(UGen):
    r'''Extraction of instantaneous loudness in `sones`.

    ::

        >>> loudness = ugentools.Loudness(
        ...     pv_chain=None,
        ...     smask=0.25,
        ...     tmask=1,
        ...     )
        >>> loudness

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'smask',
        'tmask',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        pv_chain=None,
        smask=0.25,
        tmask=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            smask=smask,
            tmask=tmask,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        smask=0.25,
        tmask=1,
        ):
        r'''Constructs a control-rate Loudness.

        ::

            >>> loudness = ugentools.Loudness.kr(
            ...     pv_chain=None,
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
            pv_chain=pv_chain,
            smask=smask,
            tmask=tmask,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of Loudness.

        ::

            >>> loudness = ugentools.Loudness.ar(
            ...     pv_chain=None,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def smask(self):
        r'''Gets `smask` input of Loudness.

        ::

            >>> loudness = ugentools.Loudness.ar(
            ...     pv_chain=None,
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
            ...     pv_chain=None,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.tmask

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('tmask')
        return self._inputs[index]