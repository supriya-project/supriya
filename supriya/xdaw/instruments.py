from typing import Dict, Union

from supriya import conversions
from supriya.assets.synthdefs import default
from supriya.provider import SynthProxy
from supriya.synthdefs import SynthDef, SynthDefFactory

from .devices import AllocatableDevice


class Instrument(AllocatableDevice):

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        synthdef: Union[SynthDef, SynthDefFactory] = None,
        name=None,
        parameter_map=None,
        parameters=None,
        synthdef_kwargs=None,
        uuid=None,
    ):
        # TODO: Polyphony Limit
        # TODO: Polyphony Mode
        AllocatableDevice.__init__(self, name=name, uuid=uuid)
        self._synthdef = synthdef or default
        self._synthdef_kwargs = dict(synthdef_kwargs or {})
        self._notes_to_synths: Dict[float, SynthProxy] = {}

    ### PRIVATE METHODS ###

    def _deallocate(self, old_provider, *, dispose_only=False):
        AllocatableDevice._deallocate(self, old_provider, dispose_only=dispose_only)
        self._notes_to_synths.clear()

    def _handle_note_off(self, moment, midi_message):
        self._input_notes.remove(midi_message.pitch)
        synth = self._notes_to_synths.pop(midi_message.pitch, None)
        if synth is not None:
            synth.free()
        return []

    def _handle_note_on(self, moment, midi_message):
        pitch = midi_message.pitch
        if pitch in self._input_notes:
            self._handle_note_off(moment, midi_message)
        self._input_notes.add(midi_message.pitch)
        self._notes_to_synths[pitch] = self.node_proxies["body"].add_synth(
            synthdef=self.synthdef,
            **self.synthdef_kwargs,
            frequency=conversions.midi_note_number_to_frequency(pitch),
            amplitude=conversions.midi_velocity_to_amplitude(midi_message.velocity),
            out=self._audio_bus_proxies["output"],
        )
        return []

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self) -> Union[SynthDef, SynthDefFactory]:
        return self._synthdef

    @property
    def synthdef_kwargs(self):
        return self._synthdef_kwargs
