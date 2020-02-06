import dataclasses
from typing import Optional


@dataclasses.dataclass
class MidiMessage:
    channel_number: Optional[int]
    timestamp: Optional[float]


@dataclasses.dataclass
class ControllerChangeMessage(MidiMessage):
    channel_number: Optional[int]
    controller_number: Optional[int]
    controller_value: Optional[int]
    timestamp: Optional[float]


@dataclasses.dataclass
class NoteOffMessage(MidiMessage):
    channel_number: Optional[int]
    pitch: Optional[int]
    timestamp: Optional[float]
    velocity: Optional[int]


@dataclasses.dataclass
class NoteOnMessage(MidiMessage):
    channel_number: Optional[int]
    pitch: Optional[int]
    timestamp: Optional[float]
    velocity: Optional[int]
