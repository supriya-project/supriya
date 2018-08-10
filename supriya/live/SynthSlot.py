import supriya.synthdefs
import supriya.system
from supriya.live.Slot import Slot
from supriya.system.Bindable import Bindable
from supriya.system.BindableNamespace import BindableNamespace


class SynthSlot(Slot):

    ### INITIALIZER ###

    def __init__(
        self,
        name,
        track,
        synthdef,
        **kwargs
        ):
        import supriya.assets.synthdefs
        self._synthdef = synthdef or supriya.assets.synthdefs.default
        Slot.__init__(self, name, track, self._synthdef, **kwargs)
        self._synth = supriya.realtime.Synth(
            synthdef=self._synthdef,
            **self.bindable_namespace
            )
        for key in self._bindable_namespace:
            supriya.system.bind(self[key], self._synth.controls[key])

    ### PRIVATE METHODS ###

    def _setup_bindable_namespace(self, **kwargs):
        for name, parameter in self._synthdef.parameters.items():
            if parameter.parameter_rate in (
                supriya.synthdefs.ParameterRate.AUDIO,
                supriya.synthdefs.ParameterRate.SCALAR,
                ):
                continue
            elif name in kwargs:
                continue
            kwargs[name] = parameter.value
        for key in tuple(kwargs):
            if key in ('in_', 'out', 'gate'):
                kwargs.pop(key)
            elif key not in self._synthdef.parameter_names:
                kwargs.pop(key)
        return BindableNamespace(**kwargs)

    ### PUBLIC METHODS ###

    @Bindable(rebroadcast=True)
    def play(self, state):
        if not self.is_allocated:
            return False
        if state:
            if self._synth.is_allocated:
                self._synth.unrelease()
            else:
                # TODO: build synth kwargs, using synthdef
                kwargs = dict(self._bindable_namespace)
                kwargs.update(self.synth_kwargs)
                self._synth.allocate(**kwargs)
        elif self._synth.is_allocated:
            self._synth.release()
        return state
