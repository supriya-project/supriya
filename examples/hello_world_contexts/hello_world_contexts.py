import argparse
import asyncio
import time

import supriya


def play_synths(context: supriya.Context) -> list[supriya.Synth]:
    # Define a C-major chord in Hertz
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


def run_threaded() -> None:
    # Create a server and boot it:
    server = supriya.Server().boot()
    # Start an OSC bundle to run immediately:
    with server.at():
        # Start playing the synths
        synths = play_synths(context=server)
    # Let the notes play for 4 seconds:
    time.sleep(4)
    # Loop over the synths and free them:
    stop_synths(synths)
    # Wait a second for the notes to fade out:
    time.sleep(1)
    # Quit the server:
    server.quit()


async def run_async() -> None:
    # Create an async server and boot it:
    server = await supriya.AsyncServer().boot()
    # Start an OSC bundle to run immediately:
    with server.at():
        # Start playing the synths:
        synths = play_synths(context=server)
    # Let the notes play for 4 seconds:
    await asyncio.sleep(4)
    # Loop over the synths and free them:
    stop_synths(synths)
    # Wait a second for the notes to fade out:
    await asyncio.sleep(1)
    # Quit the async server:
    await server.quit()


def run_nonrealtime() -> None:
    # Create a score with stereo outputs:
    score = supriya.Score(output_bus_channel_count=2)
    # Start an OSC bundle to run at 0 seconds:
    with score.at(0):
        # Start playing the synths:
        synths = play_synths(context=score)
    # Start an OSC bundle to run at 4 seconds:
    with score.at(4):
        # Loop over the synths and free them:
        stop_synths(synths)
    # Start an OSC bundle to run at 5 seconds:
    with score.at(5):
        # A no-op message to tell the score there's nothing left to do:
        score.do_nothing()
    # Render the score to disk and open the soundfile:
    supriya.play(score)


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Play a C-major chord via different kinds of contexts"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--realtime-threaded",
        action="store_true",
        help="use a realtime threaded Server",
    )
    group.add_argument(
        "--realtime-async",
        action="store_true",
        help="use a realtime asyncio-enabled AsyncServer",
    )
    group.add_argument(
        "--nonrealtime", action="store_true", help="use a non-realtime Score"
    )
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> None:
    parsed_args = parse_args(args)
    if parsed_args.realtime_threaded:
        run_threaded()
    elif parsed_args.realtime_async:
        asyncio.run(run_async())
    else:
        run_nonrealtime()


if __name__ == "__main__":
    main()
