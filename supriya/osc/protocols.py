import contextlib
import dataclasses
import logging
import socket
import time
from collections.abc import Sequence as SequenceABC
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

from ..enums import BootStatus
from ..typing import FutureLike
from .messages import OscBundle, OscMessage

osc_protocol_logger = logging.getLogger(__name__)
osc_in_logger = logging.getLogger("supriya.osc.in")
osc_out_logger = logging.getLogger("supriya.osc.out")
udp_in_logger = logging.getLogger("supriya.udp.in")
udp_out_logger = logging.getLogger("supriya.udp.out")


def find_free_port():
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class OscProtocolOffline(Exception):
    pass


class OscProtocolAlreadyConnected(Exception):
    pass


class OscCallback(NamedTuple):
    pattern: tuple[str | int | float, ...]
    procedure: Callable
    failure_pattern: Optional[Tuple[Union[str, int, float], ...]] = None
    once: bool = False
    args: tuple | None = None
    kwargs: dict | None = None


@dataclasses.dataclass
class HealthCheck:
    request_pattern: List[str]
    response_pattern: List[str]
    active: bool = True
    timeout: float = 1.0
    backoff_factor: float = 1.5
    max_attempts: int = 5


class CaptureEntry(NamedTuple):
    timestamp: float
    label: str
    message: Union[OscMessage, OscBundle]


class Capture:
    ### INITIALIZER ###

    def __init__(self, osc_protocol):
        self.osc_protocol = osc_protocol
        self.messages = []

    ### SPECIAL METHODS ###

    def __enter__(self):
        self.osc_protocol.captures.add(self)
        self.messages[:] = []
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.osc_protocol.captures.remove(self)

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)

    ### PUBLIC METHODS ###

    def filtered(
        self, sent=True, received=True, status=True
    ) -> List[Union[OscBundle, OscMessage]]:
        messages = []
        for _, label, message in self.messages:
            if label == "R" and not received:
                continue
            if label == "S" and not sent:
                continue
            if (
                isinstance(message, OscMessage)
                and message.address in ("/status", "/status.reply")
                and not status
            ):
                continue
            messages.append(message)
        return messages

    ### PUBLIC PROPERTIES ###

    @property
    def received_messages(self):
        return [
            (timestamp, osc_message)
            for timestamp, label, osc_message in self.messages
            if label == "R"
        ]

    @property
    def sent_messages(self):
        return [
            (timestamp, osc_message)
            for timestamp, label, osc_message in self.messages
            if label == "S"
        ]


