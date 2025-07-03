import logging
import os
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


@pytest.mark.skipif(
    bool(os.environ.get("CI")) and platform.system() == "Windows",
    reason="hangs on Windows in CI",
)
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
        "score-0c3a86ac039b84ca308975d210f0245607074cc97d76fcc5999aea0174460d0a.aiff",
        "score-0c3a86ac039b84ca308975d210f0245607074cc97d76fcc5999aea0174460d0a.osc",
    ]
    if platform.system() != "Windows":
        expected_file_names.extend(
            [
                "say-3d7f815142f4edadfca73bd01c264223de1e4f5fd5e50a4c9e6f917eddeddba6.aiff",
                "say-3d7f815142f4edadfca73bd01c264223de1e4f5fd5e50a4c9e6f917eddeddba6.mp3",
            ]
        )
    # Haven't found a /simple/ cross-platforn solution for detecting audio device SR
    expected_44100_file_names = expected_file_names + [
        "audio-08abe38d842cbaa19789618fe4675f1cf64de0eb6f9ab7ebd2165c078ce31429.mp3",
        "audio-08abe38d842cbaa19789618fe4675f1cf64de0eb6f9ab7ebd2165c078ce31429.wav",
        "plot-99e2c0700b9eab6f980db17cc773b1ecdc8cd5db7e9fed14e03622176ef7599c.svg",
    ]
    expected_48000_file_names = expected_file_names + [
        "audio-4f0fd44621b74146c936fab67a7544438ddb60abe59b506082268778ec2e285f.mp3",
        "audio-4f0fd44621b74146c936fab67a7544438ddb60abe59b506082268778ec2e285f.wav",
        "plot-282e7e88a25aa93b5fcf85a028bbc14b2445171e3c43018124f120579a0d2afe.svg",
    ]
    actual_file_names = sorted(path.name for path in image_path.iterdir())
    for file_name in sorted(actual_file_names):
        print(f"actual: {file_name}")
    for file_name in sorted(expected_44100_file_names):
        print(f"44100: {file_name}")
    for file_name in sorted(expected_48000_file_names):
        print(f"48000: {file_name}")
    all_44100_files_exist = all(
        [file_name in actual_file_names for file_name in expected_44100_file_names]
    )
    all_48000_files_exist = all(
        [file_name in actual_file_names for file_name in expected_48000_file_names]
    )
    assert all_44100_files_exist or all_48000_files_exist
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
