from .bases import UGen, param, ugen


@ugen(ar=True, kr=True)
class Gendy1(UGen):
    """
    A dynamic stochastic synthesis generator.

    ::

        >>> gendy_1 = supriya.ugens.Gendy1.ar(
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
        ... )
        >>> gendy_1
        Gendy1.ar()

    """

    ### CLASS VARIABLES ###

    ampdist = param(1)
    durdist = param(1)
    adparam = param(1)
    ddparam = param(1)
    minfrequency = param(440)
    maxfrequency = param(660)
    ampscale = param(0.5)
    durscale = param(0.5)
    init_cps = param(12)
    knum = param(None)

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


@ugen(ar=True, kr=True)
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
        ... )
        >>> gendy_2
        Gendy2.ar()

    """

    ampdist = param(1)
    durdist = param(1)
    adparam = param(1)
    ddparam = param(1)
    minfrequency = param(440)
    maxfrequency = param(660)
    ampscale = param(0.5)
    durscale = param(0.5)
    init_cps = param(12)
    knum = param(None)
    a = param(1.17)
    c = param(0.31)


@ugen(ar=True, kr=True)
class Gendy3(UGen):
    """
    A dynamic stochastic synthesis generator.

    ::

        >>> gendy_3 = supriya.ugens.Gendy3.ar(
        ...     adparam=1,
        ...     ampdist=1,
        ...     ampscale=0.5,
        ...     ddparam=1,
        ...     durdist=1,
        ...     durscale=0.5,
        ...     frequency=440,
        ...     init_cps=12,
        ...     knum=10,
        ... )
        >>> gendy_3
        Gendy3.ar()

    """

    ampdist = param(1)
    durdist = param(1)
    adparam = param(1)
    ddparam = param(1)
    frequency = param(440)
    ampscale = param(0.5)
    durscale = param(0.5)
    init_cps = param(12)
    knum = param(None)
