from supriya.tools import patterntools
from supriya.tools import systemtools
from supriya.tools.livetools.PatternSlot import PatternSlot


class AutoPatternSlot(PatternSlot):

    ### INITIALIZER ###

    def __init__(
        self,
        name,
        track,
        pattern,
        synthdef=None,
        **kwargs
        ):
        self._event_player = None
        PatternSlot.__init__(
            self,
            name=name,
            track=track,
            pattern=pattern,
            synthdef=synthdef,
            **kwargs,
            )

    ### PUBLIC METHODS ###

    @systemtools.Bindable(rebroadcast=True)
    def play(self, state):
        if not self.is_allocated:
            return False
        if state and not self._event_player:
            kwargs = self.synth_kwargs
            kwargs['add_action'] = 'add_to_head'
            kwargs['target_node'] = self._group
            if self._synthdef is not None:
                kwargs['synthdef'] = self._synthdef
            pattern = patterntools.Pbindf(self._pattern, **kwargs)
            self._event_player = pattern.play()
        elif not state:
            self._event_player.stop()
            self._event_player = None
        return state

    def set_pattern(self, pattern):
        assert isinstance(pattern, patterntools.EventPattern)
        self._pattern = pattern
        if self._event_player is None:
            return
        self.play(False)
        self.play(True)
