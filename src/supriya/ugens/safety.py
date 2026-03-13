from typing import Any

from ..enums import CalculationRate
from .core import UGen, param, ugen


@ugen(ar=True, kr=True)
class CheckBadValues(UGen):
    """
    Tests for infinity, not-a-number, and denormals.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> ugen_id = 23
        >>> post_mode = 0
        >>> check_bad_values = supriya.ugens.CheckBadValues.ar(
        ...     source=source,
        ...     ugen_id=ugen_id,
        ...     post_mode=post_mode,
        ... )
        >>> check_bad_values
        <CheckBadValues.ar()[0]>
    """

    source = param()
    ugen_id = param(0)
    post_mode = param(2)

    def _postprocess_kwargs(
        self,
        *,
        calculation_rate: CalculationRate,
        **kwargs,
    ) -> tuple[CalculationRate, dict[str, Any]]:
        if kwargs["post_mode"] not in (0, 1, 2):
            raise ValueError(f"Invalid post mode: {kwargs['post_mode']}")
        return calculation_rate, kwargs


@ugen(ar=True, kr=True)
class Sanitize(UGen):
    """
    Remove infinity, NaN, and denormals.
    """

    source = param()
    replace = param(0.0)
