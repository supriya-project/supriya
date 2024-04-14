import aifc
import logging
import platform

import pytest

from supriya import default, output_path, render
from supriya.contexts.nonrealtime import Score


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
            / "score-89dc8e276da005ed1b2f5826dccdc19cf3e21015701332dfcb59f064bc2431f5.aiff",
            8,
            3.0,
            44100,
        ),
        (
            lambda path: dict(duration=1.5),
            lambda path: output_path
            / "score-97892fdf5d7540a33e1dce9d0dcdf05d3b6be27c21140fdfab90e0fb1e7e2b94.aiff",
            8,
            1.5,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=2.5),
            lambda path: output_path
            / "score-27d30ed52df6c0f4a3d31c55a90b46d10735c11b2daaa7ccddc48954871fea9f.aiff",
            2,
            2.5,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=3.0),
            lambda path: output_path
            / "score-d0b3f1165f80bdda40f2de3d2bc4cded79a79cdd2748899fc189c0b1e6beaf46.aiff",
            2,
            3.0,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=3.5),
            lambda path: output_path
            / "score-54c84a39561ece824a5151e6798d9f60a488f1a9c6b665bd9f6ef5010ab2294c.aiff",
            2,
            3.5,
            44100,
        ),
        (
            lambda path: dict(render_directory_path=path),
            lambda path: output_path
            / "score-89dc8e276da005ed1b2f5826dccdc19cf3e21015701332dfcb59f064bc2431f5.aiff",
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
            / "score-773b079939a228b9977a2a2a72ee3a46ccf7a1b2aa94343620fd9dcd4546bc47.aiff",
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
    actual_path, exit_code = await context.render(**render_kwargs(tmp_path))
    if platform.system() == "Windows":
        assert exit_code == 3221226505
    else:
        assert exit_code == 0
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
        / "score-89dc8e276da005ed1b2f5826dccdc19cf3e21015701332dfcb59f064bc2431f5.aiff"
    )
    if expected_path.exists():
        expected_path.unlink()
    if platform.system() == "Windows":
        expected_exit_code = 3221226505
    else:
        expected_exit_code = 0
    actual_path, actual_exit_code = render(context)
    assert expected_path == actual_path
    assert expected_exit_code == actual_exit_code
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
