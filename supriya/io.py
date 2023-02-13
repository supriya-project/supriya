import asyncio
import dataclasses
import datetime
import hashlib
import platform
import subprocess
from os import PathLike
from pathlib import Path
from typing import Callable, Coroutine, Optional, Tuple

from uqbar.graphs import Grapher
from uqbar.io import open_path

import supriya

from .typing import SupportsRender


@dataclasses.dataclass(frozen=True)
class PlayMemo:
    contents: bytes
    suffix: str

    def __call__(
        self,
        output_file_path: Optional[PathLike] = None,
        render_directory_path: Optional[PathLike] = None,
        **kwargs,
    ) -> Tuple[Callable[[], Coroutine[None, None, int]], Path]:
        async def render_function():
            path.write_bytes(self.contents)
            return 0

        if output_file_path is None:
            hexdigest = hashlib.sha1(self.contents).hexdigest()
            file_name = f"audio-{hexdigest}{self.suffix}"
            path = Path(render_directory_path or supriya.output_path) / file_name
        else:
            path = Path(output_file_path)
        return render_function, path

    @classmethod
    def from_path(cls, path: Path) -> "PlayMemo":
        return cls(contents=path.read_bytes(), suffix=path.suffix)


class Player:
    ### INITIALIZER ###

    def __init__(self, renderable, **kwargs):
        self.renderable = renderable
        self.render_kwargs = kwargs

    ### SPECIAL METHODS ###

    def __call__(self):
        _, output_path = self.render()
        self.open_output_path(output_path)
        return output_path

    ### PUBLIC METHODS ###

    def open_output_path(self, output_path):
        if platform.system() == "Darwin":
            subprocess.run(
                ["open", "-a", "QuickTime Player", str(output_path)], check=True
            )
        else:
            open_path(output_path)

    def render(self):
        result = self.renderable.__render__(**self.render_kwargs)
        if hasattr(result, "__render__"):
            result = result.__render__(**self.render_kwargs)
        coroutine, path = result
        exit_code = asyncio.run(coroutine())
        return exit_code, path


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
        open_path(output_path)

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
) -> Tuple[int, Path]:
    result = renderable.__render__(
        output_file_path=output_file_path,
        render_directory_path=render_directory_path,
        **kwargs,
    )
    if callable(result):
        render_function, path = result()
    else:
        render_function, path = result
    exit_code = asyncio.run(render_function())
    return exit_code, path


__all__ = ["Player", "Plotter", "graph", "play", "plot", "render"]
