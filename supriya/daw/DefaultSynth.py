from supriya import conversions
from supriya.assets import synthdefs
from supriya.commands.NodeSetRequest import NodeSetRequest
from supriya.commands.Request import Request
from supriya.commands.SynthNewRequest import SynthNewRequest
from supriya.enums import AddAction
from supriya.midi import NoteOffMessage, NoteOnMessage
from supriya.realtime.nodes import Synth

from .Instrument import Instrument


class DefaultSynth(Instrument):

    ### INITIALIZER ###

    def __init__(self, channel_count=None, name=None):
        Instrument.__init__(self, channel_count=channel_count or 2, name=name)
        self._event_handlers.update(
            {NoteOnMessage: self._handle_note_on, NoteOffMessage: self._handle_note_off}
        )
        self._synthdef = synthdefs.default

    ### PRIVATE METHODS ###

    def _allocate_synthdefs(self, server):
        self._synthdef.allocate(server=server)

    def _handle_note_on(self, message: NoteOnMessage):
        amplitude = conversions.midi_velocity_to_amplitude(message.velocity)
        frequency = conversions.midi_note_number_to_frequency(message.note_number)
        if message.note_number in self._input_note_numbers:
            request: Request = NodeSetRequest(
                amplitude=amplitude,
                node_id=self._input_note_numbers[message.note_number],
            )
        else:
            bus_id = 0
            node_id = -1
            if self.server is not None:
                bus_id = int(self.parent.parent.bus_group)
                node_id = self.server.node_id_allocator.allocate_node_id()
                synth = Synth(
                    synthdef=self._synthdef,
                    amplitude=amplitude,
                    frequency=frequency,
                    out=bus_id,
                )
                self.server._pending_synths[node_id] = synth
            self._input_note_numbers[message.note_number] = [node_id]
            request = SynthNewRequest(
                add_action=AddAction.ADD_TO_TAIL,
                amplitude=amplitude,
                frequency=frequency,
                node_id=node_id,
                out=bus_id,
                synthdef=self._synthdef,
                target_node_id=self.node,
            )
        return (), (request,)

    def _handle_note_off(self, message: NoteOffMessage):
        node_id = self._input_note_numbers.pop(message.note_number, None)
        if node_id is None:
            return (), ()
        request = NodeSetRequest(node_id=node_id, gate=0)
        return (), (request,)
