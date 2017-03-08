# -*- encoding: utf-8 -*-
import hashlib
import pathlib
import struct
import subprocess
import yaml
from abjad.tools.systemtools import TemporaryDirectoryChange
from supriya.tools import servertools
from supriya.tools import soundfiletools
from supriya.tools.nonrealtimetools import (
    NonrealtimeRenderError,
    NonrealtimeOutputMissing,
)
from supriya.tools.systemtools import SupriyaObject
from supriya.tools.systemtools import Trellis


class SessionRenderer(SupriyaObject):
    """
    Renders non-realtime sessions as audio files.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Internals'

    __slots__ = (
        '_session',
        '_print_transcript',
        '_trellis',
        '_transcript',
        '_transcript_prefix',
        '_compiled_sessions',
        '_session_file_paths',
        '_prerender_tuples',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        print_transcript=None,
        transcript_prefix=None,
        ):
        self._session = session
        if print_transcript:
            print_transcript = bool(print_transcript)
        self._print_transcript = print_transcript
        transcript_prefix = transcript_prefix or None
        if transcript_prefix:
            transcript_prefix = str(transcript_prefix)
        self._transcript_prefix = transcript_prefix
        self._reset()

    ### PRIVATE METHODS ###

    def _build_datagram(self, osc_bundles):
        datagrams = []
        for osc_bundle in osc_bundles:
            datagram = osc_bundle.to_datagram(realtime=False)
            size = len(datagram)
            size = struct.pack('>i', size)
            datagrams.append(size)
            datagrams.append(datagram)
        datagram = b''.join(datagrams)
        return datagram

    def _build_file_path(
        self,
        datagram,
        input_file_path,
        session,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        ):
        md5 = hashlib.md5()
        hash_values = [datagram]
        if input_file_path is not None:
            hash_values.append(str(input_file_path))
        for value in (
            session.options.input_bus_channel_count,
            session.options.output_bus_channel_count,
            sample_rate,
            header_format,
            sample_format,
            ):
            hash_values.append(str(value))
        for value in hash_values:
            if isinstance(value, pathlib.Path):
                value = str(value)
            if isinstance(value, str):
                value = value.encode()
            md5.update(value)
        md5 = md5.hexdigest()
        file_path = '{}.osc'.format(md5)
        return pathlib.Path(file_path)

    def _build_render_command(
        self,
        input_file_path,
        output_file_path,
        session_file_path,
        server_options=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        ):
        from supriya import supriya_configuration
        cwd = pathlib.Path.cwd()
        server_options = server_options or servertools.ServerOptions()
        scsynth_path = supriya_configuration.scsynth_path
        if session_file_path.is_absolute():
            session_file_path = session_file_path.relative_to(cwd)
        parts = [scsynth_path, '-N', session_file_path]
        if input_file_path:
            if input_file_path.is_absolute():
                input_file_path = input_file_path.relative_to(cwd)
            parts.append(input_file_path)
        else:
            parts.append('_')
        if output_file_path.is_absolute() and cwd in output_file_path.parents:
            output_file_path = output_file_path.relative_to(cwd)
        parts.append(output_file_path)
        parts.append(str(int(sample_rate)))
        header_format = soundfiletools.HeaderFormat.from_expr(header_format)
        parts.append(header_format.name.lower())  # Must be lowercase.
        sample_format = soundfiletools.SampleFormat.from_expr(sample_format)
        parts.append(sample_format.name.lower())  # Must be lowercase.
        server_options = server_options.as_options_string(realtime=False)
        if server_options:
            parts.append(server_options)
        command = ' '.join(str(_) for _ in parts)
        return command

    def _build_render_yaml(self, session_prefixes):
        session_prefixes = session_prefixes[:]
        render_data = {'render': session_prefixes.pop(), 'source': None}
        if session_prefixes:
            render_data['source'] = list(reversed(session_prefixes))
        render_yaml = yaml.dump(
            render_data,
            default_flow_style=False,
            indent=4,
            )
        return render_yaml

    def _build_xrefd_bundles(
        self,
        osc_bundles,
        session_file_paths,
        header_format=soundfiletools.HeaderFormat.AIFF,
        ):
        extension = '.{}'.format(header_format.name.lower())
        for osc_bundle in osc_bundles:
            for osc_message in osc_bundle.contents:
                contents = list(osc_message.contents)
                for i, x in enumerate(contents):
                    try:
                        if x in session_file_paths:
                            session_file_path = session_file_paths[x].with_suffix(extension)
                            contents[i] = str(session_file_path)
                    except TypeError:
                        pass
                osc_message._contents = tuple(contents)
        return osc_bundles

    def _call_subprocess(self, command):
        return subprocess.call(command, shell=True)

    def _collect_prerender_data(
        self,
        session,
        duration=None,
        ):
        from supriya.tools import nonrealtimetools
        input_ = session.input_
        if isinstance(input_, str):
            input_ = pathlib.Path(input_)
        non_xrefd_bundles = session._to_non_xrefd_osc_bundles(duration)
        self.compiled_sessions[session] = input_, non_xrefd_bundles
        if session is self.session:
            self.trellis.add(session)
        if isinstance(input_, nonrealtimetools.Session):
            if input_ not in self.trellis:
                self._collect_prerender_data(input_)
            self.trellis.add(input_, parent=session)
        for non_xrefd_bundle in non_xrefd_bundles:
            for request in non_xrefd_bundle.contents:
                for x in request.contents:
                    if not isinstance(x, nonrealtimetools.Session):
                        continue
                    if x not in self.trellis:
                        self._collect_prerender_data(x)
                    self.trellis.add(x, parent=session)

    def _collect_prerender_tuples(
        self,
        session,
        duration=None,
        render_path=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        ):
        self._collect_prerender_data(session, duration=duration)
        assert self.trellis.is_acyclic()
        for trellis_session in self.trellis:
            if trellis_session is session:
                constraint_duration = (duration or session.duration) or 0.
            else:
                constraint_duration = session.duration
            assert 0. < constraint_duration < float('inf')
        for session in self.trellis:
            input_, non_xrefd_bundles = self.compiled_sessions[session]
            osc_bundles = self._build_xrefd_bundles(
                non_xrefd_bundles,
                self.session_file_paths,
                header_format=header_format,
                )
            input_file_path = self.session_file_paths.get(input_, input_)
            if input_file_path and render_path in input_file_path.parents:
                input_file_path = input_file_path.relative_to(render_path)
            datagram = self._build_datagram(osc_bundles)
            session_file_path = self._build_file_path(
                datagram,
                input_file_path,
                session,
                header_format=header_format,
                sample_format=sample_format,
                sample_rate=sample_rate,
                )
            self.session_file_paths[session] = session_file_path
            prerender_tuple = (
                datagram,
                input_file_path,
                osc_bundles,
                session,
                session_file_path,
                )
            self.prerender_tuples.append(prerender_tuple)
        return self.prerender_tuples

    def _render_datagram(
        self,
        session,
        input_file_path,
        output_file_path,
        session_file_path,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        **kwargs
        ):
        from supriya import new
        relative_session_file_path = session_file_path
        if relative_session_file_path.is_absolute():
            relative_session_file_path = session_file_path.relative_to(
                pathlib.Path.cwd())
        self._report('Rendering {}.'.format(relative_session_file_path))
        if output_file_path.exists():
            self._report('    Skipped {}. Output already exists.'.format(
                relative_session_file_path))
            return 0
        old_server_options = session._options
        new_server_options = new(old_server_options, **kwargs)
        command = self._build_render_command(
            input_file_path,
            output_file_path,
            session_file_path,
            server_options=new_server_options,
            sample_rate=sample_rate,
            header_format=header_format,
            sample_format=sample_format,
            )
        self._report('    Command: {}'.format(command))
        exit_code = self._call_subprocess(command)
        self._report('    Rendered {} with exit code {}.'.format(
            relative_session_file_path, exit_code))
        return exit_code

    def _read(self, file_path, mode=''):
        try:
            with open(str(file_path), 'r' + mode) as file_pointer:
                return file_pointer.read()
        except FileNotFoundError:
            return None

    def _report(self, message):
        if self.transcript_prefix:
            message = '{}{}'.format(self.transcript_prefix, message)
        if self.print_transcript:
            print(message)
        self.transcript.append(message)

    def _reset(self):
        self._compiled_sessions = {}
        self._prerender_tuples = []
        self._session._transcript = self._transcript = []
        self._session_file_paths = {}
        self._trellis = Trellis()

    def _write_datagram(self, file_path, new_contents):
        self._write(file_path, new_contents, mode='b')

    def _write_render_yaml(self, file_path, render_yaml):
        self._write(file_path, render_yaml)

    def _write(self, file_path, new_contents, mode=''):
        cwd = pathlib.Path.cwd()
        relative_file_path = file_path
        if file_path.is_absolute() and cwd in file_path.parents:
            relative_file_path = file_path.relative_to(cwd)
        self._report('Writing {}.'.format(relative_file_path))
        old_contents = self._read(file_path, mode=mode)
        if old_contents == new_contents:
            self._report('    Skipped {}. File already exists.'.format(
                relative_file_path))
        else:
            with open(str(file_path), 'w' + mode) as file_pointer:
                file_pointer.write(new_contents)
            self._report('    Wrote {}.'.format(relative_file_path))

    ### PUBLIC METHODS ###

    def to_lists(
        self,
        duration=None,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        sample_rate=44100,
        ):
        osc_bundles = self.to_osc_bundles(
            duration=duration,
            header_format=header_format,
            sample_format=sample_format,
            sample_rate=sample_rate,
            )
        return [osc_bundle.to_list() for osc_bundle in osc_bundles]

    def to_osc_bundles(
        self,
        duration=None,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        sample_rate=44100,
        ):
        self._reset()
        self._collect_prerender_tuples(
            self.session,
            duration=duration,
            header_format=header_format,
            sample_format=sample_format,
            sample_rate=sample_rate,
            )
        (
            datagram,
            input_file_path,
            osc_bundles,
            session,
            session_file_path,
            ) = self.prerender_tuples[-1]
        return osc_bundles

    def render(
        self,
        output_file_path=None,
        debug=None,
        duration=None,
        header_format=soundfiletools.HeaderFormat.AIFF,
        render_path=None,
        sample_format=soundfiletools.SampleFormat.INT24,
        sample_rate=44100,
        build_render_yml=None,
        **kwargs
        ):
        from supriya import supriya_configuration
        extension = '.{}'.format(header_format.name.lower())
        self.transcript[:] = []
        render_path = render_path or supriya_configuration.output_directory
        render_path = pathlib.Path(render_path).expanduser().absolute()
        if output_file_path is not None:
            output_file_path = pathlib.Path(output_file_path)
            output_file_path = output_file_path.expanduser().absolute()
        original_output_file_path = output_file_path
        self._collect_prerender_tuples(
            self.session,
            duration=duration,
            header_format=header_format,
            render_path=render_path,
            sample_format=sample_format,
            sample_rate=sample_rate,
            )
        assert self.prerender_tuples, self.prerender_tuples
        session_prefixes = []
        for i, prerender_tuple in enumerate(self.prerender_tuples):
            (
                datagram,
                input_file_path,
                osc_bundles,
                session,
                session_file_path,
                ) = prerender_tuple
            prefix = session_file_path.with_suffix('').name
            session_prefixes.append(prefix)
            if i < len(self.prerender_tuples) - 1 or not output_file_path:
                output_file_path = session_file_path.with_suffix(extension)
            else:
                output_file_path = original_output_file_path
            if input_file_path and input_file_path.suffix == '.osc':
                input_file_path = input_file_path.with_suffix(extension)
            with TemporaryDirectoryChange(directory=str(render_path)):
                self._write_datagram(session_file_path, datagram)
                exit_code = self._render_datagram(
                    session,
                    input_file_path,
                    output_file_path,
                    session_file_path,
                    header_format=header_format,
                    sample_format=sample_format,
                    sample_rate=sample_rate,
                    **kwargs
                    )
            if exit_code:
                self._report('    SuperCollider errored!')
                raise NonrealtimeRenderError(exit_code)
        if not output_file_path.is_absolute() and render_path:
            output_file_path = render_path / output_file_path
        if not output_file_path.exists():
            self._report('    Output file is missing!')
            raise NonrealtimeOutputMissing(output_file_path)
        if build_render_yml:
            render_yaml = self._build_render_yaml(session_prefixes)
            self._write_render_yaml(
                output_file_path.parent / 'render.yml',
                render_yaml,
                )
        return exit_code, self.transcript, output_file_path

    ### PUBLIC PROPERTIES ###

    @property
    def compiled_sessions(self):
        return self._compiled_sessions

    @property
    def prerender_tuples(self):
        return self._prerender_tuples

    @property
    def print_transcript(self):
        return self._print_transcript

    @property
    def session(self):
        return self._session

    @property
    def session_file_paths(self):
        return self._session_file_paths

    @property
    def transcript(self):
        return self._transcript

    @property
    def transcript_prefix(self):
        return self._transcript_prefix

    @property
    def trellis(self):
        return self._trellis
