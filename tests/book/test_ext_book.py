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
        "audio-838b1f6946d1fbbc947f9e6658e77055028fef3f.mp3",
        "audio-838b1f6946d1fbbc947f9e6658e77055028fef3f.wav",
        "plot-f46471ac74ea8ba66e38333bd574323ff613faae.svg",
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
    assert sorted(path.name for path in image_path.iterdir()) == sorted(
        expected_file_names
    )


@pytest.mark.sphinx("text", testroot="book")
def test_sphinx_book_text(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
