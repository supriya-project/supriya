import math
from typing import TYPE_CHECKING, Sequence, SupportsFloat, cast

from .. import utils
from ..enums import EnvelopeShape
from ..utils import expand_deep
from .core import OutputProxy, UGen, UGenOperable, UGenVector, param, ugen

if TYPE_CHECKING:
    import numpy


class Envelope:
    """
    An envelope.

    ::

        >>> from supriya.ugens import Envelope
        >>> envelope = Envelope()

    ::

        >>> list(envelope.serialize())
        [<0.0>, <2.0>, <-99.0>, <-99.0>, <1.0>, <1.0>, <1.0>, <0.0>, <0.0>, <1.0>, <1.0>, <0.0>]
    """

    def __init__(
        self,
        amplitudes: Sequence[UGenOperable | float] = (0, 1, 0),
        durations: Sequence[UGenOperable | float] = (1, 1),
        curves: Sequence[EnvelopeShape | UGenOperable | float | str | None] = (
            EnvelopeShape.LINEAR,
            EnvelopeShape.LINEAR,
        ),
        release_node: int | None = None,
        loop_node: int | None = None,
        offset: UGenOperable | float = 0.0,
    ) -> None:
        if len(amplitudes) <= 1:
            raise ValueError(amplitudes)
        if not (len(durations) == (len(amplitudes) - 1)):
            raise ValueError(durations, amplitudes)
        if isinstance(curves, (int, float, str, EnvelopeShape, UGenOperable)):
            curves = [curves]
        elif curves is None:
            curves = []
        self._release_node = release_node
        self._loop_node = loop_node
        self._offset = offset
        self._initial_amplitude: UGenOperable | float = self._flatten(
            float(amplitudes[0])
            if not isinstance(amplitudes[0], UGenOperable)
            else amplitudes[0]
        )
        self._amplitudes: tuple[UGenOperable | float, ...] = tuple(
            self._flatten(
                float(amplitude)
                if not isinstance(amplitude, UGenOperable)
                else amplitude
            )
            for amplitude in amplitudes[1:]
        )
        self._durations: tuple[UGenOperable | float, ...] = tuple(
            self._flatten(
                float(duration) if not isinstance(duration, UGenOperable) else duration
            )
            for duration in durations
        )
        curves_: list[EnvelopeShape | UGenOperable | float] = []
        for x in curves:
            if isinstance(x, (EnvelopeShape, UGenOperable)):
                curves_.append(self._flatten(x))
            elif isinstance(x, str) or x is None:
                curves_.append(EnvelopeShape.from_expr(x))
            else:
                curves_.append(float(x))
        self._curves: tuple[EnvelopeShape | UGenOperable | float, ...] = tuple(curves_)
        self._envelope_segments = tuple(
            utils.zip_cycled(self._amplitudes, self._durations, self._curves)
        )

    def __plot__(self) -> tuple["numpy.ndarray", float]:
        import numpy

        duration = sum(self.durations)
        if not isinstance(duration, float):
            raise ValueError(duration)
        array = self.to_array(length=int(44100 * duration))
        return numpy.array([array, [0.0] * len(array)]), 44100.0

    @staticmethod
    def _flatten(item: UGenOperable | float) -> UGenOperable | float:
        if isinstance(item, (float, int)):
            return item
        elif isinstance(item, OutputProxy):
            return item
        elif isinstance(item, UGen) and len(item) == 1:
            return item[0]
        return item

    @classmethod
    def adsr(
        cls,
        attack_time=0.01,
        decay_time=0.3,
        sustain=0.5,
        release_time=1.0,
        peak=1.0,
        curve=-4.0,
        bias=0.0,
    ) -> "Envelope":
        amplitudes = [x + bias for x in [0, peak, peak * sustain, 0]]
        durations = [attack_time, decay_time, release_time]
        curves = [curve]
        release_node = 2
        return Envelope(
            amplitudes=amplitudes,
            durations=durations,
            curves=curves,
            release_node=release_node,
        )

    @classmethod
    def asr(
        cls, attack_time=0.01, sustain=1.0, release_time=1.0, curve=-4.0
    ) -> "Envelope":
        amplitudes = [0, sustain, 0]
        durations = [attack_time, release_time]
        curves = [curve]
        release_node = 1
        return Envelope(
            amplitudes=amplitudes,
            durations=durations,
            curves=curves,
            release_node=release_node,
        )

    def at(self, time: float) -> float:
        PI = math.pi
        PI2 = PI / 2.0
        start_time = 0.0
        start_amplitude = self._initial_amplitude
        if not isinstance(start_amplitude, float):
            raise ValueError(start_amplitude)
        if time < start_time:
            return start_amplitude
        for stop_amplitude, duration, curve in self._envelope_segments:
            if not isinstance(stop_amplitude, float):
                raise ValueError(stop_amplitude)
            if not isinstance(duration, float):
                raise ValueError
            if not isinstance(curve, (EnvelopeShape, float)):
                raise ValueError(curve)
            stop_time = start_time + duration
            if time < stop_time:
                position = (time - start_time) / duration
                if isinstance(curve, float):
                    if abs(curve) < 0.0001:
                        return (
                            position * (stop_amplitude - start_amplitude)
                            + start_amplitude
                        )
                    denominator = 1.0 - math.exp(curve)
                    numerator = 1.0 - math.exp(position * curve)
                    return start_amplitude + (stop_amplitude - start_amplitude) * (
                        numerator / denominator
                    )
                elif curve is EnvelopeShape.STEP:
                    return stop_amplitude
                elif curve is EnvelopeShape.HOLD:
                    return start_amplitude
                elif curve is EnvelopeShape.LINEAR:
                    return (
                        position * (stop_amplitude - start_amplitude) + start_amplitude
                    )
                elif curve is EnvelopeShape.EXPONENTIAL:
                    return start_amplitude * math.pow(
                        stop_amplitude / start_amplitude, position
                    )
                elif curve is EnvelopeShape.SINE:
                    return start_amplitude + (stop_amplitude - start_amplitude) * (
                        -math.cos(PI * position) * 0.5 + 0.5
                    )
                elif curve is EnvelopeShape.WELCH:
                    if start_amplitude < stop_amplitude:
                        return start_amplitude + (
                            stop_amplitude - start_amplitude
                        ) * math.sin(PI2 * position)
                    return stop_amplitude - (
                        stop_amplitude - start_amplitude
                    ) * math.sin(PI2 - PI2 * position)
                elif curve is EnvelopeShape.SQUARED:
                    start_amplitude_sqrt = math.sqrt(start_amplitude)
                    stop_amplitude_sqrt = math.sqrt(stop_amplitude)
                    amplitude_sqrt = (
                        position * (stop_amplitude_sqrt - start_amplitude_sqrt)
                        + start_amplitude_sqrt
                    )
                    return amplitude_sqrt * amplitude_sqrt
                elif curve is EnvelopeShape.CUBED:
                    start_amplitude_cbrt = pow(start_amplitude, 0.3333333)
                    stop_amplitude_cbrt = pow(stop_amplitude, 0.3333333)
                    cbrt = (
                        position * (stop_amplitude_cbrt - start_amplitude_cbrt)
                        + start_amplitude_cbrt
                    )
                    return cbrt * cbrt * cbrt
                break
            start_time = stop_time
            start_amplitude = stop_amplitude
        return start_amplitude

    @classmethod
    def from_segments(
        cls,
        initial_amplitude=0,
        segments=None,
        release_node=None,
        loop_node=None,
        offset=None,
    ) -> "Envelope":
        amplitudes = [initial_amplitude]
        durations = []
        curves = []
        for amplitude, duration, curve in segments:
            amplitudes.append(amplitude)
            durations.append(duration)
            curves.append(curve)
        return cls(
            amplitudes=amplitudes,
            durations=durations,
            curves=curves,
            release_node=release_node,
            loop_node=loop_node,
            offset=offset,
        )

    @classmethod
    def percussive(
        cls,
        attack_time: UGenOperable | float = 0.01,
        release_time: UGenOperable | float = 1.0,
        amplitude: UGenOperable | float = 1.0,
        curve: EnvelopeShape | UGenOperable | float | str = -4.0,
    ) -> "Envelope":
        """
        Make a percussion envelope.

        ::

            >>> from supriya.ugens import Envelope
            >>> envelope = Envelope.percussive()

        ::

            >>> list(envelope.serialize())
            [<0.0>, <2.0>, <-99.0>, <-99.0>, <1.0>, <0.01>, <5.0>, <-4.0>, <0.0>, <1.0>, <5.0>, <-4.0>]
        """
        amplitudes = [0, amplitude, 0]
        durations = [attack_time, release_time]
        curves = [curve]
        return Envelope(amplitudes=amplitudes, durations=durations, curves=curves)

    @classmethod
    def linen(
        cls, attack_time=0.01, sustain_time=1.0, release_time=1.0, level=1.0, curve=1
    ) -> "Envelope":
        amplitudes = [0, level, level, 0]
        durations = [attack_time, sustain_time, release_time]
        curves = [curve]
        return Envelope(amplitudes=amplitudes, durations=durations, curves=curves)

    def serialize(self, **kwargs) -> UGenVector:
        result: list[UGenOperable | float] = []
        result.append(self.initial_amplitude)
        result.append(len(self.envelope_segments))
        result.append(-99 if self.release_node is None else self.release_node)
        result.append(-99 if self.loop_node is None else self.loop_node)
        for amplitude, duration, curve in self._envelope_segments:
            result.append(amplitude)
            result.append(duration)
            if isinstance(curve, EnvelopeShape):
                shape = int(curve)
                curve = 0.0
            else:
                shape = int(EnvelopeShape.CUSTOM)
            result.append(shape)
            result.append(curve)
        expanded = [
            UGenVector(*cast(Sequence[SupportsFloat | UGenOperable], x))
            for x in expand_deep(result)  # type: ignore
        ]
        if len(expanded) == 1:
            return expanded[0]
        return UGenVector(*expanded)

    def serialize_interpolated(self) -> UGenVector:
        result: list[UGenOperable | float] = []
        result.append(self.offset or 0.0)
        result.append(self.initial_amplitude)
        result.append(len(self.envelope_segments))
        result.append(self.duration)
        for amplitude, duration, curve in self._envelope_segments:
            result.append(duration)
            if isinstance(curve, EnvelopeShape):
                shape = int(curve)
                curve = 0.0
            else:
                shape = 5
            result.append(shape)
            result.append(curve)
            result.append(amplitude)
        expanded = [
            UGenVector(*cast(Sequence[SupportsFloat | UGenOperable], x))
            for x in expand_deep(result)  # type: ignore
        ]
        if len(expanded) == 1:
            return expanded[0]
        return UGenVector(*expanded)

    def to_array(self, length: int = 1024) -> list[float]:
        """
        Convert envelope to a list of floats.

        ::

            >>> from supriya.ugens import Envelope

        ::

            >>> triangle = Envelope.triangle()
            >>> [round(x, 3) for x in triangle.to_array(length=9)]
            [0.0, 0.25, 0.5, 0.75, 1.0, 0.75, 0.5, 0.25, 0.0]

        ::

            >>> adsr = Envelope.adsr()
            >>> [round(x, 3) for x in adsr.to_array(length=9)]
            [0.0, 0.556, 0.466, 0.237, 0.119, 0.057, 0.025, 0.009, 0.0]

        """
        if length < 1:
            raise ValueError(length)
        length = max(length, len(self._amplitudes))
        if not isinstance(length, int):
            raise ValueError("Envelope may not include UGenOperables")
        total_duration = sum(self._durations)
        if not isinstance(total_duration, float):
            raise ValueError("Envelope may not include UGenOperables")
        ratio = total_duration / (length - 1)
        return [self.at(i * ratio) for i in range(length)]

    @classmethod
    def triangle(cls, duration=1.0, amplitude=1.0) -> "Envelope":
        """
        Make a triangle envelope.

        ::

            >>> from supriya.ugens import Envelope
            >>> envelope = Envelope.triangle()
            >>> list(envelope.serialize())
            [<0.0>, <2.0>, <-99.0>, <-99.0>, <1.0>, <0.5>, <1.0>, <0.0>, <0.0>, <0.5>, <1.0>, <0.0>]
        """
        amplitudes = [0, amplitude, 0]
        duration = duration / 2.0
        durations = [duration, duration]
        return Envelope(amplitudes=amplitudes, durations=durations)

    ### PUBLIC PROPERTIES ###

    @property
    def amplitudes(self) -> tuple[UGenOperable | float]:
        return (self.initial_amplitude,) + tuple(_[0] for _ in self.envelope_segments)

    @property
    def curves(self) -> tuple[EnvelopeShape | UGenOperable | float]:
        return tuple(_[2] for _ in self.envelope_segments)

    @property
    def duration(self) -> UGenOperable | float:
        return sum(self.durations)

    @property
    def durations(self) -> tuple[UGenOperable | float]:
        return tuple(_[1] for _ in self.envelope_segments)

    @property
    def envelope_segments(self):
        return self._envelope_segments

    @property
    def initial_amplitude(self) -> UGenOperable | float:
        return self._initial_amplitude

    @property
    def loop_node(self) -> int | None:
        return self._loop_node

    @property
    def offset(self) -> UGenOperable | float:
        return self._offset

    @property
    def release_node(self) -> int | None:
        return self._release_node


