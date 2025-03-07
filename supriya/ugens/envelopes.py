from typing import List, Optional, Sequence, Tuple, Union

from uqbar.objects import get_repr

from .. import utils
from ..enums import DoneAction, EnvelopeShape
from .core import Parameter, UGen, UGenOperable, UGenVector, param, ugen


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
        amplitudes: Sequence[Union[UGenOperable, float]] = (0, 1, 0),
        durations: Sequence[Union[UGenOperable, float]] = (1, 1),
        curves: Sequence[Union[EnvelopeShape, UGenOperable, float, str, None]] = (
            EnvelopeShape.LINEAR,
            EnvelopeShape.LINEAR,
        ),
        release_node: Optional[int] = None,
        loop_node: Optional[int] = None,
        offset: Union[UGenOperable, float] = 0.0,
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
        self._initial_amplitude = amplitudes[0]
        self._amplitudes: Tuple[Union[UGenOperable, float], ...] = tuple(amplitudes[1:])
        self._durations: Tuple[Union[UGenOperable, float], ...] = tuple(durations)
        curves_: List[Union[EnvelopeShape, UGenOperable, float]] = []
        for x in curves:
            if isinstance(x, (EnvelopeShape, UGenOperable)):
                curves_.append(x)
            elif isinstance(x, str) or x is None:
                curves_.append(EnvelopeShape.from_expr(x))
            else:
                curves_.append(float(x))
        self._curves: Tuple[Union[EnvelopeShape, UGenOperable, float], ...] = tuple(
            curves_
        )
        self._envelope_segments = tuple(
            utils.zip_cycled(self._amplitudes, self._durations, self._curves)
        )

    def __repr__(self) -> str:
        return get_repr(self)

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
        attack_time: Union[UGenOperable, float] = 0.01,
        release_time: Union[UGenOperable, float] = 1.0,
        amplitude: Union[UGenOperable, float] = 1.0,
        curve: Union[EnvelopeShape, UGenOperable, float, str] = -4.0,
    ) -> "Envelope":
        """
        Make a percussion envelope.

        ::

            >>> from supriya.ugens import Envelope
            >>> envelope = Envelope.percussive()
            >>> envelope
            Envelope(
                curves=(-4.0, -4.0),
                durations=(0.01, 1.0),
            )

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
        result: List[Union[UGenOperable, float]] = []
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
                shape = 5
            result.append(shape)
            result.append(curve)
        return UGenVector(*result)

    def serialize_interpolated(self) -> UGenVector:
        result: List[Union[UGenOperable, float]] = []
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
        return UGenVector(*result)

    @classmethod
    def triangle(cls, duration=1.0, amplitude=1.0) -> "Envelope":
        """
        Make a triangle envelope.

        ::

            >>> from supriya.ugens import Envelope
            >>> envelope = Envelope.triangle()
            >>> envelope
            Envelope(
                durations=(0.5, 0.5),
            )

        ::

            >>> list(envelope.serialize())
            [<0.0>, <2.0>, <-99.0>, <-99.0>, <1.0>, <0.5>, <1.0>, <0.0>, <0.0>, <0.5>, <1.0>, <0.0>]
        """
        amplitudes = [0, amplitude, 0]
        duration = duration / 2.0
        durations = [duration, duration]
        return Envelope(amplitudes=amplitudes, durations=durations)

    ### PUBLIC PROPERTIES ###

    @property
    def amplitudes(self) -> Tuple[Union[UGenOperable, float]]:
        return (self.initial_amplitude,) + tuple(_[0] for _ in self.envelope_segments)

    @property
    def curves(self) -> Tuple[Union[EnvelopeShape, UGenOperable, float]]:
        return tuple(_[2] for _ in self.envelope_segments)

    @property
    def duration(self) -> Union[float, UGenOperable]:
        return sum(self.durations)

    @property
    def durations(self) -> Tuple[Union[float, UGenOperable]]:
        return tuple(_[1] for _ in self.envelope_segments)

    @property
    def envelope_segments(self):
        return self._envelope_segments

    @property
    def initial_amplitude(self) -> Union[float, UGenOperable]:
        return self._initial_amplitude

    @property
    def loop_node(self) -> Optional[int]:
        return self._loop_node

    @property
    def offset(self) -> Union[float, UGenOperable]:
        return self._offset

    @property
    def release_node(self) -> Optional[int]:
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
        if not isinstance(done_action, Parameter):
            done_action = DoneAction.from_expr(done_action)
        return super(EnvGen, cls)._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            envelope=(envelope or Envelope()).serialize(),
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
