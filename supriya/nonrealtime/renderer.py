import asyncio
import hashlib
import logging
import pathlib
import platform
import shutil
import struct
from os import PathLike
from typing import List, Optional, Tuple

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

logger = logging.getLogger(__name__)


class SessionRenderer(SupriyaObject):
    """
    Renders non-realtime sessions as audio files.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        session: "supriya.nonrealtime.sessions.Session",
        header_format: HeaderFormatLike = HeaderFormat.AIFF,
        render_directory_path: Optional[PathLike] = None,
        sample_format: SampleFormatLike = SampleFormat.INT24,
        sample_rate: int = 44100,
    ):
        self._session = session
        self._header_format = HeaderFormat.from_expr(header_format)
        self._render_directory_path = pathlib.Path(
            render_directory_path or supriya.output_path
        ).resolve()
        self._sample_format = SampleFormat.from_expr(sample_format)
        self._sample_rate = int(sample_rate)
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
        server_options: Optional[scsynth.Options] = None,
    ):
        options = new(server_options or scsynth.Options(), realtime=False)
        command = list(options)
        command.extend(["-N", session_osc_file_path])
        command.append(input_file_path or "_")
        command.extend(
            [
                output_file_path,
                self.sample_rate,
                self.header_format.name.lower(),  # Must be lowercase.
                self.sample_format.name.lower(),  # Must be lowercase.
            ]
        )
        return [str(_) for _ in command]

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

    async def _render_datagram(
        self,
        session,
        input_file_path,
        output_file_path,
        session_osc_file_path,
        scsynth_path=None,
        **kwargs,
    ):
        relative_session_osc_file_path = session_osc_file_path
        logger.info(f"Rendering {relative_session_osc_file_path}.")
        if output_file_path.exists():
            logger.info(
                f"    Skipped {relative_session_osc_file_path}. Output already exists."
            )
            return 0
        server_options = session._options
        server_options = new(server_options, **kwargs)
        memory_size = server_options.memory_size
        for factor in range(1, 6):
            command = self._build_render_command(
                input_file_path,
                output_file_path.name,
                session_osc_file_path,
                server_options=server_options,
            )
            logger.info(f"    Command: {' '.join(command)}")
            exit_future = asyncio.get_running_loop().create_future()
            protocol = AsyncProcessProtocol(exit_future)
            await protocol.run(command, self.render_directory_path)
            await exit_future
            exit_code = exit_future.result()
            if exit_code == -6:
                logger.info(
                    f"    Out of memory. Increasing to {server_options.memory_size}."
                )
            else:
                logger.info(
                    f"    Rendered {relative_session_osc_file_path} with exit code {exit_code}."
                )
                break
            server_options = new(
                server_options, memory_size=memory_size * (2**factor)
            )
        return exit_code

    def _read_datagram(self, file_path):
        try:
            with open(str(file_path), "rb") as file_pointer:
                return file_pointer.read()
        except FileNotFoundError:
            return None

    def _reset(self):
        self._compiled_sessions = {}
        self._prerender_tuples = []
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
        logger.info(f"Writing {file_path.name}.")
        old_contents = None
        if file_path.exists():
            old_contents = file_path.read_bytes()
        if old_contents == new_contents:
            logger.info(f"    Skipped {file_path.name}. File already exists.")
        else:
            file_path.write_bytes(new_contents)
            logger.info(f"    Wrote {file_path.name}.")

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

    async def render(
        self,
        output_file_path: Optional[PathLike] = None,
        duration: Optional[float] = None,
        scsynth_path: Optional[str] = None,
        **kwargs,
    ) -> Tuple[int, pathlib.Path]:
        import supriya.nonrealtime

        if output_file_path is not None:
            output_file_path = pathlib.Path(output_file_path).resolve()
        self._collect_prerender_tuples(self.session, duration=duration)
        assert self.prerender_tuples, self.prerender_tuples
        extension = f".{self.header_format.name.lower()}"
        visited_renderable_prefixes = []
        for prerender_tuple in self.prerender_tuples:
            renderable = prerender_tuple[0]
            renderable_prefix = self.renderable_prefixes[renderable]
            visited_renderable_prefixes.append(renderable_prefix.with_suffix("").name)
            relative_output_file_path = renderable_prefix.with_suffix(extension)
            if not isinstance(renderable, supriya.nonrealtime.Session):
                result = renderable.__render__(
                    output_file_path=self.render_directory_path
                    / relative_output_file_path
                )
                if asyncio.iscoroutine(result):
                    await result
                continue
            (session, datagram, input_, _) = prerender_tuple
            osc_file_path = renderable_prefix.with_suffix(".osc")
            input_file_path = self.session_input_paths.get(session)
            self._write_datagram(self.render_directory_path / osc_file_path, datagram)
            exit_code = await self._render_datagram(
                session,
                input_file_path,
                self.render_directory_path / relative_output_file_path,
                osc_file_path,
                scsynth_path=scsynth_path,
                **kwargs,
            )
            if exit_code:
                if (
                    platform.system() == "Windows"
                    and (
                        self.render_directory_path / relative_output_file_path
                    ).exists()
                ):
                    # scsynth.exe renders but exits non-zero
                    # https://github.com/supercollider/supercollider/issues/5769
                    # logger.info(
                    #     "    SuperCollider exited with non-zero but output exists!"
                    # )
                    pass
                else:
                    logger.info("    SuperCollider errored!")
                    raise NonrealtimeRenderError(exit_code)
        final_rendered_file_path = (
            self.render_directory_path / relative_output_file_path
        )
        if not final_rendered_file_path.exists():
            logger.info("    Output file is missing!")
            raise NonrealtimeOutputMissing(final_rendered_file_path)
        # TODO: Make this cross-platform
        if output_file_path is not None:
            shutil.copy(final_rendered_file_path, output_file_path)
        return (exit_code, output_file_path or final_rendered_file_path)

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


class AsyncProcessProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future: asyncio.Future):
        self.buffer_ = ""
        self.exit_future = exit_future

    async def run(self, command: List[str], render_directory_path: pathlib.Path):
        _, _ = await asyncio.get_running_loop().subprocess_exec(
            lambda: self,
            *command,
            stdin=None,
            stderr=None,
            start_new_session=True,
            cwd=render_directory_path,
        )

    def handle_line(self, line):
        logger.debug(f"Received: {line}")

    def connection_made(self, transport):
        self.transport = transport

    def pipe_data_received(self, fd, data):
        # *nix and OSX return full lines,
        # but Windows will return partial lines
        # which obligates us to reconstruct them.
        text = self.buffer_ + data.decode().replace("\r\n", "\n")
        if "\n" in text:
            text, _, self.buffer_ = text.rpartition("\n")
            for line in text.splitlines():
                self.handle_line(line)
        else:
            self.buffer_ = text

    def process_exited(self):
        self.exit_future.set_result(self.transport.get_returncode())
