import base64
import hashlib
import pathlib
import pickle
import textwrap
import warnings

import librosa.display
from docutils.nodes import FixedTextElement, General, SkipNode
from matplotlib import pyplot
from uqbar.book.extensions import Extension
from uqbar.strings import normalize

from supriya.ext import websafe_audio
from supriya.io import Player, Plotter


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

    def __init__(self, renderable, render_kwargs):
        try:
            self.renderable = pickle.loads(pickle.dumps(renderable))
        except TypeError:
            self.renderable = renderable.__render__()
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
        return websafe_audio(
            renderable.__render__(render_directory_path=output_path, **render_kwargs)
        )

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
        # Suppress "PySoundFile failed. Trying audioread instead."
        warnings.filterwarnings(
            "ignore", category=UserWarning, module="librosa.core.audio"
        )
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
        output_path.mkdir(exist_ok=True)
        array, sample_rate = pickle.loads(base64.b64decode("".join(node[0].split())))
        fig, ax = pyplot.subplots(nrows=1)
        fig.set_size_inches(8, 2)
        fig.patch.set_alpha(0.0)
        ax.set_facecolor("white")
        ax.xaxis.label.set_color("white")
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")
        librosa.display.waveshow(array, sr=sample_rate, ax=ax)
        hexdigest = hashlib.sha1(node[0].encode()).hexdigest()
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
