import asyncio
import contextlib
import difflib
import logging
import textwrap
import time
import warnings
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from pytest_lazy_fixtures import lf

import supriya


async def get(x):
    # if x is awaitable, await it
    if asyncio.iscoroutine(x):
        return await x
    # otherwise just return it
    return x


@pytest.fixture
def server() -> Generator[supriya.Server, None, None]:
    # setup
    server = supriya.Server(name="test-server").boot()
    # yield to test
    yield server
    # teardown, even if the test fails
    server.quit()


@pytest_asyncio.fixture
async def async_server() -> AsyncGenerator[supriya.AsyncServer, None]:
    # setup
    server = await supriya.AsyncServer(name="test-server").boot()
    # yield to test
    yield server
    # teardown, even if the test fails
    await server.quit()


@pytest_asyncio.fixture(params=[supriya.AsyncServer, supriya.Server])
async def context(
    request,
) -> AsyncGenerator[supriya.AsyncServer | supriya.Server, None]:
    # this fixture will cause tests using it to run twice:
    # the context class is first AsyncServer, then Server
    context_class = request.param
    # instantiation looks the same
    context = context_class(name="test-server")
    # booting might need to be awaited
    await get(context.boot())
    # yield the context
    yield context
    # quitting might need to be awaited
    await get(context.quit())


@pytest.mark.asyncio
async def test_async(async_server: supriya.AsyncServer) -> None:
    # operation
    actual_tree = str(await async_server.query_tree())
    # validation
    expected_tree = textwrap.dedent(
        """\
        NODE TREE 0 group
            1 group
        """
    )
    assert actual_tree == expected_tree


@pytest.mark.asyncio
async def test_async_and_sync(context: supriya.AsyncServer | supriya.Server) -> None:
    # operation
    actual_tree = str(await get(context.query_tree()))
    # validate they're the same
    expected_tree = textwrap.dedent(
        """\
        NODE TREE 0 group
            1 group
        """
    )
    assert actual_tree == expected_tree


def test_basic() -> None:
    # setup
    server = supriya.Server().boot()
    # operation
    actual_tree = str(server.query_tree())
    # validation
    expected_tree = textwrap.dedent(
        """\
        NODE TREE 0 group
            1 group
        """
    )
    assert actual_tree == expected_tree
    # teardown (but might not happen if the assert fails)
    server.quit()


def test_exceptions(server: supriya.Server) -> None:
    # if the server is already online,
    # booting again will throw an exception
    with pytest.raises(supriya.exceptions.ServerOnline) as exception_info:
        # the test fails if the exception doesn't raise
        server.boot()
    # and we can assert even more about the raised exception
    # e.g. what the custom message for the exception was
    assert "Server already online!" in str(exception_info.value)


def test_fixtures(
    # note: the server argument name matches the server fixture name exactly
    server: supriya.Server,
) -> None:
    # operation
    actual_tree = str(server.query_tree())
    # validation
    expected_tree = textwrap.dedent(
        """\
        NODE TREE 0 group
            1 group
        """
    )
    assert actual_tree == expected_tree


def test_logging(caplog: pytest.LogCaptureFixture, server: supriya.Server) -> None:
    # capture logs from the supriya.osc.out logger
    # that are at or higher than logging.DEBUG
    caplog.set_level(logging.DEBUG, logger="supriya.osc.out")
    # do something that should emit some osc logging
    server.add_group()
    # validate that the logs are what we expect...
    # ``caplog.record_tuples`` is a list of triples: logger, level, message
    assert caplog.record_tuples == [
        (
            "supriya.osc.out",
            logging.DEBUG,
            f"[127.0.0.1:57110/{server.name}] OscMessage('/g_new', 1000, 0, 1)",
        ),
    ]


def test_node_tree_diff(server: supriya.Server) -> None:
    # capture the tree before
    before_tree = str(server.query_tree())
    # perform an operation
    with server.at():
        for _ in range(5):
            server.add_group()
    # capture the tree after
    after_tree = str(server.query_tree())
    # build a diff of the two trees
    actual_diff = "".join(
        difflib.unified_diff(
            before_tree.splitlines(True),
            after_tree.splitlines(True),
            fromfile="before",
            tofile="after",
        )
    )
    # tidy up the expected diff
    expected_diff = textwrap.dedent(
        """\
        --- before
        +++ after
        @@ -1,2 +1,7 @@
         NODE TREE 0 group
             1 group
        +        1004 group
        +        1003 group
        +        1002 group
        +        1001 group
        +        1000 group
        """
    )
    # validate
    assert actual_diff == expected_diff


