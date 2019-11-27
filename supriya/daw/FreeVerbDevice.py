from supriya.realtime import Synth
from supriya.synthdefs import SynthDefFactory
from supriya.ugens import FreeVerb, Lag

from .AudioDevice import AudioDevice
from .DawNode import DawNode
from .synthdefs import _gate_block


class FreeVerbDevice(AudioDevice):

    ### INITIALIZER ###

    def __init__(self, *, channel_count=2, name=None):
        AudioDevice.__init__(self, channel_count=channel_count, name=name)
        self._synth = Synth(synthdef=self._build_synthdef(channel_count))
        self.node.append(self.synth)

    ### PRIVATE METHODS ###

    def _build_synthdef(self, channel_count):
        def _signal_block(builder, source, state):
            return FreeVerb.ar(
                source=source,
                mix=Lag.kr(builder["mix"], lag_time=0.1),
                room_size=Lag.kr(builder["room_size"], lag_time=0.1),
                damping=Lag.kr(builder["damping"], lag_time=0.1),
            )

        factory = (
            SynthDefFactory(
                active=1, gate=1, lag=0.1, mix=0.5, room_size=0.75, damping=0.75
            )
            .with_signal_block(_signal_block)
            .with_signal_block(_gate_block)
            .with_input()
            .with_output()
            .with_channel_count(channel_count)
        )
        return factory.build()

    def _create_bus_routings(self, server):
        self.synth["out"] = int(self.parent.parent.bus_group)

    def _reallocate(self):
        DawNode._reallocate(self)
        if int(self.parent.parent.bus_group) == self.synth["out"]:
            return
        self.synth.release()
        self.synth = Synth(synthdef=self._build_synthdef(self.channel_count))
        self.node.append(self.synth)

    ### PUBLIC PROPERTIES ###

    @property
    def synth(self):
        return self._synth
