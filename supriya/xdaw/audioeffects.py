from typing import Union

from supriya.enums import AddAction
from supriya.synthdefs import SynthDef, SynthDefFactory

from .devices import AllocatableDevice


class AudioEffect(AllocatableDevice):

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef: Union[SynthDef, SynthDefFactory],
        *,
        name=None,
        synthdef_kwargs=None,
        parameters=None,
        parameter_map=None,
        uuid=None,
    ):
        AllocatableDevice.__init__(self, name=name, uuid=uuid)
        self._synthdef = synthdef
        self._synthdef_kwargs = dict(synthdef_kwargs or {})

    ### PRIVATE METHODS ###

    def _allocate_synths(self, provider, channel_count, *, synth_pair=None):
        synthdef = self.synthdef
        if isinstance(synthdef, SynthDefFactory):
            synthdef = synthdef.build(channel_count=self.effective_channel_count)
        synth_target, synth_action = synth_pair or (
            self.node_proxies["body"],
            AddAction.ADD_TO_HEAD,
        )
        self._node_proxies["synth"] = provider.add_synth(
            add_action=synth_action,
            synthdef=synthdef,
            target_node=synth_target,
            out=self.audio_bus_proxies["output"],
            **self.synthdef_kwargs,
        )

    def _reallocate(self, difference):
        channel_count = self.effective_channel_count
        synth_synth = self._node_proxies.pop("synth")
        self._free_audio_buses()
        self._allocate_audio_buses(self.provider, channel_count)
        self._allocate_synths(
            self.provider,
            self.effective_channel_count,
            synth_pair=(synth_synth, AddAction.ADD_AFTER),
        )
        synth_synth.free()

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self) -> Union[SynthDef, SynthDefFactory]:
        return self._synthdef

    @property
    def synthdef_kwargs(self):
        return self._synthdef_kwargs
