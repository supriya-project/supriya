# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.ugens.MultiOutUGen import MultiOutUGen


class PureMultiOutUGen(MultiOutUGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _optimize_graph(self):
        self._perform_dead_code_elimination()
