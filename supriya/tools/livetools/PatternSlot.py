import abc
from supriya.tools import patterntools
from supriya.tools.livetools.Slot import Slot


class PatternSlot(Slot):

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        name,
        track,
        synthdef,
        pattern,
        **kwargs
        ):
        Slot.__init__(self, name, track, synthdef, **kwargs)
        if pattern is not None:
            self.set_pattern(pattern)

    ### PRIVATE METHODS ###

    def _setup_bindable_namespace(self, **kwargs):
        pass
