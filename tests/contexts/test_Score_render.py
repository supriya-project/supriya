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
            / "score-e6beae761b2c8f192cfcd48948f0b51239699355b4450e640ffc97ec7243c4a4.aiff",
            8,
            3.0,
            44100,
        ),
        (
            lambda path: dict(duration=1.5),
            lambda path: output_path
            / "score-fbd0f324690ab445771bfa1932339f2cd4fc023e5e79986854091e79f1139f94.aiff",
            8,
            1.5,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=2.5),
            lambda path: output_path
            / "score-31d5cda432402e03a4fdb507b479408d26eec2879f342e790d6c3ee825cab67d.aiff",
            2,
            2.5,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=3.0),
            lambda path: output_path
            / "score-b7b44173bb96829b38b0792ac209e2dc96e0d9022c322f4a011b533f32579743.aiff",
            2,
            3.0,
            44100,
        ),
        (
            lambda path: dict(output_bus_channel_count=2, duration=3.5),
            lambda path: output_path
            / "score-c8561182c6faabda4ad0b10278fe1edb62306f1beca0eaeba82311d7e5020368.aiff",
            2,
            3.5,
            44100,
        ),
        (
            lambda path: dict(render_directory_path=path),
            lambda path: output_path
            / "score-e6beae761b2c8f192cfcd48948f0b51239699355b4450e640ffc97ec7243c4a4.aiff",
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
            / "score-2140a1b747033ecdbeac8c656586ba444abf60a6e1c60362c6aa40d9481612b7.aiff",
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
        / "score-e6beae761b2c8f192cfcd48948f0b51239699355b4450e640ffc97ec7243c4a4.aiff"
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
