import supriya.realtime
from supriya.tools import synthdeftools
from supriya.tools import systemtools
from supriya.tools.livetools.Slot import Slot


class SynthSlot(Slot):

    ### INITIALIZER ###

    def __init__(
        self,
        name,
        track,
        synthdef,
        **kwargs
        ):
        from supriya import synthdefs
        self._synthdef = synthdef or synthdefs.default
        Slot.__init__(self, name, track, self._synthdef, **kwargs)
        self._synth = supriya.realtime.Synth(
            synthdef=self._synthdef,
            **self.bindable_namespace
            )
        for key in self._bindable_namespace:
            systemtools.bind(self[key], self._synth.controls[key])

    ### PRIVATE METHODS ###

    def _setup_bindable_namespace(self, **kwargs):
        for name, parameter in self._synthdef.parameters.items():
            if parameter.parameter_rate in (
                synthdeftools.ParameterRate.AUDIO,
                synthdeftools.ParameterRate.SCALAR,
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
        return systemtools.BindableNamespace(**kwargs)

    ### PUBLIC METHODS ###

    @systemtools.Bindable(rebroadcast=True)
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
