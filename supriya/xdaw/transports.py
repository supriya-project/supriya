import enum
from typing import Dict, Set, Union

from supriya.clock import TempoClock

from .bases import ApplicationObject
from .parameters import Action, Float, Parameter, ParameterGroup


class Transport(ApplicationObject):

    ### CLASS VARIABLES ###

    class EventType(enum.IntEnum):
        CHANGE = 0
        SCHEDULE = 1
        MIDI_PERFORM = 2
        DEVICE_NOTE_OFF = 3
        DEVICE_NOTE_ON = 4
        CLIP_LAUNCH = 5
        CLIP_EDIT = 6
        CLIP_PERFORM = 7

    ### INITIALIZER ###

    def __init__(self):
        ApplicationObject.__init__(self)
        self._parameter_group = ParameterGroup()
        self._parameters: Dict[str, Union[Action, Parameter]] = {}
        self._add_parameter(Action("start", lambda client: client.start()))
        self._add_parameter(Action("stop", lambda client: client.stop()))
        self._add_parameter(
            Parameter(
                "tempo",
                Float(default=120, minimum=1, maximum=1000),
                callback=lambda client, value: client._set_tempo(value),
            )
        )
        self._clock = TempoClock()
        self._dependencies: Set[ApplicationObject] = set()
        self._mutate(slice(None), [self._parameter_group])

    ### PRIVATE METHODS ###

    def _application_perform_callback(
        self, current_moment, desired_moment, event, midi_message
    ):
        self.application.perform([midi_message], moment=current_moment)

    def _set_tempo(self, beats_per_minute):
        self._clock.change(beats_per_minute=beats_per_minute)

    ### PUBLIC METHODS ###

    def perform(self, midi_messages):
        if (
            self.application is None
            or self.application.status != self.application.Status.REALTIME
        ):
            return
        self._debug_tree(
            self, "Perform", suffix=repr([type(_).__name__ for _ in midi_messages])
        )
        self.schedule(self._application_perform_callback, args=midi_messages)
        if not self.is_running:
            self.start()

    def cue(self, *args, **kwargs):
        self._clock.cue(*args, **kwargs)

    def schedule(self, *args, **kwargs):
        self._clock.schedule(*args, **kwargs)

    def serialize(self):
        return {
            "kind": type(self).__name__,
            "spec": {
                "tempo": self._clock.beats_per_minute,
                "time_signature": "{}/{}".format(*self._clock.time_signature),
            },
        }

    def set_tempo(self, beats_per_minute: float):
        with self.lock([self]):
            self._set_tempo(beats_per_minute)

    def set_time_signature(self, numerator, denominator):
        with self.lock([self]):
            self._clock.change(time_signature=[numerator, denominator])

    def start(self):
        with self.lock([self]):
            for dependency in self._dependencies:
                dependency._start()
            self._clock.start()

    def stop(self):
        self._clock.stop()
        with self.lock([self]):
            for dependency in self._dependencies:
                dependency._stop()
            self.application.flush()

    ### PUBLIC PROPERTIES ###

    @property
    def is_running(self):
        return self._clock.is_running

    @property
    def parameters(self):
        return self._parameters
