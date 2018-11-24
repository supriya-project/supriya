import io
import pytest
import supriya.cli
import uqbar.io
import unittest.mock


def test_success(cli_paths):
    string_io = io.StringIO()
    pytest.helpers.create_cli_project(cli_paths.test_directory_path)
    material_path = pytest.helpers.create_cli_material(
        cli_paths.test_directory_path, "test_material"
    )
    script = supriya.cli.ManageMaterialScript()
    command = ["--edit", "test_material"]
    mock_path = "supriya.cli.ProjectPackageScript._call_subprocess"
    with unittest.mock.patch(mock_path) as mock:
        mock.return_value = 0
        with uqbar.io.RedirectedStreams(stdout=string_io), uqbar.io.DirectoryChange(
            cli_paths.inner_project_path
        ):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError("SystemExit: {}".format(e.code))
    pytest.helpers.compare_strings(
        r"""
        Edit candidates: 'test_material' ...
        """,
        string_io.getvalue(),
    )
    definition_path = material_path.joinpath("definition.py")
    command = "{} {!s}".format(
        supriya.config.get("core", "editor", fallback="vim"), definition_path
    )
    mock.assert_called_with(command)
