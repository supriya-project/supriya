"""
Tools for interacting with soundfiles.
"""
import aifc
import hashlib
import pathlib
import shlex
import sndhdr
import subprocess
import wave
from os import PathLike
from typing import Optional

import uqbar.strings

import supriya
from supriya.system import SupriyaObject, SupriyaValueObject


class Say(SupriyaValueObject):
    """
    Wrapper for OSX ``say`` command.

    ::

        >>> say = supriya.Say("Hello World!", voice="Daniel")
        >>> supriya.play(say)  # doctest: +SKIP

    """

    ### CLASS VARIABLES ###

    _voices = (
        "Alex",
        "Alice",
        "Alva",
        "Amelie",
        "Anna",
        "Carmit",
        "Damayanti",
        "Daniel",
        "Diego",
        "Ellen",
        "Fiona",
        "Fred",
        "Ioana",
        "Joana",
        "Jorge",
        "Juan",
        "Kanya",
        "Karen",
        "Kyoko",
        "Laura",
        "Lekha",
        "Luca",
        "Luciana",
        "Maged",
        "Mariska",
        "Mei-Jia",
        "Melina",
        "Milena",
        "Moira",
        "Monica",
        "Nora",
        "Paulina",
        "Samantha",
        "Sara",
        "Satu",
        "Sin-ji",
        "Tessa",
        "Thomas",
        "Ting-Ting",
        "Veena",
        "Victoria",
        "Xander",
        "Yelda",
        "Yuna",
        "Yuri",
        "Zosia",
        "Zuzana",
    )

    ### INITIALIZER ###

    def __init__(self, text, voice=None):
        self._text = str(text)
        if voice is not None:
            voice = str(voice)
            assert voice in self._voices
        self._voice = voice

    ### SPECIAL METHODS ###

    def __render__(
        self,
        output_file_path: Optional[PathLike] = None,
        render_directory_path: Optional[PathLike] = None,
        print_transcript: bool = False,
        **kwargs,
    ) -> pathlib.Path:
        file_path = self._build_output_file_path(
            output_file_path=output_file_path,
            render_directory_path=render_directory_path,
        )
        assert file_path.parent.exists()
        if file_path.is_absolute():
            cwd = pathlib.Path.cwd()
            try:
                relative_file_path = file_path.relative_to(cwd)
            except ValueError:
                relative_file_path = file_path
        if print_transcript:
            print("Rendering {}".format(relative_file_path))
        if uqbar.io.find_executable("say"):
            command_parts = ["say"]
            command_parts.extend(["-o", str(relative_file_path)])
            if self.voice:
                command_parts.extend(["-v", self.voice])
        else:
            command_parts = ["espeak", "-w", str(relative_file_path)]
        command_parts.append(shlex.quote(self.text))
        command = " ".join(command_parts)
        if print_transcript:
            print("    Command: {}".format(command))
        if file_path.exists():
            if print_transcript:
                print(
                    "    Skipping {}. File already exists.".format(relative_file_path)
                )
            return file_path
        exit_code = subprocess.call(command, shell=True)
        if print_transcript:
            print(
                "    Rendered {} with exit code {}.".format(
                    relative_file_path, exit_code
                )
            )
        if exit_code:
            raise RuntimeError
        return file_path

    ### PRIVATE METHODS ###

    def _build_file_path(self):
        md5 = hashlib.md5()
        md5.update(self.text.encode())
        if self.voice is not None:
            md5.update(self.voice.encode())
        md5 = md5.hexdigest()
        file_path = "{}-{}.aiff".format(
            uqbar.strings.to_dash_case(type(self).__name__), md5
        )
        return pathlib.Path(file_path)

    def _build_output_file_path(
        self, output_file_path=None, render_directory_path=None
    ) -> pathlib.Path:
        if output_file_path:
            output_file_path = pathlib.Path(output_file_path).expanduser().absolute()
        elif render_directory_path:
            render_directory_path = (
                pathlib.Path(render_directory_path).expanduser().absolute()
            )
            output_file_path = render_directory_path / self._build_file_path()
        else:
            output_file_path = self._build_file_path()
            render_directory_path = (
                pathlib.Path(supriya.output_path).expanduser().absolute()
            )
            output_file_path = render_directory_path / self._build_file_path()
        return output_file_path

    ### PUBLIC PROPERTIES ###

    @property
    def text(self):
        return self._text

    @property
    def voice(self):
        return self._voice


class SoundFile(SupriyaObject):

    ### INITIALIZER ###

    def __init__(self, file_path):
        self._file_path = pathlib.Path(file_path)
        if not self._file_path.exists():
            raise ValueError(self._file_path)
        headers = sndhdr.what(self._file_path)
        self._frame_count = headers.nframes
        self._sample_rate = headers.framerate
        self._channel_count = headers.nchannels
        self._sample_width = headers.sampwidth
        self._file_type = headers.filetype

    ### PUBLIC METHODS ###

    def at_frame(self, frame):
        if self.file_type not in ("aiff", "wav"):
            raise ValueError(self.file_type)
        if not (0 <= frame <= self.frame_count):
            raise ValueError(frame)
        if self.sample_width not in (16, 24, 32):
            raise ValueError(f"Cannot decode sample width {self.sample_width}")
        with open(self.file_path, "rb") as file_pointer:
            reader_proc = {"aiff": aifc.open, "wav": wave.open}[self.file_type]
            with reader_proc(file_pointer, "rb") as reader:
                reader.setpos(frame)
                raw_data = reader.readframes(1)
        maximum = 2 ** (self.sample_width - 1)
        integers = []
        stride = self.sample_width // 8
        endianness = "big" if self.file_type == "aiff" else "little"
        for i in range(self.channel_count):
            chunk = raw_data[i * stride : i * stride + stride]
            integers.append(int.from_bytes(chunk, endianness, signed=True))
        return [float(x) / maximum for x in integers]

    def at_percent(self, percent):
        return self.at_frame(int(self.frame_count * percent))

    def at_second(self, second):
        return self.at_frame(int(second * self.sample_rate))

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def seconds(self):
        return float(self._frame_count) / float(self._sample_rate)

    @property
    def file_path(self):
        return self._file_path

    @property
    def file_type(self):
        return self._file_type

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def sample_width(self):
        return self._sample_width
