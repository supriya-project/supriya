from typing import Set

from supriya.clock import TempoClock

from .bases import ApplicationObject


class Transport(ApplicationObject):
    def __init__(self):
        ApplicationObject.__init__(self)
        self._clock = TempoClock()
        self._dependencies: Set[ApplicationObject] = set()

    def perform(self, midi_messages):
        if self.application is None:
            return
        self.schedule(self.application.perform, args=[midi_messages])
        if not self.is_running:
            self.start()

    def set_tempo(self, beats_per_minute: float):
        with self.lock([self]):
            self._clock.change(beats_per_minute=beats_per_minute)

    def set_time_signature(self, numerator, denominator):
        with self.lock([self]):
            self._clock.change(time_signature=[numerator, denominator])

    def start(self):
        with self.lock([self]):
            for dependency in self.dependencies:
                dependency.start()
            self._clock.start()

    def stop(self):
        with self.lock([self]):
            self._clock.stop()
            for dependency in self.dependencies:
                dependency.stop()

    @property
    def is_running(self):
        return self._clock.is_running
