from abjad import Infinity, NegativeInfinity
from abjad.timespans import Timespan


class Block(Timespan):

    ### CLASS VARIABLES ###

    __documentation_section__ = "Server Internals"

    __slots__ = ("_used",)

    ### INITIALIZER ###

    def __init__(self, start_offset=NegativeInfinity, stop_offset=Infinity, used=False):
        if start_offset is None:
            start_offset = NegativeInfinity
        if stop_offset is None:
            stop_offset = Infinity
        Timespan.__init__(self, start_offset=start_offset, stop_offset=stop_offset)
        self._used = bool(used)

    ### PRIVATE METHODS ###

    def _initialize_offset(self, offset):
        if offset in (NegativeInfinity, Infinity):
            return offset
        else:
            return int(offset)

    ### PUBLIC PROPERTIES ###

    @property
    def used(self):
        return self._used
