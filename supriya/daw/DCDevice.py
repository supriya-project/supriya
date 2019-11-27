from uqbar.strings import delimit_words

from supriya.realtime import Synth
from supriya.synthdefs import SynthDefFactory
from supriya.ugens import DC

from .AudioDevice import AudioDevice
from .DawNode import DawNode
from .synthdefs import _gate_block


class DCDevice(AudioDevice):

    ### INITIALIZER ###

    def __init__(self, *, channel_count=2, dc=1.0, name=None):
        AudioDevice.__init__(
            self,
            channel_count=channel_count,
            name=" ".join(_.lower() for _ in delimit_words(type(self).__name__)),
        )
        self._synth = Synth(synthdef=self._build_synthdef(channel_count), dc=dc)
        self.node.append(self.synth)

    ### PRIVATE METHODS ###

    def _build_synthdef(self, channel_count):
        def _signal_block(builder, source, state):
            return DC.ar(source=[builder["dc"]] * state["channel_count"])

        factory = (
            SynthDefFactory(active=1, dc=1, gate=1, lag=0.1)
            .with_signal_block(_signal_block)
            .with_signal_block(_gate_block)
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
