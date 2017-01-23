# -*- encoding: utf-8 -*-
from supriya.tools.patterntools.Pattern import Pattern
from supriya.tools.patterntools.Pseq import Pseq


class Prand(Pseq):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def _iterate(self, state=None):
        rng = self._get_rng()
        for _ in self._loop(self._repetitions):
            index = int(next(rng) * 0x7FFFFFFF) % len(self.sequence)
            choice = self.sequence[index]
            if isinstance(choice, Pattern):
                yield from choice
            else:
                yield choice
