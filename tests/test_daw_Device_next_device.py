from supriya.daw import AudioDevice, AudioRack, Instrument, MidiDevice, MidiRack, Track


def test_01():
    track = Track()

    midi_device = MidiDevice()

    midi_rack = MidiRack()
    midi_device_a1 = MidiDevice()
    midi_device_a2 = MidiDevice()
    midi_device_b1 = MidiDevice()
    midi_device_b2 = MidiDevice()
    midi_rack.add_chain().devices.extend([midi_device_a1, midi_device_a2])
    midi_rack.add_chain().devices.extend([midi_device_b1, midi_device_b2])

    instrument = Instrument()

    audio_rack = AudioRack()
    audio_device_a1 = AudioDevice()
    audio_device_a2 = AudioDevice()
    audio_device_b1 = AudioDevice()
    audio_device_b2 = AudioDevice()
    audio_rack.add_chain().devices.extend([audio_device_a1, audio_device_a2])
    audio_rack.add_chain().devices.extend([audio_device_b1, audio_device_b2])

    track.devices.extend([midi_device, midi_rack, instrument, audio_rack])

    assert audio_device_a1.next_device() is audio_device_a2
    assert audio_device_a2.next_device() is None
    assert audio_device_b1.next_device() is audio_device_b2
    assert audio_device_b2.next_device() is None
    assert audio_rack.next_device() is None
    assert instrument.next_device() is audio_rack
    assert midi_device.next_device() is midi_rack
    assert midi_device_a1.next_device() is midi_device_a2
    assert midi_device_a2.next_device() is instrument
    assert midi_device_b1.next_device() is midi_device_b2
    assert midi_device_b2.next_device() is instrument
    assert midi_rack.next_device() is instrument
