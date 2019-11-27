import time

import pytest

from supriya.realtime import BusGroup, Server, Synth
from supriya.xdaw.sends import Send


@pytest.fixture
def server():
    server = Server.default().boot()
    yield server
    server.quit()


def prepare(server, input_count, output_count, indices):
    synthdef = Send.build_synthdef(
        input_count, output_count, calculation_rate="control"
    )
    input_buses = BusGroup.control(input_count).allocate(server=server)
    output_buses = BusGroup.control(output_count).allocate(server=server)
    synth = Synth(synthdef=synthdef, in_=int(input_buses), out=int(output_buses))
    synth.allocate(server=server)
    for index in indices:
        input_buses[index].set(1.0)
    time.sleep(0.1)
    amplitudes = output_buses.get()
    return [round(x, 3) for x in amplitudes]


@pytest.mark.parametrize(
    "input_count, output_count, indices, expected",
    [
        (1, 2, [0], [1.0, 1.0]),
        (1, 4, [0], [1.0, 1.0, 1.0, 1.0]),
        (1, 8, [0], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
        (2, 1, [0, 1], [1.0]),
        (2, 1, [0], [0.5]),
        (2, 1, [1], [0.5]),
        (4, 1, [0, 1, 2, 3], [1.0]),
        (4, 1, [0], [0.25]),
        (4, 1, [1], [0.25]),
        (4, 1, [2], [0.25]),
        (4, 1, [3], [0.25]),
        (8, 1, [0, 1, 2, 3, 4, 5, 6, 7], [1.0]),
        (8, 1, [0], [0.125]),
        (8, 1, [1], [0.125]),
        (8, 1, [2], [0.125]),
        (8, 1, [3], [0.125]),
        (8, 1, [4], [0.125]),
        (8, 1, [5], [0.125]),
        (8, 1, [6], [0.125]),
        (8, 1, [7], [0.125]),
    ],
)
def test_uni(server, input_count, output_count, indices, expected):
    assert prepare(server, input_count, output_count, indices) == expected


@pytest.mark.parametrize(
    "input_count, output_count, indices, expected",
    [
        (1, 1, [0], [1.0]),
        (2, 2, [0, 1], [1.0, 1.0]),
        (2, 2, [0], [1.0, 0.0]),
        (2, 2, [1], [0.0, 1.0]),
        (4, 4, [0, 1, 2, 3], [1.0, 1.0, 1.0, 1.0]),
        (4, 4, [0], [1.0, 0.0, 0.0, 0.0]),
        (4, 4, [1], [0.0, 1.0, 0.0, 0.0]),
        (4, 4, [2], [0.0, 0.0, 1.0, 0.0]),
        (4, 4, [3], [0.0, 0.0, 0.0, 1.0]),
        (8, 8, [0, 1, 2, 3, 4, 5, 6, 7], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
        (8, 8, [0], [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        (8, 8, [1], [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        (8, 8, [2], [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        (8, 8, [3], [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]),
        (8, 8, [4], [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]),
        (8, 8, [5], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]),
        (8, 8, [6], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]),
        (8, 8, [7], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]),
    ],
)
def test_same(server, input_count, output_count, indices, expected):
    assert prepare(server, input_count, output_count, indices) == expected


@pytest.mark.parametrize(
    "input_count, output_count, indices, expected",
    [
        (2, 4, [0, 1], [1.0, 1.0, 1.0, 1.0]),
        (2, 4, [0], [1.0, 1.0, 0.0, 0.0]),
        (2, 4, [1], [0.0, 0.0, 1.0, 1.0]),
        (2, 8, [0, 1], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
        (2, 8, [0], [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]),
        (2, 8, [1], [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]),
        (4, 8, [0, 1, 2, 3], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
        (4, 8, [0], [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        (4, 8, [1], [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]),
        (4, 8, [2], [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0]),
        (4, 8, [3], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0]),
    ],
)
def test_upmix(server, input_count, output_count, indices, expected):
    assert prepare(server, input_count, output_count, indices) == expected


@pytest.mark.parametrize(
    "input_count, output_count, indices, expected",
    [
        (4, 2, [0, 1, 2, 3], [1.0, 1.0]),
        (4, 2, [0], [0.414, 0.0]),
        (4, 2, [1], [0.293, 0.293]),
        (4, 2, [2], [0.0, 0.414]),
        (4, 2, [3], [0.293, 0.293]),
        (8, 2, [0, 1, 2, 3, 4, 5, 6, 7], [1.0, 1.0]),
        (8, 2, [0], [0.199, 0.0]),
        (8, 2, [1], [0.184, 0.076]),
        (8, 2, [2], [0.141, 0.141]),
        (8, 2, [3], [0.076, 0.184]),
        (8, 2, [4], [0.0, 0.199]),
        (8, 2, [5], [0.076, 0.184]),
        (8, 2, [6], [0.141, 0.141]),
        (8, 2, [7], [0.184, 0.076]),
        (8, 4, [0, 1, 2, 3, 4, 5, 6, 7], [1.0, 1.0, 1.0, 1.0]),
        (8, 4, [0], [0.414, 0.0, 0.0, 0.0]),
        (8, 4, [1], [0.293, 0.293, 0.0, 0.0]),
        (8, 4, [2], [0.0, 0.414, 0.0, 0.0]),
        (8, 4, [3], [0.0, 0.293, 0.293, 0.0]),
        (8, 4, [4], [0.0, 0.0, 0.414, 0.0]),
        (8, 4, [5], [0.0, 0.0, 0.293, 0.293]),
        (8, 4, [6], [0.0, 0.0, 0.0, 0.414]),
        (8, 4, [7], [0.293, 0.0, 0.0, 0.293]),
    ],
)
def test_downmix(server, input_count, output_count, indices, expected):
    assert prepare(server, input_count, output_count, indices) == expected
