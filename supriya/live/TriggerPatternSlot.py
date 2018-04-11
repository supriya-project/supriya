import supriya.patterns
import supriya.realtime
from supriya.tools import systemtools
from supriya.live.PatternSlot import PatternSlot


class TriggerPatternSlot(PatternSlot):

    ### INITIALIZER ###

    def __init__(
        self,
        name,
        track,
        synthdef=None,
        pattern=None,
        maximum_replicas=64,
        **kwargs
        ):
        PatternSlot.__init__(
            self,
            name=name,
            track=track,
            pattern=pattern,
            synthdef=synthdef,
            **kwargs,
            )
        maximum_replicas = int(maximum_replicas)
        assert 0 < maximum_replicas
        self._maximum_replicas = maximum_replicas
        self._iterator = None
        if self._pattern is not None:
            self._iterator = iter(self._pattern)
        self._synths = []

    ### PUBLIC METHODS ###

    def set_pattern(self, pattern):
        assert isinstance(pattern, supriya.patterns.EventPattern)
        self._pattern = pattern
        self._iterator = iter(pattern)

    @systemtools.Bindable(rebroadcast=True)
    def trigger(self, state):
        from supriya import synthdefs
        if not self.is_allocated or not self._iterator:
            return state
        else:
            # clear out unallocated synths
            for synth in self._synths[:]:
                if not synth.is_allocated:
                    self._synths.remove(synth)
            try:
                event = next(self._iterator)
            except StopIteration:
                return state
            assert isinstance(event, supriya.patterns.NoteEvent)
            synthdef = (
                self.synthdef or
                event.get('synthdef') or
                synthdefs.default
                )
            settings = {
                key: value for key, value in event._settings.items()
                if value is not None
                }
            for synth_kwargs in event._expand(
                settings=settings,
                synthdef=synthdef,
                uuids=[],
                synth_parameters_only=True,
                ):
                synth_kwargs.update(self.synth_kwargs)
                synth = supriya.realtime.Synth(synthdef=synthdef)
                synth.allocate(**synth_kwargs)
                self._synths.append(synth)
            # release old surplus synths
            while len(self._synths) > self._maximum_replicas:
                synth = self._synths.pop(0)
                synth.release()
        return state

    ### PUBLIC PROPERTIES ###

    @property
    def maximum_replicas(self):
        return self._maximum_replicas
