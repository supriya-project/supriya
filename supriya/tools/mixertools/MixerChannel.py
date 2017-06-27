class MixerChannel:

    __slots__ = (
        '_gain',
        '_is_cued',
        '_is_muted',
        '_is_soloed',
        '_mixer',
        '_name',
        )

    def __init__(self, mixer, name=None):
        from supriya.tools import mixertools
        assert isinstance(mixer, mixertools.Mixer)
        self._gain = 0
        self._is_cued = False
        self._is_muted = False
        self._is_soloed = False
        self._mixer = mixer
        self._name = name

    def cue(self, state):
        pass

    def mute(self, state):
        pass

    def solo(self, state):
        pass

    def set_gain(self, gain):
        pass
