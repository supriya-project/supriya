# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_HainsworthFoote(PV_ChainUGen):
    r'''

    ::

        >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote.(
        ...     buffer_id=None,
        ...     propf=0,
        ...     proph=0,
        ...     threshold=1,
        ...     waittime=0.04,
        ...     )
        >>> pv_hainsworth_foote

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'proph',
        'propf',
        'threshold',
        'waittime',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        propf=0,
        proph=0,
        threshold=1,
        waittime=0.04,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            propf=propf,
            proph=proph,
            threshold=threshold,
            waittime=waittime,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        propf=0,
        proph=0,
        threshold=1,
        waittime=0.04,
        ):
        r'''Constructs an audio-rate PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote.ar(
            ...     buffer_id=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            propf=propf,
            proph=proph,
            threshold=threshold,
            waittime=waittime,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote.ar(
            ...     buffer_id=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def propf(self):
        r'''Gets `propf` input of PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote.ar(
            ...     buffer_id=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.propf

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('propf')
        return self._inputs[index]

    @property
    def proph(self):
        r'''Gets `proph` input of PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote.ar(
            ...     buffer_id=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.proph

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('proph')
        return self._inputs[index]

    @property
    def threshold(self):
        r'''Gets `threshold` input of PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote.ar(
            ...     buffer_id=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.threshold

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]

    @property
    def waittime(self):
        r'''Gets `waittime` input of PV_HainsworthFoote.

        ::

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote.ar(
            ...     buffer_id=None,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.waittime

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('waittime')
        return self._inputs[index]