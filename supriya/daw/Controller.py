import rtmidi
from supriya.midi import ControllerChangeMessage, NoteOffMessage, NoteOnMessage


class Controller:

    ### INITIALIZER ###

    def __init__(self):
        self.is_running = False
        self.midi_in = rtmidi.MidiIn()
        self.midi_out = rtmidi.MidiOut()
        self.callbacks = set()

    ### PRIVATE METHODS ###

    def _callback(self, *args):
        data, timestamp = args[0]
        status_byte, data = data[0], data[1:]
        message_type = status_byte >> 4
        channel_number = status_byte & 0x0F
        if message_type == 8:
            message = NoteOffMessage(
                channel_number=channel_number,
                note_number=data[0],
                velocity=data[1],
                timestamp=timestamp,
            )
        elif message_type == 9:
            message = NoteOnMessage(
                channel_number=channel_number,
                note_number=data[0],
                velocity=data[1],
                timestamp=timestamp,
            )
        elif message_type == 11:
            message = ControllerChangeMessage(
                channel_number=channel_number,
                controller_number=data[0],
                controller_value=data[1],
                timestamp=timestamp,
            )
        else:
            raise ValueError(data)
        for callback in self.callbacks:
            callback(message)

    ### PUBLIC METHODS ###

    def boot(self, port_number=0, virtual=False):
        if virtual:
            ports_before = self.midi_in.get_ports()
            self.midi_out.open_virtual_port(name="virtual")
            ports_after = self.midi_in.get_ports()
            midi_out_port_name = list(set(ports_after).difference(ports_before))[0]
            for port_number, port in enumerate(ports_after):
                if port == midi_out_port_name:
                    self.midi_in.open_port(port_number)
                    break
            else:
                raise IOError("Could not find MIDI output port.")
        else:
            self.midi_in.open_port(port=port_number)
            self.midi_out.open_port(port=port_number)
        self.midi_in.set_callback(self._callback)
        self.is_running = True

    def register(self, callback):
        self.callbacks.add(callback)

    def quit(self):
        self.midi_in.close_port()
        self.midi_out.close_port()
        self.is_running = False

    def send_message(self, message):
        self.midi_out.send_message(message)

    def unregister(self, callback):
        self.callbacks.remove(callback)
