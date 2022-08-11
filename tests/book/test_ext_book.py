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
    aif_file_names, mp3_file_names, osc_file_names, wav_file_names = [], [], [], []
    for path in sorted(image_path.iterdir()):
        if path.suffix.startswith(".aif"):
            aif_file_names.append(path.name)
        elif path.suffix == ".mp3":
            mp3_file_names.append(path.name)
        elif path.suffix == ".osc":
            osc_file_names.append(path.name)
        elif path.suffix == ".wav":
            wav_file_names.append(path.name)
    # AIF output for all files
    expected_file_names = [
        "session-1675b54d9f2b8a493bab995877ba679e.aiff",
        "session-462b5896f380a14a732e461bade2148f.aiff",
        "session-d536a6a4819769a80987605aa31b86ae.aiff",
    ]
    if platform.system() != "Windows":
        expected_file_names.insert(0, "say-b62c21527eaa5d8536687ce77b85a57c.aiff")
    assert aif_file_names == expected_file_names
    if platform.system() != "Windows":
        # Only the Say output is 2-channel and can be converted
        assert mp3_file_names == ["say-b62c21527eaa5d8536687ce77b85a57c.mp3"]
    # All Sessions generate an OSC file
    assert osc_file_names == [
        "session-1675b54d9f2b8a493bab995877ba679e.osc",
        "session-462b5896f380a14a732e461bade2148f.osc",
        "session-d536a6a4819769a80987605aa31b86ae.osc",
    ]
    # Only the played session is converted to WAV
    assert wav_file_names == ["session-d536a6a4819769a80987605aa31b86ae.wav"]


@pytest.mark.sphinx("text", testroot="book")
def test_sphinx_book_text(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
