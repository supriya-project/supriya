"""
Tools for interacting with non-realtime execution contexts.
"""
import asyncio
import hashlib
import logging
import platform
import shutil
import struct
from contextlib import ExitStack
from os import PathLike
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Iterator, List, Optional, SupportsInt, Tuple, Type, Union

from uqbar.objects import new

from ..assets.synthdefs import system_synthdefs
from ..enums import CalculationRate, HeaderFormat, SampleFormat
from ..osc import OscBundle
from ..scsynth import AsyncNonrealtimeProcessProtocol, Options
from ..synthdefs import SynthDef
from ..typing import HeaderFormatLike, SampleFormatLike, SupportsOsc
from .core import Context, ContextError, ContextObject, Node
from .requests import DoNothing, RequestBundle, Requestable

logger = logging.getLogger(__name__)


class Score(Context):
    """
    A non-realtime execution context.

    :param options: The context's options.
    :param kwargs: Keyword arguments for options.
    """

    ### INITIALIZER ###

    def __init__(self, options: Optional[Options] = None, **kwargs):
        super().__init__(options=options, **kwargs)
        self._requests: Dict[float, List[Requestable]] = {}

    ### CLASS METHODS ###

    async def __render__(
        self,
        *,
        output_file_path: Optional[PathLike] = None,
        render_directory_path: Optional[PathLike] = None,
        **kwargs,
    ) -> Tuple[Optional[Path], int]:
        return await self.render(
            output_file_path,
            render_directory_path=render_directory_path,
            **kwargs,
        )

    ### PRIVATE METHODS ###

    def _free_id(
        self,
        type_: Type[ContextObject],
        id_: int,
        calculation_rate: Optional[CalculationRate] = None,
    ) -> None:
        pass

    def _resolve_node(self, node: Union[Node, SupportsInt, None]) -> int:
        if node is None:
            return 0
        return int(node)

    def _validate_can_request(self) -> None:
        if self._get_moment() is None:
            raise ContextError

    def _validate_moment_timestamp(self, seconds: Optional[float]) -> None:
        if seconds is None or seconds < 0:
            raise ContextError

    ### PUBLIC METHODS ###

    async def render(
        self,
        output_file_path: Optional[PathLike] = None,
        *,
        duration: Optional[float] = None,
        header_format: HeaderFormatLike = HeaderFormat.AIFF,
        input_file_path: Optional[PathLike] = None,
        options: Optional[Options] = None,
        render_directory_path: Optional[PathLike] = None,
        sample_format: SampleFormatLike = SampleFormat.INT24,
        sample_rate: float = 44100,
        suppress_output: bool = False,
        **kwargs,
    ) -> Tuple[Optional[Path], int]:
        """
        Render the score.

        :param duration: Optional duration to render the score until.
        :param header_format: The :term:`header format` to render with.
        :param input_file_path: The input file to render with.
        :param options: The context's options.
        :param render_directory_path: The directory to render the output in. This
            affords using relative paths and (therefore) stable hashes when rendering
            multiple scores that interrelate.
        :param sample_format: The :term:`sample format` to render with.
        :param sample_rate: The sample rate to render at.
        :param suppress_output: Flag for writing the output soundfile to ``/dev/null``
            (or equivalent).
        :param kwargs: Keyword arguments for options.

        :return: A pair of the output path (if output exists) and the process exit code.
            If no output file path was provided, one will be generated based on the hash
            of the score's datagram, its input file (if provided) and any flags to
            ``scsynth`` that affect rendering.
        """
        from .. import output_path

        # validate inputs
        header_format_ = HeaderFormat.from_expr(header_format).name.lower()
        sample_format_ = SampleFormat.from_expr(sample_format).name.lower()
        # build initial command
        command = new(options or self._options, **kwargs, realtime=False).serialize()
        # build datagram
        datagram_pieces: List[bytes] = []
        for datagram_piece in self.iterate_datagrams(until=duration):
            datagram_pieces.append(struct.pack(">i", len(datagram_piece)))
            datagram_pieces.append(datagram_piece)
        datagram = b"".join(datagram_pieces)
        # setup render directory
        exit_stack = ExitStack()
        with exit_stack:
            # setup render directory
            if render_directory_path:
                render_directory_path_ = Path(render_directory_path).resolve()
            else:
                render_directory_path_ = Path(
                    exit_stack.enter_context(TemporaryDirectory())
                )
            logger.info(f"Render directory: {render_directory_path_}")
            # calculate input path relative to render directory
            input_file_path_ = "_"  # underscore, not dash
            if input_file_path:
                input_file_path_ = str(Path(input_file_path).resolve())
            # build file name
            hasher = hashlib.sha256()
            hasher.update(datagram)
            hasher.update((" ".join(command[1:])).encode())
            hasher.update(input_file_path_.encode())
            hasher.update(str(sample_rate).encode())
            digest = hasher.hexdigest()
            # build render file path and output file path
            if suppress_output:
                render_file_name = (
                    "NUL" if platform.system() == "Windows" else "/dev/null"
                )
                output_file_path_ = None
            else:
                render_file_name = f"score-{digest}.{header_format_}"
                output_file_path_ = Path(
                    output_file_path or (output_path / render_file_name)
                )
            # write .osc file
            osc_file_name = f"score-{digest}.osc"
            (render_directory_path_ / osc_file_name).write_bytes(datagram)
            # build nonrealtime command
            command.extend(
                [
                    "-N",
                    osc_file_name,
                    input_file_path_,
                    render_file_name,
                    str(sample_rate),
                    header_format_,
                    sample_format_,
                ]
            )
            # render the datagram
            exit_future = asyncio.get_running_loop().create_future()
            protocol = AsyncNonrealtimeProcessProtocol(exit_future)
            await protocol.run(command, render_directory_path_)
            exit_code: int = await exit_future
            assert render_directory_path_ / render_file_name
            if output_file_path_:
                shutil.copy(
                    render_directory_path_ / render_file_name, output_file_path_
                )
        return output_file_path_, exit_code

    def iterate_datagrams(self, until: Optional[float] = None) -> Iterator[bytes]:
        """
        Iterate datagrams.

        :param until: Timestamp to stop iterating at.
        """
        for osc_bundle in self.iterate_osc_bundles(until=until):
            yield osc_bundle.to_datagram(realtime=False)

    def iterate_osc_bundles(self, until: Optional[float] = None) -> Iterator[OscBundle]:
        """
        Iterate OSC bundles.

        :param until: Timestamp to stop iterating at.
        """
        for request_bundle in self.iterate_request_bundles(until=until):
            yield request_bundle.to_osc()

    def iterate_request_bundles(
        self, until: Optional[float] = None
    ) -> Iterator[RequestBundle]:
        """
        Iterate request bundles.

        :param until: Timestamp to stop iterating at.
        """
        for timestamp, requests in sorted(self._requests.items()):
            if until:
                if timestamp == until:
                    yield RequestBundle(
                        timestamp=timestamp, contents=requests + [DoNothing()]
                    )
                    return
                elif timestamp > until:
                    yield RequestBundle(timestamp=until, contents=[DoNothing()])
                    return
            if requests:
                yield RequestBundle(timestamp=timestamp, contents=requests)
        if until and until > timestamp:
            yield RequestBundle(timestamp=until, contents=[DoNothing()])

    def send(self, message: SupportsOsc) -> None:
        """
        Send a message to the execution context.

        :param message: The message to send.
        """
        if not isinstance(message, RequestBundle):
            raise ContextError
        elif message.timestamp is None:
            raise ContextError
        self._requests.setdefault(message.timestamp, []).extend(message.contents)

    def setup_system_synthdefs(self) -> None:
        """
        Load all system synthdefs.
        """
        synthdefs = []
        for name in dir(system_synthdefs):
            synthdef = getattr(system_synthdefs, name)
            if isinstance(synthdef, SynthDef):
                synthdefs.append(synthdef)
        with self.at(0):
            self.add_synthdefs(*synthdefs)
