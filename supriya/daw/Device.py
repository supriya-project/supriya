from collections import deque
from typing import (
    Callable,
    Deque,
    Dict,
    Generator,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
)

from supriya.clock import Moment
from supriya.commands.Request import Request
from supriya.midi import MidiMessage, NoteOffMessage, NoteOnMessage

from .DawNode import DawNode


class Device(DawNode):

    ### CLASS VARIABLES ###

    class CaptureEntry(NamedTuple):
        moment: Moment
        label: str
        message: MidiMessage

    class Capture:
        def __init__(self, device: "Device"):
            self.device = device
            self.entries: List["Device.CaptureEntry"] = []

        def __enter__(self):
            self.device._captures.add(self)
            self.entries[:] = []
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.device._captures.remove(self)

        def __getitem__(self, i):
            return self.entries[i]

        def __iter__(self):
            return iter(self.entries)

        def __len__(self):
            return len(self.entries)

    ### INITIALIZER ###

    def __init__(self, *, channel_count=None, name=None):
        DawNode.__init__(self, channel_count=channel_count, name=name)
        self._captures: Set[Device.Capture] = set()
        self._event_handlers: Dict[
            Type[MidiMessage],
            Callable[[MidiMessage], Tuple[Sequence[MidiMessage], Sequence[Request]]],
        ] = {}
        self._input_note_numbers: Dict[float, List[float]] = {}
        self._output_note_numbers: Dict[float, List[float]] = {}

    ### PRIVATE METHODS ###

    def _update_captures(self, moment, message, label):
        if not self._captures:
            return
        entry = self.CaptureEntry(moment=moment, message=message, label=label)
        for capture in self._captures:
            capture.entries.append(entry)

    ### PUBLIC METHODS ###

    def capture(self):
        return self.Capture(self)

    def delete(self):
        self.parent.remove(self)

    def filter_in_midi_messages(
        self, in_midi_messages
    ) -> Generator[MidiMessage, None, None]:
        for message in in_midi_messages:
            if isinstance(message, NoteOnMessage) and not message.velocity:
                message = NoteOffMessage(
                    channel_number=message.channel_number,
                    note_number=message.note_number,
                    timestamp=message.timestamp,
                )
            yield message

    def filter_out_midi_messages(self, in_midi_messages) -> Sequence[MidiMessage]:
        result: List[MidiMessage] = []
        for message in in_midi_messages:
            if isinstance(message, NoteOnMessage):
                if (
                    message.velocity
                    and message.note_number not in self._output_note_numbers
                ):
                    self._output_note_numbers[message.note_number] = message.velocity
                    result.append(message)
                elif (
                    not message.velocity
                    and message.note_number in self._output_note_numbers
                ):
                    self._output_note_numbers.pop(message.note_number)
                    note_off_message = NoteOffMessage(
                        channel_number=message.channel_number,
                        note_number=message.note_number,
                        timestamp=message.timestamp,
                    )
                    result.append(note_off_message)
            elif (
                isinstance(message, NoteOffMessage)
                and message.note_number in self._output_note_numbers
            ):
                self._output_note_numbers.pop(message.note_number)
                result.append(message)
            else:
                result.append(message)
        return result

    def flush(self, moment=None):
        if not self._output_note_numbers:
            return
        performer = self.next_performer()
        if not performer:
            return
        midi_messages = [
            NoteOffMessage(note_number=note_number)
            for note_number in self._output_note_numbers
        ]
        self._output_note_numbers.clear()
        requests = self.perform_loop(moment, performer, midi_messages)
        self.application.send_requests(moment, requests)

    def next_performer(self) -> Optional[Callable]:
        if self.parent is None:
            return None
        index = self.parent.index(self)
        if index < len(self.parent) - 1:
            return self.parent[index + 1].perform
        for parent in self.parentage[1:]:
            if hasattr(parent, "perform_output"):
                return parent.perform_output
        return None

    def perform(
        self, moment, in_midi_messages
    ) -> Generator[
        Tuple[Optional[Callable], Sequence[MidiMessage], Sequence[Request]], None, None
    ]:
        next_performer = self.next_performer()
        if not self.ready:
            yield next_performer, in_midi_messages, ()
        out_midi_messages: List[MidiMessage] = []
        out_requests: List[Request] = []
        for message in self.filter_in_midi_messages(in_midi_messages):
            self._update_captures(moment, message, "I")
            event_handler = self._event_handlers.get(type(message))
            if not event_handler:
                out_midi_messages.append(message)
                continue
            messages, requests = event_handler(message)
            out_midi_messages.extend(messages)
            out_requests.extend(requests)
        for message in self.filter_out_midi_messages(out_midi_messages):
            self._update_captures(moment, message, "O")
        yield next_performer, out_midi_messages, out_requests

    @classmethod
    def perform_loop(cls, moment, performer, midi_messages) -> Sequence[Request]:
        requests: List[Request] = []
        stack: Deque = deque()
        stack.append((performer, midi_messages))
        while stack:
            in_performer, in_messages = stack.popleft()
            for out_performer, out_messages, out_requests in in_performer(
                moment, in_messages
            ):
                requests.extend(out_requests)
                if out_messages and out_performer:
                    stack.append((out_performer, out_messages))
        return requests
