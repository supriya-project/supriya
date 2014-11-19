# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Select(PureUGen):
    r'''

    ::

        >>> select = ugentools.Select.(
        ...     array=None,
        ...     which=None,
        ...     )
        >>> select

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'which',
        'array',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        array=None,
        which=None,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            array=array,
            which=which,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        array=None,
        which=None,
        ):
        r'''Constructs an audio-rate Select.

        ::

            >>> select = ugentools.Select.ar(
            ...     array=None,
            ...     which=None,
            ...     )
            >>> select

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            array=array,
            which=which,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        array=None,
        which=None,
        ):
        r'''Constructs a control-rate Select.

        ::

            >>> select = ugentools.Select.kr(
            ...     array=None,
            ...     which=None,
            ...     )
            >>> select

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            array=array,
            which=which,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def which(self):
        r'''Gets `which` input of Select.

        ::

            >>> select = ugentools.Select.ar(
            ...     array=None,
            ...     which=None,
            ...     )
            >>> select.which

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('which')
        return self._inputs[index]

    @property
    def array(self):
        r'''Gets `array` input of Select.

        ::

            >>> select = ugentools.Select.ar(
            ...     array=None,
            ...     which=None,
            ...     )
            >>> select.array

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('array')
        return self._inputs[index]