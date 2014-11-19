# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class DynKlank(UGen):
    r'''

    ::

        >>> dyn_klank = ugentools.DynKlank.(
        ...     decayscale=1,
        ...     freqoffset=0,
        ...     freqscale=1,
        ...     input=None,
        ...     specifications_array_ref=None,
        ...     )
        >>> dyn_klank

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'specifications_array_ref',
        'input',
        'freqscale',
        'freqoffset',
        'decayscale',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        decayscale=1,
        freqoffset=0,
        freqscale=1,
        input=None,
        specifications_array_ref=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            decayscale=decayscale,
            freqoffset=freqoffset,
            freqscale=freqscale,
            input=input,
            specifications_array_ref=specifications_array_ref,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decayscale=1,
        freqoffset=0,
        freqscale=1,
        input=None,
        specifications_array_ref=None,
        ):
        r'''Constructs an audio-rate DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=None,
            ...     specifications_array_ref=None,
            ...     )
            >>> dyn_klank

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decayscale=decayscale,
            freqoffset=freqoffset,
            freqscale=freqscale,
            input=input,
            specifications_array_ref=specifications_array_ref,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        decayscale=1,
        freqoffset=0,
        freqscale=1,
        input=None,
        specifications_array_ref=None,
        ):
        r'''Constructs a control-rate DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.kr(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=None,
            ...     specifications_array_ref=None,
            ...     )
            >>> dyn_klank

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decayscale=decayscale,
            freqoffset=freqoffset,
            freqscale=freqscale,
            input=input,
            specifications_array_ref=specifications_array_ref,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def decayscale(self):
        r'''Gets `decayscale` input of DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=None,
            ...     specifications_array_ref=None,
            ...     )
            >>> dyn_klank.decayscale

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('decayscale')
        return self._inputs[index]

    @property
    def freqoffset(self):
        r'''Gets `freqoffset` input of DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=None,
            ...     specifications_array_ref=None,
            ...     )
            >>> dyn_klank.freqoffset

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('freqoffset')
        return self._inputs[index]

    @property
    def freqscale(self):
        r'''Gets `freqscale` input of DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=None,
            ...     specifications_array_ref=None,
            ...     )
            >>> dyn_klank.freqscale

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('freqscale')
        return self._inputs[index]

    @property
    def input(self):
        r'''Gets `input` input of DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=None,
            ...     specifications_array_ref=None,
            ...     )
            >>> dyn_klank.input

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('input')
        return self._inputs[index]

    @property
    def specifications_array_ref(self):
        r'''Gets `specifications_array_ref` input of DynKlank.

        ::

            >>> dyn_klank = ugentools.DynKlank.ar(
            ...     decayscale=1,
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     input=None,
            ...     specifications_array_ref=None,
            ...     )
            >>> dyn_klank.specifications_array_ref

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('specifications_array_ref')
        return self._inputs[index]