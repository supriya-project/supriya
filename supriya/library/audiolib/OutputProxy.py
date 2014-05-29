# -*- encoding: utf-8 -*-
from supriya.library.audiolib.UGenMethodMixin import UGenMethodMixin


class OutputProxy(UGenMethodMixin):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_output_index',
        '_source',
        )

    ### INITIALIZER ###

    def __init__(self, source=None, output_index=None):
        from supriya import audiolib
        assert isinstance(source, audiolib.UGen)
        assert isinstance(output_index, int)
        self._output_index = output_index
        self._source = source

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self

    ### PRIVATE METHODS ###

    def _get_output_number(self):
        return self._output_index

    def _get_source(self):
        return self._source

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        return self.source.calculation_rate

    @property
    def output_index(self):
        return self._output_index

    @property
    def source(self):
        return self._source
