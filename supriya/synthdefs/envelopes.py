from typing import List, Optional, Sequence, Tuple, Union

from uqbar.objects import get_repr

from .. import utils
from ..enums import EnvelopeShape
from ..ugens import UGenArray, UGenOperable


class Envelope:
    """
    An envelope.

    ::

        >>> from supriya.synthdefs import Envelope
        >>> envelope = Envelope()

    ::

        >>> list(envelope.serialize())
        [0, 2, -99, -99, 1, 1, 1, 0.0, 0, 1, 1, 0.0]
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
        assert len(amplitudes) > 1
        assert len(durations) == (len(amplitudes) - 1)
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

            >>> from supriya.synthdefs import Envelope
            >>> envelope = Envelope.percussive()
            >>> envelope
            Envelope(
                curves=(-4.0, -4.0),
                durations=(0.01, 1.0),
            )

        ::

            >>> list(envelope.serialize())
            [0, 2, -99, -99, 1.0, 0.01, 5, -4.0, 0, 1.0, 5, -4.0]
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

    def serialize(self, for_interpolation=False) -> UGenArray:
        result: List[Union[UGenOperable, float]] = []
        if for_interpolation:
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
        else:
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
        return UGenArray(result)

    @classmethod
    def triangle(cls, duration=1.0, amplitude=1.0) -> "Envelope":
        """
        Make a triangle envelope.

        ::

            >>> from supriya.synthdefs import Envelope
            >>> envelope = Envelope.triangle()
            >>> envelope
            Envelope(
                durations=(0.5, 0.5),
            )

        ::

            >>> list(envelope.serialize())
            [0, 2, -99, -99, 1.0, 0.5, 1, 0.0, 0, 0.5, 1, 0.0]
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
