from IPython.display import Audio, display  # type: ignore

from supriya.ext import websafe_audio
from supriya.io import Player


def load_ipython_extension(ipython):
    ipython.extension_manager.load_extension("uqbar.ext.ipython")
    patch_player()


def patch_player():
    async def patched_call(self):
        output_path, status_code = await self.renderable.__render__(
            **self.render_kwargs,
        )
        if output_path:
            output_path = websafe_audio(output_path)
            display(Audio(filename=str(output_path)))
        return output_path, status_code

    Player.__call__ = patched_call
