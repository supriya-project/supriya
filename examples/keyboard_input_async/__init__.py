"""
Keyboard input, async.

Let's revisit playing live with either a MIDI keyboard or our QWERTY keyboard,
but this time using the asyncio framework.

Invoke with:

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    python -m examples.keyboard_input_async --help

... to see complete options.

See the :doc:`example documentation </examples/keyboard_input_async>` for a
complete explanation.

"""

import asyncio
import signal

import rtmidi

import supriya

from ..keyboard_input import (
    InputHandler,
    MidiHandler,
    NoteOff,
    NoteOn,
    PolyphonyManager,
    QwertyHandler,
    parse_args,
)


async def run(input_handler: InputHandler) -> None:
    """
    Run the script.
    """

    async def on_boot(*args) -> None:  # run this during server.boot()
        server.add_synthdefs(polyphony.synthdef)  # add the polyphony's synthdef
        await server.sync()  # wait for the synthdef to load before moving on

    async def on_quitting(*args) -> None:  # run this during server.quit()
        polyphony.free_all()  # free all the synths
        await asyncio.sleep(0.5)  # wait for them to fade out before moving on

    def signal_handler(*args) -> None:
        exit_future.set_result(True)  # set the exit future flag

    def input_callback(event: NoteOn | NoteOff) -> None:
        # drop the event onto the queue
        loop.call_soon_threadsafe(queue.put_nowait, event)

    async def queue_consumer() -> None:
        while True:  # run forever
            # grab an event off the queue and play it
            polyphony.perform(await queue.get())

    # grab a reference to the current event loop
    loop = asyncio.get_event_loop()
    # create a future we can wait on to quit the script
    exit_future: asyncio.Future[bool] = loop.create_future()
    # create a server and polyphony manager
    server = supriya.AsyncServer()
    polyphony = PolyphonyManager(server=server)
    # setup lifecycle callbacks
    server.register_lifecycle_callback("BOOTED", on_boot)
    server.register_lifecycle_callback("QUITTING", on_quitting)
    # hook up Ctrl-C so we can gracefully shutdown the server
    loop.add_signal_handler(signal.SIGINT, signal_handler)
    # boot the server and let the user know we're ready to play
    await server.boot()
    print("Server online. Press Ctrl-C to exit.")
    # setup an event queue, turn on the input handler, and teach the input
    # handler to callback against the queue
    queue: asyncio.Queue[NoteOn | NoteOff] = asyncio.Queue()
    # setup a queue consumer task to run asynchronously
    queue_consumer_task = loop.create_task(queue_consumer())
    # turn on the input handler and teach it to callback against the queue
    with input_handler.listen(callback=input_callback):
        await exit_future  # wait for Ctrl-C
    queue_consumer_task.cancel()  # cancel the queue consumer task
    # stop the input handler and quit the server
    await server.quit()


def main(args: list[str] | None = None) -> None:
    """
    The example entry-point function.
    """
    parsed_args = parse_args(args)
    if parsed_args.list_midi_inputs:
        # print out available MIDI input ports
        rtmidi.midiutil.list_input_ports()
    elif parsed_args.use_midi is not None:
        asyncio.run(run(MidiHandler(port=parsed_args.use_midi)))
    elif parsed_args.use_qwerty:
        asyncio.run(run(QwertyHandler()))


if __name__ == "__main__":
    main()
