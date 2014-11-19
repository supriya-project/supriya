# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BHiCut import BHiCut


class LRHiCut(BHiCut):
    r'''

    ::

        >>> lrhi_cut = ugentools.LRHiCut.(
        ...     frequency=None,
        ...     max_order=5,
        ...     order=2,
        ...     source=None,
        ...     )
        >>> lrhi_cut

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'order',
        'max_order',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=None,
        max_order=5,
        order=2,
        source=None,
        ):
        BHiCut.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            max_order=max_order,
            order=order,
            source=source,
            )

    ### PUBLIC METHODS ###

    # def allRQs(): ...

    @classmethod
    def ar(
        cls,
        frequency=None,
        max_order=5,
        order=2,
        source=None,
        ):
        r'''Constructs an audio-rate LRHiCut.

        ::

            >>> lrhi_cut = ugentools.LRHiCut.ar(
            ...     frequency=None,
            ...     max_order=5,
            ...     order=2,
            ...     source=None,
            ...     )
            >>> lrhi_cut

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            max_order=max_order,
            order=order,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    # def filterClass(): ...

    # def initClass(): ...

    @classmethod
    def kr(
        cls,
        frequency=None,
        max_order=5,
        order=2,
        source=None,
        ):
        r'''Constructs a control-rate LRHiCut.

        ::

            >>> lrhi_cut = ugentools.LRHiCut.kr(
            ...     frequency=None,
            ...     max_order=5,
            ...     order=2,
            ...     source=None,
            ...     )
            >>> lrhi_cut

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            max_order=max_order,
            order=order,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def new1(): ...

    # def newFixed(): ...

    # def newVari(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of LRHiCut.

        ::

            >>> lrhi_cut = ugentools.LRHiCut.ar(
            ...     frequency=None,
            ...     max_order=5,
            ...     order=2,
            ...     source=None,
            ...     )
            >>> lrhi_cut.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def max_order(self):
        r'''Gets `max_order` input of LRHiCut.

        ::

            >>> lrhi_cut = ugentools.LRHiCut.ar(
            ...     frequency=None,
            ...     max_order=5,
            ...     order=2,
            ...     source=None,
            ...     )
            >>> lrhi_cut.max_order

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('max_order')
        return self._inputs[index]

    @property
    def order(self):
        r'''Gets `order` input of LRHiCut.

        ::

            >>> lrhi_cut = ugentools.LRHiCut.ar(
            ...     frequency=None,
            ...     max_order=5,
            ...     order=2,
            ...     source=None,
            ...     )
            >>> lrhi_cut.order

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('order')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of LRHiCut.

        ::

            >>> lrhi_cut = ugentools.LRHiCut.ar(
            ...     frequency=None,
            ...     max_order=5,
            ...     order=2,
            ...     source=None,
            ...     )
            >>> lrhi_cut.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]