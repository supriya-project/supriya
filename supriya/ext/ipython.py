from IPython.core.display import display  # type: ignore
from IPython.display import Audio  # type: ignore

from supriya.ext import websafe_audio
from supriya.io import Player


def load_ipython_extension(ipython):
    ipython.extension_manager.load_extension("uqbar.ext.ipython")
    patch_player()


def patch_player():
    def render(self):
        output_path = self.renderable.__render__(**self.render_kwargs)
        return websafe_audio(output_path)

    def open_output_path(self, output_path):
        display(Audio(filename=str(output_path)))

    Player.open_output_path = open_output_path
    Player.render = render
