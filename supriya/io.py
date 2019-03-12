import subprocess
import sys

from uqbar.graphs import Grapher

import supriya


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
        return self.renderable.__render__(**self.render_kwargs)


def graph(graphable, format_="pdf", layout="dot", verbose=False):
    return Grapher(
        graphable,
        format_=format_,
        layout=layout,
        output_directory=supriya.output_path,
        verbose=verbose,
    )()


def play(renderable, **kwargs):
    return Player(renderable, **kwargs)()


def render(renderable, output_file_path=None, render_directory_path=None, **kwargs):
    return renderable.__render__(
        output_file_path=output_file_path,
        render_directory_path=render_directory_path,
        **kwargs,
    )


__all__ = ["Player", "graph", "play", "render"]
