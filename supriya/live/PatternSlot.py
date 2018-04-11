import abc
import supriya.system
from supriya.live.Slot import Slot


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
        self._pattern = None
        if pattern is not None:
            self.set_pattern(pattern)

    ### PRIVATE METHODS ###

    def _setup_bindable_namespace(self, **kwargs):
        for key in tuple(kwargs):
            if key in ('in_', 'out', 'gate'):
                kwargs.pop(key)
        return supriya.system.BindableNamespace(**kwargs)
