import dataclasses
import datetime
import hashlib
import pathlib
import subprocess
import sys
from os import PathLike
from typing import Optional

from uqbar.graphs import Grapher

import supriya

from .typing import SupportsRender


@dataclasses.dataclass(frozen=True)
class PlayMemo:
    contents: bytes
    suffix: str

    def __render__(
        self,
        output_file_path: Optional[PathLike] = None,
        render_directory_path: Optional[PathLike] = None,
        **kwargs,
    ) -> pathlib.Path:
        if output_file_path is None:
            hexdigest = hashlib.sha1(self.contents).hexdigest()
            file_name = f"audio-{hexdigest}{self.suffix}"
            file_path = (
                pathlib.Path(render_directory_path or supriya.output_path) / file_name
            )
        else:
            file_path = pathlib.Path(output_file_path)
        file_path.write_bytes(self.contents)
        return file_path

    @classmethod
    def from_path(cls, path: pathlib.Path) -> "PlayMemo":
        return cls(contents=path.read_bytes(), suffix=path.suffix)


class Player:

    ### INITIALIZER ###

    def __init__(self, renderable, **kwargs):
        self.renderable = renderable
        self.render_kwargs = kwargs

    ### SPECIAL METHODS ###

    def __call__(self):
        output_path = self.render()
        self.open_output_path(output_path)
        return output_path

    ### PUBLIC METHODS ###

    def open_output_path(self, output_path):
        viewer = "open -a 'QuickTime Player'"
        if sys.platform.lower().startswith("linux"):
            viewer = "xdg-open"
        subprocess.run(f"{viewer} {output_path}", shell=True, check=True)

    def render(self):
        result = self.renderable.__render__(**self.render_kwargs)
        if hasattr(result, "__render__"):
            result = result.__render__(**self.render_kwargs)
        return result


class Plotter:

    ### INITIALIZER ###

    def __init__(self, plottable, **kwargs):
        self.plottable = plottable
        self.plot_kwargs = kwargs

    ### SPECIAL METHODS ###

    def __call__(self):
        output_path = self.render()
        self.open_output_path(output_path)
        return output_path

    ### PUBLIC METHODS ###

    def open_output_path(self, output_path):
        viewer = "open"
        if sys.platform.lower().startswith("linux"):
            viewer = "xdg-open"
        subprocess.run(f"{viewer} {output_path}", shell=True, check=True)

    def render(self):
        import librosa.display
        from matplotlib import pyplot

        array, sample_rate = self.plottable.__plot__()
        fig, ax = pyplot.subplots(nrows=1)
        librosa.display.waveshow(array, sr=sample_rate, ax=ax)
        timestamp = (
            datetime.datetime.now().isoformat().replace(".", "-").replace(":", "-")
        )
        extension = self.plot_kwargs.get("format_", "png")
        output_path = supriya.output_path / f"{timestamp}.{extension}"
        fig.savefig(output_path)
        return output_path


def graph(graphable, format_="pdf", layout="dot"):
    return Grapher(
        graphable, format_=format_, layout=layout, output_directory=supriya.output_path
    )()


def play(renderable: SupportsRender, **kwargs):
    return Player(renderable, **kwargs)()


def plot(plottable, format_="png", **kwargs):
    return Plotter(plottable, format_=format_, **kwargs)()


def render(
    renderable: SupportsRender,
    output_file_path: Optional[PathLike] = None,
    render_directory_path: Optional[PathLike] = None,
    **kwargs,
):
    return renderable.__render__(
        output_file_path=output_file_path,
        render_directory_path=render_directory_path,
        **kwargs,
    )


__all__ = ["Player", "Plotter", "graph", "play", "plot", "render"]
