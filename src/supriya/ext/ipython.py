from IPython.display import Audio, display  # type: ignore

from ..io import Player, Plotter
from ..typing import SupportsRenderMemo
from . import websafe_audio


def load_ipython_extension(ipython):
    ipython.extension_manager.load_extension("uqbar.ext.ipython")
    patch_player()
    patch_plotter()


def patch_player():
    async def patched_call(self):
        if isinstance(self.renderable, SupportsRenderMemo):
            supports_render = self.renderable.__render_memo__()
        else:
            supports_render = self.renderable
        output_path, status_code = await supports_render.__render__(
            **self.render_kwargs,
        )
        if output_path:
            # Don't open the output path natively
            output_path = websafe_audio(output_path)
            display(Audio(filename=str(output_path)))
        return output_path, status_code

    Player.__call__ = patched_call


def patch_plotter():
    def patched_call(self):
        # Don't open the output path natively
        return self.render()

    Plotter.__call__ = patched_call
