# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Klang(UGen):
    r'''

    ::

        >>> klang = ugentools.Klang.(
        ...     freqoffset=0,
        ...     freqscale=1,
        ...     specifications_array_ref=None,
        ...     )
        >>> klang

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'specifications_array_ref',
        'freqscale',
        'freqoffset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        freqoffset=0,
        freqscale=1,
        specifications_array_ref=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            freqoffset=freqoffset,
            freqscale=freqscale,
            specifications_array_ref=specifications_array_ref,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        freqoffset=0,
        freqscale=1,
        specifications_array_ref=None,
        ):
        r'''Constructs an audio-rate Klang.

        ::

            >>> klang = ugentools.Klang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=None,
            ...     )
            >>> klang

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            freqoffset=freqoffset,
            freqscale=freqscale,
            specifications_array_ref=specifications_array_ref,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def specifications_array_ref(self):
        r'''Gets `specifications_array_ref` input of Klang.

        ::

            >>> klang = ugentools.Klang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=None,
            ...     )
            >>> klang.specifications_array_ref

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('specifications_array_ref')
        return self._inputs[index]

    @property
    def freqscale(self):
        r'''Gets `freqscale` input of Klang.

        ::

            >>> klang = ugentools.Klang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=None,
            ...     )
            >>> klang.freqscale

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('freqscale')
        return self._inputs[index]

    @property
    def freqoffset(self):
        r'''Gets `freqoffset` input of Klang.

        ::

            >>> klang = ugentools.Klang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=None,
            ...     )
            >>> klang.freqoffset

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('freqoffset')
        return self._inputs[index]