@contextlib.asynccontextmanager
async def assert_node_tree_diff(
    context: supriya.AsyncServer | supriya.Server,
    expected_diff: str,
) -> AsyncGenerator[None, None]:
    # capture the tree before
    before_tree = str(await get(context.query_tree()))
    # run the body of the context manager block
    yield
    # capture the tree after
    after_tree = str(await get(context.query_tree()))
    # build a diff of the two trees
    actual_diff = "".join(
        difflib.unified_diff(
            before_tree.splitlines(True),
            after_tree.splitlines(True),
            fromfile="before",
            tofile="after",
        )
    )
    # tidy up the expected diff so we don't need to dedent inside our tests
    expected_diff = textwrap.dedent(expected_diff)
    # validate that they match
    assert actual_diff == expected_diff


@pytest.mark.asyncio
async def test_node_tree_diff_context_manager(
    context: supriya.AsyncServer | supriya.Server,
) -> None:
    # the validation happens once we exit this context manager
    async with assert_node_tree_diff(
        context=context,
        expected_diff="""\
            --- before
            +++ after
            @@ -1,2 +1,7 @@
             NODE TREE 0 group
                 1 group
            +        1004 group
            +        1003 group
            +        1002 group
            +        1001 group
            +        1000 group
        """,
    ):
        # perform an operation
        with context.at():
            for _ in range(5):
                context.add_group()


def test_osc_transcript(server: supriya.Server) -> None:
    # sniff OSC messages going to and coming from the server
    with server.osc_protocol.capture() as transcript:
        # perform an action that will emit OSC messages
        server.add_group()
    # validate that sent messages match what we expect
    assert [entry.message for entry in transcript.filtered(received=False)] == [
        supriya.OscMessage("/g_new", 1000, 0, 1),
    ]


