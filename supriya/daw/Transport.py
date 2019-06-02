from supriya.clock import TempoClock
from supriya.realtime import Synth
from supriya.synthdefs import SynthDefBuilder

from .DawNode import DawNode


class Transport(DawNode):
    def __init__(self):
        DawNode.__init__(self)
        self._clock = TempoClock()
        self._node = Synth(synthdef=self._build_synthdef(), name="transport")

    def _build_synthdef(self):
        with SynthDefBuilder(
            numerator=4, denominator=4, beats_per_minute=120
        ) as builder:
            pass
        return builder.build(name="transport")
