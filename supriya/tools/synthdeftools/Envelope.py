# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Envelope(SupriyaObject):
    r'''An envelope.

    ::

        >>> from supriya.tools import *
        >>> envelope = synthdeftools.Envelope()
        >>> envelope
        Envelope(
            amplitudes=(0.0, 1.0, 0.0),
            durations=(1.0, 1.0),
            curves=('linear',),
            offset=0.0
            )

    ::

        >>> tuple(envelope)
        (0.0, 2, -99, -99, 1.0, 1.0, 1, 0.0, 0.0, 1.0, 1, 0.0)

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_amplitudes',
        '_curves',
        '_durations',
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
        offset=0.,
        ):
        assert len(amplitudes)
        assert len(durations) and len(durations) == (len(amplitudes) - 1)
        self._amplitudes = tuple(float(x) for x in amplitudes)
        self._durations = tuple(float(x) for x in durations)
        if isinstance(curves, (int, float, str)):
            curves = (curves,)
        elif curves is None:
            curves = ()
        self._curves = tuple(curves)
        if release_node is not None:
            release_node = int(release_node)
            assert 0 <= release_node < len(amplitudes)
        self._release_node = release_node
        if loop_node is not None:
            assert self._release_node is not None
            loop_node = int(loop_node)
            assert 0 <= loop_node <= release_node
        self._loop_node = loop_node
        self._offset = float(offset)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self, expr):
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

    def __iter__(self):
        from supriya.tools import synthdeftools
        result = []
        result.append(self.amplitudes[0])
        result.append(len(self.durations))
        release_node = self.release_node
        if release_node is None:
            release_node = -99
        result.append(release_node)
        loop_node = self.loop_node
        if loop_node is None:
            loop_node = -99
        result.append(loop_node)
        for i in range(len(self.durations)):
            result.append(self.amplitudes[i + 1])
            result.append(self.durations[i])
            curve = self.curves[i % len(self.curves)]
            if isinstance(curve, str):
                shape = synthdeftools.EnvelopeShape.from_expr(curve)
                shape = int(shape)
                curve = 0.
            else:
                shape = 5
            result.append(shape)
            result.append(curve)
        for x in result:
            yield x

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
                curves=(-4.0,),
                offset=0.0
                )

        ::

            >>> tuple(envelope)
            (0.0, 2, -99, -99, 1.0, 0.01, 5, -4.0, 0.0, 1.0, 5, -4.0)

        '''
        amplitudes = (0, float(amplitude), 0)
        durations = (float(attack_time), float(release_time))
        curves = (float(curve),)
        return Envelope(
            amplitudes=amplitudes,
            durations=durations,
            curves=curves,
            )

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
                curves=('linear',),
                offset=0.0
                )

        ::

            >>> tuple(envelope)
            (0.0, 2, -99, -99, 1.0, 0.5, 1, 0.0, 0.0, 0.5, 1, 0.0)

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
        return self._amplitudes

    @property
    def curves(self):
        return self._curves

    @property
    def durations(self):
        return self._durations

    @property
    def loop_node(self):
        return self._loop_node

    @property
    def offset(self):
        return self._offset

    @property
    def release_node(self):
        return self._release_node