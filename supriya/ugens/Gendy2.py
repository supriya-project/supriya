from supriya.ugens.UGen import UGen


class Gendy2(UGen):
    """
    A dynamic stochastic synthesis generator.

    ::

        >>> gendy_2 = supriya.ugens.Gendy2.ar(
        ...     a=1.17,
        ...     adparam=1,
        ...     ampdist=1,
        ...     ampscale=0.5,
        ...     c=0.31,
        ...     ddparam=1,
        ...     durdist=1,
        ...     durscale=0.5,
        ...     init_cps=12,
        ...     knum=10,
        ...     maxfrequency=660,
        ...     minfrequency=440,
        ...     )
        >>> gendy_2
        Gendy2.ar()

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
        'a',
        'c',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a=1.17,
        adparam=1,
        ampdist=1,
        ampscale=0.5,
        c=0.31,
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
            a=a,
            adparam=adparam,
            ampdist=ampdist,
            ampscale=ampscale,
            c=c,
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
        a=1.17,
        adparam=1,
        ampdist=1,
        ampscale=0.5,
        c=0.31,
        ddparam=1,
        durdist=1,
        durscale=0.5,
        init_cps=12,
        knum=None,
        maxfrequency=660,
        minfrequency=440,
        ):
        """
        Constructs an audio-rate Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2
            Gendy2.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            adparam=adparam,
            ampdist=ampdist,
            ampscale=ampscale,
            c=c,
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
        a=1.17,
        adparam=1,
        ampdist=1,
        ampscale=0.5,
        c=0.31,
        ddparam=1,
        durdist=1,
        durscale=0.5,
        init_cps=12,
        knum=None,
        maxfrequency=1000,
        minfrequency=20,
        ):
        """
        Constructs a control-rate Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.kr(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=1000,
            ...     minfrequency=20,
            ...     )
            >>> gendy_2
            Gendy2.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            adparam=adparam,
            ampdist=ampdist,
            ampscale=ampscale,
            c=c,
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
    def a(self):
        """
        Gets `a` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.a
            1.17

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def adparam(self):
        """
        Gets `adparam` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.adparam
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('adparam')
        return self._inputs[index]

    @property
    def ampdist(self):
        """
        Gets `ampdist` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.ampdist
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('ampdist')
        return self._inputs[index]

    @property
    def ampscale(self):
        """
        Gets `ampscale` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.ampscale
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('ampscale')
        return self._inputs[index]

    @property
    def c(self):
        """
        Gets `c` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.c
            0.31

        Returns ugen input.
        """
        index = self._ordered_input_names.index('c')
        return self._inputs[index]

    @property
    def ddparam(self):
        """
        Gets `ddparam` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.ddparam
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('ddparam')
        return self._inputs[index]

    @property
    def durdist(self):
        """
        Gets `durdist` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.durdist
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('durdist')
        return self._inputs[index]

    @property
    def durscale(self):
        """
        Gets `durscale` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.durscale
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('durscale')
        return self._inputs[index]

    @property
    def init_cps(self):
        """
        Gets `init_cps` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.init_cps
            12.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('init_cps')
        return self._inputs[index]

    @property
    def knum(self):
        """
        Gets `knum` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.knum
            10.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('knum')
        return self._inputs[index]

    @property
    def maxfrequency(self):
        """
        Gets `maxfrequency` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.maxfrequency
            660.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maxfrequency')
        return self._inputs[index]

    @property
    def minfrequency(self):
        """
        Gets `minfrequency` input of Gendy2.

        ::

            >>> gendy_2 = supriya.ugens.Gendy2.ar(
            ...     a=1.17,
            ...     adparam=1,
            ...     ampdist=1,
            ...     ampscale=0.5,
            ...     c=0.31,
            ...     ddparam=1,
            ...     durdist=1,
            ...     durscale=0.5,
            ...     init_cps=12,
            ...     knum=10,
            ...     maxfrequency=660,
            ...     minfrequency=440,
            ...     )
            >>> gendy_2.minfrequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minfrequency')
        return self._inputs[index]
