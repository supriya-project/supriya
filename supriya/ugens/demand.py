from collections.abc import Sequence
from typing import Any

from ..enums import CalculationRate
from .core import UGen, param, ugen


@ugen(dr=True)
class Dbrown(UGen):
    """
    A demand-rate brownian movement generator.

    ::

        >>> dbrown = supriya.ugens.Dbrown.dr(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ...     step=0.01,
        ... )
        >>> dbrown
        <Dbrown.dr()[0]>
    """

    minimum = param(0.0)
    maximum = param(1.0)
    step = param(0.01)
    length = param(float("inf"))


@ugen(dr=True)
class Dbufrd(UGen):
    """
    A buffer-reading demand-rate UGen.

    ::

        >>> dbufrd = supriya.ugens.Dbufrd.dr(
        ...     buffer_id=0,
        ...     loop=1,
        ...     phase=0,
        ... )
        >>> dbufrd
        <Dbufrd.dr()[0]>
    """

    buffer_id = param(0)
    phase = param(0)
    loop = param(1)


@ugen(dr=True)
class Dbufwr(UGen):
    """
    A buffer-writing demand-rate UGen.

    ::

        >>> dbufwr = supriya.ugens.Dbufwr.dr(
        ...     buffer_id=0,
        ...     source=0,
        ...     loop=1,
        ...     phase=0,
        ... )
        >>> dbufwr
        <Dbufwr.dr()[0]>
    """

    source = param(0.0)
    buffer_id = param(0.0)
    phase = param(0.0)
    loop = param(1.0)


@ugen(ar=True, kr=True)
class Demand(UGen):
    """
    Demands results from demand-rate UGens.

    ::

        >>> source = [
        ...     supriya.ugens.Dseries.dr(),
        ...     supriya.ugens.Dwhite.dr(),
        ... ]
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> demand = supriya.ugens.Demand.ar(
        ...     reset=0,
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> demand
        <Demand.ar()>
    """

    trigger = param(0)
    reset = param(0)
    source = param(unexpanded=True)

    def _postprocess_kwargs(
        self,
        *,
        calculation_rate: CalculationRate,
        **kwargs,
    ) -> tuple[CalculationRate, dict[str, Any]]:
        if not isinstance(source := kwargs["source"], Sequence):
            kwargs["source"] = [source]
        self._channel_count = len(kwargs["source"])
        return calculation_rate, kwargs