@ugen(kr=True)
class Done(UGen):
    """
    Triggers when `source` sets its `done` flag.

    ::

        >>> source = supriya.ugens.Line.kr()
        >>> done = supriya.ugens.Done.kr(
        ...     source=source,
        ... )
        >>> done
        <Done.kr()[0]>
    """

    source = param()


@ugen(ar=True, kr=True, has_done_flag=True)
class EnvGen(UGen):
    """
    An envelope generator.

    ::

        >>> from supriya.ugens import Envelope, EnvGen
        >>> EnvGen.ar(envelope=Envelope.percussive())
        <EnvGen.ar()[0]>
    """

    gate = param(1.0)
    level_scale = param(1.0)
    level_bias = param(0.0)
    time_scale = param(1.0)
    done_action = param(0.0)
    envelope = param(unexpanded=True)

    @classmethod
    def _new_expanded(
        cls,
        *,
        calculation_rate=None,
        done_action=None,
        envelope=None,
        gate=1.0,
        level_bias=0.0,
        level_scale=1.0,
        time_scale=1.0,
    ):
        return super(EnvGen, cls)._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            envelope=envelope,
            gate=gate,
            level_bias=level_bias,
            level_scale=level_scale,
            time_scale=time_scale,
        )


@ugen(kr=True)
class Free(UGen):
    """
    Frees the node at `node_id` when triggered by `trigger`.

    ::

        >>> node_id = 1000
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> free = supriya.ugens.Free.kr(
        ...     node_id=node_id,
        ...     trigger=trigger,
        ... )
        >>> free
        <Free.kr()[0]>
    """

    trigger = param(0)
    node_id = param()


