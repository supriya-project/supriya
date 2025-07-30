import logging
import time

import supriya


def play_synths(context: supriya.Context) -> list[supriya.Synth]:
    # A C-major chord
    frequencies = [261.63, 329.63, 392.00]
    # Create an empty list to store synths in:
    synths: list[supriya.Synth] = []
    # Add the default synthdef to the server and open a "completion" context
    # manager to group further commands for when the synthdef finishes loading:
    with context.add_synthdefs(supriya.default):
        # Loop over the frequencies:
        for frequency in frequencies:
            # Create a synth using the default synthdef and the frequency
            # and add it to the list of synths:
            synths.append(
                context.add_synth(synthdef=supriya.default, frequency=frequency)
            )
    return synths


def stop_synths(synths: list[supriya.Synth]) -> None:
    # Loop over the synths and free them
    for synth in synths:
        synth.free()


def debug(
    header: str, server: supriya.Server, transcript: supriya.osc.Capture | None = None
) -> None:
    # Print a header:
    print(header)
    # Print the server status
    print(f"Server status: {server.status}")
    # Print the node tree:
    print(server.query_tree())
    # Filter the OSC transcript down to just non-status sent messages and print them:
    if transcript is not None:
        for message in transcript.filtered(sent=True, received=False, status=False):
            print(f"Sent: {message!r}")


def main() -> None:
    # Turn on basic logging system-wide
    logging.basicConfig(level=logging.WARN)
    # Set Supriya's supriya.scsynth logger level to INFO
    logging.getLogger("supriya.scsynth").setLevel(logging.INFO)
    # Create a server and boot it:
    server = supriya.Server().boot()
    # Debug:
    debug("BEFORE PLAYING:", server)
    # Create an empty list to store synths in:
    synths: list[supriya.Synth] = []
    # Capture the OSC messages send to the server to load the SynthDef and create the synths:
    with server.osc_protocol.capture() as transcript:
        # N.B. This block is now indented inside the .capture() context manager
        # Start an OSC bundle to run immediately:
        with server.at():
            # Start playing the synths
            synths = play_synths(context=server)
    # Sync the server so we can see the node tree updates:
    server.sync()
    # Debug:
    debug("PLAYING:", server, transcript)
    # Let the notes play for 4 seconds:
    time.sleep(4)
    # Print a header:
    debug("JUST BEFORE STOPPING:", server)
    # Capture the OSC messages send to the server to free the synths:
    with server.osc_protocol.capture() as transcript:
        # N.B. This block is now indented inside the .capture() context manager
        # Loop over the synths and free them
        stop_synths(synths)
    # Debug:
    debug("AFTER STOPPING:", server, transcript)
    # Wait a second for the notes to fade out:
    time.sleep(1)
    # Print a header:
    debug("A LITTLE AFTER STOPPING:", server, transcript)
    # Quit the server:
    server.quit()


if __name__ == "__main__":
    main()
