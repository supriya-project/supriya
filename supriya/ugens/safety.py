from .bases import UGen, param, ugen


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
        CheckBadValues.ar()

    """

    source = param(None)
    ugen_id = param(0)
    post_mode = param(2)

    def __init__(self, calculation_rate=None, ugen_id=0, post_mode=2, source=None):
        assert int(post_mode) in (0, 1, 2)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            ugen_id=ugen_id,
            post_mode=post_mode,
            source=source,
        )


@ugen(ar=True, kr=True)
class Sanitize(UGen):
    """
    Remove infinity, NaN, and denormals.
    """

    source = param(None)
    replace = param(0.0)
