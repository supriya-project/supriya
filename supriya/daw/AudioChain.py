from typing import Tuple

from supriya.realtime import BusGroup, Group, Synth

from .Chain import Chain
from .DeviceType import DeviceType
from .Send import Send
from .SendManager import SendManager
from .synthdefs import build_chain_input_synthdef, build_chain_output_synthdef


class AudioChain(Chain):

    ### INITIALIZER ###

    def __init__(self, channel_count=2):
        Chain.__init__(self)
        self._levels = dict(input=None, prefader=None, postfader=None)
        self._osc_callbacks = dict(input=None, prefader=None, postfader=None)
        self._bus_group = BusGroup.audio(bus_count=channel_count)
        self._input_synth = Synth(synthdef=build_chain_input_synthdef(channel_count))
        self._output_synth = Synth(synthdef=build_chain_output_synthdef(channel_count))
        self._sends = SendManager()
        self._mutate([self.devices, self.sends])
        self._node = Group(
            children=[
                self.input_synth,
                self.devices.node,
                self.sends.pre_fader_group,
                self.output_synth,
                self.sends.post_fader_group,
            ],
            name="audio chain",
        )

    ### PRIVATE METHODS ###

    def _create_bus_routings(self, server):
        self._input_synth["in_"] = int(self.parent.parent.parent.parent.bus_group)
        self._input_synth["out"] = int(self._bus_group)
        self._output_synth["in_"] = int(self._bus_group)
        self._output_synth["out"] = int(self._bus_group)

    def _create_osc_callbacks(self, server):
        def update_levels(key, levels):
            self._levels[key] = levels

        self._osc_callbacks["input"] = server.osc_io.register(
            ["/levels/chain/input", self._input_synth.node_id],
            lambda osc_message: update_levels("input", osc_message.contents[2:]),
        )
        self._osc_callbacks["prefader"] = server.osc_io.register(
            ["/levels/chain/prefader", self._output_synth.node_id],
            lambda osc_message: update_levels("prefader", osc_message.contents[2:]),
        )
        self._osc_callbacks["postfader"] = server.osc_io.register(
            ["/levels/chain/postfader", self._output_synth.node_id],
            lambda osc_message: update_levels("postfader", osc_message.contents[2:]),
        )

    def _destroy_osc_callbacks(self, server):
        for key, callback in self._osc_callbacks.items():
            if callback and server:
                server.osc_io.unregister(callback)

    def _list_bus_groups(self):
        return [self.bus_group]

    ### PUBLIC METHODS ###

    def add_send(self, target, *, post_fader=True) -> Send:
        send = Send(self, target, post_fader=post_fader)
        self.sends.append(send)
        return send

    ### PUBLIC PROPERTIES ###

    @property
    def bus_group(self):
        return self._bus_group

    @property
    def channel_count(self):
        return len(self._bus_group)

    @property
    def device_types(self) -> Tuple[DeviceType, ...]:
        return (DeviceType.AUDIO,)

    @property
    def input_synth(self):
        return self._input_synth

    @property
    def output_synth(self):
        return self._output_synth

    @property
    def sends(self):
        return self._sends
