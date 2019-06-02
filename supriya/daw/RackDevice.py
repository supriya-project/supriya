from typing import List, Tuple

from uqbar.containers import UniqueTreeTuple

from .AudioChain import AudioChain
from .Chain import Chain
from .ChainContainer import ChainContainer
from .Device import Device
from .DeviceType import DeviceType
from .InstrumentChain import InstrumentChain
from .MidiChain import MidiChain
from .MixerContext import MixerContext
from .Note import Note


class RackDevice(Device, UniqueTreeTuple, MixerContext):

    ### INITIALIZER ###

    def __init__(self):
        Device.__init__(self)
        MixerContext.__init__(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _device_type(self):
        chain_class = self.chains._node_class
        if chain_class is AudioChain:
            return DeviceType.AUDIO
        elif chain_class is InstrumentChain:
            return DeviceType.INSTRUMENT
        elif chain_class is MidiChain:
            return DeviceType.MIDI
        raise ValueError(chain_class)

    ### PUBLIC METHODS ###

    def add_chain(self) -> Chain:
        chain = self.chains._node_class()
        self.chains.append(chain)
        return chain

    def perform(
        self, moment, start_notes, stop_notes
    ) -> List[Tuple["Device", List[Note], List[Note]]]:
        results = []
        for chain in self.chains:
            if chain.devices:
                results.append((chain.devices[0], start_notes, stop_notes))
        if not results:
            next_device = self.next_device()
            return [(next_device, start_notes, stop_notes)]
        return results

    ### PUBLIC PROPERTIES ###

    @property
    def chains(self) -> ChainContainer:
        return self.chains
