import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class CuspL(UGen):
    """
    A linear-interpolating cusp map chaotic generator.

    ::

        >>> cusp_l = supriya.ugens.CuspL.ar(
        ...     a=1,
        ...     b=1.9,
        ...     frequency=22050,
        ...     xi=0,
        ... )
        >>> cusp_l
        CuspL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.0), ("b", 1.9), ("xi", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class CuspN(UGen):
    """
    A non-interpolating cusp map chaotic generator.

    ::

        >>> cusp_n = supriya.ugens.CuspN.ar(
        ...     a=1,
        ...     b=1.9,
        ...     frequency=22050,
        ...     xi=0,
        ... )
        >>> cusp_n
        CuspN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.0), ("b", 1.9), ("xi", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class FBSineC(UGen):
    """
    A cubic-interpolating feedback sine with chaotic phase indexing.

    ::

        >>> fbsine_c = supriya.ugens.FBSineC.ar(
        ...     a=1.1,
        ...     c=0.5,
        ...     fb=0.1,
        ...     frequency=22050,
        ...     im=1,
        ...     xi=0.1,
        ...     yi=0.1,
        ... )
        >>> fbsine_c
        FBSineC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("frequency", 22050),
            ("im", 1.0),
            ("fb", 0.1),
            ("a", 1.1),
            ("c", 0.5),
            ("xi", 0.1),
            ("yi", 0.1),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class FBSineL(UGen):
    """
    A linear-interpolating feedback sine with chaotic phase indexing.

    ::

        >>> fbsine_l = supriya.ugens.FBSineL.ar(
        ...     a=1.1,
        ...     c=0.5,
        ...     fb=0.1,
        ...     frequency=22050,
        ...     im=1,
        ...     xi=0.1,
        ...     yi=0.1,
        ... )
        >>> fbsine_l
        FBSineL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("frequency", 22050),
            ("im", 1.0),
            ("fb", 0.1),
            ("a", 1.1),
            ("c", 0.5),
            ("xi", 0.1),
            ("yi", 0.1),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class FBSineN(UGen):
    """
    A non-interpolating feedback sine with chaotic phase indexing.

    ::

        >>> fbsine_n = supriya.ugens.FBSineN.ar(
        ...     a=1.1,
        ...     c=0.5,
        ...     fb=0.1,
        ...     frequency=22050,
        ...     im=1,
        ...     xi=0.1,
        ...     yi=0.1,
        ... )
        >>> fbsine_n
        FBSineN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("frequency", 22050),
            ("im", 1.0),
            ("fb", 0.1),
            ("a", 1.1),
            ("c", 0.5),
            ("xi", 0.1),
            ("yi", 0.1),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class GbmanL(UGen):
    """
    A non-interpolating gingerbreadman map chaotic generator.

    ::

        >>> gbman_l = supriya.ugens.GbmanL.ar(
        ...     frequency=22050,
        ...     xi=1.2,
        ...     yi=2.1,
        ... )
        >>> gbman_l
        GbmanL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("xi", 1.2), ("yi", 2.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class GbmanN(UGen):
    """
    A non-interpolating gingerbreadman map chaotic generator.

    ::

        >>> gbman_n = supriya.ugens.GbmanN.ar(
        ...     frequency=22050,
        ...     xi=1.2,
        ...     yi=2.1,
        ... )
        >>> gbman_n
        GbmanN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("xi", 1.2), ("yi", 2.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class HenonC(UGen):
    """
    A cubic-interpolating henon map chaotic generator.

    ::

        >>> henon_c = supriya.ugens.HenonC.ar(
        ...     a=1.4,
        ...     b=0.3,
        ...     frequency=22050,
        ...     x_0=0,
        ...     x_1=0,
        ... )
        >>> henon_c
        HenonC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.4), ("b", 0.3), ("x_0", 0), ("x_1", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class HenonL(UGen):
    """
    A linear-interpolating henon map chaotic generator.

    ::

        >>> henon_l = supriya.ugens.HenonL.ar(
        ...     a=1.4,
        ...     b=0.3,
        ...     frequency=22050,
        ...     x_0=0,
        ...     x_1=0,
        ... )
        >>> henon_l
        HenonL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.4), ("b", 0.3), ("x_0", 0), ("x_1", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class HenonN(UGen):
    """
    A non-interpolating henon map chaotic generator.

    ::

        >>> henon_n = supriya.ugens.HenonN.ar(
        ...     a=1.4,
        ...     b=0.3,
        ...     frequency=22050,
        ...     x_0=0,
        ...     x_1=0,
        ... )
        >>> henon_n
        HenonN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.4), ("b", 0.3), ("x_0", 0), ("x_1", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class LatoocarfianC(UGen):
    """
    A cubic-interpolating Latoocarfian chaotic generator.

    ::

        >>> latoocarfian_c = supriya.ugens.LatoocarfianC.ar(
        ...     a=1,
        ...     b=3,
        ...     c=0.5,
        ...     d=0.5,
        ...     frequency=22050,
        ...     xi=0.5,
        ...     yi=0.5,
        ... )
        >>> latoocarfian_c
        LatoocarfianC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("frequency", 22050),
            ("a", 1),
            ("b", 3),
            ("c", 0.5),
            ("d", 0.5),
            ("xi", 0.5),
            ("yi", 0.5),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class LatoocarfianL(UGen):
    """
    A linear-interpolating Latoocarfian chaotic generator.

    ::

        >>> latoocarfian_l = supriya.ugens.LatoocarfianL.ar(
        ...     a=1,
        ...     b=3,
        ...     c=0.5,
        ...     d=0.5,
        ...     frequency=22050,
        ...     xi=0.5,
        ...     yi=0.5,
        ... )
        >>> latoocarfian_l
        LatoocarfianL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("frequency", 22050),
            ("a", 1),
            ("b", 3),
            ("c", 0.5),
            ("d", 0.5),
            ("xi", 0.5),
            ("yi", 0.5),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class LatoocarfianN(UGen):
    """
    A non-interpolating Latoocarfian chaotic generator.

    ::

        >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
        ...     a=1,
        ...     b=3,
        ...     c=0.5,
        ...     d=0.5,
        ...     frequency=22050,
        ...     xi=0.5,
        ...     yi=0.5,
        ... )
        >>> latoocarfian_n
        LatoocarfianN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("frequency", 22050),
            ("a", 1),
            ("b", 3),
            ("c", 0.5),
            ("d", 0.5),
            ("xi", 0.5),
            ("yi", 0.5),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class LinCongC(UGen):
    """
    A cubic-interpolating linear congruential chaotic generator.

    ::

        >>> lin_cong_c = supriya.ugens.LinCongC.ar(
        ...     a=1.1,
        ...     c=0.13,
        ...     frequency=22050,
        ...     m=1,
        ...     xi=0,
        ... )
        >>> lin_cong_c
        LinCongC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.1), ("c", 0.13), ("m", 1), ("xi", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class LinCongL(UGen):
    """
    A linear-interpolating linear congruential chaotic generator.

    ::

        >>> lin_cong_l = supriya.ugens.LinCongL.ar(
        ...     a=1.1,
        ...     c=0.13,
        ...     frequency=22050,
        ...     m=1,
        ...     xi=0,
        ... )
        >>> lin_cong_l
        LinCongL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.1), ("c", 0.13), ("m", 1), ("xi", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class LinCongN(UGen):
    """
    A non-interpolating linear congruential chaotic generator.

    ::

        >>> lin_cong_n = supriya.ugens.LinCongN.ar(
        ...     a=1.1,
        ...     c=0.13,
        ...     frequency=22050,
        ...     m=1,
        ...     xi=0,
        ... )
        >>> lin_cong_n
        LinCongN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.1), ("c", 0.13), ("m", 1), ("xi", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class LorenzL(UGen):
    """
    A linear-interpolating Lorenz chaotic generator.

    ::

        >>> lorenz_l = supriya.ugens.LorenzL.ar(
        ...     b=2.667,
        ...     frequency=22050,
        ...     h=0.05,
        ...     r=28,
        ...     s=10,
        ...     xi=0.1,
        ...     yi=0,
        ...     zi=0,
        ... )
        >>> lorenz_l
        LorenzL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("frequency", 22050),
            ("s", 10),
            ("r", 28),
            ("b", 2.667),
            ("h", 0.05),
            ("xi", 0.1),
            ("yi", 0),
            ("zi", 0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class QuadC(UGen):
    """
    A cubic-interpolating general quadratic map chaotic generator.

    ::

        >>> quad_c = supriya.ugens.QuadC.ar(
        ...     a=1,
        ...     b=-1,
        ...     c=-0.75,
        ...     frequency=22050,
        ...     xi=0,
        ... )
        >>> quad_c
        QuadC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1), ("b", -1), ("c", -0.75), ("xi", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class QuadL(UGen):
    """
    A linear-interpolating general quadratic map chaotic generator.

    ::

        >>> quad_l = supriya.ugens.QuadL.ar(
        ...     a=1,
        ...     b=-1,
        ...     c=-0.75,
        ...     frequency=22050,
        ...     xi=0,
        ... )
        >>> quad_l
        QuadL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1), ("b", -1), ("c", -0.75), ("xi", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class QuadN(UGen):
    """
    A non-interpolating general quadratic map chaotic generator.

    ::

        >>> quad_n = supriya.ugens.QuadN.ar(
        ...     a=1,
        ...     b=-1,
        ...     c=-0.75,
        ...     frequency=22050,
        ...     xi=0,
        ... )
        >>> quad_n
        QuadN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1), ("b", -1), ("c", -0.75), ("xi", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class StandardL(UGen):
    """
    A linear-interpolating standard map chaotic generator.

    ::

        >>> standard_l = supriya.ugens.StandardL.ar(
        ...     frequency=22050,
        ...     k=1,
        ...     xi=0.5,
        ...     yi=0,
        ... )
        >>> standard_l
        StandardL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("k", 1), ("xi", 0.5), ("yi", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class StandardN(UGen):
    """
    A non-interpolating standard map chaotic generator.

    ::

        >>> standard_n = supriya.ugens.StandardN.ar(
        ...     frequency=22050,
        ...     k=1,
        ...     xi=0.5,
        ...     yi=0,
        ... )
        >>> standard_n
        StandardN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("k", 1), ("xi", 0.5), ("yi", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)
