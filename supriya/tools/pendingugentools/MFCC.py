# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class MFCC(MultiOutUGen):
    r'''

    ::

        >>> mfcc = ugentools.MFCC.(
        ...     chain=None,
        ...     numcoeff=13,
        ...     )
        >>> mfcc

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'chain',
        'numcoeff',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        chain=None,
        numcoeff=13,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chain=chain,
            numcoeff=numcoeff,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        chain=None,
        numcoeff=13,
        ):
        r'''Constructs a control-rate MFCC.

        ::

            >>> mfcc = ugentools.MFCC.kr(
            ...     chain=None,
            ...     numcoeff=13,
            ...     )
            >>> mfcc

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chain=chain,
            numcoeff=numcoeff,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def chain(self):
        r'''Gets `chain` input of MFCC.

        ::

            >>> mfcc = ugentools.MFCC.ar(
            ...     chain=None,
            ...     numcoeff=13,
            ...     )
            >>> mfcc.chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('chain')
        return self._inputs[index]

    @property
    def numcoeff(self):
        r'''Gets `numcoeff` input of MFCC.

        ::

            >>> mfcc = ugentools.MFCC.ar(
            ...     chain=None,
            ...     numcoeff=13,
            ...     )
            >>> mfcc.numcoeff

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('numcoeff')
        return self._inputs[index]