# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Envelope(SupriyaObject):

    ### CLASS VARIABLES ###

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
        amplitudes=None,
        durations=None,
        curves=None,
        release_node=None,
        loop_node=None,
        offset=0.,
        ):
        self._amplitudes = tuple(amplitudes)
        self._durations = tuple(durations)
        if isinstance(curves, (int, float)):
            curves = (curves,)
        self._curves = tuple(curves)
        self._release_node = release_node
        self._loop_node = loop_node
        self._offset = offset

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self, expr):
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

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