@pytest.mark.parametrize(
    "add_action, expected_diff",
    [
        (
            supriya.AddAction.ADD_TO_HEAD,
            """\
            --- before
            +++ after
            @@ -1,4 +1,5 @@
             NODE TREE 0 group
                 1 group
                     1000 group
            +            1002 group
                         1001 group
            """,
        ),
        (
            supriya.AddAction.ADD_TO_TAIL,
            """\
            --- before
            +++ after
            @@ -2,3 +2,4 @@
                 1 group
                     1000 group
                         1001 group
            +            1002 group
            """,
        ),
        (
            supriya.AddAction.ADD_BEFORE,
            """\
            --- before
            +++ after
            @@ -1,4 +1,5 @@
             NODE TREE 0 group
                 1 group
            +        1002 group
                     1000 group
                         1001 group
            """,
        ),
        (
            supriya.AddAction.ADD_AFTER,
            """\
            --- before
            +++ after
            @@ -2,3 +2,4 @@
                 1 group
                     1000 group
                         1001 group
            +        1002 group
            """,
        ),
        (
            supriya.AddAction.REPLACE,
            """\
            --- before
            +++ after
            @@ -1,4 +1,3 @@
             NODE TREE 0 group
                 1 group
            -        1000 group
            -            1001 group
            +        1002 group
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_parametrized(
    add_action: supriya.AddAction,
    expected_diff: str,
    server: supriya.Server,
) -> None:
    # add a group
    group = server.add_group()
    # make sure the group has a child group
    group.add_group()
    async with assert_node_tree_diff(
        context=server,
        expected_diff=expected_diff,
    ):
        # add another group relative to the first one
        # with the add action varying depending on the scenario
        group.add_group(add_action=add_action)


@pytest.mark.parametrize(
    "add_action, expected_diff",
    [
        (
            supriya.AddAction.ADD_TO_HEAD,
            """\
            --- before
            +++ after
            @@ -1,4 +1,5 @@
             NODE TREE 0 group
                 1 group
                     1000 group
            +            1002 group
                         1001 group
            """,
        ),
        (
            supriya.AddAction.ADD_TO_TAIL,
            """\
            --- before
            +++ after
            @@ -2,3 +2,4 @@
                 1 group
                     1000 group
                         1001 group
            +            1002 group
            """,
        ),
        (
            supriya.AddAction.ADD_BEFORE,
            """\
            --- before
            +++ after
            @@ -1,4 +1,5 @@
             NODE TREE 0 group
                 1 group
            +        1002 group
                     1000 group
                         1001 group
            """,
        ),
        (
            supriya.AddAction.ADD_AFTER,
            """\
            --- before
            +++ after
            @@ -2,3 +2,4 @@
                 1 group
                     1000 group
                         1001 group
            +        1002 group
            """,
        ),
        (
            supriya.AddAction.REPLACE,
            """\
            --- before
            +++ after
            @@ -1,4 +1,3 @@
             NODE TREE 0 group
                 1 group
            -        1000 group
            -            1001 group
            +        1002 group
            """,
        ),
    ],
)
@pytest.mark.asyncio
async def test_parametrized_combinatoric(
    add_action: supriya.AddAction,
    expected_diff: str,
    context: supriya.AsyncServer | supriya.Server,
) -> None:
    # add a group
    group = context.add_group()
    # make sure the group has a child group
    group.add_group()
    async with assert_node_tree_diff(
        context=context,
        expected_diff=expected_diff,
    ):
        # add another group relative to the first one
        # with the add action varying depending on the scenario
        group.add_group(add_action=add_action)


@pytest.mark.parametrize(
    "add_action, expected_diff",
    [
        (
            supriya.AddAction.ADD_TO_HEAD,
            """\
            --- before
            +++ after
            @@ -1,4 +1,5 @@
             NODE TREE 0 group
                 1 group
                     1000 group
            +            1002 group
                         1001 group
            """,
        ),
        (
            supriya.AddAction.ADD_TO_TAIL,
            """\
            --- before
            +++ after
            @@ -2,3 +2,4 @@
                 1 group
                     1000 group
                         1001 group
            +            1002 group
            """,
        ),
        (
            supriya.AddAction.ADD_BEFORE,
            """\
            --- before
            +++ after
            @@ -1,4 +1,5 @@
             NODE TREE 0 group
                 1 group
            +        1002 group
                     1000 group
                         1001 group
            """,
        ),
        (
            supriya.AddAction.ADD_AFTER,
            """\
            --- before
            +++ after
            @@ -2,3 +2,4 @@
                 1 group
                     1000 group
                         1001 group
            +        1002 group
            """,
        ),
        (
            supriya.AddAction.REPLACE,
            """\
            --- before
            +++ after
            @@ -1,4 +1,3 @@
             NODE TREE 0 group
                 1 group
            -        1000 group
            -            1001 group
            +        1002 group
            """,
        ),
    ],
)
@pytest.mark.parametrize("context_", [lf("async_server"), lf("server")])
@pytest.mark.asyncio
async def test_parametrized_lazy_fixtures(
    add_action: supriya.AddAction,
    expected_diff: str,
    # we use a slightly different name so as to not shadow the context fixture
    # otherwise pytest will complain:
    context_: supriya.AsyncServer | supriya.Server,
) -> None:
    # add a group
    group = context_.add_group()
    # make sure the group has a child group
    group.add_group()
    async with assert_node_tree_diff(
        context=context_,
        expected_diff=expected_diff,
    ):
        # add another group relative to the first one
        # with the add action varying depending on the scenario
        group.add_group(add_action=add_action)


def test_process_transcript(server: supriya.Server) -> None:
    for _ in range(5):
        server.add_group()
    with server.process_protocol.capture() as transcript:
        # tell the server to "trace" the default group
        server.default_group.trace()
        # the trace has no end-delimiter so we don't know explicitly when to
        # stop capturing the output, so we'll just sleep and hope for the best:
        time.sleep(0.1)
    assert transcript.lines == [
        "TRACE Group 1",
        "   1004 group",
        "   1003 group",
        "   1002 group",
        "   1001 group",
        "   1000 group",
    ]


def test_try_finally() -> None:
    # setup
    server = supriya.Server().boot()
    # ugly!
    try:
        # operation
        actual_tree = str(server.query_tree())
        # validation
        expected_tree = textwrap.dedent(
            """\
            NODE TREE 0 group
                1 group
            """
        )
        assert actual_tree == expected_tree
    finally:
        # teardown (even if the assert fails)
        server.quit()


def test_warnings(server: supriya.Server) -> None:
    # let's create a client-side reference to a group that doesn't exist on the
    # server
    nonexistent_group = supriya.Group(context=server, id_=666)
    # capture warnings
    with warnings.catch_warnings(record=True) as warnings_:
        # operation: try to free a group that doesn't exist
        nonexistent_group.free()
        # wait for the server, because the warning arrives asynchronously
        server.sync()
    # validation
    assert len(warnings_) == 1
    assert str(warnings_[0].message) == "/n_free Node 666 not found"
