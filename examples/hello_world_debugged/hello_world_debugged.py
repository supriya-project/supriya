import contextlib
import logging
import time
from typing import Generator

import supriya


def play_synths(context: supriya.Context) -> list[supriya.Synth]:
    # Start an OSC bundle to run immediately:
    with context.at():
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


def stop_synths(context: supriya.Context, synths: list[supriya.Synth]) -> None:
    # Start an OSC bundle to run immediately:
    with context.at():
        # Loop over the synths and free them
        for synth in synths:
            synth.free()


@contextlib.contextmanager
def debug(
    header: str,
    server: supriya.Server,
) -> Generator[None, None, None]:
    # Capture any OSC messages sent or received
    with server.osc_protocol.capture() as transcript:
        # Yield to the with block body
        yield
    # Print a header
    print(header)
    # Print the server status
    print(f"    Status: {server.status}")
    # Filter out any /status or /status.reply messages from the transcript
    if len(entries := transcript.filtered()):
        print("    Transcript:")
    # Print the OSC transcript's filtered, captured messages
    for entry in entries:
        print(f"        {'Recv' if entry.label == 'R' else 'Sent'}: {entry.message!r}")
    # Print the node tree
    for line in str(server.query_tree()).splitlines():
        print(f"    Tree: {line}")


def main() -> None:
    # Turn on basic logging output interpreter-wide
    logging.basicConfig(level=logging.WARN)

    # Set Supriya's supriya.scsynth logger level to INFO
    logging.getLogger("supriya.scsynth").setLevel(logging.INFO)

    # Create a server and boot it:
    server = supriya.Server().boot()

    # Print debug info before we play anything
    with debug("BEFORE PLAYING:", server):
        pass

    # Print debug info immediately after we play the synths
    with debug("IMMEDIATELY AFTER PLAYING:", server):
        # Start playing the synths
        synths = play_synths(context=server)

    # Print debug info after syncing with the server
    with debug("PLAYING:", server):
        server.sync()

    # Print debug info after 4 seconds of waiting
    with debug("JUST BEFORE STOPPING:", server):
        time.sleep(4)

    # Print debug info immediately after stopping the synths
    with debug("IMMEDIATELY AFTER STOPPING:", server):
        stop_synths(context=server, synths=synths)

    # Print debug info after 1 second of waiting
    with debug("AFTER RELEASING:", server):
        time.sleep(1)

    # Quit the server
    server.quit()


if __name__ == "__main__":
    main()
