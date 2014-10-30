# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PureMultiOutUGen(MultiOutUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _optimize_graph(self):
        self._perform_dead_code_elimination()