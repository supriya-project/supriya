# -*- encoding: utf-8 -*-
import collections
import inspect
import os
import sys
import traceback
from abjad.tools import systemtools
from supriya.tools.commandlinetools.ProjectPackageScript import (
    ProjectPackageScript
)
from supriya.tools.nonrealtimetools import (
    NonrealtimeRenderError,
    NonrealtimeOutputMissing,
)


class ManageMaterialScript(ProjectPackageScript):
    '''
    Manages project package materials.

    ..  shell::

        spv material --help

    '''

    ### CLASS VARIABLES ###

    alias = 'material'
    short_description = 'manage project package materials'

    ### PRIVATE METHODS ###

    def _handle_copy(
        self,
        source_material_name,
        target_material_name,
        force=False,
        ):
        self._copy_package(
            source_material_name,
            target_material_name,
            'materials',
            force=force,
            )

    def _handle_delete(self, material_name):
        self._remove_package(material_name, 'materials')

    def _handle_edit(self, material_names):
        self._edit_packages(material_names, 'materials')

    def _handle_list(self):
        from abjad.tools.abctools import (
            AbjadObject, AbjadValueObject,
        )
        from supriya.tools.systemtools import (
            SupriyaObject, SupriyaValueObject,
        )
        basic_bases = (
            AbjadObject,
            AbjadValueObject,
            SupriyaObject,
            SupriyaValueObject,
            object,
            )
        print('Available materials:')
        all_materials = self._import_all_materials(verbose=False)
        if not all_materials:
            print('    No materials available.')
            sys.exit(1)
        materials = {}
        for material_name, material in all_materials.items():
            class_ = type(material)
            base = class_.__bases__[0]
            attrs = {attr.name: attr for attr in
                inspect.classify_class_attrs(class_)}
            if any(_ in class_.__bases__ for _ in basic_bases):
                base = class_
            elif getattr(class_, '__is_terminal_ajv_list_item__', False) and \
                attrs['__is_terminal_ajv_list_item__'].defining_class is class_:
                base = class_
            materials.setdefault(base, []).append((material_name, class_))
        materials = sorted(materials.items(), key=lambda pair: pair[0].__name__)
        for base, material_names in materials:
            print('    {}:'.format(base.__name__))
            for material_name, class_ in material_names:
                print('        {} [{}]'.format(material_name, class_.__name__))
        sys.exit(1)

    def _handle_new(self, material_name, force=False):
        self._create_package_from_template(
            package_name=material_name,
            section='materials',
            force=force,
            )

    def _handle_rename(
        self,
        source_material_name,
        target_material_name,
        force=False,
        ):
        self._rename_package(
            source_material_name,
            target_material_name,
            'materials',
            force=force,
            )

    def _handle_render(self, material_names, force=False):
        globbable_names = self._collect_globbable_names(material_names)
        print('Render candidates: {!r} ...'.format(
            ' '.join(globbable_names)))
        matching_paths = self._collect_matching_paths(
            globbable_names, 'materials')
        if not matching_paths:
            print('    No matching materials.')
            self._handle_list()
            sys.exit(1)
        for path in matching_paths:
            self._render_one_material(
                material_directory_path=path
                )
            print('    Rendered {path!s}{sep}'.format(
                path=path.relative_to(self.inner_project_path.parent),
                sep=os.path.sep))

    def _import_all_materials(self, verbose=True):
        materials = collections.OrderedDict()
        for path in self._list_material_subpackages():
            name = path.name
            material = self._import_material(path, verbose=verbose)
            materials[name] = material
        return materials

    def _import_material(self, material_directory_path, verbose=True):
        material_import_path = self._path_to_packagesystem_path(
            material_directory_path)
        material_name = material_directory_path.name
        definition_import_path = material_import_path + '.definition'
        try:
            module = self._import_path(
                definition_import_path,
                self.outer_project_path,
                verbose=verbose,
                )
            material = getattr(module, material_name)
        except (ImportError, AttributeError):
            print(traceback.format_exc())
            sys.exit(1)
        return material

    def _list_material_subpackages(self, project_path=None):
        return self._list_subpackages('materials', project_path=project_path)

    def _process_args_inner(self, args):
        if args.new is not None:
            self._handle_new(
                force=args.force,
                material_name=args.new,
                )
        if args.edit is not None:
            self._handle_edit(
                material_names=args.edit,
                )
        if args.render is not None:
            self._handle_render(
                force=args.force,
                material_names=args.render,
                )
        if args.list_:
            self._handle_list()
        if args.copy is not None:
            self._handle_copy(
                source_material_name=args.copy[0],
                target_material_name=args.copy[1],
                force=args.force,
                )
        if args.rename is not None:
            self._handle_rename(
                source_material_name=args.rename[0],
                target_material_name=args.rename[1],
                force=args.force,
                )
        if args.delete is not None:
            self._handle_delete(
                material_name=args.delete,
                )

    def _render_one_material(self, material_directory_path):
        from supriya import render
        from supriya.tools import nonrealtimetools
        print('Rendering {path!s}{sep}'.format(
            path=material_directory_path.relative_to(
                self.inner_project_path.parent),
            sep=os.path.sep))
        output_file_path = material_directory_path / 'render.aiff'
        with systemtools.Timer() as timer:
            material = self._import_material(material_directory_path)
            if not hasattr(material, '__render__'):
                template = '    Cannot render material of type {}.'
                message = template.format(type(material).__name__)
                print(message)
                sys.exit(1)

            kwargs = {}
            if isinstance(material, nonrealtimetools.Session):
                kwargs.update(self._build_nrt_server_options(material))
                kwargs.update({
                    'print_transcript': True,
                    'transcript_prefix': '    ',
                    'build_render_yml': True,
                    })

            try:
                render(
                    material,
                    output_file_path=output_file_path,
                    render_directory_path=self._renders_path,
                    **kwargs
                    )
            except (NonrealtimeRenderError, NonrealtimeOutputMissing):
                self._report_time(timer, prefix='Python/SC runtime')
                print('    Render failed. Exiting.')
                sys.exit(1)
            except:
                print(traceback.format_exc())
                sys.exit(1)

            self._report_time(timer, prefix='Python/SC runtime')

    def _build_nrt_server_options(self, session):
        from supriya.tools import commandlinetools
        project_settings = commandlinetools.ProjectSettings(
            yaml_path=self.inner_project_path.joinpath(
                'project-settings.yml'),
            )
        server_options = project_settings.get('server_options', {})
        server_options.update(
            input_bus_channel_count=session.input_bus_channel_count,
            output_bus_channel_count=session.output_bus_channel_count,
            )
        for key, value in tuple(server_options.items()):
            if value is None:
                server_options.pop(key)
        return server_options

    def _setup_argument_parser(self, parser):
        action_group = parser.add_argument_group('actions')
        action_group = action_group.add_mutually_exclusive_group(
            required=True)
        action_group.add_argument(
            '--new', '-N',
            help='create a new material',
            metavar='NAME',
            )
        action_group.add_argument(
            '--edit', '-E',
            help='edit materials',
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--render', '-R',
            help='render materials',
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--list', '-L',
            dest='list_',
            help='list materials',
            action='store_true',
            )
        action_group.add_argument(
            '--copy', '-Y',
            help='copy material',
            metavar=('SOURCE', 'TARGET'),
            nargs=2,
            )
        action_group.add_argument(
            '--rename', '-M',
            help='rename material',
            metavar=('SOURCE', 'TARGET'),
            nargs=2,
            )
        action_group.add_argument(
            '--delete', '-D',
            help='delete material',
            metavar='NAME',
            )
        common_group = parser.add_argument_group('common options')
        common_group.add_argument(
            '--force', '-f',
            action='store_true',
            help='force overwriting',
            )
        common_group.add_argument(
            '--project-path',
            metavar='project',
            help='project path or package name',
            default=os.path.curdir,
            )
        common_group.add_argument(
            '--profile',
            action='store_true',
            help='display profiler info',
            )
