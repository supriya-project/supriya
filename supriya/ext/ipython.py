import subprocess

import uqbar.io
from IPython.core.display import display  # type: ignore
from IPython.display import Audio  # type: ignore

from supriya.io import Player


def load_ipython_extension(ipython):
    ipython.extension_manager.load_extension("uqbar.ext.ipython")
    patch_player()


def patch_player():
    def render(self):
        output_path = self.renderable.__render__(**self.render_kwargs)
        # HTML5 Audio element can't display AIFFs properly, but can WAVE:
        if uqbar.io.find_executable("ffmpeg") and output_path.suffix.startswith(".aif"):
            new_output_path = output_path.with_suffix(".wav")
            command = "ffmpeg -i {} {}".format(output_path, new_output_path)
            exit_code = subprocess.call(command, shell=True)
            if not exit_code:
                output_path = new_output_path
        # Convert to MP3 if possible for smaller file sizes:
        if uqbar.io.find_executable("lame"):
            new_output_path = output_path.with_suffix(".mp3")
            command = "lame -V2 {} {}".format(output_path, new_output_path)
            exit_code = subprocess.call(command, shell=True)
            if not exit_code:
                output_path = new_output_path
        return output_path

    def open_output_path(self, output_path):
        display(Audio(filename=str(output_path)))

    Player.open_output_path = open_output_path
    Player.render = render
