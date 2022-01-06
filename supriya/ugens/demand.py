import collections
from collections.abc import Sequence

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen, UGen


class DUGen(UGen):
    """
    Abstract base class of demand-rate UGens.
    """

    def __init__(self, **kwargs):
        kwargs["calculation_rate"] = CalculationRate.DEMAND
        UGen.__init__(self, **kwargs)


class Dbrown(DUGen):
    """
    A demand-rate brownian movement generator.

    ::

        >>> dbrown = supriya.ugens.Dbrown.new(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ...     step=0.01,
        ... )
        >>> dbrown
        Dbrown()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0.0), ("maximum", 1.0), ("step", 0.01), ("length", float("inf"))]
    )
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dbufrd(DUGen):
    """
    A buffer-reading demand-rate UGen.

    ::

        >>> dbufrd = supriya.ugens.Dbufrd(
        ...     buffer_id=0,
        ...     loop=1,
        ...     phase=0,
        ... )
        >>> dbufrd
        Dbufrd()

    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", 0), ("phase", 0), ("loop", 1)]
    )
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dbufwr(DUGen):
    """
    A buffer-writing demand-rate UGen.

    ::

        >>> dbufwr = supriya.ugens.Dbufwr(
        ...     buffer_id=0,
        ...     source=0,
        ...     loop=1,
        ...     phase=0,
        ... )
        >>> dbufwr
        Dbufwr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", 0.0), ("buffer_id", 0.0), ("phase", 0.0), ("loop", 1.0)]
    )
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Demand(MultiOutUGen):
    """
    Demands results from demand-rate UGens.

    ::

        >>> source = [
        ...     supriya.ugens.Dseries(),
        ...     supriya.ugens.Dwhite(),
        ... ]
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> demand = supriya.ugens.Demand.ar(
        ...     reset=0,
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> demand
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    _default_channel_count = 1
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict(
        [("trigger", 0), ("reset", 0), ("source", None)]
    )
    _unexpanded_input_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, trigger=None, reset=None, source=None):
        if not isinstance(source, Sequence):
            source = [source]
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            trigger=trigger,
            reset=reset,
            source=source,
            channel_count=len(source),
        )


class DemandEnvGen(UGen):
    """
    A demand rate envelope generator.

    ::

        >>> demand_env_gen = supriya.ugens.DemandEnvGen.ar(
        ...     curve=0,
        ...     done_action=0,
        ...     duration=1,
        ...     gate=1,
        ...     level=1,
        ...     level_bias=0,
        ...     level_scale=1,
        ...     reset=1,
        ...     shape=1,
        ...     time_scale=1,
        ... )
        >>> demand_env_gen
        DemandEnvGen.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("level", None),
            ("duration", None),
            ("shape", 1),
            ("curve", 0),
            ("gate", 1),
            ("reset", 1),
            ("level_scale", 1),
            ("level_bias", 0),
            ("time_scale", 1),
            ("done_action", 0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Dgeom(DUGen):
    """
    A demand-rate geometric series generator.

    ::

        >>> dgeom = supriya.ugens.Dgeom.new(
        ...     grow=2,
        ...     length=float("inf"),
        ...     start=1,
        ... )
        >>> dgeom
        Dgeom()

    """

    _ordered_input_names = collections.OrderedDict(
        [("start", 1), ("grow", 2), ("length", float("inf"))]
    )
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dibrown(DUGen):
    """
    An integer demand-rate brownian movement generator.

    ::

        >>> dibrown = supriya.ugens.Dibrown.new(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ...     step=0.01,
        ... )
        >>> dibrown
        Dibrown()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0), ("maximum", 12), ("step", 1), ("length", float("inf"))]
    )
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Diwhite(DUGen):
    """
    An integer demand-rate white noise random generator.

    ::

        >>> diwhite = supriya.ugens.Diwhite.new(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ... )
        >>> diwhite
        Diwhite()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0), ("maximum", 1), ("length", float("inf"))]
    )
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Drand(DUGen):
    """
    A demand-rate random sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> drand = supriya.ugens.Drand.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> drand
        Drand()

    """

    _ordered_input_names = collections.OrderedDict([("repeats", 1), ("sequence", None)])
    _unexpanded_input_names = ("sequence",)
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dreset(DUGen):
    """
    Resets demand-rate UGens.

    ::

        >>> source = supriya.ugens.Dseries(start=0, step=2)
        >>> dreset = supriya.ugens.Dreset(
        ...     reset=0,
        ...     source=source,
        ... )
        >>> dreset
        Dreset()

    """

    _ordered_input_names = collections.OrderedDict([("source", None), ("reset", 0)])
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dseq(DUGen):
    """
    A demand-rate sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dseq = supriya.ugens.Dseq.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dseq
        Dseq()

    """

    _ordered_input_names = collections.OrderedDict([("repeats", 1), ("sequence", None)])
    _unexpanded_input_names = ("sequence",)
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dser(DUGen):
    """
    A demand-rate sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dser = supriya.ugens.Dser.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dser
        Dser()

    """

    _ordered_input_names = collections.OrderedDict([("repeats", 1), ("sequence", None)])
    _unexpanded_input_names = ("sequence",)
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dseries(DUGen):
    """
    A demand-rate arithmetic series.

    ::

        >>> dseries = supriya.ugens.Dseries.new(
        ...     length=float("inf"),
        ...     start=1,
        ...     step=1,
        ... )
        >>> dseries
        Dseries()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("start", 1), ("step", 1), ("length", float("inf"))]
    )
    _valid_calculation_rates = (CalculationRate.DEMAND,)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, length=float("inf"), start=1, step=1):
        if length is None:
            length = float("inf")
        DUGen.__init__(self, length=length, start=start, step=step)


