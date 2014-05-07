import collections
from supriya.synthdefs.UGen import UGen
from supriya.synthdefs import ArgumentSpecification


class Out(UGen):

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        special_index=0,
        bus=0,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            special_index=special_index,
            )
        ArgumentSpecification('bus').configure(self, bus)
        if not isinstance(source, collections.Sequence):
            source = [source]
        for single_source in source:
            ArgumentSpecification('source').configure(self, single_source)

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []
