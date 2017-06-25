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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.FormatSpecification(
            client=self,
            storage_format_kwargs_names=[],
            )
