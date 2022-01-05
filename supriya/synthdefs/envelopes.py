from supriya import EnvelopeShape, utils
from supriya.system import SupriyaValueObject

from .mixins import OutputProxy


class Envelope(SupriyaValueObject):
    """
    An envelope.

    ::

        >>> envelope = supriya.synthdefs.Envelope()
        >>> envelope
        Envelope()

    ::

        >>> envelope.serialize()
        [0.0, 2.0, -99.0, -99.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0]

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_envelope_segments",
        "_initial_amplitude",
        "_loop_node",
        "_offset",
        "_release_node",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        amplitudes=(0, 1, 0),
        durations=(1, 1),
        curves=("linear", "linear"),
        release_node=None,
        loop_node=None,
        offset=None,
    ):
        assert len(amplitudes)
        assert len(durations) and len(durations) == (len(amplitudes) - 1)
        if isinstance(curves, (int, float, str, EnvelopeShape, OutputProxy)):
            curves = [curves]
        elif curves is None:
            curves = []
        self._release_node = release_node
        self._loop_node = loop_node
        self._offset = offset
        self._initial_amplitude = amplitudes[0]
        self._envelope_segments = tuple(
            utils.zip_sequences(amplitudes[1:], durations, curves)
        )

    ### PUBLIC METHODS ###

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
    ):
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
    def asr(cls, attack_time=0.01, sustain=1.0, release_time=1.0, curve=-4.0):
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
    ):
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
    def percussive(cls, attack_time=0.01, release_time=1.0, amplitude=1.0, curve=-4.0):
        """
        Make a percussion envelope.

        ::

            >>> import supriya.synthdefs
            >>> envelope = supriya.synthdefs.Envelope.percussive()
            >>> envelope
            Envelope(
                curves=(-4.0, -4.0),
                durations=(0.01, 1.0),
            )

        ::

            >>> envelope.serialize()
            [0.0, 2.0, -99.0, -99.0, 1.0, 0.01, 5.0, -4.0, 0.0, 1.0, 5.0, -4.0]

        """
        amplitudes = [0, amplitude, 0]
        durations = [attack_time, release_time]
        curves = [curve]
        return Envelope(amplitudes=amplitudes, durations=durations, curves=curves)

    @classmethod
    def linen(
        cls, attack_time=0.01, sustain_time=1.0, release_time=1.0, level=1.0, curve=1
    ):
        amplitudes = [0, level, level, 0]
        durations = [attack_time, sustain_time, release_time]
        curves = [curve]
        return Envelope(amplitudes=amplitudes, durations=durations, curves=curves)

    def serialize(self, for_interpolation=False):
        result = []
        if for_interpolation:
            result.append(self.offset or 0)
            result.append(self.initial_amplitude)
            result.append(len(self.envelope_segments))
            result.append(self.duration)
            for amplitude, duration, curve in self._envelope_segments:
                result.append(duration)
                if isinstance(curve, str):
                    shape = EnvelopeShape.from_expr(curve)
                    shape = int(shape)
                    curve = 0.0
                else:
                    shape = 5
                result.append(shape)
                result.append(curve)
                result.append(amplitude)
        else:
            result.append(self.initial_amplitude)
            result.append(len(self.envelope_segments))
            release_node = self.release_node
            if release_node is None:
                release_node = -99
            result.append(release_node)
            loop_node = self.loop_node
            if loop_node is None:
                loop_node = -99
            result.append(loop_node)
            for amplitude, duration, curve in self._envelope_segments:
                result.append(amplitude)
                result.append(duration)
                if isinstance(curve, str):
                    shape = EnvelopeShape.from_expr(curve)
                    shape = int(shape)
                    curve = 0.0
                else:
                    shape = 5
                result.append(shape)
                result.append(curve)
        serialized = []
        for x in result:
            if isinstance(x, int):
                x = float(x)
            serialized.append(x)
        return serialized

    @classmethod
    def triangle(cls, duration=1.0, amplitude=1.0):
        """
        Make a triangle envelope.

        ::

            >>> import supriya.synthdefs
            >>> envelope = supriya.synthdefs.Envelope.triangle()
            >>> envelope
            Envelope(
                durations=(0.5, 0.5),
            )

        ::

            >>> envelope.serialize()
            [0.0, 2.0, -99.0, -99.0, 1.0, 0.5, 1.0, 0.0, 0.0, 0.5, 1.0, 0.0]

        """
        amplitudes = [0, amplitude, 0]
        duration = duration / 2.0
        durations = [duration, duration]
        return Envelope(amplitudes=amplitudes, durations=durations)

    ### PUBLIC PROPERTIES ###

    @property
    def amplitudes(self):
        return (self.initial_amplitude,) + tuple(_[0] for _ in self.envelope_segments)

    @property
    def curves(self):
        return tuple(_[2] for _ in self.envelope_segments)

    @property
    def duration(self):
        return sum(self.durations)

    @property
    def durations(self):
        return tuple(_[1] for _ in self.envelope_segments)

    @property
    def envelope_segments(self):
        return self._envelope_segments

    @property
    def initial_amplitude(self):
        return self._initial_amplitude

    @property
    def loop_node(self):
        return self._loop_node

    @property
    def offset(self):
        return self._offset

    @property
    def release_node(self):
        return self._release_node
