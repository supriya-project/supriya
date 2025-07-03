import aifc
import logging
import platform

import pytest

from supriya import default, output_path, render
from supriya.contexts.nonrealtime import Score

# 3.13 would exit with 0
# develop as of 2025/02/11 exits with -11 (why??)
EXPECTED_EXIT_CODES_NIX = (0, -11)
# I simply do not understand why Windows is like this
EXPECTED_EXIT_CODES_WINDOWS = (1, 3221226505, 3221225477)


@pytest.fixture(autouse=True)
def use_caplog(caplog) -> None:
    caplog.set_level(logging.DEBUG)


@pytest.fixture
def context() -> Score:
    context = Score()
    with context.at(0):
        with context.add_synthdefs(default):
            context.add_synth(default, frequency=440.0)
    with context.at(1):
        context.add_synth(default, frequency=550.0)
    with context.at(2):
        context.add_synth(default, frequency=660.0)
    with context.at(3):
        context.do_nothing()
    return context


HASHES = [
    "5b07512abbcdd4d5b41209007897606e7775614d77a701cd9319412ed60ad4b9",
    "002481bceb377fbae290121c7013d935fe7f7da9d31a4dbf0591656570386483",
    "0cd77ffdd61b7c16797fb12e17d8e9ce10ceeaf726ecd09822f47c90350d52e8",
    "bf01598980d868e00d7d82a0090a3e691dec0f5e6d54d18c688463ca6aa2925f",
    "0ed76eb72244131f2d17d40aabe9d641bc630ac399c63aac83d2c5bce21ef03e",
    "5b07512abbcdd4d5b41209007897606e7775614d77a701cd9319412ed60ad4b9",
    "a81e6e39461983b37bfd23189e5c85da0aa72a29bf8ffd4a6fe287514fa2a677",
    "5b07512abbcdd4d5b41209007897606e7775614d77a701cd9319412ed60ad4b9",
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ", ".join(
        [
            "render_kwargs",
            "expected_path",
            "expected_channel_count",
            "expected_duration",
            "expected_sample_rate",
        ]
    ),
    [
        (
            lambda path: dict(),
            lambda path: output_path / f"score-{HASHES[0]}.aiff",
            8,
            3.0,
            44100,
        ),
        (
            lambda path: dict(duration=1.5),
            lambda path: output_path / f"score-{HASHES[1]}.aiff",
            8,
            1.5,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=2.5),
            lambda path: output_path / f"score-{HASHES[2]}.aiff",
            2,
            2.5,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=3.0),
            lambda path: output_path / f"score-{HASHES[3]}.aiff",
            2,
            3.0,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=3.5),
            lambda path: output_path / f"score-{HASHES[4]}.aiff",
            2,
            3.5,
            44100,
        ),
        (
            lambda path: dict(render_directory_path=path),
            lambda path: output_path / f"score-{HASHES[5]}.aiff",
            8,
            3.0,
            44100,
        ),
        (
            lambda path: dict(output_file_path=path / "foo.aiff"),
            lambda path: path / "foo.aiff",
            8,
            3.0,
            44100,
        ),
        (
            lambda path: dict(sample_rate=48000),
            lambda path: output_path / f"score-{HASHES[6]}.aiff",
            8,
            3.0,
            48000,
        ),
        (lambda path: dict(suppress_output=True), lambda path: None, 8, 3.0, 44100),
    ],
)
async def test_render(
    context: Score,
    expected_channel_count,
    expected_duration,
    expected_path,
    expected_sample_rate,
    render_kwargs,
    tmp_path,
) -> None:
    actual_path, actual_exit_code = await context.render(**render_kwargs(tmp_path))
    assert actual_exit_code in (
        EXPECTED_EXIT_CODES_WINDOWS
        if platform.system() == "Windows"
        else EXPECTED_EXIT_CODES_NIX
    )
    assert actual_path == expected_path(tmp_path)
    if actual_path is None:
        return
    assert actual_path.exists()
    with actual_path.open("rb") as file_pointer:
        aifc_file = aifc.open(file_pointer)
        (
            actual_channel_count,
            _,
            actual_sample_rate,
            actual_frame_count,
            _,
            _,
        ) = aifc_file.getparams()
        assert actual_channel_count == expected_channel_count
        assert actual_sample_rate == expected_sample_rate
        assert round(actual_frame_count / actual_sample_rate, 2) == expected_duration


def test___render__(context: Score) -> None:
    expected_path = output_path / f"score-{HASHES[7]}.aiff"
    if expected_path.exists():
        expected_path.unlink()
    actual_path, actual_exit_code = render(context)
    assert actual_exit_code in (
        EXPECTED_EXIT_CODES_WINDOWS
        if platform.system() == "Windows"
        else EXPECTED_EXIT_CODES_NIX
    )
    assert actual_path == expected_path
    with expected_path.open("rb") as file_pointer:
        aifc_file = aifc.open(file_pointer)
        (
            actual_channel_count,
            _,
            actual_sample_rate,
            actual_frame_count,
            _,
            _,
        ) = aifc_file.getparams()
        assert actual_channel_count == 8
        assert actual_sample_rate == 44100
        assert round(actual_frame_count / actual_sample_rate, 2) == 3.0
