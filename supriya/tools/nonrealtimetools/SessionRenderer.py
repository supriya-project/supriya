# -*- encoding: utf-8 -*-
import hashlib
import os
import struct
import subprocess
from supriya.tools import servertools
from supriya.tools import soundfiletools
from supriya.tools.systemtools import SupriyaObject
from supriya.tools.systemtools import Trellis


class SessionRenderer(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_session',
        '_transcript',
        )

    ### INITIALIZER ###

    def __init__(self, session):
        self._session = session
        self._transcript = []

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
        render_path,
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
        if render_path is not None:
            file_path = os.path.join(render_path, file_path)
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
        """
        Builds non-realtime rendering command.

        ::

            >>> session._build_render_command('output.aiff')
            'scsynth -N {} _ output.aiff 44100 aiff int24'

        """
        from abjad.tools import systemtools
        server_options = server_options or servertools.ServerOptions()
        scsynth_path = 'scsynth'
        if not systemtools.IOManager.find_executable('scsynth'):
            found_scsynth = False
            for path in (
                '/Applications/SuperCollider/SuperCollider.app/Contents/MacOS/scsynth',  # pre-7
                '/Applications/SuperCollider/SuperCollider.app/Contents/Resources/scsynth',  # post-7
                ):
                if os.path.exists(path):
                    scsynth_path = path
                    found_scsynth = True
            if not found_scsynth:
                raise Exception('Cannot find scsynth. Is it on your $PATH?')
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

    def _collect_prerender_data(
        self,
        session,
        compiled_sessions,
        trellis,
        duration=None,
        ):
        from supriya.tools import nonrealtimetools
        input_ = session.input_
        bundles = session._to_non_xrefd_osc_bundles(duration)
        compiled_sessions[session] = input_, bundles
        if session is self.session:
            trellis.add(session)
        if isinstance(input_, nonrealtimetools.Session):
            if input_ not in trellis:
                self._collect_prerender_data(
                    input_, compiled_sessions, trellis)
            trellis.add(input_, parent=session)
        for bundle in bundles:
            for request in bundle.contents:
                for x in request.contents:
                    if not isinstance(x, nonrealtimetools.Session):
                        continue
                    if x not in trellis:
                        self._collect_prerender_data(
                            x, compiled_sessions, trellis)
                    trellis.add(x, parent=session)

    def _collect_prerender_tuples(
        self,
        session,
        duration=None,
        render_path=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        ):
        trellis = Trellis()
        compiled_sessions = {}
        session_file_paths = {}
        prerender_tuples = []
        self._collect_prerender_data(
            session,
            compiled_sessions,
            trellis,
            duration=duration,
            )
        assert trellis.is_acyclic()
        for i, session in enumerate(trellis):
            input_, osc_bundles = compiled_sessions[session]
            osc_bundles = self._build_bundles(
                osc_bundles,
                session_file_paths,
                header_format=header_format,
                )
            input_file_path = session_file_paths.get(input_, input_)
            datagram = self._build_datagram(osc_bundles)
            session_file_paths[session] = self._build_file_path(
                datagram,
                input_file_path,
                render_path,
                session,
                header_format=header_format,
                sample_format=sample_format,
                sample_rate=sample_rate,
                )
            session_file_path = session_file_paths[session]
            prerender_tuple = (
                datagram,
                input_file_path,
                osc_bundles,
                session,
                session_file_path,
                )
            prerender_tuples.append(prerender_tuple)
        return prerender_tuples

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
        self.transcript.append('Rendering {}.'.format(
            os.path.relpath(session_file_path)))
        if os.path.exists(output_file_path):
            self.transcript.append(
                '    Skipped {}. Output already exists.'.format(
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
        self.transcript.append('    Command: {}'.format(command))
        exit_code = subprocess.call(command, shell=True)
        self.transcript.append('    Rendered {} with exit code {}.'.format(
            os.path.relpath(session_file_path), exit_code))
        return exit_code

    def _write_datagram(self, file_path, datagram):
        self.transcript.append(
            'Writing {}.'.format(os.path.relpath(file_path)))
        should_write = True
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file_pointer:
                if file_pointer.read() == datagram:
                    should_write = False
        if should_write:
            with open(file_path, 'wb') as file_pointer:
                file_pointer.write(datagram)
            self.transcript.append(
                '    Wrote {}.'.format(os.path.relpath(file_path)))
        else:
            self.transcript.append(
                '    Skipped {}. OSC file already exists.'.format(
                    os.path.relpath(file_path)))

    ### PUBLIC METHODS ###

    def to_lists(
        self,
        duration=None,
        header_format=soundfiletools.HeaderFormat.AIFF,
        render_path=None,
        sample_format=soundfiletools.SampleFormat.INT24,
        sample_rate=44100,
        ):
        osc_bundles = self.to_osc_bundles(
            duration=duration,
            header_format=header_format,
            render_path=render_path,
            sample_format=sample_format,
            sample_rate=sample_rate,
            )
        return [osc_bundle.to_list() for osc_bundle in osc_bundles]

    def to_osc_bundles(
        self,
        duration=None,
        header_format=soundfiletools.HeaderFormat.AIFF,
        render_path=None,
        sample_format=soundfiletools.SampleFormat.INT24,
        sample_rate=44100,
        ):
        prerender_tuples = self._collect_prerender_tuples(
            self.session,
            duration=duration,
            header_format=header_format,
            render_path=render_path,
            sample_format=sample_format,
            sample_rate=sample_rate,
            )
        (
            datagram,
            input_file_path,
            osc_bundles,
            session,
            session_file_path,
            ) = prerender_tuples[-1]
        return osc_bundles

    def render(
        self,
        output_file_path,
        debug=None,
        duration=None,
        header_format=soundfiletools.HeaderFormat.AIFF,
        render_path=None,
        sample_format=soundfiletools.SampleFormat.INT24,
        sample_rate=44100,
        **kwargs
        ):
        self.transcript[:] = []
        original_output_file_path = output_file_path
        prerender_tuples = self._collect_prerender_tuples(
            self.session,
            duration=duration,
            render_path=render_path,
            header_format=header_format,
            sample_format=sample_format,
            sample_rate=sample_rate,
            )
        assert prerender_tuples, prerender_tuples
        for i, prerender_tuple in enumerate(prerender_tuples):
            (
                datagram,
                input_file_path,
                osc_bundles,
                session,
                session_file_path,
                ) = prerender_tuple
            extension = header_format.name.lower()
            if i < len(prerender_tuples) - 1:
                output_file_path, _ = os.path.splitext(session_file_path)
                output_file_path = '{}.{}'.format(output_file_path, extension)
            else:
                output_file_path = original_output_file_path
            if input_file_path and input_file_path.endswith('.osc'):
                input_file_path, _ = os.path.splitext(input_file_path)
                input_file_path = '{}.{}'.format(input_file_path, extension)
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
                raise Exception(exit_code)
        return exit_code, self.transcript

    ### PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session

    @property
    def transcript(self):
        return self._transcript
