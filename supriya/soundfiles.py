"""
Tools for interacting with soundfiles.
"""
import aifc
import asyncio
import hashlib
import shlex
import sndhdr
import wave
from os import PathLike
from pathlib import Path
from typing import Callable, Coroutine, Optional, Tuple

from uqbar.io import find_executable
from uqbar.strings import to_dash_case

from . import output_path
from .system import SupriyaObject, SupriyaValueObject


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
        **kwargs,
    ) -> Tuple[Callable[[], Coroutine[None, None, int]], Path]:
        async def render():
            if path.exists():
                return 0
            if find_executable("say"):
                command = ["say", "-o", str(path)]
                if self.voice:
                    command.extend(["-v", self.voice])
            else:
                command = ["espeak", "-w", str(path)]
            command.append(shlex.quote(self.text))
            process = await asyncio.create_subprocess_exec(
                *command, cwd=render_directory_path
            )
            await process.communicate()
            return process.returncode

        path = self._build_output_file_path(
            output_file_path=output_file_path,
            render_directory_path=render_directory_path,
        )
        return render, path

    ### PRIVATE METHODS ###

    def _build_file_path(self):
        md5 = hashlib.md5()
        md5.update(self.text.encode())
        if self.voice is not None:
            md5.update(self.voice.encode())
        md5 = md5.hexdigest()
        file_path = "{}-{}.aiff".format(to_dash_case(type(self).__name__), md5)
        return Path(file_path)

    def _build_output_file_path(
        self, output_file_path=None, render_directory_path=None
    ) -> Path:
        if output_file_path:
            output_file_path = Path(output_file_path).resolve()
        elif render_directory_path:
            render_directory_path = Path(render_directory_path).resolve()
            output_file_path = render_directory_path / self._build_file_path()
        else:
            output_file_path = self._build_file_path()
            render_directory_path = Path(output_path).resolve()
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
        self._file_path = Path(file_path)
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
