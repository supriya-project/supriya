import time

import supriya

# A C-major chord
FREQUENCIES = [261.63, 329.63, 392.00]


def main() -> None:
    # Create a server and boot it:
    server = supriya.Server().boot()
    # Create an empty list to store synths in:
    synths: list[supriya.Synth] = []
    # Start an OSC bundle to run immediately:
    with server.at():
        # Add the default synthdef to the server and open a "completion" context
        # manager to group further commands for when the synthdef finishes loading:
        with server.add_synthdefs(supriya.default):
            # Loop over the frequencies:
            for frequency in FREQUENCIES:
                # Create a synth using the default synthdef and the frequency
                # and add it to the list of synths:
                synths.append(
                    server.add_synth(synthdef=supriya.default, frequency=frequency)
                )
    # Let the notes play for 4 seconds:
    time.sleep(4)
    # Loop over the synths and free them
    for synth in synths:
        synth.free()
    # Wait a second for the notes to fade out:
    time.sleep(1)
    # Quit the server:
    server.quit()


if __name__ == "__main__":
    main()
