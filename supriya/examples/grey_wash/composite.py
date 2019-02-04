import supriya

from . import project_settings, sessions, synthdefs

session = supriya.Session.from_project_settings(project_settings)

with session.at(0):
    chants_buffer = session.add_buffer(file_path=sessions.chants)
    choral_wash_buffer = session.add_buffer(file_path=sessions.choral_wash)
    lost_and_found_buffer = session.add_buffer(file_path=sessions.lost_and_found)
    noise_wash_buffer = session.add_buffer(file_path=sessions.noise_wash)
    chants_buffer.normalize()
    choral_wash_buffer.normalize()
    lost_and_found_buffer.normalize()
    noise_wash_buffer.normalize()

with session.at(0):
    session.add_synth(
        buffer_id=chants_buffer,
        synthdef=synthdefs.player_synthdef,
        duration=90,
        fade_in_duration=5,
        fade_out_duration=85,
        gain=6,
    )

with session.at(15):
    session.add_synth(
        buffer_id=noise_wash_buffer,
        synthdef=synthdefs.player_synthdef,
        duration=150,
        fade_in_duration=30,
        fade_out_duration=60,
        gain=-12,
    )

with session.at(90):
    session.add_synth(
        buffer_id=lost_and_found_buffer,
        synthdef=synthdefs.player_synthdef,
        duration=150,
        fade_in_duration=60,
        fade_out_duration=60,
    )

with session.at(120):
    session.add_synth(
        buffer_id=choral_wash_buffer,
        synthdef=synthdefs.player_synthdef,
        duration=180,
        fade_in_duration=60,
        fade_out_duration=60,
        gain=-6,
    )

with session.at(210):
    session.add_synth(
        buffer_id=chants_buffer,
        synthdef=synthdefs.player_synthdef,
        duration=90,
        fade_in_duration=80,
        fade_out_duration=10,
    )
