import abc


class Device:
    @abc.abstractmethod
    def activate(self):
        raise NotImplementedError

    @abc.abstractmethod
    def deactivate(self):
        raise NotImplementedError

    @abc.abstractmethod
    def allocate(self):
        raise NotImplementedError

    @abc.abstractmethod
    def free(self):
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self, moment):
        raise NotImplementedError

    @abc.abstractmethod
    def perform(self, moment, midi_messages=None):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def is_active(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def has_midi_inputs(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def has_midi_outputs(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def has_audio_inputs(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def has_audio_outputs(self):
        raise NotImplementedError
