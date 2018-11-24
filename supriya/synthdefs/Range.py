import collections

from supriya.system.SupriyaObject import SupriyaObject


class Range(SupriyaObject):
    """
    A range.

    ::

        >>> supriya.synthdefs.Range(-1., 1.)
        Range(
            maximum=1.0,
            minimum=-1.0,
            )

    ::

        >>> supriya.synthdefs.Range(minimum=0.)
        Range(
            maximum=inf,
            minimum=0.0,
            )

    ::

        >>> supriya.synthdefs.Range()
        Range(
            maximum=inf,
            minimum=-inf,
            )

    ::

        >>> supriya.synthdefs.Range((0.1, 0.9))
        Range(
            maximum=0.9,
            minimum=0.1,
            )

    ::

        >>> supriya.synthdefs.Range(supriya.synthdefs.Range(-3, 3))
        Range(
            maximum=3.0,
            minimum=-3.0,
            )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Main Classes"

    __slots__ = ("_minimum", "_maximum")

    ### INITIALIZER ###

    def __init__(self, minimum=None, maximum=None):
        if (
            isinstance(minimum, collections.Sequence)
            and maximum is None
            and len(minimum) == 2
        ):
            minimum, maximum = minimum
        elif isinstance(minimum, type(self)):
            minimum, maximum = minimum.minimum, minimum.maximum
        if minimum is None:
            minimum = float("-inf")
        if not isinstance(minimum, (float, int)):
            raise ValueError(minimum)
        minimum = float(minimum)
        if maximum is None:
            maximum = float("inf")
        if not isinstance(maximum, (float, int)):
            raise ValueError(maximum)
        maximum = float(maximum)
        assert minimum <= maximum
        self._minimum = minimum
        self._maximum = maximum

    ### PUBLIC METHODS ###

    @staticmethod
    def scale(value, input_range, output_range, exponent=1.0):
        """
        Scales `value` from `input_range` to `output_range`.

        Curve value exponentially by `exponent`.

        ::

            >>> input_range = supriya.synthdefs.Range(0., 10.)
            >>> output_range = supriya.synthdefs.Range(-2.5, 2.5)

        ::

            >>> supriya.synthdefs.Range.scale(0., input_range, output_range)
            -2.5

        ::

            >>> supriya.synthdefs.Range.scale(5., input_range, output_range)
            0.0

        ::

            >>> supriya.synthdefs.Range.scale(5., input_range, output_range, 2.)
            -1.25

        ::

            >>> supriya.synthdefs.Range.scale(5., input_range, output_range, 0.5)
            1.0355...

        Returns float.
        """
        value = (value - input_range.minimum) / input_range.width
        if exponent != 1:
            value = pow(value, exponent)
        value = (value * output_range.width) + output_range.minimum
        return value

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        return self._maximum

    @property
    def minimum(self):
        return self._minimum

    @property
    def width(self):
        return self._maximum - self._minimum