@ugen(kr=True)
class FreeSelf(UGen):
    """
    Frees the enclosing synth when triggered by `trigger`.

    ::

        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> free_self = supriya.ugens.FreeSelf.kr(
        ...     trigger=trigger,
        ... )
        >>> free_self
        <FreeSelf.kr()[0]>
    """

    trigger = param()


@ugen(kr=True)
class FreeSelfWhenDone(UGen):
    """
    Frees the enclosing synth when `source` sets its `done` flag.

    ::

        >>> source = supriya.ugens.Line.kr()
        >>> free_self_when_done = supriya.ugens.FreeSelfWhenDone.kr(
        ...     source=source,
        ... )
        >>> free_self_when_done
        <FreeSelfWhenDone.kr()[0]>
    """

    source = param()


@ugen(kr=True, has_done_flag=True)
class Linen(UGen):
    """
    A simple line generating unit generator.

    ::

        >>> supriya.ugens.Linen.kr()
        <Linen.kr()[0]>
    """

    gate = param(1.0)
    attack_time = param(0.01)
    sustain_level = param(1.0)
    release_time = param(1.0)
    done_action = param(0)


@ugen(kr=True)
class Pause(UGen):
    """
    Pauses the node at `node_id` when triggered by `trigger`.

    ::

        >>> node_id = 1000
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> pause = supriya.ugens.Pause.kr(
        ...     node_id=node_id,
        ...     trigger=trigger,
        ... )
        >>> pause
        <Pause.kr()[0]>
    """

    trigger = param()
    node_id = param()


@ugen(kr=True)
class PauseSelf(UGen):
    """
    Pauses the enclosing synth when triggered by `trigger`.

    ::

        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> pause_self = supriya.ugens.PauseSelf.kr(
        ...     trigger=trigger,
        ... )
        >>> pause_self
        <PauseSelf.kr()[0]>
    """

    trigger = param()


@ugen(kr=True)
class PauseSelfWhenDone(UGen):
    """
    Pauses the enclosing synth when `source` sets its `done` flag.

    ::

        >>> source = supriya.ugens.Line.kr()
        >>> pause_self_when_done = supriya.ugens.PauseSelfWhenDone.kr(
        ...     source=source,
        ... )
        >>> pause_self_when_done
        <PauseSelfWhenDone.kr()[0]>
    """

    source = param()
