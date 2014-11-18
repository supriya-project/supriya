# -*- encoding: utf-8 -*-
from supriya.tools.bindingtools.BindingSource import BindingSource


class BindingInput(BindingSource):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_binding_targets',
        '_output_range',
        )

    ### INITIALIZER ###

    def __init__(self, output_range=None):
        BindingSource.__init__(
            self,
            output_range=output_range,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(),
            )