@ugen(ar=True, kr=True)
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
        <DemandEnvGen.ar()[0]>
    """

    level = param()
    duration = param()
    shape = param(1)
    curve = param(0)
    gate = param(1)
    reset = param(1)
    level_scale = param(1)
    level_bias = param(0)
    time_scale = param(1)
    done_action = param(0)


@ugen(dr=True)
class Dgeom(UGen):
    """
    A demand-rate geometric series generator.

    ::

        >>> dgeom = supriya.ugens.Dgeom.dr(
        ...     grow=2,
        ...     length=float("inf"),
        ...     start=1,
        ... )
        >>> dgeom
        <Dgeom.dr()[0]>
    """

    start = param(1)
    grow = param(2)
    length = param(float("inf"))


@ugen(dr=True)
class Dibrown(UGen):
    """
    An integer demand-rate brownian movement generator.

    ::

        >>> dibrown = supriya.ugens.Dibrown.dr(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ...     step=0.01,
        ... )
        >>> dibrown
        <Dibrown.dr()[0]>
    """

    minimum = param(0)
    maximum = param(12)
    step = param(1)
    length = param(float("inf"))


@ugen(dr=True)
class Diwhite(UGen):
    """
    An integer demand-rate white noise random generator.

    ::

        >>> diwhite = supriya.ugens.Diwhite.dr(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ... )
        >>> diwhite
        <Diwhite.dr()[0]>
    """

    minimum = param(0)
    maximum = param(1)
    length = param(float("inf"))


@ugen(dr=True)
class Drand(UGen):
    """
    A demand-rate random sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> drand = supriya.ugens.Drand.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> drand
        <Drand.dr()[0]>
    """

    repeats = param(1)
    sequence = param(unexpanded=True)


@ugen(dr=True)
class Dreset(UGen):
    """
    Resets demand-rate UGens.

    ::

        >>> source = supriya.ugens.Dseries.dr(start=0, step=2)
        >>> dreset = supriya.ugens.Dreset.dr(
        ...     reset=0,
        ...     source=source,
        ... )
        >>> dreset
        <Dreset.dr()[0]>
    """

    source = param()
    reset = param(0)


@ugen(dr=True)
class Dseq(UGen):
    """
    A demand-rate sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dseq = supriya.ugens.Dseq.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dseq
        <Dseq.dr()[0]>
    """

    repeats = param(1)
    sequence = param(unexpanded=True)


@ugen(dr=True)
class Dser(UGen):
    """
    A demand-rate sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dser = supriya.ugens.Dser.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dser
        <Dser.dr()[0]>
    """

    repeats = param(1)
    sequence = param(unexpanded=True)


@ugen(dr=True)
class Dseries(UGen):
    """
    A demand-rate arithmetic series.

    ::

        >>> dseries = supriya.ugens.Dseries.dr(
        ...     length=float("inf"),
        ...     start=1,
        ...     step=1,
        ... )
        >>> dseries
        <Dseries.dr()[0]>
    """

    length = param(float("inf"))
    start = param(1)
    step = param(1)


@ugen(dr=True)
class Dshuf(UGen):
    """
    A demand-rate random sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dshuf = supriya.ugens.Dshuf.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dshuf
        <Dshuf.dr()[0]>
    """

    repeats = param(1)
    sequence = param(unexpanded=True)


@ugen(dr=True)
class Dstutter(UGen):
    """
    A demand-rate input replicator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> dstutter = supriya.ugens.Dstutter.dr(
        ...     n=2,
        ...     source=source,
        ... )
        >>> dstutter
        <Dstutter.dr()[0]>
    """

    n = param(2)
    source = param()


@ugen(dr=True)
class Dswitch(UGen):
    """
    A demand-rate generator for embedding different inputs.

    ::

        >>> index = supriya.ugens.Dseq.dr(sequence=[0, 1, 2, 1, 0])
        >>> sequence = (1.0, 2.0, 3.0)
        >>> dswitch = supriya.ugens.Dswitch.dr(
        ...     index_=index,
        ...     sequence=sequence,
        ... )
        >>> dswitch
        <Dswitch.dr()[0]>
    """

    index_ = param()
    sequence = param(unexpanded=True)


@ugen(dr=True)
class Dswitch1(UGen):
    """
    A demand-rate generator for switching between inputs.

    ::

        >>> index = supriya.ugens.Dseq.dr(sequence=[0, 1, 2, 1, 0])
        >>> sequence = (1.0, 2.0, 3.0)
        >>> dswitch_1 = supriya.ugens.Dswitch1.dr(
        ...     index_=index,
        ...     sequence=sequence,
        ... )
        >>> dswitch_1
        <Dswitch1.dr()[0]>
    """

    index_ = param()
    sequence = param(unexpanded=True)


@ugen(dr=True)
class Dunique(UGen):
    """
    Returns the same unique series of values for several demand streams.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> dunique = supriya.ugens.Dunique.dr(
        ...     max_buffer_size=1024,
        ...     protected=True,
        ...     source=source,
        ... )
        >>> dunique
        <Dunique.dr()[0]>
    """

    source = param()
    max_buffer_size = param(1024)
    protected = param(True)


@ugen(ar=True, kr=True)
class Duty(UGen):
    """
    A value is demanded of each UGen in the list and output according to a stream of duration values.

    ::

        >>> duty = supriya.ugens.Duty.kr(
        ...     done_action=0,
        ...     duration=supriya.ugens.Drand.dr(
        ...         sequence=[0.01, 0.2, 0.4],
        ...         repeats=2,
        ...     ),
        ...     reset=0,
        ...     level=supriya.ugens.Dseq.dr(
        ...         sequence=[204, 400, 201, 502, 300, 200],
        ...         repeats=2,
        ...     ),
        ... )
        >>> duty
        <Duty.kr()[0]>
    """

    duration = param(1.0)
    reset = param(0.0)
    level = param(1.0)
    done_action = param(0.0)


@ugen(dr=True)
class Dwhite(UGen):
    """
    A demand-rate white noise random generator.

    ::

        >>> dwhite = supriya.ugens.Dwhite.dr(
        ...     length=float("inf"),
        ...     maximum=1,
        ...     minimum=0,
        ... )
        >>> dwhite
        <Dwhite.dr()[0]>
    """

    minimum = param(0.0)
    maximum = param(0.0)
    length = param(float("inf"))


@ugen(dr=True)
class Dwrand(UGen):
    """
    A demand-rate weighted random sequence generator.

    ::

        >>> sequence = [0, 1, 2, 7]
        >>> weights = [0.4, 0.4, 0.1, 0.1]
        >>> dwrand = supriya.ugens.Dwrand.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     weights=weights,
        ... )
        >>> dwrand
        <Dwrand.dr()[0]>
    """

    repeats = param(1)
    length = param()
    weights = param(unexpanded=True)
    sequence = param(unexpanded=True)

    @classmethod
    def dr(cls, repeats=1, sequence=None, weights=None):
        if not isinstance(sequence, Sequence):
            sequence = [sequence]
        sequence = tuple(float(_) for _ in sequence)
        if not isinstance(weights, Sequence):
            weights = [weights]
        weights = tuple(float(_) for _ in weights)
        weights = weights[: len(sequence)]
        weights += (0.0,) * (len(sequence) - len(weights))
        return cls._new_expanded(
            calculation_rate=CalculationRate.DEMAND,
            repeats=repeats,
            length=len(sequence),
            sequence=sequence,
            weights=weights,
        )


@ugen(dr=True)
class Dxrand(UGen):
    """
    A demand-rate random sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dxrand = supriya.ugens.Dxrand.dr(
        ...     repeats=1,
        ...     sequence=sequence,
        ... )
        >>> dxrand
        <Dxrand.dr()[0]>
    """

    repeats = param(1)
    sequence = param(unexpanded=True)
