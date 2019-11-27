from typing import Callable, Generator, Optional, Sequence, Tuple

from uqbar.containers import UniqueTreeTuple

from supriya.commands import Request
from supriya.midi import MidiMessage

from .AudioChain import AudioChain
from .Chain import Chain
from .ChainContainer import ChainContainer
from .Device import Device
from .DeviceType import DeviceType
from .InstrumentChain import InstrumentChain
from .MidiChain import MidiChain
from .MixerContext import MixerContext


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
        self, moment, in_midi_messages
    ) -> Generator[
        Tuple[Optional[Callable], Sequence[MidiMessage], Sequence[Request]], None, None
    ]:
        # TODO: Refactor for zone control
        performers = []
        for chain in self.chains:
            if chain.devices:
                performers.append(chain.devices[0].perform)
            else:
                performers.append(self.perform_output)
        for message in self.filter_in_midi_messages(in_midi_messages):
            self._update_captures(moment, message, "I")
            for performer in performers:
                yield performer, (message,), ()

    def perform_output(
        self, moment, in_midi_messages
    ) -> Generator[
        Tuple[Optional[Callable], Sequence[MidiMessage], Sequence[Request]], None, None
    ]:
        for message in self.filter_out_midi_messages(in_midi_messages):
            self._update_captures(moment, message, "O")
            yield None, (message,), ()

    ### PUBLIC PROPERTIES ###

    @property
    def chains(self) -> ChainContainer:
        return self.chains
