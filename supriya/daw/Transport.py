from supriya.clock import TempoClock
from supriya.realtime import Synth
from supriya.synthdefs.SynthDef import SynthDef
from supriya.synthdefs.SynthDefBuilder import SynthDefBuilder

from .DawNode import DawNode


class Transport(DawNode):

    ### INITIALIZER ###

    def __init__(self):
        DawNode.__init__(self)
        self._clock = TempoClock()
        self._node = Synth(synthdef=self._build_synthdef(), name="transport")
        self._default_quantization = "1/4"

    ### PRIVATE METHODS ###

    def _build_synthdef(self) -> SynthDef:
        with SynthDefBuilder(
            numerator=4, denominator=4, beats_per_minute=120
        ) as builder:
            pass
        return builder.build(name="transport")

    ### PUBLIC METHODS ###

    def start(self):
        self._clock.start()

    def stop(self):
        self._clock.stop()

    ### PUBLIC PROPERTIES ###

    @property
    def clock(self) -> TempoClock:
        return self._clock

    @property
    def default_quantization(self):
        return self._default_quantization

    @property
    def is_running(self) -> bool:
        return self.clock.is_running
