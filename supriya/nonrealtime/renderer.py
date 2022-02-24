import hashlib
import pathlib
import shutil
import struct
import subprocess
from os import PathLike
from typing import Any, Optional, Tuple

import tqdm  # type: ignore
import uqbar.containers
import uqbar.io
import yaml
from uqbar.objects import new

import supriya
import supriya.realtime
import supriya.soundfiles
import supriya.system
from supriya import HeaderFormat, SampleFormat, scsynth
from supriya.exceptions import NonrealtimeOutputMissing, NonrealtimeRenderError
from supriya.system import SupriyaObject
from supriya.typing import HeaderFormatLike, SampleFormatLike


class SessionRenderer(SupriyaObject):
    """
    Renders non-realtime sessions as audio files.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        session: "supriya.nonrealtime.sessions.Session",
        header_format: HeaderFormatLike = HeaderFormat.AIFF,
        print_transcript: bool = False,
        render_directory_path: Optional[PathLike] = None,
        sample_format: SampleFormatLike = SampleFormat.INT24,
        sample_rate: int = 44100,
        transcript_prefix: Optional[str] = None,
    ):
        self._session = session

        self._header_format = HeaderFormat.from_expr(header_format)

        if print_transcript:
            print_transcript = bool(print_transcript)
        self._print_transcript = print_transcript

        self._render_directory_path = (
            pathlib.Path(render_directory_path or supriya.output_path)
            .expanduser()
            .absolute()
        )

        self._sample_format = SampleFormat.from_expr(sample_format)

        self._sample_rate = int(sample_rate)

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
            size = struct.pack(">i", size)
            datagrams.append(size)
            datagrams.append(datagram)
        datagram = b"".join(datagrams)
        return datagram

    def _build_file_path(self, datagram, input_file_path, session):
        # print('BUILDING FILE PATH')
        md5 = hashlib.md5()
        md5.update(datagram)
        hash_values = []
        if input_file_path is not None:
            hash_values.append(input_file_path)
        for value in (
            session.options.input_bus_channel_count,
            session.options.output_bus_channel_count,
            self.sample_rate,
            self.header_format,
            self.sample_format,
        ):
            hash_values.append(value)
        for value in hash_values:
            if not isinstance(value, str):
                value = str(value)
            value = value.encode()
            md5.update(value)
        md5 = md5.hexdigest()
        file_path = "session-{}.osc".format(md5)
        return pathlib.Path(file_path)

    def _build_render_command(
        self,
        input_file_path,
        output_file_path,
        session_osc_file_path,
        *,
        scsynth_path=None,
        server_options=None,
    ):
        cwd = pathlib.Path.cwd()
        scsynth_path = scsynth.find(scsynth_path)
        server_options = server_options or scsynth.Options()
        if session_osc_file_path.is_absolute():
            session_osc_file_path = session_osc_file_path.relative_to(cwd)
        parts = [scsynth_path, "-N", session_osc_file_path]
        if input_file_path:
            parts.append(input_file_path)
        else:
            parts.append("_")
        if output_file_path.is_absolute() and cwd in output_file_path.parents:
            output_file_path = output_file_path.relative_to(cwd)
        parts.append(output_file_path)
        parts.append(self.sample_rate)
        parts.append(self.header_format.name.lower())  # Must be lowercase.
        parts.append(self.sample_format.name.lower())  # Must be lowercase.
        server_options = server_options.as_options_string(realtime=False)
        if server_options:
            parts.append(server_options)
        command = " ".join(str(_) for _ in parts)
        return command

    def _build_render_yml(self, session_prefixes):
        session_prefixes = session_prefixes[:]
        render_data = {"render": session_prefixes.pop(), "source": None}
        if session_prefixes:
            render_data["source"] = list(reversed(session_prefixes))
        render_yaml = yaml.dump(render_data, default_flow_style=False, indent=4)
        return render_yaml

    def _build_xrefd_bundles(self, osc_bundles):
        extension = ".{}".format(self.header_format.name.lower())
        for osc_bundle in osc_bundles:
            for osc_message in osc_bundle.contents:
                contents = list(osc_message.contents)
                for i, x in enumerate(contents):
                    x = self._sessionable_to_session(x)
                    try:
                        if x not in self.renderable_prefixes:
                            continue
                    except TypeError:
                        continue
                    renderable_file_path = self.renderable_prefixes[x].with_suffix(
                        extension
                    )
                    contents[i] = str(renderable_file_path)
                osc_message.contents = tuple(contents)
        return osc_bundles

    def _build_dependency_graph_and_nonxrefd_osc_bundles_conditionally(
        self, expr, parent
    ):
        import supriya.nonrealtime

        expr = self._sessionable_to_session(expr)
        if isinstance(expr, supriya.nonrealtime.Session):
            if expr not in self.dependency_graph:
                self._build_dependency_graph_and_nonxrefd_osc_bundles(expr)
            self.dependency_graph.add(expr, parent=parent)
        elif hasattr(expr, "__render__"):
            self.dependency_graph.add(expr, parent=parent)

    def _build_dependency_graph_and_nonxrefd_osc_bundles(self, session, duration=None):
        input_ = session.input_
        if isinstance(input_, str):
            input_ = pathlib.Path(input_)
        input_ = self._sessionable_to_session(input_)
        non_xrefd_bundles = session._to_non_xrefd_osc_bundles(duration)
        self.compiled_sessions[session] = input_, non_xrefd_bundles
        if session is self.session:
            self.dependency_graph.add(session)
        self._build_dependency_graph_and_nonxrefd_osc_bundles_conditionally(
            input_, session
        )
        for non_xrefd_bundle in non_xrefd_bundles:
            for request in non_xrefd_bundle.contents:
                for x in request.contents:
                    self._build_dependency_graph_and_nonxrefd_osc_bundles_conditionally(
                        x, session
                    )

    def _call_subprocess(self, command):
        return subprocess.call(command, shell=True)

    def _stream_subprocess(self, command, session_duration):
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        previous_value = 0
        progress_bar = tqdm.tqdm(
            bar_format=(), total=int(session_duration * 1000), unit="ms"
        )
        with progress_bar:
            while True:
                output = process.stdout.readline()
                if not output:
                    if process.poll() is not None:
                        break
                    continue
                output = output.decode().strip()
                if output.startswith("nextOSCPacket"):
                    current_value = int(float(output.split()[-1]) * 1000)
                    difference = current_value - previous_value
                    progress_bar.update(difference)
                    previous_value = current_value
                elif output.startswith("FAILURE"):
                    if output.startswith("FAILURE IN SERVER /n_free Node"):
                        continue
                    progress_bar.write(output)
                elif output.startswith("start time 0"):
                    continue
                else:
                    progress_bar.write("WARNING: {}".format(output))
                    if output.startswith("alloc failed"):
                        return -6
        return process.poll()

    def _collect_prerender_tuples(self, session, duration=None):
        import supriya.nonrealtime

        self._build_dependency_graph_and_nonxrefd_osc_bundles(
            session, duration=duration
        )
        assert self.dependency_graph.is_acyclic()
        extension = ".{}".format(self.header_format.name.lower())
        for renderable in self.dependency_graph:
            if isinstance(renderable, supriya.nonrealtime.Session):
                result = self._collect_session_prerender_tuple(renderable, extension)
                prerender_tuple, renderable_prefix = result
            else:
                result = self._collect_renderable_prerender_tuple(renderable)
                prerender_tuple, renderable_prefix = result
            self.prerender_tuples.append(prerender_tuple)
            self.renderable_prefixes[renderable] = renderable_prefix
        return self.prerender_tuples

    def _collect_renderable_prerender_tuple(self, renderable):
        renderable_prefix = renderable._build_file_path().with_suffix("")
        return (renderable,), renderable_prefix

    def _collect_session_prerender_tuple(self, session, extension):
        input_, non_xrefd_bundles = self.compiled_sessions[session]
        osc_bundles = self._build_xrefd_bundles(non_xrefd_bundles)
        input_file_path = input_
        if input_ and input_ in self.renderable_prefixes:
            input_file_path = self.renderable_prefixes[input_]
            input_file_path = input_file_path.with_suffix(extension)
        if input_file_path:
            input_file_path = self.get_path_relative_to_render_path(
                input_file_path, self.render_directory_path
            )
            self.session_input_paths[session] = input_file_path
        datagram = self._build_datagram(osc_bundles)
        renderable_prefix = self._build_file_path(
            datagram, input_file_path, session
        ).with_suffix("")
        return (session, datagram, input_, osc_bundles), renderable_prefix

    def _render_datagram(
        self,
        session,
        input_file_path,
        output_file_path,
        session_osc_file_path,
        scsynth_path=None,
        **kwargs,
    ):
        relative_session_osc_file_path = session_osc_file_path
        if relative_session_osc_file_path.is_absolute():
            relative_session_osc_file_path = session_osc_file_path.relative_to(
                pathlib.Path.cwd()
            )
        self._report("Rendering {}.".format(relative_session_osc_file_path))
        if output_file_path.exists():
            self._report(
                "    Skipped {}. Output already exists.".format(
                    relative_session_osc_file_path
                )
            )
            return 0
        server_options = session._options
        server_options = new(server_options, **kwargs)
        memory_size = server_options.memory_size
        for factor in range(1, 6):
            command = self._build_render_command(
                input_file_path,
                output_file_path,
                session_osc_file_path,
                scsynth_path=scsynth_path,
                server_options=server_options,
            )
            self._report("    Command: {}".format(command))
            try:
                exit_code = self._stream_subprocess(command, session.duration)
            except KeyboardInterrupt:
                if output_file_path.exists():
                    output_file_path.unlink()
                raise
            server_options = new(
                server_options, memory_size=memory_size * (2**factor)
            )
            if exit_code == -6:
                self._report(
                    "    Out of memory. Increasing to {}.".format(
                        server_options.memory_size
                    )
                )
            else:
                self._report(
                    "    Rendered {} with exit code {}.".format(
                        relative_session_osc_file_path, exit_code
                    )
                )
                break
        return exit_code

    def _read(self, file_path, mode=""):
        try:
            with open(str(file_path), "r" + mode) as file_pointer:
                return file_pointer.read()
        except FileNotFoundError:
            return None

    def _report(self, message):
        if self.transcript_prefix:
            message = "{}{}".format(self.transcript_prefix, message)
        if self.print_transcript:
            print(message)
        self.transcript.append(message)

    def _reset(self):
        self._compiled_sessions = {}
        self._prerender_tuples = []
        self._session._transcript = self._transcript = []
        self._renderable_prefixes = {}
        self._dependency_graph = uqbar.containers.DependencyGraph()
        self._session_input_paths = {}
        self._sessionables_to_sessions = {}

    def _sessionable_to_session(self, expr):
        if hasattr(expr, "__session__"):
            if expr not in self._sessionables_to_sessions:
                self._sessionables_to_sessions[expr] = expr.__session__()
            return self._sessionables_to_sessions[expr]
        return expr

    def _write_datagram(self, file_path, new_contents):
        self._write(file_path, new_contents, mode="b")

    def _write_render_yml(self, file_path, render_yaml):
        self._write(file_path, render_yaml)

    def _write(self, file_path, new_contents, mode=""):
        cwd = pathlib.Path.cwd()
        relative_file_path = file_path
        if file_path.is_absolute() and cwd in file_path.parents:
            relative_file_path = file_path.relative_to(cwd)
        self._report("Writing {}.".format(relative_file_path))
        old_contents = self._read(file_path, mode=mode)
        if old_contents == new_contents:
            self._report(
                "    Skipped {}. File already exists.".format(relative_file_path)
            )
        else:
            with open(str(file_path), "w" + mode) as file_pointer:
                file_pointer.write(new_contents)
            self._report("    Wrote {}.".format(relative_file_path))

    ### PUBLIC METHODS ###

    def to_lists(self, duration=None):
        osc_bundles = self.to_osc_bundles(duration=duration)
        return [osc_bundle.to_list() for osc_bundle in osc_bundles]

    def to_osc_bundles(self, duration=None):
        self._collect_prerender_tuples(self.session, duration=duration)
        (session, datagram, input_file_path, osc_bundles) = self.prerender_tuples[-1]
        return osc_bundles

    @classmethod
    def get_path_relative_to_render_path(cls, target_path, render_path):
        target_path = pathlib.Path(target_path)
        render_path = pathlib.Path(render_path)
        try:
            return target_path.relative_to(render_path)
        except ValueError:
            pass
        target_path = pathlib.Path(target_path)
        render_path = pathlib.Path(render_path)
        target_path_parents = set(target_path.parents)
        render_path_parents = set(render_path.parents)
        common_parents = target_path_parents.intersection(render_path_parents)
        if not common_parents:
            return target_path
        common_parent = sorted(common_parents)[-1]
        target_path = target_path.relative_to(common_parent)
        render_path = render_path.relative_to(common_parent)
        parts = [".." for _ in render_path.parts] + [target_path]
        return pathlib.Path().joinpath(*parts)

    def render(
        self,
        output_file_path: Optional[PathLike] = None,
        debug: bool = False,
        duration: Optional[float] = None,
        build_render_yml: bool = False,
        scsynth_path: Optional[str] = None,
        **kwargs,
    ) -> Tuple[int, Any, pathlib.Path]:
        import supriya.nonrealtime

        if output_file_path is not None:
            output_file_path = pathlib.Path(output_file_path).expanduser().absolute()

        self._collect_prerender_tuples(self.session, duration=duration)
        assert self.prerender_tuples, self.prerender_tuples

        extension = ".{}".format(self.header_format.name.lower())
        visited_renderable_prefixes = []

        with uqbar.io.DirectoryChange(directory=str(self.render_directory_path)):
            for prerender_tuple in self.prerender_tuples:
                renderable = prerender_tuple[0]
                renderable_prefix = self.renderable_prefixes[renderable]
                visited_renderable_prefixes.append(
                    renderable_prefix.with_suffix("").name
                )
                relative_output_file_path = renderable_prefix.with_suffix(extension)
                if isinstance(renderable, supriya.nonrealtime.Session):
                    (session, datagram, input_, _) = prerender_tuple
                    osc_file_path = renderable_prefix.with_suffix(".osc")
                    input_file_path = self.session_input_paths.get(session)
                    self._write_datagram(osc_file_path, datagram)
                    exit_code = self._render_datagram(
                        session,
                        input_file_path,
                        relative_output_file_path,
                        osc_file_path,
                        scsynth_path=scsynth_path,
                        **kwargs,
                    )
                    if exit_code:
                        self._report("    SuperCollider errored!")
                        raise NonrealtimeRenderError(exit_code)
                else:
                    renderable.__render__(
                        output_file_path=relative_output_file_path,
                        print_transcript=self.print_transcript,
                    )

        final_rendered_file_path = (
            self.render_directory_path / relative_output_file_path
        )
        if not final_rendered_file_path.exists():
            self._report("    Output file is missing!")
            raise NonrealtimeOutputMissing(final_rendered_file_path)

        if output_file_path is not None:
            shutil.copy(final_rendered_file_path, output_file_path)

        if build_render_yml:
            output_directory = (output_file_path or final_rendered_file_path).parent
            render_yaml = self._build_render_yml(visited_renderable_prefixes)
            self._write_render_yml(output_directory / "render.yml", render_yaml)

        return (
            exit_code,
            self.transcript,
            output_file_path or final_rendered_file_path,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def compiled_sessions(self):
        return self._compiled_sessions

    @property
    def dependency_graph(self):
        return self._dependency_graph

    @property
    def header_format(self) -> HeaderFormat:
        return self._header_format

    @property
    def prerender_tuples(self):
        return self._prerender_tuples

    @property
    def print_transcript(self) -> bool:
        return self._print_transcript

    @property
    def render_directory_path(self) -> pathlib.Path:
        return self._render_directory_path

    @property
    def renderable_prefixes(self):
        return self._renderable_prefixes

    @property
    def sample_format(self) -> SampleFormat:
        return self._sample_format

    @property
    def sample_rate(self) -> int:
        return self._sample_rate

    @property
    def session(self) -> "supriya.nonrealtime.sessions.Session":
        return self._session

    @property
    def session_input_paths(self):
        return self._session_input_paths

    @property
    def transcript(self):
        return self._transcript

    @property
    def transcript_prefix(self):
        return self._transcript_prefix
