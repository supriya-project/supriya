from typing import Set

from supriya.clock import TempoClock

from .bases import ApplicationObject


class Transport(ApplicationObject):
    def __init__(self):
        ApplicationObject.__init__(self)
        self._clock = TempoClock()
        self._dependencies: Set[ApplicationObject] = set()

    def _application_perform_callback(
        self,
        current_moment,
        desired_moment,
        event,
        midi_message,
    ):
        self.application.perform([midi_message], moment=current_moment)

    def perform(self, midi_messages):
        self._debug_tree(self, "Perform", suffix=repr([type(_).__name__ for _ in midi_messages]))
        if self.application is None:
            return
        self.schedule(self._application_perform_callback, args=midi_messages)
        if not self.is_running:
            self.start()

    def schedule(self, *args, **kwargs):
        self._clock.schedule(*args, **kwargs)

    def set_tempo(self, beats_per_minute: float):
        with self.lock([self]):
            self._clock.change(beats_per_minute=beats_per_minute)

    def set_time_signature(self, numerator, denominator):
        with self.lock([self]):
            self._clock.change(time_signature=[numerator, denominator])

    def start(self):
        with self.lock([self]):
            for dependency in self._dependencies:
                dependency.start()
            self._clock.start()

    def stop(self):
        with self.lock([self]):
            self._clock.stop()
            for dependency in self. dependencies:
                dependency.stop()

    @property
    def is_running(self):
        return self._clock.is_running
