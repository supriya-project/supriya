import doctest
import pathlib
import re
import shutil
import sys
import types

import jinja2
import pytest
from uqbar.io import DirectoryChange
from uqbar.strings import normalize

from supriya.cli import (
    ManageMaterialScript,
    ManageProjectScript,
    ManageSessionScript,
)


@pytest.fixture
def cli_paths(tmpdir):
    package_name = "test_project"
    test_directory_path = pathlib.Path(tmpdir)
    outer_project_path = test_directory_path.joinpath(package_name)
    inner_project_path = outer_project_path.joinpath(package_name)
    cli_paths = types.SimpleNamespace(
        test_directory_path=test_directory_path,
        outer_project_path=outer_project_path,
        inner_project_path=inner_project_path,
        assets_path=inner_project_path.joinpath("assets"),
        sessions_path=inner_project_path.joinpath("sessions"),
        distribution_path=inner_project_path.joinpath("distribution"),
        materials_path=inner_project_path.joinpath("materials"),
        renders_path=inner_project_path.joinpath("renders"),
        synthdefs_path=inner_project_path.joinpath("synthdefs"),
        tools_path=inner_project_path.joinpath("tools"),
    )
    if outer_project_path.exists():
        shutil.rmtree(outer_project_path)
    if sys.path[0] != str(outer_project_path):
        sys.path.insert(0, str(outer_project_path))
    yield cli_paths
    for module_path, module in tuple(sys.modules.items()):
        if not module_path or not module:
            continue
        if module_path.startswith(package_name):
            del sys.modules[module_path]


@pytest.helpers.register
def compare_path_contents(path_to_search, expected_files, test_path):
    actual_files = sorted(
        str(path.relative_to(test_path))
        for path in sorted(path_to_search.glob("**/*.*"))
        if "__pycache__" not in path.parts and path.suffix != ".pyc"
    )
    pytest.helpers.compare_strings(
        "\n".join(str(_) for _ in actual_files),
        "\n".join(str(_) for _ in expected_files),
    )


@pytest.helpers.register
def compare_strings(expected, actual):
    ansi_escape = re.compile(r"\x1b[^m]*m")
    actual = normalize(ansi_escape.sub("", actual))
    expected = normalize(ansi_escape.sub("", expected))
    example = types.SimpleNamespace()
    example.want = expected
    output_checker = doctest.OutputChecker()
    flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.REPORT_NDIFF
    success = output_checker.check_output(expected, actual, flags)
    if not success:
        diff = output_checker.output_difference(example, actual, flags)
        raise Exception(diff)


@pytest.helpers.register
def create_cli_material(
    test_directory_path,
    material_name="test_material",
    force=False,
    expect_error=False,
    definition_contents=None,
):
    test_directory_path = pathlib.Path(test_directory_path)
    inner_project_path = test_directory_path / "test_project" / "test_project"
    script = ManageMaterialScript()
    command = ["--new", material_name]
    if force:
        command.insert(0, "-f")
    with DirectoryChange(str(inner_project_path)):
        if expect_error:
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
        else:
            try:
                script(command)
            except SystemExit as exception:
                if exception.args[0]:
                    raise RuntimeError("SystemExit")
    material_path = inner_project_path / "materials" / material_name
    if definition_contents:
        definition_contents = normalize(definition_contents)
        definition_file_path = material_path / "definition.py"
        with open(str(definition_file_path), "w") as file_pointer:
            file_pointer.write(definition_contents)
    return material_path


@pytest.helpers.register
def create_cli_project(test_directory_path, force=False, expect_error=False):
    test_directory_path = pathlib.Path(test_directory_path)
    script = ManageProjectScript()
    command = [
        "--new",
        "Test Project",
        "--composer-name",
        "Josiah Wolf Oberholtzer",
        "--composer-email",
        "josiah.oberholtzer@gmail.com",
        "--composer-github",
        "josiah-wolf-oberholtzer",
        "--composer-website",
        "www.josiahwolfoberholtzer.com",
        "--composer-library",
        "amazing_library",
    ]
    if force:
        command.insert(0, "-f")
    with DirectoryChange(str(test_directory_path)):
        if expect_error:
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
        else:
            try:
                script(command)
            except SystemExit as exception:
                if exception.args[0]:
                    raise RuntimeError("SystemExit")


