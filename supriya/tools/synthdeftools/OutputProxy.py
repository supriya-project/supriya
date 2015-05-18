# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class OutputProxy(UGenMethodMixin):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    __slots__ = (
        '_output_index',
        '_source',
        )

    ### INITIALIZER ###

    def __init__(self, source=None, output_index=None):
        from supriya import synthdeftools
        prototype = (
            synthdeftools.UGen,
            synthdeftools.Parameter,
            )
        assert isinstance(source, prototype)
        assert isinstance(output_index, int)
        self._output_index = output_index
        self._source = source

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) != type(expr):
            return False
        if self._output_index != expr._output_index:
            return False
        if self._source != expr._source:
            return False
        return True

    def __hash__(self):
        hash_values = (
            type(self),
            self._output_index,
            self._source,
            )
        return hash(hash_values)

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
    def has_done_flag(self):
        return self.source.has_done_flag

    @property
    def output_index(self):
        return self._output_index

    @property
    def source(self):
        return self._source