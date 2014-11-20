# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Onsets(UGen):
    r'''

    ::

        >>> onsets = ugentools.Onsets.(
        ...     pv_chain=None,
        ...     floor=0.1,
        ...     medianspan=11,
        ...     mingap=10,
        ...     odftype='"rcomplex"',
        ...     rawodf=0,
        ...     relaxtime=1,
        ...     threshold=0.5,
        ...     whtype=1,
        ...     )
        >>> onsets

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'threshold',
        'odftype',
        'relaxtime',
        'floor',
        'mingap',
        'medianspan',
        'whtype',
        'rawodf',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        pv_chain=None,
        floor=0.1,
        medianspan=11,
        mingap=10,
        odftype='"rcomplex"',
        rawodf=0,
        relaxtime=1,
        threshold=0.5,
        whtype=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            floor=floor,
            medianspan=medianspan,
            mingap=mingap,
            odftype=odftype,
            rawodf=rawodf,
            relaxtime=relaxtime,
            threshold=threshold,
            whtype=whtype,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        floor=0.1,
        medianspan=11,
        mingap=10,
        odftype='"rcomplex"',
        rawodf=0,
        relaxtime=1,
        threshold=0.5,
        whtype=1,
        ):
        r'''Constructs a control-rate Onsets.

        ::

            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=None,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype='"rcomplex"',
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            floor=floor,
            medianspan=medianspan,
            mingap=mingap,
            odftype=odftype,
            rawodf=rawodf,
            relaxtime=relaxtime,
            threshold=threshold,
            whtype=whtype,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of Onsets.

        ::

            >>> onsets = ugentools.Onsets.ar(
            ...     pv_chain=None,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype='"rcomplex"',
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def floor(self):
        r'''Gets `floor` input of Onsets.

        ::

            >>> onsets = ugentools.Onsets.ar(
            ...     pv_chain=None,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype='"rcomplex"',
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.floor

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('floor')
        return self._inputs[index]

    @property
    def medianspan(self):
        r'''Gets `medianspan` input of Onsets.

        ::

            >>> onsets = ugentools.Onsets.ar(
            ...     pv_chain=None,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype='"rcomplex"',
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.medianspan

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('medianspan')
        return self._inputs[index]

    @property
    def mingap(self):
        r'''Gets `mingap` input of Onsets.

        ::

            >>> onsets = ugentools.Onsets.ar(
            ...     pv_chain=None,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype='"rcomplex"',
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.mingap

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('mingap')
        return self._inputs[index]

    @property
    def odftype(self):
        r'''Gets `odftype` input of Onsets.

        ::

            >>> onsets = ugentools.Onsets.ar(
            ...     pv_chain=None,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype='"rcomplex"',
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.odftype

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('odftype')
        return self._inputs[index]

    @property
    def rawodf(self):
        r'''Gets `rawodf` input of Onsets.

        ::

            >>> onsets = ugentools.Onsets.ar(
            ...     pv_chain=None,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype='"rcomplex"',
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.rawodf

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('rawodf')
        return self._inputs[index]

    @property
    def relaxtime(self):
        r'''Gets `relaxtime` input of Onsets.

        ::

            >>> onsets = ugentools.Onsets.ar(
            ...     pv_chain=None,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype='"rcomplex"',
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.relaxtime

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('relaxtime')
        return self._inputs[index]

    @property
    def threshold(self):
        r'''Gets `threshold` input of Onsets.

        ::

            >>> onsets = ugentools.Onsets.ar(
            ...     pv_chain=None,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype='"rcomplex"',
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.threshold

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]

    @property
    def whtype(self):
        r'''Gets `whtype` input of Onsets.

        ::

            >>> onsets = ugentools.Onsets.ar(
            ...     pv_chain=None,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype='"rcomplex"',
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.whtype

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('whtype')
        return self._inputs[index]