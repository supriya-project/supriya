import pathlib
import platform
import shutil

import pytest
import uqbar.io


@pytest.fixture
def rm_dirs(app):
    for path in [pathlib.Path(app.doctreedir), pathlib.Path(app.outdir) / "_images"]:
        if path.exists():
            shutil.rmtree(path)
    yield


@pytest.mark.sphinx("html", testroot="book")
def test_sphinx_book_html(app, status, warning, rm_dirs):
    app.build()
    for root, paths, dirs in uqbar.io.walk(app.outdir):
        for path in paths:
            print(path)
    assert not warning.getvalue().strip()
    image_path = pathlib.Path(app.outdir) / "_images"
    expected_file_names = [
        "session-1675b54d9f2b8a493bab995877ba679e.aiff",
        "session-1675b54d9f2b8a493bab995877ba679e.osc",
        "session-462b5896f380a14a732e461bade2148f.aiff",
        "session-462b5896f380a14a732e461bade2148f.osc",
        "session-d536a6a4819769a80987605aa31b86ae.aiff",
        "session-d536a6a4819769a80987605aa31b86ae.osc",
        "session-d536a6a4819769a80987605aa31b86ae.wav",
    ]
    if platform.system() != "Windows":
        expected_file_names.extend(
            [
                "say-b62c21527eaa5d8536687ce77b85a57c.aiff",
                "say-b62c21527eaa5d8536687ce77b85a57c.mp3",
            ]
        )
    actual_file_names = sorted(path.name for path in image_path.iterdir())
    assert all(file_name in actual_file_names for file_name in expected_file_names)
    # audio and plot names are not stable across platforms
    audio_mp3_paths = list(image_path.glob("audio-*.mp3"))
    audio_wav_paths = list(image_path.glob("audio-*.wav"))
    plot_svg_paths = list(image_path.glob("plot-*.svg"))
    assert len(audio_mp3_paths) == 1
    assert len(audio_wav_paths) == 1
    assert len(plot_svg_paths) == 1


@pytest.mark.sphinx("text", testroot="book")
def test_sphinx_book_text(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
