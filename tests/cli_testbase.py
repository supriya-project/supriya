import jinja2
import pathlib
import pytest
import shutil
import supriya.cli
import supriya.soundfiles
import supriya.system
import sys
import uqbar.io
import uqbar.strings


class ProjectPackageScriptTestCase(supriya.system.TestCase):

    package_name = 'test_project'
    test_path = pathlib.Path(__file__).parent
    outer_project_path = test_path.joinpath(package_name)
    inner_project_path = outer_project_path.joinpath(package_name)
    assets_path = inner_project_path.joinpath('assets')
    sessions_path = inner_project_path.joinpath('sessions')
    distribution_path = inner_project_path.joinpath('distribution')
    materials_path = inner_project_path.joinpath('materials')
    renders_path = inner_project_path.joinpath('renders')
    synthdefs_path = inner_project_path.joinpath('synthdefs')
    tools_path = inner_project_path.joinpath('tools')

    basic_session_template = jinja2.Template(uqbar.strings.normalize('''
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
    '''))

    session_factory_template = jinja2.Template(uqbar.strings.normalize('''
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
    '''))

    chained_session_template = jinja2.Template(uqbar.strings.normalize('''
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
    '''))

    ### TEST LIFECYCLE ###

    def setUp(self):
        super(ProjectPackageScriptTestCase, self).setUp()
        if self.outer_project_path.exists():
            shutil.rmtree(str(self.outer_project_path))
        self.directory_items = set(self.test_path.iterdir())
        sys.path.insert(0, str(self.outer_project_path))

    def tearDown(self):
        super(ProjectPackageScriptTestCase, self).tearDown()
#        for path in sorted(self.test_path.iterdir()):
#            if path in self.directory_items:
#                continue
#            if path.is_file():
#                path.unlink()
#            else:
#                shutil.rmtree(str(path))
#        sys.path.remove(str(self.outer_project_path))
        for path, module in tuple(sys.modules.items()):
            if not path or not module:
                continue
            if path.startswith(self.package_name):
                del(sys.modules[path])

    ### UTILITY METHODS ###

    def create_material(
        self,
        material_name='test_material',
        force=False,
        expect_error=False,
        definition_contents=None,
        ):
        script = supriya.cli.ManageMaterialScript()
        command = ['--new', material_name]
        if force:
            command.insert(0, '-f')
        with uqbar.io.DirectoryChange(str(self.inner_project_path)):
            if expect_error:
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        material_path = self.inner_project_path / 'materials' / material_name
        if definition_contents:
            definition_contents = uqbar.strings.normalize(definition_contents)
            definition_file_path = material_path / 'definition.py'
            with open(str(definition_file_path), 'w') as file_pointer:
                file_pointer.write(definition_contents)
        return material_path

    def create_project(self, force=False, expect_error=False):
        script = supriya.cli.ManageProjectScript()
        command = [
            '--new',
            'Test Project',
            '--composer-name', 'Josiah Wolf Oberholtzer',
            '--composer-email', 'josiah.oberholtzer@gmail.com',
            '--composer-github', 'josiah-wolf-oberholtzer',
            '--composer-website', 'www.josiahwolfoberholtzer.com',
            '--composer-library', 'amazing_library',
            ]
        if force:
            command.insert(0, '-f')
        with uqbar.io.DirectoryChange(str(self.test_path)):
            if expect_error:
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')

    def create_session(
        self,
        session_name='test_session',
        force=False,
        expect_error=False,
        definition_contents=None,
        ):
        script = supriya.cli.ManageSessionScript()
        command = ['--new', session_name]
        if force:
            command.insert(0, '-f')
        with uqbar.io.DirectoryChange(str(self.inner_project_path)):
            if expect_error:
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        session_path = self.inner_project_path / 'sessions' / session_name
        if definition_contents:
            definition_contents = uqbar.strings.normalize(definition_contents)
            definition_file_path = session_path / 'definition.py'
            with open(str(definition_file_path), 'w') as file_pointer:
                file_pointer.write(definition_contents)
        return session_path
