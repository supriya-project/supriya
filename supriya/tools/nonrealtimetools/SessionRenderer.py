# -*- encoding: utf-8 -*-
import hashlib
import os
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

    def _build_bundles(
        self,
        osc_bundles,
        session_file_paths,
        header_format=soundfiletools.HeaderFormat.AIFF,
        ):
        extension = header_format.name.lower()
        for osc_bundle in osc_bundles:
            for osc_message in osc_bundle.contents:
                contents = list(osc_message.contents)
                for i, x in enumerate(contents):
                    try:
                        if x in session_file_paths:
                            session_file_path = session_file_paths[x]
                            session_file_path, _ = os.path.splitext(session_file_path)
                            session_file_path = '{}.{}'.format(session_file_path, extension)
                            contents[i] = session_file_path
                    except TypeError:
                        pass
                osc_message._contents = tuple(contents)
        return osc_bundles

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
            hash_values.append(input_file_path)
        for value in (
            session.options.input_bus_channel_count,
            session.options.output_bus_channel_count,
            sample_rate,
            header_format,
            sample_format,
            ):
            hash_values.append(str(value))
        for value in hash_values:
            if isinstance(value, str):
                value = value.encode()
            md5.update(value)
        md5 = md5.hexdigest()
        file_path = '{}.osc'.format(md5)
        return file_path

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
        server_options = server_options or servertools.ServerOptions()
        scsynth_path = supriya_configuration.scsynth_path
        parts = [scsynth_path, '-N', os.path.relpath(session_file_path)]
        if input_file_path:
            parts.append(os.path.relpath(os.path.expanduser(input_file_path)))
        else:
            parts.append('_')
        parts.append(os.path.relpath(os.path.expanduser(output_file_path)))
        parts.append(str(int(sample_rate)))
        header_format = soundfiletools.HeaderFormat.from_expr(header_format)
        parts.append(header_format.name.lower())  # Must be lowercase.
        sample_format = soundfiletools.SampleFormat.from_expr(sample_format)
        parts.append(sample_format.name.lower())  # Must be lowercase.
        server_options = server_options.as_options_string(realtime=False)
        if server_options:
            parts.append(server_options)
        command = ' '.join(parts)
        return command

    def _call_subprocess(self, command):
        return subprocess.call(command, shell=True)

    def _collect_prerender_data(
        self,
        session,
        duration=None,
        ):
        from supriya.tools import nonrealtimetools
        input_ = session.input_
        bundles = session._to_non_xrefd_osc_bundles(duration)
        self.compiled_sessions[session] = input_, bundles
        if session is self.session:
            self.trellis.add(session)
        if isinstance(input_, nonrealtimetools.Session):
            if input_ not in self.trellis:
                self._collect_prerender_data(input_)
            self.trellis.add(input_, parent=session)
        for bundle in bundles:
            for request in bundle.contents:
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
        render_path='',
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
            input_, osc_bundles = self.compiled_sessions[session]
            osc_bundles = self._build_bundles(
                osc_bundles,
                self.session_file_paths,
                header_format=header_format,
                )
            input_file_path = self.session_file_paths.get(input_, input_)
            if input_file_path and input_file_path.startswith(render_path):
                input_file_path = os.path.relpath(
                    input_file_path, render_path)
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
        self._report('Rendering {}.'.format(
            os.path.relpath(session_file_path)))
        if os.path.exists(output_file_path):
            self._report('    Skipped {}. Output already exists.'.format(
                os.path.relpath(session_file_path)))
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
            os.path.relpath(session_file_path), exit_code))
        return exit_code

    def _read(self, file_path):
        contents = None
        try:
            with open(file_path, 'rb') as file_pointer:
                contents = file_pointer.read()
        except FileNotFoundError:
            pass
        return contents

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

    def _write_datagram(self, file_path, new_datagram):
        self._report('Writing {}.'.format(os.path.relpath(file_path)))
        old_datagram = self._read(file_path)
        if old_datagram == new_datagram:
            self._report('    Skipped {}. OSC file already exists.'.format(
                os.path.relpath(file_path)))
        else:
            with open(file_path, 'wb') as file_pointer:
                file_pointer.write(new_datagram)
            self._report('    Wrote {}.'.format(os.path.relpath(file_path)))

    def _write_render_yaml(self, file_path, session_prefixes):
        self._report('Writing {}.'.format(os.path.relpath(str(file_path))))
        session_prefixes = session_prefixes[:]
        render_data = {'render': session_prefixes.pop(), 'source': None}
        if session_prefixes:
            render_data['source'] = list(reversed(session_prefixes))
        render_yaml = yaml.dump(
            render_data,
            default_flow_style=False,
            indent=4,
            )
        with open(str(file_path), 'w') as file_pointer:
            file_pointer.write(render_yaml)

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
        **kwargs
        ):
        from supriya import supriya_configuration
        render_path = render_path or supriya_configuration.output_directory
        self.transcript[:] = []
        original_output_file_path = output_file_path
        self._collect_prerender_tuples(
            self.session,
            duration=duration,
            header_format=header_format,
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
            prefix = pathlib.Path(session_file_path).with_suffix('').name
            session_prefixes.append(prefix)
            extension = header_format.name.lower()
            if i < len(self.prerender_tuples) - 1 or not output_file_path:
                output_file_path, _ = os.path.splitext(session_file_path)
                output_file_path = '{}.{}'.format(output_file_path, extension)
            else:
                output_file_path = original_output_file_path
            if input_file_path and input_file_path.endswith('.osc'):
                input_file_path, _ = os.path.splitext(input_file_path)
                input_file_path = '{}.{}'.format(input_file_path, extension)
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
        if not os.path.isabs(output_file_path) and render_path:
            output_file_path = os.path.join(
                str(render_path),
                output_file_path,
                )
        if not os.path.exists(output_file_path):
            self._report('    Output file is missing!')
            raise NonrealtimeOutputMissing(output_file_path)
        self._write_render_yaml(
            str(pathlib.Path(output_file_path).parent / 'render.yml'),
            session_prefixes,
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