class OscProtocol:
    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        on_connect_callback: Optional[Callable] = None,
        on_disconnect_callback: Optional[Callable] = None,
        on_panic_callback: Optional[Callable] = None,
    ) -> None:
        self.callbacks: Dict[Any, Any] = {}
        self.captures: Set[Capture] = set()
        self.healthcheck: Optional[HealthCheck] = None
        self.healthcheck_osc_callback: Optional[OscCallback] = None
        self.attempts = 0
        self.ip_address = "127.0.0.1"
        self.name = name
        self.port = 57551
        self.on_connect_callback = on_connect_callback
        self.on_disconnect_callback = on_disconnect_callback
        self.on_panic_callback = on_panic_callback
        self.status = BootStatus.OFFLINE

    ### PRIVATE METHODS ###

    def _activate_healthcheck(self) -> bool:
        if not self.healthcheck:
            return False
        elif self.healthcheck.active:
            return False
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "activating healthcheck..."
        )
        return True

    def _add_callback(self, callback: OscCallback) -> None:
        patterns = [callback.pattern]
        if callback.failure_pattern:
            patterns.append(callback.failure_pattern)
        for pattern in patterns:
            callback_map = self.callbacks
            for item in pattern:
                callbacks, callback_map = callback_map.setdefault(item, ([], {}))
            callbacks.append(callback)

    def _disconnect(self, panicked: bool = False) -> Optional[Awaitable[None]]:
        if panicked:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
                "panicking ..."
            )
        else:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
                "disconnecting ..."
            )
        self.status = BootStatus.QUITTING
        if self.healthcheck_osc_callback is not None:
            self.unregister(self.healthcheck_osc_callback)
        return None

    def _match_callbacks(self, message) -> List[OscCallback]:
        items = (message.address,) + message.contents
        matching_callbacks = []
        callback_map = self.callbacks
        for item in items:
            if item not in callback_map:
                break
            callbacks, callback_map = callback_map[item]
            matching_callbacks.extend(callbacks)
        for callback in matching_callbacks:
            if callback.once:
                self.unregister(callback)
        return matching_callbacks

    def _on_connect(
        self, *, boot_future: FutureLike[bool]
    ) -> Optional[Awaitable[None]]:
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "... connected!"
        )
        self.status = BootStatus.ONLINE
        boot_future.set_result(True)
        return None

    def _on_disconnect(
        self,
        *,
        boot_future: FutureLike[bool],
        exit_future: FutureLike[bool],
        panicked: bool = False,
    ) -> Optional[Awaitable[None]]:
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "... disconnected!"
        )
        self.status = BootStatus.OFFLINE
        if not boot_future.done():
            boot_future.set_result(False)
        if not exit_future.done():
            exit_future.set_result(not panicked)
        return None

    def _on_healthcheck_passed(self, message: OscMessage) -> Optional[Awaitable[None]]:
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "healthcheck: passed"
        )
        self.attempts = 0
        return None

    def _remove_callback(self, callback: OscCallback) -> None:
        def delete(pattern, original_callback_map):
            key = pattern.pop(0)
            if key not in original_callback_map:
                return
            callbacks, callback_map = original_callback_map[key]
            if pattern:
                delete(pattern, callback_map)
            if callback in callbacks:
                callbacks.remove(callback)
            if not callbacks and not callback_map:
                original_callback_map.pop(key)

        patterns = [callback.pattern]
        if callback.failure_pattern:
            patterns.append(callback.failure_pattern)
        for pattern in patterns:
            delete(list(pattern), self.callbacks)

    def _register(
        self,
        pattern,
        procedure,
        *,
        failure_pattern=None,
        once: bool = False,
        args: Optional[Tuple] = None,
        kwargs: Optional[Dict] = None,
    ) -> OscCallback:
        if isinstance(pattern, (str, int, float)):
            pattern = [pattern]
        if isinstance(failure_pattern, (str, int, float)):
            failure_pattern = [failure_pattern]
        if not callable(procedure):
            raise ValueError(procedure)
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            f"registering pattern: {pattern!r}"
        )
        return OscCallback(
            pattern=tuple(pattern),
            failure_pattern=failure_pattern,
            procedure=procedure,
            once=bool(once),
            args=args,
            kwargs=kwargs,
        )

    def _send(self, message):
        if self.status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise OscProtocolOffline
        if not isinstance(message, (str, SequenceABC, OscBundle, OscMessage)):
            raise ValueError(message)
        if isinstance(message, str):
            message = OscMessage(message)
        elif isinstance(message, SequenceABC):
            message = OscMessage(*message)
        osc_out_logger.debug(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            f"{message!r}"
        )
        for capture in self.captures:
            capture.messages.append(
                CaptureEntry(timestamp=time.time(), label="S", message=message)
            )
        datagram = message.to_datagram()
        udp_out_logger.debug(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            f"{datagram}"
        )
        return datagram

    def _setup(
        self, ip_address: str, port: int, healthcheck: Optional[HealthCheck]
    ) -> None:
        self.status = BootStatus.BOOTING
        self.ip_address = ip_address
        self.port = port
        self.healthcheck = healthcheck
        if self.healthcheck:
            self.healthcheck_osc_callback = self.register(
                pattern=self.healthcheck.response_pattern,
                procedure=self._on_healthcheck_passed,
            )

    def _validate_receive(self, datagram):
        udp_in_logger.debug(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            f"{datagram}"
        )
        try:
            message = OscMessage.from_datagram(datagram)
        except Exception:
            raise
        osc_in_logger.debug(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            f"{message!r}"
        )
        for capture in self.captures:
            capture.messages.append(
                CaptureEntry(timestamp=time.time(), label="R", message=message)
            )
        for callback in self._match_callbacks(message):
            yield callback, message

    ### PUBLIC METHODS ###

    def activate_healthcheck(self) -> None:
        raise NotImplementedError

    def capture(self) -> "Capture":
        return Capture(self)

    def disconnect(self) -> Optional[Awaitable[None]]:
        raise NotImplementedError

    def register(
        self,
        pattern: Sequence[Union[str, float]],
        procedure: Callable[[OscMessage], Optional[Awaitable[None]]],
        *,
        failure_pattern: Optional[Sequence[Union[str, float]]] = None,
        once: bool = False,
        args: Optional[Tuple] = None,
        kwargs: Optional[Dict] = None,
    ) -> OscCallback:
        raise NotImplementedError

    def send(self, message: Union[OscBundle, OscMessage, SequenceABC, str]) -> None:
        raise NotImplementedError

    def unregister(self, callback: OscCallback) -> None:
        raise NotImplementedError
