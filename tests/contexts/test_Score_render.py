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
EXPECTED_EXIT_CODES_WINDOWS = (3221226505, 3221225477)


@pytest.fixture(autouse=True)
def use_caplog(caplog):
    caplog.set_level(logging.DEBUG)


@pytest.fixture
def context():
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
            lambda path: output_path
            / "score-1f2fad799464ced28d0af160e819d261488c4361ca8a32288f742f6e8e0fb01a.aiff",
            8,
            3.0,
            44100,
        ),
        (
            lambda path: dict(duration=1.5),
            lambda path: output_path
            / "score-d50ec5c18a801a6f0b2a2e61e65b1f1e320256272c90cef2293ef60cd7a5e839.aiff",
            8,
            1.5,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=2.5),
            lambda path: output_path
            / "score-387cf3edc49f67f6ebbc144cd23306b960926dc673f2817c68543400493fb5e5.aiff",
            2,
            2.5,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=3.0),
            lambda path: output_path
            / "score-846a0d8cfdcc83340a4cf7d181fab89e1f630637ff93c1354e9addb3ee2837b0.aiff",
            2,
            3.0,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=3.5),
            lambda path: output_path
            / "score-8581bbe2f384d3748d7cc156957483430da6b549662599b5b14d6fecc6e3f78a.aiff",
            2,
            3.5,
            44100,
        ),
        (
            lambda path: dict(render_directory_path=path),
            lambda path: output_path
            / "score-1f2fad799464ced28d0af160e819d261488c4361ca8a32288f742f6e8e0fb01a.aiff",
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
            lambda path: output_path
            / "score-274be7ac8705739c0e67baf6a220a486f1e361aba9f7e92d536f666a8b43b28f.aiff",
            8,
            3.0,
            48000,
        ),
        (lambda path: dict(suppress_output=True), lambda path: None, 8, 3.0, 44100),
    ],
)
async def test_render(
    context,
    expected_channel_count,
    expected_duration,
    expected_path,
    expected_sample_rate,
    render_kwargs,
    tmp_path,
):
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


def test___render__(context):
    expected_path = (
        output_path
        / "score-1f2fad799464ced28d0af160e819d261488c4361ca8a32288f742f6e8e0fb01a.aiff"
    )
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
