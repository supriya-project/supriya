from typing import Tuple


def midi_note_number_to_frequency(midi_note_number):
    return pow(2.0, (midi_note_number - 69) / 12) * 440.0


def midi_velocity_to_amplitude(midi_velocity):
    return pow(midi_velocity / 127.0, 2.0)


def midi_velocity_to_decibels(midi_velocity):
    pass


def amplitude_to_decibels(amplitude):
    pass


def decibels_to_amplitude(decibels):
    pass


def measure_to_offset(
    measure: int,
    time_signature: Tuple[int, int],
    previous_measure: int,
    previous_time_signature_change_offset: float,
) -> float:
    return (
        (measure - previous_measure) * (time_signature[0] / time_signature[1])
    ) + previous_time_signature_change_offset


def offset_to_measure(
    offset: float,
    time_signature: Tuple[int, int],
    previous_measure: int,
    previous_time_signature_change_offset: float,
) -> int:
    return (
        int(
            (offset - previous_time_signature_change_offset)
            // (time_signature[0] / time_signature[1])
        )
        + previous_measure
    )


def offset_to_measure_offset(
    offset: float,
    time_signature: Tuple[int, int],
    previous_time_signature_change_offset: float,
) -> float:
    return (offset - previous_time_signature_change_offset) % (
        time_signature[0] / time_signature[1]
    )


def offset_to_seconds(
    beats_per_minute: float,
    current_offset: float,
    previous_offset: float,
    previous_seconds: float,
    beat_duration: float,
) -> float:
    return (
        (current_offset - previous_offset) / (beats_per_minute / 60) / beat_duration
    ) + previous_seconds


def seconds_to_offset(
    beats_per_minute: float,
    current_time: float,
    previous_offset: float,
    previous_seconds: float,
    beat_duration: float,
) -> float:
    return (
        (current_time - previous_seconds) * (beats_per_minute / 60) * beat_duration
    ) + previous_offset
