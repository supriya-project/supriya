from supriya.tools.ugentools.UGen import UGen


class Gendy3(UGen):
    """
    A dynamic stochastic synthesis generator.

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
        ...     knum=10,
        ...     )
        >>> gendy_3
        Gendy3.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

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
        """
        Constructs an audio-rate Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3
            Gendy3.ar()

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
        """
        Constructs a control-rate Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3
            Gendy3.kr()

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
            frequency=frequency,
            init_cps=init_cps,
            knum=knum,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def adparam(self):
        """
        Gets `adparam` input of Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3.adparam
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('adparam')
        return self._inputs[index]

    @property
    def ampdist(self):
        """
        Gets `ampdist` input of Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3.ampdist
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('ampdist')
        return self._inputs[index]

    @property
    def ampscale(self):
        """
        Gets `ampscale` input of Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3.ampscale
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('ampscale')
        return self._inputs[index]

    @property
    def ddparam(self):
        """
        Gets `ddparam` input of Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3.ddparam
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('ddparam')
        return self._inputs[index]

    @property
    def durdist(self):
        """
        Gets `durdist` input of Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3.durdist
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('durdist')
        return self._inputs[index]

    @property
    def durscale(self):
        """
        Gets `durscale` input of Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3.durscale
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('durscale')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def init_cps(self):
        """
        Gets `init_cps` input of Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3.init_cps
            12.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('init_cps')
        return self._inputs[index]

    @property
    def knum(self):
        """
        Gets `knum` input of Gendy3.

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
            ...     knum=10,
            ...     )
            >>> gendy_3.knum
            10.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('knum')
        return self._inputs[index]
