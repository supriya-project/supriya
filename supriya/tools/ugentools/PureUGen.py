# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PureUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _optimize_graph(self):
        self._perform_dead_code_elimination()