@pytest.helpers.register
def create_cli_session(
    test_directory_path,
    session_name="test_session",
    force=False,
    expect_error=False,
    definition_contents=None,
):
    test_directory_path = pathlib.Path(test_directory_path)
    inner_project_path = test_directory_path / "test_project" / "test_project"
    script = ManageSessionScript()
    command = ["--new", session_name]
    if force:
        command.insert(0, "-f")
    with DirectoryChange(str(inner_project_path)):
        if expect_error:
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
        else:
            try:
                script(command)
            except SystemExit as exception:
                if exception.args[0]:
                    raise RuntimeError("SystemExit")
    session_path = inner_project_path / "sessions" / session_name
    if definition_contents:
        definition_contents = normalize(definition_contents)
        definition_file_path = session_path / "definition.py"
        with open(str(definition_file_path), "w") as file_pointer:
            file_pointer.write(definition_contents)
    return session_path


@pytest.helpers.register
def get_basic_session_template():
    return jinja2.Template(
        normalize(
            r"""
    import supriya
    from test_project import project_settings


    {{ output_section_singular }} = supriya.Session.from_project_settings(project_settings)

    with supriya.synthdefs.SynthDefBuilder(
        duration=1.,
        out_bus=0,
        ) as builder:
        source = supriya.ugens.Line.ar(
            duration=builder['duration'],
            ) * {{ multiplier | default(1.0) }}
        supriya.ugens.Out.ar(
            bus=builder['out_bus'],
            source=[source] * len({{ output_section_singular }}.audio_output_bus_group),
            )
    ramp_synthdef = builder.build()

    with {{ output_section_singular }}.at(0):
        {{ output_section_singular }}.add_synth(
            duration=1,
            synthdef=ramp_synthdef,
            )
    """
        )
    )


@pytest.helpers.register
def get_session_factory_template():
    return jinja2.Template(
        normalize(
            r"""
    import supriya
    from test_project import project_settings


    class SessionFactory:

        def __init__(self, project_settings):
            self.project_settings = project_settings

        def _build_ramp_synthdef(self):
            server_options = self.project_settings['server_options']
            channel_count = server_options['output_bus_channel_count']
            with supriya.synthdefs.SynthDefBuilder(
                duration=1.,
                out_bus=0,
                ) as builder:
                source = supriya.ugens.Line.ar(
                    duration=builder['duration'],
                    ) * {{ multiplier | default(1.0) }}
                supriya.ugens.Out.ar(
                    bus=builder['out_bus'],
                    source=[source] * channel_count,
                    )
            ramp_synthdef = builder.build()
            return ramp_synthdef

        def __session__(self):
            session = supriya.Session.from_project_settings(self.project_settings)
            ramp_synthdef = self._build_ramp_synthdef()
            with session.at(0):
                session.add_synth(
                    duration=1,
                    synthdef=ramp_synthdef,
                    )
            return session


    {{ output_section_singular }} = SessionFactory(project_settings)
    """
        )
    )


@pytest.helpers.register
def get_chained_session_template():
    return jinja2.Template(
        normalize(
            r"""
    import supriya
    from test_project import project_settings
    from test_project.{{ input_section_singular }}s.{{ input_name }}.definition \
        import {{ input_section_singular }} as {{ input_name }}


    {{ output_section_singular }} = supriya.Session.from_project_settings(
        project_settings,
        input_={{ input_name }},
        )

    with supriya.SynthDefBuilder(
        in_bus=0,
        out_bus=0,
        multiplier=1,
        ) as builder:
        source = supriya.ugens.In.ar(
            bus=builder['in_bus'],
            channel_count=len({{ output_section_singular }}.audio_output_bus_group),
            )
        supriya.ugens.ReplaceOut.ar(
            bus=builder['out_bus'],
            source=source * builder['multiplier'],
            )
    multiplier_synthdef = builder.build()

    with {{ output_section_singular }}.at(0):
        {{ output_section_singular }}.add_synth(
            duration=1,
            in_bus={{ output_section_singular }}.audio_input_bus_group,
            multiplier={{ multiplier }},
            synthdef=multiplier_synthdef,
            )
    """
        )
    )