class Dshuf(DUGen):
    """
    A demand-rate random sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dshuf = supriya.ugens.Dshuf.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dshuf
        Dshuf()

    """

    _ordered_input_names = collections.OrderedDict([("repeats", 1), ("sequence", None)])
    _unexpanded_input_names = ("sequence",)
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dstutter(DUGen):
    """
    A demand-rate input replicator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> dstutter = supriya.ugens.Dstutter.new(
        ...     n=2,
        ...     source=source,
        ... )
        >>> dstutter
        Dstutter()

    """

    _ordered_input_names = collections.OrderedDict([("n", 2.0), ("source", None)])
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dswitch(DUGen):
    """
    A demand-rate generator for embedding different inputs.

    ::

        >>> index = supriya.ugens.Dseq(sequence=[0, 1, 2, 1, 0])
        >>> sequence = (1.0, 2.0, 3.0)
        >>> dswitch = supriya.ugens.Dswitch.new(
        ...     index=index,
        ...     sequence=sequence,
        ... )
        >>> dswitch
        Dswitch()

    """

    _ordered_input_names = collections.OrderedDict(
        [("index", None), ("sequence", None)]
    )
    _unexpanded_input_names = ("sequence",)
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dswitch1(DUGen):
    """
    A demand-rate generator for switching between inputs.

    ::

        >>> index = supriya.ugens.Dseq(sequence=[0, 1, 2, 1, 0])
        >>> sequence = (1.0, 2.0, 3.0)
        >>> dswitch_1 = supriya.ugens.Dswitch1.new(
        ...     index=index,
        ...     sequence=sequence,
        ... )
        >>> dswitch_1
        Dswitch1()

    """

    _ordered_input_names = collections.OrderedDict(
        [("index", None), ("sequence", None)]
    )
    _unexpanded_input_names = ("sequence",)
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dunique(DUGen):
    """
    Returns the same unique series of values for several demand streams.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> dunique = supriya.ugens.Dunique.new(
        ...     max_buffer_size=1024,
        ...     protected=True,
        ...     source=source,
        ... )
        >>> dunique
        Dunique()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("max_buffer_size", 1024), ("protected", True)]
    )
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Duty(UGen):
    """
    A value is demanded of each UGen in the list and output according to a stream of duration values.

    ::

        >>> duty = supriya.ugens.Duty.kr(
        ...     done_action=0,
        ...     duration=supriya.ugens.Drand(
        ...         sequence=[0.01, 0.2, 0.4],
        ...         repeats=2,
        ...     ),
        ...     reset=0,
        ...     level=supriya.ugens.Dseq(
        ...         sequence=[204, 400, 201, 502, 300, 200],
        ...         repeats=2,
        ...     ),
        ... )
        >>> duty
        Duty.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("duration", 1.0), ("reset", 0.0), ("level", 1.0), ("done_action", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Dwhite(DUGen):
    """
    A demand-rate white noise random generator.

    ::

        >>> dwhite = supriya.ugens.Dwhite.new(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ... )
        >>> dwhite
        Dwhite()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0.0), ("maximum", 1.0), ("length", float("inf"))]
    )
    _valid_calculation_rates = (CalculationRate.DEMAND,)


class Dwrand(DUGen):
    """
    A demand-rate weighted random sequence generator.

    ::

        >>> sequence = [0, 1, 2, 7]
        >>> weights = [0.4, 0.4, 0.1, 0.1]
        >>> dwrand = supriya.ugens.Dwrand.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     weights=weights,
        ... )
        >>> dwrand
        Dwrand()

    """

    ### CLASS VARIABLES ###

    # TODO: We should not include length in the generated methods

    _ordered_input_names = collections.OrderedDict(
        [("repeats", 1), ("length", None), ("weights", None), ("sequence", None)]
    )
    _unexpanded_input_names = ("weights", "sequence")
    _valid_calculation_rates = (CalculationRate.DEMAND,)

    ### INITIALIZER ###

    def __init__(self, repeats=1, sequence=None, weights=None, **kwargs):
        if not isinstance(sequence, Sequence):
            sequence = [sequence]
        sequence = tuple(float(_) for _ in sequence)
        if not isinstance(weights, Sequence):
            weights = [weights]
        weights = tuple(float(_) for _ in weights)
        weights = weights[: len(sequence)]
        weights += (0.0,) * (len(sequence) - len(weights))
        DUGen.__init__(
            self,
            repeats=repeats,
            length=len(sequence),
            sequence=sequence,
            weights=weights,
        )


class Dxrand(DUGen):
    """
    A demand-rate random sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dxrand = supriya.ugens.Dxrand.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dxrand
        Dxrand()

    """

    _ordered_input_names = collections.OrderedDict([("repeats", 1), ("sequence", None)])
    _unexpanded_input_names = ("sequence",)
    _valid_calculation_rates = (CalculationRate.DEMAND,)
