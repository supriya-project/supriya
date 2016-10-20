# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class Gendy1(UGen):
    """
    A dynamic stochastic synthesis generator.

    ::

        >>> gendy_1 = ugentools.Gendy1.ar(
        ...     adparam=1,
        ...     ampdist=1,
        ...     ampscale=0.5,
        ...     ddparam=1,
        ...     durdist=1,
        ...     durscale=0.5,
        ...     init_cps=12,
        ...     knum=10,
        ...     maxfrequency=660,
        ...     minfrequency=440,
        ...     )
        >>> gendy_1
        Gendy1.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'ampdist',
        'durdist',
        'adparam',
        'ddparam',
        'minfrequency',
        'maxfrequency',
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
        init_cps=12,
        knum=None,
        maxfrequency=660,
        minfrequency=440,
        ):
        if knum is None:
            knum = init_cps
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            adparam=adparam,
            ampdist=ampdist,
            ampscale=ampscale,
            ddparam=ddparam,
            durdist=durdist,
            durscale=durscale,
            init_cps=init_cps,
            knum=knum,
            maxfrequency=maxfrequency,
            minfrequency=minfrequency,
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
        init_cps=12,
        knum=None,
        maxfrequency=660,
        minfrequency=440,
        ):
        """
        Constructs an audio-rate Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1
            Gendy1.ar()

        Returns ugen graph.
        """
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
            init_cps=init_cps,
            knum=knum,
            maxfrequency=maxfrequency,
            minfrequency=minfrequency,
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
        init_cps=12,
        knum=None,
        maxfrequency=1000,
        minfrequency=20,
        ):
        """
        Constructs a control-rate Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.kr(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=1000,
            ...     minfrequency=20,
            ...     )
            >>> gendy_1
            Gendy1.kr()

        Returns ugen graph.
        """
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
            init_cps=init_cps,
            knum=knum,
            maxfrequency=maxfrequency,
            minfrequency=minfrequency,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def adparam(self):
        """
        Gets `adparam` input of Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1.adparam
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('adparam')
        return self._inputs[index]

    @property
    def ampdist(self):
        """
        Gets `ampdist` input of Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1.ampdist
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('ampdist')
        return self._inputs[index]

    @property
    def ampscale(self):
        """
        Gets `ampscale` input of Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1.ampscale
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('ampscale')
        return self._inputs[index]

    @property
    def ddparam(self):
        """
        Gets `ddparam` input of Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1.ddparam
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('ddparam')
        return self._inputs[index]

    @property
    def durdist(self):
        """
        Gets `durdist` input of Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1.durdist
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('durdist')
        return self._inputs[index]

    @property
    def durscale(self):
        """
        Gets `durscale` input of Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1.durscale
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('durscale')
        return self._inputs[index]

    @property
    def init_cps(self):
        """
        Gets `init_cps` input of Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1.init_cps
            12.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('init_cps')
        return self._inputs[index]

    @property
    def knum(self):
        """
        Gets `knum` input of Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1.knum
            10.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('knum')
        return self._inputs[index]

    @property
    def maxfrequency(self):
        """
        Gets `maxfrequency` input of Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1.maxfrequency
            660.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maxfrequency')
        return self._inputs[index]

    @property
    def minfrequency(self):
        """
        Gets `minfrequency` input of Gendy1.

        ::

            >>> gendy_1 = ugentools.Gendy1.ar(
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_1.minfrequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minfrequency')
        return self._inputs[index]
