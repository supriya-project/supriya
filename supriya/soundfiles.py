"""
Tools for interacting with soundfiles.
"""

import asyncio
import dataclasses
import hashlib
import shlex
from os import PathLike
from pathlib import Path

from uqbar.io import find_executable
from uqbar.strings import to_dash_case

from . import output_path


@dataclasses.dataclass(frozen=True)
class Say:
    """
    Wrapper for OSX ``say`` command.

    ::

        >>> from supriya.soundfiles import Say
        >>> say = Say("Hello World!", voice="Daniel")
        >>> supriya.play(say)  # doctest: +SKIP
    """

    text: str
    voice: str | None

    ### CLASS VARIABLES ###

    _valid_voices = (
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

    def __post_init__(self):
        if self.voice and self.voice not in self._valid_voices:
            raise ValueError(self.voice)

    ### SPECIAL METHODS ###

    async def __render__(
        self,
        output_file_path: PathLike | None = None,
        render_directory_path: PathLike | None = None,
        **kwargs,
    ) -> tuple[Path, int]:
        path = self._build_output_file_path(
            output_file_path=output_file_path,
            render_directory_path=render_directory_path,
        )
        if path.exists():
            return path, 0
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
        return path, process.returncode or 0

    ### PRIVATE METHODS ###

    def _build_file_path(self):
        md5 = hashlib.sha256()
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
