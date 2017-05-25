# -*- encoding: utf-8 -*-
import jinja2
import pathlib
import shutil
import sys
from abjad.tools import stringtools
from abjad.tools import systemtools
from supriya.tools import commandlinetools
from supriya.tools import soundfiletools


class ProjectPackageScriptTestCase(systemtools.TestCase):

    package_name = 'test_project'
    test_path = pathlib.Path(__file__).parent
    outer_project_path = test_path.joinpath(package_name)
    inner_project_path = outer_project_path.joinpath(package_name)
    assets_path = inner_project_path.joinpath('assets')
    composites_path = inner_project_path.joinpath('composites')
    distribution_path = inner_project_path.joinpath('distribution')
    materials_path = inner_project_path.joinpath('materials')
    renders_path = inner_project_path.joinpath('renders')
    synthdefs_path = inner_project_path.joinpath('synthdefs')
    tools_path = inner_project_path.joinpath('tools')

    basic_session_template = jinja2.Template(stringtools.normalize('''
    # -*- encoding: utf-8 -*-
    import supriya
    from test_project import project_settings


    {{ output_section_singular }} = supriya.Session.from_project_settings(project_settings)

    with supriya.synthdeftools.SynthDefBuilder(
        duration=1.,
        out_bus=0,
        ) as builder:
        source = supriya.ugentools.Line.ar(
            duration=builder['duration'],
            ) * {{ multiplier | default(1.0) }}
        supriya.ugentools.Out.ar(
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

    chained_session_template = jinja2.Template(stringtools.normalize('''
    # -*- encoding: utf-8 -*-
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
        source = supriya.ugentools.In.ar(
            bus=builder['in_bus'],
            channel_count=len({{ output_section_singular }}.audio_output_bus_group),
            )
        supriya.ugentools.ReplaceOut.ar(
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
        for path in sorted(self.test_path.iterdir()):
            if path in self.directory_items:
                continue
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(str(path))
        sys.path.remove(str(self.outer_project_path))
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
        script = commandlinetools.ManageMaterialScript()
        command = ['--new', material_name]
        if force:
            command.insert(0, '-f')
        with systemtools.TemporaryDirectoryChange(str(self.inner_project_path)):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        material_path = self.inner_project_path / 'materials' / material_name
        if definition_contents:
            definition_contents = stringtools.normalize(definition_contents)
            definition_file_path = material_path / 'definition.py'
            with open(str(definition_file_path), 'w') as file_pointer:
                file_pointer.write(definition_contents)
        return material_path

    def create_project(self, force=False, expect_error=False):
        script = commandlinetools.ManageProjectScript()
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
        with systemtools.TemporaryDirectoryChange(str(self.test_path)):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')

    def sample(self, file_path, rounding=6):
        soundfile = soundfiletools.SoundFile(file_path)
        return {
            0.0: [round(x, rounding) for x in soundfile.at_percent(0)],
            0.21: [round(x, rounding) for x in soundfile.at_percent(0.21)],
            0.41: [round(x, rounding) for x in soundfile.at_percent(0.41)],
            0.61: [round(x, rounding) for x in soundfile.at_percent(0.61)],
            0.81: [round(x, rounding) for x in soundfile.at_percent(0.81)],
            0.99: [round(x, rounding) for x in soundfile.at_percent(0.99)],
            }
