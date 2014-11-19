# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Gendy3(UGen):
    r'''

    ::

        >>> gendy_3 = ugentools.Gendy3.(
        ...     adparam=1,
        ...     ampdist=1,
        ...     ampscale=0.5,
        ...     ddparam=1,
        ...     durdist=1,
        ...     durscale=0.5,
        ...     frequency=440,
        ...     init_cps=12,
        ...     knum=None,
        ...     )
        >>> gendy_3

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'ampdist',
        'durdist',
        'adparam',
        'ddparam',
        'frequency',
        'ampscale',
        'durscale',
        'init_cps',
        'knum',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        adparam=1,
        ampdist=1,
        ampscale=0.5,
        ddparam=1,
        durdist=1,
        durscale=0.5,
        frequency=440,
        init_cps=12,
        knum=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            adparam=adparam,
            ampdist=ampdist,
            ampscale=ampscale,
            ddparam=ddparam,
            durdist=durdist,
            durscale=durscale,
            frequency=frequency,
            init_cps=init_cps,
            knum=knum,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        adparam=1,
        ampdist=1,
        ampscale=0.5,
        ddparam=1,
        durdist=1,
        durscale=0.5,
        frequency=440,
        init_cps=12,
        knum=None,
        ):
        r'''Constructs an audio-rate Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            adparam=adparam,
            ampdist=ampdist,
            ampscale=ampscale,
            ddparam=ddparam,
            durdist=durdist,
            durscale=durscale,
            frequency=frequency,
            init_cps=init_cps,
            knum=knum,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        adparam=1,
        ampdist=1,
        ampscale=0.5,
        ddparam=1,
        durdist=1,
        durscale=0.5,
        frequency=440,
        init_cps=12,
        knum=None,
        ):
        r'''Constructs a control-rate Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.kr(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            adparam=adparam,
            ampdist=ampdist,
            ampscale=ampscale,
            ddparam=ddparam,
            durdist=durdist,
            durscale=durscale,
            frequency=frequency,
            init_cps=init_cps,
            knum=knum,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def adparam(self):
        r'''Gets `adparam` input of Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3.adparam

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('adparam')
        return self._inputs[index]

    @property
    def ampdist(self):
        r'''Gets `ampdist` input of Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3.ampdist

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('ampdist')
        return self._inputs[index]

    @property
    def ampscale(self):
        r'''Gets `ampscale` input of Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3.ampscale

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('ampscale')
        return self._inputs[index]

    @property
    def ddparam(self):
        r'''Gets `ddparam` input of Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3.ddparam

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('ddparam')
        return self._inputs[index]

    @property
    def durdist(self):
        r'''Gets `durdist` input of Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3.durdist

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('durdist')
        return self._inputs[index]

    @property
    def durscale(self):
        r'''Gets `durscale` input of Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3.durscale

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('durscale')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def init_cps(self):
        r'''Gets `init_cps` input of Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3.init_cps

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('init_cps')
        return self._inputs[index]

    @property
    def knum(self):
        r'''Gets `knum` input of Gendy3.

        ::

            >>> gendy_3 = ugentools.Gendy3.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     frequency=440,
            ...     init_cps=12,
            ...     knum=None,
            ...     )
            >>> gendy_3.knum

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('knum')
        return self._inputs[index]