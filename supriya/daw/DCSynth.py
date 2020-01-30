from supriya.commands.NodeFreeRequest import NodeFreeRequest
from supriya.commands.NodeSetRequest import NodeSetRequest
from supriya.commands.Request import Request
from supriya.commands.SynthNewRequest import SynthNewRequest
from supriya.enums import AddAction
from supriya.midi import NoteOffMessage, NoteOnMessage
from supriya.realtime.nodes import Synth
from supriya.synthdefs import SynthDefBuilder
from supriya.ugens import DC, Out

from .Instrument import Instrument


class DCSynth(Instrument):
    # TODO: How can we collapse all instrument subclasses together

    ### INITIALIZER ###

    def __init__(self, channel_count=None, name=None):
        Instrument.__init__(self, channel_count=channel_count or 2, name=name)
        self._event_handlers.update(
            {NoteOnMessage: self._handle_note_on, NoteOffMessage: self._handle_note_off}
        )
        self._synthdef = self._build_synthdef()

    ### PRIVATE METHODS ###

    def _allocate_synthdefs(self, server):
        self._synthdef.allocate(server=server)

    def _build_synthdef(self):
        with SynthDefBuilder(out=0, amplitude=0) as builder:
            source = DC.ar(source=builder["amplitude"])
            Out.ar(bus=builder["out"], source=[source] * self._channel_count)
        return builder.build()

    ### PRIVATE METHODS ###

    def _handle_note_on(self, message: NoteOnMessage):
        amplitude = message.note_number * message.velocity
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
                synth = Synth(synthdef=self._synthdef, amplitude=amplitude, out=bus_id)
                self.server._pending_synths[node_id] = synth
            request = SynthNewRequest(
                add_action=AddAction.ADD_TO_TAIL,
                target_node_id=self.node,
                amplitude=amplitude,
                node_id=node_id,
                out=bus_id,
                synthdef=self._synthdef,
            )
            self._input_note_numbers[message.note_number] = [node_id]
        return (), (request,)

    def _handle_note_off(self, message: NoteOffMessage):
        node_id = self._input_note_numbers.pop(message.note_number, None)
        if node_id is None:
            return (), ()
        request = NodeFreeRequest(node_ids=(node_id,))
        return (), (request,)
