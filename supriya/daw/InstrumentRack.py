from uqbar.containers import UniqueTreeTuple

from supriya.realtime import BusGroup, Group, Synth

from .ChainContainer import ChainContainer
from .InstrumentChain import InstrumentChain
from .RackDevice import RackDevice
from .RackReceive import RackReceive
from .ReturnChain import ReturnChain
from .Send import Send
from .synthdefs import build_rack_output_synthdef


class InstrumentRack(RackDevice):

    ### INITIALIZER ###

    def __init__(self, channel_count=2, name=None):
        RackDevice.__init__(self)
        self._levels = dict(output=None)
        self._osc_callbacks = dict(output=None)
        self._bus_group = BusGroup.audio(bus_count=channel_count)
        self._chains = ChainContainer(chain_class=InstrumentChain)
        self._return_chains = ChainContainer(
            chain_class=ReturnChain, name="return chain container"
        )
        self._receive = RackReceive()
        UniqueTreeTuple.__init__(
            self, children=[self.chains, self.return_chains, self.receive]
        )
        self._rack_output_synth = Synth(
            synthdef=build_rack_output_synthdef(channel_count), name="rack output"
        )
        self._node = Group(
            children=[
                self.chains._node,
                self.return_chains._node,
                self.rack_output_synth,
            ],
            name=name or "instrument rack",
        )

    ### PRIVATE METHODS ###

    def _create_bus_routings(self, server):
        self.rack_output_synth["in_"] = int(self.bus_group)
        self.rack_output_synth["out"] = int(self.parent.parent.bus_group)

    def _create_osc_callbacks(self, server):
        self._osc_callbacks["output"] = server.osc_io.register(
            ["/levels/rack/output", self._rack_output_synth.node_id],
            lambda osc_message: self._update_levels("output", osc_message.contents[2:]),
        )

    def _destroy_osc_callback(self, server):
        for key, callback in self._osc_callbacks.items():
            if callback and server:
                server.osc_io.unregister(callback)

    def _list_bus_groups(self):
        return [self.bus_group]

    def _update_levels(self, key, levels):
        self._levels[key] = levels

    ### PUBLIC METHODS ###

    def add_chain(self) -> InstrumentChain:
        chain = InstrumentChain()
        self.chains.append(chain)
        chain.sends.append(Send(chain, self))
        return chain

    def add_return_chain(self) -> ReturnChain:
        chain = self.return_chains._node_class()
        self.return_chains.append(chain)
        chain.sends.append(Send(chain, self))
        return chain

    ### PUBLIC PROPERTIES ###

    @property
    def bus_group(self) -> BusGroup:
        return self._bus_group

    @property
    def chains(self):
        return self._chains

    @property
    def channel_count(self):
        return len(self._bus_group)

    @property
    def return_chains(self):
        return self._return_chains

    @property
    def rack_output_synth(self):
        return self._rack_output_synth

    @property
    def receive(self):
        return self._receive
