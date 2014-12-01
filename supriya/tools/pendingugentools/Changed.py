# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Changed(Filter):
    r'''

    ::

        >>> changed = ugentools.Changed.ar(
        ...     input=input,
        ...     threshold=0,
        ...     )
        >>> changed
        Changed.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'input',
        'threshold',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        input=None,
        threshold=0,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            input=input,
            threshold=threshold,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        input=None,
        threshold=0,
        ):
        r'''Constructs an audio-rate Changed.

        ::

            >>> changed = ugentools.Changed.ar(
            ...     input=input,
            ...     threshold=0,
            ...     )
            >>> changed
            Changed.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            input=input,
            threshold=threshold,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        input=None,
        threshold=0,
        ):
        r'''Constructs a control-rate Changed.

        ::

            >>> changed = ugentools.Changed.kr(
            ...     input=input,
            ...     threshold=0,
            ...     )
            >>> changed
            Changed.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            input=input,
            threshold=threshold,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def input(self):
        r'''Gets `input` input of Changed.

        ::

            >>> changed = ugentools.Changed.ar(
            ...     input=input,
            ...     threshold=0,
            ...     )
            >>> changed.input

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('input')
        return self._inputs[index]

    @property
    def threshold(self):
        r'''Gets `threshold` input of Changed.

        ::

            >>> changed = ugentools.Changed.ar(
            ...     input=input,
            ...     threshold=0,
            ...     )
            >>> changed.threshold
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]