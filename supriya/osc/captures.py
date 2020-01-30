from typing import NamedTuple, Optional, Union

from supriya.commands.Requestable import Requestable
from supriya.commands.Response import Response

from .messages import OscBundle, OscMessage


class CaptureEntry(NamedTuple):
    timestamp: float
    label: str
    message: Union[OscMessage, OscBundle]
    command: Optional[Union[Requestable, Response]]


class Capture:

    ### INITIALIZER ###

    def __init__(self, osc_protocol):
        self.osc_protocol = osc_protocol
        self.messages = []

    ### SPECIAL METHODS ###

    def __enter__(self):
        self.osc_protocol.captures.add(self)
        self.messages[:] = []
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.osc_protocol.captures.remove(self)

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)

    ### PUBLIC PROPERTIES ###

    @property
    def received_messages(self):
        return [
            (timestamp, osc_message)
            for timestamp, label, osc_message, _ in self.messages
            if label == "R"
        ]

    @property
    def requests(self):
        return [
            (timestamp, command)
            for timestamp, label, _, command in self.messages
            if label == "S" and command is not None
        ]

    @property
    def responses(self):
        return [
            (timestamp, command)
            for timestamp, label, _, command in self.messages
            if label == "R" and command is not None
        ]

    @property
    def sent_messages(self):
        return [
            (timestamp, osc_message)
            for timestamp, label, osc_message, _ in self.messages
            if label == "S"
        ]
