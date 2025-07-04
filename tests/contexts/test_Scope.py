import time
from typing import Generator, Literal

import pytest
from uqbar.strings import normalize

from supriya import Bus, BusGroup, Server, SynthDef, SynthDefBuilder
from supriya.ugens import Out, SinOsc


@pytest.fixture
def context(synthdef: SynthDef) -> Generator[Server, None, None]:
    context = Server().boot()
    with context.at():
        with context.add_synthdefs(synthdef):
            context.add_synth(synthdef=synthdef)
    context.sync()
    yield context
    context.quit()


@pytest.fixture
def synthdef() -> SynthDef:
    with SynthDefBuilder(frequency=440, out=0) as builder:
        Out.ar(bus=builder["out"], source=SinOsc.ar(frequency=builder["frequency"]))

    return builder.build(name="test:sine")


@pytest.mark.parametrize(
    "bus_index, expected_tree",
    [
        (
            0,
            """
            NODE TREE 0 group
                1 group
                    1000 test:sine
                        frequency: 440.0, out: 0.0
                1001 supriya:amp-scope-ar:1
                    in_: 0.0, max_frames: 4096.0, scope_frames: 4096.0, scope_id: 0.0
            """,
        ),
        (
            slice(0, 2),
            """
            NODE TREE 0 group
                1 group
                    1000 test:sine
                        frequency: 440.0, out: 0.0
                1001 supriya:amp-scope-ar:2
                    in_: 0.0, max_frames: 4096.0, scope_frames: 4096.0, scope_id: 0.0
            """,
        ),
    ],
)
def test_amplitude_scope(
    bus_index: int | slice, context: Server, expected_tree: str, synthdef: SynthDef
) -> None:
    bus_group = context.audio_output_bus_group
    buses: Bus | BusGroup
    if isinstance(bus_index, int):
        buses = bus_group[bus_index]
    else:
        start, stop, _ = bus_index.indices(len(bus_group))
        buses = BusGroup(
            calculation_rate=bus_group.calculation_rate,
            context=bus_group.context,
            count=stop - start,
            id_=start,
        )
    scope = context.add_amplitude_scope(bus=buses)
    context.sync()
    assert str(context.query_tree()) == normalize(expected_tree)
    results: list[tuple[int, list[float]]] = []
    for i in range(10):
        available_frames, data = scope.read()
        results.append((available_frames, data))
        print(
            f"{available_frames=} {data[:4]=} {scope.channel_count=} {scope.max_frames=}"
        )
        time.sleep(0.1)
    assert any([entry[0] for entry in results])
    assert all([any(entry[1]) for entry in results if entry[0]])
    scope.stop()


@pytest.mark.parametrize(
    "bus_index, fft_size, frequency_mode, expected_tree",
    [
        (
            0,
            4096,
            "linear",
            """
            NODE TREE 0 group
                1 group
                    1000 test:sine
                        frequency: 440.0, out: 0.0
                1001 supriya:freq-scope-lin-shm:1
                    fft_buffer_size: 4096.0, rate: 4.0, scope_id: 0.0, in_: 0.0
            """,
        ),
        # this one is "silent" because there's no output on the bus
        (
            4,
            8192,
            "linear",
            """
            NODE TREE 0 group
                1 group
                    1000 test:sine
                        frequency: 440.0, out: 0.0
                1001 supriya:freq-scope-lin-shm:1
                    fft_buffer_size: 8192.0, rate: 4.0, scope_id: 0.0, in_: 4.0
            """,
        ),
        (
            0,
            4096,
            "logarithmic",
            """
            NODE TREE 0 group
                1 group
                    1000 test:sine
                        frequency: 440.0, out: 0.0
                1001 supriya:freq-scope-log-shm:1
                    fft_buffer_size: 4096.0, rate: 4.0, scope_id: 0.0, in_: 0.0
            """,
        ),
    ],
)
def test_frequency_scope(
    bus_index: int,
    context: Server,
    expected_tree: str,
    fft_size: int,
    frequency_mode: Literal["linear", "logarithmic"],
    synthdef: SynthDef,
) -> None:
    bus_group = context.audio_output_bus_group
    scope = context.add_frequency_scope(
        bus=bus_group[bus_index],
        fft_size=fft_size,
        frequency_mode=frequency_mode,
    )
    context.sync()
    assert str(context.query_tree()) == normalize(expected_tree)
    results: list[tuple[int, list[float]]] = []
    for i in range(10):
        available_frames, data = scope.read()
        results.append((available_frames, data))
        print(
            f"{available_frames=} {data[:4]=} {scope.channel_count=} {scope.max_frames=}"
        )
        time.sleep(0.1)
    assert any([entry[0] for entry in results])
    assert all([any(entry[1]) for entry in results if entry[0]])
    scope.stop()
