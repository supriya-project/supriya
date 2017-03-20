# -*- encoding: utf-8 -*-
import hashlib
import pathlib
import shlex
import subprocess
from abjad.tools.stringtools import to_dash_case
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Say(SupriyaValueObject):

    ### CLASS VARIABLES ###

    _voices = (
        'Alex', 'Alice', 'Alva', 'Amelie', 'Anna', 'Carmit', 'Damayanti',
        'Daniel', 'Diego', 'Ellen', 'Fiona', 'Fred', 'Ioana', 'Joana', 'Jorge',
        'Juan', 'Kanya', 'Karen', 'Kyoko', 'Laura', 'Lekha', 'Luca', 'Luciana',
        'Maged', 'Mariska', 'Mei-Jia', 'Melina', 'Milena', 'Moira', 'Monica',
        'Nora', 'Paulina', 'Samantha', 'Sara', 'Satu', 'Sin-ji', 'Tessa',
        'Thomas', 'Ting-Ting', 'Veena', 'Victoria', 'Xander', 'Yelda', 'Yuna',
        'Yuri', 'Zosia', 'Zuzana',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        text,
        voice=None,
        ):
        self._text = str(text)
        if voice is not None:
            voice = str(voice)
            assert voice in self._voices
        self._voice = voice

    ### SPECIAL METHODS ###

    def __render__(
        self,
        output_file_path=None,
        render_directory_path=None,
        ):
        output_file_path = self._build_output_file_path(
            output_file_path=output_file_path,
            render_directory_path=render_directory_path,
            )
        assert output_file_path.parent.exists()
        if output_file_path.exists():
            print('Skipping {}'.format(output_file_path))
            return
        command_parts = ['say']
        command_parts.extend(['-o', str(output_file_path)])
        if self.voice:
            command_parts.extend(['-v', self.voice])
        command_parts.append(shlex.quote(self.text))
        command = ' '.join(command_parts)
        print(command)
        exit_code = subprocess.call(command, shell=True)
        if exit_code:
            raise RuntimeError
        return output_file_path

    ### PRIVATE METHODS ###

    def _build_file_path(self):
        md5 = hashlib.md5()
        md5.update(self.text.encode())
        if self.voice is not None:
            md5.update(self.voice.encode())
        md5 = md5.hexdigest()
        file_path = '{}-{}.aiff'.format(
            to_dash_case(type(self).__name__), md5,
            )
        return pathlib.Path(file_path)

    def _build_output_file_path(
        self,
        output_file_path=None,
        render_directory_path=None,
        ):
        from supriya import supriya_configuration
        if output_file_path:
            output_file_path = pathlib.Path(
                output_file_path).expanduser().absolute()
        elif render_directory_path:
            render_directory_path = pathlib.Path(
                render_directory_path).expanduser().absolute()
            output_file_path = render_directory_path / self._build_file_path()
        else:
            output_file_path = self._build_file_path()
            render_directory_path = pathlib.Path(
                supriya_configuration.output_directory_path,
                ).expanduser().absolute()
            output_file_path = render_directory_path / self._build_file_path()
        return output_file_path

    ### PUBLIC PROPERTIES ###

    @property
    def text(self):
        return self._text

    @property
    def voice(self):
        return self._voice
