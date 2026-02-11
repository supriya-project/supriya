import asyncio
import base64
import hashlib
import logging
import pathlib
import pickle
import textwrap
import typing

from docutils.nodes import FixedTextElement, General, SkipNode
from uqbar.apis.documenters import MemberDocumenter
from uqbar.book.extensions import Extension
from uqbar.strings import normalize

from ..io import Player, Plotter
from ..typing import SupportsRender, SupportsRenderMemo
from . import websafe_audio

logger = logging.getLogger(__name__)


class PlayExtension(Extension):
    template = normalize(
        """
        <audio controls src="{file_path}">
            Your browser does not support the <code>audio</code> element.
        </audio>
        """
    )

    class play_block(General, FixedTextElement):
        pass

    @classmethod
    def setup_console(cls, console, monkeypatch):
        monkeypatch.setattr(
            Player,
            "__call__",
            lambda self: console.push_proxy(cls(self.renderable, self.render_kwargs)),
        )

    @classmethod
    def setup_sphinx(cls, app):
        app.add_node(
            cls.play_block,
            html=[cls.visit_block_html, None],
            latex=[cls.visit_block_latex, None],
            text=[cls.visit_block_text, cls.depart_block_text],
        )

    def __init__(
        self, renderable: SupportsRender | SupportsRenderMemo, render_kwargs
    ) -> None:
        if isinstance(renderable, SupportsRenderMemo):
            self.renderable = pickle.loads(pickle.dumps(renderable.__render_memo__()))
        else:
            self.renderable = pickle.loads(pickle.dumps(renderable))
        self.render_kwargs = pickle.loads(pickle.dumps(render_kwargs))

    def to_docutils(self):
        code = "\n".join(
            textwrap.wrap(
                base64.b64encode(
                    pickle.dumps((self.renderable, self.render_kwargs))
                ).decode()
            )
        )
        node = self.play_block(code, code)
        return [node]

    @classmethod
    def render(cls, node, output_path):
        output_path.mkdir(exist_ok=True)
        renderable, render_kwargs = pickle.loads(
            base64.b64decode("".join(node[0].split()))
        )
        path, _ = asyncio.run(
            renderable.__render__(
                render_directory_path=output_path,
                **render_kwargs,
            )
        )
        return websafe_audio(path)

    @staticmethod
    def visit_block_html(self, node):
        absolute_file_path = PlayExtension.render(
            node, pathlib.Path(self.builder.outdir) / "_images"
        )
        relative_file_path = (
            pathlib.Path(self.builder.imgpath) / absolute_file_path.name
        )
        result = PlayExtension.template.format(file_path=relative_file_path)
        self.body.append(result)
        raise SkipNode


class PlotExtension(Extension):
    template = normalize(
        """
        <object data="{file_path}" type="image/svg+xml"></object>
        """
    )

    class plot_block(General, FixedTextElement):
        pass

    @classmethod
    def setup_console(cls, console, monkeypatch):
        monkeypatch.setattr(
            Plotter, "__call__", lambda self: console.push_proxy(cls(self.plottable))
        )

    @classmethod
    def setup_sphinx(cls, app):
        app.add_node(
            cls.plot_block,
            html=[cls.visit_block_html, None],
            latex=[cls.visit_block_latex, None],
            text=[cls.visit_block_text, cls.depart_block_text],
        )

    def __init__(self, plottable, **kwargs):
        self.array, self.sample_rate = plottable.__plot__()

    def to_docutils(self):
        code = "\n".join(
            textwrap.wrap(
                base64.b64encode(pickle.dumps((self.array, self.sample_rate))).decode()
            )
        )
        node = self.plot_block(code, code)
        return [node]

    @classmethod
    def render(cls, node, output_path):
        import numpy
        from matplotlib import pyplot

        output_path.mkdir(exist_ok=True)
        array, sample_rate = pickle.loads(base64.b64decode("".join(node[0].split())))
        fig, ax = pyplot.subplots(nrows=1)
        fig.set_size_inches(8, 2)
        fig.patch.set_alpha(1.0)
        ax.set_facecolor("white")
        ax.xaxis.label.set_color("white")
        ax.tick_params(axis="x", colors="black")
        ax.tick_params(axis="y", colors="black")

        # kludgy replacement for librosa.display.waveshow()
        time = numpy.linspace(
            [0] * len(array), 
            [len(array[0]) / sample_rate] * len(array),
            num=len(array[0]),
        )
        pyplot.plot(time, array.transpose())

        hexdigest = hashlib.sha256(node[0].encode()).hexdigest()
        file_path = output_path / f"plot-{hexdigest}.svg"
        fig.savefig(file_path, bbox_inches="tight")
        pyplot.close(fig)
        return file_path

    @staticmethod
    def visit_block_html(self, node):
        absolute_file_path = PlotExtension.render(
            node, pathlib.Path(self.builder.outdir) / "_images"
        )
        relative_file_path = (
            pathlib.Path(self.builder.imgpath) / absolute_file_path.name
        )
        result = PlotExtension.template.format(file_path=relative_file_path)
        self.body.append(result)
        raise SkipNode


class TypeVarDocumenter(MemberDocumenter):
    """
    A TypeVar documenter.
    """

    def __str__(self) -> str:
        return ".. autotypevar:: {}".format(getattr(self.client, "__name__"))

    @classmethod
    def validate_client(cls, client: object, module_path: str) -> bool:
        return isinstance(client, typing.TypeVar) and client.__module__ == module_path
