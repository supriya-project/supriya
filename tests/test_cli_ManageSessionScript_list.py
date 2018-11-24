import io

import pytest
import uqbar.io

import supriya.cli


def test_list_sessions(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    pytest.helpers.create_cli_session(cli_paths.test_directory_path, "foo")
    pytest.helpers.create_cli_session(cli_paths.test_directory_path, "bar")
    pytest.helpers.create_cli_session(cli_paths.test_directory_path, "baz")
    pytest.helpers.create_cli_session(cli_paths.test_directory_path, "quux")
    script = supriya.cli.ManageSessionScript()
    command = ["--list"]
    with uqbar.io.RedirectedStreams(stdout=string_io), uqbar.io.DirectoryChange(
        cli_paths.inner_project_path
    ), pytest.raises(SystemExit) as exception_info:
        script(command)
    assert exception_info.value.code == 1
    pytest.helpers.compare_strings(
        r"""
        Available sessions:
            Session:
                bar [Session]
                baz [Session]
                foo [Session]
                quux [Session]
        """,
        string_io.getvalue(),
    )


def test_list_sessions_no_sessions(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    script = supriya.cli.ManageSessionScript()
    command = ["--list"]
    with uqbar.io.RedirectedStreams(stdout=string_io), uqbar.io.DirectoryChange(
        cli_paths.inner_project_path
    ), pytest.raises(SystemExit) as exception_info:
        script(command)
    assert exception_info.value.code == 1
    pytest.helpers.compare_strings(
        r"""
        Available sessions:
            No sessions available.
        """,
        string_io.getvalue(),
    )
