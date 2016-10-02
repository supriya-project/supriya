# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Envelope(SupriyaValueObject):
    r'''An envelope.

    ::

        >>> from supriya.tools import *
        >>> envelope = synthdeftools.Envelope()
        >>> envelope
        Envelope(
            amplitudes=(0.0, 1.0, 0.0),
            durations=(1.0, 1.0),
            curves=('linear', 'linear')
            )

    ::

        >>> envelope.serialize()
        [0.0, 2, -99, -99, 1.0, 1.0, 1, 0.0, 0.0, 1.0, 1, 0.0]

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_envelope_segments',
        '_initial_amplitude',
        '_loop_node',
        '_offset',
        '_release_node',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        amplitudes=(0, 1, 0),
        durations=(1, 1),
        curves='linear',
        release_node=None,
        loop_node=None,
        offset=None,
        ):
        from supriya.tools import synthdeftools
        assert len(amplitudes)
        assert len(durations) and len(durations) == (len(amplitudes) - 1)
        amplitudes = list(amplitudes)
        for i, amplitude in enumerate(amplitudes):
            if isinstance(amplitude, int):
                amplitudes[i] = float(amplitude)
        durations = list(durations)
        for i, duration in enumerate(durations):
            if isinstance(duration, int):
                durations[i] = float(duration)
        if isinstance(curves, (
            int, float, str, synthdeftools.EnvelopeShape,
            )):
            curves = (curves,)
        elif curves is None:
            curves = ()
        curves = tuple(curves)
        if release_node is not None:
            release_node = int(release_node)
            assert 0 <= release_node < len(amplitudes)
        self._release_node = release_node
        if loop_node is not None:
            assert self._release_node is not None
            loop_node = int(loop_node)
            assert 0 <= loop_node <= release_node
        self._loop_node = loop_node
        if offset is not None:
            offset = float(offset)
        self._offset = offset
        self._initial_amplitude = amplitudes[0]
        self._envelope_segments = tuple(sequencetools.zip_sequences([
            amplitudes[1:],
            durations,
            curves,
            ], cyclic=True))

    ### PUBLIC METHODS ###

    @staticmethod
    def asr(
        attack_time=0.01,
        release_time=1.0,
        amplitude=1.0,
        curve=-4.0,
        ):
        amplitudes = (0, float(amplitude), 0)
        durations = (float(attack_time), float(release_time))
        curves = (float(curve),)
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

    @staticmethod
    def percussive(
        attack_time=0.01,
        release_time=1.0,
        amplitude=1.0,
        curve=-4.0,
        ):
        r'''Make a percussion envelope.

        ::

            >>> from supriya.tools import synthdeftools
            >>> envelope = synthdeftools.Envelope.percussive()
            >>> envelope
            Envelope(
                amplitudes=(0.0, 1.0, 0.0),
                durations=(0.01, 1.0),
                curves=(-4.0, -4.0)
                )

        ::

            >>> envelope.serialize()
            [0.0, 2, -99, -99, 1.0, 0.01, 5, -4.0, 0.0, 1.0, 5, -4.0]

        '''
        amplitudes = (0, float(amplitude), 0)
        durations = (float(attack_time), float(release_time))
        curves = (float(curve),)
        return Envelope(
            amplitudes=amplitudes,
            durations=durations,
            curves=curves,
            )

    def serialize(self, for_interpolation=False):
        from supriya.tools import synthdeftools
        result = []
        if for_interpolation:
            result.append(self.offset or 0)
            result.append(self.initial_amplitude)
            result.append(len(self.envelope_segments))
            result.append(self.duration)
            for amplitude, duration, curve in self._envelope_segments:
                result.append(duration)
                if isinstance(curve, (synthdeftools.EnvelopeShape, str)):
                    shape = synthdeftools.EnvelopeShape.from_expr(curve)
                    shape = int(shape)
                    curve = 0.
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
                    shape = synthdeftools.EnvelopeShape.from_expr(curve)
                    shape = int(shape)
                    curve = 0.
                else:
                    shape = 5
                result.append(shape)
                result.append(curve)
        return result

    @staticmethod
    def triangle(
        duration=1.0,
        amplitude=1.0,
        ):
        r'''Make a triangle envelope.

        ::

            >>> from supriya.tools import synthdeftools
            >>> envelope = synthdeftools.Envelope.triangle()
            >>> envelope
            Envelope(
                amplitudes=(0.0, 1.0, 0.0),
                durations=(0.5, 0.5),
                curves=('linear', 'linear')
                )

        ::

            >>> envelope.serialize()
            [0.0, 2, -99, -99, 1.0, 0.5, 1, 0.0, 0.0, 0.5, 1, 0.0]

        '''
        amplitudes = (0, float(amplitude), 0)
        duration = float(duration) / 2.
        durations = (duration, duration)
        return Envelope(
            amplitudes=amplitudes,
            durations=durations,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def amplitudes(self):
        return (self.initial_amplitude,) + \
            tuple(_[0] for _ in self.envelope_segments)

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
