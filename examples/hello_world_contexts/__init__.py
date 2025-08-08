"""
Hello, world!, context-agnostic.

Let's play a C-major chord with different kinds of contexts, and compare what
needs to change between them, and what can stay the same.

Invoke with:

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    python -m examples.hello_world_contexts --help

... to see complete options.

See the :doc:`example documentation </examples/hello_world_contexts>` for a
complete explanation.
"""

import argparse
import asyncio
import time

import supriya


def play_synths(context: supriya.Context) -> list[supriya.Synth]:
    """
    Play a C-major chord on ``context``.
    """
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
    """
    Stop ``synths``.
    """
    # Loop over the synths and free them
    for synth in synths:
        synth.free()


def run_threaded() -> None:
    """
    Run the example on a realtime threaded
    :py:class:`~supriya.contexts.realtime.Server`.
    """
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
    """
    Run the example on an realtime async
    :py:class:`~supriya.contexts.realtime.AsyncServer`.
    """
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
    """
    Run the example on a non-realtime
    :py:class:`~supriya.contexts.nonrealtime.Score`.
    """
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
    """
    Parse CLI arguments.
    """
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
    """
    The example entry-point function.
    """
    parsed_args = parse_args(args)
    if parsed_args.realtime_threaded:
        run_threaded()
    elif parsed_args.realtime_async:
        asyncio.run(run_async())
    elif parsed_args.nonrealtime:
        run_nonrealtime()


if __name__ == "__main__":
    main()
