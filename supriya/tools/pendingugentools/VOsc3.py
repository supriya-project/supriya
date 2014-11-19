# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class VOsc3(PureUGen):
    r'''

    ::

        >>> vosc_3 = ugentools.VOsc3.(
        ...     bufpos=None,
        ...     freq_1=110,
        ...     freq_2=220,
        ...     freq_3=440,
        ...     )
        >>> vosc_3

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'bufpos',
        'freq_1',
        'freq_2',
        'freq_3',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bufpos=None,
        freq_1=110,
        freq_2=220,
        freq_3=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufpos=bufpos,
            freq_1=freq_1,
            freq_2=freq_2,
            freq_3=freq_3,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bufpos=None,
        freq_1=110,
        freq_2=220,
        freq_3=440,
        ):
        r'''Constructs an audio-rate VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.ar(
            ...     bufpos=None,
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufpos=bufpos,
            freq_1=freq_1,
            freq_2=freq_2,
            freq_3=freq_3,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bufpos=None,
        freq_1=110,
        freq_2=220,
        freq_3=440,
        ):
        r'''Constructs a control-rate VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.kr(
            ...     bufpos=None,
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufpos=bufpos,
            freq_1=freq_1,
            freq_2=freq_2,
            freq_3=freq_3,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bufpos(self):
        r'''Gets `bufpos` input of VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.ar(
            ...     bufpos=None,
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3.bufpos

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bufpos')
        return self._inputs[index]

    @property
    def freq_1(self):
        r'''Gets `freq_1` input of VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.ar(
            ...     bufpos=None,
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3.freq_1

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('freq_1')
        return self._inputs[index]

    @property
    def freq_2(self):
        r'''Gets `freq_2` input of VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.ar(
            ...     bufpos=None,
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3.freq_2

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('freq_2')
        return self._inputs[index]

    @property
    def freq_3(self):
        r'''Gets `freq_3` input of VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.ar(
            ...     bufpos=None,
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3.freq_3

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('freq_3')
        return self._inputs[index]