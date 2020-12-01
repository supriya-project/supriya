import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


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

    _ordered_input_names = collections.OrderedDict(
        [
            ("ampdist", 1),
            ("durdist", 1),
            ("adparam", 1),
            ("ddparam", 1),
            ("minfrequency", 440),
            ("maxfrequency", 660),
            ("ampscale", 0.5),
            ("durscale", 0.5),
            ("init_cps", 12),
            ("knum", None),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

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

    _ordered_input_names = collections.OrderedDict(
        [
            ("ampdist", 1),
            ("durdist", 1),
            ("adparam", 1),
            ("ddparam", 1),
            ("minfrequency", 440),
            ("maxfrequency", 660),
            ("ampscale", 0.5),
            ("durscale", 0.5),
            ("init_cps", 12),
            ("knum", None),
            ("a", 1.17),
            ("c", 0.31),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


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

    _ordered_input_names = collections.OrderedDict(
        [
            ("ampdist", 1),
            ("durdist", 1),
            ("adparam", 1),
            ("ddparam", 1),
            ("frequency", 440),
            ("ampscale", 0.5),
            ("durscale", 0.5),
            ("init_cps", 12),
            ("knum", None),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
