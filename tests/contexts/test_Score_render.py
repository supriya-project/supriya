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
            / "score-e286c01caf6513600e6bc8ff491dea22e1e0366284ea8a96545215fb78267b20.aiff",
            8,
            3.0,
            44100,
        ),
        (
            lambda path: dict(duration=1.5),
            lambda path: output_path
            / "score-175ec72a18d7f3af4deced81962f9244849ba6edf5b52c7e781cd420ddbe4221.aiff",
            8,
            1.5,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=2.5),
            lambda path: output_path
            / "score-826392767c60fea2986c21a58b91ba1137c5c5be66a4d4501a1b644fcf4d3ba9.aiff",
            2,
            2.5,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=3.0),
            lambda path: output_path
            / "score-abf2f776bee43fea071b05ae8bdc93a0882e17280ae84acaa4f8cdacef4a78cc.aiff",
            2,
            3.0,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=3.5),
            lambda path: output_path
            / "score-4d2ac6a4683a40532c2c5b52bca90fc93096dbdb1c998ac889cd0b13245d4470.aiff",
            2,
            3.5,
            44100,
        ),
        (
            lambda path: dict(render_directory_path=path),
            lambda path: output_path
            / "score-e286c01caf6513600e6bc8ff491dea22e1e0366284ea8a96545215fb78267b20.aiff",
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
            / "score-c23d78bb9b542c7d30e2c3e213bedd33a6193ab1112d3b4a4cd5e5894f40179b.aiff",
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
    expected_path = (
        output_path
        / "score-e286c01caf6513600e6bc8ff491dea22e1e0366284ea8a96545215fb78267b20.aiff"
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
