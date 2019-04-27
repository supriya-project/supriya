import subprocess

import uqbar.io


def websafe_audio(output_path):
    # Convert to MP3 if possible for smaller file sizes:
    if uqbar.io.find_executable("lame"):
        new_output_path = output_path.with_suffix(".mp3")
        if new_output_path.exists():
            return new_output_path
        command = "lame -V2 {} {}".format(output_path, new_output_path)
        exit_code = subprocess.call(command, shell=True)
        if not exit_code:
            return new_output_path
    # If MP3-conversion, fails, try to convert to .wav
    if uqbar.io.find_executable("ffmpeg"):
        new_output_path = output_path.with_suffix(".wav")
        command = "ffmpeg -i {} {}".format(output_path, new_output_path)
        exit_code = subprocess.call(command, shell=True)
        if not exit_code:
            return new_output_path
    return output_path
