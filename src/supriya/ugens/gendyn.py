from typing import Any

from ..enums import CalculationRate
from ..typing import Default
from .core import UGen, param, ugen


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
        <Gendy1.ar()[0]>
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
    knum = param(Default())

    def _postprocess_kwargs(
        self, *, calculation_rate: CalculationRate, **kwargs
    ) -> tuple[CalculationRate, dict[str, Any]]:
        kwargs["knum"] = (
            kwargs["init_cps"]
            if isinstance(kwargs["knum"], Default)
            else kwargs["knum"]
        )
        return calculation_rate, kwargs


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
        <Gendy2.ar()[0]>
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
    knum = param(Default())
    a = param(1.17)
    c = param(0.31)

    def _postprocess_kwargs(
        self, *, calculation_rate: CalculationRate, **kwargs
    ) -> tuple[CalculationRate, dict[str, Any]]:
        kwargs["knum"] = (
            kwargs["init_cps"]
            if isinstance(kwargs["knum"], Default)
            else kwargs["knum"]
        )
        return calculation_rate, kwargs


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
        <Gendy3.ar()[0]>
    """

    ampdist = param(1)
    durdist = param(1)
    adparam = param(1)
    ddparam = param(1)
    frequency = param(440)
    ampscale = param(0.5)
    durscale = param(0.5)
    init_cps = param(12)
    knum = param(Default())

    def _postprocess_kwargs(
        self, *, calculation_rate: CalculationRate, **kwargs
    ) -> tuple[CalculationRate, dict[str, Any]]:
        kwargs["knum"] = (
            kwargs["init_cps"]
            if isinstance(kwargs["knum"], Default)
            else kwargs["knum"]
        )
        return calculation_rate, kwargs
