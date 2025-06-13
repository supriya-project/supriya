import asyncio
import dataclasses
import datetime
import hashlib
import platform
import subprocess
from os import PathLike
from pathlib import Path
from typing import Coroutine

from uqbar.graphs import Grapher
from uqbar.io import open_path

import supriya

from .typing import SupportsPlot, SupportsRender, SupportsRenderMemo


@dataclasses.dataclass(frozen=True)
class PlayMemo:
    """
    For renderables that need to be captured during Sphinx output, e.g. realtime buffers.

    A realtime buffer does not exist by the time Sphinx writes output, so we capture the
    state of the buffer during Sphinx's read pass as a memo, and render the memo as
    audio during the write pass.
    """

    contents: bytes
    suffix: str

    def __render__(
        self,
        output_file_path: PathLike | None = None,
        render_directory_path: PathLike | None = None,
        **kwargs,
    ) -> Coroutine[None, None, tuple[Path | None, int]]:
        async def render_function() -> tuple[Path, int]:
            if output_file_path is None:
                hexdigest = hashlib.sha256(self.contents).hexdigest()
                file_name = f"audio-{hexdigest}{self.suffix}"
                path = Path(render_directory_path or supriya.output_path) / file_name
            else:
                path = Path(output_file_path)
            path.write_bytes(self.contents)
            return path, 0

        return render_function()

    @classmethod
    def from_path(cls, path: Path) -> "PlayMemo":
        return cls(contents=path.read_bytes(), suffix=path.suffix)


class Player:
    ### INITIALIZER ###

    def __init__(self, renderable: SupportsRender, **kwargs) -> None:
        self.renderable = renderable
        self.render_kwargs = kwargs

    ### SPECIAL METHODS ###

    def __call__(self) -> tuple[Path | None, int]:
        path, exit_code = self.render()
        if path:
            self.open_output_path(path)
        return path, exit_code

    ### PUBLIC METHODS ###

    def open_output_path(self, output_path) -> None:
        if platform.system() == "Darwin":
            subprocess.run(
                ["open", "-a", "QuickTime Player", str(output_path)], check=True
            )
        else:
            open_path(output_path)

    def render(self) -> tuple[Path | None, int]:
        return render(self.renderable, **self.render_kwargs)


class Plotter:
    ### INITIALIZER ###

    def __init__(self, plottable: SupportsPlot, **kwargs):
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
        # TODO: Drop color="blue" after upgrading librosa > 0.10.1
        #       https://github.com/librosa/librosa/issues/1763
        librosa.display.waveshow(array, sr=sample_rate, ax=ax, color="blue")
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


def plot(plottable: SupportsPlot, format_="png", **kwargs):
    return Plotter(plottable, format_=format_, **kwargs)()


def render(
    renderable: SupportsRender | SupportsRenderMemo,
    output_file_path: PathLike | None = None,
    render_directory_path: PathLike | None = None,
    **kwargs,
) -> tuple[Path | None, int]:
    if isinstance(renderable, SupportsRenderMemo):
        supports_render = renderable.__render_memo__()
    else:
        supports_render = renderable
    return asyncio.run(
        supports_render.__render__(
            output_file_path=output_file_path,
            render_directory_path=render_directory_path,
            **kwargs,
        )
    )


__all__ = ["Player", "Plotter", "graph", "play", "plot", "render"]
