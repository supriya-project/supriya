import logging
import os
import pathlib
import platform
import shutil
import sys

import pytest
import uqbar.io


@pytest.fixture
def rm_dirs(app):
    for path in [pathlib.Path(app.doctreedir), pathlib.Path(app.outdir) / "_images"]:
        if path.exists():
            shutil.rmtree(path)
    yield


@pytest.mark.skipif(bool(os.environ.get("CI")), reason="Import breaks under GHA")
@pytest.mark.sphinx("html", testroot="book")
def test_sphinx_book_html(caplog, app, status, warning, rm_dirs):
    caplog.set_level(logging.INFO)
    app.build()
    for root, paths, dirs in uqbar.io.walk(app.outdir):
        for path in paths:
            print(path)
    assert not warning.getvalue().strip()
    image_path = pathlib.Path(app.outdir) / "_images"
    expected_file_names = [
        "audio-4f0fd44621b74146c936fab67a7544438ddb60abe59b506082268778ec2e285f.mp3",
        "audio-4f0fd44621b74146c936fab67a7544438ddb60abe59b506082268778ec2e285f.wav",
        "plot-6e8cafcdb775004ffba3051b743f9d5a539d541c6601f723ecfcc3145f0217b4.svg",
        "score-759292a876c9e866721fda737f939bcc7e84e04108d6adb207480e887de6b24a.aiff",
        "score-759292a876c9e866721fda737f939bcc7e84e04108d6adb207480e887de6b24a.osc",
    ]
    if platform.system() != "Windows":
        expected_file_names.extend(
            [
                "say-3d7f815142f4edadfca73bd01c264223de1e4f5fd5e50a4c9e6f917eddeddba6.aiff",
                "say-3d7f815142f4edadfca73bd01c264223de1e4f5fd5e50a4c9e6f917eddeddba6.mp3",
            ]
        )
    actual_file_names = sorted(path.name for path in image_path.iterdir())
    print(actual_file_names)
    assert all(file_name in actual_file_names for file_name in expected_file_names)
    # audio and plot names are not stable across platforms
    audio_mp3_paths = list(image_path.glob("audio-*.mp3"))
    audio_wav_paths = list(image_path.glob("audio-*.wav"))
    plot_svg_paths = list(image_path.glob("plot-*.svg"))
    assert len(audio_mp3_paths) == 1
    assert len(audio_wav_paths) == 1
    assert len(plot_svg_paths) == 1


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Sphinx paths broken in 3.8")
@pytest.mark.sphinx("text", testroot="book")
def test_sphinx_book_text(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
