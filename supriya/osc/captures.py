from typing import NamedTuple, Union

from .messages import OscBundle, OscMessage


class CaptureEntry(NamedTuple):
    timestamp: float
    label: str
    message: Union[OscMessage, OscBundle]


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
            for timestamp, label, osc_message in self.messages
            if label == "R"
        ]

    @property
    def sent_messages(self):
        return [
            (timestamp, osc_message)
            for timestamp, label, osc_message in self.messages
            if label == "S"
        ]
