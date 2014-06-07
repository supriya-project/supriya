import collections
from supriya.library.audiolib.Argument import Argument
from supriya.library.audiolib.UGen import UGen


class Out(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _unexpanded_argument_names = ('source',)

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            )
        Argument('bus').configure(self, bus)
        if not isinstance(source, collections.Sequence):
            source = [source]
        for single_source in source:
            Argument('source').configure(self, single_source)

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []
